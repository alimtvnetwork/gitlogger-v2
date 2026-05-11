# Contributing

Thanks for helping out! Git Logs v2 is two codebases in one repo — the Go CLI
(`glci/`) and the WordPress plugin (`git-logs-plugin/`). Pick the half you're
touching and follow its dev loop.

## Ground rules

1. **Specs are the contract.** `spec/22..28/` define the wire format, exit
   codes, and security model. If you need to change a spec, do it in a
   dedicated PR before the implementation change.
2. **Tests are required.** Every behavioural change ships with unit coverage.
   See per-package test layouts under `glci/internal/*/` and
   `git-logs-plugin/tests/`.
3. **No silent divergence.** Surface server errors verbatim, keep error codes
   stable, never repurpose an exit code.
4. **Two auth lanes only.** App Passwords (Lane A) and Ed25519 (Lane B). Don't
   add a third without a spec amendment.

## Dev loop — `glci` (Go)

```sh
cd glci
go test ./... -race -cover                 # unit + e2e
bash scripts/coverage-gate.sh coverage.out # per-package floors
golangci-lint run                          # lint
go build ./...                             # build
```

- Add tests next to the code (`foo.go` → `foo_test.go`).
- New packages with non-trivial logic should land with a coverage floor in
  `glci/scripts/coverage-gate.sh`.
- The e2e harness in `glci/internal/e2e/` builds the binary once and exec's
  it against an httptest stub — keep new CLI commands smoke-tested there.

## Dev loop — WordPress plugin (PHP)

```sh
cd git-logs-plugin
php tests/run.php       # auth + REST suite (in-memory stubs)
php tests/run-db.php    # DB suite (real PDO/SQLite)
```

- Storage classes guard against double-loading with
  `if ( class_exists( __NAMESPACE__ . '\\X', false ) ) return;` so tests can
  pre-load stubs.
- Stubs live under `tests/stubs/`. Real PDO migrations live under
  `includes/db/migrations/`.

## Dev loop — Admin UI

```sh
cd git-logs-plugin/admin-ui
bun install
bun run dev               # local Vite, mounts admin.html harness
bun run build
bun x tsc --noEmit
bun x playwright test     # E2E (Docker image preferred — see ci-admin-ui.yml)
```

- Specs use the Playwright fixture pattern in `e2e/fixtures/` (canned API
  payloads via `window.__GL_FIXTURES__`).

## CI

| Workflow                        | Trigger                  |
|---------------------------------|--------------------------|
| `.github/workflows/ci-glci.yml`        | `glci/**` changes        |
| `.github/workflows/ci-wp-plugin.yml`   | `git-logs-plugin/**` changes (PHP) |
| `.github/workflows/ci-admin-ui.yml`    | `git-logs-plugin/admin-ui/**` changes |
| `.github/workflows/release-glci.yml`   | git tag `glci-v*`        |
| `.github/workflows/release-wp-plugin.yml` | git tag `plugin-v*`   |

A PR is mergeable when its relevant CI job is green. Coverage uploads to
Codecov use the `glci` flag for Go and `wp-plugin` for PHP.

## Pull request checklist

- [ ] Unit tests added/updated and passing locally
- [ ] Coverage gate passes (`glci/scripts/coverage-gate.sh`) for Go changes
- [ ] `tsc --noEmit` clean for admin-ui changes
- [ ] PHPUnit-lite suites pass for plugin changes
- [ ] Spec links cited in the PR description if the change touches the wire format
- [ ] `mem/implementation/phase-tracker.md` and a `POST-P8-N-*.md` acceptance
      file added if the change closes a backlog item

## Releasing

- **glci**: tag `glci-vX.Y.Z` → `release-glci.yml` builds cross-platform
  binaries and publishes the release.
- **plugin**: tag `plugin-vX.Y.Z` → `release-wp-plugin.yml` zips the plugin
  directory and publishes.

## Code of conduct

Be excellent to each other. Bug reports with reproductions get prioritised.
