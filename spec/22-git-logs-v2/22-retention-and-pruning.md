# Retention & Pruning (v2)

**Version:** 2.9.0  
**Updated:** 2026-04-26 (Phase 3: rewrite around per-SHA split-DB — prune walks `ShaRegistry`, deletes `.db` files)

The plugin keeps every log entry forever by default. Operators control disk growth via an **opt-in** `wp git-logs prune` WP-CLI command. There is no automatic background prune in v2.

> **v3.8.3 (Q3 Split-DB) note.** As of schema v2.9.0 the root DB no longer
> stores `LogEntry` / `ErrorLogEntry` rows — they live exclusively inside
> per-SHA SQLite files at `<dataDir>/<ShaLogsRoot>/<Sha[0:2]>/<Sha>.db`
> (see §39). Pruning is therefore a **file-level** operation: the command
> walks `ShaRegistry`, decides which SHAs are eligible, deletes the
> corresponding per-SHA `.db` files, then deletes the matching
> `ShaRegistry` rows. The pre-v2.9.0 row-level `DELETE FROM LogEntry`
> path is **gone** — there is no longer a row-level prune mode.

---

## Eligibility rules

A `ShaRegistry` row (and its per-SHA `.db` file) is eligible for deletion iff **all** of:

1. `ShaRegistry.LastSeenAt < (now - --older-than)`.
2. The owning `Pipeline.HasError = 0`, **OR** the caller passed `--include-errors`.
3. The owning `Pipeline` is not referenced by an unresolved `PipelineAction` row dated within the retention window (avoid orphaning audit context).
4. No `History` row in the retention window references the same `(RepoVersionId, GitSha)` (history is the audit floor; never orphan a history row's logs).

A `Pipeline` row itself is eligible for deletion iff it has zero remaining `ShaRegistry` rows after the file-level prune. Pipelines are **never** deleted in the same transaction as their `ShaRegistry` rows — two-phase, so a crash leaves the root DB consistent.

`History`, `PipelineAction`, `SystemEvent`, `AuditTrail` rows are **never** pruned by this command. They are the audit floor.

---

## Command surface

```
wp git-logs prune \
  --older-than=<duration>     # required, e.g. 30d, 12w, 6mo, 1y
  [--include-errors]          # also prune SHAs whose Pipeline.HasError = 1
  [--include-pipelines]       # phase-3 sweep: drop now-empty Pipeline rows
  [--app=<AppSlug>]           # scope to one App
  [--repo=<RepoUrl>]          # scope to one Repo
  [--dry-run]                 # report counts only; no file/row deletes
  [--batch=<n>]               # default 200; ShaRegistry rows per transaction
  [--quiet | --verbose]
```

### Exit codes

| Code | Meaning |
|------|---------|
| 0    | Success (including dry-run) |
| 1    | Validation error (bad `--older-than`, unknown `--app`) |
| 2    | DB locked / SQLite busy after retries |
| 3    | Aborted by operator (Ctrl-C between batches) |
| 4    | Per-SHA file delete failed (FS error) — see `GL-SHA-DB-OPEN-FAILED` |

### Duration grammar

`<int><unit>` where unit is `d`, `w`, `mo`, `y`. No fractions, no compound (`1mo15d` invalid). Lower bound `7d` — refused below to prevent foot-guns.

---

## Audit trail

Every prune run emits exactly **one** `AuditTrail` row (not one per file):

| Field | Value |
|-------|-------|
| `AuditActionTypeId` | seed for `Prune` (already in `18-schema.sql`, ID 19) |
| `AuditOutcomeId`    | `Success` / `Error` |
| `ProfileId`         | NULL (CLI runs as system) |
| `Detail`            | JSON: `{ olderThan, includeErrors, scope, eligibleShaCount, deletedShaCount, reclaimedBytes, deletedPipelines, dryRun, durationMs, errors: [{sha, code}] }` |

`errors[]` lists per-SHA failures (e.g., `GL-SHA-DB-OPEN-FAILED`) — the run continues past per-file errors and reports them at the end; only a fatal root-DB error aborts the whole run.

---

## Transaction & file-deletion shape

Per-SHA prune is **two-step per row** so that an interrupted run never leaves a `ShaRegistry` row pointing at a missing file or a `.db` file with no registry entry:

```
-- Phase 1: select a batch of eligible SHAs (no writes)
SELECT ShaRegistryId, PipelineId, Sha, DbFilePath, FileSizeBytes
  FROM ShaRegistry sr
  JOIN Pipeline   p ON p.PipelineId = sr.PipelineId
 WHERE sr.LastSeenAt < :cutoff
   AND (p.HasError = 0 OR :includeErrors = 1)
   AND <scope filters>
   AND <history-window guard>
 ORDER BY sr.LastSeenAt
 LIMIT :batch;

-- Phase 2: per-row, do file delete first, then root-DB row delete
FOR EACH row:
    rename(<dataDir>/<DbFilePath>, <dataDir>/<DbFilePath>.pruning)   # atomic
    fsync(parent dir)
    BEGIN IMMEDIATE;
      DELETE FROM ShaRegistry WHERE ShaRegistryId = :id;
    COMMIT;
    unlink(<dataDir>/<DbFilePath>.pruning)
```

Crash-safety:
* If we crash after `rename` but before `DELETE`, the next prune sees a `ShaRegistry` row pointing at `<file>.pruning` — it finishes the delete (idempotent recovery on startup).
* If we crash after `DELETE` but before `unlink`, a startup janitor sweeps any `*.pruning` files with no matching `ShaRegistry` row.

Loop until the eligibility query returns zero rows. Then **phase-3 sweep** (only if `--include-pipelines`):

```
BEGIN IMMEDIATE;
  DELETE FROM Pipeline
   WHERE PipelineId NOT IN (SELECT DISTINCT PipelineId FROM ShaRegistry)
     AND PipelineId NOT IN (SELECT PipelineId FROM History         WHERE PipelineId IS NOT NULL UNION
                            SELECT PipelineId FROM PipelineAction  WHERE PipelineId IS NOT NULL)
     AND UpdatedAt < :cutoff;
COMMIT;
```

Run `PRAGMA wal_checkpoint(TRUNCATE);` on the **root DB** once at the end to reclaim its file size. (Per-SHA files are deleted whole, so no per-file checkpoint is needed.)

---

## Empty-shard cleanup

After all eligible files in a `<Sha[0:2]>` shard folder have been unlinked, the folder is removed (`rmdir`, ignore ENOTEMPTY). The `<ShaLogsRoot>` root itself is **never** removed by `prune` — only by §29 Wipe.

---

## Output (human format)

```
Git Logs prune
  Cutoff: 2026-03-26 00:00:00 UTC (older than 30d)
  Scope:  all apps / all repos
  Mode:   dry-run

Eligible:
  ShaRegistry rows    :     12,901
  Per-SHA .db files   :     12,901  (≈ 412 MiB on disk)
  Pipeline rows       :        117  (would be dropped — no --include-pipelines)
  Skipped (HasError)  :        842  (no --include-errors)

Estimated reclaim    : ~412 MiB
```

Same shape with `Deleted:` instead of `Eligible:` for a real run, plus a final `Errors: <n>` line if any per-file deletes failed.

---

## What NOT to do

- Do **not** add a `wp_cron` auto-prune in v2. Operators choose retention windows; surprise deletes erode trust.
- Do **not** allow prune to run while a migration is pending (`MigrationState.PluginVersion != ConfigKv.PluginVersion`). Refuse with exit 1.
- Do **not** prune below `7d` — minimum retention floor for incident triage.
- Do **not** delete the per-SHA `.db` file before deleting (or arming for delete) the `ShaRegistry` row pointing at it — always rename → delete-row → unlink.
- Do **not** open the per-SHA file during prune. The pool is for readers; prune operates on the file path only.
