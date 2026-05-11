package selfupdate

import (
	"crypto/sha256"
	"encoding/hex"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestAssetFor(t *testing.T) {
	if got := assetFor("linux", "amd64"); got != "glci_linux_amd64" {
		t.Errorf("linux/amd64: %q", got)
	}
	if got := assetFor("windows", "amd64"); got != "glci_windows_amd64.exe" {
		t.Errorf("windows ext missing: %q", got)
	}
	if got := assetFor("darwin", "arm64"); got != "glci_darwin_arm64" {
		t.Errorf("darwin/arm64: %q", got)
	}
}

type asset = struct {
	Name               string `json:"name"`
	BrowserDownloadURL string `json:"browser_download_url"`
}

func TestVerifyChecksum_Match(t *testing.T) {
	body := []byte("fake-binary-payload")
	sum := sha256.Sum256(body)
	hexSum := hex.EncodeToString(sum[:])

	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_, _ = w.Write([]byte(hexSum + "  myasset\n"))
	}))
	defer srv.Close()

	rel := &Release{TagName: "v1"}
	rel.Assets = append(rel.Assets, asset{Name: "SHA256SUMS", BrowserDownloadURL: srv.URL})

	dir := t.TempDir()
	path := filepath.Join(dir, "myasset")
	_ = os.WriteFile(path, body, 0o644)

	if err := verifyChecksum(http.DefaultClient, rel, "myasset", path); err != nil {
		t.Fatalf("match should succeed: %v", err)
	}
}

func TestVerifyChecksum_Mismatch(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_, _ = w.Write([]byte("0000000000000000000000000000000000000000000000000000000000000000  myasset\n"))
	}))
	defer srv.Close()

	rel := &Release{TagName: "v1"}
	rel.Assets = append(rel.Assets, asset{Name: "SHA256SUMS", BrowserDownloadURL: srv.URL})

	dir := t.TempDir()
	path := filepath.Join(dir, "myasset")
	_ = os.WriteFile(path, []byte("not-matching"), 0o644)

	err := verifyChecksum(http.DefaultClient, rel, "myasset", path)
	if err == nil || !strings.Contains(err.Error(), "GLCI-UPDATE-CHECKSUM-MISMATCH") {
		t.Fatalf("want checksum-mismatch, got %v", err)
	}
}

func TestVerifyChecksum_NoSumsFileIsAccepted(t *testing.T) {
	rel := &Release{TagName: "v1"} // no SHA256SUMS asset
	dir := t.TempDir()
	path := filepath.Join(dir, "x")
	_ = os.WriteFile(path, []byte("anything"), 0o644)
	if err := verifyChecksum(http.DefaultClient, rel, "x", path); err != nil {
		t.Fatalf("absent sums file should pass: %v", err)
	}
}

func TestVerifyChecksum_AssetNotInSumsListIsAccepted(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_, _ = w.Write([]byte("dead  other-asset\n"))
	}))
	defer srv.Close()
	rel := &Release{TagName: "v1"}
	rel.Assets = append(rel.Assets, asset{Name: "SHA256SUMS", BrowserDownloadURL: srv.URL})
	dir := t.TempDir()
	path := filepath.Join(dir, "myasset")
	_ = os.WriteFile(path, []byte("anything"), 0o644)
	if err := verifyChecksum(http.DefaultClient, rel, "myasset", path); err != nil {
		t.Fatalf("missing entry should be accepted: %v", err)
	}
}

func TestDownload_SavesBody(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_, _ = w.Write([]byte("hello-binary"))
	}))
	defer srv.Close()
	dst := filepath.Join(t.TempDir(), "out.bin")
	if err := download(http.DefaultClient, srv.URL, dst); err != nil {
		t.Fatal(err)
	}
	got, _ := os.ReadFile(dst)
	if string(got) != "hello-binary" {
		t.Errorf("payload: %q", got)
	}
}

func TestDownload_Non200(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(404)
	}))
	defer srv.Close()
	if err := download(http.DefaultClient, srv.URL, filepath.Join(t.TempDir(), "x")); err == nil {
		t.Fatal("expected non-200 error")
	}
}

func TestCopyFile_RoundTrip(t *testing.T) {
	dir := t.TempDir()
	src := filepath.Join(dir, "src")
	dst := filepath.Join(dir, "dst")
	want := []byte("payload")
	_ = os.WriteFile(src, want, 0o644)
	if err := copyFile(src, dst); err != nil {
		t.Fatal(err)
	}
	got, _ := os.ReadFile(dst)
	if string(got) != string(want) {
		t.Errorf("copyFile: %q != %q", got, want)
	}
}
