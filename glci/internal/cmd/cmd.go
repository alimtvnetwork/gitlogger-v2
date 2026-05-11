// Package cmd dispatches glci subcommands.
package cmd

import (
	"errors"
	"fmt"
)

// Run dispatches to the requested subcommand.
func Run(args []string, version string) error {
	if len(args) == 0 {
		printUsage(version)
		return nil
	}

	switch args[0] {
	case "ping":
		return Ping(args[1:])
	case "version", "--version", "-v":
		fmt.Println("glci " + version)
		return nil
	case "help", "--help", "-h":
		printUsage(version)
		return nil
	default:
		return errors.New("unknown command: " + args[0] + " (try `glci help`)")
	}
}

func printUsage(version string) {
	fmt.Println("glci " + version + " — Universal CI CLI (spec/28)")
	fmt.Println()
	fmt.Println("Usage:")
	fmt.Println("  glci <command> [flags]")
	fmt.Println()
	fmt.Println("Commands:")
	fmt.Println("  ping       Probe a Git Logs plugin /health endpoint")
	fmt.Println("  version    Print glci version")
	fmt.Println("  help       Show this help")
}
