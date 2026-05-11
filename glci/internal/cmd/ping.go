package cmd

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

// Ping calls /wp-json/git-logs/v1/health on the given base URL and prints the body.
//
// Usage:
//
//	glci ping --base https://example.com
func Ping(args []string) error {
	fs := flag.NewFlagSet("ping", flag.ContinueOnError)
	base := fs.String("base", "", "Base URL of the WordPress site hosting the git-logs plugin (required)")
	timeout := fs.Duration("timeout", 5*time.Second, "HTTP request timeout")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *base == "" {
		return errors.New("`--base` is required, e.g. --base https://example.com")
	}

	url := strings.TrimRight(*base, "/") + "/wp-json/git-logs/v1/health"
	client := &http.Client{Timeout: *timeout}

	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		return err
	}
	req.Header.Set("Accept", "application/json")
	req.Header.Set("User-Agent", "glci/0.1.0 (+https://example.com/glci)")

	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("GET %s: %w", url, err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("health check failed: HTTP %d — %s", resp.StatusCode, strings.TrimSpace(string(body)))
	}

	// Pretty-print JSON if the body parses as JSON; else print raw.
	var pretty map[string]any
	if err := json.Unmarshal(body, &pretty); err == nil {
		out, _ := json.MarshalIndent(pretty, "", "  ")
		fmt.Println(string(out))
	} else {
		fmt.Println(string(body))
	}
	return nil
}
