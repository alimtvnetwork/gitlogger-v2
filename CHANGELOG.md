# Changelog

All notable changes to this project (the `git-logs` WordPress plugin and the
`glci` Go CLI) are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-05-12

Coherent version bump aligning the WordPress plugin and the `glci` CLI on a
single release line. No breaking API changes vs `0.4.x`.

### Added
- Landing site: `/docs` route, configurable repo URLs via `src/config/site.ts`,
  real Open Graph image (1200×630).
- `.github/dependabot.yml` — weekly grouped updates for Go modules, root npm,
  admin-UI npm, and GitHub Actions.
- `CHANGELOG.md` (this file).

### Changed
- Bumped `git-logs-plugin` to `0.5.0` (`Version:` header + `GIT_LOGS_VERSION`).
- Bumped `openapi.yaml` (plugin + glci copies) to `0.5.0`.
- Plugin `README.md` health-check example now reflects `0.5.0`.
- Footer + QuickStart on the landing site now read all repo URLs from
  `@/config/site`.

### Tests / CI
- Plugin: 48 stub REST/auth tests + 41 real PDO/SQLite DB tests, green across
  PHP 8.1–8.4 in `ci-wp-plugin.yml`.
- glci: ~78.6% Go coverage, race + lint gated in `ci-glci.yml`, Codecov upload.
- Admin UI: tsc + Vite build + Playwright E2E in `ci-admin-ui.yml`.

### Known limitations
- Live integration test against a hosted WordPress instance is still pending —
  blocked on operator-supplied infra.
- Real admin-UI screenshots on the landing page require a running WP install.

## [0.4.0] - prior

Initial code-complete release covering Phases P1–P8 (plugin skeleton, dual
auth lanes, SQLite schema, REST surface, glci CLI, shipping client +
self-test, admin UI + diagrams, streaming + Lane B + self-update + redaction
+ GoReleaser + SVN release workflow).

[0.5.0]: https://github.com/git-logs/git-logs/releases/tag/v0.5.0
[0.4.0]: https://github.com/git-logs/git-logs/releases/tag/v0.4.0
