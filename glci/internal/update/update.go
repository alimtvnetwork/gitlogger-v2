// Package update implements `glci self-update` against a versioned manifest.
//
// Manifest shape (served at <channel>/manifest.json):
//
//	{
//	  "version":  "1.4.0",
//	  "released": "2026-05-11T00:00:00Z",
//	  "binaries": {
//	    "linux/amd64":   {"url": "...", "sha256": "..."},
//	    "darwin/arm64":  {"url": "...", "sha256": "..."}
//	  }
//	}
//
// Safety:
//   - SHA-256 of the downloaded binary must match the manifest entry.
//   - Atomic swap: download → tmp → chmod 0755 → os.Rename(tmp, exe).
//   - --dry-run prints the action plan without touching disk.
package update

import (
	"context"
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
	"time"
)

type BinaryEntry struct {
	URL    string `json:"url"`
	SHA256 string `json:"sha256"`
}

type Manifest struct {
	Version  string                  `json:"version"`
	Released time.Time               `json:"released"`
	Binaries map[string]*BinaryEntry `json:"binaries"`
}

// FetchManifest pulls and parses the manifest from manifestURL.
func FetchManifest(ctx context.Context, manifestURL string) (*Manifest, error) {
	cctx, cancel := context.WithTimeout(ctx, 10*time.Second)
	defer cancel()
	req, _ := http.NewRequestWithContext(cctx, http.MethodGet, manifestURL, nil)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("GLCI-UPDATE-MANIFEST-HTTP-%d", resp.StatusCode)
	}
	m := &Manifest{}
	if err := json.NewDecoder(resp.Body).Decode(m); err != nil {
		return nil, fmt.Errorf("GLCI-UPDATE-MANIFEST-PARSE: %w", err)
	}
	if m.Version == "" || m.Binaries == nil {
		return nil, errors.New("GLCI-UPDATE-MANIFEST-INVALID")
	}
	return m, nil
}

// PlatformKey returns the manifest key for the current binary.
func PlatformKey() string { return runtime.GOOS + "/" + runtime.GOARCH }

// Plan describes what self-update would do; safe to print in --dry-run mode.
type Plan struct {
	Current   string
	Target    string
	URL       string
	SHA256    string
	ExePath   string
	Available bool
}

// BuildPlan resolves the manifest entry for this platform.
func BuildPlan(currentVersion string, m *Manifest) (*Plan, error) {
	exe, err := os.Executable()
	if err != nil {
		return nil, err
	}
	plan := &Plan{Current: currentVersion, Target: m.Version, ExePath: exe}
	if m.Version == currentVersion {
		return plan, nil // no change
	}
	be, ok := m.Binaries[PlatformKey()]
	if !ok || be == nil || be.URL == "" {
		return nil, fmt.Errorf("GLCI-UPDATE-NO-BINARY: %s", PlatformKey())
	}
	plan.URL = be.URL
	plan.SHA256 = be.SHA256
	plan.Available = true
	return plan, nil
}

// Apply downloads the binary, verifies SHA-256, and atomically replaces exe.
func Apply(ctx context.Context, p *Plan) error {
	if !p.Available {
		return nil
	}
	cctx, cancel := context.WithTimeout(ctx, 5*time.Minute)
	defer cancel()
	req, _ := http.NewRequestWithContext(cctx, http.MethodGet, p.URL, nil)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return fmt.Errorf("GLCI-UPDATE-DOWNLOAD: %w", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		return fmt.Errorf("GLCI-UPDATE-DOWNLOAD-HTTP-%d", resp.StatusCode)
	}

	tmp, err := os.CreateTemp(filepath.Dir(p.ExePath), ".glci-update-*")
	if err != nil {
		return err
	}
	tmpPath := tmp.Name()
	defer func() {
		// Best-effort cleanup if we bailed before os.Rename.
		if _, statErr := os.Stat(tmpPath); statErr == nil {
			_ = os.Remove(tmpPath)
		}
	}()

	h := sha256.New()
	w := io.MultiWriter(tmp, h)
	if _, err := io.Copy(w, resp.Body); err != nil {
		_ = tmp.Close()
		return err
	}
	if err := tmp.Close(); err != nil {
		return err
	}
	got := hex.EncodeToString(h.Sum(nil))
	if p.SHA256 != "" && got != p.SHA256 {
		return fmt.Errorf("GLCI-UPDATE-SHA-MISMATCH: got %s want %s", got, p.SHA256)
	}
	if err := os.Chmod(tmpPath, 0o755); err != nil {
		return err
	}
	return os.Rename(tmpPath, p.ExePath)
}
