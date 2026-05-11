package auth

import (
	"bytes"
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestGenerateKeypair_Shape(t *testing.T) {
	seed, pub, kid, err := GenerateKeypair()
	if err != nil {
		t.Fatal(err)
	}
	if len(seed) != 32 {
		t.Errorf("seed len = %d, want 32", len(seed))
	}
	if len(pub) != ed25519.PublicKeySize {
		t.Errorf("pub len = %d, want %d", len(pub), ed25519.PublicKeySize)
	}
	if len(kid) != 8 {
		t.Errorf("keyId len = %d, want 8", len(kid))
	}
	if _, err := hex.DecodeString(kid); err != nil {
		t.Errorf("keyId not hex: %v", err)
	}
	// Seed should derive same pub.
	derivedPub := ed25519.NewKeyFromSeed(seed).Public().(ed25519.PublicKey)
	if !bytes.Equal(derivedPub, pub) {
		t.Errorf("derived pub mismatch")
	}
}

func TestLoadPrivateSeed_RoundTrip(t *testing.T) {
	seed, _, _, err := GenerateKeypair()
	if err != nil {
		t.Fatal(err)
	}
	dir := t.TempDir()
	path := filepath.Join(dir, "key")
	body := "# comment\n\n" + PrivPrefix + base64.StdEncoding.EncodeToString(seed) + "\n"
	if err := os.WriteFile(path, []byte(body), 0o600); err != nil {
		t.Fatal(err)
	}
	got, err := LoadPrivateSeed(path)
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(got, seed) {
		t.Errorf("seed mismatch")
	}
}

func TestLoadPrivateSeed_BadPrefix(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "key")
	_ = os.WriteFile(path, []byte("not-a-key xxx\n"), 0o600)
	if _, err := LoadPrivateSeed(path); err == nil {
		t.Fatal("expected error for bad prefix")
	}
}

func TestApply_AppPasswordSetsBasic(t *testing.T) {
	c := &Config{Mode: ModeAppPassword, User: "alice", AppPassword: "s3cret"}
	req, _ := http.NewRequest("GET", "https://example.com/x", nil)
	if err := c.Apply(req); err != nil {
		t.Fatal(err)
	}
	u, p, ok := req.BasicAuth()
	if !ok || u != "alice" || p != "s3cret" {
		t.Errorf("basic auth not set: u=%q p=%q ok=%v", u, p, ok)
	}
}

func TestApply_NoneFails(t *testing.T) {
	c := &Config{}
	req, _ := http.NewRequest("GET", "https://example.com/x", nil)
	if err := c.Apply(req); err == nil {
		t.Fatal("expected error for ModeNone")
	}
}

func TestApply_Ed25519_HeaderVerifies(t *testing.T) {
	seed, pub, kid, err := GenerateKeypair()
	if err != nil {
		t.Fatal(err)
	}
	body := []byte(`{"hello":"world"}`)
	req, _ := http.NewRequest("POST", "https://example.com/api/v1/append-log?x=1", io.NopCloser(bytes.NewReader(body)))

	c := &Config{Mode: ModeEd25519, KeyID: kid, PrivateSeed: seed}
	if err := c.Apply(req); err != nil {
		t.Fatal(err)
	}
	hdr := req.Header.Get("X-GitLogs-Auth")
	if !strings.HasPrefix(hdr, Scheme+" ") {
		t.Fatalf("missing/invalid auth header: %q", hdr)
	}

	// Body must still be readable for downstream HTTP client.
	got, _ := io.ReadAll(req.Body)
	if !bytes.Equal(got, body) {
		t.Fatalf("body not preserved after sign")
	}

	// Reconstruct canonical string and verify signature.
	parts := parseAuthHeader(hdr)
	bodyHash := sha256.Sum256(body)
	canonical := strings.Join([]string{
		Scheme, "POST", "/api/v1/append-log?x=1",
		hex.EncodeToString(bodyHash[:]),
		parts["nonce"], parts["ts"], kid,
	}, "\n")
	sigBytes, err := base64.StdEncoding.DecodeString(parts["sig"])
	if err != nil {
		t.Fatal(err)
	}
	if !ed25519.Verify(pub, []byte(canonical), sigBytes) {
		t.Fatalf("signature did not verify")
	}
}

func parseAuthHeader(h string) map[string]string {
	out := map[string]string{}
	rest := strings.TrimPrefix(h, Scheme+" ")
	for _, kv := range strings.Split(rest, ",") {
		i := strings.IndexByte(kv, '=')
		if i <= 0 {
			continue
		}
		out[strings.TrimSpace(kv[:i])] = strings.TrimSpace(kv[i+1:])
	}
	return out
}
