# Fixture: glci-exec-runner-crashed

**Owner:** spec/28-universal-ci-cli §97 **T-28-29** → **AC-28-29** (`GLCI-EXEC-RUNNER-CRASHED`).

Synthetic, intentionally-hostile fixture proving the §28 CLI surfaces
`GLCI-EXEC-RUNNER-CRASHED` (NOT `GLCI-EXEC-TIMEOUT`, NOT a generic non-zero exit)
when a child runner process is killed by an uncatchable signal mid-phase.

## Files

- `runner.sh` — wrapper that prints one progress line, then `kill -9 $$`
  to SIGKILL itself before completing the phase.
- `expected.json` — load-evidence contract the runner MUST meet.

## How to use

```
glci ts-test --fixture linter-scripts/fixtures/glci-exec-runner-crashed/ --json
```

Expected (per `expected.json`):
- exit code = `1`
- stderr JSON envelope `ErrorCode == "GLCI-EXEC-RUNNER-CRASHED"`
- `Signal` field present and equal to `"SIGKILL"` (or numeric `9`)
- `RequestId` field present (per AC-28-26 envelope shape)

## Failure modes this fixture detects

- Mapping SIGKILL to `GLCI-EXEC-TIMEOUT` (wrong discriminator).
- Swallowing the signal into a generic exit-1 with no `ErrorCode`.
- Omitting the `Signal` field (auditor cannot distinguish SIGKILL/SIGTERM/SIGSEGV).

DO NOT add per-fixture ignores. The corpus is hostile by design and exists
to load-prove AC-28-29 / T-28-29 end-to-end.
