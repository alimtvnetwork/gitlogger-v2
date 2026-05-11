# Post-P8 #3 — Codecov + golangci-lint CI Badges

## Delivered
- `.github/workflows/ci-glci.yml` — runs `golangci-lint` and `go test -race -coverprofile` on every push/PR touching `glci/**`, then uploads `coverage.out` to Codecov.
- `glci/.golangci.yml` — pinned linter set (errcheck, govet, staticcheck, gosimple, ineffassign, unused, gofmt, goimports, misspell, revive, unconvert, bodyclose) with 5m timeout and `goimports` local-prefix matching the module path.
- Workflow gated by path filter so unrelated plugin/admin-UI changes don't trigger Go CI.

## Badges (paste into README)

```md
[![CI - glci](https://github.com/<OWNER>/<REPO>/actions/workflows/ci-glci.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/ci-glci.yml)
[![codecov](https://codecov.io/gh/<OWNER>/<REPO>/branch/main/graph/badge.svg?flag=glci)](https://codecov.io/gh/<OWNER>/<REPO>)
[![golangci-lint](https://img.shields.io/badge/golangci--lint-v1.61-blue)](https://golangci-lint.run/)
```

## Operator setup
1. Add `CODECOV_TOKEN` repo secret (only required for private repos; public repos work tokenless).
2. Replace `<OWNER>/<REPO>` in badges.
3. First push to `main` populates the badge.

## Acceptance
- ✅ Lint job runs `golangci-lint` v1.61 against `glci/`.
- ✅ Test job emits atomic-mode coverage profile and uploads to Codecov with `glci` flag.
- ✅ Path filter prevents noise from non-Go changes.
- ✅ Linter config matches module's import style (`goimports.local-prefixes`).
