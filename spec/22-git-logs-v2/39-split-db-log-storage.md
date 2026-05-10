# Split-DB Log Storage (per-SHA SQLite files)

**Version:** 1.0.0  
**Created:** 2026-04-26  
**Status:** Active (introduced in v3.8.0)  
**Pattern source:** [`../05-split-db-architecture/00-overview.md`](../05-split-db-architecture/00-overview.md)

---

## Why split

The root DB (`wp-content/uploads/git-logs/git-logs.sqlite`) is shared across **every** GitProfile / Repo / RepoVersion in the install. If we kept every CI log line there, the file would grow unbounded, vacuums would block the admin UI, and a corrupt single file would lose every customer's history.

Per the [Split-DB Architecture](../05-split-db-architecture/00-overview.md) pattern:

- **Root DB** = registry + control plane (small, hot, always-open).
- **Per-SHA child DB** = bulk log data for one Git commit SHA on one RepoVersion (large, cold, opened lazily).

The plugin's own internal logger (Trace/Debug/Info/Warn/Error/Fatal — the *plugin's* operational logs, see §06) **stays in the root DB**. Only **GitHub-pushed CI logs** are split out per SHA.

---

## Filesystem layout

```
wp-content/uploads/git-logs/
├── git-logs.sqlite                       ← root DB (Profile, GitProfile, Repo, RepoVersion, Pipeline, ShaRegistry, History, PipelineAction, SystemEvent, AuditTrail, …)
└── logs/
    └── <RepoVersionId>/
        └── <GitSha256>.sqlite            ← one file per (RepoVersion, SHA)
```

Multisite: `uploads/sites/<id>/git-logs/logs/<RepoVersionId>/<GitSha256>.sqlite`.

`<RepoVersionId>` is used as the directory partition (not `<GitSha256>` first) so that pruning a deleted RepoVersion is a single `rm -rf` of one folder.

`ConfigKv` keys (defaults seeded in §18):

| Key | Default | Purpose |
|-----|--------:|---------|
| `ShaLogsRoot` | `wp-content/uploads/git-logs/logs` | Override for tests / shared storage |
| `MaxOpenShaDbHandles` | `64` | LRU cap on open per-SHA handles per PHP process |
| `ShaDbIdleCloseSec` | `300` | Close a per-SHA handle after this many seconds idle |

---

## Per-SHA DB schema

Every per-SHA SQLite file is **self-contained** — a denormalized copy of `LogSeverity` is included so the file can be exported / zipped / handed to support without joining back to the root DB.

```sql
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- Single-row metadata (lets the file identify itself out-of-context)
CREATE TABLE ShaMeta (
    ShaMetaId INTEGER PRIMARY KEY AUTOINCREMENT,
    RepoVersionId INTEGER NOT NULL,
    GitSha256 TEXT NOT NULL,
    RepoUrl TEXT NOT NULL,
    BranchName TEXT NOT NULL,         -- last branch we saw push for this SHA
    CreatedAt INTEGER NOT NULL,
    PluginVersion TEXT NOT NULL       -- plugin version that created the file
);

-- Denormalized LogSeverity copy (file is portable)
CREATE TABLE LogSeverity (
    LogSeverityId INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE,
    Numeric INTEGER NOT NULL
);

-- The actual log lines
CREATE TABLE LogEntry (
    LogEntryId INTEGER PRIMARY KEY AUTOINCREMENT,
    PipelineId INTEGER NOT NULL,      -- root-DB FK; not enforced cross-file
    BranchName TEXT NOT NULL,
    PipelineName TEXT NOT NULL,
    LineNumber INTEGER NOT NULL,
    LogText TEXT NOT NULL,
    LogSeverityId INTEGER NOT NULL REFERENCES LogSeverity(LogSeverityId),
    FilePath TEXT NULL,
    OccurredAt INTEGER NOT NULL
);
CREATE INDEX idx_LogEntry_pipeline ON LogEntry(PipelineId, LineNumber);
CREATE INDEX idx_LogEntry_severity ON LogEntry(LogSeverityId, OccurredAt);

-- Error-only stream (mirrors LogEntry rows where severity ≥ Error, plus any line the caller flagged as error)
CREATE TABLE ErrorLogEntry (
    ErrorLogEntryId INTEGER PRIMARY KEY AUTOINCREMENT,
    PipelineId INTEGER NOT NULL,
    BranchName TEXT NOT NULL,
    PipelineName TEXT NOT NULL,
    LineNumber INTEGER NOT NULL,
    LogText TEXT NOT NULL,
    FilePath TEXT NULL,
    OccurredAt INTEGER NOT NULL
);
CREATE INDEX idx_ErrorLogEntry_pipeline ON ErrorLogEntry(PipelineId, LineNumber);

-- One row per (BranchName, PipelineName) execution within this SHA
CREATE TABLE PipelineRun (
    PipelineRunId INTEGER PRIMARY KEY AUTOINCREMENT,
    PipelineId INTEGER NOT NULL,
    BranchName TEXT NOT NULL,
    PipelineName TEXT NOT NULL,
    StartedAt INTEGER NOT NULL,
    EndedAt INTEGER NULL,             -- NULL = still running
    HasError INTEGER NOT NULL DEFAULT 0,
    ErrorCount INTEGER NOT NULL DEFAULT 0,
    LineCount INTEGER NOT NULL DEFAULT 0,
    LastSeverityId INTEGER NULL REFERENCES LogSeverity(LogSeverityId)
);
CREATE UNIQUE INDEX uq_PipelineRun ON PipelineRun(PipelineId, BranchName, PipelineName, StartedAt);

-- Single-row rolling aggregate that answers "what's the status of this SHA?"
CREATE TABLE StatusSnapshot (
    StatusSnapshotId INTEGER PRIMARY KEY AUTOINCREMENT,
    LastStatus TEXT NOT NULL DEFAULT 'Pending',  -- Green | Red | Pending
    FailureCount INTEGER NOT NULL DEFAULT 0,
    LastFailureAt INTEGER NULL,
    LastSuccessAt INTEGER NULL,
    LastEntryAt INTEGER NULL,
    UpdatedAt INTEGER NOT NULL
);
```

---

## Semantic queries the per-SHA file must answer (no app-side joins)

| Question | Query |
|----------|-------|
| What is the last status for this SHA? | `SELECT LastStatus FROM StatusSnapshot LIMIT 1;` |
| When was the last entry? | `SELECT LastEntryAt FROM StatusSnapshot LIMIT 1;` |
| How many failures? | `SELECT FailureCount FROM StatusSnapshot LIMIT 1;` |
| Is the branch green or red? | `SELECT LastStatus FROM StatusSnapshot LIMIT 1;` |
| Which pipelines are currently failing? | `SELECT BranchName, PipelineName FROM PipelineRun WHERE HasError = 1 AND EndedAt IS NULL OR (EndedAt IS NOT NULL AND HasError = 1);` |
| What's the per-pipeline error count? | `SELECT PipelineName, ErrorCount FROM PipelineRun ORDER BY StartedAt DESC;` |
| Get all errors for a pipeline | `SELECT * FROM ErrorLogEntry WHERE PipelineId = ? ORDER BY LineNumber;` |
| Which file produced the most errors? | `SELECT FilePath, COUNT(*) FROM ErrorLogEntry GROUP BY FilePath ORDER BY 2 DESC LIMIT 10;` |

---

## Lifecycle

1. **Create** — first `/append-log` for `(RepoVersionId, GitSha256)` not yet in `ShaRegistry`:
   - Acquire write lock on `ShaRegistry`.
   - `INSERT INTO ShaRegistry (RepoVersionId, GitSha256, ShaDbPath, FirstSeenAt, LastSeenAt, …) VALUES (…)`.
   - Create folder + per-SHA SQLite file via SQLite Online Backup API or fresh `sqlite3_open_v2`.
   - Apply the per-SHA schema above + seed denormalized `LogSeverity` rows.
   - Insert `ShaMeta` single row.
   - Insert `StatusSnapshot` single row (`LastStatus='Pending'`).
2. **Append** — every `/append-log` call:
   - Open per-SHA handle (LRU-cached, see `MaxOpenShaDbHandles`).
   - Insert into `LogEntry` (and `ErrorLogEntry` if severity ≥ Error or caller flagged).
   - Upsert the matching `PipelineRun` row (`LineCount += N`, `ErrorCount += K`, `HasError = HasError OR caller_HasError`, `LastSeverityId = max(...)`).
   - Update `StatusSnapshot` (`LastEntryAt = now`; if `HasError → LastStatus='Red', FailureCount += 1, LastFailureAt = now`; else `LastSuccessAt = now`; if no errors anywhere → `LastStatus='Green'`).
   - Mirror `EntryCount`/`ErrorCount`/`LastStatus`/`LastSeverityId`/`LastFailureAt`/`LastSuccessAt` back into root-DB `ShaRegistry` (so dashboards never have to open the per-SHA file).
3. **Idle close** — daemon / wp-cron closes any handle idle > `ShaDbIdleCloseSec`.
4. **Prune** — `wp git-logs prune --older-than=Nd` (see §22) walks `ShaRegistry`, deletes the per-SHA file, then deletes the row.
5. **Backup** — `wp git-logs backup` (see §23) zips the entire `git-logs/` directory, including the `logs/` subtree. Manifest lists every per-SHA file with row counts + sha256 of the file.
6. **Uninstall — Wipe mode** (see §29) — deletes the entire `uploads/git-logs/` folder including all per-SHA files.

---

## Error codes (added to §15)

| Code | HTTP | Meaning |
|------|-----:|---------|
| `GL-SHA-DB-CREATE-FAILED` | 500 | Could not create per-SHA file (perms / disk full) |
| `GL-SHA-DB-OPEN-FAILED` | 500 | File exists but `sqlite3_open_v2` returned non-OK |
| `GL-SHA-DB-CORRUPT` | 500 | `PRAGMA integrity_check` returned non-`ok` |
| `GL-SHA-DB-NOT-FOUND` | 404 | `ShaRegistry` row exists but file is missing |

---

## Cross-references

- Root-DB `ShaRegistry` table: §02
- Pruning: §22
- Backup/restore + manifest format: §23
- Uninstall behaviors: §29
- ER diagram (split boundary): `spec/26-gitlogs-diagrams/01-er-diagram.mmd`
- Domain diagram (split boundary): `spec/26-gitlogs-diagrams/02-domain-design.mmd`
- Split-DB pattern: `spec/05-split-db-architecture/00-overview.md`
