# Error Catalog

**Version:** 1.2.0  
**Updated:** 2026-05-10 (Phase-5 T-38 / P19c — appended `Self-test exit codes (gate #40)` 4-row table mapping `0`→pass · `1`→violation · `2`→invocation error · `3`→fixture-rot, inheriting §27 cohort contract verbatim per Lesson #36; bound by §97 AC-28-49. Prior: Phase 153 A11g GLCI-DOCTOR-PROFILE-NOT-FOUND clarification.)

All `GLCI-*` codes the CLI itself emits. Server-originated `GL-*` codes are surfaced verbatim per [`spec/22-git-logs-v2/15-error-codes.md`](../22-git-logs-v2/15-error-codes.md). Adding a new code requires a row here.

---

## Configuration

| Code | Exit | Cause | Caller action |
|------|-----:|-------|---------------|
| GLCI-CONFIG-MISSING-FILE | 2 | `--config <path>` does not exist | Pass an existing file or run `glci config print --defaults-only > glci.toml` |
| GLCI-CONFIG-PARSE-FAILED | 2 | `glci.toml` is not valid TOML | Run `taplo lint glci.toml` |
| GLCI-CONFIG-MISSING-ENV | 2 | `${env:NAME}` referenced but env var unset | Export the env var |
| GLCI-CONFIG-MISSING-TOKEN | 2 | `auth_mode=temptoken` but no `temp_token` | Set `GLCI_TEMP_TOKEN` |
| GLCI-CONFIG-SSH-KEY-MISSING | 2 | `auth_mode=ssh` but key file unreadable | `chmod 600 <key>` and check path |
| GLCI-CONFIG-INSECURE-URL | 2 | `server.url` is `http://` without `--insecure-http` | Use HTTPS or pass `--insecure-http` |
| GLCI-CONFIG-BACKOFF-LENGTH | 2 | `len(backoff_ms) != max_retries` | Adjust array length |
| GLCI-CONFIG-BAD-TEMPLATE | 2 | `pipeline.name_template` has unknown placeholder | Use only `{runtime}` and `{phase}` |
| GLCI-CONFIG-NO-RUNTIME | 2 | All `[runtime.*].enabled=false` | Enable at least one |
| GLCI-CONFIG-BATCH-TOO-LARGE | 2 | `batch_max_bytes > 1048576` | Lower the value |

## Detection

| Code | Exit | Cause | Caller action |
|------|-----:|-------|---------------|
| GLCI-DETECT-NONE | 2 | No runtime markers found | Add `package.json`/`go.mod`/`composer.json` or pass `--cwd` |
| GLCI-DETECT-AMBIGUOUS-LOCK | 2 | Multiple TS lockfiles present | Delete all but one or pin manager in `glci.toml` |
| GLCI-DETECT-MULTIPLE-MODULES | 2 | `go.work` references modules outside `--cwd` | Pass `--cwd` to repo root |

## Doctor

| Code | Exit | Cause | Caller action |
|------|-----:|-------|---------------|
| GLCI-DOCTOR-RUNNER-MISSING | 5 | A required runner binary is not on PATH | Install the runner (e.g. `npm i -D vitest`) |
| GLCI-DOCTOR-LINTER-MISSING | 5 (warn) | `golangci-lint` absent; falling back to `go vet` | Install golangci-lint for full coverage |
| GLCI-DOCTOR-SERVER-UNREACHABLE | 5 | TCP/TLS handshake to `server.url` failed | Check network/firewall/cert |
| GLCI-DOCTOR-AUTH-INVALID | 5 | Server returned `GL-AUTH-*` on probe | Re-issue TempToken in admin UI |
| GLCI-DOCTOR-PROFILE-NOT-FOUND | 5 | Server returned `GL-VALIDATION-PROFILE-NOT-FOUND` (server resolves the runner's `RepoUrl` to a `GitProfile` row in the admin database; the CLI itself MUST NOT attempt local profile lookup — it merely surfaces the server's 404 verbatim) | Add the GitProfile in the admin UI for this `RepoUrl` |
| GLCI-DOCTOR-CLOCK-SKEW | 5 | Local clock vs server > 60s; would fail SSH `GL-SSH-TIMESTAMP-SKEW` | NTP sync the runner |

## Execution

| Code | Exit | Cause | Caller action |
|------|-----:|-------|---------------|
| GLCI-EXEC-RUNNER-FAILED | 1 | A runner exited non-zero | Read `ErrorLogs[]` in the admin UI |
| GLCI-EXEC-RUNNER-CRASHED | 1 | Runner died with signal (SIGSEGV, SIGKILL) | Inspect `ErrorLogs[]`; OOM likely |
| GLCI-EXEC-TIMEOUT | 1 | Phase exceeded `phase_timeout_secs` (default 1800) | Raise timeout or split tests |
| GLCI-EXEC-DEPS-MISSING | 1 | Per-runtime dependency directory absent before phase invocation: `node_modules/` for TypeScript (AC-28-37), `vendor/` for PHP (AC-28-39). Go is not subject to this code (modules cache lives outside the repo). The CLI MUST NOT install dependencies implicitly. | Run `<pm> install` (TS — `npm`/`pnpm`/`bun`/`yarn`) or `composer install` (PHP) before re-invoking the phase. |

## Push (transport)

| Code | Exit | Cause | Caller action |
|------|-----:|-------|---------------|
| GLCI-PUSH-NO-SHA | 2 | `GitSha256` could not be resolved | Pass `--git-sha` or run inside CI |
| GLCI-PUSH-RETRIES-EXHAUSTED | 4 | All `max_retries` POSTs failed (5xx/network) | Check server logs / network |
| GLCI-PUSH-BAD-RESPONSE | 4 | Server returned 2xx but body could not be parsed as ack envelope | Server/CLI version mismatch — check changelog |
| GLCI-PUSH-STREAM-BROKEN | 4 | Streaming connection dropped mid-flight after retry | Switch to batched mode for unstable links |
| GLCI-PUSH-PAYLOAD-TOO-LARGE | 4 | Server returned 413 | Lower `batch_max_bytes` or split phases |
| GLCI-STREAM-MALFORMED | 4 | While `--stream` is active, the server closed the chunked connection mid-frame (TCP reset, HTTP/2 GOAWAY, or NDJSON parse error reported by the server as `400 GLCI-STREAM-MALFORMED` per AC-28-26). Distinct from `GLCI-PUSH-STREAM-BROKEN`: that code indicates the underlying connection dropped after retries; this code indicates the server actively rejected the stream framing. | Re-invoke; if persistent, switch to batched mode (`shipping.mode=batched`) and capture the malformed frame for server-side debugging. |

## Auth (server-surfaced; exit 3)

These are NOT new codes — they are forwarded verbatim:

| Forwarded code | Source |
|----------------|--------|
| `GL-AUTH-TEMPTOKEN-INVALID` | §22/15 |
| `GL-AUTH-TOKEN-MISMATCH` | §22/15 |
| `GL-AUTH-PROFILE-INACTIVE` | §22/15 |
| `GL-AUTH-LANE-DISABLED` | §22/15 |
| `GL-SSH-*` (entire family) | §22/15 |
| `GL-VALIDATION-*` | §22/15 |
| `GL-APP-NOT-ACTIVE` | §22/15 |

CLI prints both: its own context line then the verbatim server envelope.

---

## Output Format

Every error printed by the CLI uses this exact shape on stderr:

```
glci: error
  Code:    GLCI-PUSH-RETRIES-EXHAUSTED
  Exit:    4
  Phase:   ts-test
  Server:  https://example.com/wp-json/git-logs/v2
  Cause:   POST /append-log failed 3 times (last: 502 Bad Gateway)
  Action:  Check server logs / network
```

In `--json` mode:

```json
{
  "Code": "GLCI-PUSH-RETRIES-EXHAUSTED",
  "Exit": 4,
  "Phase": "ts-test",
  "Server": "https://example.com/wp-json/git-logs/v2",
  "Cause": "POST /append-log failed 3 times (last: 502 Bad Gateway)",
  "Action": "Check server logs / network"
}
```

---

## Self-test exit codes (gate #40 / `--self-test`)

The `glci --self-test` harness (§04) inherits the §27 cohort
self-test exit-code contract verbatim per Lesson #36
(link-don't-restate). vacuously-passing scanner is auto-fail
per R5.

| Exit | Meaning |
|-----:|---------|
| `0` → pass | All clauses passed; ≥1 fixture exercised per `--check` mode |
| `1` → violation | One or more clauses failed; stderr lists each violation |
| `2` → invocation error | Bad CLI usage (unknown `--check` mode, missing files) |
| `3` → fixture-rot | Built-in fixture suite is broken (F-1 unique-passing fixture failed, or a failure-fixture passed). Distinguishes "self-test broken" from "implementation broken" |

