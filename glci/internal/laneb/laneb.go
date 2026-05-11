// Package laneb implements §02 Lane B SSH-signed shipping.
//
// Lane B uses a detached ssh-keygen signature over the canonical
// JSON payload. Two modes are supported:
//
//   - Agent mode (default): delegate to the running ssh-agent via
//     `ssh-keygen -Y sign -n gitlogs -f <pubkey>` reading the payload
//     from stdin. This avoids touching private key material on disk.
//   - File mode: --ssh-key <path> uses the private key file directly.
//
// The signature (PEM-armored SSH SIG block) is sent in the
// `X-GL-SSH-Sig` header along with `X-GL-SSH-KeyId` (sha256:base64
// fingerprint of the public key).
package laneb

import (
	"bytes"
	"crypto/sha256"
	"encoding/base64"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

type SignResult struct {
	Signature string // PEM-armored SSHSIG block
	KeyID     string // sha256:<base64> fingerprint
}

type SignOptions struct {
	PublicKeyPath  string // ~/.ssh/id_ed25519.pub (required)
	PrivateKeyPath string // optional; if empty, use ssh-agent
	Namespace      string // default "gitlogs"
}

// Sign produces a detached SSH signature over payload. Requires the
// `ssh-keygen` binary in PATH (OpenSSH 8.0+).
func Sign(payload []byte, opts SignOptions) (*SignResult, error) {
	if opts.PublicKeyPath == "" {
		return nil, errors.New("GLCI-SSH-NO-PUBKEY: --ssh-pub <path> required")
	}
	if _, err := os.Stat(opts.PublicKeyPath); err != nil {
		return nil, fmt.Errorf("GLCI-SSH-PUBKEY-MISSING: %w", err)
	}
	ns := opts.Namespace
	if ns == "" {
		ns = "gitlogs"
	}

	args := []string{"-Y", "sign", "-n", ns, "-f", opts.PublicKeyPath}
	if opts.PrivateKeyPath != "" {
		args = []string{"-Y", "sign", "-n", ns, "-f", opts.PrivateKeyPath}
	}
	cmd := exec.Command("ssh-keygen", args...)
	cmd.Stdin = bytes.NewReader(payload)
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	if err := cmd.Run(); err != nil {
		return nil, fmt.Errorf("GLCI-SSH-SIGN-FAILED: %s: %w",
			strings.TrimSpace(stderr.String()), err)
	}

	pub, err := os.ReadFile(opts.PublicKeyPath)
	if err != nil {
		return nil, fmt.Errorf("GLCI-SSH-PUBKEY-READ: %w", err)
	}
	return &SignResult{
		Signature: stdout.String(),
		KeyID:     keyFingerprint(pub),
	}, nil
}

// keyFingerprint computes sha256:<base64> over the second whitespace
// field of an OpenSSH public key line ("ssh-ed25519 <b64> comment").
func keyFingerprint(pubLine []byte) string {
	parts := strings.Fields(strings.TrimSpace(string(pubLine)))
	if len(parts) < 2 {
		return ""
	}
	raw, err := base64.StdEncoding.DecodeString(parts[1])
	if err != nil {
		return ""
	}
	sum := sha256.Sum256(raw)
	return "sha256:" + base64.RawStdEncoding.EncodeToString(sum[:])
}
