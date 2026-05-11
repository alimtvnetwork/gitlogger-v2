package laneb

import (
	"crypto/ed25519"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

func TestKeyFingerprint_KnownVector(t *testing.T) {
	pub, _, err := ed25519.GenerateKey(rand.Reader)
	if err != nil {
		t.Fatal(err)
	}
	b64 := base64.StdEncoding.EncodeToString(pub)
	line := "ssh-ed25519 " + b64 + " user@host"
	got := keyFingerprint([]byte(line))
	sum := sha256.Sum256(pub)
	want := "sha256:" + base64.RawStdEncoding.EncodeToString(sum[:])
	if got != want {
		t.Errorf("fingerprint mismatch:\n got=%s\nwant=%s", got, want)
	}
}

func TestKeyFingerprint_BadInputReturnsEmpty(t *testing.T) {
	for _, in := range []string{"", "only-one-field", "ssh-ed25519 not-base64!!! comment"} {
		if got := keyFingerprint([]byte(in)); got != "" {
			t.Errorf("expected empty for %q, got %q", in, got)
		}
	}
}

func TestSign_PreflightNoPubkey(t *testing.T) {
	_, err := Sign([]byte("payload"), SignOptions{})
	if err == nil || !strings.Contains(err.Error(), "GLCI-SSH-NO-PUBKEY") {
		t.Fatalf("want GLCI-SSH-NO-PUBKEY, got %v", err)
	}
}

func TestSign_PreflightMissingPubkeyFile(t *testing.T) {
	_, err := Sign([]byte("payload"), SignOptions{PublicKeyPath: "/no/such/path.pub"})
	if err == nil || !strings.Contains(err.Error(), "GLCI-SSH-PUBKEY-MISSING") {
		t.Fatalf("want GLCI-SSH-PUBKEY-MISSING, got %v", err)
	}
}

func TestSign_FileModeRoundTrip(t *testing.T) {
	if _, err := exec.LookPath("ssh-keygen"); err != nil {
		t.Skip("ssh-keygen not in PATH")
	}
	dir := t.TempDir()
	priv := filepath.Join(dir, "id_ed25519")
	pub := priv + ".pub"
	out, err := exec.Command("ssh-keygen", "-t", "ed25519", "-N", "", "-f", priv, "-q").CombinedOutput()
	if err != nil {
		t.Skipf("ssh-keygen keygen failed (sandboxed?): %v: %s", err, out)
	}

	res, err := Sign([]byte("hello world"), SignOptions{
		PublicKeyPath:  pub,
		PrivateKeyPath: priv,
	})
	if err != nil {
		t.Fatalf("Sign: %v", err)
	}
	if !strings.Contains(res.Signature, "BEGIN SSH SIGNATURE") {
		t.Errorf("signature missing PEM header: %q", res.Signature)
	}
	if !strings.HasPrefix(res.KeyID, "sha256:") {
		t.Errorf("keyId not a sha256 fingerprint: %q", res.KeyID)
	}
	pubBytes, _ := os.ReadFile(pub)
	if got := keyFingerprint(pubBytes); got != res.KeyID {
		t.Errorf("fingerprint mismatch: got %s want %s", res.KeyID, got)
	}
}
