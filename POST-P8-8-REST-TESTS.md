# Post-P8 #8 — REST Controller PHP Test Harness

**Status:** ✅ done

## Scope
Exercise every REST controller in `git-logs-plugin/includes/rest/` directly,
without spinning up `WP_REST_Server` or a real WordPress install.

## Approach
- Extended `tests/bootstrap.php` to load three new shim layers BEFORE the
  production classes:
  - `tests/stubs/wp-rest-stubs.php` — `WP_REST_Response`,
    `WP_REST_Request_Ext` (param/JSON/ArrayAccess-aware), `register_rest_route`,
    `sanitize_key`, `current_user_can`, `wp_get_current_user`, and the
    `GitLogs\GIT_LOGS_REST_NS` namespace constant via `define()`.
  - `tests/stubs/db-stubs.php` — in-memory namespaced re-implementations of
    `\GitLogs\DB\{RepoStore,RunStore,EventStore,BranchStore,AuditLog}`.
  - `tests/stubs/public-keys-stub.php` — extended with the
    `list_for_user / add / delete` surface used by `/keys`.
- Added a `class_exists(__NAMESPACE__ . '\\X', false ) { return; }` guard at
  the top of every DB store class (mirroring the existing `PublicKeys`
  pattern), so the controllers' `require_once` calls become no-ops when a
  stub has already declared the class.
- `tests/run.php` now resets `__user_caps`, the user identity globals, and
  every DB stub between tests for full isolation.

## New tests (30)
- `test-rest-repos.php` (5): create + audit lane (wp_session vs ed25519),
  invalid slug rejection, idempotent upsert, archived filter.
- `test-rest-runs.php` (10): run create with audit, unknown slug 404,
  short-SHA rejection, list (slug required + repo lookup),
  list-recent, fetch 404, append/read events round-trip with severity
  counters, bad-body rejection, finalize success + audit, finalize
  invalid-status rejection.
- `test-rest-events.php` (6): first-call run materialisation + repo derivation
  from URL, `Final=true` with errors → `failed` (exit 1), without errors →
  `succeeded`, bad-JSON `GL-EVENTS-BAD-JSON`, missing-fields
  `GL-EVENTS-MISSING-FIELDS`, existing `RunId` skips repo creation.
- `test-rest-whoami-keys-audit.php` (9):
  whoami lane reporting (wp_session/ed25519), keys add→list→delete,
  delete-unknown 404, bad pubkey length 400, per-user isolation, audit
  admin-gate WP_Error, admin filtered-by-action listing, limit clamp.

## Result
```
Tests: 48 | Passed: 48 | Failed: 0 | Assertions: 106
```
(18 prior auth tests + 30 new REST controller tests, all green under PHP 8.2.)

The existing `.github/workflows/ci-wp-plugin.yml` matrix automatically picks
up the new tests across PHP 8.1–8.4.

## Files changed
- new: `git-logs-plugin/tests/stubs/wp-rest-stubs.php`
- new: `git-logs-plugin/tests/stubs/db-stubs.php`
- new: `git-logs-plugin/tests/test-rest-repos.php`
- new: `git-logs-plugin/tests/test-rest-runs.php`
- new: `git-logs-plugin/tests/test-rest-events.php`
- new: `git-logs-plugin/tests/test-rest-whoami-keys-audit.php`
- edited: `git-logs-plugin/tests/bootstrap.php`
- edited: `git-logs-plugin/tests/run.php`
- edited: `git-logs-plugin/tests/stubs/public-keys-stub.php` (extended REST surface)
- edited: `git-logs-plugin/includes/db/class-{repo,run,event,branch,audit-log}*.php`
  (added `class_exists` guard, mirroring `PublicKeys`)
