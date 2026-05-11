package runner

import (
	"context"
	"os/exec"
	"runtime"
	"strings"
	"testing"
	"time"
)

func skipIfNoSh(t *testing.T) {
	t.Helper()
	if runtime.GOOS == "windows" {
		t.Skip("POSIX shell not available on Windows runner")
	}
	if _, err := exec.LookPath("sh"); err != nil {
		t.Skip("sh not in PATH")
	}
}

func TestRun_CapturesStdoutAndStderrInOrder(t *testing.T) {
	skipIfNoSh(t)
	r, err := Run(context.Background(), "", "ts", "lint",
		"sh", []string{"-c", "echo first; echo second 1>&2; echo third"})
	if err != nil {
		t.Fatal(err)
	}
	if r.ExitCode != 0 {
		t.Errorf("exit code: %d", r.ExitCode)
	}
	if len(r.Lines) != 3 {
		t.Fatalf("want 3 lines, got %d: %+v", len(r.Lines), r.Lines)
	}
	for i, w := range []string{"first", "second", "third"} {
		if r.Lines[i].Text != w {
			t.Errorf("line %d: want %q got %q", i, w, r.Lines[i].Text)
		}
	}
}

func TestRun_NonZeroExitReported(t *testing.T) {
	skipIfNoSh(t)
	r, err := Run(context.Background(), "", "go", "test",
		"sh", []string{"-c", "echo boom; exit 7"})
	if err != nil {
		t.Fatal(err)
	}
	if r.ExitCode != 7 {
		t.Errorf("want exit 7, got %d", r.ExitCode)
	}
	if len(r.Lines) != 1 || r.Lines[0].Text != "boom" {
		t.Errorf("output: %+v", r.Lines)
	}
}

func TestRun_StripsTrailingNewlinesAndCRs(t *testing.T) {
	skipIfNoSh(t)
	r, err := Run(context.Background(), "", "x", "x",
		"sh", []string{"-c", "printf 'a\\r\\nb\\n'"})
	if err != nil {
		t.Fatal(err)
	}
	if len(r.Lines) != 2 || r.Lines[0].Text != "a" || r.Lines[1].Text != "b" {
		t.Errorf("CR/LF not stripped: %+v", r.Lines)
	}
}

func TestRun_RecordsTimestamps(t *testing.T) {
	skipIfNoSh(t)
	r, err := Run(context.Background(), "", "x", "x",
		"sh", []string{"-c", "echo hi"})
	if err != nil {
		t.Fatal(err)
	}
	if r.Started.IsZero() || r.Ended.IsZero() {
		t.Errorf("missing timestamps")
	}
	if r.Ended.Before(r.Started) {
		t.Errorf("ended before started")
	}
}

func TestRun_SetsCIEnvForChild(t *testing.T) {
	skipIfNoSh(t)
	r, err := Run(context.Background(), "", "x", "x",
		"sh", []string{"-c", "echo CI=$CI NO_COLOR=$NO_COLOR"})
	if err != nil {
		t.Fatal(err)
	}
	if len(r.Lines) == 0 || !strings.Contains(r.Lines[0].Text, "CI=true") || !strings.Contains(r.Lines[0].Text, "NO_COLOR=1") {
		t.Errorf("CI env not applied: %+v", r.Lines)
	}
}

func TestRun_SpawnFailureReturnsError(t *testing.T) {
	_, err := Run(context.Background(), "", "x", "x",
		"definitely-not-a-real-binary-xyz", nil)
	if err == nil {
		t.Fatal("expected spawn error")
	}
}

func TestRun_ContextCancellationStopsChild(t *testing.T) {
	skipIfNoSh(t)
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()
	r, err := Run(ctx, "", "x", "x", "sh", []string{"-c", "sleep 5; echo done"})
	if err != nil {
		t.Fatal(err)
	}
	if r.ExitCode == 0 {
		t.Errorf("expected non-zero on cancelled child, got %d", r.ExitCode)
	}
}

func TestStripNL(t *testing.T) {
	cases := map[string]string{
		"abc\n":    "abc",
		"abc\r\n":  "abc",
		"abc":      "abc",
		"abc\n\n":  "abc",
		"":         "",
		"a\rb\r\n": "a\rb",
	}
	for in, want := range cases {
		if got := stripNL(in); got != want {
			t.Errorf("stripNL(%q)=%q want %q", in, got, want)
		}
	}
}
