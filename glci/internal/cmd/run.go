package cmd

import (
	"context"
	"flag"
	"fmt"
	"os"
	"regexp"
	"sort"
	"strings"

	"github.com/example/glci/internal/auth"
	"github.com/example/glci/internal/ci"
	"github.com/example/glci/internal/classify"
	"github.com/example/glci/internal/config"
	"github.com/example/glci/internal/detect"
	"github.com/example/glci/internal/redact"
	"github.com/example/glci/internal/runner"
	"github.com/example/glci/internal/selftest"
	"github.com/example/glci/internal/ship"
	"github.com/example/glci/internal/stream"
)

// Detect implements `glci detect`.
func Detect(args []string) error {
	fs := flag.NewFlagSet("detect", flag.ContinueOnError)
	cwd := fs.String("cwd", ".", "Project root for detection")
	jsonOut := fs.Bool("json", false, "Emit deterministic JSON")
	if err := fs.Parse(args); err != nil {
		return exitErr(64, err)
	}
	r, derr := detect.Detect(*cwd)
	if derr != nil {
		// Still emit JSON so consumers can parse Skipped[].
		if *jsonOut && r != nil {
			b, _ := r.JSON()
			fmt.Println(string(b))
		} else {
			fmt.Fprintln(os.Stderr, derr.Error())
		}
		return exitErr(2, derr)
	}
	if *jsonOut {
		b, _ := r.JSON()
		fmt.Println(string(b))
		return nil
	}
	fmt.Printf("cwd: %s\n", r.Cwd)
	for _, rt := range r.Runtimes {
		fmt.Printf("runtime: %s", rt.ID)
		if rt.Manager != "" {
			fmt.Printf(" (%s)", rt.Manager)
		}
		fmt.Println()
		for _, p := range rt.Phases {
			fmt.Printf("  %-5s  %s %s\n", p.Phase, p.Runner, strings.Join(p.Args, " "))
		}
	}
	for _, sk := range r.Skipped {
		fmt.Printf("skipped: %s (%s)\n", sk.ID, sk.Reason)
	}
	return nil
}

// Run implements `glci run` (and lint/build/test single-phase variants).
func RunCmd(args []string, only string) error {
	fs := flag.NewFlagSet("run", flag.ContinueOnError)
	cwd := fs.String("cwd", ".", "Project root")
	cfgPath := fs.String("config", "", "Config file path")
	server := fs.String("server", "", "Server URL override")
	tempToken := fs.String("temp-token", "", "Lane B TempToken")
	tok := fs.String("token", "", "Lane B Token")
	authMode := fs.String("auth-mode", "", "temptoken | ssh")
	repoURL := fs.String("repo-url", "", "Override RepoUrl")
	branch := fs.String("branch", "", "Override Branch")
	gitSha := fs.String("git-sha", "", "Override GitSha256")
	noPush := fs.Bool("no-push", false, "Run locally; never POST")
	keepGoing := fs.Bool("keep-going", false, "Run all phases even if one fails")
	runtimeFilter := fs.String("runtime", "", "Restrict to one runtime")
	phasesCSV := fs.String("phases", "", "CSV subset (default lint,build,test)")
	jsonOut := fs.Bool("json", false, "Machine-readable output")
	streamMode := fs.Bool("stream", false, "Incrementally POST events (§06 streaming mode)")
	keyID := fs.String("key-id", "", "Ed25519 key ID (Lane B)")
	keyFile := fs.String("key-file", "", "Ed25519 private seed file (Lane B)")
	if err := fs.Parse(args); err != nil {
		return exitErr(64, err)
	}

	cfg, err := config.Resolve(*cwd, config.Flags{
		ConfigPath: *cfgPath, Server: *server, TempToken: *tempToken,
		Token: *tok, AuthMode: *authMode,
		RepoURL: *repoURL, Branch: *branch, GitSha: *gitSha,
	}, os.Getenv)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return exitErr(2, err)
	}

	// Resolve auth lane: ssh ⇒ Ed25519 signed header; else App Password / temp-token.
	authCfg, aerr := resolveAuth(cfg, *keyID, *keyFile)
	if aerr != nil {
		fmt.Fprintln(os.Stderr, aerr)
		return exitErr(2, aerr)
	}

	// CI harvest is best-effort — flags/env may already supply the fields.
	if h, herr := ci.HarvestEnv(os.Getenv); herr == nil {
		if cfg.RepoURL == "" {
			cfg.RepoURL = h.RepoUrl
		}
		if cfg.Branch == "" {
			cfg.Branch = h.Branch
		}
		if cfg.GitSha == "" {
			cfg.GitSha = h.GitSha256
		}
	}

	det, derr := detect.Detect(*cwd)
	if derr != nil {
		fmt.Fprintln(os.Stderr, derr)
		return exitErr(2, derr)
	}

	wantPhases := []string{"lint", "build", "test"}
	if only != "" {
		wantPhases = []string{only}
	} else if *phasesCSV != "" {
		wantPhases = strings.Split(*phasesCSV, ",")
	}

	exit := 0
	for _, rt := range det.Runtimes {
		if *runtimeFilter != "" && rt.ID != *runtimeFilter {
			continue
		}
		for _, p := range rt.Phases {
			if !contains(wantPhases, p.Phase) {
				continue
			}
			var str *stream.Streamer
			if *streamMode && !*noPush {
				str = stream.New(stream.Options{
					ServerURL: cfg.ServerURL, RepoUrl: cfg.RepoURL,
					Branch: cfg.Branch, GitSha256: cfg.GitSha,
					TempToken: cfg.TempToken, Token: cfg.Token,
				})
			}
			res, runErr := runner.Run(context.Background(), *cwd, rt.ID, p.Phase, p.Runner, p.Args)
			if str != nil {
				for _, ln := range res.Lines {
					level := "info"
					switch classify.Classify(ln.Text, nil, nil) {
					case classify.Error:
						level = "error"
					case classify.Warn:
						level = "warn"
					}
					str.Append(level, redact.Line(ln.Text))
				}
				_ = str.Close(context.Background())
			}
			if runErr != nil {
				fmt.Fprintf(os.Stderr, "spawn %s/%s: %v\n", rt.ID, p.Phase, runErr)
				exit = 4
				if !*keepGoing {
					return exitCode(exit)
				}
				continue
			}
			emitResult(res, *jsonOut)

			// §06 shipping (batched mode); Lane B Ed25519 if authCfg set.
			if !*noPush {
				body := buildBody(cfg, rt.ID, p.Phase, res)
				sres := ship.Ship(context.Background(), ship.Options{
					ServerURL:  cfg.ServerURL,
					MaxRetries: cfg.MaxRetries,
					Auth:       authCfg,
				}, body)
				if sres.ExitCode != 0 {
					if *jsonOut {
						fmt.Printf(`{"Push":"failed","Runtime":%q,"Phase":%q,"ExitCode":%d,"OurCode":%q,"ServerCode":%q,"Attempts":%d}`+"\n",
							rt.ID, p.Phase, sres.ExitCode, sres.OurCode, sres.ServerCode, sres.Attempts)
					} else {
						fmt.Fprintf(os.Stderr, "[ship] %s/%s exit=%d code=%s%s attempts=%d\n",
							rt.ID, p.Phase, sres.ExitCode, sres.OurCode, sres.ServerCode, sres.Attempts)
					}
					if exit < sres.ExitCode {
						exit = sres.ExitCode
					}
					if !*keepGoing {
						return exitCode(exit)
					}
				}
			}

			if res.ExitCode != 0 {
				if exit == 0 {
					exit = 1
				}
				if !*keepGoing {
					return exitCode(exit)
				}
			}
		}
	}
	return exitCode(exit)
}

// buildBody assembles the §06 batched body from runner output.
//
// FilePaths[] is sorted lexicographically (determinism contract).
// HasError is true iff ErrorLogs[] is non-empty OR runner exit code ≠ 0.
func buildBody(cfg *config.Config, runtimeID, phase string, r *runner.Result) ship.Body {
	pipeline := strings.NewReplacer("{runtime}", runtimeID, "{phase}", phase).Replace(cfg.PipelineTpl)

	logs := make([]string, 0, len(r.Lines))
	errs := make([]string, 0)
	pathSet := map[string]struct{}{}
	pathRe := regexp.MustCompile(`(?:[A-Za-z0-9_./\-]+\.(?:go|ts|tsx|js|jsx|php|py|md))(?::\d+)?`)

	for _, ln := range r.Lines {
		safe := redact.Line(ln.Text)
		logs = append(logs, safe)
		if classify.Classify(ln.Text, nil, nil) == classify.Error {
			errs = append(errs, safe)
			for _, m := range pathRe.FindAllString(ln.Text, -1) {
				if i := strings.Index(m, ":"); i > 0 {
					m = m[:i]
				}
				if len(pathSet) < 100 {
					pathSet[m] = struct{}{}
				}
			}
		}
	}
	paths := make([]string, 0, len(pathSet))
	for p := range pathSet {
		paths = append(paths, p)
	}
	sort.Strings(paths)

	rootRepo := stripVersionSuffix(cfg.RepoURL)
	return ship.Body{
		RepoUrl:      cfg.RepoURL,
		RootRepo:     rootRepo,
		Branch:       cfg.Branch,
		TempToken:    cfg.TempToken,
		Token:        cfg.Token,
		PipelineName: pipeline,
		GitSha256:    cfg.GitSha,
		Logs:         logs,
		ErrorLogs:    errs,
		FilePaths:    paths,
		HasError:     len(errs) > 0 || r.ExitCode != 0,
	}
}

// stripVersionSuffix removes a trailing -vN segment from a repo URL
// (e.g. ".../repo-v2" → ".../repo") per §08 RootRepo derivation.
func stripVersionSuffix(u string) string {
	re := regexp.MustCompile(`-v\d+$`)
	return re.ReplaceAllString(u, "")
}

// SelfTest implements `glci --self-test [--check <mode>]`.
func SelfTest(args []string) error {
	fs := flag.NewFlagSet("self-test", flag.ContinueOnError)
	mode := fs.String("check", "all", "self-test mode")
	if err := fs.Parse(args); err != nil {
		return exitErr(64, err)
	}
	code, msg := selftest.Run(selftest.Mode(*mode))
	if code == 0 {
		fmt.Println(msg)
		return nil
	}
	fmt.Fprintln(os.Stderr, msg)
	return exitCode(code)
}

func emitResult(r *runner.Result, jsonOut bool) {
	errCount, warnCount := 0, 0
	for _, ln := range r.Lines {
		switch classify.Classify(ln.Text, nil, nil) {
		case classify.Error:
			errCount++
		case classify.Warn:
			warnCount++
		}
	}
	if jsonOut {
		fmt.Printf(`{"Runtime":%q,"Phase":%q,"ExitCode":%d,"Lines":%d,"Errors":%d,"Warnings":%d}`+"\n",
			r.Runtime, r.Phase, r.ExitCode, len(r.Lines), errCount, warnCount)
		return
	}
	dur := r.Ended.Sub(r.Started).Truncate(1e6)
	fmt.Printf("[%s/%s] exit=%d lines=%d errors=%d warnings=%d (%s)\n",
		r.Runtime, r.Phase, r.ExitCode, len(r.Lines), errCount, warnCount, dur)
	for _, ln := range r.Lines {
		fmt.Println(ln.Text)
	}
}

// ConfigPrint implements `glci config print`.
func ConfigPrint(args []string) error {
	fs := flag.NewFlagSet("config print", flag.ContinueOnError)
	cwd := fs.String("cwd", ".", "Project root")
	cfgPath := fs.String("config", "", "Config file")
	if err := fs.Parse(args); err != nil {
		return exitErr(64, err)
	}
	cfg, err := config.Resolve(*cwd, config.Flags{ConfigPath: *cfgPath}, os.Getenv)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return exitErr(2, err)
	}
	red := cfg.Redacted()
	fmt.Printf(`{
  "ServerURL":   %q,   // %s
  "AuthMode":    %q,   // %s
  "TempToken":   %q,   // %s
  "Token":       %q,   // %s
  "PushMode":    %q,   // %s
  "MaxRetries":  %d,   // %s
  "VerifyTLS":   %t,   // %s
  "RepoURL":     %q,   // %s
  "Branch":      %q,   // %s
  "GitSha":      %q,   // %s
  "PipelineTpl": %q    // %s
}`+"\n",
		red.ServerURL, cfg.Provenance["ServerURL"],
		red.AuthMode, cfg.Provenance["AuthMode"],
		red.TempToken, cfg.Provenance["TempToken"],
		red.Token, cfg.Provenance["Token"],
		red.PushMode, cfg.Provenance["PushMode"],
		red.MaxRetries, cfg.Provenance["MaxRetries"],
		red.VerifyTLS, cfg.Provenance["VerifyTLS"],
		red.RepoURL, cfg.Provenance["RepoURL"],
		red.Branch, cfg.Provenance["Branch"],
		red.GitSha, cfg.Provenance["GitSha"],
		red.PipelineTpl, cfg.Provenance["PipelineTpl"],
	)
	return nil
}

// Doctor implements `glci doctor` pre-flight checks.
func Doctor(args []string) error {
	fs := flag.NewFlagSet("doctor", flag.ContinueOnError)
	cwd := fs.String("cwd", ".", "Project root")
	if err := fs.Parse(args); err != nil {
		return exitErr(64, err)
	}
	// Check 1: detect runtime.
	if _, err := detect.Detect(*cwd); err != nil {
		fmt.Fprintln(os.Stderr, "doctor: "+err.Error())
		return exitCode(5)
	}
	fmt.Println("doctor: detect      ok")
	// Check 2: config resolves.
	cfg, err := config.Resolve(*cwd, config.Flags{}, os.Getenv)
	if err != nil {
		fmt.Fprintln(os.Stderr, "doctor: "+err.Error())
		return exitCode(5)
	}
	fmt.Println("doctor: config      ok")
	// Check 3: server reach via GET /get-logs?q=<repo>&limit=0 (§06).
	authCfg, _ := resolveAuth(cfg, "", "")
	status, rerr := ship.Reach(context.Background(), ship.Options{
		ServerURL: cfg.ServerURL,
		Auth:      authCfg,
	}, cfg.RepoURL, cfg.TempToken, cfg.Token)
	switch {
	case rerr != nil:
		fmt.Fprintf(os.Stderr, "doctor: server reach failed: %v\n", rerr)
		return exitCode(5)
	case status == 401:
		fmt.Fprintln(os.Stderr, "doctor: GLCI-DOCTOR-AUTH-INVALID (HTTP 401)")
		return exitCode(5)
	case status == 404:
		fmt.Fprintln(os.Stderr, "doctor: GLCI-DOCTOR-PROFILE-NOT-FOUND (HTTP 404)")
		return exitCode(5)
	case status >= 500:
		fmt.Fprintf(os.Stderr, "doctor: server error HTTP %d\n", status)
		return exitCode(5)
	}
	fmt.Printf("doctor: server      ok (HTTP %d)\n", status)
	return nil
}

// --- helpers ---

// resolveAuth returns an *auth.Config when the resolved configuration
// indicates Lane B (AuthMode=ssh) — explicit flags win, then env, then
// cfg.SSHKeyPath. Returns (nil, nil) when no auth lane is configured;
// callers can ship without auth (TempToken/Token headers may still be set).
func resolveAuth(cfg *config.Config, flagKeyID, flagKeyFile string) (*auth.Config, error) {
	if cfg.AuthMode != "ssh" {
		return nil, nil
	}
	a := &auth.Config{
		Mode:  auth.ModeEd25519,
		KeyID: flagKeyID,
	}
	keyFile := flagKeyFile
	if keyFile == "" {
		keyFile = cfg.SSHKeyPath
	}
	if keyFile == "" {
		return nil, fmt.Errorf("GLCI-AUTH-SSH-NO-KEY: AuthMode=ssh requires --key-file or GLCI_SSH_KEY_PATH")
	}
	seed, err := auth.LoadPrivateSeed(keyFile)
	if err != nil {
		return nil, fmt.Errorf("GLCI-AUTH-SSH-KEY-LOAD: %w", err)
	}
	a.PrivateSeed = seed
	if err := a.Resolve(); err != nil {
		return nil, err
	}
	if a.KeyID == "" {
		return nil, fmt.Errorf("GLCI-AUTH-SSH-NO-KEYID: pass --key-id or set GLCI_KEY_ID")
	}
	return a, nil
}

type cmdErr struct {
	code int
	err  error
}

func (e *cmdErr) Error() string { return e.err.Error() }
func (e *cmdErr) Code() int     { return e.code }

func exitErr(code int, err error) error { return &cmdErr{code: code, err: err} }
func exitCode(code int) error {
	if code == 0 {
		return nil
	}
	return &cmdErr{code: code, err: fmt.Errorf("exit %d", code)}
}

// CodeOf returns the exit code stored on a cmdErr, or 1 for any other error.
func CodeOf(err error) int {
	if err == nil {
		return 0
	}
	if ce, ok := err.(*cmdErr); ok {
		return ce.code
	}
	return 1
}

func contains(xs []string, x string) bool {
	for _, v := range xs {
		if v == x {
			return true
		}
	}
	return false
}
