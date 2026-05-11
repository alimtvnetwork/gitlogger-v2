package cmd

import (
	"context"
	"flag"
	"fmt"
	"os"

	"github.com/example/glci/internal/update"
)

// SelfUpdate implements `glci self-update`.
//
// Usage:
//
//	glci self-update --manifest <url> [--dry-run]
func SelfUpdate(args []string, currentVersion string) error {
	fs := flag.NewFlagSet("self-update", flag.ContinueOnError)
	manifestURL := fs.String("manifest", os.Getenv("GLCI_UPDATE_MANIFEST"),
		"Manifest URL (or set GLCI_UPDATE_MANIFEST)")
	dry := fs.Bool("dry-run", false, "Print the plan without applying")
	if err := fs.Parse(args); err != nil {
		return exitErr(64, err)
	}
	if *manifestURL == "" {
		return exitErr(2, fmt.Errorf("GLCI-UPDATE-NO-MANIFEST: --manifest or GLCI_UPDATE_MANIFEST required"))
	}

	ctx := context.Background()
	m, err := update.FetchManifest(ctx, *manifestURL)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return exitCode(5)
	}
	plan, err := update.BuildPlan(currentVersion, m)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return exitCode(5)
	}
	if !plan.Available {
		fmt.Printf("self-update: already on %s\n", plan.Current)
		return nil
	}
	fmt.Printf("self-update: %s → %s\n  url:    %s\n  sha256: %s\n  exe:    %s\n",
		plan.Current, plan.Target, plan.URL, plan.SHA256, plan.ExePath)
	if *dry {
		return nil
	}
	if err := update.Apply(ctx, plan); err != nil {
		fmt.Fprintln(os.Stderr, err)
		return exitCode(5)
	}
	fmt.Println("self-update: ok")
	return nil
}
