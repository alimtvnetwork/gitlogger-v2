// Package main is the entrypoint for the `glci` Universal CI CLI (spec/28).
//
// Phase 5 wires the full command surface: detect, lint, build, test, run,
// doctor, config print — backed by lockfile-based runtime detection
// (internal/detect), GitHub Actions env harvest (internal/ci), config
// resolution (internal/config), and a kernel-pipe-merged runner
// (internal/runner). Shipping (POST /events, /finalize) and the SSH auth
// lane remain stubbed pending the shipping client phase.
package main

import (
	"fmt"
	"os"

	"github.com/example/glci/internal/cmd"
)

// Version is the glci CLI version. Overridden at link time via -ldflags.
var Version = "0.8.0-dev"

func main() {
	err := cmd.Run(os.Args[1:], Version)
	if err != nil {
		fmt.Fprintln(os.Stderr, "glci: "+err.Error())
		os.Exit(cmd.CodeOf(err))
	}
}
