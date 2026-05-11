package config

import (
	"os"
	"path/filepath"
	"testing"
)

func emptyEnv(string) string { return "" }

func TestResolve_DefaultsRequireServerURL(t *testing.T) {
	dir := t.TempDir()
	_, err := Resolve(dir, Flags{}, emptyEnv)
	if err == nil {
		t.Fatal("expected GLCI-CONFIG-MISSING-ENV")
	}
}

func TestResolve_FlagsBeatEnv_BeatFile(t *testing.T) {
	dir := t.TempDir()
	toml := `
[server]
url = "https://from-file.example"
auth_mode = "temptoken"
[auth]
temp_token = "file-tok"
`
	if err := os.WriteFile(filepath.Join(dir, "glci.toml"), []byte(toml), 0o600); err != nil {
		t.Fatal(err)
	}
	env := func(k string) string {
		switch k {
		case "GLCI_SERVER_URL":
			return "https://from-env.example"
		case "GLCI_TEMP_TOKEN":
			return "env-tok"
		}
		return ""
	}
	c, err := Resolve(dir, Flags{Server: "https://from-flag.example"}, env)
	if err != nil {
		t.Fatal(err)
	}
	if c.ServerURL != "https://from-flag.example" {
		t.Errorf("flag should win, got %q", c.ServerURL)
	}
	if c.Provenance["ServerURL"] != SrcFlag {
		t.Errorf("provenance not flag: %v", c.Provenance["ServerURL"])
	}
	if c.TempToken != "env-tok" {
		t.Errorf("env should beat file, got %q", c.TempToken)
	}
	if c.Provenance["TempToken"] != SrcEnv {
		t.Errorf("provenance not env: %v", c.Provenance["TempToken"])
	}
}

func TestResolve_RejectsBadScheme(t *testing.T) {
	_, err := Resolve(t.TempDir(), Flags{Server: "ftp://nope"}, func(k string) string {
		if k == "GLCI_TEMP_TOKEN" {
			return "x"
		}
		return ""
	})
	if err == nil {
		t.Fatal("expected GLCI-CONFIG-INSECURE-URL")
	}
}

func TestResolve_TempTokenLaneRequiresToken(t *testing.T) {
	_, err := Resolve(t.TempDir(), Flags{Server: "https://x"}, emptyEnv)
	if err == nil {
		t.Fatal("expected GLCI-CONFIG-MISSING-TOKEN")
	}
}

func TestResolve_SSHLaneRequiresKeyFile(t *testing.T) {
	env := func(k string) string {
		switch k {
		case "GLCI_AUTH_MODE":
			return "ssh"
		case "GLCI_SSH_KEY_PATH":
			return "/no/such/file"
		}
		return ""
	}
	_, err := Resolve(t.TempDir(), Flags{Server: "https://x"}, env)
	if err == nil {
		t.Fatal("expected GLCI-CONFIG-SSH-KEY-MISSING")
	}
}

func TestResolve_BadAuthMode(t *testing.T) {
	_, err := Resolve(t.TempDir(), Flags{Server: "https://x", AuthMode: "weird"}, emptyEnv)
	if err == nil {
		t.Fatal("expected GLCI-CONFIG-BAD-MODE")
	}
}

func TestRedacted_MasksSecrets(t *testing.T) {
	c := &Config{TempToken: "abc", Token: "xyz"}
	r := c.Redacted()
	if r.TempToken != "***" || r.Token != "***" {
		t.Fatalf("not redacted: %+v", r)
	}
	if c.TempToken != "abc" {
		t.Fatal("Redacted mutated original")
	}
}

func TestLoadMinimalTOML_Comments(t *testing.T) {
	dir := t.TempDir()
	toml := `
# top comment
[server]
url = "https://ok.example" # trailing comment
auth_mode = "temptoken"
verify_tls = false
[push]
mode = "streaming"
max_retries = 7
[auth]
temp_token = "tt"
`
	_ = os.WriteFile(filepath.Join(dir, "glci.toml"), []byte(toml), 0o600)
	c, err := Resolve(dir, Flags{}, emptyEnv)
	if err != nil {
		t.Fatal(err)
	}
	if c.ServerURL != "https://ok.example" {
		t.Errorf("server url: %q", c.ServerURL)
	}
	if c.VerifyTLS {
		t.Error("verify_tls=false not honored")
	}
	if c.PushMode != "streaming" {
		t.Errorf("push mode: %q", c.PushMode)
	}
	if c.MaxRetries != 7 {
		t.Errorf("max_retries: %d", c.MaxRetries)
	}
}

func TestValidate_BadTemplateRejected(t *testing.T) {
	c := &Config{ServerURL: "https://x", AuthMode: "temptoken", TempToken: "t", PipelineTpl: "{runtime}-{phase}-{bogus}"}
	if err := c.validate(); err == nil {
		t.Fatal("expected GLCI-CONFIG-BAD-TEMPLATE")
	}
}
