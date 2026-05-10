# Backup & Restore (v2)

**Version:** 2.9.0  
**Updated:** 2026-04-26 (Phase 3: backup manifest enumerates per-SHA `.db` files with row counts + sha256)

The Git Logs plugin stores root metadata in a **single SQLite file** at `wp-content/uploads/git-logs/git-logs.sqlite`, plus a tree of per-SHA SQLite files at `wp-content/uploads/git-logs/<ShaLogsRoot>/<Sha[0:2]>/<Sha>.db` (see §39). Backup = root copy + per-SHA tree copy. Restore = atomic swap of both. This document spells out the safe procedure so a hot copy never produces a torn or unreadable database **and never leaves a `ShaRegistry` row pointing at a missing per-SHA file**.

---

## File layout

| Path | Purpose |
|------|---------|
| `wp-content/uploads/git-logs/git-logs.sqlite`              | Root DB |
| `wp-content/uploads/git-logs/git-logs.sqlite-wal`          | Root WAL (transient) |
| `wp-content/uploads/git-logs/git-logs.sqlite-shm`          | Root shared memory (transient) |
| `wp-content/uploads/git-logs/<ShaLogsRoot>/<aa>/<sha>.db`     | Per-SHA log file (one per Git SHA — `<aa>` is the first 2 hex chars of `<sha>`) |
| `wp-content/uploads/git-logs/<ShaLogsRoot>/<aa>/<sha>.db-wal` | Per-SHA WAL (transient) |
| `wp-content/uploads/git-logs/<ShaLogsRoot>/<aa>/<sha>.db-shm` | Per-SHA shared memory (transient) |

WAL mode is mandatory on **both** root and per-SHA files (set via `PRAGMA journal_mode = WAL` in §18 and §39). Every `-wal` file MUST be included in any backup, OR a `wal_checkpoint(TRUNCATE)` must be run on every open file before copying so all data lives in the main `.db` file.

---

## Backup — recommended (`wp git-logs backup`)

```
wp git-logs backup --to=<path> [--checkpoint] [--gzip] [--skip-sha-checksum]
```

`<path>` is a **directory** (or a `.tar.gz` if `--gzip`); the backup is a tree, not a single file:

```
<path>/
  git-logs.sqlite                  # root DB (Online Backup API copy)
  manifest.json                    # see schema below
  logs/
    <aa>/
      <sha>.db                     # one file per ShaRegistry row
      ...
```

Internally:

```
1. PRAGMA wal_checkpoint(TRUNCATE);      -- on root DB; merge WAL into main
2. Open SQLite Online Backup API handle on root → <path>/git-logs.sqlite
3. Stream pages in 1000-page chunks
4. PRAGMA integrity_check on the destination root
5. SELECT ShaRegistryId, PipelineId, Sha, DbFilePath, RowCount, FileSizeBytes
   FROM ShaRegistry  ORDER BY ShaRegistryId
6. For each ShaRegistry row:
   a. Acquire pool handle to <dataDir>/<DbFilePath>
   b. PRAGMA wal_checkpoint(TRUNCATE)
   c. Open SQLite Online Backup API → <path>/<DbFilePath>
   d. PRAGMA integrity_check on the destination per-SHA file
   e. Recompute sha256 of the destination file (unless --skip-sha-checksum)
   f. Append a manifest entry with {Sha, DbFilePath, RowCount, FileSizeBytes, Sha256}
7. Write <path>/manifest.json (see schema below)
8. Optional: tar -czf <path>.tar.gz <path>
```

The Online Backup API is the **only** safe hot copy — `cp` of a live DB will tear under concurrent writes even in WAL mode. This applies to **every** per-SHA file as well.

---

## Backup — operator manual (no CLI)

If WP-CLI is unavailable:

```
1. systemctl stop php-fpm    # or set plugin to maintenance mode
2. sqlite3 git-logs.sqlite "PRAGMA wal_checkpoint(TRUNCATE);"
3. for f in $(find logs -name '*.db'); do
     sqlite3 "$f" "PRAGMA wal_checkpoint(TRUNCATE);"
   done
4. cp -a git-logs.sqlite logs /backup/git-logs-$(date +%Y%m%d)/
5. systemctl start php-fpm
```

Cold-copy of the whole tree is always safe. Hot-copy without per-file checkpoints is unsafe.

---

## Restore — recommended (`wp git-logs restore`)

```
wp git-logs restore --from=<path> [--force] [--skip-sha-checksum]
```

Internally:

```
 1. Refuse unless plugin is in maintenance mode (`ConfigKv.MaintenanceMode = '1'`)
    OR --force was passed.
 2. PRAGMA integrity_check on <path>/git-logs.sqlite; abort on failure.
 3. Compare <path>/manifest.json:
    - SchemaChecksum must match current code expectations,
      OR --force allows mismatch (operator accepts migration risk).
 4. For each ShaFile entry in manifest.ShaFiles:
    a. Verify <path>/<DbFilePath> exists; abort if missing.
    b. PRAGMA integrity_check on the per-SHA file; abort on failure.
    c. Recompute sha256 and compare to manifest.Sha256
       (skip if --skip-sha-checksum) — abort with GL-SHA-DB-CHECKSUM-MISMATCH on drift.
 5. Move current git-logs.sqlite{,-wal,-shm} to .bak with timestamp.
 6. Move current logs/ tree to logs.bak.<timestamp>/.
 7. Copy <path>/git-logs.sqlite into place; chmod 0600; chown to web user.
 8. Copy <path>/logs/ tree into place; chmod 0600 on each .db; chown to web user.
 9. Open root DB; run migrator (idempotent — see §06).
10. Walk ShaRegistry once and assert that every DbFilePath exists on disk
    (missing file ⇒ abort + roll back to .bak).
11. Verify row counts non-zero on Pipeline + Profile.
12. Clear MaintenanceMode.
13. Emit AuditTrail row (AuditActionType=Restore, seed ID 20).
```

Restore is **all-or-nothing**: if any per-SHA verification fails, the original `.bak` tree is rolled back into place and the run aborts with a non-zero exit code.

---

## Manifest schema

Stored at `<path>/manifest.json`. Required for safe restore.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| PluginVersion  | string  | yes | semver |
| SchemaChecksum | string  | yes | sha256 of canonicalized `CREATE` statements from root `sqlite_master` |
| TakenAt        | int64   | yes | unix seconds |
| RowCounts      | object  | yes | per-root-table counts; sanity check on restore |
| ShaFiles       | array   | yes | one entry per per-SHA file — see below |
| ShaFileTotal   | int64   | yes | sum of `ShaFiles[].RowCount` (split-DB equivalent of `RowCounts.LogEntry` + `RowCounts.ErrorLogEntry` in pre-v2.9.0 backups) |
| WpVersion      | string  | no  | for diagnostics |
| PhpVersion     | string  | no  | for diagnostics |
| Notes          | string  | no  | free text from operator |

### `ShaFiles[]` entry

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| PipelineId    | int64  | yes | FK from `ShaRegistry.PipelineId` |
| Sha           | string | yes | 40-char lowercase hex |
| DbFilePath    | string | yes | relative path under `<ShaLogsRoot>` (e.g. `logs/ab/abc123…db`) |
| RowCount      | int64  | yes | total rows in per-SHA file (LogEntry + ErrorLogEntry) at backup time |
| FileSizeBytes | int64  | yes | post-checkpoint file size in bytes |
| Sha256        | string | yes | sha256 of the per-SHA `.db` file as written into the backup tree |

The `ShaFiles[]` list is the **canonical inventory** consulted by §29 (Wipe enumerates the tree before unlink) and by `verify` (re-walks `ShaRegistry` and compares against the manifest).

---

## Cross-version restore

| From → To | Behavior |
|-----------|----------|
| Same major | Auto-migrate via `MigrationState`; no operator action. |
| Older major (e.g. 2.x → 3.x) | `--force` required. Migrator runs forward; no rollback path. Per-SHA file format is **append-only-compatible** within a major; cross-major may require a rebuild. |
| Newer major (downgrade) | **Refused, no override.** Schema may have columns the older code can't read. Operator must restore to a matching plugin version first. |
| Pre-v2.9.0 → v2.9.0+ | `--force` required. Migrator splits the legacy root `LogEntry`/`ErrorLogEntry` rows into per-SHA files keyed by `(PipelineId, GitSha)`. No data loss; one-way. |

---

## Verification after restore

`wp git-logs verify` runs:

1. `PRAGMA integrity_check` on root (must return `ok`).
2. `PRAGMA foreign_key_check` on root (must return zero rows).
3. Row count of `Profile` ≥ 1.
4. `MigrationState.PluginVersion = ConfigKv.PluginVersion`.
5. Walk `ShaRegistry`: every `DbFilePath` exists AND `PRAGMA integrity_check` returns `ok` AND (optional) sha256 matches the manifest.
6. Latest `AuditTrail` row is the `Restore` event (sanity).

Exit 0 on all-pass; exit 1 with the failed check name otherwise. Per-SHA failures emit `GL-SHA-DB-OPEN-FAILED` / `GL-SHA-DB-CHECKSUM-MISMATCH` per §15. Site Health card (§20) surfaces the same checks for non-CLI operators.

---

## What is NOT in scope for v2

- Incremental / differential backups (full only — but per-SHA files are immutable once a SHA is fully ingested, so an external incremental tool can dedupe trivially).
- Off-site upload (S3, GCS).
- Encryption-at-rest of the backup file (operator's job until v3 §11 lands).
- Point-in-time restore (no WAL archive shipping).
