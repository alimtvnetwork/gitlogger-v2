package cmd

import (
	"bytes"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"

	"github.com/example/glci/internal/auth"
)

// Whoami calls GET /wp-json/git-logs/v1/whoami using either auth lane and prints the JSON.
//
// Examples:
//
//	# App Password lane
//	glci whoami --base https://site.test --user alice --app-password "abcd EFGH ijkl MNOP"
//
//	# Ed25519 lane
//	glci whoami --base https://site.test --key-id ab12cd34 --key-file ~/.glci/key
func Whoami(args []string) error {
	fs := flag.NewFlagSet("whoami", flag.ContinueOnError)
	base := fs.String("base", "", "Base URL of the WordPress site (required)")
	timeout := fs.Duration("timeout", 5*time.Second, "HTTP request timeout")

	user := fs.String("user", "", "WP user login (App Password lane)")
	appPwd := fs.String("app-password", "", "WP App Password (App Password lane)")

	keyID := fs.String("key-id", "", "Registered Ed25519 keyId (Ed25519 lane)")
	keyFile := fs.String("key-file", "", "Path to glci-ed25519-priv key file (Ed25519 lane)")

	if err := fs.Parse(args); err != nil {
		return err
	}
	if *base == "" {
		return errors.New("`--base` is required")
	}

	cfg := auth.Config{User: *user, AppPassword: *appPwd, KeyID: *keyID}
	if *keyFile != "" {
		seed, err := auth.LoadPrivateSeed(*keyFile)
		if err != nil {
			return err
		}
		cfg.PrivateSeed = seed
	}
	if err := cfg.Resolve(); err != nil {
		return err
	}

	url := strings.TrimRight(*base, "/") + "/wp-json/git-logs/v1/whoami"
	req, err := http.NewRequest(http.MethodGet, url, bytes.NewReader(nil))
	if err != nil {
		return err
	}
	req.Header.Set("Accept", "application/json")
	req.Header.Set("User-Agent", "glci/0.2.0")
	if err := cfg.Apply(req); err != nil {
		return err
	}

	resp, err := (&http.Client{Timeout: *timeout}).Do(req)
	if err != nil {
		return fmt.Errorf("GET %s: %w", url, err)
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("whoami failed: HTTP %d — %s", resp.StatusCode, strings.TrimSpace(string(body)))
	}

	var pretty map[string]any
	if err := json.Unmarshal(body, &pretty); err == nil {
		out, _ := json.MarshalIndent(pretty, "", "  ")
		fmt.Println(string(out))
	} else {
		fmt.Println(string(body))
	}
	return nil
}
