package cmd

import (
	"errors"
	"reflect"
	"strings"
	"testing"
)

func TestCodeOf(t *testing.T) {
	if CodeOf(nil) != 0 {
		t.Errorf("CodeOf(nil) = %d, want 0", CodeOf(nil))
	}
	if got := CodeOf(errors.New("plain")); got != 1 {
		t.Errorf("CodeOf(plain) = %d, want 1", got)
	}
	ce := exitErr(7, errors.New("boom"))
	if got := CodeOf(ce); got != 7 {
		t.Errorf("CodeOf(exitErr 7) = %d, want 7", got)
	}
	if msg := ce.Error(); msg != "boom" {
		t.Errorf("Error() = %q, want %q", msg, "boom")
	}
	if c := ce.(*cmdErr).Code(); c != 7 {
		t.Errorf("Code() = %d, want 7", c)
	}
}

func TestExitCode(t *testing.T) {
	if err := exitCode(0); err != nil {
		t.Errorf("exitCode(0) should be nil, got %v", err)
	}
	err := exitCode(3)
	if err == nil || CodeOf(err) != 3 {
		t.Errorf("exitCode(3) wrong: %v", err)
	}
}

func TestFilterOut(t *testing.T) {
	got := filterOut([]string{"a", "x", "b", "x", "c"}, "x")
	want := []string{"a", "b", "c"}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("filterOut = %v, want %v", got, want)
	}
	if got := filterOut(nil, "x"); len(got) != 0 {
		t.Errorf("filterOut(nil) = %v, want empty", got)
	}
	if got := filterOut([]string{"a", "b"}, "z"); !reflect.DeepEqual(got, []string{"a", "b"}) {
		t.Errorf("filterOut no-match = %v", got)
	}
}

func TestContains(t *testing.T) {
	if !contains([]string{"a", "b", "c"}, "b") {
		t.Error("contains: missed 'b'")
	}
	if contains([]string{"a", "b"}, "z") {
		t.Error("contains: false positive on 'z'")
	}
	if contains(nil, "x") {
		t.Error("contains(nil) should be false")
	}
}

func TestRunHelpAndVersion(t *testing.T) {
	for _, args := range [][]string{
		{},
		{"help"}, {"--help"}, {"-h"},
		{"version"}, {"--version"}, {"-v"},
	} {
		if err := Run(args, "1.2.3"); err != nil {
			t.Errorf("Run(%v) = %v, want nil", args, err)
		}
	}
}

func TestRunUnknownCommand(t *testing.T) {
	err := Run([]string{"frobnicate"}, "0.0.0")
	if err == nil {
		t.Fatal("expected error for unknown command")
	}
	if !strings.Contains(err.Error(), "unknown command") {
		t.Errorf("error = %q, want contains 'unknown command'", err.Error())
	}
}

func TestRunConfigPrintRequiresPrintSub(t *testing.T) {
	if err := Run([]string{"config"}, "0"); err == nil {
		t.Error("`config` without subcommand should error")
	}
	if err := Run([]string{"config", "bogus"}, "0"); err == nil {
		t.Error("`config bogus` should error")
	}
}
