# Phase 5 — Acceptance Notes

> Status: **DONE** (2026-05-11). Closes spec/28 §03 (runtime detection),
> §04 (command surface, partial — auth-bearing commands stubbed), §05
> (config resolution, minimal-TOML subset), §08 (CI provider bindings —
> GitHub Actions only per AC-28-47), and §09 (output classification, default
> patterns).

## Scope

Phase 5 lands the **client-side** halves of the v2 contract: a user can run
`glci detect`, `glci run`, `glci doctor`, and `glci config print` on any
TS/Go/PHP repo and observe deterministic output **without** the shipping
client (POST `/events`, `/finalize`) yet wired. The shipping layer is
deferred to a later phase to keep this milestone reviewable.

## Components Shipped

| File | Purpose | Spec anchor |
|------|---------|-------------|
| `glci/internal/detect/detect.go` | Lockfile-/manifest-based runtime detection (`ts`, `go`, `php`); `Result.JSON()` is byte-deterministic | §03 |
| `glci/internal/ci/ci.go`        | `HarvestEnv()` returns Provider+RepoUrl+Branch+GitSha256+PipelineName for GitHub Actions; `NormalizeRepoURL()` covers SSH→HTTPS + trailing `.git`/`/` | §08 |
| `glci/internal/config/config.go`| `Resolve(cwd, flags, getenv)` merges defaults < glci.toml (minimal subset) < env < flags; `validate()` enforces seven rules from §05 | §05 |
| `glci/internal/runner/runner.go`| `Run()` invokes (cmd, args) with `Cmd.Stderr = Cmd.Stdout` (one OS pipe — kernel FIFO ordering); CI suppression env applied (`CI=true`, `FORCE_COLOR=0`, `npm_config_progress=false`); each captured line timestamped at read time | §04 step 3 (normative) |
| `glci/internal/classify/classify.go` | Default error/warn regex set; user patterns are merged additively | §09 |
| `glci/internal/cmd/run.go`      | `Detect`, `RunCmd` (lint/build/test/run), `Doctor`, `ConfigPrint` subcommands; exit-code helper | §04 |
| `glci/internal/cmd/cmd.go`      | Dispatcher updated; `glci config print` parsed as two-token subcommand | §04 |
| `glci/main.go`                  | Bumped to `0.5.0-dev`; propagates `cmd.CodeOf(err)` so phase failures map to the §04 exit-code matrix | §04 (Exit Matrix) |

## Acceptance Checklist

- [x] `glci detect --json` against a `package.json`+`bun.lockb` repo emits
      a `Runtimes[0].Manager == "bun"` block with the bun lint/build/test
      runners from §03.
- [x] `glci detect` against an empty dir exits `2` with
      `GLCI-DETECT-NONE`.
- [x] Two JS lockfiles (`bun.lockb` + `package-lock.json`) → `glci detect`
      surfaces `GLCI-DETECT-AMBIGUOUS-LOCK`.
- [x] `ci.HarvestEnv` returns `provider="github"` only when
      `GITHUB_ACTIONS=true`; otherwise `GLCI-DETECT-NONE-CI`.
- [x] `NormalizeRepoURL("git@github.com:org/repo.git")` →
      `"https://github.com/org/repo"` (matches §22 server parser).
- [x] `config.Resolve` rejects `auth_mode=temptoken` without
      `GLCI_TEMP_TOKEN` (`GLCI-CONFIG-MISSING-TOKEN`).
- [x] `glci config print` masks `TempToken` and `Token` to `"***"`.
- [x] Runner spawns the child with **one** OS pipe shared between
      stdout+stderr (no two-pipe goroutine multiplex). Kernel FIFO
      preserves ordering per §04 step 3.
- [x] PTY allocation is forbidden (and not used) — runner relies on
      env-based TTY suppression.
- [x] `glci build ./...` compiles clean with `go 1.22+` (verified on
      `go1.25.7 linux/amd64`).

## Out of Scope (deferred)

- Shipping client (`POST /events`, `POST /finalize`, `PUT /fixed-log`,
  `POST /clear-log`, batched + streaming modes, retry/backoff). Lands in
  the next phase alongside the doctor server-reach check.
- SSH (Lane B) signing inside the shipping client. Key generation already
  ships under `glci keys generate` (Phase 2).
- `--self-test` / `--check <mode>` harness from §04 v1.2.0 (gate #40
  surface). Tracked separately under spec/28 T-38.
- Full TOML parser (arrays, nested tables, datetime). Current minimal
  parser covers the env-override path that CI actually exercises.

## Remaining Tasks (project-level)

| Phase | Title | Status |
|-------|-------|--------|
| ~~P1~~ | Walking skeleton | done |
| ~~P2~~ | Dual auth lanes | done |
| ~~P3~~ | SQLite schema + repository layer | done |
| ~~P4~~ | Public REST surface + OpenAPI | done |
| ~~P5~~ | glci command surface + runtime detection + CI bindings | **done** |
| **P6** | **Generic CLI runtime + self-update + shipping client** | **next** |
| P7 | Admin UI full surface (Dashboard, Run detail, Diagram viewer) | todo |
| P8 | E2E, load tests, security hardening, release pipeline | todo |
