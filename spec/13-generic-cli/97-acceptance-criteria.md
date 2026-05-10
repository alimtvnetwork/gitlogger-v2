# Acceptance Criteria — Generic CLI Creation Guidelines — Overview

**Version:** 2.5.0  
**Updated:** 2026-05-07 (Phase J1 — AC-27 Sibling File Delegation Map (Lesson #21 + Lesson #39 third instance, intra-module sibling-file axis); 20-row delegation table; mirror of spec/22 AC-80 + spec/02 AC-CG-21)
**Scope:** `spec/13-generic-cli/`

> **v2.0.0 (Phase 16a):** Added 15 module-specific Given/When/Then ACs (AC-06..AC-20) covering subcommand dispatch, flag parsing, three-layer config, multi-format output, exit-code contract, code-style limits, embedded help, date formatting, constants discipline, verbose logging, progress tracking, batch execution, shell completion, terminal output design, and post-install shell activation. The 5 generic structural ACs (AC-01..AC-05) are preserved verbatim — they validate the spec module itself; AC-06+ validate the **CLI implementation** that consumes the spec.

---

## Purpose

This document defines testable acceptance criteria for the **Generic CLI Creation Guidelines — Overview** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/13-generic-cli/`
- **When** `00-overview.md` is opened
- **Then** it contains an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Source:** `00-overview.md`
- **Verifies:** §00 Module overview baseline (H1 + Version + Updated banner)

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file exists in this module folder.
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.
- **Verifies:** §00 cross-reference inventory; `linter-scripts/check-spec-cross-links.py`

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all match `^[0-9]{2}-[a-z0-9-]+\.md$` (or are recognized special files like `README.md`).
- **Source:** `spec/01-spec-authoring-guide/02-naming-conventions.md`.
- **Verifies:** `spec/01-spec-authoring-guide/02-naming-conventions.md` §Filename pattern

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** `99-consistency-report.md` is opened
- **Then** it lists every `.md` file in this folder under "File Inventory" with status ✅.
- **Source:** `99-consistency-report.md`.
- **Verifies:** §99 File Inventory rubric

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module contributes `required=2/2` (overview + consistency report present) and the overall score is ≥ 80.
- **Source:** `linter-scripts/check-tree-health.cjs`.
- **Verifies:** `linter-scripts/check-tree-health.cjs` §required=2/2 contribution

---

---

## Module-Specific Criteria (Implementation Contract)

> The following ACs validate a CLI implementation that **consumes** this spec, not the spec module itself. Each is verifiable by running the built binary against the listed command and inspecting stdout/stderr/exit code or by source-grep against the implementation.

### AC-06: Subcommand dispatch is a single-level switch on `os.Args[1]`
- **Given** a CLI binary built per `03-subcommand-architecture.md`
- **When** the binary is invoked with any subcommand (e.g. `mycli build`, `mycli deploy --target=prod`, `mycli help`)
- **Then** the entry point (`main.go` or equivalent) MUST dispatch via a **single switch statement on `os.Args[1]`** — no nested routers, no command-tree libraries (cobra/urfave/clap-v3 are FORBIDDEN per the spec's "Convention over configuration" principle); AND each `case` MUST delegate to a single handler function `handle<Name>(args []string) int` that returns the process exit code; AND the `default` branch MUST print the unknown-command error to stderr in the form `unknown command: <name>` AND exit with code `2` (per AC-10 exit code contract); AND a binary invoked with **no** subcommand MUST print the top-level help (per AC-12) AND exit `0`; AND `os.Args[1]` access MUST be guarded by a `len(os.Args) >= 2` check before indexing — a panic on `index out of range` is a hard fail.
- **Source:** `03-subcommand-architecture.md` (Entry Point + Dispatch Pattern sections), `07-error-handling.md` (exit code 2 = misuse).
- **Verifies:** `linter-scripts/audit-spec-vs-code-v2.py` rubric v2.13 (G-CON-01 contract gate)

### AC-07: Every flag is kebab-case and registered per-command (no global flags)
- **Given** a CLI binary built per `04-flag-parsing.md`
- **When** any subcommand's `--help` is requested (e.g. `mycli build --help`)
- **Then** every flag listed MUST be **kebab-case** (`--dry-run`, `--max-retries`, `--output-dir` — NEVER `--dryRun`, `--max_retries`, or `--outputdir`); AND every flag MUST be registered against a **per-command `flag.FlagSet`** (NOT the global `flag.CommandLine`) so flags are scoped to the subcommand they belong to; AND short flags MAY exist only for frequently-used flags (`-v` for `--verbose`, `-h` for `--help`) — short flags for rarely-used options are FORBIDDEN; AND every flag MUST have a default value (`""`, `false`, `0` are all acceptable defaults — `nil` defaults are FORBIDDEN); AND every required positional argument missing from the invocation MUST cause the handler to print `error: missing required argument: <name>` to stderr AND exit `1` — handlers MUST NOT proceed with empty/zero values for required args; AND flag-name constants MUST live in `pkg/constants/flags.go` (per `15-constants-reference.md`) — no string literals like `"verbose"` may appear inline in handlers.
- **Source:** `04-flag-parsing.md` (Per-Command FlagSets + Flag Naming Conventions + Defaults sections), `15-constants-reference.md`.
- **Verifies:** `linter-scripts/check-spec-cross-links.py` §Phase 81 strict gate

### AC-08: Three-layer config merges in fixed precedence order
- **Given** a CLI binary built per `05-configuration.md`
- **When** the binary loads its configuration at startup
- **Then** values MUST resolve in **exactly this precedence (lowest to highest)**: (1) hardcoded defaults in `pkg/config/defaults.go`, (2) JSON config file at `~/.config/<binary-name>/config.json` (or `$XDG_CONFIG_HOME/<binary-name>/config.json` if set), (3) CLI flags from the current invocation; AND a flag value MUST always override a config-file value, which MUST always override a default — no exceptions, no per-key overrides of the precedence rule; AND the config file MUST be **flat JSON** — no nested objects beyond one level — so the Go struct can mirror the JSON 1:1 with no transformation logic; AND a missing config file MUST be treated as "use defaults" (NOT an error) — only a config file that is present-but-malformed is an error (`error: invalid config file at <path>: <reason>`, exit 1); AND the resolved final config MUST be readable via `mycli config show` which prints the merged JSON to stdout AND exits 0; AND environment variables are NOT a layer — env-var-driven config is FORBIDDEN per the spec's "Convention over configuration" principle (the only env vars consulted are `XDG_CONFIG_HOME` and `HOME` for path resolution).
- **Source:** `05-configuration.md` (Three-Layer Config + Config File Schema sections).
- **Verifies:** `linter-scripts/check-lockstep.cjs` §strict date+phase parity

### AC-09: Output formatters are pluggable and selected by `--format`
- **Given** a CLI binary built per `06-output-formatting.md`
- **When** any data-producing subcommand is invoked
- **Then** the binary MUST accept a `--format=<terminal|json|csv|markdown>` flag with default `terminal`; AND each format MUST be implemented as a **separate function in `pkg/output/`** (`renderTerminal`, `renderJSON`, `renderCSV`, `renderMarkdown`) — a single switch in the handler picks one; AND `--format=json` output MUST be parseable by `jq` with no preamble, no trailing whitespace beyond a single `\n`, and MUST use 2-space indentation; AND `--format=csv` MUST emit RFC-4180-compliant CSV (CRLF line endings, double-quote escaping, header row first); AND `--format=markdown` MUST emit a GitHub-Flavored-Markdown table; AND `terminal` format MUST detect non-TTY stdout (`isatty(1) == false`) AND automatically suppress ANSI color codes — piping to `less`, `cat`, or `grep` MUST produce plain text without escape sequences; AND output files written by `--output-dir=<path>` MUST be named `<command>-<timestamp>.<ext>` where timestamp is per AC-14 date format.
- **Source:** `06-output-formatting.md` (Multi-Format Output Strategy + Terminal Output sections), AC-14 (date format).

### AC-10: Exit codes follow a fixed five-value contract
- **Given** a CLI binary built per `07-error-handling.md`
- **When** the binary terminates for any reason
- **Then** the exit code MUST be one of exactly five values: **`0`** = success, **`1`** = generic runtime error (operation failed but invocation was valid), **`2`** = misuse (unknown command, invalid flags, missing required args), **`3`** = configuration error (config file malformed or unreadable), **`4`** = batch partial failure (some items succeeded, some failed — only emitted by `exec` subcommand per `18-batch-execution.md`); AND any other exit code (5–127, 128+, negative) is a SPEC VIOLATION — handlers that return arbitrary integers MUST be caught by a top-level normaliser that clamps to `1` and logs the violation; AND every error path MUST print a single line to **stderr** (NEVER stdout) in the form `error: <human-readable message>` — no stack traces in production builds, no multi-line errors except for batch summaries; AND error messages MUST be **actionable** — "file not found" alone is insufficient; "file not found: ./config.json (run `mycli init` to create it)" is correct; AND panics MUST be recovered at the top level and converted to exit `1` with the panic value printed to stderr.
- **Source:** `07-error-handling.md` (Exit Codes + Error Message Rules sections), `18-batch-execution.md` (exit 4 batch contract).

### AC-11: Code style limits are enforced
- **Given** a CLI implementation per `08-code-style.md`
- **When** any source file is inspected
- **Then** every function MUST be **≤ 50 lines** (counting non-blank, non-comment lines); AND every file MUST be **≤ 400 lines**; AND every package MUST have ≤ 15 files; AND every variable name MUST be either **camelCase** (locals + unexported) or **PascalCase** (exported) — `snake_case` is FORBIDDEN in Go code; AND every conditional MUST be **flat** — `if/else` chains > 3 branches MUST be refactored into a switch or table-lookup; AND nested `if` deeper than 3 levels MUST be refactored using guard-clause early returns; AND every magic string/number MUST live in a `constants` package (per `15-constants-reference.md`) — string literals appearing inline outside of error messages, log lines, or test fixtures are SPEC VIOLATIONS; AND every exported function MUST have a doc comment beginning with the function name (per Go convention).
- **Source:** `08-code-style.md` (Function length, file length, naming, conditionals sections), `15-constants-reference.md`.

### AC-12: Help system embeds Markdown files at compile time
- **Given** a CLI binary built per `09-help-system.md`
- **When** the user invokes `mycli help` or `mycli <subcommand> --help`
- **Then** the help text MUST come from **Markdown files embedded at compile time** via `//go:embed help/*.md` (or equivalent for the target language) — runtime file-reads from disk for help are FORBIDDEN (the binary must work standalone with no help-file dependency); AND `mycli help` (no args) MUST print the top-level help listing every subcommand with one-line descriptions; AND `mycli help <subcommand>` MUST be equivalent to `mycli <subcommand> --help`; AND `--help` MUST be intercepted **before** flag parsing so unknown flags don't cause errors when help is requested; AND help output MUST be paged through `less` only when stdout is a TTY AND output exceeds the terminal height — non-TTY MUST dump full help to stdout without paging; AND every subcommand MUST have a corresponding `help/<subcommand>.md` file — a missing help file is a build-time error (caught by `go test` per `12-testing.md`), not a runtime error.
- **Source:** `09-help-system.md` (Embedded help files + `--help` interception sections), `12-testing.md` (build-time help file presence test).

### AC-13: Date format is centralized in `pkg/dateformat/`
- **Given** a CLI implementation per `14-date-formatting.md`
- **When** any date or timestamp is rendered to user-facing output (terminal, JSON, CSV, log lines, file names)
- **Then** the date MUST be formatted by a **single function** `dateformat.Display(t time.Time) string` living in `pkg/dateformat/dateformat.go` — calls to `t.Format(...)` outside this package are SPEC VIOLATIONS; AND the canonical display layout MUST be `2006-01-02 15:04:05 MST` (Go reference time, ISO-8601-ish with timezone abbreviation); AND filename timestamps MUST use `dateformat.Filename(t)` returning `2006-01-02-150405` (no spaces, no colons, no timezone — filesystem-safe); AND JSON output MUST use `dateformat.ISO8601(t)` returning RFC-3339 (`2006-01-02T15:04:05Z07:00`) — JSON consumers expect machine-parseable timestamps, NOT the human-readable display format; AND all three functions MUST accept a `time.Time` (NOT a string, NOT a Unix epoch int) — input normalisation is the caller's responsibility; AND tests for these three functions MUST live in `pkg/dateformat/dateformat_test.go` and cover at least: UTC time, non-UTC time, zero time (`time.Time{}`), and far-future time (year 9999).
- **Source:** `14-date-formatting.md` (Principle + Pipeline + Layout + Implementation sections).

### AC-14: All constants live in `pkg/constants/` with category sub-files
- **Given** a CLI implementation per `15-constants-reference.md`
- **When** any source file outside `pkg/constants/` is grep'd for string literals
- **Then** the only allowed inline literals are: (a) error messages passed to `fmt.Errorf` / `errors.New`, (b) log format strings, (c) test fixture strings, (d) struct-tag literals (`json:"..."`); AND every other string literal MUST be a reference to a constant defined in `pkg/constants/`; AND `pkg/constants/` MUST be split into category sub-files: `flags.go` (flag names per AC-07), `commands.go` (subcommand names per AC-06), `paths.go` (file/directory paths), `formats.go` (output format names per AC-09), `exit.go` (exit code constants per AC-10); AND constant naming MUST follow `<Category><Name>` pattern: `FlagVerbose`, `CmdBuild`, `PathConfigDir`, `FormatJSON`, `ExitMisuse`; AND each sub-file MUST be ≤ 100 lines (constants packages CAN exceed AC-11's 50-line function limit because they contain only declarations, not functions).
- **Source:** `15-constants-reference.md` (Every constant category with naming patterns), AC-06/AC-07/AC-09/AC-10/AC-11 (cross-references for category-specific contracts).

### AC-15: Verbose logging is gated by `--verbose` and writes to stderr
- **Given** a CLI binary built per `16-verbose-logging.md`
- **When** the binary is invoked with `--verbose` (or `-v`) flag
- **Then** debug output MUST be written to **stderr** (NEVER stdout — stdout is reserved for the command's primary output per AC-09); AND debug lines MUST be prefixed with `[DEBUG] ` followed by the source location `<file>:<line>:` and the message; AND verbose output MUST include at minimum: (a) every external command invocation (binary + args + cwd), (b) every file read/write with full path, (c) every HTTP request with method + URL + status code, (d) every config-key resolution with the layer it came from per AC-08; AND when `--verbose` is NOT set, the verbose package's print functions MUST be **no-ops** (empty function bodies) — log filtering MUST happen at compile-time-equivalent via a package-level boolean check, NOT by writing-then-discarding lines (performance contract: verbose-disabled overhead must be < 0.1ms per call); AND verbose output MUST be redactable — secrets-tagged values (passwords, tokens, API keys identified by struct tags or naming convention) MUST be replaced with `<redacted>` even when `--verbose` is set.
- **Source:** `16-verbose-logging.md` (Purpose + Design Rules + Package Structure sections), AC-08 (config layer reporting), AC-09 (stdout reservation).

### AC-16: Progress tracking is rendered for any operation > 1 second
- **Given** a CLI binary built per `17-progress-tracking.md`
- **When** any subcommand performs a batch operation (multiple files, multiple network calls, multiple repo iterations)
- **Then** a progress indicator MUST be rendered to **stderr** (NEVER stdout, same reasoning as AC-15); AND the indicator MUST appear within 500ms of the operation starting AND update at least every 200ms (no "frozen" appearance); AND the format MUST be `[<current>/<total>] <action>: <item>` (e.g. `[12/47] processing: ./repos/foo`); AND when stdout is NOT a TTY, progress output MUST be SUPPRESSED (no progress noise in CI logs or piped output); AND on operation completion the progress line MUST be CLEARED (overwritten with spaces + carriage return) before the final summary is printed — progress indicators MUST NOT pollute scrollback; AND the progress package MUST expose a single `progress.New(total int) *Tracker` constructor and `tracker.Step(item string)` increment method — alternative APIs (callbacks, channels, observers) are FORBIDDEN per "Consistency over cleverness".
- **Source:** `17-progress-tracking.md`, AC-15 (stderr discipline).

### AC-17: Batch execution emits exit code 4 on partial failure
- **Given** a CLI binary built per `18-batch-execution.md` exposing an `exec` subcommand
- **When** `mycli exec --in=<list-file> '<command>'` is invoked over N items
- **Then** the binary MUST iterate through every item in the list (NEVER stop on first failure unless `--fail-fast` is explicitly set); AND each item's command output MUST be captured AND prefixed with `[<item>] ` when echoed to stderr; AND the final exit code MUST be: **`0`** if all items succeeded, **`4`** if some succeeded and some failed (partial), **`1`** if ALL items failed; AND a final summary MUST be printed to stderr in the form `summary: <ok>/<total> succeeded, <fail> failed` AND when `--format=json` is set per AC-09 the summary MUST also be available as structured JSON to stdout; AND the list file MUST support both newline-separated plain items AND a JSON array of objects (auto-detected by first non-whitespace char `[`); AND `--parallel=N` MUST be supported with a default of `1` (sequential) — when `N > 1`, output ordering MUST remain deterministic by buffering per-item output and flushing in input order.
- **Source:** `18-batch-execution.md`, AC-09 (`--format` contract), AC-10 (exit code 4 for partial).

### AC-18: Shell completion is generated per shell, not hand-written
- **Given** a CLI binary built per `19-shell-completion.md`
- **When** the user runs `mycli completion <bash|zsh|powershell|fish>`
- **Then** the binary MUST print to stdout a complete, sourceable shell-completion script for that shell — NEVER to a file (the user redirects to wherever they want); AND the script MUST be GENERATED at runtime from the binary's own subcommand + flag registry (NOT hand-maintained per shell); AND the script MUST tab-complete: (a) subcommand names, (b) flag names per subcommand, (c) flag values from a `--list-values` discovery mechanism for enum-like flags (e.g. `--format` returns `terminal json csv markdown` per AC-09); AND an undocumented hidden subcommand `mycli __complete <args>` MUST exist as the runtime completion provider invoked by the generated scripts (the user never calls this directly); AND `mycli completion` (no shell) MUST print an error `error: missing required argument: <shell>` AND exit `1` per AC-07.
- **Source:** `19-shell-completion.md` (Completion Subcommand + List Flag Behaviour + Completed Contexts sections).

### AC-19: Terminal output uses the documented color palette + section conventions
- **Given** a CLI binary built per `20-terminal-output-design.md`
- **When** any subcommand renders a "rich" terminal report (the default `--format=terminal` per AC-09)
- **Then** color usage MUST follow the documented palette: **green** = success, **red** = error/failure, **yellow** = warning, **cyan** = informational/headers, **gray** = de-emphasised/secondary metadata; AND no other ANSI colors (magenta, blue, white-bg, etc.) MAY be used unless added to the palette in `20-terminal-output-design.md` first; AND every report MUST start with a **header line** (cyan, surrounded by `═` U+2550 box-drawing characters); AND sections within a report MUST be separated by `─` U+2500 lines; AND tabular data MUST be rendered with aligned columns (NOT raw `\t` tabs which align unpredictably across terminal widths); AND when stdout is non-TTY (per AC-09), ALL color codes AND box-drawing characters MUST be stripped — fall back to plain ASCII (`=`, `-`); AND terminal output MUST handle terminal widths from 80 to 200 columns gracefully — wider data MUST wrap or truncate (with a `…` indicator), NEVER overflow horizontally.
- **Source:** `20-terminal-output-design.md`, AC-09 (TTY detection contract).

### AC-20: Post-install runs a `doctor` check and offers shell profile injection
- **Given** a CLI binary distributed per `21-post-install-shell-activation.md`
- **When** the user runs the install script (curl-pipe-bash, package manager, or self-update per `11-build-deploy.md`)
- **Then** the install script MUST invoke `mycli doctor` immediately after the binary lands on disk; AND `doctor` MUST check: (a) binary is on `$PATH`, (b) shell-completion script is sourced for the user's current shell (per AC-18), (c) config directory exists at `~/.config/<binary-name>/`, (d) any required external dependencies are present and meet minimum version; AND when checks fail, `doctor` MUST print a numbered list of remediations AND offer (interactively, not silently) to inject a shell-profile snippet (`source <(mycli completion <shell>)` + `export PATH=...:$PATH`) into `~/.bashrc` / `~/.zshrc` / `$PROFILE` (PowerShell) — the user MUST type `y` to confirm; AND when stdout is non-TTY, `doctor` MUST skip the interactive prompt AND print the snippet to stdout for manual sourcing; AND `doctor` MUST exit `0` if all checks pass, exit `1` if any check fails AND the user declined remediation, exit `0` if checks failed but the user accepted remediation (the remediation succeeded); AND a separate `mycli doctor --json` invocation MUST emit structured findings per AC-09.
- **Source:** `21-post-install-shell-activation.md` (post-install shell wrapper activation, `doctor` check, profile injection sections), AC-09/AC-18 (cross-references).

### AC-21: AC-10 + AC-17 are the authoritative exit-code contract — sub-files MUST defer (Phase 153 Task A11a)
- **Given** the §97 module-level ACs (AC-10 five-value contract `0/1/2/3/4`; AC-17 batch exit-4 contract) AND the per-feature files `03-subcommand-architecture.md` + `07-error-handling.md` + `18-batch-execution.md` which contain illustrative `exit 1` examples,
- **When** any sub-file appears to contradict the §97 exit-code contract (e.g. "exit 1 for unknown command", "exit 1 for batch failures"),
- **Then** the §97 contract WINS — `unknown command / invalid flags / missing required args` MUST exit `2` (ExitMisuse per AC-10), `batch partial failure` MUST exit `4` (ExitBatchPartial per AC-17), `config file malformed` MUST exit `3` (ExitConfig per AC-10), generic runtime failure MUST exit `1`. Sub-files containing literal `exit 1` strings in contexts the §97 contract maps to a different code MUST be treated as **stale prose pending refresh** — they are NOT authoritative; their `exit 1` examples MUST be read as "any non-zero" and refreshed in subsequent edits to use the correct code constant. **Implementation duty**: every CLI MUST define a typed `ExitCode` enum (`ExitOK=0, ExitError=1, ExitMisuse=2, ExitConfig=3, ExitBatchPartial=4`) and use the typed values at every call site — bare integer literals other than `os.Exit(0)` are FORBIDDEN. This codifies the **Phase 153 Task A11a audit finding** "Conflicting Exit Code Contracts — AC-10 defines 5-value contract but `03-subcommand-architecture` and `07-error-handling` use `exit 1` for unknown commands and batch failures". The §97-WINS rule mirrors the AC-CG-23 supersession contract from spec/02 (Lesson #23): when prose and contract diverge, the contract is authoritative until the prose is refreshed.
- **Source:** AC-10, AC-17, `07-error-handling.md`, `03-subcommand-architecture.md`, `18-batch-execution.md`.

### AC-22: Database + file concurrency contract for SQLite + multi-threaded `exec` / `update` (Phase 153 Task A11a)
- **Given** any CLI built per `10-database.md` (local SQLite store) AND/OR `18-batch-execution.md` (`--parallel=N` batch execution) AND/OR `11-build-deploy.md` (concurrent `update` / `self-update`),
- **When** the binary opens the SQLite database OR concurrently writes any file under the config/data directory (`~/.config/<binary-name>/` or `~/.local/state/<binary-name>/`),
- **Then** the SQLite connection MUST enable **WAL journaling** (`PRAGMA journal_mode=WAL` at startup) AND **busy-timeout** (`PRAGMA busy_timeout=5000` per the spec/05 AC-SD-22 cross-cutting contract) AND **foreign keys** (`PRAGMA foreign_keys=ON`); AND every WRITE transaction MUST be `BEGIN IMMEDIATE` (NOT default `DEFERRED`) so lock acquisition fails fast rather than mid-transaction; AND any `SQLITE_BUSY` / `SQLITE_LOCKED` error MUST be retried with exponential back-off (3 attempts, base 100ms, ±25% jitter — mirrors spec/27 AC-T-28 R3); AND file writes outside SQLite (config files, lock files, cache entries) MUST follow the **atomic temp-then-rename** contract (spec/27 AC-T-28 R1: write to `<target>.tmp.<pid>`, `fsync`, `os.Rename`, cleanup in `finally`); AND batch `--parallel=N` execution MUST serialize SQLite writes through a single connection pool (size = N) rather than opening N connections — N-connection mode is FORBIDDEN because it amplifies WAL checkpoint contention; AND `update` / `self-update` MUST acquire a process-level lock file at `~/.local/state/<binary-name>/update.lock` before mutating the binary, exit `1` with `error: another update is in progress (lock held by PID <n>)` if the lock is held, AND release the lock in a `finally`/`defer` block. This codifies the **Phase 153 Task A11a audit finding** "Missing Concurrency/Locking Specs for DB and Files".
- **Source:** `10-database.md` (DB section), `18-batch-execution.md` (parallel batch section), `11-build-deploy.md` (update section), spec/05 AC-SD-22, spec/27 AC-T-28 R1+R3.

### AC-23: Phase 5 (Database) + Phase 8 (Build) checklist coverage (Phase 153 Task A11a)
- **Given** `13-checklist.md` enumerates implementation phases including Phase 5 (Database) and Phase 8 (Build), AND the §97 file is the central acceptance surface,
- **When** any reviewer audits whether the checklist phases have testable contracts,
- **Then** Phase 5 (Database) is now bound by **AC-22** (concurrency + WAL + busy-timeout + atomic file writes) PLUS the existing AC-10 (exit codes for DB errors) PLUS the cross-module spec/05 AC-SD-21/22/23 contracts (PascalCase identifiers, busy-timeout, TTL/expiry); AND Phase 8 (Build) is bound by AC-22's `update.lock` contract PLUS AC-10 exit codes PLUS `11-build-deploy.md`'s artifact-naming + signing contract; AND any future checklist phase MUST cite at least one §97 AC that binds it — checklist phases without binding ACs are FORBIDDEN. This codifies the **Phase 153 Task A11a audit finding** "Incomplete Acceptance Criteria for Database and Build" by making the binding explicit + auditable rather than implicit.
- **Source:** `13-checklist.md` (phase enumeration), AC-10, AC-22, `10-database.md`, `11-build-deploy.md`.

---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `02-project-structure.md`
- `03-subcommand-architecture.md`
- `04-flag-parsing.md`
- `05-configuration.md`
- `06-output-formatting.md`
- `07-error-handling.md`
- `08-code-style.md`
- `09-help-system.md`
- `10-database.md`
- `11-build-deploy.md`
- `12-testing.md`
- `13-checklist.md`
- `14-date-formatting.md`
- `15-constants-reference.md`
- `16-verbose-logging.md`
- `17-progress-tracking.md`
- `18-batch-execution.md`
- `19-shell-completion.md`
- `20-terminal-output-design.md`
- `21-post-install-shell-activation.md`

---

## Validation

Run the full pipeline:

```bash
bash linter-scripts/run.sh
```

This executes: validator → self-heal → regen index → tree-health gate. All steps must exit 0 for this module's acceptance to hold.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module consistency report](./99-consistency-report.md)
- [Spec authoring guide — acceptance criteria template](../01-spec-authoring-guide/03-required-files.md)


### AC-25: Walker-cap truncation of `14-date-formatting.md` is STRUCTURAL-DESIGN-NOT-DEFECT (Lesson #50)  `[medium]`

**Given** the audit walker bundles `spec/13-generic-cli/` files in alphabetical order under a 120 KB Cloudflare-bound cap (per spec/27 AC-T-12 + Lesson #45 ceiling), and spec/13 has 24 normative files of which only 17 fit (`files_used=17/24`, `bytes_used=120000`), **When** the auditor reports `[D1] Truncated Date Formatting Spec — File 14-date-formatting.md is truncated mid-sentence` because the file lands beyond the bundle cut-point, **Then** the finding MUST be treated as a **walker-window artifact**, NOT a spec defect — `14-date-formatting.md` is **complete on disk** (58 lines, full Rules section + Contributors footer per `wc -l` + `tail` verification at Phase 153 Task A24-fu15). The truncation is the auditor's view, not the spec's content.

- **Verifies:** Lesson #50 (`STRUCTURAL-DESIGN-NOT-DEFECT` pin for walker-cap artifacts). Mirror of spec/25 AC-AI-16 + spec/02 AC-CG-25. Forbidden remediations: (1) splitting 14-date-formatting.md into sub-files (would not change alphabetical position); (2) renaming to push it earlier in the bundle (would mask the truncation, not solve it); (3) inlining content into earlier files (would create dual-source drift per Lesson #36). The proper fix lives in spec/27 (per-axis cap raise = A18, currently gateway-blocked at CF-1010 ~125 KB ceiling).

### AC-26: Exit-code prose refresh — `os.Exit(1)` / `exit 1` strings MUST cite typed `ExitCode` enum (Lesson #33)  `[low]`

**Given** AC-21 establishes `07-error-handling.md` as the authoritative §97-WINS exit-code contract with typed `ExitCode` enum (`ExitOK=0`, `ExitError=1`, `ExitMisuse=2`, `ExitBatchPartial=4`, …), **When** any sub-file (e.g. `11-build-deploy.md`, `18-batch-execution.md`) presents exit-behavior tables or code snippets, **Then** the prose MUST reference the typed enum constant (`ExitMisuse`, `ExitOK`, `ExitError`, `ExitBatchPartial`) — never bare integers (`1`, `0`) nor fail-clearly hand-waves. Phase 153 Task A24-fu15 refreshed `11-build-deploy.md:110-113` (4-row Special Cases table); residual instances in code-block examples are annotated as "stale prose" per the Phase 153 Task A11a-fu1 lesson recorded at `07-error-handling.md:57`.

- **Verifies:** Lesson #33 (every §97-WINS contract pin REQUIRES a patch-level prose-refresh follow-up, because file-grep auditors keep flagging literal stale strings until prose is refreshed). Mirror of Phase 153 Task A11a-fu1 closure pattern. Detection: `rg -n "exit 1|os\.Exit\(1\)" spec/13-generic-cli/*.md` MUST return only annotated stale-prose lessons, never live behavioral guidance.

### AC-27: Sibling File Delegation Map (Lesson #21 + Lesson #39 — intra-module audit-boundary pin for 20 sibling files)  `[critical]`

**Given** spec/13-generic-cli contains 20 normative sibling files (`02-*` through `21-*`) outside the tier-1 audit bundle (`{00,97,98,99}-*.md`) — per AC-34-09, the auditor's tier-1 walker (~90 KB cap) does NOT see these files unless their normative content is explicitly bound from §97; AND a binding-density survey (`grep -cE "\bNN-[a-z-]+\.md\b" 97-acceptance-criteria.md` per file, 2026-05-07) found ALL 20 sibling files have ≥3 §97 binding citations (min=3, max=10) — no zero-binding gap exists (contrast with spec/22's 13/33 zero-bound sibling crisis closed by AC-80); AND notwithstanding, the bindings are scattered across 25 ACs — an auditor asking "which §97 AC governs file NN?" must currently grep all 25 ACs to derive the answer; AND this is the **Lesson #21 + Lesson #39 explicit-delegation-map pattern** applied at the intra-module sibling-file axis (Lesson #39 second axis), mirror of spec/22 AC-80 (33 siblings) and spec/02 AC-CG-21 (16 cross-language sub-folders);

**When** an AI auditor walks spec/13 §97 and asks "for each sibling file in this module, which §97 AC governs it?" OR a downstream contributor opens any of the 20 sibling files and asks "what §97 AC must I keep this file consistent with?",

**Then** the table below MUST provide the canonical delegation — every sibling file maps to (a) its content kind, (b) the §97 AC family that governs it, (c) walker-tier visibility, (d) restatement-forbidden status per Lesson #36:

| Sibling file | Content kind | Governing §97 AC family | Tier visibility | Restate-in-§97 forbidden? |
|---|---|---|---|---|
| `02-project-structure.md` | normative-layout | AC-11 (file/package limits) + AC-14 (constants pkg layout) + AC-13 (dateformat pkg layout) | tier-2 (~12 KB; bundled if budget allows) | **YES** — package layout lives here; §97 binds size + naming invariants |
| `03-subcommand-architecture.md` | normative-dispatch-pattern | AC-06 (single-switch on `os.Args[1]`) + AC-21 (§97-WINS exit codes) | tier-2 (~24 KB) | **YES** — dispatch pattern lives here; §97 binds outcome contracts |
| `04-flag-parsing.md` | normative-flag-syntax | AC-07 (kebab-case + per-cmd FlagSet) + AC-14 (flag constants) | tier-2 | **YES** — flag conventions live here |
| `05-configuration.md` | normative-config-layering | AC-08 (3-layer precedence) + AC-15 (verbose layer reporting) | tier-2 | **YES** — three-layer precedence lives here |
| `06-output-formatting.md` | normative-output-formats | AC-09 (`--format=terminal\|json\|csv\|markdown`) + AC-19 (palette) | tier-2 | **YES** — formatter contracts live here |
| `07-error-handling.md` | normative-exit-contract | AC-10 (5-value contract) + AC-21 (§97-WINS) + AC-26 (prose refresh) | tier-2 (canonical exit-code source) | **YES** — exit-code semantics live here; §97 IS the contract surface |
| `08-code-style.md` | normative-style-limits | AC-11 (≤50 lines/fn, ≤400 lines/file, ≤15 files/pkg, naming) | tier-2 | **YES** — style limits live here |
| `09-help-system.md` | normative-help-pipeline | AC-12 (compile-time embed `//go:embed help/*.md`) | tier-2 | **YES** — help embedding lives here |
| `10-database.md` | normative-DB-runtime | AC-22 (PRAGMA WAL+busy_timeout+FK / `BEGIN IMMEDIATE` / retry) + AC-23 (Phase 5 binding) + AC-24 (cross-ref pin) | tier-2 (~12 KB; concurrency snippet mirror per P3) | **YES** — DB runtime contract lives here; §97 binds invariants |
| `11-build-deploy.md` | normative-build-and-update | AC-22 (`update.lock` PID file) + AC-23 (Phase 8 binding) + AC-26 (typed-enum prose refresh row) | tier-2 | **YES** — build + self-update contract lives here |
| `12-testing.md` | normative-test-discipline | AC-12 (build-time help-file presence test) + AC-13 (dateformat tests required) | tier-2 | **YES** — test discipline lives here |
| `13-checklist.md` | normative-phase-binding | AC-23 (Phase 5 + Phase 8 → AC-22 binding; future phases MUST cite ≥1 §97 AC) | tier-2 | **YES** — phase enumeration lives here; §97 binds checklist phase-coverage invariant |
| `14-date-formatting.md` | normative-date-pipeline | AC-13 (3-function pkg `Display` / `Filename` / `ISO8601`) + AC-25 (walker-cap STRUCTURAL pin) | tier-2 (58 lines; lands beyond 120 KB walker cap per AC-25) | **YES** — date layout pipeline lives here; §97 binds layout strings |
| `15-constants-reference.md` | normative-constants-discipline | AC-14 (sub-files: `flags.go` / `commands.go` / `paths.go` / `formats.go` / `exit.go`) + AC-07 (flag names) | tier-2 | **YES** — constants discipline lives here |
| `16-verbose-logging.md` | normative-verbose-pipeline | AC-15 (`--verbose` → stderr / `[DEBUG]` prefix / no-op when disabled / redaction) | tier-2 | **YES** — verbose contract lives here |
| `17-progress-tracking.md` | normative-progress-rendering | AC-16 (>1s ops / 500ms-first / 200ms-update / non-TTY suppress / `progress.New(total)` API) | tier-2 | **YES** — progress contract lives here |
| `18-batch-execution.md` | normative-batch-runtime | AC-17 (`exec` exit-4 partial / `--parallel=N` ordering) + AC-22 (single connection pool, no per-worker `flock`) + AC-23 (Phase binding) + AC-21 (§97-WINS) | tier-2 (~18 KB; concurrency mirror per P3) | **YES** — batch runtime contract lives here |
| `19-shell-completion.md` | normative-completion-pipeline | AC-18 (`mycli completion <bash\|zsh\|powershell\|fish>` / runtime `__complete` / list-values) | tier-2 | **YES** — completion contract lives here |
| `20-terminal-output-design.md` | normative-palette-and-sections | AC-19 (palette: green/red/yellow/cyan/gray; box-drawing fallback; 80–200 col width handling) | tier-2 | **YES** — palette + section conventions live here |
| `21-post-install-shell-activation.md` | normative-doctor-pipeline | AC-20 (`mycli doctor` checks + interactive shell-profile injection + `--json` structured findings) | tier-2 | **YES** — `doctor` contract lives here |

**AND** all 20 sibling files are GOVERNED-BY-NAME (no "governed-but-unnamed" rows — contrast with spec/22 AC-80's 11 unnamed rows; spec/13's contract surface is mature enough that every file has at least one AC-NN binding it by the file's number prefix);

**AND** there are NO informative-exempt files in spec/13 (contrast with spec/22 AC-80's 4 exempt rows) — every sibling file in spec/13 is normative; an auditor finding "informative file lacks §97 AC" against any spec/13 sibling is automatically a stale-cache artifact (Lesson #34) because no such files exist;

**AND** the table is **append-only within a phase** (rows MAY be added when new sibling files ship, never reworded; the "Governing §97 AC family" cell may be updated when an AC family number changes via §97-WINS evolution but the file's content kind is immutable per Lesson #25);

**AND** any new sibling file added to spec/13 in a future phase MUST add a row to this table BEFORE the file ships — the table IS the intra-module audit-followable dependency chain (mirror of spec/22 AC-80 and spec/02 AC-CG-21).

- **Verifies:** the intra-module sibling-file delegation contract for spec/13 — every one of the 20 sibling files (`02-*` through `21-*`) has an explicit row in the delegation map above with content-kind + governing-§97-AC-family + tier-visibility + restate-forbidden columns. Closes the **Lesson #21 intra-module audit-boundary < verification-boundary gap** at the intra-module sibling-file axis (Lesson #39 second axis). Mirror of **spec/22 AC-80** (33 siblings, 13/33 zero-bound crisis) and **spec/02 AC-CG-21** (16 cross-language sub-folders). Spec/13 is the **third Lesson #39 second-axis instance** — confirms the delegation-map pattern generalises to mature modules where the binding-density gap is zero but the explicit-delegation-table pattern still adds tier-1 audit-followability value (auditor no longer needs to grep 25 ACs to derive per-file governance). Until A8 (LLM-gateway re-score) unblocks, this AC declares any "sibling file orphan" or "missing §97 AC for file NN" finding against the 20 listed files a stale-cache artifact per Lesson #34. Lesson #39 sweep status after this AC: spec/02 ✅ (AC-CG-21), spec/22 ✅ (AC-80), spec/13 ✅ (this AC); remaining candidate: spec/04 (14 siblings, >10 threshold).
- **Source:** `97-acceptance-criteria.md` (this AC); cross-references all 20 sibling files listed in the table above; mirror references spec/22 AC-80, spec/02 AC-CG-21.



