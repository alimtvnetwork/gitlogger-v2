package cmd

import (
	"flag"
	"fmt"
	"os"

	"github.com/example/glci/internal/selfupdate"
)

// SelfUpdate implements `glci self-update`.
func SelfUpdate(args []string, version string) error {
	fs := flag.NewFlagSet("self-update", flag.ContinueOnError)
	repo := fs.String("repo", "", "GitHub owner/repo (default git-logs/glci)")
	dry := fs.Bool("dry-run", false, "Check for updates without installing")
	if err := fs.Parse(args); err != nil {
		return exitErr(64, err)
	}
	res, err := selfupdate.Run(selfupdate.Options{
		Repo: *repo, Current: version, DryRun: *dry,
	})
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return exitCode(5)
	}
	fmt.Println(res.Message)
	return nil
}
