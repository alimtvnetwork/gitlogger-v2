# Local Database

> **Related specs:**
> - [05-configuration.md](05-configuration.md) — config layer that coexists with DB persistence
> - [18-batch-execution.md](18-batch-execution.md) — DB-based repo loading for batch operations
> - [02-project-structure.md](02-project-structure.md) — `store/` package placement for DB code

## Overview

Use a local SQLite database for persistence. This enables slug-based
lookup, grouping, batch operations, and history tracking without
external dependencies.

## SQLite Setup

### Driver

Use a **CGo-free** SQLite driver (e.g., `modernc.org/sqlite` for Go).
No C compiler required.

### Location

| Item | Value |
|------|-------|
| Directory | `toolname-output/data/` (auto-created) |
| File name | `toolname.db` |

### Auto-Creation

On first data-producing command:
1. Check if database exists.
2. If missing, create it and initialize all tables.
3. Upsert data into tables.

## Concurrency & Locking (Normative)

> **AC anchor:** [`97-acceptance-criteria.md` § AC-22](97-acceptance-criteria.md) is the normative source. This section is the implementer-facing prose surface — if the two diverge, AC-22 wins and this prose MUST be patched (Lesson #33).

Every CLI built per this spec runs in a multi-process / multi-thread environment (concurrent invocations from shells, IDE plugins, watchers, and `--parallel=N` batch execution per `18-batch-execution.md`). The SQLite store and any sibling files under the config/data directory MUST therefore obey a closed concurrency contract.

### Required PRAGMAs (apply at every connection open)

| PRAGMA | Value | Why |
|--------|-------|-----|
| `journal_mode` | `WAL` | Concurrent readers + single writer; required for `--parallel=N` batches and IDE-plugin watchers |
| `busy_timeout` | `5000` (ms) | Cross-cuts spec/05 AC-SD-22 — kernel-level wait before `SQLITE_BUSY` is returned |
| `foreign_keys` | `ON` | SQLite default is OFF; FK enforcement is load-bearing for AC-23 cascade contracts |
| `synchronous` | `NORMAL` | Safe under WAL; `FULL` is wasteful, `OFF` risks corruption |

### Reference Go implementation (normative example)

The PRAGMAs above MUST be applied at every connection open. Concrete Go form using `mattn/go-sqlite3`:

```go
import (
    "database/sql"
    "fmt"
    "math/rand"
    "time"

    _ "github.com/mattn/go-sqlite3"
)

func openDB(path string) (*sql.DB, error) {
    // PRAGMAs are encoded in the DSN — applied per-connection automatically.
    dsn := fmt.Sprintf(
        "file:%s?_journal=WAL&_busy_timeout=5000&_foreign_keys=ON&_synchronous=NORMAL",
        path,
    )
    db, err := sql.Open("sqlite3", dsn)
    if err != nil {
        return nil, err
    }
    // Single connection — SQLite serialises writers regardless; pool > 1 just amplifies WAL contention.
    db.SetMaxOpenConns(1)
    return db, nil
}

// withWriteTx wraps every write transaction in BEGIN IMMEDIATE + retry-on-busy
// (3 attempts, base 100 ms, ±25 % jitter — mirrors spec/27 AC-T-28 R3).
func withWriteTx(db *sql.DB, fn func(tx *sql.Tx) error) error {
    var lastErr error
    for attempt := 0; attempt < 3; attempt++ {
        tx, err := db.Begin() // sqlite3 driver maps Begin → BEGIN; use raw Exec for IMMEDIATE:
        if err == nil {
            if _, err = tx.Exec("ROLLBACK; BEGIN IMMEDIATE"); err == nil {
                if err = fn(tx); err == nil {
                    if err = tx.Commit(); err == nil {
                        return nil
                    }
                }
                _ = tx.Rollback()
            }
        }
        lastErr = err
        if !isBusyOrLocked(err) {
            return err
        }
        // 100 ms base, ±25 % jitter.
        backoff := 100*time.Millisecond + time.Duration(rand.Int63n(int64(50*time.Millisecond))) - 25*time.Millisecond
        time.Sleep(backoff)
    }
    return lastErr
}
```

`isBusyOrLocked` matches `sqlite3.ErrBusy` (`SQLITE_BUSY`) or `sqlite3.ErrLocked` (`SQLITE_LOCKED`). After 3 failed retries, surface the original error to the caller — do NOT swallow it.

### Transaction discipline

- **Every WRITE transaction MUST use `BEGIN IMMEDIATE`** (NOT default `DEFERRED`). Reason: `DEFERRED` acquires the write lock at first write statement, mid-transaction — by then the application has done useful work and the rollback cost is high. `IMMEDIATE` fails fast at `BEGIN` with `SQLITE_BUSY`, letting the retry loop kick in cheaply.
- **`SQLITE_BUSY` / `SQLITE_LOCKED` MUST be retried** with exponential back-off: **3 attempts, base 100 ms, ±25 % jitter** (mirrors spec/27 AC-T-28 R3). After 3 failures, surface the original error to the caller.
- **Read-only queries** MAY use `BEGIN DEFERRED` or no explicit transaction — WAL allows them to proceed against any snapshot regardless of writer state.

### File writes outside SQLite (config files, lock files, cache entries)

Use the **atomic temp-then-rename** pattern (spec/27 AC-T-28 R1):

1. Write payload to `<target>.tmp.<pid>` (same directory as `<target>` — must be on the same filesystem so `rename(2)` is atomic).
2. `fsync` the temp file's file descriptor.
3. `os.Rename(<target>.tmp.<pid>, <target>)` — POSIX guarantees atomic replace.
4. `fsync` the parent directory (Linux requirement for rename durability).
5. Cleanup the temp file in a `finally` / `defer` block on any error path.

Direct in-place writes (`os.WriteFile(<target>, ...)`) are **FORBIDDEN** for any file another process may read concurrently — a partial write is observable as truncated content.

### Process-level update lock

`update` and `self-update` subcommands MUST acquire a process-level lock file at:

```
~/.local/state/<binary-name>/update.lock
```

before mutating the binary on disk. The lock file MUST contain the holding process's PID. If the lock is already held:

```
$ <binary-name> update
error: another update is in progress (lock held by PID 12345)
```

Exit code MUST be `1` (`ExitError` per spec/13 AC-21 typed enum). The lock MUST be released in a `finally` / `defer` block — never rely on process exit alone, because a SIGKILL'd updater leaves a stale lock that blocks future invocations until the user clears it manually.

### Forbidden patterns

- Opening **N independent SQLite connections** for a `--parallel=N` batch — amplifies WAL checkpoint contention and starves readers. Use a single connection pool sized N instead (see `18-batch-execution.md` § "Concurrency Discipline").
- Skipping `busy_timeout` and "rolling your own" timeout in application code — the kernel-level PRAGMA is correct and battle-tested; application-level timeouts race against the SQLite mutex internals.
- Using `BEGIN DEFERRED` for any transaction that contains an `INSERT` / `UPDATE` / `DELETE` (lock acquisition is then mid-transaction — see "Transaction discipline" above).
- Writing config/cache files in-place without temp-then-rename — partial writes corrupt the file from a concurrent reader's perspective.

## Schema Conventions


| Convention | Detail |
|------------|--------|
| Table names | PascalCase (`Repos`, `Groups`) |
| Column names | PascalCase (`RepoName`, `AbsolutePath`) |
| Primary keys | `Id TEXT PRIMARY KEY` (UUID) |
| Timestamps | `TEXT DEFAULT CURRENT_TIMESTAMP` |
| Booleans | `INTEGER DEFAULT 0` (0/1) |
| String defaults | `DEFAULT ''` (never NULL) |

## Core Tables

### Items Table (e.g., Repos)

```sql
CREATE TABLE IF NOT EXISTS Repos (
    Id            TEXT PRIMARY KEY,
    Slug          TEXT NOT NULL,
    Name          TEXT NOT NULL,
    HttpsUrl      TEXT NOT NULL,
    AbsolutePath  TEXT NOT NULL,
    CreatedAt     TEXT DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt     TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_repos_path ON Repos(AbsolutePath);
```

### Groups Table

```sql
CREATE TABLE IF NOT EXISTS Groups (
    Id          TEXT PRIMARY KEY,
    Name        TEXT NOT NULL UNIQUE,
    Description TEXT DEFAULT '',
    CreatedAt   TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Join Table

```sql
CREATE TABLE IF NOT EXISTS GroupItems (
    GroupId TEXT NOT NULL REFERENCES Groups(Id) ON DELETE CASCADE,
    ItemId  TEXT NOT NULL REFERENCES Repos(Id) ON DELETE CASCADE,
    PRIMARY KEY (GroupId, ItemId)
);
```

### History Table

```sql
CREATE TABLE IF NOT EXISTS CommandHistory (
    Id         TEXT PRIMARY KEY,
    Command    TEXT NOT NULL,
    Args       TEXT DEFAULT '',
    StartedAt  TEXT NOT NULL,
    DurationMs INTEGER DEFAULT 0,
    ExitCode   INTEGER DEFAULT 0,
    CreatedAt  TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## Upsert Strategy

Match by unique field (e.g., `AbsolutePath`). If exists, update.
Otherwise, insert.

```go
const UpsertRepo = `
INSERT INTO Repos (Id, Slug, Name, AbsolutePath)
VALUES (?, ?, ?, ?)
ON CONFLICT(AbsolutePath) DO UPDATE SET
    Slug = excluded.Slug,
    Name = excluded.Name,
    UpdatedAt = CURRENT_TIMESTAMP
`
```

## DB-First Lookup with Fallback

Commands that resolve items by slug:
1. Try the database first.
2. Fall back to JSON file if database doesn't exist.

## Store Package Structure

```
store/
├── store.go     DB init, open, close, migration, reset
├── repo.go      Item CRUD (upsert, list, find by slug)
├── group.go     Group CRUD
└── history.go   History insert + query
```

## Contributors

- [**Md. Alim Ul Karim**](https://www.linkedin.com/in/alimkarim) — Creator & Lead Architect. System architect with 20+ years of professional software engineering experience across enterprise, fintech, and distributed systems. Recognized as one of the top software architects globally. Alim's architectural philosophy — consistency over cleverness, convention over configuration — is the driving force behind every design decision in this framework.
  - [Google Profile](https://www.google.com/search?q=Alim+Ul+Karim)
- [Riseup Asia LLC (Top Leading Software Company in WY)](https://riseup-asia.com) (2026)
  - [Facebook](https://www.facebook.com/riseupasia.talent/)
  - [LinkedIn](https://www.linkedin.com/company/105304484/)
  - [YouTube](https://www.youtube.com/@riseup-asia)
