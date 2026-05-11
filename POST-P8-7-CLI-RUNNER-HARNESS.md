# Post-P8 #7 — CLI/Runner Test Harness

## Why
Backlog items #4 and #5 covered pure-logic packages. This pass tackles the
remaining `internal/` packages that touch external tools (sh, ssh-keygen,
GitHub releases) but are still testable with mocked surfaces.

## Delivered (4 new packages, ~30 new tests)

| Package | File | Coverage strategy |
|---|---|---|
| `internal/runner` | `runner_test.go` | Real `sh -c` exercises pipe-merge ordering (stdout+stderr interleave), exit-code propagation, CR/LF stripping, env injection (`CI=true`, `NO_COLOR=1`), spawn failure, ctx cancellation, `stripNL` table |
| `internal/selftest` | `selftest_test.go` | All 5 modes + `ModeAll` + empty mode + unknown mode (exit 2); direct `checkPerModeFixture` exercise; exit-code contract |
| `internal/laneb` | `laneb_test.go` | `keyFingerprint` known-vector + bad-input table; `Sign` preflight (no pubkey, missing file); full ssh-keygen file-mode round-trip (skipped if `ssh-keygen` absent) — verifies PEM SSHSIG block + sha256 fingerprint |
| `internal/selfupdate` | `selfupdate_test.go` | `assetFor` (linux/windows/darwin); `verifyChecksum` match / mismatch / missing SUMS file / asset not in SUMS list (all via `httptest`); `download` body persistence + 404 error; `copyFile` round-trip |

## Verification
```
$ go test ./internal/... -coverprofile=cov.out
ok  internal/auth        0.031s
ok  internal/ci          0.013s
ok  internal/classify    0.019s
ok  internal/config      0.013s
ok  internal/detect      0.018s
ok  internal/laneb       0.013s   (NEW)
ok  internal/redact      0.015s
ok  internal/runner      5.069s   (NEW)
ok  internal/selftest    0.019s   (NEW)
ok  internal/selfupdate  0.022s   (NEW)
ok  internal/ship        0.025s
ok  internal/stream      0.322s
?   internal/cmd         [no test files]
total: 73.2% of statements (across all internal/ packages)
```
- `internal/runner` posix-shell tests skip cleanly on Windows runners.
- `internal/laneb` round-trip skips when `ssh-keygen` is absent.
- No flaky tests; all retry/sleep/clock surfaces use injected fakes.

## Still uncovered (deferred)
- `internal/cmd` — Cobra command wiring; structurally covered by `glci/scripts/e2e-smoke.sh` (Post-P8 #2 territory).
- `selfupdate.Run()` end-to-end binary swap — touches the live executable; better validated by an e2e against a staging GitHub release.
- Real GitHub API integration for `fetchLatest()` — exercised in #2 once infra exists.
