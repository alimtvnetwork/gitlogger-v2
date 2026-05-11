# Implementation Plan — Git Logs v2 + glci + Generic Runtime

## Stack (locked)

| Component | Language | Repo | Source spec |
|---|---|---|---|
| WP Git Logs plugin (backend: REST + SQLite + auth) | PHP 8.1+, PSR-4/PSR-12 | `git-logs-plugin/` (new) | spec/22, spec/23 |
| Admin UI bundle (loaded into wp-admin page) | TypeScript + React + Vite | inside plugin repo (`/admin-ui`) | spec/24, spec/26 |
| `glci` Universal CI CLI | Go 1.22+ | `glci/` (new) | spec/28 |
| Generic CLI runtime (update, install, status) | Go 1.22+ | shared Go module in `glci/` | spec/13, spec/14, spec/15, spec/16 (referenced by spec/28) |
| Spec corpus + linter-scripts | unchanged | this repo | spec/22..28 (frozen scope) |

Memory note: this turn lifts the "spec-only" lock because you said "implementation". Spec edits still respect the 7-folder scope lock.

## Architecture (one diagram)

```text
  ┌──────────────────┐  WP App-Password / SSH-key signed
  │ glci (Go CLI)    │ ───────────────────────────────► ┌──────────────────────┐
  └──────────────────┘                                  │  WP Git Logs plugin  │
  ┌──────────────────┐  fetch (same-origin, WP nonce)   │  PHP · REST · SQLite │
  │ wp-admin UI (TS) │ ───────────────────────────────► │  10 endpoints        │
  └──────────────────┘                                  └──────────────────────┘
                                                              │
                                                              ▼
                                                     root.sqlite + per-SHA *.sqlite
```

No Go backend. No standalone dashboard. WP plugin is the single source of truth.

## Phase 1 — Walking skeleton (MVP)

Goal: end-to-end "hello world" across all four components. **One** REST endpoint, **one** CLI command, **one** UI page.

- `git-logs-plugin/`: PHP plugin scaffold, activates in WP, registers `/wp-json/gitlogs/v1/health`, opens root SQLite on activate, runs migration #1 (one table).
- `glci/`: Go module, `glci ping <wp-url>` calls `/health` with App Password auth, prints OK.
- `admin-ui/`: Vite + React, builds to `plugin/build/`, plugin enqueues bundle on a "Git Logs" wp-admin page that hits `/health` and renders status.
- CI: GitHub Actions per repo — `phpcs` + `phpstan` for plugin, `go test ./... + golangci-lint` for CLI, `tsc + vitest` for UI.

Acceptance: fresh WordPress install + plugin activation + `glci ping` + admin page = green.

## Phase 2 — Auth lanes (spec/22 §auth)

- WP App Password lane (cookie + Basic for REST).
- SSH-key signed-request lane (Ed25519, nonce + timestamp window per spec/22).
- Shared PHP middleware that resolves `current_user` from either lane.
- glci: `glci auth login` (App Password) and `glci auth key add` (SSH key registration).

## Phase 3 — Database layer (spec/23)

- Root SQLite schema: repos, branches, runs, sha_index, users, audit.
- Per-SHA SQLite file lifecycle: create on first push, sealed when run completes, GC policy.
- PHP repository classes (one per aggregate), prepared statements only, WAL mode.
- Migration runner with `phinx`-style versioning.

## Phase 4 — Full REST surface (spec/22, all 10 endpoints)

`POST /runs`, `GET /runs/{id}`, `POST /runs/{id}/events`, `POST /runs/{id}/finalize`, `GET /repos`, `GET /repos/{id}/shas`, `GET /shas/{sha}/diagram`, `GET /diagrams/{id}`, `GET /audit`, `POST /admin/gc`. Includes OpenAPI 3 doc generated from PHP attributes; mirrored to `glci/internal/api/openapi.yaml`.

## Phase 5 — glci feature parity (spec/28)

- Runtime detection (TS/Go/PHP/Rust/C# per spec/28 §03).
- Command surface: `init`, `run`, `submit`, `status`, `diagram`, `config` (spec/28 §04).
- CI-provider bindings: GitHub Actions, GitLab CI, generic (spec/28 §08).
- Output classification + error catalog (spec/28 §07, §09).
- Config resolution chain: flag > env > file > defaults (spec/28 §05).

## Phase 6 — Generic CLI runtime (spec/13–16, referenced by spec/28)

Pulled into `glci/internal/runtime` as a reusable Go package: parallel V→V+5 update discovery (spec/14 §24), pinned-installer self-update, `Status.ps1`/`Status.sh` JSON contract, pre/post-command hooks, JSON fallback store.

## Phase 7 — Admin UI full surface (spec/24, spec/26)

- Design system: tokens, typography, motion (spec/24 §01..§06).
- Pages: dashboard, run detail, diagram viewer (Mermaid), repo list, audit log, settings.
- spec/26 diagram parity: all 24 AC-DG diagrams render identically client-side.
- a11y: WCAG 2.2 AA, keyboard nav, screen-reader pass.

## Phase 8 — Hardening + release

- E2E: Playwright (UI ↔ plugin) + `glci` integration tests against ephemeral WP container.
- Load tests: 1000 concurrent run-events.
- Release pipeline: WP.org plugin SVN push, `glci` GoReleaser → GitHub releases + Homebrew tap + scoop bucket.
- Security: dependency scan, RLS-equivalent (capability checks) audit, SBOM.

## Backlog — Listed up front

- **P1** Walking skeleton
- **P2** Auth lanes
- **P3** Database layer
- **P4** Full REST surface
- **P5** glci feature parity
- **P6** Generic CLI runtime
- **P7** Admin UI full surface
- **P8** Hardening + release

`next` after approval = start P1. I will only do **one phase per `next`**, render a per-phase done-checklist when complete, and ask before starting the next.

## Open questions (none blocking; flag if you disagree)

1. **Plugin repo name** — proposing `git-logs` (slug for WP.org). OK?
2. **Go module path** — proposing `github.com/<your-handle>/glci`. Confirm handle.
3. **Mermaid renderer in UI** — using `mermaid` npm (client-side). spec/26 doesn't mandate server-side render. OK?
4. **WP min version** — proposing WP 6.5 + PHP 8.1. OK?
5. **glci distribution** — Homebrew + Scoop + raw binaries. Add `apt`/`yum` later? (P8 decision, not blocking.)

If any of those are wrong, tell me before P1.