# Output Classification

**Version:** 1.0.0  
**Updated:** 2026-04-25

The classifier turns the captured stdout+stderr stream of one runner into the three v2 payload fields: `Logs[]`, `ErrorLogs[]`, `FilePaths[]`. It is **deterministic** and **stateless across phases**.

---

## Pipeline

```
RAW LINE  →  Strip ANSI  →  Apply runner-specific patterns  →  Classify  →  Emit
                                                                 │
                                                  ┌──────────────┼──────────────┐
                                                  ▼              ▼              ▼
                                                Logs[]      ErrorLogs[]    FilePaths[]
```

Every line ends up in **exactly one** of `Logs[]` or `ErrorLogs[]`. `FilePaths[]` is a derivative — extracted from any line, regardless of bucket.

---

## Step 1 — ANSI strip

All escape sequences (`\x1b\[[0-9;]*m`, OSC sequences, BEL) are stripped before classification but re-attached to the original line in `Logs[]` only when `[push].preserve_ansi = true` (default false).

---

## Step 2 — Built-in pattern table

Tried in order; first match wins.

| Bucket | Runtime | Pattern (Go regexp) | Notes |
|--------|---------|---------------------|-------|
| ErrorLogs | any | `^panic:` | Go panic |
| ErrorLogs | any | `^Fatal error:` | PHP fatal |
| ErrorLogs | any | `^FAIL\b` | vitest/jest FAIL line |
| ErrorLogs | any | `^✗` | vitest/mocha failed assertion bullet |
| ErrorLogs | any | `^---\sFAIL:` | `go test` failure summary |
| ErrorLogs | any | `\bError:\s` | TS compile error from `tsc` |
| ErrorLogs | ts | `^\S+\(\d+,\d+\):\serror\sTS\d+:` | tsc diagnostic line (also yields `FilePaths`) |
| ErrorLogs | go | `^\S+\.go:\d+:\d+:\s` | golangci-lint diagnostic (also yields `FilePaths`) |
| ErrorLogs | php | `^\S+\.php:\d+:\s` | phpcs/phpstan diagnostic (also yields `FilePaths`) |
| Logs | any | _(fallback)_ | |

Then the **user-supplied** patterns from `[classify].error_patterns` are appended (lower priority — built-ins win on conflict).

---

## Step 3 — `FilePaths[]` extraction

For any line classified into `ErrorLogs[]`, run path-extracting regex per runtime:

| Runtime | Path regex |
|---------|------------|
| ts  | `(?P<path>[^\s:]+\.tsx?)(?:[:\(]\d+)` |
| go  | `(?P<path>[^\s:]+\.go):\d+:\d+:` |
| php | `(?P<path>[^\s:]+\.php):\d+:` |

Extracted paths are:

1. Resolved relative to `--cwd`.
2. Filtered to those that exist on disk (no synthetic test names).
3. Deduplicated, sorted lexicographically.
4. Capped at 100 entries (overflow logged as Warn but not an error).

---

## Step 4 — Determinism guarantees

- Line order in `Logs[]` and `ErrorLogs[]` MUST match capture order from the runner (PTY merge of stdout/stderr is line-buffered; CRLF normalized to LF).
- `FilePaths[]` MUST be lexicographically sorted regardless of capture order.
- For a fixed input transcript, the classifier MUST produce byte-identical output across OSes and Go versions.

---

## Step 5 — `HasError`

After classification:

```
HasError = (len(ErrorLogs) > 0) || (runner_exit_code != 0)
```

There is no third source of truth. A runner that exits 0 but printed `FAIL` lines still results in `HasError=true` (matches the v2 server's expectation that `HasError` reflects functional pass/fail, not OS-level exit).

---

## Worked Example (ts-test)

Runner output:

```
RUN  v1.0.0 /repo
✓ src/foo.spec.ts (1)
FAIL src/bar.spec.ts > sums correctly
  Error: expected 4 got 5
  ❯ src/bar.spec.ts:7:12
Test Files  1 failed | 1 passed (2)
```

After classification:

```json
{
  "Logs": [
    "RUN  v1.0.0 /repo",
    "✓ src/foo.spec.ts (1)",
    "Test Files  1 failed | 1 passed (2)"
  ],
  "ErrorLogs": [
    "FAIL src/bar.spec.ts > sums correctly",
    "  Error: expected 4 got 5",
    "  ❯ src/bar.spec.ts:7:12"
  ],
  "FilePaths": ["src/bar.spec.ts"],
  "HasError": true
}
```
