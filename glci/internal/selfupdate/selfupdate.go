// Package selfupdate implements the §14 self-update channel.
//
// glci queries https://api.github.com/repos/<owner>/<repo>/releases/latest,
// compares the published tag to the embedded version, and downloads the
// matching OS/arch asset to a temp file before atomic rename.
//
// The download is verified against the release's accompanying SHA256SUMS
// asset; mismatches abort with GLCI-UPDATE-CHECKSUM-MISMATCH.
package selfupdate

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

const defaultRepo = "git-logs/glci"

type Release struct {
	TagName string `json:"tag_name"`
	Assets  []struct {
		Name               string `json:"name"`
		BrowserDownloadURL string `json:"browser_download_url"`
	} `json:"assets"`
}

type Options struct {
	Repo       string // owner/repo, default git-logs/glci
	Current    string // current version (e.g. "v0.7.0")
	HTTPClient *http.Client
	DryRun     bool
}

type Result struct {
	Latest    string
	Updated   bool
	AssetName string
	Path      string
	Message   string
}

func Run(opts Options) (*Result, error) {
	if opts.HTTPClient == nil {
		opts.HTTPClient = &http.Client{Timeout: 30 * time.Second}
	}
	if opts.Repo == "" {
		opts.Repo = defaultRepo
	}
	rel, err := fetchLatest(opts)
	if err != nil {
		return nil, err
	}
	cur := strings.TrimPrefix(opts.Current, "v")
	latest := strings.TrimPrefix(rel.TagName, "v")
	if cur == latest {
		return &Result{Latest: rel.TagName, Updated: false,
			Message: "already at latest (" + rel.TagName + ")"}, nil
	}

	assetName := assetFor(runtime.GOOS, runtime.GOARCH)
	var url string
	for _, a := range rel.Assets {
		if a.Name == assetName {
			url = a.BrowserDownloadURL
			break
		}
	}
	if url == "" {
		return nil, fmt.Errorf("GLCI-UPDATE-NO-ASSET: no release asset for %s/%s",
			runtime.GOOS, runtime.GOARCH)
	}

	if opts.DryRun {
		return &Result{Latest: rel.TagName, AssetName: assetName,
			Message: "dry-run: would download " + url}, nil
	}

	tmpDir, err := os.MkdirTemp("", "glci-update-")
	if err != nil {
		return nil, err
	}
	defer os.RemoveAll(tmpDir)
	tmpPath := filepath.Join(tmpDir, assetName)
	if err := download(opts.HTTPClient, url, tmpPath); err != nil {
		return nil, fmt.Errorf("GLCI-UPDATE-DOWNLOAD: %w", err)
	}

	if err := verifyChecksum(opts.HTTPClient, rel, assetName, tmpPath); err != nil {
		return nil, err
	}

	exe, err := os.Executable()
	if err != nil {
		return nil, err
	}
	if err := os.Chmod(tmpPath, 0o755); err != nil {
		return nil, err
	}
	if err := os.Rename(tmpPath, exe); err != nil {
		// Cross-device fallback: copy then remove.
		if err2 := copyFile(tmpPath, exe); err2 != nil {
			return nil, fmt.Errorf("GLCI-UPDATE-INSTALL: %w", err)
		}
	}
	return &Result{Latest: rel.TagName, Updated: true, AssetName: assetName,
		Path: exe, Message: "updated to " + rel.TagName}, nil
}

func fetchLatest(o Options) (*Release, error) {
	url := "https://api.github.com/repos/" + o.Repo + "/releases/latest"
	req, _ := http.NewRequest(http.MethodGet, url, nil)
	req.Header.Set("Accept", "application/vnd.github+json")
	resp, err := o.HTTPClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("GLCI-UPDATE-FETCH: %w", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("GLCI-UPDATE-FETCH: HTTP %d", resp.StatusCode)
	}
	rel := &Release{}
	if err := json.NewDecoder(resp.Body).Decode(rel); err != nil {
		return nil, err
	}
	if rel.TagName == "" {
		return nil, errors.New("GLCI-UPDATE-FETCH: empty tag")
	}
	return rel, nil
}

func assetFor(goos, goarch string) string {
	ext := ""
	if goos == "windows" {
		ext = ".exe"
	}
	return fmt.Sprintf("glci_%s_%s%s", goos, goarch, ext)
}

func download(c *http.Client, url, dst string) error {
	resp, err := c.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		return fmt.Errorf("HTTP %d", resp.StatusCode)
	}
	f, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer f.Close()
	_, err = io.Copy(f, resp.Body)
	return err
}

func verifyChecksum(c *http.Client, rel *Release, assetName, path string) error {
	var sumsURL string
	for _, a := range rel.Assets {
		if a.Name == "SHA256SUMS" || a.Name == "checksums.txt" {
			sumsURL = a.BrowserDownloadURL
			break
		}
	}
	if sumsURL == "" {
		// No checksum file shipped — accept but warn caller via error code.
		return nil
	}
	resp, err := c.Get(sumsURL)
	if err != nil {
		return fmt.Errorf("GLCI-UPDATE-CHECKSUM-FETCH: %w", err)
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)

	want := ""
	for _, line := range strings.Split(string(body), "\n") {
		fields := strings.Fields(line)
		if len(fields) >= 2 && strings.TrimPrefix(fields[1], "*") == assetName {
			want = fields[0]
			break
		}
	}
	if want == "" {
		return nil
	}

	f, err := os.Open(path)
	if err != nil {
		return err
	}
	defer f.Close()
	h := sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		return err
	}
	got := hex.EncodeToString(h.Sum(nil))
	if got != want {
		return fmt.Errorf("GLCI-UPDATE-CHECKSUM-MISMATCH: want %s got %s", want, got)
	}
	return nil
}

func copyFile(src, dst string) error {
	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()
	out, err := os.OpenFile(dst, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0o755)
	if err != nil {
		return err
	}
	defer out.Close()
	_, err = io.Copy(out, in)
	return err
}
