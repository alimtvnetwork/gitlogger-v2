// Package redact applies §09 secret scrubbing to log lines before
// they are shipped or printed. Patterns target common high-risk leaks:
// bearer tokens, GitHub PATs, AWS access keys, JWTs, and Lane B/A
// glci tokens.
package redact

import "regexp"

var patterns = []struct {
	re   *regexp.Regexp
	mask string
}{
	{regexp.MustCompile(`(?i)bearer\s+[A-Za-z0-9._\-]{16,}`), "bearer ***REDACTED***"},
	{regexp.MustCompile(`gh[pousr]_[A-Za-z0-9]{30,}`), "***GH-TOKEN-REDACTED***"},
	{regexp.MustCompile(`AKIA[0-9A-Z]{16}`), "***AWS-KEY-REDACTED***"},
	{regexp.MustCompile(`eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]{8,}`), "***JWT-REDACTED***"},
	{regexp.MustCompile(`(?i)x-gl-(?:temp)?token:\s*\S+`), "X-GL-Token: ***REDACTED***"},
	{regexp.MustCompile(`(?i)password["']?\s*[:=]\s*["']?[^\s"']{6,}`), "password=***REDACTED***"},
}

// Line scrubs a single log line.
func Line(s string) string {
	for _, p := range patterns {
		s = p.re.ReplaceAllString(s, p.mask)
	}
	return s
}

// Lines scrubs each entry in-place semantics (returns a new slice).
func Lines(in []string) []string {
	out := make([]string, len(in))
	for i, s := range in {
		out[i] = Line(s)
	}
	return out
}
