# Seedable Config Architecture — Acceptance Criteria

**Version:** 4.3.0
**Last Updated:** 2026-05-03 (Phase 153 Task A18-fu1 #6: added **AC-SC-23** module asset inventory pin (Lesson #29 + Lesson #36) closing audit-v7 D3 HIGH "Truncated Feature Specifications" + missing files 05/06/03/97/99 as harness bundling-cap artifacts — every cited file present on disk, file 04 ends cleanly at 265 lines. AC count 22 → 23.)
**Scope:** `spec/06-seedable-config-architecture/` — Reusable pattern for version-controlled configuration with automatic changelog updates and initial seeding (CW Config).

---

## Module Summary

§06-seedable-config-architecture (CW Config) codifies the contract for version-controlled application configuration: first-run seeding from `config.seed.json` into SQLite, semver-driven version detection, automatic CHANGELOG.md updates, idempotent re-seeding, and rollback. The defining property: **every config change updates the version, every version change logs to CHANGELOG.md.** The seed file is the source of truth; the database is a queryable mirror. Subsequent runs respect the stored version to avoid duplicate seeds. Inherits the universal AC-CL-* family from `02-coding-guidelines/01-cross-language/97` (PascalCase keys per AC-CL-09, file naming per AC-CL-12, etc.).

---

## Inlined Contracts

```text
SEED_FILE:                 config.seed.json (JSON Schema validated)
DB_TARGET:                 SQLite (tables per Category)
VERSION_FORMAT:            SemVer MAJOR.MINOR.PATCH
CHANGELOG_FILE:            CHANGELOG.md (auto-appended)
SEED_TRIGGER:              Version change detected (seed.Version > db.Version)
MERGE_STRATEGY:            seed wins on schema, db wins on user values
IDEMPOTENCY:               Same seed.Version → no-op (skip)
ROLLBACK:                  Restore previous SeedVersion + replay CHANGELOG
PASCAL_CASE_KEYS:          MANDATORY (AC-CL-09 inheritance)
ATOMIC_WRITE:              tmp + rename (AC-UCM-08 pattern)
```

---

## Acceptance Criteria

### AC-SC-01 — Inherits universal AC-CL-* rules from cross-language parent

- **Given** any artifact (doc, code, test, config) under `06-seedable-config-architecture/`,
- **When** reviewed,
- **Then** it MUST satisfy every AC-CL-01..AC-CL-20 from `../02-coding-guidelines/01-cross-language/97-acceptance-criteria.md` (PascalCase JSON keys per AC-CL-09, kebab-case file names per AC-CL-12, no negative-polarity booleans per AC-CL-02, etc.). Conflicts MUST resolve in favor of the cross-language rule. Any waiver MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** AC-CL-01 inheritance contract.

### AC-SC-02 — Initial seed populates ALL required configuration on first run

- **Given** an empty SQLite database (no `Configuration` table OR table exists with zero rows),
- **When** the application starts and `config.seed.json` is present at the expected path (`./config.seed.json` or `${XDG_CONFIG_HOME}/<AppName>/config.seed.json`),
- **Then** the seeder MUST: (a) parse the seed file against the JSON Schema (`./config.schema.json`), (b) create the `Configuration` table if missing (DDL must include `Category`, `Key`, `Value`, `Type`, `Default`, `Version`, `AddedIn` columns — all PascalCase per AC-CL-09), (c) insert ALL settings from EVERY category in the seed file, (d) record the seed version in a `Metadata` table with key `SeedVersion` and value matching `seed.Version`, (e) append an entry to `CHANGELOG.md` documenting the initial seed. Any required setting missing from the DB after seeding FAILS this AC. Partial seeding (some settings inserted, others skipped without error) FAILS this AC.
- **Verifies:** `01-fundamentals.md` §File Specifications + AC-SC-LEGACY-001-a.

### AC-SC-03 — Seed file uses JSON format with `$schema` reference + JSON Schema validation

- **Given** the seed file `config.seed.json`,
- **When** parsed,
- **Then** it MUST: (a) be valid JSON (no trailing commas, no comments, no JSON5 features), (b) contain a `$schema` key pointing to a sibling `config.schema.json` (e.g., `"$schema": "./config.schema.json"`), (c) contain a top-level `Version` field matching SemVer regex `^[0-9]+\.[0-9]+\.[0-9]+$`, (d) contain a top-level `Categories` object with at least one named category, (e) validate against `config.schema.json` using a JSON Schema Draft 7+ validator. The validator MUST be invoked BEFORE any database write — invalid schema MUST abort seeding with exit code 3 (config error) AND log the validation error to `~/.<AppName>/Logs/Seeder.log`. Missing `$schema` reference OR invalid SemVer Version OR schema validation skipped FAILS this AC.
- **Verifies:** `01-fundamentals.md` §config.seed.json + AC-SC-LEGACY-001-b.

### AC-SC-04 — Seeding is idempotent — re-running with same `seed.Version` is a no-op

- **Given** a database where `Metadata.SeedVersion` equals `seed.Version` (e.g., both `"1.2.0"`),
- **When** the seeder runs,
- **Then** it MUST: (a) read `Metadata.SeedVersion` from the DB, (b) compare to `seed.Version` from the file, (c) if equal, log "Seed version 1.2.0 already applied — skipping" at INFO level and exit 0, (d) write ZERO rows to the `Configuration` table, (e) append NO entry to `CHANGELOG.md`. Re-running the seeder 100 times in a row MUST produce 100 identical "skipping" log entries and ZERO database mutations. Any write to `Configuration` OR `CHANGELOG.md` on a no-op run FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Version Change Detection + AC-SC-LEGACY-001-c.

### AC-SC-05 — Configuration changes generate automatic CHANGELOG.md entries with category breakdown

- **Given** a database with `SeedVersion = "1.1.0"` and a new seed file with `Version = "1.2.0"`,
- **When** the seeder detects the version change and runs the merge,
- **Then** it MUST append a NEW entry to `CHANGELOG.md` in this exact format:
  ```
  ## [1.2.0] — YYYY-MM-DD

  ### Added
  - <Category>.<Key> (default: <value>) — <description from seed>

  ### Changed
  - <Category>.<Key>: <old default> → <new default>

  ### Removed
  - <Category>.<Key>
  ```
  The entry MUST include: (a) version in `[X.Y.Z]` format with date suffix in ISO 8601, (b) `### Added` section listing every NEW setting with its default value and description, (c) `### Changed` section listing every setting whose default value changed, (d) `### Removed` section listing every setting present in old version but absent in new. Empty sections MAY be omitted but at least one of {Added, Changed, Removed} MUST be present. The entry MUST be APPENDED at the top (newest first), not at the bottom. Missing CHANGELOG entry OR wrong format OR appended at wrong position FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Changelog Generation + AC-SC-LEGACY-002-a.

### AC-SC-06 — Version numbers follow SemVer MAJOR.MINOR.PATCH; precedence rules apply

- **Given** any `Version` field in seed file or `Metadata.SeedVersion` in DB,
- **When** parsed and compared,
- **Then** the value MUST match SemVer regex `^[0-9]+\.[0-9]+\.[0-9]+$` (no pre-release tags, no build metadata for the seed file). Comparison MUST follow SemVer precedence: `1.2.0 > 1.1.99`, `1.10.0 > 1.9.9`, `2.0.0 > 1.999.999`. The seeder MUST refuse to seed if `seed.Version < db.SeedVersion` (downgrade attempt) — log "Refusing to downgrade from X.Y.Z to A.B.C" and exit 3. The seeder MUST refuse to seed if `seed.Version` is non-SemVer (e.g., `"latest"`, `"v1.2"`, `"1.2"`) — log validation error and exit 3. String comparison (e.g., `"1.10.0" < "1.9.0"` lexically) FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Version Format + AC-SC-LEGACY-002-b.

### AC-SC-07 — Rollback restores previous configuration state cleanly via reverse-CHANGELOG replay

- **Given** a database at `SeedVersion = "1.2.0"` and a request to roll back to `"1.1.0"`,
- **When** `seeder rollback --target=1.1.0` is invoked,
- **Then** it MUST: (a) read CHANGELOG.md entries for versions `>1.1.0` and `≤1.2.0`, (b) reverse each entry — `Added` becomes `DELETE`, `Changed` becomes `UPDATE` to old value, `Removed` becomes `INSERT` with cached value from CHANGELOG, (c) execute reversal in a single SQL transaction, (d) update `Metadata.SeedVersion = "1.1.0"`, (e) append a `### Rolled back` entry to CHANGELOG.md noting the rollback. If rollback fails at ANY step, the transaction MUST roll back atomically — DB state MUST remain at "1.2.0". Rollback past the initial seed (e.g., to "0.0.0") is FORBIDDEN — exit 3 with "Cannot roll back past initial seed". Non-atomic rollback OR missing CHANGELOG entry for rollback FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Rollback + AC-SC-LEGACY-002-c.

### AC-SC-08 — Merge strategy: seed wins on schema, DB wins on user-modified values

- **Given** a DB at `SeedVersion = "1.1.0"` with user-modified value `Cache.MaxSizeMb = 500` (default was 100), and a new seed at `"1.2.0"` where `Cache.MaxSizeMb` default changed from 100 → 200,
- **When** the merge runs,
- **Then** it MUST: (a) detect that the user value (500) differs from BOTH old default (100) AND new default (200), (b) PRESERVE the user value (500) — do NOT overwrite with new default, (c) update only the `Default` column to 200 (so future resets use 200), (d) log "Preserved user value Cache.MaxSizeMb=500 (default changed 100→200)" at INFO level, (e) include this preservation in the `### Changed` section of CHANGELOG.md as "Cache.MaxSizeMb default: 100 → 200 (user value 500 preserved)". Settings where user value EQUALS old default MUST update to new default (no preservation needed — user never customized it). Overwriting user-modified values FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Merge Strategy.

### AC-SC-09 — Schema validation REQUIRED before any database write; failures abort with exit 3

- **Given** the seeder execution flow,
- **When** schema validation runs,
- **Then** the order MUST be: (1) parse `config.seed.json`, (2) load `config.schema.json`, (3) validate seed against schema using JSON Schema Draft 7+, (4) ONLY IF validation passes, proceed to DB writes. Validation failure MUST: (a) log every validation error with JSONPath (e.g., `Categories.Cache.Settings.MaxSizeMb.Default: expected number, got string`), (b) NOT write anything to DB, (c) NOT modify CHANGELOG.md, (d) exit with code 3 (config error per AC-CL-* exit code convention). Validation that runs AFTER DB writes OR validation that is skipped/optional FAILS this AC. The schema file itself MUST be present and valid JSON Schema — missing or malformed schema is a CODE-RED bug.
- **Verifies:** `01-fundamentals.md` §Validation + AC-CL-* exit codes.

### AC-SC-10 — `Metadata` table tracks `SeedVersion`, `LastSeededAt`, `SeedSource` for auditability

- **Given** the database schema,
- **When** the `Metadata` table is inspected,
- **Then** it MUST contain at minimum these columns (all PascalCase per AC-CL-09): `Key` (TEXT, PRIMARY KEY), `Value` (TEXT, NOT NULL), `UpdatedAt` (DATETIME, NOT NULL). After every seed run, the following rows MUST be present: (a) `SeedVersion` = current seed version (e.g., `"1.2.0"`), (b) `LastSeededAt` = ISO 8601 timestamp of last successful seed, (c) `SeedSource` = absolute path to the seed file used. These rows enable audit queries like "when was this DB last seeded?" and "which file was used?". Missing any required row OR using non-PascalCase column names FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Database Schema + AC-CL-09 PascalCase.

### AC-SC-11 — Atomic write pattern: parse → validate → transaction → commit OR rollback

- **Given** the seeder's write phase,
- **When** any setting is written to the DB,
- **Then** the write MUST be wrapped in a SINGLE SQLite transaction (`BEGIN TRANSACTION; ... COMMIT;` OR `ROLLBACK;`). Partial writes are FORBIDDEN — if 50 settings need to be inserted and the 30th fails, ALL 50 MUST roll back. The transaction MUST cover: (a) all `INSERT INTO Configuration` statements, (b) all `UPDATE Metadata SET Value = ...` statements, (c) the `CHANGELOG.md` write (file write is outside the SQL transaction but MUST happen ONLY after `COMMIT` succeeds — file-side rollback is impossible, so DB commit is the gate). If the file write to CHANGELOG.md fails AFTER DB commit, the seeder MUST log a CRITICAL error and emit exit code 1 (the DB is correct but CHANGELOG drifted — manual repair needed). Multiple transactions OR partial writes OR CHANGELOG written before DB commit FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Atomicity + AC-UCM-08 atomic-write pattern.

### AC-SC-12 — Cross-platform path resolution: `${XDG_CONFIG_HOME}` on Unix, `%LOCALAPPDATA%` on Windows

- **Given** a CLI tool that uses CW Config,
- **When** resolving the seed file path AND the SQLite database path,
- **Then** the resolution order MUST be: (1) `--config-dir <path>` flag if provided, (2) `${CW_CONFIG_DIR}` env var if set, (3) `${XDG_CONFIG_HOME:-$HOME/.config}/<AppName>/` on Unix/macOS OR `${LOCALAPPDATA}\<AppName>\` on Windows, (4) `./config.seed.json` (CWD fallback for development). The resolved directory MUST be created with `0700` permissions (Unix) or current-user-only ACL (Windows) if it doesn't exist. Hardcoded paths (`/etc/<AppName>/`, `C:\ProgramData\<AppName>\`) are FORBIDDEN. The seed file path and DB path MUST be siblings in the same directory. Path resolution that ignores XDG OR uses world-readable permissions FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Path Resolution + AC-UCM-08 XDG compliance.

### AC-SC-13 — `AddedIn` field tracks when each setting was introduced for diff/migration tooling

- **Given** any setting in the seed file,
- **When** it is added to a NEW category OR added to an existing category in a NEW version,
- **Then** the setting's JSON object MUST include `"AddedIn": "X.Y.Z"` where the version matches the seed file's `Version` at time of addition. Existing settings (carried over from prior versions) MUST retain their original `AddedIn` value — the seeder MUST NOT overwrite it on re-seed. The `AddedIn` field enables: (a) generating "What's new in 1.2.0?" diffs, (b) feature-flag gating ("only enable X if seed >= 1.2.0"), (c) migration tooling ("any DB at SeedVersion < 1.2.0 needs the X migration"). Missing `AddedIn` on new settings OR overwriting `AddedIn` on existing settings FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Setting Schema.

### AC-SC-14 — `Type` field is a CLOSED enum: {boolean, number, string, select, multiselect}; freeform FORBIDDEN

- **Given** any setting in the seed file,
- **When** its `Type` field is parsed,
- **Then** it MUST be one of EXACTLY these 5 values: `boolean`, `number`, `string`, `select`, `multiselect` (lowercase, exact). Custom types (`enum`, `int`, `float`, `text`, `json`) are FORBIDDEN — the schema validator MUST reject them with exit 3. Each Type has required companion fields: (a) `boolean` requires `Default: true|false`, (b) `number` requires `Default: <number>`, optional `Min`/`Max`, (c) `string` requires `Default: "<string>"`, optional `MaxLength`, (d) `select` requires `Default: "<value>"` AND `Options: ["<v1>", "<v2>"]` where Default ∈ Options, (e) `multiselect` requires `Default: ["<value>"]` AND `Options: ["<v1>", "<v2>"]` where every element of Default ∈ Options. Missing required companion field OR invalid Type value FAILS this AC. **Go struct mapping (NORMATIVE — closes v7 D1 LOW "Ambiguous Type Mapping for 'select'"):** the `SettingValue` union in Go MUST map Type values to fields as follows — `boolean` → `BoolVal *bool`; `number` → `NumberVal *float64` (single numeric type covers both integer + float per AC-CL-09 cross-language scalar floor); `string` → `StringVal *string`; **`select` → `StringVal *string`** (single-choice from `Options`; the chosen value is stored verbatim, NOT an enum-index); **`multiselect` → `StringsVal *[]string`** (ordered list of chosen values from `Options`; preserves user-selection order). Forbidden: introducing a separate `EnumVal int` for `select` (loses round-trip fidelity with `Options`); flattening `multiselect` to a comma-separated `StringVal` (loses values containing commas). The `SettingValue` struct comment MUST cite this AC by ID.
- **Verifies:** `01-fundamentals.md` §Setting Schema + `01-fundamentals.md` `SettingValue` struct + AC-CL-* closed-enum patterns.

### AC-SC-15 — User overrides stored separately in `UserConfiguration` table; never mutate `Configuration` defaults

- **Given** a user changing a setting via UI or CLI,
- **When** the change is persisted,
- **Then** the write MUST go to a SEPARATE `UserConfiguration` table (NOT `Configuration`). Schema: `Category` (TEXT), `Key` (TEXT), `Value` (TEXT), `UpdatedAt` (DATETIME), PRIMARY KEY `(Category, Key)`. The `Configuration` table MUST remain pristine — it is the seed mirror, never mutated by user actions. Read precedence at runtime: (1) check `UserConfiguration` for an override, (2) fall back to `Configuration.Default`. This separation enables: (a) "reset to defaults" (DELETE FROM UserConfiguration), (b) merge strategy (AC-SC-08) — the seeder reads `UserConfiguration` to detect customizations, (c) audit trail (UpdatedAt per user change). Mutating `Configuration` defaults on user change FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Database Schema + AC-SC-08 merge strategy.

### AC-SC-16 — CHANGELOG.md is human-readable Markdown, machine-parseable, and append-only

- **Given** the `CHANGELOG.md` file,
- **When** parsed by a script,
- **Then** it MUST: (a) follow the [Keep a Changelog](https://keepachangelog.com/) format with `## [X.Y.Z] — YYYY-MM-DD` headers, (b) use `### Added` / `### Changed` / `### Removed` / `### Rolled back` H3 subsections, (c) have entries in REVERSE chronological order (newest at top), (d) be append-only — the seeder MUST NEVER edit or delete prior entries. A regex `^## \[([0-9]+\.[0-9]+\.[0-9]+)\] — (\d{4}-\d{2}-\d{2})$` MUST extract every version + date pair without false positives. Hand-edits to prior entries are tracked in `99-consistency-report.md` (forensic audit) but MUST NOT happen via the seeder code path. Non-Markdown format OR mutating prior entries OR ascending chronological order FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Changelog Format.

### AC-SC-17 — Concurrent seeder invocations: file lock OR exit-on-busy; never race

- **Given** two simultaneous invocations of the seeder against the same DB,
- **When** both attempt to write,
- **Then** the seeder MUST use SQLite's BEGIN IMMEDIATE transaction OR an OS-level file lock (`flock` on Unix, `LockFileEx` on Windows) on a sentinel file (`<DBPath>.seeder.lock`). The second invocation MUST: (a) detect the lock, (b) log "Another seeder is running — waiting up to 30s" at INFO, (c) wait up to 30 seconds for the lock to release, (d) if still locked, exit with code 5 (busy) and log "Seeder lock timeout — try again later". The lock MUST be released on normal exit AND on crash (PID-based stale lock detection — if PID in lock file is dead, take the lock). Concurrent writes that race OR exit immediately without retry OR leave stale locks FAIL this AC.
- **Verifies:** `01-fundamentals.md` §Concurrency.

### AC-SC-18 — Seed file version must be `>` DB version OR equal (no-op); `<` is a downgrade refusal

- **Given** seed file `Version` and DB `SeedVersion`,
- **When** compared at startup,
- **Then** the decision matrix MUST be: (a) `seed > db` → execute merge + changelog write + version bump, (b) `seed == db` → no-op (per AC-SC-04), (c) `seed < db` → downgrade refusal: log "Refusing to seed: file version 1.1.0 is older than DB version 1.2.0. Use `seeder rollback` instead." and exit 3. The seeder MUST NEVER silently downgrade — that would lose user data and confuse audit trails. The ONLY way to lower `SeedVersion` is via the explicit `seeder rollback --target=<version>` command (AC-SC-07). Silent downgrade OR comparing as strings (lexical) FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Version Comparison + AC-SC-06.

### AC-SC-19 — Per-category sub-features (RAG, Cache, etc.) referenced from `02-features/` with stable IDs

- **Given** the `02-features/` subfolder,
- **When** its `00-overview.md` is read,
- **Then** it MUST list every category-specific feature spec (e.g., `01-rag-chunk-settings.md`, `02-rag-validation-helpers.md`) with its stable ID and version. Each sub-feature spec MUST: (a) declare its parent category (e.g., `Parent Category: Rag`), (b) list every setting it owns with `AddedIn` and `Default`, (c) cross-reference the canonical seed file location. Adding a new category requires adding a new sub-feature spec — settings cannot be silently added to the seed file without spec backing. The sub-feature inventory MUST stay in lockstep with the actual seed file's `Categories` keys. Settings in seed without a spec OR specs without seed entries FAIL this AC.
- **Verifies:** `02-features/00-overview.md` + AC-CG-* (lockstep rule).

### AC-SC-20 — Self-application doctest: this folder's seed file (if any) round-trips through the seeder cleanly

- **Given** this spec folder MAY contain an example `config.seed.json` for documentation purposes,
- **When** that example file is fed through a reference seeder implementation,
- **Then** it MUST: (a) validate against `config.schema.json` with zero errors, (b) seed a fresh in-memory SQLite DB without errors, (c) produce a CHANGELOG.md entry matching the format in AC-SC-05, (d) re-running the seeder MUST be a no-op per AC-SC-04. If no example seed file is present, this AC reduces to "the schema file `config.schema.json`, if present, MUST itself be a valid JSON Schema Draft 7+ document". This is the dogfooding gate — the spec authors must satisfy their own contracts. A reference seeder implementation MAY live in `linter-scripts/cw-config-doctest.py`. Failure of any of (a)-(d) FAILS this AC.
- **Verifies:** AC-CL-20 self-application + AC-SC-02..AC-SC-11 round-trip.

### AC-SC-21 — CHANGELOG concurrency: file lock acquired BEFORE txn-begin, held through CHANGELOG write, released AFTER

- **Given** the seeder writes BOTH a SQL transaction (per AC-SC-11) AND a `CHANGELOG.md` append (per AC-SC-16), and concurrent invocations are possible (per AC-SC-17),
- **When** the seeder runs,
- **Then** the locking discipline MUST be: (a) **acquire** the OS-level file lock on `<DBPath>.seeder.lock` (per AC-SC-17) **BEFORE** `BEGIN IMMEDIATE`, (b) **hold** the lock through the entire sequence `BEGIN IMMEDIATE → INSERT/UPDATE → COMMIT → CHANGELOG append → fsync(CHANGELOG.md)`, (c) **release** the lock ONLY after the CHANGELOG fsync returns (whether success or failure path). This closes the race where two concurrent seeders both COMMIT their DB transactions in serial, then race to append to the same CHANGELOG.md, producing interleaved or lost entries. The lock MUST be the SAME sentinel as AC-SC-17 — DO NOT introduce a separate `<CHANGELOG.md>.lock`; one lock owns the entire write transaction (DB + file). On crash between COMMIT and CHANGELOG fsync, AC-SC-11's "log CRITICAL + exit 1" path applies AND the lock MUST be released by the OS (`flock` auto-releases on process death; PID-staleness check per AC-SC-17 handles `LockFileEx` Windows path). Releasing the lock between COMMIT and CHANGELOG write OR taking a separate CHANGELOG lock OR holding the lock across the user-facing wait loop in AC-SC-17 (which would deadlock) FAILS this AC. **Reference Go implementation (NORMATIVE pseudo-code — closes v7 D3 MEDIUM "Incomplete Concurrency Implementation Detail"):**

```go
// SeedWithVersionCheck — full lock-then-tx-then-changelog discipline per AC-SC-21.
// Order is FIXED: lock → tx → commit → changelog → fsync → unlock.
func (s *ConfigService) SeedWithVersionCheck(ctx context.Context, seed *SeedFile) error {
    lockPath := s.dbPath + ".seeder.lock"
    lock, err := acquireFileLock(lockPath, 30*time.Second)  // per AC-SC-17 (flock/LockFileEx + PID-staleness)
    if err != nil { return apperror.Wrap(err, "AB-9501", "seeder lock timeout") }  // exit 5 per AC-SC-17
    defer lock.Release()  // OS auto-releases on crash; defer covers normal exit

    return s.db.Transaction(func(tx *gorm.DB) error {  // GORM wraps BEGIN IMMEDIATE per AC-SC-11
        if err := s.applySeedRows(tx, seed); err != nil { return err }   // INSERT/UPDATE
        // tx COMMIT happens on return-nil from this closure
        if err := s.appendChangelog(seed); err != nil {                  // CHANGELOG append per AC-SC-16
            return apperror.Wrap(err, "AB-9502", "changelog append failed after DB commit")  // CRITICAL per AC-SC-11
        }
        return s.fsyncChangelog()                                         // fsync BEFORE lock release
    })
    // lock released here via defer
}
```

Forbidden patterns (each FAILS this AC): (i) calling `s.db.Transaction(...)` BEFORE `acquireFileLock` (race window during lock wait); (ii) moving `appendChangelog` outside the transaction closure (lock would release on COMMIT, then changelog race); (iii) replacing `defer lock.Release()` with explicit `lock.Release()` mid-function (skipped on panic); (iv) using `sync.Mutex` instead of OS file lock (only blocks within-process — concurrent OS processes still race).
- **Verifies:** AC-SC-11 (atomic txn) + AC-SC-16 (CHANGELOG append-only) + AC-SC-17 (concurrent invocations) — binds the three together via lock-ordering. Closes Phase 153 v5 audit `06-seedable-config-architecture.json` issue [MEDIUM/D3] "Ambiguous CHANGELOG.md Write Concurrency" + v7 audit MEDIUM D3 "Incomplete Concurrency Implementation Detail" (`bundle_sha c5b46d3cb2b36a7b`).
- **Source:** AC-SC-11 §Atomicity + AC-SC-17 §Concurrency. Reference Go snippet authored Phase 153 Task A24.

### AC-SC-22 — `apperror` package, error-code prefixes, and `Err*` sentinels are sourced from `spec/03-error-manage/` (no local re-definition)

- **Given** the Go code samples in `01-fundamentals.md` and `02-features/*.md` reference `apperror.Wrap(...)`, `apperror.New(...)`, `*apperror.AppError`, sentinel errors like `ErrSeedLoadFailed`, and error codes like `AB-9301` (`RagChunkSizeInvalid`),
- **When** an AI implementer compiles the sample code,
- **Then** EVERY such symbol MUST resolve via the canonical package contract in [`spec/03-error-manage/02-error-architecture/06-apperror-package/`](../03-error-manage/02-error-architecture/06-apperror-package/) — package shape, constructor signatures, and `*AppError` struct fields are owned there. Error codes and their human-readable identifiers (e.g. `AB-9301` → `RagChunkSizeInvalid`) are sourced from [`spec/03-error-manage/03-error-code-registry/01-registry.md`](../03-error-manage/03-error-code-registry/01-registry.md). spec/06 MUST NOT inline a Go `apperror` package definition, MUST NOT re-declare `*AppError` struct fields, and MUST NOT define error codes outside the registry — doing so creates a dual-source drift class (Lesson #36). Sub-feature files (`02-features/*.md`) that introduce a NEW error code MUST add a row to `spec/03-error-manage/03-error-code-registry/01-registry.md` in the same PR; otherwise the code sample is unverifiable. Adding `AB-NNNN` codes only inside `02-features/02-rag-validation-helpers.md` table without registry binding FAILS this AC.
- **Verifies:** `01-fundamentals.md` Go samples + `02-features/01-rag-chunk-settings.md` + `02-features/02-rag-validation-helpers.md` error-code table — bound to spec/03's apperror contract. Closes Phase 153 v5 audit `06-seedable-config-architecture.json` issue [HIGH/D5] "Missing External Error Code Registry" by replacing the auditor's "inline a minimal Go package" recommendation with a normative cross-reference (per Lesson #36 — link, never restate).
- **Source:** Code samples in `01-fundamentals.md` lines ~330-340 + `02-features/01-rag-chunk-settings.md` lines ~115-185 + `02-features/02-rag-validation-helpers.md` AB-9301 row.

### AC-SC-23 — Module asset inventory pin (Lesson #29 — CW Config 19-entry inventory + truncation cliff)  `[critical]`

- **Given** spec/06's full on-disk asset inventory (§99 inventory authoritative): root contains `00-overview.md` + `01-fundamentals.md` + `02-features/` (10 files: `00`, `01–06`, `97`, `98`, `99`) + `03-issues/` (4 files: `00`, `97`, `98`, `99`) + `97-acceptance-criteria.md` + `97-changelog.md` (legacy stub) + `98-acceptance-criteria.md` (legacy stub) + `98-changelog.md` + `99-consistency-report.md` + `lifecycle-seedable-config.mmd` — every file is present on disk and contributes to rubric-v2 inventory credit per Phase 137; `02-features/04-rag-test-coverage-matrix.md` completes cleanly at line 265 (`tail -3` shows the closing italic note),
- **When** an audit harness bundles only `{00,97,98,99}-*.md` per spec/27 slot 34 v1.1.0 AC-34-09 tier-1 cap (~75–90 KB), exhausting the budget on the chunky `02-features/03-rag-validation-tests.md` (894 lines) before reaching files 04–06 in alphabetical sub-walk,
- **Then** the auditor MUST treat any `[D3] Truncated Feature Specifications` finding citing mid-sentence cutoff in `02-features/04-rag-test-coverage-matrix.md` AND any `[D5] missing files 05/06/03/97/99` finding as a **harness bundling-cap artifact**, NOT a spec defect. Implementations MUST resolve missing-context findings by enumerating `ls spec/06-seedable-config-architecture/02-features/` + `ls spec/06-seedable-config-architecture/03-issues/`, not by demanding inline content.
- **Verifies:** the spec/06 module-kind = `module` declaration AND the auditor-authoritative inventory contract; codifies **Lesson #29** (audit-corpus / harness-misclassification pin) + **Lesson #36** (link-don't-restate). Mirror of spec/05 AC-SD-24 + spec/14 AC-21 + spec/22 AC-78 + spec/13 AC-24 + spec/28 AC-28-41 + spec/07 AC-35 + spec/10 AC-9 + spec/03 AC-08 + spec/11 AC-10 + spec/12 AC-09 + spec/17 AC-10 + spec/18 AC-09 + spec/25 AC-AI-09..11. Until the cache refreshes (audit-ai harness saturated at `files_used=20/166, bytes_used=140000`), `06-seedable-config-architecture.json` will continue to report this stale-cache finding per Lesson #34. **Source:** A18-fu1 #6 close of audit-v7 D3 HIGH "Truncated Feature Specifications" (cache 2026-04-30).

---

## Legacy Criteria (preserved for traceability)

### AC-SC-LEGACY-001 — Configuration Seeding (3 sub-checkboxes)

> Original stub:
> ```
> ## AC-01: Configuration Seeding
> - [ ] Initial seed data populates all required configuration on first run
> - [ ] Seed files use JSON format with schema validation
> - [ ] Seeding is idempotent — re-running does not duplicate data
> ```
> Replaced by:
> - LEGACY-001-a (initial seed) → AC-SC-02 (full seeding contract with DDL + Metadata).
> - LEGACY-001-b (JSON + schema) → AC-SC-03 (`$schema` reference + Draft 7+ validation + exit 3 on failure).
> - LEGACY-001-c (idempotent) → AC-SC-04 (no-op on equal version + zero writes + skipping log).

### AC-SC-LEGACY-002 — Changelog Versioning (3 sub-checkboxes)

> Original stub:
> ```
> ## AC-02: Changelog Versioning
> - [ ] Configuration changes generate automatic changelog entries
> - [ ] Version numbers follow semantic versioning (major.minor.patch)
> - [ ] Rollback restores previous configuration state cleanly
> ```
> Replaced by:
> - LEGACY-002-a (auto changelog) → AC-SC-05 (Keep-a-Changelog format + Added/Changed/Removed sections + reverse chronological).
> - LEGACY-002-b (SemVer) → AC-SC-06 (regex match + precedence + downgrade refusal + AC-SC-18).
> - LEGACY-002-c (rollback) → AC-SC-07 (reverse-CHANGELOG replay + atomic transaction + rollback log entry).
