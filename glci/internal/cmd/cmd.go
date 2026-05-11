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

	// Global --self-test short-circuits subcommand dispatch (§04 v1.2.0).
	for _, a := range args {
		if a == "--self-test" {
			return SelfTest(filterOut(args, "--self-test"))
		}
	}

	switch args[0] {
	case "ping":
		return Ping(args[1:])
	case "whoami":
		return Whoami(args[1:])
	case "keys":
		return Keys(args[1:])
	case "detect":
		return Detect(args[1:])
	case "lint":
		return RunCmd(args[1:], "lint")
	case "build":
		return RunCmd(args[1:], "build")
	case "test":
		return RunCmd(args[1:], "test")
	case "run":
		return RunCmd(args[1:], "")
	case "doctor":
		return Doctor(args[1:])
	case "config":
		if len(args) < 2 || args[1] != "print" {
			return errors.New("usage: glci config print [--cwd <dir>] [--config <file>]")
		}
		return ConfigPrint(args[2:])
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
	fmt.Println("  detect          Print phase plan + detected runtimes")
	fmt.Println("  lint|build|test Run a single phase across detected runtimes")
	fmt.Println("  run             CI/CD entry point (lint, build, test in one process)")
	fmt.Println("  doctor          Pre-flight environment checks")
	fmt.Println("  config print    Print resolved config with provenance (secrets redacted)")
	fmt.Println("  ping            Probe a Git Logs plugin /health endpoint")
	fmt.Println("  whoami          Authenticated identity probe (App Password OR Ed25519)")
	fmt.Println("  keys            Manage Ed25519 keys (generate)")
	fmt.Println("  version         Print glci version")
	fmt.Println("  help            Show this help")
}

func filterOut(xs []string, drop string) []string {
	out := make([]string, 0, len(xs))
	for _, x := range xs {
		if x != drop {
			out = append(out, x)
		}
	}
	return out
}
