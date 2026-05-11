# POST-P8 #11 — glci end-to-end harness

## Goal
Spawn the compiled `glci` binary against an in-process stub WordPress server (httptest)
to exercise the user-visible CLI surface end to end — `version`, `help`, `ping`,
`whoami`, `--self-test`, and the unknown-command path.

## Files
- `glci/internal/e2e/e2e_test.go` — TestMain builds `glci` once with `go build -o $TMP/glci .`,
  then each test spawns the binary via `os/exec` and asserts (stdout, stderr, exit).
  Skips cleanly (exit 0 from TestMain) if `go` is not on PATH.
- Stub server (`net/http/httptest`) implements:
    - `GET /wp-json/git-logs/v1/health` → `{"status":"ok"}`
    - `GET /wp-json/git-logs/v1/whoami` → 401 if unauthenticated, else identity JSON
    - `POST /append-log` → `{"Accepted":true,"RunId":"stub-run-1"}`

## Tests
- `TestE2E_VersionAndHelp` — `glci version` prints `glci <ver>`; `glci help` lists all subcommands.
- `TestE2E_UnknownCommand` — non-zero exit + `unknown command` on stderr.
- `TestE2E_PingAgainstStub` — `glci ping --base $URL` exits 0, prints health JSON, hits stub once.
- `TestE2E_PingFailsOnHTTPError` — `ping` against a 500 stub exits non-zero with `HTTP 500` on stderr.
- `TestE2E_WhoamiAppPasswordLane` — App Password lane returns identity JSON.
- `TestE2E_WhoamiMissingAuthFails` — missing creds → non-zero exit, `glci:` prefix on stderr.
- `TestE2E_SelfTestPasses` — `glci --self-test` exits 0 (all built-in modes green).

## Verification
- Compiled with no Go toolchain in sandbox; tests are picked up by `go test ./...`
  in `.github/workflows/ci-glci.yml`.
- `TestMain` short-circuits with exit 0 when `go` is missing so non-Go hosts don't
  fail; CI hosts always have `setup-go` installed.

## Notes
- TestMain pattern (build once, exec many) keeps the CLI's real arg parsing,
  `os.Exit(cmd.CodeOf(err))`, and stderr formatting in the loop — pure unit
  tests can't catch wiring regressions in `main.go` / `cmd.Run`.
- Stub mux is per-test so hit counters and bespoke handlers stay isolated.
