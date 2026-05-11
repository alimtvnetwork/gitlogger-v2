package classify

import (
	"regexp"
	"testing"
)

func TestClassify_DefaultErrors(t *testing.T) {
	cases := []string{
		"panic: runtime error: index out of range",
		"fatal error: all goroutines are asleep",
		"--- FAIL: TestThing (0.01s)",
		"Error: unable to open file",
		"unexpected syntax error near token",
	}
	for _, in := range cases {
		if got := Classify(in, nil, nil); got != Error {
			t.Errorf("expected Error for %q, got %v", in, got)
		}
	}
}

func TestClassify_DefaultWarns(t *testing.T) {
	cases := []string{
		"warning: ignoring deprecated flag",
		"this API is DEPRECATED",
	}
	for _, in := range cases {
		if got := Classify(in, nil, nil); got != Warn {
			t.Errorf("expected Warn for %q, got %v", in, got)
		}
	}
}

func TestClassify_Info(t *testing.T) {
	if got := Classify("build succeeded in 1.2s", nil, nil); got != Info {
		t.Errorf("expected Info, got %v", got)
	}
}

func TestClassify_ExtraPatternsTakePrecedenceOverInfo(t *testing.T) {
	extraErr := []*regexp.Regexp{regexp.MustCompile(`segfault`)}
	if got := Classify("kernel: segfault at 0x0", extraErr, nil); got != Error {
		t.Errorf("custom error pattern ignored, got %v", got)
	}
	extraWarn := []*regexp.Regexp{regexp.MustCompile(`(?i)slow query`)}
	if got := Classify("DB: slow query detected", nil, extraWarn); got != Warn {
		t.Errorf("custom warn pattern ignored, got %v", got)
	}
}

func TestClassify_ErrorBeatsWarn(t *testing.T) {
	// Line matches both "deprecated" (warn) and "FAIL" (error). Error must win.
	in := "FAIL: deprecated path used"
	if got := Classify(in, nil, nil); got != Error {
		t.Fatalf("error must take precedence, got %v", got)
	}
}
