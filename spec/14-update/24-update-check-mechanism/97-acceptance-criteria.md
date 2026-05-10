# Acceptance Criteria — Update Check Mechanism

**Version:** 2.0.0
**Last Updated:** 2026-04-26 (Phase 16q: full GWT rewrite — replaced 34 table-row criteria with 20 module-specific Given/When/Then ACs covering discovery, persistence, CLI behavior, pre-command hook, logging, naming standards, and migration. Old 34 criteria preserved as AC-UCM-LEGACY-001..034 at end.)
**Scope:** `spec/14-update/24-update-check-mechanism/` — Non-blocking, parallel, status-script-driven update-check mechanism (detection half of update lifecycle).
**Parent:** [spec/14-update/00-overview.md](../00-overview.md) · Inherits from [spec/14-update/97-acceptance-criteria.md](../97-acceptance-criteria.md) (AC-06..AC-20)

---

## Module Summary

§14/24-update-check-mechanism codifies the **detection half** of the update lifecycle (the **application half** — rename-first deploy, handoff, cleanup — lives in parent §14 files 01–08). This module defines: parallel V→V+5 version discovery with 6 probes (1 current + 5 lookahead), status-script fetching from `raw.githubusercontent.com`, combined JSON after parallel discovery, `UpdateChecker` table + `UpdateStatus` enum persistence, reusable `UpdateCheckerService` class, `update-check` / `do-update` CLI commands, pre-command hook with interval gating, error handling with file-system log, JSON fallback store when no SQLite exists, and migration/backwards-compat. Every check is fire-and-forget detached — no daemon, no cron, no background service. Inherits ALL **AC-06..AC-20** from parent §14 §97 per AC-UCM-01.

---

## Inlined Contracts

```text
PARENT_INHERITANCE:        ../97-acceptance-criteria.md (AC-06..AC-20)
DISCOVERY_PROBES:          6 (V current + V+1..V+5 lookahead)
PROBE_TIMEOUT:             5s per probe
DISCOVERY_DEADLINE:        10s total
MAX_LOOKAHEAD:             V+5 (hard stop, no walking)
CHECK_INTERVAL_DEFAULT:    12h
PRE_HOOK_MAX_MS:           50ms happy path
PRE_HOOK_NEVER_BLOCKS:     true (fire-and-forget)
PERSISTENCE_MODES:         SQLite (primary) + JSON fallback (atomic tmp+rename)
EXIT_CODES:                0 success, 1 generic error, 2 misuse, 3 config, 4 batch partial
UPDATE_STATUS_ENUM:        UpToDate, UpdateFound, UpdateApplied, Failed, Migrated
```

---

## Acceptance Criteria

### AC-UCM-01 — Inherits all AC-06..AC-20 from parent §14-update §97

- **Given** any artifact (doc, code, test) under `24-update-check-mechanism/`,
- **When** reviewed against parent §14 §97,
- **Then** it MUST satisfy every AC-06..AC-20 from `../97-acceptance-criteria.md` (rename-first deploy, Windows handoff, version verification, code signing, SHA-256 checksums, install script version probe, updater binary, XDG config, update command workflow, non-blocking parallel check, JSON fallback, deploy-path resolution, cleanup, atomic rollback, generic installer behavior). Conflicts MUST resolve in favor of the parent rule. Any waiver MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** Parent §14 §97 AC-06..AC-20 inheritance contract.

### AC-UCM-02 — Six probes (V + V+1..V+5) fire in parallel; wall time ≤ 6s; discovery NEVER walks past V+5

- **Given** a CLI with current version V running `update-check`,
- **When** the discovery phase executes,
- **Then** EXACTLY 6 HTTP probes MUST fire in parallel: 1 for the current version V status script + 5 lookahead probes for V+1 through V+5. The measured wall time of the full discovery phase MUST be ≤ 6 seconds on a healthy network. Discovery MUST NEVER walk past V+5 — even if all five lookahead probes return HTTP 200 with valid JSON, the algorithm MUST stop at V+5 and return the highest successful version found. A probe count ≠ 6 OR sequential (non-parallel) execution OR walking past V+5 FAILS this AC.
- **Verifies:** `00-overview.md` Defining Property #2 + `01-fundamentals.md` §3 Discovery Algorithm + AC-UCM-LEGACY-001/002.

### AC-UCM-03 — 404 = not-found (no retry); malformed JSON = logged + not-found; 200+valid JSON wins

- **Given** the 6 parallel probes from AC-UCM-02,
- **When** individual probe responses are processed,
- **Then** the response handling MUST follow: (a) HTTP 404 on ANY probe is treated as not-found — NO retry, NO error escalation, NO exponential backoff; (b) HTTP 200 with malformed/unparseable JSON is logged to `~/.<CliName>/Logs/UpdateChecker.log` with the URL + error detail, then treated as not-found; (c) HTTP 200 with valid JSON is a candidate; (d) the highest version among all candidates wins — if V+3 returns 200+valid and V+5 returns 404, the winner is V+3, NOT V. A 404 that triggers retry OR a malformed JSON that is silently swallowed OR a winner that is not the highest candidate FAILS this AC.
- **Verifies:** `01-fundamentals.md` §3.4 Response Classification + `08-error-handling.md` + AC-UCM-LEGACY-003/004/005.

### AC-UCM-04 — Per-probe timeout = 5s; total discovery deadline = 10s; timeout emits AC-UCM-04-TIMEOUT finding

- **Given** the discovery phase,
- **When** probe timing is configured,
- **Then** EACH individual probe MUST have a hard timeout of 5 seconds (TCP connect + read + parse). The TOTAL discovery phase MUST have a deadline of 10 seconds (wall-clock from first probe fired to last response processed OR deadline exceeded). A probe that exceeds 5s MUST be treated as not-found (same as 404 — no retry). If the total deadline of 10s is exceeded, discovery MUST abort immediately, return the best candidate found so far (or "no update" if none), and emit an `AC-UCM-04-TIMEOUT` warning to the log. Missing per-probe timeout OR missing total deadline OR timeout treated as error (not not-found) FAILS this AC.
- **Verifies:** `01-fundamentals.md` §3.5 Timeouts + `08-error-handling.md` + AC-UCM-LEGACY-006.

### AC-UCM-05 — `UpdateChecker` table stores BOTH `RawJson` AND each parsed column; schema matches §14/04-database-schema.md

- **Given** the persistence layer,
- **When** the `UpdateChecker` table schema is inspected,
- **Then** it MUST contain ALL of these columns: `UpdateCheckerId` (PK, UUID or auto-increment), `CurrentVersion` (string, NOT NULL), `LatestVersion` (string, nullable), `HasUpdate` (boolean/integer 0|1, NOT NULL, DEFAULT 0), `PreviousHasError` (boolean/integer 0|1, NOT NULL, DEFAULT 0 — per Phase 9), `LastCheckedAt` (datetime, nullable), `CheckIntervalHours` (integer, NOT NULL, DEFAULT 12), `RawJson` (TEXT/BLOB, nullable — the FULL raw response body), `ErrorMessage` (TEXT, nullable), `ErrorAt` (datetime, nullable), `UpdateStatusId` (TINYINT FK to `UpdateStatus` lookup, NOT NULL). The table MUST store BOTH the raw JSON AND each parsed column — parsing-only (no RawJson) OR raw-only (no parsed columns) FAILS this AC. The schema MUST match `04-database-schema.md` exactly — column names, types, nullability, defaults, and FK relationships.
- **Verifies:** `04-database-schema.md` + AC-UCM-LEGACY-007 + Phase 9 `PreviousHasError` addition.

### AC-UCM-06 — `UpdateStatus` is a code enum AND a DB lookup table with TINYINT PK; values: UpToDate, UpdateFound, UpdateApplied, Failed, Migrated

- **Given** the status enumeration,
- **When** implemented in code AND persisted in the database,
- **Then** `UpdateStatus` MUST exist in TWO forms: (a) a code enum (language-native: Go `iota`, TypeScript `const enum`, Rust `#[repr(u8)]`, C# `enum`) with EXACTLY these 5 values: `UpToDate = 0`, `UpdateFound = 1`, `UpdateApplied = 2`, `Failed = 3`, `Migrated = 4`; (b) a database lookup table `UpdateStatus` with TINYINT PK (0-4) + `Name` string + `Description` string. The code enum values MUST map 1:1 to the DB lookup PKs. Adding a 6th value requires a schema migration. Removing a value is a BREAKING CHANGE. The enum MUST NOT be a string-enum (e.g., `type UpdateStatus = "UpToDate" | "UpdateFound"`) — TINYINT PK is required for DB storage efficiency and index performance.
- **Verifies:** `04-database-schema.md` + `05-update-checker-service.md` + AC-UCM-LEGACY-008.

### AC-UCM-07 — Failed re-check does NOT clear `LatestVersion`/`HasUpdate` from prior successful check; write is atomic single-UPDATE

- **Given** an `UpdateChecker` row with `LatestVersion = "1.2.3"` and `HasUpdate = true` from a prior successful check,
- **When** a subsequent re-check fails (network error, timeout, malformed JSON),
- **Then** the row MUST retain `LatestVersion = "1.2.3"` and `HasUpdate = true` — the failed re-check does NOT clear or overwrite these values. The ONLY fields that MAY update on failure are: `ErrorMessage`, `ErrorAt`, `UpdateStatusId = Failed`. The write MUST be atomic — a single `UPDATE` statement (not read-modify-write). A failed re-check that clears `LatestVersion` OR sets `HasUpdate = false` OR uses a non-atomic write FAILS this AC. Mirrors §22 AC-75 (back-fill + write atomicity).
- **Verifies:** `05-update-checker-service.md` §4 Write Rules + `08-error-handling.md` + AC-UCM-LEGACY-010.

### AC-UCM-08 — JSON fallback at `~/.<CliName>/data/UpdateChecker.json` works when no DB exists; writes are atomic (tmp + rename)

- **Given** a CLI running on a machine with NO SQLite database (first run, embedded device, or DB-less build),
- **When** `update-check` executes,
- **Then** it MUST fall back to a JSON file at `~/.<CliName>/data/UpdateChecker.json` (path: `${XDG_DATA_HOME:-$HOME/.local/share}/<CliName>/data/UpdateChecker.json` on Unix, `%LOCALAPPDATA%\<CliName>\data\UpdateChecker.json` on Windows). The JSON schema MUST be identical to the SQLite row structure — same keys, same types, same nullability. Writes to the JSON file MUST be atomic: write to `.tmp` file in same directory, then `rename()` / `MoveFileEx` with `MOVEFILE_REPLACE_EXISTING`. A crash during write MUST leave the previous file intact. Non-atomic write OR schema mismatch OR path not XDG-compliant FAILS this AC.
- **Verifies:** `09-json-fallback-store.md` + AC-UCM-LEGACY-011/012.

### AC-UCM-09 — Plain `update-check` runs synchronously, prints formatted output, AND persists; `--async` returns in < 200ms

- **Given** a CLI with the `update-check` subcommand,
- **When** invoked in two modes,
- **Then** the behavior MUST be: (a) Plain `update-check` (no flags) runs SYNCHRONOUSLY — blocks until discovery completes, prints formatted human-readable output to stdout (version status, changelog URL, action prompt), AND writes the result to the store (SQLite OR JSON fallback); (b) `update-check --async` returns in < 200ms — it spawns a detached child process that performs the actual check and writes to the store, then the parent exits immediately; the user sees NO output from `--async`. A synchronous `update-check` that does NOT persist OR an `--async` that takes ≥ 200ms OR `--async` that prints to stdout FAILS this AC.
- **Verifies:** `06-cli-commands.md` + AC-UCM-LEGACY-013/014.

### AC-UCM-10 — `update-check --force` bypasses interval gate; `do-update` runs unattended; exit codes match §06 §3

- **Given** a CLI with `update-check` and `do-update` subcommands,
- **When** invoked with various flags,
- **Then** the behavior MUST be: (a) `update-check --force` bypasses the interval gate — it performs discovery EVEN if `Now - LastCheckedAt < CheckIntervalHours`; (b) `do-update` runs FULLY unattended — NO interactive prompt, NO TTY check, NO confirmation; it downloads, verifies, deploys, and exits; (c) `do-update` failure leaves `HasUpdate = true` so the warning persists on next command; (d) exit codes match `06-cli-commands.md` §3: `0` success, `1` generic error, `2` misuse (unknown flag), `3` config error, `4` batch partial failure. Any other exit code is FORBIDDEN. `--force` that still respects the interval gate OR `do-update` with interactive prompt OR exit code mismatch FAILS this AC.
- **Verifies:** `06-cli-commands.md` §3 + AC-UCM-LEGACY-015/016/017/018.

### AC-UCM-11 — Pre-hook returns in < 50ms; NEVER blocks; does NOT recurse on `update-check`/`do-update`; warning to stderr

- **Given** a CLI with pre-command hook integration,
- **When** the hook runs before every user command,
- **Then** it MUST satisfy: (a) returns in < 50ms on the happy path (interval gate check + spawn detached child + print trailing warning if update found); (b) NEVER blocks the user's command — even if the update-check subsystem crashes, throws, or hangs, the user's original command MUST proceed unaffected; (c) does NOT recurse — if the user's command IS `update-check` or `do-update`, the hook MUST skip the update check entirely (no infinite recursion); (d) `BackgroundUpdateCheckEnabled = false` disables the spawn entirely; (e) `PendingUpdateWarningEnabled = false` disables the trailing warning; (f) the trailing warning MUST print to **stderr**, not stdout — so it doesn't corrupt piped output. A hook that takes ≥ 50ms OR blocks on error OR recurses OR prints warning to stdout FAILS this AC.
- **Verifies:** `07-pre-command-hook.md` + AC-UCM-LEGACY-019/020/021/022/023/024.

### AC-UCM-12 — Every error written to `~/.<CliName>/Logs/UpdateChecker.log` with file + line; capped at 1 MiB; rotated to `.log.1`

- **Given** the error handling subsystem,
- **When** any error occurs during update check,
- **Then** EVERY error MUST be written to `~/.<CliName>/Logs/UpdateChecker.log` (Unix) or `%LOCALAPPDATA%\<CliName>\Logs\UpdateChecker.log` (Windows) with: (a) timestamp (ISO8601), (b) severity (Error|Warning|Info), (c) message, (d) file path, (e) line number, (f) function name. Subsystem errors MUST additionally set: `ErrorMessage` column in `UpdateChecker` table, `ErrorAt` timestamp, and `UpdateStatusId = Failed`. Errors are NEVER silently swallowed EXCEPT at the pre-hook boundary (where swallowing is intentional to prevent blocking). The log file MUST be capped at 1 MiB and rotated to `.log.1` when exceeded (not truncated — truncation loses diagnostic data). A missing log file OR missing file+line metadata OR silent swallow OR truncation instead of rotation FAILS this AC.
- **Verifies:** `08-error-handling.md` + AC-UCM-LEGACY-025/026/027/028.

### AC-UCM-13 — All JSON keys, JSON string-enum values, table names, column names, and code identifiers use PascalCase

- **Given** any JSON output, database schema, or code artifact in this module,
- **When** identifiers are inspected,
- **Then** ALL of the following MUST use PascalCase: (a) JSON keys in status script output (`CurrentVersion`, `LatestVersion`, `HasUpdate`, `ReleaseNotesUrl`), (b) JSON string-enum values (`UpToDate`, `UpdateFound`, `UpdateApplied`, `Failed`, `Migrated`), (c) database table names (`UpdateChecker`, `UpdateStatus`), (d) database column names (`UpdateCheckerId`, `CurrentVersion`, `LatestVersion`, `HasUpdate`, `LastCheckedAt`, `CheckIntervalHours`, `RawJson`, `ErrorMessage`, `ErrorAt`, `UpdateStatusId`), (e) code identifiers (class names, method names, property names). snake_case (`update_checker`), camelCase (`hasUpdate`), SCREAMING_SNAKE_CASE (`HAS_UPDATE`), or kebab-case (`has-update`) are FORBIDDEN for these identifiers. This AC applies to ALL languages — even Go (which normally uses camelCase) MUST use PascalCase for this subsystem's public identifiers per AC-CL-09 JSON key naming.
- **Verifies:** `04-database-schema.md` + `02-status-script-json.md` + AC-UCM-LEGACY-029.

### AC-UCM-14 — `UpdateChecker` table includes `Description`, `Notes`, `ErrorMessage` per Schema Rule 11 (transactional)

- **Given** the `UpdateChecker` table schema,
- **When** its columns are inspected,
- **Then** it MUST include these three free-text columns per Schema Rule 11 (transactional pattern): `Description` (TEXT, nullable, no DEFAULT — human-readable summary of the check result), `Notes` (TEXT, nullable, no DEFAULT — additional context, changelog URL, action prompt), `ErrorMessage` (TEXT, nullable, no DEFAULT — populated ONLY on failure, cleared on next success). All free-text columns MUST be nullable with no DEFAULT (Schema Rule 12). The table MUST also include `UpdateCheckerId` (PK), `CurrentVersion`, `LatestVersion`, `HasUpdate`, `PreviousHasError`, `LastCheckedAt`, `CheckIntervalHours`, `RawJson`, `ErrorAt`, `UpdateStatusId`. Missing any of these columns OR non-nullable free-text OR DEFAULT on free-text FAILS this AC.
- **Verifies:** `04-database-schema.md` + AC-UCM-LEGACY-031.

### AC-UCM-15 — No nested `if` in service code; update-checker service uses flat guard-clause structure

- **Given** the `UpdateCheckerService` implementation,
- **When** its control flow is inspected,
- **Then** it MUST contain ZERO nested `if` statements (CODE RED P6). ALL branching MUST use flat guard clauses: `if (condition) { return early; }` at the top of functions. The `UpdateCheckerService` class MUST follow this structure: (a) `CheckForUpdate()` — flat guards for interval gate, then parallel discovery, then persistence; (b) `ParseStatusJson()` — flat guards for schema validation, then extraction; (c) `WriteResult()` — flat guards for DB vs JSON fallback, then atomic write. Any nested `if` (an `if` inside another `if` at any depth) OR any `else` block longer than 3 lines OR any ternary nested inside another ternary FAILS this AC.
- **Verifies:** `05-update-checker-service.md` + AC-UCM-LEGACY-032 + CODE RED P6.

### AC-UCM-16 — JSON-to-SQLite migration: on first init, JSON contents migrate into new table; `NewRepoUrl` non-null surfaces migration banner

- **Given** a project upgrading from JSON-file storage to SQLite database,
- **When** the SQLite database is first initialized,
- **Then** the migration MUST: (a) read the existing JSON file at `~/.<CliName>/data/UpdateChecker.json`, (b) parse it into the `UpdateChecker` table row structure, (c) insert the migrated row with `UpdateStatusId = Migrated` (value 4), (d) delete or archive the JSON file (rename to `.json.migrated` — do NOT leave stale data). The migration MUST be all-or-nothing: if any step fails, the database MUST roll back and the JSON file MUST remain intact. Additionally, if the status JSON contains `NewRepoUrl` non-null (the repository has moved to a new owner/name), the pre-command hook MUST surface a migration banner via the warning channel (stderr) pointing to the new repo URL. The banner MUST appear ONCE per session, not on every command.
- **Verifies:** `09-json-fallback-store.md` + `07-pre-command-hook.md` + AC-UCM-LEGACY-033/034.

### AC-UCM-17 — `update-check --async` spawns detached child; parent exits < 200ms; child writes to store silently

- **Given** a CLI with `--async` flag support,
- **When** `update-check --async` is invoked,
- **Then** the parent process MUST exit in < 200ms. It MUST spawn a detached child process (OS-specific: `STARTF_USESHOWWINDOW` + `CREATE_NEW_PROCESS_GROUP` on Windows, `setsid()` + `nohup` on Unix) that performs the actual discovery and writes to the store. The parent MUST NOT wait for the child. The child MUST write silently — no stdout/stderr output (logs go to file). The user sees NOTHING from `--async` except the parent's < 200ms return. A parent that waits for child completion OR takes ≥ 200ms OR child that prints to stdout FAILS this AC.
- **Verifies:** `06-cli-commands.md` §2 Async Mode + AC-UCM-LEGACY-014.

### AC-UCM-18 — Pre-command hook: interval gate check + spawn `--async` if due; trailing warning to stderr if update found

- **Given** a CLI with pre-command hook integration,
- **When** the hook runs before a user command,
- **Then** it MUST: (a) check `Now - LastCheckedAt < CheckIntervalHours` (default 12h) — if NOT due, skip silently; (b) if due, spawn `update-check --async` (detached child, see AC-UCM-17) and continue immediately; (c) if `HasUpdate = true` from a PRIOR check, print a ONE-LINE trailing warning to stderr (e.g., "⚠️ Update available: 1.2.3 → 1.3.0. Run `<binary> update` to apply."); (d) the warning MUST NOT appear if the user's command IS `update-check` or `do-update` (recursion guard); (e) the warning MUST be suppressible via `PendingUpdateWarningEnabled = false`. A hook that blocks OR spawns synchronously OR prints warning to stdout OR warns on `update-check` FAILS this AC.
- **Verifies:** `07-pre-command-hook.md` + AC-UCM-LEGACY-019/020/021/022/023/024.

### AC-UCM-19 — Status script fetched from `raw.githubusercontent.com`; output is PascalCase JSON; combined after parallel discovery

- **Given** the discovery phase,
- **When** status scripts are fetched,
- **Then** the CLI MUST fetch `Status.ps1` (Windows) or `Status.sh` (Unix) from `https://raw.githubusercontent.com/{owner}/{repo}/main/` (or `/releases/download/v{X.Y.Z}/` for pinned releases). The script MUST be executed server-side semantics — it emits a JSON document to stdout, which the CLI captures and parses. The JSON MUST use PascalCase keys: `CurrentVersion`, `LatestVersion`, `HasUpdate`, `ReleaseNotesUrl`, `DownloadUrl`, `ChecksumSha256`, `NewRepoUrl`. After parallel discovery, the CLI MUST produce a "combined JSON" — the merged result of all 6 probes, with the highest successful version winning. The combined JSON schema MUST match `03-combined-json.md` exactly.
- **Verifies:** `01-fundamentals.md` §2 Status Script + `02-status-script-json.md` + `03-combined-json.md`.

### AC-UCM-20 — Self-application doctest: all 34 legacy criteria are traceable to new ACs; no orphan legacy items

- **Given** this §97 file after Phase 16q rewrite,
- **When** the legacy criteria are reviewed,
- **Then** EVERY ONE of the 34 original criteria (AC-UCM-LEGACY-001..034) MUST have a traceability note pointing to the new GWT AC that replaces it. The mapping MUST be: LEGACY-001/002 → AC-UCM-02 (discovery probes), LEGACY-003 → AC-UCM-03 (404 handling), LEGACY-004 → AC-UCM-03 (malformed JSON), LEGACY-005 → AC-UCM-03 (highest version wins), LEGACY-006 → AC-UCM-04 (timeouts), LEGACY-007 → AC-UCM-05 (UpdateChecker table), LEGACY-008 → AC-UCM-06 (UpdateStatus enum), LEGACY-009 → AC-UCM-07 (DB writes try/catch), LEGACY-010 → AC-UCM-07 (failed re-check preserves state), LEGACY-011 → AC-UCM-08 (JSON fallback), LEGACY-012 → AC-UCM-08 (atomic writes), LEGACY-013 → AC-UCM-09 (sync update-check), LEGACY-014 → AC-UCM-09/17 (--async), LEGACY-015 → AC-UCM-10 (--force), LEGACY-016 → AC-UCM-10 (do-update unattended), LEGACY-017 → AC-UCM-10 (do-update failure preserves HasUpdate), LEGACY-018 → AC-UCM-10 (exit codes), LEGACY-019 → AC-UCM-11/18 (pre-hook < 50ms), LEGACY-020 → AC-UCM-11/18 (pre-hook never blocks), LEGACY-021 → AC-UCM-11/18 (pre-hook no recursion), LEGACY-022 → AC-UCM-11/18 (BackgroundUpdateCheckEnabled=false disables spawn), LEGACY-023 → AC-UCM-11/18 (PendingUpdateWarningEnabled=false disables warning), LEGACY-024 → AC-UCM-11/18 (warning to stderr), LEGACY-025 → AC-UCM-12 (error log file), LEGACY-026 → AC-UCM-12 (ErrorMessage/ErrorAt/Failed), LEGACY-027 → AC-UCM-12 (no silent swallow), LEGACY-028 → AC-UCM-12 (log rotation), LEGACY-029 → AC-UCM-13 (PascalCase), LEGACY-030 → AC-UCM-14 (free-text nullable), LEGACY-031 → AC-UCM-14 (Description/Notes/ErrorMessage), LEGACY-032 → AC-UCM-15 (no nested if), LEGACY-033 → AC-UCM-16 (JSON-to-SQLite migration), LEGACY-034 → AC-UCM-16 (NewRepoUrl migration banner). Any legacy criterion without a traceability note OR a note pointing to a non-existent new AC FAILS this AC.
- **Verifies:** This §97 file integrity + AC-CL-20 traceability requirement.

---

## Legacy Criteria (preserved for traceability)

### AC-UCM-LEGACY-001 — All six probes (V + V+1..V+5) fire in parallel — measured wall time of full discovery ≤ 6s on a healthy network

> Original stub: "| 1 | All six probes (V + V+1..V+5) fire in parallel — measured wall time of full discovery ≤ 6s on a healthy network | Integration test with mocked HTTP |"
> Replaced by: AC-UCM-02 (discovery probes with parallel guarantee + wall time ≤ 6s + hard V+5 stop).

### AC-UCM-LEGACY-002 — Discovery NEVER walks past V+5, even if all five lookahead probes succeed

> Original stub: "| 2 | Discovery NEVER walks past V+5, even if all five lookahead probes succeed | Unit test: assert `len(Candidates) == 5` always |"
> Replaced by: AC-UCM-02 (hard V+5 stop).

### AC-UCM-LEGACY-003 — A 404 on any probe is treated as not-found (no retry, no error escalation)

> Original stub: "| 3 | A 404 on any probe is treated as not-found (no retry, no error escalation) | Unit test |"
> Replaced by: AC-UCM-03 (404 = not-found, no retry, no escalation).

### AC-UCM-LEGACY-004 — A 200 with malformed JSON is logged and treated as not-found

> Original stub: "| 4 | A 200 with malformed JSON is logged and treated as not-found | Unit test |"
> Replaced by: AC-UCM-03 (malformed JSON logged + not-found).

### AC-UCM-LEGACY-005 — The highest version returning HTTP 200 + valid JSON wins

> Original stub: "| 5 | The highest version returning HTTP 200 + valid JSON wins | Unit test with mixed 200/404 matrix |"
> Replaced by: AC-UCM-03 (highest version wins).

### AC-UCM-LEGACY-006 — Per-probe HTTP timeout = 5s; total discovery deadline = 10s

> Original stub: "| 6 | Per-probe HTTP timeout = 5s; total discovery deadline = 10s | Code review + timeout test |"
> Replaced by: AC-UCM-04 (per-probe 5s + total 10s + timeout findings).

### AC-UCM-LEGACY-007 — `UpdateChecker` table stores BOTH `RawJson` AND each parsed column

> Original stub: "| 7 | `UpdateChecker` table stores BOTH `RawJson` AND each parsed column | Schema inspection + insert/select test |"
> Replaced by: AC-UCM-05 (RawJson + parsed columns + exact schema match).

### AC-UCM-LEGACY-008 — `UpdateStatus` is implemented as a code enum AND a DB lookup table with TINYINT PK

> Original stub: "| 8 | `UpdateStatus` is implemented as a code enum AND a DB lookup table with TINYINT PK | Schema inspection + enum test |"
> Replaced by: AC-UCM-06 (code enum + DB lookup + 5 values + TINYINT PK).

### AC-UCM-LEGACY-009 — All DB writes wrapped in try/catch (or language equivalent)

> Original stub: "| 9 | All DB writes wrapped in try/catch (or language equivalent) | Static check / code review |"
> Replaced by: AC-UCM-07 (atomic single-UPDATE + try/catch + failed re-check preserves state).

### AC-UCM-LEGACY-010 — A failed re-check does NOT clear `LatestVersion`/`HasUpdate` from a prior successful check

> Original stub: "| 10 | A failed re-check does NOT clear `LatestVersion`/`HasUpdate` from a prior successful check | Unit test |"
> Replaced by: AC-UCM-07 (failed re-check preserves LatestVersion/HasUpdate).

### AC-UCM-LEGACY-011 — When no DB exists, JSON fallback at `~/.<CliName>/data/UpdateChecker.json` works with the same interface

> Original stub: "| 11 | When no DB exists, JSON fallback at `~/.<CliName>/data/UpdateChecker.json` works with the same interface | Backend-swap integration test |"
> Replaced by: AC-UCM-08 (JSON fallback + XDG paths + atomic writes).

### AC-UCM-LEGACY-012 — JSON fallback writes are atomic (tmp + rename)

> Original stub: "| 12 | JSON fallback writes are atomic (tmp + rename) | Crash-injection test |"
> Replaced by: AC-UCM-08 (atomic tmp+rename writes).

### AC-UCM-LEGACY-013 — Plain `update-check` runs synchronously, prints formatted output, AND persists

> Original stub: "| 13 | Plain `update-check` runs synchronously, prints formatted output, AND persists | E2E test |"
> Replaced by: AC-UCM-09 (sync + print + persist).

### AC-UCM-LEGACY-014 — `update-check --async` returns in < 200 ms and the child writes to the store

> Original stub: "| 14 | `update-check --async` returns in < 200 ms and the child writes to the store | Process-timing test |"
003e Replaced by: AC-UCM-09/17 (--async < 200ms + detached child).

### AC-UCM-LEGACY-015 — `update-check --force` bypasses the interval gate

> Original stub: "| 15 | `update-check --force` bypasses the interval gate | Unit test |"
> Replaced by: AC-UCM-10 (--force bypasses interval).

### AC-UCM-LEGACY-016 — `do-update` runs unattended (no interactive prompt)

> Original stub: "| 16 | `do-update` runs unattended (no interactive prompt) | E2E test |"
> Replaced by: AC-UCM-10 (do-update unattended).

### AC-UCM-LEGACY-017 — `do-update` failure leaves `HasUpdate = true` so the warning persists

> Original stub: "| 17 | `do-update` failure leaves `HasUpdate = true` so the warning persists | Unit test |"
> Replaced by: AC-UCM-10 (do-update failure preserves HasUpdate).

### AC-UCM-LEGACY-018 — Exit codes match [06 §3](./06-cli-commands.md#3-exit-codes)

> Original stub: "| 18 | Exit codes match [06 §3](./06-cli-commands.md#3-exit-codes) | E2E test |"
> Replaced by: AC-UCM-10 (exit codes 0/1/2/3/4).

### AC-UCM-LEGACY-019 — Pre-hook returns in < 50 ms on the happy path

> Original stub: "| 19 | Pre-hook returns in < 50 ms on the happy path | Benchmark |"
> Replaced by: AC-UCM-11/18 (pre-hook < 50ms).

### AC-UCM-LEGACY-020 — Pre-hook NEVER blocks the user's command, even on subsystem error

> Original stub: "| 20 | Pre-hook NEVER blocks the user's command, even on subsystem error | Fault-injection test |"
> Replaced by: AC-UCM-11/18 (pre-hook never blocks).

### AC-UCM-LEGACY-021 — Pre-hook does NOT recurse on `update-check` / `do-update`

> Original stub: "| 21 | Pre-hook does NOT recurse on `update-check` / `do-update` | Unit test |"
> Replaced by: AC-UCM-11/18 (no recursion).

### AC-UCM-LEGACY-022 — `BackgroundUpdateCheckEnabled = false` disables the spawn

> Original stub: "| 22 | `BackgroundUpdateCheckEnabled = false` disables the spawn | Config test |"
> Replaced by: AC-UCM-11/18 (config gate).

### AC-UCM-LEGACY-023 — `PendingUpdateWarningEnabled = false` disables the warning

> Original stub: "| 23 | `PendingUpdateWarningEnabled = false` disables the warning | Config test |"
> Replaced by: AC-UCM-11/18 (warning gate).

### AC-UCM-LEGACY-024 — Trailing warning prints to **stderr**, not stdout

> Original stub: "| 24 | Trailing warning prints to **stderr**, not stdout | Pipe-redirection test |"
> Replaced by: AC-UCM-11/18 (stderr discipline).

### AC-UCM-LEGACY-025 — Every error is written to `~/.<CliName>/Logs/UpdateChecker.log` with file + line metadata

> Original stub: "| 25 | Every error is written to `~/.<CliName>/Logs/UpdateChecker.log` with file + line metadata | Log-format test |"
> Replaced by: AC-UCM-12 (error logging).

### AC-UCM-LEGACY-026 — Subsystem errors set `ErrorMessage`, `ErrorAt`, and `UpdateStatusId = Failed`

> Original stub: "| 26 | Subsystem errors set `ErrorMessage`, `ErrorAt`, and `UpdateStatusId = Failed` | Unit test |"
> Replaced by: AC-UCM-12 (subsystem error columns).

### AC-UCM-LEGACY-027 — Errors are NEVER silently swallowed except at the named pre-hook boundary

> Original stub: "| 27 | Errors are NEVER silently swallowed except at the named pre-hook boundary | Static check (CODE RED P1) |"
> Replaced by: AC-UCM-12 (no silent swallow).

### AC-UCM-LEGACY-028 — Log file is capped at 1 MiB and rotated to `.log.1`

> Original stub: "| 28 | Log file is capped at 1 MiB and rotated to `.log.1` | File-size test |"
> Replaced by: AC-UCM-12 (log rotation).

### AC-UCM-LEGACY-029 — All JSON keys, JSON string-enum values, table names, column names, and code identifiers use PascalCase

> Original stub: "| 29 | All JSON keys, JSON string-enum values, table names, column names, and code identifiers use PascalCase | `validate-guidelines.py` |"
> Replaced by: AC-UCM-13 (PascalCase mandate).

### AC-UCM-LEGACY-030 — All free-text columns are nullable with no DEFAULT (Schema Rule 12)

> Original stub: "| 30 | All free-text columns are nullable with no DEFAULT (Schema Rule 12) | SQL linter |"
> Replaced by: AC-UCM-14 (Schema Rule 12 compliance).

### AC-UCM-LEGACY-031 — `UpdateChecker` includes `Description`, `Notes`, `ErrorMessage` (Schema Rule 11 — transactional)

> Original stub: "| 31 | `UpdateChecker` includes `Description`, `Notes`, `ErrorMessage` (Schema Rule 11 — transactional) | Schema inspection |"
> Replaced by: AC-UCM-14 (Schema Rule 11 transactional columns).

### AC-UCM-LEGACY-032 — No nested `if` in service code (CODE RED P6)

> Original stub: "| 32 | No nested `if` in service code (CODE RED P6) | `validate-guidelines.py` |"
> Replaced by: AC-UCM-15 (flat guard-clause structure).

### AC-UCM-LEGACY-033 — A project upgrading from JSON to SQLite migrates the JSON contents into the new table on first init

> Original stub: "| 33 | A project upgrading from JSON to SQLite migrates the JSON contents into the new table on first init | Migration test |"
> Replaced by: AC-UCM-16 (JSON-to-SQLite migration).

### AC-UCM-LEGACY-034 — Status JSON `NewRepoUrl` non-null surfaces a migration banner via the warning channel

> Original stub: "| 34 | Status JSON `NewRepoUrl` non-null surfaces a migration banner via the warning channel | E2E test |"
> Replaced by: AC-UCM-16 (NewRepoUrl migration banner).
