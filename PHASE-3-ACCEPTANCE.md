# Phase 3 — SQLite Schema + Repository Layer (Acceptance)

Adds the persistent storage substrate. From here on, runs and events have a real home.

## Storage layout

Under `wp-content/uploads/git-logs/`:

```
db/
  .htaccess                # Require all denied
  index.html               # empty (directory-listing block)
  root.sqlite              # repos, branches, runs, sha_index, audit, schema_migrations
  sha/
    <40-hex-sha>.sqlite    # per-commit DB: events + summary
```

All connections use:

| PRAGMA | Value | Why |
|--------|-------|-----|
| `journal_mode` | `WAL` | concurrent readers + 1 writer |
| `synchronous` | `NORMAL` | WAL-safe, faster than FULL |
| `foreign_keys` | `ON` | enforce FK constraints |
| `busy_timeout` | `5000` ms | 5s lock-retry window |

## Components shipped in P3

| Component | Path | Purpose |
|-----------|------|---------|
| Database | `git-logs-plugin/includes/db/class-database.php` | PDO factories: `Database::root()` + `Database::sha($sha)`, with on-demand per-SHA schema |
| MigrationRunner | `git-logs-plugin/includes/db/class-migration-runner.php` | Applies `migrations/NNNN_*.sql` in order, records SHA-256 checksums, refuses to re-apply edited files |
| 0001_root_schema | `git-logs-plugin/includes/db/migrations/0001_root_schema.sql` | repos, branches, runs, sha_index, audit, schema_migrations |
| RepoStore | `git-logs-plugin/includes/db/class-repo-store.php` | upsert/lookup/list/archive |
| BranchStore | `git-logs-plugin/includes/db/class-branch-store.php` | touch + list-for-repo |
| RunStore | `git-logs-plugin/includes/db/class-run-store.php` | create (UUIDv4), set_status (state machine), update_counts, find, list_recent |
| ShaIndex | `git-logs-plugin/includes/db/class-sha-index.php` | sha → run-ids reverse index |
| AuditLog | `git-logs-plugin/includes/db/class-audit-log.php` | append-only audit trail |
| EventStore | `git-logs-plugin/includes/db/class-event-store.php` | batched event append into per-SHA DB + summary recompute + mirror counts to `runs` |
| `/admin/migrate` | `git-logs-plugin/includes/rest/class-rest-admin-migrate.php` | GET = applied versions, POST = run pending (admin-only) |

## State machines

### Run status

```
queued → running → succeeded
                 → failed
                 → cancelled
                 → timed_out
```

`RunStore::set_status()` enforces the allowed values and stamps `finished_utc` + `duration_ms` on terminal transitions.

### Event severity

`debug | info | warn | error | fatal`

`EventStore::append()` increments `summary.error_count` for `error|fatal` and `summary.warn_count` for `warn`, then mirrors the totals onto the root `runs` row via `RunStore::update_counts()`.

## Acceptance checklist

### 1. Activation creates DB + applies migrations
Re-activate the plugin (Plugins → Deactivate → Activate). Then:
```bash
ls wp-content/uploads/git-logs/db/
# expect: root.sqlite, sha/, .htaccess, index.html

sqlite3 wp-content/uploads/git-logs/db/root.sqlite '.tables'
# expect: audit  branches  repos  runs  schema_migrations  sha_index
```

### 2. Migration runner is idempotent
```bash
curl -u alice:'XXXX YYYY ZZZZ AAAA' -X POST \
  https://your-site.test/wp-json/git-logs/v1/admin/migrate
# expect: {"applied":[],"skipped":["0001_root_schema"],"failed":null}
```

### 3. Migration runner detects edited migrations
- Edit one byte of `migrations/0001_root_schema.sql`.
- POST `/admin/migrate` again.
- Expect HTTP 500 with `failed: "migration 0001_root_schema has been edited..."`. Revert the edit.

### 4. End-to-end CRUD smoke (PHP REPL via wp-cli)
```bash
wp eval '
  require WP_PLUGIN_DIR."/git-logs/includes/db/class-repo-store.php";
  require WP_PLUGIN_DIR."/git-logs/includes/db/class-run-store.php";
  require WP_PLUGIN_DIR."/git-logs/includes/db/class-event-store.php";

  $repo = GitLogs\DB\RepoStore::upsert("acme/web", "Acme Web");
  $run  = GitLogs\DB\RunStore::create([
    "repo_id"=>$repo, "branch"=>"main",
    "sha"=>str_repeat("a", 40), "ci_provider"=>"local",
    "triggered_by"=>"smoke",
  ]);
  GitLogs\DB\RunStore::set_status($run, "running");
  GitLogs\DB\EventStore::append(str_repeat("a",40), $run, [
    ["seq"=>1,"ts_utc"=>gmdate("c"),"stream"=>"stdout","phase"=>"build","severity"=>"info","message"=>"hello"],
    ["seq"=>2,"ts_utc"=>gmdate("c"),"stream"=>"stderr","phase"=>"build","severity"=>"error","message"=>"boom"],
  ]);
  GitLogs\DB\RunStore::set_status($run, "failed", 1);
  GitLogs\DB\EventStore::finalize(str_repeat("a",40), $run, null, 1);

  $row = GitLogs\DB\RunStore::find($run);
  echo "duration_ms={$row[\"duration_ms\"]} errors={$row[\"error_count\"]}\n";
'
# expect: duration_ms=<small int> errors=1
```

### 5. Per-SHA file is written
```bash
ls wp-content/uploads/git-logs/db/sha/
# expect: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.sqlite

sqlite3 wp-content/uploads/git-logs/db/sha/aaaa...aaaa.sqlite \
  'SELECT seq, severity, message FROM events ORDER BY seq;'
# expect: 1|info|hello
#         2|error|boom
```

### 6. Audit row recorded for /admin/migrate
```bash
sqlite3 wp-content/uploads/git-logs/db/root.sqlite \
  'SELECT action, result, actor_login FROM audit ORDER BY id DESC LIMIT 1;'
# expect: admin.migrate|ok|alice
```

## What is NOT in P3

- Public REST endpoints to create runs / append events / fetch summaries → P4
- Admin UI to browse runs/audit → P7
- GC of old per-SHA files → P4 (`POST /admin/gc`)
- Cross-cluster replication, backups → out of scope for this plan

## Decisions locked in P3

- **Storage location**: `wp-content/uploads/git-logs/db/` (writable by WP, denied by `.htaccess`)
- **DB engine**: SQLite via PDO (PHP `pdo_sqlite` is in core; no extra deps)
- **Concurrency**: WAL mode, 5s busy-timeout — single writer per file is fine for CI ingestion rates
- **UUID strategy**: PHP `random_bytes(16)` + RFC-4122 v4 reshape (no UUID library)
- **Per-SHA file naming**: `<40-hex-sha>.sqlite`, lowercase, validated by regex `[0-9a-f]{40}`
- **Migrations**: file-system source of truth, SHA-256 checksum stored to detect post-apply edits
- **Append safety**: `INSERT OR IGNORE` keyed on `(run_id, seq)` → idempotent re-submission of the same batch
