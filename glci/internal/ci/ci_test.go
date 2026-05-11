package ci

import (
	"errors"
	"testing"
)

func mapEnv(m map[string]string) func(string) string {
	return func(k string) string { return m[k] }
}

func TestHarvestEnv_GitHubActions(t *testing.T) {
	h, err := HarvestEnv(mapEnv(map[string]string{
		"GITHUB_ACTIONS":    "true",
		"GITHUB_SERVER_URL": "https://github.com",
		"GITHUB_REPOSITORY": "acme/widget",
		"GITHUB_REF_NAME":   "main",
		"GITHUB_SHA":        "deadbeef",
		"GITHUB_JOB":        "ci",
	}))
	if err != nil {
		t.Fatal(err)
	}
	if h.Provider != "github" {
		t.Errorf("provider: %q", h.Provider)
	}
	if h.RepoUrl != "https://github.com/acme/widget" {
		t.Errorf("repo url: %q", h.RepoUrl)
	}
	if h.Branch != "main" || h.GitSha256 != "deadbeef" || h.PipelineName != "ci" {
		t.Errorf("fields: %+v", h)
	}
}

func TestHarvestEnv_PRUsesHeadRef(t *testing.T) {
	h, err := HarvestEnv(mapEnv(map[string]string{
		"GITHUB_ACTIONS":    "true",
		"GITHUB_SERVER_URL": "https://github.com",
		"GITHUB_REPOSITORY": "a/b",
		"GITHUB_HEAD_REF":   "feature/x",
		"GITHUB_REF_NAME":   "merge-ref",
		"GITHUB_SHA":        "abc",
	}))
	if err != nil {
		t.Fatal(err)
	}
	if h.Branch != "feature/x" {
		t.Errorf("PR branch: want feature/x, got %q", h.Branch)
	}
}

func TestHarvestEnv_NoProvider(t *testing.T) {
	_, err := HarvestEnv(mapEnv(map[string]string{}))
	if !errors.Is(err, ErrNoProvider) {
		t.Fatalf("want ErrNoProvider, got %v", err)
	}
}

func TestNormalizeRepoURL(t *testing.T) {
	cases := map[string]string{
		"git@github.com:acme/widget.git":      "https://github.com/acme/widget",
		"https://github.com/acme/widget.git":  "https://github.com/acme/widget",
		"https://github.com/acme/widget/":     "https://github.com/acme/widget",
		"https://github.com/acme/widget":      "https://github.com/acme/widget",
		"":                                    "",
	}
	for in, want := range cases {
		if got := NormalizeRepoURL(in); got != want {
			t.Errorf("Normalize(%q)=%q want %q", in, got, want)
		}
	}
}
