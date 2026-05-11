# POST-P8 #14 — Cover the `cmd` dispatcher

## Goal
Add unit coverage to the previously ungated `cmd` package — the one place where
top-level argv routing, exit-code mapping, and small helpers live.

## Files
- `glci/internal/cmd/cmd_test.go` — 7 tests:
    - `TestCodeOf` — `nil → 0`, plain error → 1, `*cmdErr` → stored code; verifies `Error()` + `Code()`.
    - `TestExitCode` — `exitCode(0)` is nil; non-zero produces `*cmdErr` with the right code.
    - `TestFilterOut` — strips all matches, leaves order, handles nil + no-match.
    - `TestContains` — hit, miss, nil-slice.
    - `TestRunHelpAndVersion` — `[]`, `help`, `--help`, `-h`, `version`, `--version`, `-v` all return nil.
    - `TestRunUnknownCommand` — unknown subcommand → error containing `"unknown command"`.
    - `TestRunConfigPrintRequiresPrintSub` — bare `config` and `config bogus` both error.
- `glci/scripts/coverage-gate.sh` — added `[cmd]=15` floor (low: most cmd funcs do real IO and aren't unit-testable in-process; this guards the dispatcher + helpers).

## Verification
- Tests are pure (no network, no fs writes) and cover the deterministic dispatcher branches in `cmd.go` plus helpers in `run.go`.
- Sandbox has no Go toolchain; CI runs `go test ./...` and the new gate enforces `cmd ≥ 15%`.

## Notes
Functions like `Detect`, `Doctor`, `RunCmd`, `ConfigPrint`, etc. are exercised end-to-end by the e2e harness (#11). Adding in-process tests for them would require dependency injection that doesn't exist today — out of scope here.
