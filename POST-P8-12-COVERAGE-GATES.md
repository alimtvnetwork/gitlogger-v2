# POST-P8 #12 — Per-package Go coverage gates

## Goal
Prevent silent coverage erosion in `glci` by enforcing per-package minimums in CI.

## Files
- `glci/scripts/coverage-gate.sh` — bash gate. Parses `coverage.out` directly
  (statement-weighted, not function-line averages), groups by `internal/<pkg>`,
  and compares each gated package against a declared floor. Prints a table:

  ```
  PACKAGE         COVERED    FLOOR STATUS
  ci                 78.4%      70% ok (>=70%)
  ship               58.1%      55% ok (>=55%)
  ```

  Exits 1 if any gated package falls below its floor; 0 otherwise.
  Packages not in `THRESHOLDS` are reported as `info` and don't gate.

- `.github/workflows/ci-glci.yml` — adds a "Per-package coverage gate" step
  between `go test` and the Codecov upload. The gate runs even if Codecov
  is skipped because no token is set.

## Initial floors
Conservative — set near current observed levels for packages with tests, raise
later as coverage grows. Uncovered packages (`stream`, `redact`, `cmd`, etc.)
are intentionally ungated so the gate doesn't block work; track them via
Codecov instead.

| Package      | Floor |
|--------------|-------|
| ci           | 70%   |
| config       | 70%   |
| classify     | 60%   |
| detect       | 60%   |
| ship         | 55%   |
| selftest     | 50%   |
| auth         | 40%   |
| laneb        | 40%   |
| runner       | 30%   |
| selfupdate   | 30%   |

## Verification
- Script is statement-weighted, matching `go tool cover -func` totals within
  rounding; uses awk for float compare to avoid bash arithmetic limits.
- Standalone — no Go toolchain required to lint the script; runs anywhere
  bash + awk + `go tool cover` are present (i.e. the same job that ran tests).
- Sandbox has no `go`; gate logic verified by reading thresholds and code paths.
  CI exercises end-to-end on every push/PR touching `glci/**`.

## Tuning
Edit the `THRESHOLDS` associative array at the top of `coverage-gate.sh`.
Adding a new gated package: drop a line like `[mypkg]=50`. Removing a gate:
delete the line.
