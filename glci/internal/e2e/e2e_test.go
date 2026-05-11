// Package e2e spawns the compiled `glci` binary against an in-process stub
// WordPress server (httptest) to exercise the user-visible CLI surface end
// to end. Post-P8 #11.
//
// Skipped if `go` is not on PATH (build hosts without a Go toolchain).
package e2e_test

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"sync/atomic"
	"testing"
)

// glciBin is the absolute path to the compiled binary, populated by TestMain.
var glciBin string

func TestMain(m *testing.M) {
	goBin, err := exec.LookPath("go")
	if err != nil {
		// No go toolchain — skip everything cleanly.
		fmt.Fprintln(os.Stderr, "e2e: skipping (no `go` on PATH)")
		os.Exit(0)
	}

	// Locate the glci module root (two levels up from this _test.go file).
	_, thisFile, _, _ := runtime.Caller(0)
	moduleRoot, err := filepath.Abs(filepath.Join(filepath.Dir(thisFile), "..", ".."))
	if err != nil {
		fmt.Fprintln(os.Stderr, "e2e: cannot resolve module root:", err)
		os.Exit(1)
	}

	tmp, err := os.MkdirTemp("", "glci-e2e-*")
	if err != nil {
		fmt.Fprintln(os.Stderr, "e2e: mkdtemp:", err)
		os.Exit(1)
	}
	defer os.RemoveAll(tmp)

	binName := "glci"
	if runtime.GOOS == "windows" {
		binName += ".exe"
	}
	glciBin = filepath.Join(tmp, binName)

	build := exec.Command(goBin, "build", "-o", glciBin, ".")
	build.Dir = moduleRoot
	build.Stderr = os.Stderr
	if err := build.Run(); err != nil {
		fmt.Fprintln(os.Stderr, "e2e: go build failed:", err)
		os.Exit(1)
	}

	os.Exit(m.Run())
}

// runGLCI invokes the compiled binary with args and captures (stdout, stderr, exitCode).
func runGLCI(t *testing.T, args ...string) (string, string, int) {
	t.Helper()
	cmd := exec.Command(glciBin, args...)
	var stdout, stderr strings.Builder
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err := cmd.Run()
	code := 0
	if err != nil {
		if ee, ok := err.(*exec.ExitError); ok {
			code = ee.ExitCode()
		} else {
			t.Fatalf("exec %s %v: %v", glciBin, args, err)
		}
	}
	return stdout.String(), stderr.String(), code
}

// stubServer builds a minimal Git Logs plugin look-alike for E2E.
type stubServer struct {
	*httptest.Server
	HealthHits int32
	WhoamiHits int32
	AppendHits int32
}

func newStubServer(t *testing.T) *stubServer {
	t.Helper()
	s := &stubServer{}
	mux := http.NewServeMux()

	mux.HandleFunc("/wp-json/git-logs/v1/health", func(w http.ResponseWriter, _ *http.Request) {
		atomic.AddInt32(&s.HealthHits, 1)
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"status":"ok","plugin_version":"1.0.0-stub"}`))
	})

	mux.HandleFunc("/wp-json/git-logs/v1/whoami", func(w http.ResponseWriter, r *http.Request) {
		atomic.AddInt32(&s.WhoamiHits, 1)
		auth := r.Header.Get("Authorization")
		hasSig := r.Header.Get("X-GL-Signature") != ""
		if auth == "" && !hasSig {
			w.WriteHeader(http.StatusUnauthorized)
			_, _ = w.Write([]byte(`{"code":"GL-AUTH-MISSING"}`))
			return
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"user_login":"alice","auth_lane":"wp_session","capabilities":["edit_posts"]}`))
	})

	mux.HandleFunc("/append-log", func(w http.ResponseWriter, r *http.Request) {
		atomic.AddInt32(&s.AppendHits, 1)
		var body map[string]any
		_ = json.NewDecoder(r.Body).Decode(&body)
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"Accepted":true,"RunId":"stub-run-1"}`))
	})

	s.Server = httptest.NewServer(mux)
	t.Cleanup(s.Close)
	return s
}

func TestE2E_VersionAndHelp(t *testing.T) {
	stdout, _, code := runGLCI(t, "version")
	if code != 0 {
		t.Fatalf("version: exit %d", code)
	}
	if !strings.HasPrefix(stdout, "glci ") {
		t.Errorf("version: unexpected stdout: %q", stdout)
	}

	stdout, _, code = runGLCI(t, "help")
	if code != 0 {
		t.Fatalf("help: exit %d", code)
	}
	for _, want := range []string{"detect", "lint", "build", "test", "ping", "whoami"} {
		if !strings.Contains(stdout, want) {
			t.Errorf("help: missing %q in usage output", want)
		}
	}
}

func TestE2E_UnknownCommand(t *testing.T) {
	_, stderr, code := runGLCI(t, "doesnotexist")
	if code == 0 {
		t.Fatalf("expected non-zero exit for unknown command")
	}
	if !strings.Contains(stderr, "unknown command") {
		t.Errorf("stderr missing 'unknown command': %q", stderr)
	}
}

func TestE2E_PingAgainstStub(t *testing.T) {
	srv := newStubServer(t)
	stdout, stderr, code := runGLCI(t, "ping", "--base", srv.URL)
	if code != 0 {
		t.Fatalf("ping: exit %d, stderr=%q", code, stderr)
	}
	if !strings.Contains(stdout, `"status"`) || !strings.Contains(stdout, "ok") {
		t.Errorf("ping: missing health JSON: %q", stdout)
	}
	if atomic.LoadInt32(&srv.HealthHits) != 1 {
		t.Errorf("ping: stub /health hit count = %d, want 1", srv.HealthHits)
	}
}

func TestE2E_PingFailsOnHTTPError(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/wp-json/git-logs/v1/health", func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = w.Write([]byte(`{"code":"boom"}`))
	})
	srv := httptest.NewServer(mux)
	defer srv.Close()

	_, stderr, code := runGLCI(t, "ping", "--base", srv.URL)
	if code == 0 {
		t.Fatal("expected non-zero exit for 500")
	}
	if !strings.Contains(stderr, "HTTP 500") {
		t.Errorf("stderr missing HTTP 500: %q", stderr)
	}
}

func TestE2E_WhoamiAppPasswordLane(t *testing.T) {
	srv := newStubServer(t)
	stdout, stderr, code := runGLCI(t, "whoami",
		"--base", srv.URL,
		"--user", "alice",
		"--app-password", "abcd EFGH ijkl MNOP qrst UVWX",
	)
	if code != 0 {
		t.Fatalf("whoami: exit %d, stderr=%q", code, stderr)
	}
	if !strings.Contains(stdout, `"alice"`) {
		t.Errorf("whoami: missing alice in output: %q", stdout)
	}
}

func TestE2E_WhoamiMissingAuthFails(t *testing.T) {
	srv := newStubServer(t)
	_, stderr, code := runGLCI(t, "whoami", "--base", srv.URL)
	if code == 0 {
		t.Fatal("expected error when no auth provided")
	}
	if !strings.Contains(stderr, "glci:") {
		t.Errorf("stderr should be prefixed with glci:, got %q", stderr)
	}
}

func TestE2E_SelfTestPasses(t *testing.T) {
	stdout, stderr, code := runGLCI(t, "--self-test")
	if code != 0 {
		t.Fatalf("--self-test: exit %d\nstdout=%s\nstderr=%s", code, stdout, stderr)
	}
}
