// Package runner executes a phase command and captures interleaved
// stdout+stderr per spec/28 §04 (Behavior step 3, "stdout and stderr merged
// at the OS pipe level").
//
// Mechanism (normative): exec.Cmd.Stderr is set to exec.Cmd.Stdout so the
// kernel pipe FIFO orders bytes deterministically. NO PTY allocation; CI
// suppression env vars are set so runners avoid TTY-only output.
package runner

import (
	"bufio"
	"context"
	"io"
	"os"
	"os/exec"
	"time"
)

// Line is one captured line with a monotonic timestamp.
type Line struct {
	TS   time.Time
	Text string
}

// Result is the outcome of running a phase.
type Result struct {
	Runtime  string
	Phase    string
	Cmd      string
	Args     []string
	Lines    []Line
	ExitCode int
	Started  time.Time
	Ended    time.Time
}

// Run executes (cmd, args) inside cwd with merged stdout/stderr pipes.
// It returns a Result; non-zero ExitCode is reported, NOT returned as an error.
// An error return means failure to spawn or read pipes.
func Run(ctx context.Context, cwd, runtime, phase, cmd string, args []string) (*Result, error) {
	c := exec.CommandContext(ctx, cmd, args...)
	c.Dir = cwd
	c.Env = append(os.Environ(),
		"CI=true",
		"FORCE_COLOR=0",
		"NO_COLOR=1",
		"npm_config_progress=false",
		"NPM_CONFIG_PROGRESS=false",
	)

	pr, pw, err := os.Pipe()
	if err != nil {
		return nil, err
	}
	// Merge stderr into stdout at the OS pipe level — kernel FIFO preserves order.
	c.Stdout = pw
	c.Stderr = pw

	r := &Result{Runtime: runtime, Phase: phase, Cmd: cmd, Args: args, Started: time.Now()}

	if err := c.Start(); err != nil {
		_ = pw.Close()
		_ = pr.Close()
		return nil, err
	}
	// Close the writer in this process so the reader sees EOF when child exits.
	_ = pw.Close()

	// Read lines and timestamp at read time.
	br := bufio.NewReader(pr)
	for {
		line, err := br.ReadString('\n')
		if line != "" {
			r.Lines = append(r.Lines, Line{TS: time.Now(), Text: stripNL(line)})
		}
		if err == io.EOF {
			break
		}
		if err != nil {
			break
		}
	}

	werr := c.Wait()
	r.Ended = time.Now()
	if werr != nil {
		if ee, ok := werr.(*exec.ExitError); ok {
			r.ExitCode = ee.ExitCode()
		} else {
			r.ExitCode = -1
		}
	}
	return r, nil
}

func stripNL(s string) string {
	for len(s) > 0 && (s[len(s)-1] == '\n' || s[len(s)-1] == '\r') {
		s = s[:len(s)-1]
	}
	return s
}
