// Lane B (SSH-signed) shipping helpers.
//
// Signature contract (§02 Auth, GL-SSH-* errors):
//   1. Client requests a fresh nonce (handled by callers; nonce is opaque).
//   2. Client builds a canonical signing string:
//        "{method}\n{path}\n{nonce}\n{sha256(body)}"
//   3. Client signs with Ed25519 private key; sends:
//        X-GL-Sig:    base64(signature)
//        X-GL-Nonce:  <nonce>
//        X-GL-KeyId:  <fingerprint>
//
// On 401 GL-SSH-SIG-INVALID we MUST refresh the nonce ONCE and retry (R4).

package ship

import (
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/base64"
	"errors"
	"fmt"
)

// SignedHeaders carries the three Lane B headers a server expects.
type SignedHeaders struct {
	Sig   string // base64(signature)
	Nonce string
	KeyId string // public-key fingerprint
}

// Sign builds the canonical string and signs it with priv.
//
//	priv:   ed25519.PrivateKey (64 bytes)
//	method: HTTP verb (uppercase)
//	path:   request path including query, e.g. /append-log
//	nonce:  fresh server-issued nonce
//	body:   exact request body bytes (sha256 will be taken)
func Sign(priv ed25519.PrivateKey, keyId, method, path, nonce string, body []byte) (SignedHeaders, error) {
	if len(priv) != ed25519.PrivateKeySize {
		return SignedHeaders{}, errors.New("GL-SSH-KEY-INVALID: bad private key length")
	}
	if nonce == "" {
		return SignedHeaders{}, errors.New("GL-SSH-NONCE-MISSING")
	}
	digest := sha256.Sum256(body)
	canon := fmt.Sprintf("%s\n%s\n%s\n%x", method, path, nonce, digest)
	sig := ed25519.Sign(priv, []byte(canon))
	return SignedHeaders{
		Sig:   base64.StdEncoding.EncodeToString(sig),
		Nonce: nonce,
		KeyId: keyId,
	}, nil
}

// Verify is the inverse — exposed for the in-process self-test harness.
func Verify(pub ed25519.PublicKey, h SignedHeaders, method, path string, body []byte) error {
	sig, err := base64.StdEncoding.DecodeString(h.Sig)
	if err != nil {
		return fmt.Errorf("GL-SSH-SIG-INVALID: %w", err)
	}
	digest := sha256.Sum256(body)
	canon := fmt.Sprintf("%s\n%s\n%s\n%x", method, path, h.Nonce, digest)
	if !ed25519.Verify(pub, []byte(canon), sig) {
		return errors.New("GL-SSH-SIG-INVALID")
	}
	return nil
}
