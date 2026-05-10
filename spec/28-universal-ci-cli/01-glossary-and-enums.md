# Glossary and Enums

**Version:** 1.0.0  
**Updated:** 2026-04-25

---

## Glossary

| Term | Meaning |
|------|---------|
| **Phase** | One of `lint`, `build`, `test`. The CLI runs phases sequentially (or in parallel when `--parallel`). |
| **Runtime** | A detected stack (`ts`, `go`, `php`). One repo MAY have multiple. |
| **Runner** | The native tool actually invoked for a `(Runtime, Phase)` pair (e.g. `vitest` for `(ts, test)`). |
| **Logical pipeline** | A `(Runtime, Phase)` pair as recorded in Git Logs v2 — sent as `PipelineName = "{runtime}-{phase}"`. |
| **Append batch** | One HTTP POST `/append-log` that contains all `Logs[]` and `ErrorLogs[]` produced by one phase. |
| **Stream chunk** | One body chunk in `Transfer-Encoding: chunked` — newline-delimited JSON, one log line per chunk. |
| **Doctor check** | A pre-flight assertion (binary present, server reachable, auth valid). |
| **Phase plan** | The ordered list of `(Runtime, Phase, Runner, Args)` that `glci run` will execute. Printed by `glci detect`. |
| **PipelineName** | Mirrors v2 server field; format `{runtime}-{phase}` (e.g. `ts-test`, `go-lint`). |
| **GitSha256** | Always sourced from the CI environment (`GITHUB_SHA`, `CI_COMMIT_SHA`, …); never recomputed. |

---

## Enum: `Phase`

| Value | Description |
|-------|-------------|
| `lint` | Static analysis only. Default runners: `eslint` / `golangci-lint` / `phpcs`+`phpstan`. |
| `build` | Compile / type-check. Default runners: `tsc --noEmit` (or `bun build`) / `go build ./...` / `composer dump-autoload --strict-psr`. |
| `test` | Unit + integration tests. Default runners: `vitest run` / `go test ./...` / `phpunit`. |

---

## Enum: `Runtime`

| Value | Detection marker (any one match) | Default lock-aware runner |
|-------|----------------------------------|---------------------------|
| `ts`  | `package.json` AND (`tsconfig.json` OR any `.ts` source file) | Lockfile chooses `npm` \| `pnpm` \| `bun` (see §03) |
| `go`  | `go.mod` | `go` (system Go ≥ 1.21) |
| `php` | `composer.json` | `composer`, `phpunit`, `phpcs`/`phpstan` resolved via `vendor/bin` first |

A repo MAY ship multiple runtimes (e.g. PHP plugin + TypeScript admin SPA). `glci run` then runs each runtime's full phase set; logs are tagged separately per `PipelineName`.

---

## Enum: `Severity`

Used in `--severity` filter and in `Logs[]` line classification (§09).

| Value | Meaning | Maps to `ErrorLogs[]`? |
|-------|---------|------------------------|
| `info`  | Default; informational output | No |
| `warn`  | Linter warnings, deprecations | No (counted only) |
| `error` | Compilation error, failed test, linter rule violation at `error` severity | **Yes** |
| `fatal` | Process crash, panic, OOM | **Yes** + sets `HasError=true` |

---

## Enum: `ExitCode`

| Value | Meaning |
|-------|---------|
| `0`  | All requested phases succeeded AND all log POSTs returned 2xx |
| `1`  | At least one phase reported `error` or `fatal` (logs were still shipped successfully) |
| `2`  | Configuration error (bad `glci.toml`, missing required field, contradictory flags) |
| `3`  | Auth error from Git Logs server (`GL-AUTH-*` returned by §22 server) |
| `4`  | Network/transport error after `MaxRetries` exhausted |
| `5`  | Doctor check failed (`glci doctor`) |
| `64` | Misuse of CLI (sysexits.h `EX_USAGE`) |

The exit-code table is **non-overlapping**: each numeric value MUST map to exactly one cause class. Adding a new code requires a row here.

---

## Enum: `LogShipMode`

| Value | When used | Wire format |
|-------|-----------|-------------|
| `batched`   | default | One POST `/append-log` per phase, body = full `Logs[]`+`ErrorLogs[]` |
| `streaming` | `--stream` flag OR `[push] mode = "streaming"` in `glci.toml` | `Transfer-Encoding: chunked`, NDJSON body, one chunk per log line |

Both modes target the same endpoint; the v2 server already supports streaming per `spec/22-git-logs-v2/04-rest-api-endpoints.md` AC-12.
