# Changelog

All notable changes to this project are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [SemVer](https://semver.org/spec/v2.0.0.html).

## [0.5.0] — 2026-05-12

### Added
- **Public landing page** at `/` (TanStack Start route) — hero, feature grid,
  3-step "How it works" with copy-pasteable GitHub Actions YAML, tabbed
  screenshots gallery (Dashboard, Run detail, Repos, Diagrams, Audit log),
  3-tab quick-start installer, requirements + 8-question FAQ, footer.
- **SEO**: per-route `<head>` metadata, canonical URL, OpenGraph and
  Twitter cards, JSON-LD `SoftwareApplication` structured data.
- **CI status badges** in root `README.md` for both halves
  (glci, WP plugin, admin UI, releases, license, version).
- `PHASE-LANDING-ACCEPTANCE.md` documenting the 8-phase landing build.

### Changed
- `git-logs-plugin/git-logs.php` `Plugin URI` updated from
  `https://example.com/git-logs` → `https://github.com/git-logs/wp-plugin`.
- Plugin version bumped `0.4.0 → 0.5.0` (`Version:` header and
  `GIT_LOGS_VERSION` constant in `git-logs-plugin/git-logs.php`).
- README and landing-page version markers bumped `0.4.0 → 0.5.0`.

### Notes
- `SITE_URL` constant in `src/routes/index.tsx` is currently the placeholder
  `https://gitlogs.dev`. Swap when the production domain is decided.
- Mocked screenshots in the gallery should be replaced with real WP-Admin
  captures once the plugin is deployed somewhere public.

## [0.4.0] — 2026-04-29

### Added
- All P1–P8 implementation phases (WP plugin REST surface, glci CLI,
  admin UI, Lane B Ed25519 auth, audit log, streaming events).
- Post-P8 hardening: PHP test harness, Go coverage gates, Playwright E2E
  scaffolding, top-level READMEs, GPL-2.0/MIT licenses, GitHub
  issue/PR templates.

See `mem/implementation/phase-tracker.md` for the full P1–P8 + post-P8 log.
