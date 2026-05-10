# Fixture: glci-exec-timeout

**Owner:** spec/28-universal-ci-cli §97 **T-28-30** → **AC-28-30** (`GLCI-EXEC-TIMEOUT`).

Synthetic fixture proving the §28 CLI enforces the per-phase wall-clock cap
(`--phase-timeout-ms`) and surfaces `GLCI-EXEC-TIMEOUT` (NOT `GLCI-EXEC-RUNNER-CRASHED`).

## Files

- `runner.sh` — `sleep 600` runner that would never finish on its own.
- `expected.json` — load-evidence contract.

## How to use

```
glci ts-test --fixture linter-scripts/fixtures/glci-exec-timeout/ \
             --phase-timeout-ms=2000
```

Expected:
- exit code = `1`
- stderr JSON envelope `ErrorCode == "GLCI-EXEC-TIMEOUT"`
- elapsed wall-clock `< 3000 ms` (cap + grace)
- `RequestId` present (per AC-28-26)

## Failure modes detected

- Hang past 3 s (wall-clock cap not enforced).
- Maps timeout to `GLCI-EXEC-RUNNER-CRASHED` (wrong discriminator).
- Returns exit 0 because the runner was "successfully killed".
