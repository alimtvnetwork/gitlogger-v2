// Package classify partitions captured runner output into Logs[] vs ErrorLogs[]
// per spec/28 §09. Default heuristics; user patterns are merged additively.
package classify

import "regexp"

var defaultErrors = []*regexp.Regexp{
	regexp.MustCompile(`(?i)^panic:`),
	regexp.MustCompile(`(?i)^fatal error:`),
	regexp.MustCompile(`(?i)\bFAIL\b`),
	regexp.MustCompile(`(?i)^error:`),
	regexp.MustCompile(`(?i)\bsyntax error\b`),
}

var defaultWarns = []*regexp.Regexp{
	regexp.MustCompile(`(?i)^warning:`),
	regexp.MustCompile(`(?i)\bdeprecated\b`),
}

// Kind enumerates classification buckets.
type Kind int

const (
	Info Kind = iota
	Warn
	Error
)

// Classify returns the bucket for one line.
func Classify(line string, extraErr, extraWarn []*regexp.Regexp) Kind {
	for _, r := range defaultErrors {
		if r.MatchString(line) {
			return Error
		}
	}
	for _, r := range extraErr {
		if r.MatchString(line) {
			return Error
		}
	}
	for _, r := range defaultWarns {
		if r.MatchString(line) {
			return Warn
		}
	}
	for _, r := range extraWarn {
		if r.MatchString(line) {
			return Warn
		}
	}
	return Info
}
