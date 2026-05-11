# Post-P8 #5 — Expanded Go Test Coverage

## Delivered (4 new packages, 35 tests)

| Package | File | Coverage | Highlights |
|---|---|---|---|
| `internal/config` | `config_test.go` | high | flag>env>file precedence, scheme rejection, both auth-mode validation paths, bad template, redaction immutability, full TOML round-trip with comments |
| `internal/detect` | `detect_test.go` | high | none/ts-bun/go-only/php+phpcs/all-three, ambiguous-lockfile error, deterministic ts→go→php order, JSON marshalling |
| `internal/ci` | `ci_test.go` | high | GH Actions harvest, PR-vs-push branch (`HEAD_REF` wins), `ErrNoProvider`, all 4 RepoURL normalization shapes |
| `internal/ship` | `ship_test.go` | 75.7% | preflight no-URL/no-SHA, 200 happy path, 5xx retry-then-success, retries-exhausted, 429 rate-limit termination, 4xx surface server `ErrorCode` verbatim, 4xx fallback `HTTP-NNN`, `Reach()` headers + empty-URL error, `parseRetryAfter` (int/empty/garbage/past-date) |

## Aggregate verification
```
$ go test ./internal/... -coverprofile=cov.out
ok  internal/auth      0.012s
ok  internal/ci        0.006s     (NEW)
ok  internal/classify  0.007s
ok  internal/config    0.009s     (NEW)
ok  internal/detect    0.010s     (NEW)
ok  internal/redact    0.007s
ok  internal/ship      0.022s     (NEW)
ok  internal/stream    0.323s
total: 78.6% of statements (across the 8 covered packages)
```
No flaky tests; `ship` uses injected `Sleep`/`Now`/`Rand` to keep retry loops deterministic.

## Still uncovered (deferred)
- `internal/cmd` — CLI glue; better exercised via the e2e smoke script.
- `internal/runner` — exec-shells real binaries; needs sandbox harness or `testing.Short()` gate.
- `internal/laneb` — shells out to `ssh-keygen -Y sign`; integration test in #2.
- `internal/selfupdate` — touches GitHub releases + binary swap; integration test.
- `internal/selftest` — orchestrator; covered by e2e smoke.

These belong to backlog #2 (live integration) or a future #7 (CLI/runner harness with mocked execvp).
