# Git Logs v2

Self-hosted CI run capture, audit, and diff — built as two halves that talk
over a small REST contract:

- **[`glci/`](./glci/)** — Universal CI CLI (Go). Detects your runtime, runs
  lint/build/test, ships the output. [→ glci README](./glci/README.md)
- **[`git-logs-plugin/`](./git-logs-plugin/)** — WordPress plugin (PHP 8.1+).
  Ingests runs, persists per-SHA SQLite stores, exposes a React admin UI.
  [→ plugin README](./git-logs-plugin/README.md)

```
┌──────────────┐   detect → lint → build → test    ┌──────────────────┐
│  your repo   │ ────────────────────────────────► │  glci CLI (Go)   │
└──────────────┘                                   └────────┬─────────┘
                                                            │ POST /append-log
                                                            ▼
                                                   ┌──────────────────┐
                                                   │ Git Logs plugin  │
                                                   │  (WordPress)     │
                                                   └──────────────────┘
```

## Repository layout

```
glci/                    Go CLI (spec/28)
  internal/              cmd, ship, runner, detect, ci, config, auth, …
  scripts/               coverage gate + smoke harness
git-logs-plugin/         WordPress plugin (spec/22..26)
  includes/              REST controllers, auth, db storage
  admin-ui/              Vite + React admin app, Playwright E2E
  tests/                 PHPUnit-lite suites (auth, REST, DB)
spec/22..28/             Reference specs (read-only requirements)
.github/workflows/       CI for both halves + release pipelines
```

## Specs

Implementation tracks `spec/22..28/`. Treat the specs as the source of truth
for the wire contract, exit codes, and security model. The implementation may
extend them but never silently diverge.

## Quickstart

1. **Stand up the plugin** — install on a WordPress 6.5+ site with PHP 8.1+
   (`pdo_sqlite`, `sodium`). See [plugin README](./git-logs-plugin/README.md).
2. **Install the CLI** — `go install` or grab a release binary.
   See [glci README](./glci/README.md).
3. **Wire CI** — call `glci run --base https://your-site.example.com …` from
   your pipeline; runs land in WP Admin → Git Logs.

## Status

All eight implementation phases (P1–P8) and a post-P8 hardening backlog are
done. See [`mem/implementation/phase-tracker.md`](./mem/implementation/phase-tracker.md)
for the running record and `POST-P8-*.md` for per-task acceptance notes.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

GPL-2.0-or-later for both halves.
