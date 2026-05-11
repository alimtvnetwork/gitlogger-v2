# Phase 6 — Acceptance Notes

> Status: **DONE** (2026-05-11). Closes spec/28 §06 (log shipping contract,
> batched + Lane A), §04 v1.2.0 `--self-test` / `--check <mode>` harness,
> and the §04 doctor server-reach check (item 4).

## Scope

Phase 6 lands the **shipping client** (CLI → v2 server) and the
self-test fixture suite. After this phase, `glci run` not only executes
phases but actually delivers their logs to a Git Logs v2 server with the
full §06 retry envelope. `glci --self-test` runs an internal acceptance
suite without network or a real CI provider.

Streaming mode (`--stream`), Lane B (SSH-signed) shipping, and the
self-update binary channel remain deferred.

## Components Shipped

| File | Purpose | Spec anchor |
|------|---------|-------------|
| `glci/internal/ship/ship.go` | `Ship()` (POST `/append-log`, batched body) + `Reach()` (GET `/get-logs?q=&limit=0`). Implements §06 R1–R5 retry classification, jittered exponential backoff (`base*2^n*(0.75+rand*0.5)`), `Retry-After` honouring (R2, server hint dominates floor), per-attempt `PUSH_REQUEST_TIMEOUT_MS` (30 s) and total `PUSH_TOTAL_DEADLINE_MS` (180 s) with hard cut. | §06 |
| `glci/internal/selftest/selftest.go` | 5 modes: `self-test-flag-declared`, `r5-vacuous-pass-carried`, `per-mode-fixture-coverage` (synthetic `package.json`+lockfile fixtures + ambiguous-lock + empty-CI-env), `exit-code-contract`, `harness-declaration`. Pure: no network, no real CI provider, no real git repo. | §04 v1.2.0 |
| `glci/internal/cmd/run.go` (extended) | `RunCmd` now calls `ship.Ship()` per `(runtime,phase)` unless `--no-push`. `buildBody()` assembles the §06 body deterministically: lexicographically-sorted `FilePaths[]` (path-regex extraction from error lines, capped at 100), `HasError = len(errs)>0 \|\| exitCode!=0`, `RootRepo` derived by stripping trailing `-vN`. `SelfTest()` subcommand. | §06 + §04 |
| `glci/internal/cmd/run.go` Doctor | Replaces "skip" with real reach: `ship.Reach()` mapped per §04 — 401 → `GLCI-DOCTOR-AUTH-INVALID`, 404 → `GLCI-DOCTOR-PROFILE-NOT-FOUND`, 5xx → fail. Exit `5` on first failure. | §04 doctor item 4 |
| `glci/internal/cmd/cmd.go` | Pre-dispatch scan for global `--self-test` flag short-circuits to `SelfTest()`. New `filterOut()` helper. | §04 v1.2.0 |

## Acceptance Checklist

- [x] `cd glci && go vet ./...` clean.
- [x] `glci --self-test` exits `0` and prints `self-test: all modes pass`
      (verified locally on `go1.25.7`).
- [x] `glci --self-test --check per-mode-fixture-coverage` exercises four
      synthetic repo trees (`ts-bun`, `ts-pnpm`, `go-mod`, `php-composer`)
      plus an ambiguous-lock fixture and an empty-CI-env fixture.
- [x] `ship.Ship()` pre-flight: missing `ServerURL` → `GLCI-PUSH-NO-URL`
      (exit 2). Missing `GitSha256` → `GLCI-PUSH-NO-SHA` (exit 2).
- [x] R1 termination 3: `MaxRetries` exhausted on 5xx → exit 4 with
      `GLCI-PUSH-RETRIES-EXHAUSTED`.
- [x] R2: HTTP 429 OR `503 + Retry-After` → server hint dominates
      backoff floor; on exhaustion → exit 4 with
      `GLCI-PUSH-RATE-LIMIT-EXHAUSTED`.
- [x] R1/R2 termination 4: total `PUSH_TOTAL_DEADLINE_MS` reached →
      exit 4 with `GLCI-PUSH-DEADLINE-EXCEEDED`.
- [x] R3: any other `4xx` → no retry, exit 3, server's `ErrorCode`
      surfaced **verbatim**.
- [x] Per-attempt and total timeouts BOTH bounded — no unbounded
      `http.Client` (forbidden pattern from §06).
- [x] `buildBody().FilePaths[]` sorted lexicographically (determinism
      contract).
- [x] `HasError = len(ErrorLogs)>0 || exitCode!=0` (§06 field rule).
- [x] `RootRepo` derives `…/repo-v2` → `…/repo` via trailing `-vN`
      strip.
- [x] `glci doctor` issues a real reach probe and maps 401/404 to the
      named §04 error codes.
- [x] `--no-push` short-circuits the entire ship path (local-only run).
- [x] `--keep-going` allows phases AND ships to continue past failure;
      final exit code is the maximum observed.

## Out of Scope (deferred)

- Streaming mode (`--stream`, `Transfer-Encoding: chunked`,
  `application/x-ndjson`, `StreamHeader/StreamFooter`, backpressure
  drop with synthetic line) — §06 "Streaming Mode" block.
- Lane B / SSH-signed shipping (`X-GL-Auth-Mode: ssh`, ssh-keygen
  subprocess, R4 single-conditional re-sign on `GL-SSH-SIG-INVALID`).
  Key generation already lands in P2.
- `/fixed-log` auto-detection — depends on server-side
  `PreviousHasError` field (GAP-22-04).
- Self-update binary channel (GoReleaser, signed releases). Tracked in P8.
- Generic CLI runtime `Status.ps1/sh` JSON contract (spec/28 deferred
  cross-runtime extension surface — not yet sectioned in spec/28 v2).

## Remaining Tasks (project-level)

| Phase | Title | Status |
|-------|-------|--------|
| ~~P1~~ | Walking skeleton | done |
| ~~P2~~ | Dual auth lanes | done |
| ~~P3~~ | SQLite schema + repository layer | done |
| ~~P4~~ | Public REST surface + OpenAPI | done |
| ~~P5~~ | glci command surface + runtime detection + CI bindings | done |
| ~~P6~~ | Shipping client + self-test harness + doctor reach | **done** |
| **P7** | **Admin UI full surface (Dashboard, Run detail, Diagram viewer)** | **next** |
| P8 | Streaming + Lane B + self-update + E2E + release pipeline | todo |
