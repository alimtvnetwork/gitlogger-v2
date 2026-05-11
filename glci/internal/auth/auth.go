// Package auth implements the two glci client-side auth lanes:
//
//   1. WP App Password (HTTP Basic) — pass --user / --app-password (or env
//      GLCI_USER / GLCI_APP_PASSWORD). The plugin relies on WP core to validate.
//
//   2. Ed25519 signed request — pass --key-id and --key-file (or env
//      GLCI_KEY_ID / GLCI_KEY_FILE). Signs the canonical request string and
//      sets the X-GitLogs-Auth header.
//
// Canonical signing string (LF-separated, no trailing LF):
//
//	GLCI1-ED25519
//	<METHOD>
//	<PATH-AND-QUERY>
//	<SHA256_HEX_OF_BODY>
//	<NONCE>
//	<TIMESTAMP>
//	<KEY_ID>
//
// Key file format (32-byte private seed → produces 64-byte ed25519 priv):
//
//	first non-empty line: "glci-ed25519-priv " <base64 of 32-byte seed>
//
// The matching public file (uploaded to the plugin via POST /keys):
//
//	first non-empty line: "glci-ed25519 " <base64 of 32-byte pubkey>
package auth

import (
	"crypto/ed25519"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"
)

const (
	Scheme         = "GLCI1-ED25519"
	PrivPrefix     = "glci-ed25519-priv "
	PubPrefix      = "glci-ed25519 "
	NonceByteLen   = 18 // → 24-char base64 (no padding)
	tsWindowSecs   = 300
)

// Mode selects which lane to use.
type Mode int

const (
	ModeNone Mode = iota
	ModeAppPassword
	ModeEd25519
)

// Config carries lane parameters resolved from flags + env.
type Config struct {
	Mode         Mode
	User         string // App Password lane
	AppPassword  string // App Password lane
	KeyID        string // Ed25519 lane
	PrivateSeed  []byte // 32-byte seed, Ed25519 lane
}

// FromEnv fills missing fields from GLCI_* env vars and selects a mode.
// Precedence: explicit Mode > Ed25519 (if KeyID+PrivateSeed) > AppPassword (if User+AppPassword) > None.
func (c *Config) Resolve() error {
	if c.User == "" {
		c.User = os.Getenv("GLCI_USER")
	}
	if c.AppPassword == "" {
		c.AppPassword = os.Getenv("GLCI_APP_PASSWORD")
	}
	if c.KeyID == "" {
		c.KeyID = os.Getenv("GLCI_KEY_ID")
	}
	if len(c.PrivateSeed) == 0 {
		if path := os.Getenv("GLCI_KEY_FILE"); path != "" {
			seed, err := LoadPrivateSeed(path)
			if err != nil {
				return err
			}
			c.PrivateSeed = seed
		}
	}
	if c.Mode == ModeNone {
		switch {
		case c.KeyID != "" && len(c.PrivateSeed) == 32:
			c.Mode = ModeEd25519
		case c.User != "" && c.AppPassword != "":
			c.Mode = ModeAppPassword
		}
	}
	return nil
}

// Apply mutates req to carry credentials per the configured lane.
// For Ed25519 it must be called AFTER req.Body is finalized — it reads the body
// to compute the signature, then resets it.
func (c *Config) Apply(req *http.Request) error {
	switch c.Mode {
	case ModeNone:
		return errors.New("no auth configured: set --user/--app-password OR --key-id/--key-file (or GLCI_* env)")
	case ModeAppPassword:
		req.SetBasicAuth(c.User, c.AppPassword)
		return nil
	case ModeEd25519:
		return c.signEd25519(req)
	default:
		return fmt.Errorf("unknown auth mode: %d", c.Mode)
	}
}

func (c *Config) signEd25519(req *http.Request) error {
	if len(c.PrivateSeed) != 32 {
		return errors.New("ed25519 private seed must be 32 bytes")
	}
	priv := ed25519.NewKeyFromSeed(c.PrivateSeed)

	body, err := readAndResetBody(req)
	if err != nil {
		return err
	}
	bodyHash := sha256.Sum256(body)
	bodyHashHex := hex.EncodeToString(bodyHash[:])

	nonce, err := randomNonce()
	if err != nil {
		return err
	}
	ts := strconv.FormatInt(time.Now().Unix(), 10)

	pathAndQuery := req.URL.RequestURI() // path + "?" + query
	if !strings.HasPrefix(pathAndQuery, "/") {
		// http.Request to absolute URL → URL.Path may be empty; force "/".
		u, _ := url.Parse(req.URL.String())
		pathAndQuery = u.RequestURI()
	}

	canonical := strings.Join([]string{
		Scheme,
		strings.ToUpper(req.Method),
		pathAndQuery,
		bodyHashHex,
		nonce,
		ts,
		c.KeyID,
	}, "\n")

	sig := ed25519.Sign(priv, []byte(canonical))
	header := fmt.Sprintf("%s keyId=%s,nonce=%s,ts=%s,sig=%s",
		Scheme, c.KeyID, nonce, ts, base64.StdEncoding.EncodeToString(sig))
	req.Header.Set("X-GitLogs-Auth", header)
	return nil
}

func readAndResetBody(req *http.Request) ([]byte, error) {
	if req.Body == nil {
		return nil, nil
	}
	b, err := io.ReadAll(req.Body)
	if err != nil {
		return nil, err
	}
	_ = req.Body.Close()
	req.Body = io.NopCloser(strings.NewReader(string(b)))
	req.ContentLength = int64(len(b))
	return b, nil
}

func randomNonce() (string, error) {
	buf := make([]byte, NonceByteLen)
	if _, err := rand.Read(buf); err != nil {
		return "", err
	}
	return base64.RawURLEncoding.EncodeToString(buf), nil
}

// GenerateKeypair produces a fresh Ed25519 keypair and returns
// (privateSeed32, publicKey32, keyId8hex).
func GenerateKeypair() (seed, pub []byte, keyID string, err error) {
	pubK, privK, err := ed25519.GenerateKey(rand.Reader)
	if err != nil {
		return nil, nil, "", err
	}
	seed = make([]byte, 32)
	copy(seed, privK.Seed())
	pub = []byte(pubK)

	idBytes := make([]byte, 4)
	if _, err := rand.Read(idBytes); err != nil {
		return nil, nil, "", err
	}
	return seed, pub, hex.EncodeToString(idBytes), nil
}

// LoadPrivateSeed reads a key file and returns the 32-byte seed.
func LoadPrivateSeed(path string) ([]byte, error) {
	raw, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	for _, line := range strings.Split(string(raw), "\n") {
		line = strings.TrimSpace(line)
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		if !strings.HasPrefix(line, PrivPrefix) {
			return nil, fmt.Errorf("expected first non-empty line to start with %q", PrivPrefix)
		}
		seedB64 := strings.TrimPrefix(line, PrivPrefix)
		seed, err := base64.StdEncoding.DecodeString(seedB64)
		if err != nil {
			return nil, fmt.Errorf("decode seed base64: %w", err)
		}
		if len(seed) != 32 {
			return nil, fmt.Errorf("seed must be 32 bytes, got %d", len(seed))
		}
		return seed, nil
	}
	return nil, errors.New("no key line found in file")
}
