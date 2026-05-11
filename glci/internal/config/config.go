// Package config resolves glci configuration per spec/28 §05.
//
// Override order (low → high): defaults < glci.toml < env < flags.
// File parsing is intentionally minimal (subset: [section] + key = "string"|bool|int).
// Full TOML is a P-future enhancement; the env+flag path is the canonical CI route.
package config

import (
	"errors"
	"fmt"
	"net/url"
	"os"
	"strconv"
	"strings"
)

// Provenance records where each field came from.
type Provenance string

const (
	SrcDefault Provenance = "default"
	SrcFile    Provenance = "file"
	SrcEnv     Provenance = "env"
	SrcFlag    Provenance = "flag"
)

// Config is the resolved configuration struct.
type Config struct {
	ServerURL    string
	AuthMode     string // "temptoken" | "ssh"
	TempToken    string
	Token        string
	SSHKeyPath   string
	PushMode     string // "batched" | "streaming"
	MaxRetries   int
	VerifyTLS    bool
	RepoURL      string
	Branch       string
	GitSha       string
	PipelineTpl  string

	Provenance map[string]Provenance
}

// Defaults returns the compiled-in defaults.
func Defaults() *Config {
	c := &Config{
		AuthMode:    "temptoken",
		PushMode:    "batched",
		MaxRetries:  3,
		VerifyTLS:   true,
		PipelineTpl: "{runtime}-{phase}",
		Provenance:  map[string]Provenance{},
	}
	for _, f := range []string{"ServerURL", "AuthMode", "TempToken", "Token", "SSHKeyPath", "PushMode", "MaxRetries", "VerifyTLS", "RepoURL", "Branch", "GitSha", "PipelineTpl"} {
		c.Provenance[f] = SrcDefault
	}
	return c
}

// Flags is the subset of CLI flags that map into config.
type Flags struct {
	ConfigPath string
	Server     string
	TempToken  string
	Token      string
	AuthMode   string
	RepoURL    string
	Branch     string
	GitSha     string
}

// Resolve merges defaults < file < env < flags and validates.
func Resolve(cwd string, flags Flags, getenv func(string) string) (*Config, error) {
	if getenv == nil {
		getenv = os.Getenv
	}
	c := Defaults()

	// File (minimal subset)
	path := flags.ConfigPath
	if path == "" {
		path = cwd + "/glci.toml"
	}
	if data, err := os.ReadFile(path); err == nil {
		if err := loadMinimalTOML(c, string(data)); err != nil {
			return nil, fmt.Errorf("glci.toml: %w", err)
		}
	}

	// Env
	apply := func(env, field string, set func(string)) {
		v := getenv(env)
		if v != "" {
			set(v)
			c.Provenance[field] = SrcEnv
		}
	}
	apply("GLCI_SERVER_URL", "ServerURL", func(v string) { c.ServerURL = v })
	apply("GLCI_AUTH_MODE", "AuthMode", func(v string) { c.AuthMode = v })
	apply("GLCI_TEMP_TOKEN", "TempToken", func(v string) { c.TempToken = v })
	apply("GLCI_TOKEN", "Token", func(v string) { c.Token = v })
	apply("GLCI_SSH_KEY_PATH", "SSHKeyPath", func(v string) { c.SSHKeyPath = v })
	apply("GLCI_REPO_URL", "RepoURL", func(v string) { c.RepoURL = v })
	apply("GLCI_BRANCH", "Branch", func(v string) { c.Branch = v })
	apply("GLCI_GIT_SHA", "GitSha", func(v string) { c.GitSha = v })
	apply("GLCI_PUSH_MODE", "PushMode", func(v string) { c.PushMode = v })
	if v := getenv("GLCI_VERIFY_TLS"); v != "" {
		c.VerifyTLS = v == "1" || strings.EqualFold(v, "true")
		c.Provenance["VerifyTLS"] = SrcEnv
	}

	// Flags (highest)
	applyFlag := func(v, field string, set func(string)) {
		if v != "" {
			set(v)
			c.Provenance[field] = SrcFlag
		}
	}
	applyFlag(flags.Server, "ServerURL", func(v string) { c.ServerURL = v })
	applyFlag(flags.TempToken, "TempToken", func(v string) { c.TempToken = v })
	applyFlag(flags.Token, "Token", func(v string) { c.Token = v })
	applyFlag(flags.AuthMode, "AuthMode", func(v string) { c.AuthMode = v })
	applyFlag(flags.RepoURL, "RepoURL", func(v string) { c.RepoURL = v })
	applyFlag(flags.Branch, "Branch", func(v string) { c.Branch = v })
	applyFlag(flags.GitSha, "GitSha", func(v string) { c.GitSha = v })

	if err := c.validate(); err != nil {
		return nil, err
	}
	return c, nil
}

func (c *Config) validate() error {
	if c.ServerURL == "" {
		return errors.New("GLCI-CONFIG-MISSING-ENV: server URL not set (GLCI_SERVER_URL or [server] url)")
	}
	u, err := url.Parse(c.ServerURL)
	if err != nil {
		return fmt.Errorf("GLCI-CONFIG-INSECURE-URL: invalid URL %q: %w", c.ServerURL, err)
	}
	if u.Scheme != "https" && u.Scheme != "http" {
		return fmt.Errorf("GLCI-CONFIG-INSECURE-URL: scheme must be https (got %q)", u.Scheme)
	}
	switch c.AuthMode {
	case "temptoken":
		if c.TempToken == "" {
			return errors.New("GLCI-CONFIG-MISSING-TOKEN: auth_mode=temptoken requires GLCI_TEMP_TOKEN")
		}
	case "ssh":
		if c.SSHKeyPath == "" {
			return errors.New("GLCI-CONFIG-SSH-KEY-MISSING: auth_mode=ssh requires GLCI_SSH_KEY_PATH")
		}
		if _, err := os.Stat(c.SSHKeyPath); err != nil {
			return fmt.Errorf("GLCI-CONFIG-SSH-KEY-MISSING: %s: %w", c.SSHKeyPath, err)
		}
	default:
		return fmt.Errorf("GLCI-CONFIG-BAD-MODE: unknown auth_mode %q", c.AuthMode)
	}
	if !validTemplate(c.PipelineTpl) {
		return errors.New("GLCI-CONFIG-BAD-TEMPLATE: only {runtime} and {phase} placeholders allowed")
	}
	return nil
}

func validTemplate(t string) bool {
	s := t
	for _, p := range []string{"{runtime}", "{phase}"} {
		s = strings.ReplaceAll(s, p, "")
	}
	return !strings.ContainsAny(s, "{}")
}

// loadMinimalTOML supports `[section]` headers and `key = "value"|true|false|123` lines.
func loadMinimalTOML(c *Config, body string) error {
	section := ""
	for ln, raw := range strings.Split(body, "\n") {
		line := strings.TrimSpace(raw)
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		if strings.HasPrefix(line, "[") && strings.HasSuffix(line, "]") {
			section = strings.TrimSpace(line[1 : len(line)-1])
			continue
		}
		eq := strings.Index(line, "=")
		if eq < 0 {
			return fmt.Errorf("line %d: missing '=': %q", ln+1, raw)
		}
		key := strings.TrimSpace(line[:eq])
		val := strings.TrimSpace(line[eq+1:])
		// strip inline comment
		if hi := strings.Index(val, " #"); hi > 0 {
			val = strings.TrimSpace(val[:hi])
		}
		val = strings.Trim(val, "\"")
		set := func(field string, target *string) {
			*target = val
			c.Provenance[field] = SrcFile
		}
		switch section + "." + key {
		case "server.url":
			set("ServerURL", &c.ServerURL)
		case "server.auth_mode":
			set("AuthMode", &c.AuthMode)
		case "server.verify_tls":
			c.VerifyTLS = val == "true"
			c.Provenance["VerifyTLS"] = SrcFile
		case "auth.temp_token":
			set("TempToken", &c.TempToken)
		case "auth.token":
			set("Token", &c.Token)
		case "auth.ssh_key_path":
			set("SSHKeyPath", &c.SSHKeyPath)
		case "push.mode":
			set("PushMode", &c.PushMode)
		case "push.max_retries":
			n, err := strconv.Atoi(val)
			if err != nil {
				return fmt.Errorf("line %d: max_retries must be int", ln+1)
			}
			c.MaxRetries = n
			c.Provenance["MaxRetries"] = SrcFile
		case "repo.url":
			set("RepoURL", &c.RepoURL)
		case "repo.branch":
			set("Branch", &c.Branch)
		case "pipeline.name_template":
			set("PipelineTpl", &c.PipelineTpl)
		}
	}
	return nil
}

// Redacted returns a copy with secrets masked, suitable for `glci config print`.
func (c *Config) Redacted() *Config {
	cp := *c
	if cp.TempToken != "" {
		cp.TempToken = "***"
	}
	if cp.Token != "" {
		cp.Token = "***"
	}
	return &cp
}
