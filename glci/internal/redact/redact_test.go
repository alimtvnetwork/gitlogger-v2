package redact

import "testing"

func TestLine_RedactsBearer(t *testing.T) {
	in := "Authorization: Bearer abcdef0123456789ABCDEF"
	got := Line(in)
	if got == in || !contains(got, "***REDACTED***") {
		t.Fatalf("bearer not redacted: %q", got)
	}
}

func TestLine_RedactsGitHubPAT(t *testing.T) {
	cases := []string{
		"ghp_" + repeat("A", 36),
		"gho_" + repeat("B", 36),
		"ghs_" + repeat("c", 36),
	}
	for _, in := range cases {
		got := Line(in)
		if !contains(got, "GH-TOKEN-REDACTED") {
			t.Errorf("GH token not redacted: %q -> %q", in, got)
		}
	}
}

func TestLine_RedactsAWSKey(t *testing.T) {
	in := "key=AKIAIOSFODNN7EXAMPLE here"
	got := Line(in)
	if !contains(got, "AWS-KEY-REDACTED") {
		t.Fatalf("AWS not redacted: %q", got)
	}
}

func TestLine_RedactsJWT(t *testing.T) {
	in := "token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c done"
	got := Line(in)
	if !contains(got, "JWT-REDACTED") {
		t.Fatalf("JWT not redacted: %q", got)
	}
}

func TestLine_RedactsPassword(t *testing.T) {
	in := `password="hunter2secret"`
	got := Line(in)
	if !contains(got, "REDACTED") {
		t.Fatalf("password not redacted: %q", got)
	}
}

func TestLine_LeavesSafeText(t *testing.T) {
	in := "all systems nominal, no secrets here"
	if got := Line(in); got != in {
		t.Fatalf("safe line mutated: %q -> %q", in, got)
	}
}

func TestLines_AppliesToEach(t *testing.T) {
	in := []string{"Bearer " + repeat("x", 32), "ok"}
	out := Lines(in)
	if out[0] == in[0] {
		t.Errorf("first line not scrubbed")
	}
	if out[1] != "ok" {
		t.Errorf("second line mutated unexpectedly: %q", out[1])
	}
}

// helpers
func contains(s, sub string) bool {
	for i := 0; i+len(sub) <= len(s); i++ {
		if s[i:i+len(sub)] == sub {
			return true
		}
	}
	return false
}

func repeat(s string, n int) string {
	out := make([]byte, 0, len(s)*n)
	for i := 0; i < n; i++ {
		out = append(out, s...)
	}
	return string(out)
}
