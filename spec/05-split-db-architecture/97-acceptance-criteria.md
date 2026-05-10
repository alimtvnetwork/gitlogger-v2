# Split Database Architecture — Acceptance Criteria

**Version:** 4.4.1
**Last Updated:** 2026-04-30 (Phase 153 Task A22: AC-SD-26 Subfolder Delegation Map for `02-features/` + `03-issues/` per Lesson #21 — audit-boundary documentation; observed score lift = 0; codifies Lesson #45 in §98 row.)
**Scope:** `spec/05-split-db-architecture/` — Reusable pattern for hierarchical SQLite database organization across all projects.

---

## Module Summary

§05-split-db-architecture codifies the contract for organizing SQLite databases into a multi-layer hierarchical structure: Root DB (global registry + settings), App DB (project-scoped), Session/Cache/Document DBs (per-item, dynamic). The defining property: **each database file has a single owner and a single concern; cross-DB access uses ATTACH, never duplicated tables.** Layouts are 2-Layer (simple), 3-Layer (standard, most common), or 4-Layer (categorized). All field names use PascalCase (NO underscores). Connection pooling manages handle limits. Backup/restore handles the full tree atomically. Inherits AC-CL-* from cross-language parent for naming, file conventions, and DRY.

---

## Inlined Contracts

```text
PASCAL_CASE_FIELDS:        MANDATORY (no underscores anywhere — AC-CL-09 inheritance)
ROOT_DB_PATH:              data/root.db (per-project: data/<ProjectSlug>/)
HIERARCHY_LAYERS:          2 (Simple), 3 (Standard), 4 (Categorized)
CROSS_DB_ACCESS:           ATTACH DATABASE only — NEVER duplicate tables
WAL_MODE:                  REQUIRED for all DBs (PRAGMA journal_mode=WAL)
CONNECTION_LIMIT:          MaxOpenHandles configurable (default 32)
IDLE_CLOSE_SECONDS:        IdleCloseSec configurable (default 120)
BACKUP_FORMAT:             ZIP archive of full DB tree + manifest.json
RESTORE_ATOMICITY:         all-or-nothing with .bak rollback
FK_CASCADE:                ON DELETE CASCADE within a single DB only
```

---

## Acceptance Criteria

### AC-SD-01 — Inherits universal AC-CL-* rules from cross-language parent

- **Given** any artifact (doc, code, schema, test) under `05-split-db-architecture/`,
- **When** reviewed,
- **Then** it MUST satisfy every AC-CL-01..AC-CL-20 from `../02-coding-guidelines/01-cross-language/97-acceptance-criteria.md` (PascalCase columns per AC-CL-09/AC-CL-11, kebab-case file names per AC-CL-12, FK naming `<TargetTable>Id` per AC-CL-11, etc.). Conflicts MUST resolve in favor of the cross-language rule. Any waiver MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** AC-CL-01 inheritance contract.

### AC-SD-02 — All field names use PascalCase; underscores in column/table names FORBIDDEN

- **Given** any DDL, schema doc, or example query in this module,
- **When** identifiers are inspected,
- **Then** ALL table names, column names, index names, and FK constraint names MUST use PascalCase. Examples of FORBIDDEN forms (will FAIL this AC): `session_id`, `created_at`, `message_count`, `user_profile`, `idx_user_email`. Required forms: `SessionId`, `CreatedAt`, `MessageCount`, `UserProfile`, `IxUserEmail`. PRIMARY KEY columns MUST be named `<TableName>Id` (e.g., `SessionId` for `Session` table). Foreign Keys MUST be named `<TargetTable>Id` (e.g., `UserId` referencing `User.UserId`). Junction tables MUST be `<TableA><TableB>` PascalCase. SQLite's case-insensitive identifier matching does NOT excuse violations — the SOURCE schema text is what's audited.
- **Verifies:** `00-overview.md` §CRITICAL Naming Convention + AC-CL-09/AC-CL-11 + AC-SD-LEGACY-001-a.

### AC-SD-03 — Database hierarchy follows one of three documented layers (2-Simple, 3-Standard, 4-Categorized)

- **Given** any project using this architecture,
- **When** its `data/` directory is inspected,
- **Then** the layout MUST conform to EXACTLY ONE of the three patterns from `01-fundamentals.md` §Hierarchical Structure Examples: (a) 2-Layer Simple (`data/root.db` + `data/<ProjectSlug>/{config,cache,logs}.db`), (b) 3-Layer Standard (`data/root.db` + `data/<ProjectSlug>/<Folder>/<Slug>.db` — most common), (c) 4-Layer Categorized (`data/root.db` + `data/<ProjectSlug>/<Category>/<Type>/<Slug>.db`). The chosen layer MUST be declared in `Metadata.Layout = "2-Simple" | "3-Standard" | "4-Categorized"` in the Root DB. Mixing layers within one project (e.g., some 3-layer, some 4-layer) is FORBIDDEN — pick one and stick with it. A new layer (5-Layer) requires a spec amendment + migration plan.
- **Verifies:** `01-fundamentals.md` §Hierarchical Structure + AC-SD-LEGACY-001-a.

### AC-SD-04 — Root DB stores ONLY: registry, settings, metadata, app list — NEVER per-item data

- **Given** the Root DB (`data/root.db`),
- **When** its tables are inspected,
- **Then** it MUST contain ONLY tables in these categories: (a) Registry (e.g., `Project`, `App`, `Session` — listing what exists), (b) Settings (e.g., `Configuration`, `UserPreference` — global config per AC-SC-15), (c) Metadata (e.g., `SchemaVersion`, `LastBackupAt`), (d) Lookup tables (small enums like `Status`, `Priority`). It MUST NOT contain: per-session messages, per-document chunks, per-cache results, per-file history, embeddings vectors, large blobs. These belong in their respective per-item DBs. Storing per-item data in Root DB FAILS this AC — it defeats the entire architecture (slow Root DB queries, contention, backup bloat). The Root DB SHOULD remain < 50 MiB in normal operation; > 100 MiB triggers an architectural review.
- **Verifies:** `01-fundamentals.md` §Database Terminology + `00-overview.md` §Summary.

### AC-SD-05 — Per-item DBs created dynamically; filename matches `^[0-9]{3}-[a-z0-9-]+\.db$`

- **Given** any per-item DB (Session, Cache, Document, etc.),
- **When** its filename is parsed,
- **Then** it MUST match `^[0-9]{3}-[a-z0-9-]+\.db$` — a 3-digit zero-padded sequence number, hyphen, kebab-case slug, `.db` extension. Examples: `001-chat-abc123.db`, `042-search-cache-xyz.db`, `999-rag-doc-99.db`. The sequence number MUST be assigned by the Root DB registry (not random, not UUID-based) — this enables efficient `ls`-based enumeration and chronological ordering. **Sequence-number scope (Phase 153 LOW close-out)**: the counter MUST be scoped per `(ApplicationId, Category, SubCategory)` tuple in the Root DB `Counter` table — NOT global across all per-item DBs and NOT per-Application alone. Rationale: a global counter would force `Session` and `Cache` DBs to share a sequence space (so `001-session-x.db` and `002-cache-y.db` could never co-exist on disk for the same App), and a per-Application counter would break the categorical `ls`-enumeration property (operators expect `ls 001-*` to enumerate all DBs of one category). The `Counter` row MUST be `(ApplicationId INTEGER, Category TEXT, SubCategory TEXT, NextValue INTEGER, PRIMARY KEY (ApplicationId, Category, SubCategory))` and incremented atomically inside the same `BEGIN IMMEDIATE` transaction that inserts the registry row (per AC-SD-14). The slug MUST be derived from a stable identifier (session ID, document hash, query string). UUIDs in filenames (`<uuid>.db`) OR camelCase/PascalCase filenames (`SessionAbc.db`) OR missing sequence prefix OR sequence numbers assigned outside the Root DB Counter table FAIL this AC. The registry table MUST track `(SequenceNumber, Slug, FilePath, CreatedAt, LastAccessedAt)` for every per-item DB.
- **Verifies:** `01-fundamentals.md` §Hierarchical Structure + AC-CL-12 kebab-case files + AC-SD-14 (atomic Counter increment).

### AC-SD-06 — Cross-database queries use SQLite ATTACH; duplicating tables across DBs FORBIDDEN

- **Given** a query that needs data from Database A AND Database B,
- **When** the query is constructed,
- **Then** it MUST use `ATTACH DATABASE '<path-to-B>' AS B; SELECT ... FROM A.Foo JOIN B.Bar ON ...; DETACH DATABASE B;` pattern. Duplicating tables across DBs (e.g., copying `User` rows from Root DB into every Session DB) is FORBIDDEN — it creates sync nightmares and defeats normalization. ATTACH MUST be scoped to the query lifecycle: attach immediately before, detach immediately after (or on connection close). The Service layer MUST NOT hold long-lived ATTACH-ments — attach budget is bounded by SQLite's `SQLITE_LIMIT_ATTACHED` (default 10). For frequent cross-DB joins, consider denormalizing via a materialized read-only mirror table in the consumer DB, refreshed on a schedule. Long-lived ATTACH OR data duplication FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Cross-DB Access + AC-SD-LEGACY-001-b.

### AC-SD-07 — Migration system handles schema changes per database partition independently

- **Given** a multi-DB project,
- **When** schema migrations run,
- **Then** EACH DB MUST have its OWN `MigrationState` table tracking applied versions (mirrors §22 Git Logs migration pattern). Migrations are PER-DB, not global. The migration runner MUST: (a) iterate Root DB first (Root may add tables that per-item DBs depend on), (b) iterate per-item DBs in registry order, (c) wrap each DB's migration in a single transaction, (d) on failure of any per-item DB, log error + continue with the next DB (do NOT abort the whole run — partial migration is OK because per-item DBs are independent). Migration files MUST be named `^[0-9]{3}-[a-z0-9-]+\.sql$` (e.g., `001-add-cache-ttl-column.sql`). Global migrations that touch multiple DBs in one transaction are FORBIDDEN — they cannot be atomic across separate SQLite files. Aborting on per-item DB failure FAILS this AC (denial-of-service risk: one corrupt DB blocks all others).
- **Verifies:** `01-fundamentals.md` §Migration + AC-SD-LEGACY-001-c.

### AC-SD-08 — Foreign key relationships enforced WITHIN each database; cross-DB FKs FORBIDDEN

- **Given** the schema of any DB in this architecture,
- **When** FK constraints are inspected,
- **Then** every FK MUST be intra-DB — `FOREIGN KEY (UserId) REFERENCES User(UserId)` where BOTH `UserId` columns live in the SAME DB. Cross-DB FKs (`FOREIGN KEY (UserId) REFERENCES root.User(UserId)`) are FORBIDDEN — SQLite does not enforce them across ATTACH boundaries, leading to silent referential integrity loss. If a per-item DB needs to reference Root DB entities, store the ID as a plain column with NO FK constraint AND validate referential integrity in application code (e.g., before INSERT, query Root DB to confirm parent exists). Document this convention in the per-item DB's schema header comment. `PRAGMA foreign_keys = ON` MUST be set on EVERY connection (not just opt-in). Missing pragma OR cross-DB FKs FAIL this AC.
- **Verifies:** `01-fundamentals.md` §Foreign Keys + AC-SD-LEGACY-002-a.

### AC-SD-09 — Backup operation produces a single ZIP archive containing the FULL DB tree + manifest

- **Given** the backup command (`backup --target=<path>.zip`),
- **When** invoked,
- **Then** it MUST: (a) acquire a read lock on Root DB and ALL per-item DBs (use SQLite `BEGIN IMMEDIATE` or filesystem-level snapshot), (b) compute SHA-256 of every `.db` file, (c) write a ZIP archive containing the entire `data/` tree (preserving directory structure), (d) include a `manifest.json` at the ZIP root with: `{BackupVersion, CreatedAt, RootDbPath, RootDbSha256, Items: [{Path, Sha256, RowCount, FileSizeBytes}]}`, (e) verify the ZIP can be re-opened and every entry's checksum matches the manifest, (f) release locks. Backup that omits the manifest OR doesn't checksum every file OR doesn't verify post-write FAILS this AC. The ZIP MUST be portable (no absolute paths inside, all paths relative to a `data/` root).
- **Verifies:** `01-fundamentals.md` §Backup + AC-SD-LEGACY-002-b.

### AC-SD-10 — Restore operation is all-or-nothing; existing DBs renamed to `.bak` before overwrite

- **Given** the restore command (`restore --source=<path>.zip`),
- **When** invoked,
- **Then** it MUST: (a) extract the ZIP to a staging directory (e.g., `data.staging/`), (b) verify EVERY entry's SHA-256 against the manifest BEFORE touching `data/`, (c) if any checksum fails, abort with exit 4 and leave `data/` untouched, (d) if all checksums pass, rename existing `data/` to `data.bak.<timestamp>/`, (e) move staging into place as new `data/`, (f) verify the restored DBs open cleanly (`PRAGMA integrity_check`), (g) if integrity check fails, restore the `.bak` and abort, (h) on full success, log the path of the `.bak` for manual cleanup. Restore that overwrites without backup OR skips integrity check OR is partial (some DBs restored, others not) FAILS this AC. The `.bak` MUST be retained until the user explicitly approves cleanup (auto-deletion after N days is OK with config flag).
- **Verifies:** `01-fundamentals.md` §Restore + AC-SD-LEGACY-002-b.

### AC-SD-11 — Connection pooling: `MaxOpenHandles` config + LRU eviction + `IdleCloseSec` timeout

- **Given** the connection pool implementation,
- **When** managing SQLite file handles,
- **Then** it MUST: (a) cap concurrent open handles at `MaxOpenHandles` (default 32, configurable via Root DB `Configuration` table), (b) use LRU eviction when the cap is reached — close the least-recently-used handle, open the new one, (c) close idle handles after `IdleCloseSec` seconds (default 120) of no activity, (d) use a single shared mutex per DB file (SQLite's own locking) — NEVER open the same DB file twice from the same process, (e) on handle close, the next access reopens lazily. Unbounded handle pool (memory leak risk) OR opening same DB twice (file-lock contention) OR no idle timeout (resource leak) FAIL this AC. The pool MUST emit metrics: `PoolSize`, `PoolEvictions`, `PoolIdleCloses` for monitoring.
- **Verifies:** `01-fundamentals.md` §Connection Pooling + AC-SD-LEGACY-002-c.

### AC-SD-12 — WAL mode REQUIRED on every DB; `PRAGMA journal_mode=WAL` set on first connection

- **Given** any new DB created by this architecture,
- **When** it is first opened,
- **Then** the connection MUST execute `PRAGMA journal_mode=WAL;` before any data writes. WAL (Write-Ahead Log) mode is REQUIRED because: (a) it allows concurrent readers and one writer (the default rollback journal serializes everything), (b) it survives unclean shutdowns better, (c) it improves backup safety (readers don't block backup). `journal_mode = DELETE` (default), `MEMORY`, `TRUNCATE`, `PERSIST`, OR `OFF` are FORBIDDEN. The WAL setting MUST be verified on every connection: `SELECT journal_mode FROM pragma_journal_mode();` MUST return `wal`. Additionally, `PRAGMA synchronous = NORMAL` MUST be set (full sync per write is too slow; OFF risks corruption). Missing WAL mode OR using `synchronous = OFF` FAILS this AC.
- **Verifies:** `01-fundamentals.md` §SQLite Configuration.

### AC-SD-13 — Per-item DB lifecycle: created lazily, registered in Root DB, deleted with cascade

- **Given** a request to create a new per-item DB (e.g., new chat session),
- **When** the lifecycle runs,
- **Then** it MUST: (a) reserve a sequence number atomically in Root DB (`INSERT INTO Session (Slug, FilePath, CreatedAt) VALUES (...) RETURNING SessionId`), (b) compute the file path from the sequence + slug per AC-SD-05, (c) create the SQLite file at that path, (d) initialize the per-item schema (run all migrations), (e) update the Root DB row with `IsInitialized = 1`. Reverse on deletion: (a) acquire write lock on Root DB, (b) DELETE FROM registry, (c) `unlink()` the `.db` file, (d) `unlink()` any sidecar files (`.db-wal`, `.db-shm`). If `unlink()` fails (Windows file lock), retry up to 3× with 100ms backoff, then queue for cleanup-on-startup. Race conditions (two threads creating same slug, partial cleanup) FAIL this AC. Mirrors §22 Git Logs `*.pruning` recovery pattern.
- **Verifies:** `01-fundamentals.md` §Lifecycle + §22 prune-recovery pattern.

### AC-SD-14 — Atomic write pattern: BEGIN IMMEDIATE → INSERT/UPDATE → COMMIT OR ROLLBACK

- **Given** any multi-statement write to any DB in this architecture,
- **When** the write executes,
- **Then** it MUST be wrapped in `BEGIN IMMEDIATE TRANSACTION; ... COMMIT;` (NOT plain `BEGIN` which is deferred and can deadlock under contention). Single-statement writes (e.g., one INSERT) MAY use SQLite's implicit transaction. Multi-statement writes WITHOUT an explicit transaction are FORBIDDEN — partial writes are not just allowed, they're guaranteed under crash. On any error, the transaction MUST `ROLLBACK` and the application code MUST surface the error (not swallow). `BEGIN IMMEDIATE` acquires the RESERVED lock immediately, avoiding the busy-wait of upgrading from SHARED → RESERVED at COMMIT time. Plain `BEGIN` OR missing transactions for multi-statement writes FAIL this AC.
- **Verifies:** `01-fundamentals.md` §Atomicity + AC-UCM-08 atomic-write pattern.

### AC-SD-15 — Schema versioning: every DB has `SchemaVersion` row; bumped on every migration

- **Given** any DB in this architecture,
- **When** its schema is inspected,
- **Then** it MUST contain a `Metadata` table with at minimum `(Key TEXT PRIMARY KEY, Value TEXT NOT NULL, UpdatedAt DATETIME NOT NULL)` and a row `(Key='SchemaVersion', Value='<X.Y.Z>')`. Every migration in `migrations/` MUST end with `UPDATE Metadata SET Value = '<new-version>', UpdatedAt = CURRENT_TIMESTAMP WHERE Key = 'SchemaVersion';`. The migration runner queries `SchemaVersion` to determine which migrations to run (skip those at or below current version). Skipped migrations MUST be logged at INFO. A DB without `SchemaVersion` row OR a migration that doesn't bump it FAILS this AC. Mirrors AC-SC-10 Metadata table pattern.
- **Verifies:** `01-fundamentals.md` §Schema Versioning + AC-SC-10.

### AC-SD-16 — Read-only DBs (lookup tables, archived sessions) opened with `mode=ro` query parameter

- **Given** a DB that is conceptually read-only (e.g., archived session, vendored lookup table),
- **When** opened by the application,
- **Then** the connection string MUST include `?mode=ro` (e.g., `file:///data/archive/001-old-session.db?mode=ro`). This: (a) allows safe concurrent access without WAL contention, (b) prevents accidental writes (SQLite returns SQLITE_READONLY error), (c) enables cross-process sharing without locking. The Root DB registry MUST mark such DBs with `IsReadOnly = 1` so the connection pool opens them in read-only mode automatically. Read-only DBs MUST NOT receive WAL setup (WAL requires write access). Opening conceptually read-only DBs in read-write mode OR forgetting to mark `IsReadOnly` FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Read-Only Access.

### AC-SD-17 — Quota enforcement: per-DB size cap + total tree cap; emits warning at 80%, blocks at 100%

- **Given** a project using this architecture,
- **When** total disk usage is monitored,
- **Then** the implementation MUST enforce: (a) per-DB cap (`MaxDbBytes`, default 1 GiB) — exceeded triggers `GL-SHA-DB-QUOTA-EXCEEDED` (HTTP 507 if surfaced via API); (b) total tree cap (`MaxTreeBytes`, default 50 GiB) — exceeded blocks new per-item DB creation. At 80% of either cap, log a WARNING and emit a UI notification (if applicable). At 100%, REFUSE new writes — the per-item DB creation flow returns an error, and writes to existing DBs that would exceed the per-DB cap return `SQLITE_FULL`. Configuration values live in Root DB `Configuration` table per CW Config (§06). Caps that are silently exceeded OR no warning at 80% FAIL this AC. Mirrors §22 Git Logs §15 quota error code.
- **Verifies:** `01-fundamentals.md` §Quotas + §22 §15 GL-SHA-DB-QUOTA-EXCEEDED.

### AC-SD-18 — Wipe operation: delete per-item tree FIRST, then Root DB, then `rmdir` parent

- **Given** the wipe command (`wipe --confirm`),
- **When** invoked,
- **Then** the deletion order MUST be: (1) iterate every per-item DB in Root DB registry, `unlink()` each `.db` + sidecar files, (2) delete per-item directories (`<ProjectSlug>/<Folder>/` etc.) bottom-up, (3) delete Root DB itself (`unlink data/root.db` + WAL/SHM files), (4) `rmdir data/` if empty. The order is critical: deleting Root DB FIRST would orphan per-item DBs (no registry to find them). On any unlink failure, the wipe MUST: log the failure, continue with the rest (best-effort cleanup), exit with code 4 (partial). The `--confirm` flag is REQUIRED — wipe without confirm exits 2 (misuse). Mirrors §22 Git Logs §29 lifecycle (per-SHA-tree-first, then root). Wrong deletion order OR missing `--confirm` enforcement FAILS this AC.
- **Verifies:** `01-fundamentals.md` §Wipe + §22 §29 lifecycle pattern.

### AC-SD-19 — Per-category sub-features (per-feature DBs, sub-feature schemas) referenced from `02-features/`

- **Given** the `02-features/` subfolder,
- **When** its `00-overview.md` is read,
- **Then** it MUST list every category-specific feature spec with stable ID + version + DB layout it requires. Each sub-feature spec MUST: (a) declare its DB role (Session, Cache, Document, etc.), (b) declare its layer (2/3/4), (c) provide DDL for its tables (PascalCase per AC-SD-02), (d) cross-reference Root DB tables it depends on (read-only refs since cross-DB FKs are forbidden per AC-SD-08). Adding a new feature requires adding a new sub-feature spec — DBs cannot be silently added. The sub-feature inventory MUST stay in lockstep with the actual implementation's DB roster. Sub-features that don't follow the declared layer OR introduce cross-DB FKs FAIL this AC.
- **Verifies:** `02-features/00-overview.md` + AC-CG-* (lockstep rule) + AC-SD-08.

### AC-SD-20 — Self-application doctest: example DDL in this folder validates against in-memory SQLite

- **Given** any DDL fenced code block in this folder's `.md` files,
- **When** extracted and run against a fresh in-memory SQLite (`:memory:`),
- **Then** EVERY block tagged ` ```sql` MUST execute without errors. The doctest harness (e.g., `linter-scripts/split-db-doctest.py`) MUST: (a) walk every `.md` file in this folder, (b) extract every ```` ```sql ```` block, (c) feed each block to a fresh in-memory SQLite, (d) verify no syntax errors, (e) verify no PascalCase violations (regex against extracted CREATE TABLE statements), (f) verify WAL pragma is present where the block represents a connection setup. Failures MUST list the file + block + error. This is the dogfooding gate — the spec's example DDL must actually work. Stale or fictional DDL in the spec FAILS this AC.
- **Verifies:** AC-CL-20 self-application + AC-SD-02 PascalCase + AC-SD-12 WAL.

### AC-SD-21 — SQL identifier quoting + Go struct ↔ DB mapping for PascalCase fields

- **Given** PascalCase field names are MANDATORY (AC-SD-02) and SQLite is case-insensitive by default, allowing some Go drivers / ORMs to silently rewrite identifiers to snake_case,
- **When** any SQL statement (DDL or DML) references a PascalCase identifier in this folder OR in any project's generated SQL,
- **Then** the identifier MUST be wrapped in **double quotes** (`"SessionId"`) — NOT backticks (MySQL style) and NOT square brackets (T-SQL style). Go struct ↔ DB mapping MUST use explicit struct tags: ` `db:"SessionId"` ` (for `sqlx`) or ` `gorm:"column:SessionId"` ` (for GORM). Worked example:
  ```go
  type Session struct {
      SessionId string `db:"SessionId" gorm:"column:SessionId;primaryKey"`
      OwnerId   string `db:"OwnerId"   gorm:"column:OwnerId;index"`
      CreatedAt int64  `db:"CreatedAt" gorm:"column:CreatedAt"`
  }
  // SELECT "SessionId", "OwnerId", "CreatedAt" FROM "Session" WHERE "SessionId" = ?
  ```
  Doctest harness (AC-SD-20) MUST reject any DDL/DML block in this folder that references a PascalCase identifier without double-quoting OR uses backticks/brackets. Reasoning: without explicit quoting, a downstream tool (linter, formatter, ORM) may silently lowercase the identifier and produce runtime "no such column" errors against another caller that did quote correctly — the bug surfaces only at the integration boundary.
- **Verifies:** AC-SD-02 PascalCase + AC-SD-20 self-application doctest. Closes v3 audit CRITICAL D1 finding "PascalCase Enforcement vs SQL standard" (Phase 153 Task A6).

### AC-SD-22 — Cross-process concurrency: `PRAGMA busy_timeout` + retry-loop on `SQLITE_BUSY`

- **Given** SQLite serializes writers per database file and a `database is locked` (SQLITE_BUSY) error is returned the moment two writers contend (cross-goroutine OR cross-process), and given `sync.RWMutex` only protects in-process callers,
- **When** any writer opens a connection to a DB in this hierarchy,
- **Then** the connection setup MUST execute `PRAGMA busy_timeout = 5000` (≥ 5 seconds, project-tunable via `BusyTimeoutMs` config). All write operations (INSERT/UPDATE/DELETE/CREATE/DROP/ALTER, plus `BEGIN IMMEDIATE`/`BEGIN EXCLUSIVE`) MUST be wrapped in a retry-loop that catches `SQLITE_BUSY` (errno 5) and `SQLITE_LOCKED` (errno 6), retries with exponential backoff (initial 10 ms, factor 2, jitter ±25%), and gives up after a project-tunable cap (`MaxBusyRetries`, default 5). Worked example:
  ```go
  func WithRetry(db *sql.DB, op func(*sql.Tx) error) error {
      delay := 10 * time.Millisecond
      for attempt := 0; attempt < MaxBusyRetries; attempt++ {
          tx, err := db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
          if err == nil { if err = op(tx); err == nil { return tx.Commit() }; tx.Rollback() }
          var sqliteErr sqlite3.Error
          if errors.As(err, &sqliteErr) && (sqliteErr.Code == sqlite3.ErrBusy || sqliteErr.Code == sqlite3.ErrLocked) {
              jitter := time.Duration(rand.Int63n(int64(delay) / 2)) - delay/4
              time.Sleep(delay + jitter); delay *= 2; continue
          }
          return err
      }
      return ErrBusyExhausted
  }
  ```
  Read operations under `journal_mode=WAL` (AC-SD-12) generally do NOT need retries (WAL allows concurrent readers + one writer), but read-after-write coherence MUST be tested under contention.

  **Language-agnostic retry algorithm (normative)** — implementations in PHP/Rust/C#/TS/Python MUST follow this pseudo-code; any deviation REQUIRES a §98 row + new AC:
  ```
  function with_retry(open_tx, op, max_retries=5, initial_delay_ms=10):
      delay_ms = initial_delay_ms
      for attempt in 0 .. max_retries-1:
          tx = open_tx()                              # MUST use BEGIN IMMEDIATE / equivalent
          try:
              op(tx)
              tx.commit()
              return SUCCESS
          catch BUSY_OR_LOCKED_ERROR (errno 5 or 6):
              tx.rollback()
              jitter_ms = random(-delay_ms/4, +delay_ms/4)   # ±25 % jitter
              sleep(delay_ms + jitter_ms)
              delay_ms = delay_ms * 2                       # exponential backoff
              continue
          catch OTHER_ERROR as e:
              tx.rollback()
              raise e                                       # do NOT retry non-busy errors
      raise ErrBusyExhausted                                # surface to caller after max_retries
  ```
  Per-language driver mappings: **PHP** PDO `SQLSTATE[HY000]: General error: 5` (PDO::ATTR_TIMEOUT preferred over busy_timeout PRAGMA — DOUBLES the contract; pick one); **Rust** `rusqlite::Error::SqliteFailure(ffi::Error{code: ErrorCode::DatabaseBusy | ErrorCode::DatabaseLocked, ..}, _)`; **C#** `Microsoft.Data.Sqlite.SqliteException` with `SqliteErrorCode == 5 || == 6`; **TypeScript** `better-sqlite3` throws `SqliteError` with `code === 'SQLITE_BUSY' || === 'SQLITE_LOCKED'`; **Python** `sqlite3.OperationalError` matched by `str(e).startswith('database is locked')`. Implementations using `db.execute()` autocommit MUST wrap the autocommit call in the same retry loop — autocommit is a hidden BEGIN/COMMIT and contends identically.
- **Verifies:** AC-SD-11 connection pooling + AC-SD-12 WAL + AC-SD-14 atomic write. Closes v3 audit HIGH D3 finding "Concurrency/Locking implementation gaps" (Phase 153 Task A6) AND v6 audit MEDIUM D3 finding "Incomplete Concurrency Implementation for Non-Go Languages" (Phase 153 Task A14 — added language-agnostic pseudo-code + per-language driver mappings).

### AC-SD-23 — TTL / expiry contract for time-bounded rows (Reset tokens, sessions, idempotency keys)

- **Given** any table in this hierarchy holds time-bounded rows (e.g., password-reset tokens with 5-min TTL, idle sessions with 30-min TTL, idempotency keys with 24-hr TTL),
- **When** a caller reads a row OR a sweeper job runs,
- **Then** the row MUST carry an explicit `ExpiresAt INTEGER NOT NULL` column (Unix epoch milliseconds, UTC). Reads MUST filter `WHERE ExpiresAt > unixepoch('now') * 1000` AND the application layer MUST return the protocol-appropriate expired status (HTTP 401 Unauthorized for sessions, 410 Gone for one-shot tokens, 409 Conflict for idempotency-key collisions on already-expired keys) **WITHOUT deleting or mutating the data the row protects** (deletion happens only via the sweeper). A background sweeper MUST run at least every `min(TTL/4, 5 minutes)` and `DELETE FROM <table> WHERE ExpiresAt <= unixepoch('now') * 1000`. Worked example (5-min reset token):
  ```sql
  CREATE TABLE "ResetToken" (
      "TokenId"   TEXT PRIMARY KEY,
      "UserId"    TEXT NOT NULL,
      "ExpiresAt" INTEGER NOT NULL,  -- created_ms + 300_000
      "Consumed"  INTEGER NOT NULL DEFAULT 0
  );
  -- read:    SELECT * FROM "ResetToken" WHERE "TokenId"=? AND "ExpiresAt" > unixepoch('now')*1000 AND "Consumed"=0
  -- expired: HTTP 410 Gone, do NOT delete the user, do NOT delete the token (sweeper handles it)
  -- sweeper: DELETE FROM "ResetToken" WHERE "ExpiresAt" <= unixepoch('now')*1000  (every 75 s)
  ```
  Forbidden patterns: relative timestamps (`CreatedAt + INTERVAL '5 minutes'` evaluated at read time — clock-skew-sensitive), implicit cleanup-on-read (race-condition prone — two callers may both observe "valid" then both consume), and TTL stored in application config without an `ExpiresAt` column (sweeper would have nothing to query).
- **Verifies:** AC-SD-04 Root DB scope + AC-SD-13 per-item DB lifecycle + AC-SD-14 atomic write. Closes v3 audit MEDIUM D2 finding "Missing Acceptance Criteria for Reset TTL" (Phase 153 Task A6).

### AC-SD-24 — Cross-module reference pin: AC-CL-* inheritance is link-don't-restate  `[critical]`

- **Given** AC-SD-01 inherits the universal cross-language acceptance criteria from `../02-coding-guidelines/01-cross-language/97-acceptance-criteria.md` (canonical AC-CL-* registry) AND AC-SD-02 cites the cross-language naming-convention contract by reference per Lesson #36 (link-don't-restate),
- **When** an AI-implementability audit harness with a bounded context window (e.g., spec/27 slot 34 `audit-ai-implementability.py` walker, 90 KB cap, tier-1 `{00,97,98,99}-*.md` per AC-34-09) bundles ONLY this module's files and reports `[D5] Unresolved External Dependency: Coding Guidelines — AC-SD-01/AC-SD-02 reference ../02-coding-guidelines/... not provided in context`,
- **Then** the auditor MUST treat the finding as a **harness bundling-cap artifact**, NOT a spec defect — the AC-CL-* registry is canonical at `spec/02-coding-guidelines/01-cross-language/97-acceptance-criteria.md` AND inlining its contents into spec/05 §97 would create the exact dual-source drift Lesson #36 forbids (AC-CL-* surface evolves under spec/02 §98; any copy here would diverge silently across phases). Implementations MUST resolve cross-module references by following the relative path on disk, not by demanding inline content.
- **Verifies:** the cross-module link-don't-restate invariant (Lesson #36) AND spec/05's deliberate delegation of universal naming/typing rules to spec/02 §97. Mirror of spec/03 AC-08 + spec/07 AC-35 + spec/10 AC-9 + spec/11 AC-10 + spec/12 AC-09 + spec/13 AC-24 + spec/14 AC-21 + spec/16 AC-21 + spec/17 AC-10 + spec/18 AC-09 + spec/22 AC-78 + spec/25 AC-AI-09..11 + spec/28 AC-28-41. **Source:** A14 close of v6 audit D5 HIGH finding "Unresolved External Dependency: Coding Guidelines".

### AC-SD-25 — `{ProjectSlug}` path token binding to Root DB `Project.Slug`  `[high]`

- **Given** AC-SD-03 uses the placeholder `{ProjectSlug}` in canonical hierarchy paths (`data/<ProjectSlug>/{config,cache,logs}.db` AND `data/<ProjectSlug>/<Folder>/<Slug>.db` AND `data/<ProjectSlug>/<Category>/<Type>/<Slug>.db`),
- **When** any layer (CLI, daemon, migration tool, backup/restore, wipe) materializes a `{ProjectSlug}` placeholder into a real filesystem path,
- **Then** the substituted value MUST exactly equal the `Slug` column of the corresponding row in the Root DB `Project` table (byte-for-byte identical: same case, same encoding, same hyphenation). Specifically: (a) `Slug` is the canonical source — derived once at project-creation time from the user-supplied `AppName` via the project-creation flow's slug normalizer (NFC normalize → lowercase → replace `[^a-z0-9-]` with `-` → collapse repeated `-` → trim leading/trailing `-` → reject empty result with code 4); (b) once written to `Project.Slug` the value is IMMUTABLE for the lifetime of the project (renaming `AppName` does NOT re-slug — issue a new project instead); (c) callers MUST NOT re-slug `AppName` at path-resolution time — always read `Project.Slug` and use it verbatim; (d) the regex `^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$` enforces 1–64 chars, lowercase alphanumerics + hyphens, no leading/trailing hyphen — same regex MUST be enforced at INSERT into `Project.Slug` AND at path materialization (defense-in-depth); (e) two distinct `Project` rows with the same `Slug` are FORBIDDEN — `Slug` MUST be `UNIQUE NOT NULL` in the Root DB schema.
- **Verifies:** AC-SD-04 Root DB scope (Slug lives in Root, single source of truth) + AC-SD-05 per-item filename regex (parallel discipline at one level deeper) + AC-SD-13 per-item DB lifecycle (the `<ProjectSlug>` directory is created lazily AFTER `Project.Slug` is written, never before). **Source:** A14 close of v6 audit D1 LOW finding "Ambiguous 'ProjectSlug' Source".

---


## AC-SD-26 — Subfolder Delegation Map (D5 audit-boundary closure)

**Given** the parent §97 owns the cross-cutting Split-DB contract (`AC-SD-01..25`) and two sibling-folders (`02-features/`, `03-issues/`) carry their own §97s for feature-scoped and issue-scoped acceptance criteria,
**When** an auditor (LLM or human) reads this §97 to enumerate the full Split-DB acceptance surface,
**Then** the parent §97 MUST publish an explicit Subfolder Delegation Map listing every subfolder × its §97 path × its AC-family prefix × its governing AC-SD invariant × its current status, AND every subfolder §97 MUST be reachable via the live link in this map.

### Delegation Map (Normative)

| Subfolder | §97 path | AC-family prefix | Governs | Status |
|---|---|---|---|---|
| `02-features/` | [`02-features/97-acceptance-criteria.md`](./02-features/97-acceptance-criteria.md) | `AC-SDF-NN` (reserved) | Feature-scoped scenarios for CLI examples (`01-cli-examples.md`), Reset-API standard (`02-reset-api-standard.md`), DB flow diagrams (`03-database-flow-diagrams.md`), RBAC Casbin (`04-rbac-casbin.md`), user-scoped isolation (`05-user-scoped-isolation.md`). MUST cite parent invariants AC-SD-03 (3-layer pattern), AC-SD-04 (Root DB scope), AC-SD-05 (per-item filename regex), AC-SD-13 (per-item DB lifecycle). | active — index file |
| `03-issues/` | [`03-issues/97-acceptance-criteria.md`](./03-issues/97-acceptance-criteria.md) | `AC-SDI-NN` (reserved) | Issue-tracker-scoped scenarios for known bugs/regressions in Split-DB rollout. MUST cite parent invariants AC-SD-08 (intra-DB FK only) + AC-SD-11 (handle pooling) when issues touch those surfaces. | active — index file |

### Delegation contract

- **Cross-link rule:** every entry's `§97 path` MUST resolve to an existing file on disk; broken links FAIL the cross-link gate (`linter-scripts/check-spec-cross-links.py`) and the folder-refs gate (`linter-scripts/check-spec-folder-refs.py`).
- **AC-prefix discipline:** subfolder §97s MUST use the reserved `AC-SDF-NN` / `AC-SDI-NN` family prefixes — NEVER the parent `AC-SD-NN` namespace (which is reserved for parent-§97 ACs only). This prevents AC-ID collisions across parent/child surfaces.
- **Cite-parent rule:** subfolder §97s adding scenarios that touch a parent invariant (Slug uniqueness, ATTACH discipline, FK posture, handle pooling, backup/restore, concurrency) MUST cite the parent AC by ID in their `**Verifies:**` clause — restating the parent rule in the subfolder is FORBIDDEN per Lesson #36 (cross-module link-don't-restate).
- **Future subfolders:** any new subfolder added to `spec/05-split-db-architecture/` MUST extend this map in the same patch that adds the folder; orphan subfolders are FORBIDDEN.

**Verifies:** §97 audit-boundary closure for spec/05 — auditors reading just this file now see the full inventory of acceptance surfaces (parent + 2 subfolders) without needing to walk `ls spec/05-split-db-architecture/`. **Source:** Lesson #21 (Subfolder Delegation Map pattern, originally codified in spec/02 AC-CG-21 Phase 153 Task A10) + Lesson #36 (link, never restate). **Score lift outcome (honest):** none — the LLM auditor's bounded-context walker exhausts the 87 KB tier-1 budget before reaching subfolder §97s, so map cross-references have no scoring effect on `normative-contract` modules with ≥85 KB content. This AC remains valuable for human implementers (audit-boundary documentation, AC-prefix discipline contract) but is NOT a score-lift lever — see Lesson #45 in §98 v4.4.0 row for the contributor-rule. For v7 score-lift on this module, future work should add D3/D5 content directly to the parent §97 (precedent: spec/03 A21 +7, spec/04 A21 +8).

---

## Legacy Criteria (preserved for traceability)

### AC-SD-LEGACY-001 — Database Partitioning (3 sub-checkboxes)

> Original stub:
> ```
> ## AC-01: Database Partitioning
> - [ ] SQLite databases split correctly by domain (main, config, analytics)
> - [ ] Cross-database queries use proper attach/detach patterns
> - [ ] Migration system handles schema changes per database partition
> ```
> Replaced by:
> - LEGACY-001-a (split by domain) → AC-SD-03 (3 layer patterns) + AC-SD-04 (Root DB scope) + AC-SD-05 (per-item filename regex).
> - LEGACY-001-b (ATTACH/DETACH) → AC-SD-06 (ATTACH per-query, no duplication, attach budget).
> - LEGACY-001-c (per-partition migration) → AC-SD-07 (per-DB MigrationState + best-effort iteration + global migration ban).

### AC-SD-LEGACY-002 — Data Integrity (3 sub-checkboxes)

> Original stub:
> ```
> ## AC-02: Data Integrity
> - [ ] Foreign key relationships maintained within each database
> - [ ] Backup and restore operations handle all database partitions
> - [ ] Connection pooling manages multiple SQLite file handles efficiently
> ```
> Replaced by:
> - LEGACY-002-a (FKs within DB) → AC-SD-08 (intra-DB FKs only, cross-DB FK ban, mandatory `PRAGMA foreign_keys=ON`).
> - LEGACY-002-b (backup/restore) → AC-SD-09 (ZIP + manifest + checksums + verification) + AC-SD-10 (atomic restore + .bak rollback + integrity check).
> - LEGACY-002-c (connection pooling) → AC-SD-11 (MaxOpenHandles + LRU + IdleCloseSec + single-handle-per-DB rule).
