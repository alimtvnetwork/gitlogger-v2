# Post-P8 #9 — DB Layer PHP Tests

**Status:** ✅ done

## Scope
Cover the SQLite-backed DB layer end-to-end (real PDO, real schema, real
migrations) using a separate runner that bypasses the in-memory stubs the
auth/REST suite relies on.

## Approach
- New `tests/bootstrap-db.php`: minimal WP shims (`wp_get_upload_dir`,
  `wp_mkdir_p`, `wp_json_encode`, `__`) pointed at a per-process scratch
  directory under `/tmp/git-logs-tests-{pid}`. Loads the **real** Database,
  ShaIndex, RepoStore, RunStore, BranchStore, EventStore, AuditLog, and
  MigrationRunner — no stubs.
- New `tests/run-db.php`: discovers `tests/db/test-*.php`, runs every
  global `dbtest_*` function, calls `migrate_fresh()` between tests
  (wipe scratch dir → `Database::reset_for_tests()` → `MigrationRunner::migrate()`),
  and tears down the scratch dir on shutdown.
- Adds `assertNotNull` and `assertThrows( $fn, $expect_substr )` helpers.

## New tests (41)

`tests/db/test-database.php` (7)
- migrate creates root schema + records version `0001_root_schema`
- migrate is idempotent (second call: 0 applied / 1 skipped)
- migrate detects on-disk tampering via checksum mismatch
- WAL journal-mode and FK enforcement applied
- per-SHA db opens with `events`/`summary` tables
- SHA normalisation rejects garbage
- `ensure_dirs` writes `.htaccess` deny rule

`tests/db/test-repos-branches-sha-index.php` (10)
- repo upsert returns id, second call updates same row
- `id_for_slug` throws on missing repo
- `list_all` filters archived (configurable)
- `find_by_slug` returns null for unknown
- branch `touch` is idempotent per (repo,name) and updates head_sha
- branch `touch` with null head_sha preserves existing value
- branches isolated per repo
- ShaIndex normalises sha case across writes/reads
- `INSERT OR IGNORE` dedupe for re-adding same (sha,run)

`tests/db/test-runs.php` (9)
- create returns 36-char UUID v4 and stores metadata JSON
- create lowercases the SHA
- `running` status keeps `finished_utc`/`duration_ms` null
- terminal status writes `finished_utc` and computes `duration_ms`
- `set_status` rejects values outside the allowed enum
- `update_counts` writes through to the row
- `find` returns null for unknown id
- `list_recent` honours limit and returns full set within repo
- `list_recent` isolates per-repo

`tests/db/test-events.php` (9)
- append/read round-trip with `after_seq` paging
- summary roll-up across multiple appends; mirrored onto runs row via `RunStore::update_counts`
- duplicate `(run_id, seq)` rows skipped (`INSERT OR IGNORE` semantics)
- validation rejects bad `stream`, bad `severity`, missing required field
- `finalize` writes `finished_utc` + `exit_code`
- per-run isolation
- `attrs` array serialised as JSON and returned in the `attrs_json` column

`tests/db/test-audit.php` (6)
- `record` inserts and returns autoincrement PK
- default `auth_lane` is `'system'`
- `CHECK` constraint rejects bogus `auth_lane`
- `CHECK` constraint rejects bogus `result`
- `recent` orders DESC and honours limit
- `recent` filters by action

## Result
```
DB tests: 41 | Passed: 41 | Failed: 0 | Assertions: 115
```
Auth + REST suite still green:
```
Tests: 48 | Passed: 48 | Failed: 0 | Assertions: 106
```

## CI
`.github/workflows/ci-wp-plugin.yml` now adds `pdo_sqlite` to the matrix
extensions and runs both `tests/run.php` and `tests/run-db.php` across
PHP 8.1–8.4.

## Files changed
- new: `git-logs-plugin/tests/bootstrap-db.php`
- new: `git-logs-plugin/tests/run-db.php`
- new: `git-logs-plugin/tests/db/test-database.php`
- new: `git-logs-plugin/tests/db/test-repos-branches-sha-index.php`
- new: `git-logs-plugin/tests/db/test-runs.php`
- new: `git-logs-plugin/tests/db/test-events.php`
- new: `git-logs-plugin/tests/db/test-audit.php`
- edited: `.github/workflows/ci-wp-plugin.yml`
