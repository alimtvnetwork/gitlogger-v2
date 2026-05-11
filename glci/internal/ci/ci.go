// Package ci harvests CI-provider environment per spec/28 §08.
//
// v2 ships GitHub Actions ONLY (per §00 Scope + AC-28-47).
// Non-GitHub bindings are deferred to v3.
package ci

import (
	"errors"
	"os"
	"strings"
)

// Harvest holds the four canonical fields the server expects.
type Harvest struct {
	Provider     string
	RepoUrl      string
	Branch       string
	GitSha256    string
	PipelineName string
}

// ErrNoProvider is GLCI-DETECT-NONE-CI.
var ErrNoProvider = errors.New("GLCI-DETECT-NONE-CI: no supported CI provider detected (v2 supports GitHub Actions only)")

// HarvestEnv inspects environment variables and returns a Harvest.
// Returns ErrNoProvider if no supported CI provider is detected and no
// override has been provided.
func HarvestEnv(getenv func(string) string) (*Harvest, error) {
	if getenv == nil {
		getenv = os.Getenv
	}
	if strings.EqualFold(getenv("GITHUB_ACTIONS"), "true") {
		return &Harvest{
			Provider:     "github",
			RepoUrl:      NormalizeRepoURL(joinURL(getenv("GITHUB_SERVER_URL"), getenv("GITHUB_REPOSITORY"))),
			Branch:       firstNonEmpty(getenv("GITHUB_HEAD_REF"), getenv("GITHUB_REF_NAME")),
			GitSha256:    getenv("GITHUB_SHA"),
			PipelineName: getenv("GITHUB_JOB"),
		}, nil
	}
	return nil, ErrNoProvider
}

// NormalizeRepoURL converts SSH or trailing-slash forms to canonical HTTPS.
//
//	git@github.com:org/repo.git    → https://github.com/org/repo
//	https://github.com/org/repo.git → https://github.com/org/repo
//	https://github.com/org/repo/    → https://github.com/org/repo
func NormalizeRepoURL(in string) string {
	if in == "" {
		return ""
	}
	s := strings.TrimSpace(in)
	if strings.HasPrefix(s, "git@") {
		// git@host:org/repo(.git)
		if i := strings.Index(s, ":"); i > 4 {
			host := s[len("git@"):i]
			path := s[i+1:]
			s = "https://" + host + "/" + path
		}
	}
	s = strings.TrimSuffix(s, "/")
	s = strings.TrimSuffix(s, ".git")
	return s
}

func joinURL(base, repo string) string {
	if base == "" || repo == "" {
		return ""
	}
	return strings.TrimRight(base, "/") + "/" + strings.TrimLeft(repo, "/")
}

func firstNonEmpty(vals ...string) string {
	for _, v := range vals {
		if v != "" {
			return v
		}
	}
	return ""
}
