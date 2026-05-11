// Package main is the entrypoint for the `glci` Universal CI CLI (spec/28).
//
// Phase 1 walking skeleton: only the `ping` command is wired. It performs an
// unauthenticated GET against the WP plugin's /wp-json/git-logs/v1/health
// endpoint and prints the JSON body. Future phases add auth (App Password),
// run submission, status, diagram, config, and the generic runtime (spec/13–16).
package main

import (
	"fmt"
	"os"

	"github.com/example/glci/internal/cmd"
)

// Version is the glci CLI version. Overridden at link time via -ldflags.
var Version = "0.2.0-dev"

func main() {
	if err := cmd.Run(os.Args[1:], Version); err != nil {
		fmt.Fprintln(os.Stderr, "glci: "+err.Error())
		os.Exit(1)
	}
}
