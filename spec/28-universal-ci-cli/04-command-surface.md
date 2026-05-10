# Command Surface

**Version:** 1.2.0  
**Updated:** 2026-05-10 (Phase-5 T-38 / P19c — added `--self-test` global flag + `--check <mode>` enum (6 modes) covering the §28 built-in fixture suite; bound by §97 AC-28-49 and mechanically enforced by gate #40 `linter-scripts/check-ci-cli-self-test-harness.py`. Prior: Phase 153 A11g pipe-merge mechanism.)

Every subcommand below is normative. Adding a flag requires a row here.

---

## Global Flags (apply to every subcommand)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--cwd <dir>` | path | `$PWD` | Project root for detection + execution |
| `--config <file>` | path | `./glci.toml` | Config file path |
| `--server <url>` | url | from config | Git Logs v2 base URL (`https://example.com/wp-json/git-logs/v2`) |
| `--temp-token <s>` | string | `$GLCI_TEMP_TOKEN` | Lane B TempToken |
| `--token <s>` | string | `$GLCI_TOKEN` | Lane B Token |
| `--auth-mode <m>` | enum | `temptoken` | `temptoken` \| `ssh` (see §22 server `X-GL-Auth-Mode`) |
| `--repo-url <url>` | url | from CI env | Overrides harvested `RepoUrl` |
| `--branch <s>` | string | from CI env | Overrides harvested `Branch` |
| `--git-sha <s>` | string | from CI env | Overrides harvested `GitSha256` |
| `--no-push` | bool | false | Run phases locally, never POST |
| `--stream` | bool | false | Use streaming log shipping |
| `--keep-going` | bool | false | Run all phases even if one fails |
| `--parallel` | bool | false | Run runtimes in parallel goroutines |
| `--verbose`, `-v` | count | 0 | `-v` info, `-vv` debug, `-vvv` trace |
| `--quiet`, `-q` | bool | false | Suppress local stdout (logs still ship) |
| `--json` | bool | false | Machine-readable output on stdout |
| `--self-test` | bool | false | Run built-in fixture suite (`built-in`; `no network`; `no real CI provider`; `no real git repo`). Exits `0` pass · `1` violation · `2` invocation error · `3` fixture-rot. See §07. |
| `--check <mode>` | enum | `all` | Run a single self-test mode: `all` \| `self-test-flag-declared` \| `r5-vacuous-pass-carried` \| `per-mode-fixture-coverage` \| `exit-code-contract` \| `harness-declaration`. Used by gate #40 (Phase-5 T-38). |

---

## `glci detect`

Print phase plan + detected runtimes; do nothing else.

- Exit `0` on success (≥1 runtime).
- Exit `2` (`GLCI-DETECT-NONE`) if no runtime detected.
- Output: see §03 "Detection Output" JSON shape (when `--json`); human table otherwise.

---

## `glci lint` / `glci build` / `glci test`

Run a single phase across all detected runtimes.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--runtime <id>` | enum | _(all)_ | Restrict to one runtime (`ts` \| `go` \| `php`) |

Behavior:

1. Resolve config + harvest CI env.
2. Detect runtimes (filter by `--runtime` if set).
3. For each runtime:
   - Execute `(Phase, Runner, Args)` from §03.
   - Capture stdout + stderr **interleaved** with timestamps to preserve ordering. **Mechanism (normative):** the runner subprocess MUST be invoked with `stdout` and `stderr` merged at the OS pipe level (`exec.Cmd.Stderr = exec.Cmd.Stdout` in Go; equivalent in other runtimes), NOT via two independent pipes round-robined in user space (which loses sub-millisecond ordering). A pseudo-terminal (PTY) is **NOT required** and **SHOULD NOT** be used — runners detect TTY via `isatty(fd)` and emit ANSI escapes / progress bars / pager invocations that corrupt log parsing (`CI=true`, `FORCE_COLOR=0`, `npm_config_progress=false` per AC-28-37 already suppress most of this, but PTY allocation defeats those signals). Each captured byte is timestamped at read time with monotonic-clock millisecond resolution; ordering is preserved by the kernel pipe FIFO discipline. Forbidden: separate `Stdout` + `Stderr` pipes that the CLI multiplexes with `select` / goroutines (interleaving order is then user-space-scheduling-dependent and non-reproducible across runs).
   - Classify per §09 into `Logs[]` and `ErrorLogs[]`.
   - Ship per §06 (skip if `--no-push`).
4. Compute exit code per §01.

---

## `glci run`

The CI/CD entry point. Equivalent to `glci lint && glci build && glci test` but as one process — only one auth handshake, one detect, one config read.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--phases <list>` | csv | `lint,build,test` | Subset and order |
| `--runtime <id>` | enum | _(all)_ | Restrict to one runtime |

Behavior identical to running each phase individually with `--keep-going` unset. The first phase to fail aborts subsequent phases unless `--keep-going` is passed.

---

## `glci push-fixed`

Send `PUT /fixed-log` for the current `(RepoUrl, Branch, PipelineName)`. Used when a CI step has manually verified a previous failure is resolved (e.g. flake retry passed). Normally automatic — `glci run` calls it itself when a previously-failing pipeline now passes.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--pipeline <name>` | string | required | Logical pipeline (`ts-test`, …) |

---

## `glci clear`

Send `POST /clear-log` (single pipeline) or `POST /clear-log-all` (with `--all`).

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--pipeline <name>` | string | _(none)_ | Required unless `--all` |
| `--all` | bool | false | Clear every pipeline on `(RepoUrl, Branch)` |

Refuses to run on the `main`/`master` branch unless `--force`.

---

## `glci config print`

Print the resolved configuration as JSON, with provenance (`file` \| `env` \| `flag` \| `default`) for each field. Secrets are redacted (`"TempToken": "***"`).

---

## `glci doctor`

Pre-flight checks. Exits `5` on first failure, `0` if all pass.

Checks:

1. Detect at least one runtime.
2. Each runner binary resolvable on `$PATH` (or `vendor/bin`).
3. Server URL reachable (HTTPS handshake).
4. Auth handshake — `GET /get-logs?q=<repo>&limit=0` with current credentials. Map server response codes:
   - `200/204` → pass.
   - `401` → `GLCI-DOCTOR-AUTH-INVALID` (surface server's `ErrorCode`).
   - `404` → `GLCI-DOCTOR-PROFILE-NOT-FOUND`.
5. Clock skew ≤ 60s if `--auth-mode=ssh` (`GL-SSH-TIMESTAMP-SKEW` would fail otherwise).

---

## Exit Code Matrix per Subcommand

| Command | Possible exits |
|---------|----------------|
| `detect` | 0, 2 |
| `lint` / `build` / `test` / `run` | 0, 1, 2, 3, 4 |
| `push-fixed` / `clear` | 0, 2, 3, 4 |
| `config print` | 0, 2 |
| `doctor` | 0, 5 |
| _(any, on flag misuse)_ | 64 |
