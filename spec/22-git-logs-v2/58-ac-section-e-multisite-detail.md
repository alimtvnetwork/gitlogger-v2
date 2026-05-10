# AC-34 — Multisite Per-Site DB (Section E Detail)

**Status:** active · **Phase:** E-1 (multisite tenancy tier-1 binding) · **Bound from:** `97-acceptance-criteria.md` §AC-34
**Mirror class:** AC-05 (§53) · AC-12 (§55) · AC-23 (§56) · AC-11 (§57) — Phase D/E normative-surface promotions
**Generated:** 2026-05-10 (Lesson #19 audit-boundary pin; Lesson #36 link-don't-restate)

---

## Why this file exists

Pre-promotion AC-34 in §97 was a single dense paragraph (~3.6 KB) packing 9 distinct normative clauses (per-site path, single-shared forbidden, site-scoped reads, no aggregated UI, blog-switch invalidation, identical schema, lazy migration, deletion cleanup, single-site fallback). The audit walker chunk merge averaged d2 (testability) low because no T-IDs enumerated the scenarios. This file is the tier-1 binding surface with a 9-row T-MS-* matrix.

## Per-site DB path resolution

| Context | `blog_id` | DB path (resolved via `wp_upload_dir()`) |
|---|---:|---|
| Single-site (non-multisite) | 1 | `/wp-content/uploads/git-logs/plugin.db` |
| Multisite main site | 1 | `/wp-content/uploads/git-logs/plugin.db` |
| Multisite subsite #2 | 2 | `/wp-content/uploads/sites/2/git-logs/plugin.db` |
| Multisite subsite #N | N | `/wp-content/uploads/sites/N/git-logs/plugin.db` |

The DB locator MUST NOT branch on `is_multisite()` — the WordPress `wp_upload_dir()` function already returns subsite-scoped paths. A single shared DB across subsites is FORBIDDEN.

## Normative invariants

1. **Filesystem-level tenancy.** Per-site DB files are MANDATORY even when network-activated. Row-level multitenancy via a `blog_id` column is FORBIDDEN.
2. **Site-scoped reads.** A request handled in `blog_id=2` context MUST query ONLY the `sites/2/` DB. Cross-subsite fan-out is FORBIDDEN.
3. **No aggregated network-admin view.** Cross-site analytics is explicitly out of scope for v2.
4. **Blog-switch invalidation.** `switch_to_blog($id)` MUST invalidate the DB connection; a fresh connection MUST open against the newly-active subsite's DB on next access. Connection cache key = `(blog_id, db_path)`, NOT global.
5. **Symmetric restore.** `restore_current_blog()` MUST restore the prior connection. Leaking a connection across blog-switch boundaries is a SPEC VIOLATION.
6. **Identical schema across subsites.** Same migrations apply per AC-03 + AC-29.
7. **Lazy migration.** The migration runner runs independently per subsite on **first DB access** in that subsite's context. Eager init at network-activation is FORBIDDEN (would create N empty DBs for never-visited subsites, wasting inodes).
8. **Subsite deletion cleanup.** `wp_delete_site($id)` MUST trigger removal of `sites/<id>/git-logs/`. Orphan DBs from deleted subsites are a SPEC VIOLATION caught by an audit linter.
9. **Single-site = `blog_id=1`.** No `is_multisite()` branch in the DB locator.

## Why per-site files (rationale)

- **Per-site backup/restore** + per-site purge without cross-site impact (works with §23).
- **Quota isolation** — runaway log volume on one subsite cannot starve others.
- **WordPress mental model** — each subsite "owns" its uploads directory.
- **Operator deletability** — `rm -rf` of a subsite's uploads dir leaves zero orphan rows.

## Test invariants (T-MS-01..T-MS-09)

| T-ID | Invariant | Assertion |
|---|---|---|
| T-MS-01 | Per-site DB path uses `wp_upload_dir()`; subsite #2 → `sites/2/git-logs/plugin.db` | `assertSame('/wp-content/uploads/sites/2/git-logs/plugin.db', $locator->resolve(2))` |
| T-MS-02 | Single shared DB across subsites is FORBIDDEN | `assertNotSame($locator->resolve(2), $locator->resolve(3))` |
| T-MS-03 | Read in `blog_id=2` context queries ONLY `sites/2/` DB | `assertNoQueriesAgainst('sites/3/git-logs/plugin.db', $callable)` |
| T-MS-04 | `switch_to_blog(3)` invalidates connection; next access opens `sites/3/` | `assertNotSame($conn1, $conn2)` after switch |
| T-MS-05 | Connection cache keyed by `(blog_id, db_path)`, NOT global | `assertSame($cache->get([2, $path2]), $conn2)` |
| T-MS-06 | `restore_current_blog()` restores prior connection | `assertSame($conn1, $registry->current())` after restore |
| T-MS-07 | Migration runner runs per-subsite **lazily** on first access | `assertFileNotExists($path3)` before first access in `blog_id=3` |
| T-MS-08 | `wp_delete_site(2)` removes `sites/2/git-logs/` directory | `assertDirectoryDoesNotExist('/wp-content/uploads/sites/2/git-logs/')` post-hook |
| T-MS-09 | Single-site install resolves to `uploads/git-logs/plugin.db` (no multisite branch) | `assertSame('/wp-content/uploads/git-logs/plugin.db', $locator->resolve(1))` (with `is_multisite()=false`) |

Test files: `test/AcMultisiteTenancyTest.php` (PHPUnit) + `test/ac-multisite-tenancy.bats` (bats CLI smoke). Each test method MUST embed its T-ID; absence triggers `GL-TEST-COVERAGE-GAP` per AC-80.

## Worked example (T-MS-04 — blog-switch connection invalidation)

```php
// blog_id=1 context
$conn1 = $registry->current();              // → opens uploads/git-logs/plugin.db
$conn1->query("SELECT * FROM Pipeline LIMIT 1");

switch_to_blog(3);                          // network-admin loop
$conn3 = $registry->current();              // → MUST open sites/3/git-logs/plugin.db
assert($conn3 !== $conn1);                  // T-MS-04
assert($conn3->path === '/wp-content/uploads/sites/3/git-logs/plugin.db');

restore_current_blog();
$conn1again = $registry->current();
assert($conn1again === $conn1);             // T-MS-06 — symmetric restore
```

A leaked connection (e.g. `$registry` reuses `$conn1` after `switch_to_blog(3)`) silently writes blog 3's audit rows into blog 1's DB — a tenancy bug catastrophic for compliance audits. The cache-key invariant (T-MS-05) is the structural defense.

## Cross-references

- **§97 §AC-34** — slim binding stub (this file is the full body)
- **§24 `24-multisite.md`** — multisite per-site DB contract (full prose)
- **AC-03** — migration runner contract (applies per-site, lazily)
- **AC-29** — migration ordering and `MigrationState` markers
- **AC-21** — audit tables are per-site, not network-wide
- **AC-12** — ingest writes go to the active subsite's DB
- **AC-80** — sibling test-file delegation + `GL-TEST-COVERAGE-GAP`
