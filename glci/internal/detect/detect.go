// Package detect implements language-runtime detection per spec/28 §03.
//
// Detection is lockfile- and manifest-based; never extension-based.
// Order is fixed (ts → go → php) for deterministic output of `glci detect`.
package detect

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
)

// Phase is one of "lint" | "build" | "test".
type Phase struct {
	Phase  string   `json:"Phase"`
	Runner string   `json:"Runner"`
	Args   []string `json:"Args"`
}

// Runtime represents a single detected runtime + its phase plan.
type Runtime struct {
	ID      string  `json:"Id"`
	Manager string  `json:"Manager,omitempty"`
	Phases  []Phase `json:"Phases"`
}

// Skipped is a runtime that did not match any marker.
type Skipped struct {
	ID     string `json:"Id"`
	Reason string `json:"Reason"`
}

// Result is the full detection output (stable JSON shape per §03).
type Result struct {
	Cwd      string    `json:"Cwd"`
	Runtimes []Runtime `json:"Runtimes"`
	Skipped  []Skipped `json:"Skipped"`
}

// ErrAmbiguousLock is GLCI-DETECT-AMBIGUOUS-LOCK (multiple JS lockfiles).
var ErrAmbiguousLock = errors.New("GLCI-DETECT-AMBIGUOUS-LOCK: multiple JS lockfiles present; pick one in glci.toml")

// ErrNoRuntime is GLCI-DETECT-NONE.
var ErrNoRuntime = errors.New("GLCI-DETECT-NONE: no runtime detected (need package.json, go.mod, or composer.json)")

// Detect inspects cwd and returns a Result.
func Detect(cwd string) (*Result, error) {
	abs, err := filepath.Abs(cwd)
	if err != nil {
		return nil, err
	}
	res := &Result{Cwd: abs}

	// ts
	if exists(abs, "package.json") {
		manager, err := pickJSManager(abs)
		if err != nil {
			return nil, err
		}
		res.Runtimes = append(res.Runtimes, tsRuntime(abs, manager))
	} else {
		res.Skipped = append(res.Skipped, Skipped{ID: "ts", Reason: "no package.json"})
	}

	// go
	if exists(abs, "go.mod") {
		res.Runtimes = append(res.Runtimes, goRuntime())
	} else {
		res.Skipped = append(res.Skipped, Skipped{ID: "go", Reason: "no go.mod"})
	}

	// php
	if exists(abs, "composer.json") {
		res.Runtimes = append(res.Runtimes, phpRuntime(abs))
	} else {
		res.Skipped = append(res.Skipped, Skipped{ID: "php", Reason: "no composer.json"})
	}

	if len(res.Runtimes) == 0 {
		return res, ErrNoRuntime
	}
	return res, nil
}

func exists(root, name string) bool {
	_, err := os.Stat(filepath.Join(root, name))
	return err == nil
}

func pickJSManager(root string) (string, error) {
	hits := 0
	mgr := "npm"
	if exists(root, "bun.lockb") || exists(root, "bun.lock") {
		mgr = "bun"
		hits++
	}
	if exists(root, "pnpm-lock.yaml") {
		mgr = "pnpm"
		hits++
	}
	if exists(root, "yarn.lock") {
		mgr = "yarn"
		hits++
	}
	if exists(root, "package-lock.json") {
		if hits == 0 {
			mgr = "npm"
		}
		hits++
	}
	if hits > 1 {
		return "", ErrAmbiguousLock
	}
	return mgr, nil
}

func tsRuntime(root, mgr string) Runtime {
	hasTSConfig := exists(root, "tsconfig.json")
	r := Runtime{ID: "ts", Manager: mgr}
	switch mgr {
	case "bun":
		r.Phases = []Phase{
			{"lint", "bun", []string{"x", "eslint", "."}},
			{"build", "bun", buildArgsTS(hasTSConfig, "bun")},
			{"test", "bun", []string{"test"}},
		}
	case "pnpm":
		r.Phases = []Phase{
			{"lint", "pnpm", []string{"exec", "eslint", "."}},
			{"build", "pnpm", buildArgsTS(hasTSConfig, "pnpm")},
			{"test", "pnpm", []string{"test"}},
		}
	case "yarn":
		r.Phases = []Phase{
			{"lint", "yarn", []string{"eslint", "."}},
			{"build", "yarn", buildArgsTS(hasTSConfig, "yarn")},
			{"test", "yarn", []string{"test"}},
		}
	default: // npm
		r.Phases = []Phase{
			{"lint", "npm", []string{"exec", "eslint", "--"}},
			{"build", "npm", buildArgsTS(hasTSConfig, "npm")},
			{"test", "npm", []string{"test"}},
		}
	}
	return r
}

func buildArgsTS(hasTSConfig bool, mgr string) []string {
	if hasTSConfig {
		switch mgr {
		case "bun":
			return []string{"x", "tsc", "--noEmit"}
		case "pnpm":
			return []string{"exec", "tsc", "--noEmit"}
		case "yarn":
			return []string{"tsc", "--noEmit"}
		case "npm":
			return []string{"exec", "tsc", "--", "--noEmit"}
		}
	}
	// fallback: run package.json build script
	switch mgr {
	case "bun", "yarn":
		return []string{"run", "build"}
	case "pnpm":
		return []string{"run", "build"}
	case "npm":
		return []string{"run", "build", "--if-present"}
	}
	return []string{"run", "build"}
}

func goRuntime() Runtime {
	return Runtime{
		ID: "go",
		Phases: []Phase{
			{"lint", "golangci-lint", []string{"run", "./..."}},
			{"build", "go", []string{"build", "./..."}},
			{"test", "go", []string{"test", "-race", "-count=1", "./..."}},
		},
	}
}

func phpRuntime(root string) Runtime {
	lint := Phase{Phase: "lint", Runner: "php", Args: []string{"-l", "src"}}
	if exists(root, "phpcs.xml") || exists(root, "phpcs.xml.dist") {
		lint = Phase{Phase: "lint", Runner: "phpcs", Args: nil}
	} else if exists(root, "phpstan.neon") || exists(root, "phpstan.neon.dist") {
		lint = Phase{Phase: "lint", Runner: "phpstan", Args: []string{"analyse"}}
	}
	return Runtime{
		ID: "php",
		Phases: []Phase{
			lint,
			{"build", "composer", []string{"dump-autoload", "--strict-psr"}},
			{"test", "phpunit", nil},
		},
	}
}

// JSON returns the deterministic JSON form of a Result.
func (r *Result) JSON() ([]byte, error) {
	return json.MarshalIndent(r, "", "  ")
}
