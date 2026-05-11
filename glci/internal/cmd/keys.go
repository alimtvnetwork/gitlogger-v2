package cmd

import (
	"encoding/base64"
	"errors"
	"flag"
	"fmt"
	"os"

	"github.com/example/glci/internal/auth"
)

// Keys handles `glci keys <subcommand>`. Phase 2 ships only `generate`.
//
//	glci keys generate --out ~/.glci/key --label "ci-runner"
//
// Writes two files:
//
//	<out>       — private seed file (mode 0600), prefix "glci-ed25519-priv "
//	<out>.pub   — public key file,                prefix "glci-ed25519 "
//
// The .pub line is what you POST to /wp-json/git-logs/v1/keys to register.
// The keyId is generated server-side; this command also prints a suggested
// local keyId you can pass to the server when registering, but the
// authoritative id is whatever the plugin returns.
func Keys(args []string) error {
	if len(args) == 0 {
		return errors.New("usage: glci keys generate --out <path> [--label <text>]")
	}
	switch args[0] {
	case "generate":
		return keysGenerate(args[1:])
	default:
		return fmt.Errorf("unknown keys subcommand: %s", args[0])
	}
}

func keysGenerate(args []string) error {
	fs := flag.NewFlagSet("keys generate", flag.ContinueOnError)
	out := fs.String("out", "", "Output path for the private seed file (required)")
	label := fs.String("label", "glci-key", "Human-readable label (printed to stderr only)")
	if err := fs.Parse(args); err != nil {
		return err
	}
	if *out == "" {
		return errors.New("`--out` is required")
	}

	seed, pub, suggestedID, err := auth.GenerateKeypair()
	if err != nil {
		return err
	}

	privLine := auth.PrivPrefix + base64.StdEncoding.EncodeToString(seed) + "\n"
	pubLine := auth.PubPrefix + base64.StdEncoding.EncodeToString(pub) + "\n"

	if err := os.WriteFile(*out, []byte(privLine), 0o600); err != nil {
		return err
	}
	if err := os.WriteFile(*out+".pub", []byte(pubLine), 0o644); err != nil {
		return err
	}

	fmt.Fprintf(os.Stderr, "label:           %s\n", *label)
	fmt.Fprintf(os.Stderr, "private (kept):  %s   (mode 0600)\n", *out)
	fmt.Fprintf(os.Stderr, "public  (share): %s.pub\n", *out)
	fmt.Fprintf(os.Stderr, "suggested keyId: %s   (server may assign its own)\n", suggestedID)
	fmt.Fprintln(os.Stderr)
	fmt.Fprintln(os.Stderr, "Register the public key:")
	fmt.Fprintf(os.Stderr, `  curl -u USER:APP_PASSWORD -X POST $BASE/wp-json/git-logs/v1/keys \
    -H 'Content-Type: application/json' \
    -d "{\"label\":\"%s\",\"pubkey_b64\":\"%s\"}"`+"\n",
		*label, base64.StdEncoding.EncodeToString(pub))
	return nil
}
