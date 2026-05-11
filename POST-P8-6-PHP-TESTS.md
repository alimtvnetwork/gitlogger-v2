# Post-P8 #6 — WP Plugin PHPUnit-Lite Harness

## Why
The plugin's auth surface (Ed25519 verification + replay protection + lane dispatch)
had zero automated tests. Live integration (Post-P8 #2) is still blocked on
operator infra, so this pass shrinks the coverage gap with isolated unit tests
that run under plain `php` — no WordPress install, no DB, no PHPUnit dependency.

## Delivered
- **`tests/bootstrap.php`** — minimal WP shim: `WP_Error`, `WP_REST_Request`,
  in-memory `get_transient`/`set_transient`, `wp_unslash`, `wp_set_current_user`,
  `is_user_logged_in`, `is_wp_error`, `__()`, `get_current_user_id`. Loads the
  in-memory `PublicKeys` stub before the real auth classes.
- **`tests/stubs/public-keys-stub.php`** — namespaced in-memory key registry
  with `register/find_by_key_id/touch_last_used/reset` matching the real API.
- **`tests/run.php`** — PHPUnit-free runner. Discovers `test-*.php`, calls every
  global `test_*` function, resets transients + current user + key registry
  between tests. Provides `assertTrue/False/Same/Equals/WPError`.
- **`tests/test-nonce-store.php`** (3 tests) — first-use, replay detection,
  per-keyId scoping.
- **`tests/test-ed25519-resolver.php`** (10 tests) — happy path, empty-body
  hash, bad scheme, missing field, illegal nonce char, ±300s clock skew,
  replay via NonceStore, unknown keyId, sig length check, body-tamper +
  path-tamper signature failures.
- **`tests/test-auth-context.php`** (4 tests) — Lane 1 (logged-in cookie),
  no-creds 401, Lane 2 (Ed25519 header → wp_set_current_user), Lane 2 sig
  failure propagates `WP_Error`.
- **Plugin tweak**: added a `class_exists(..., false)` guard at the top of
  `includes/auth/class-public-keys.php` so tests can pre-load an in-memory
  stub. No-op in production (real WP load order is unchanged).
- **`.github/workflows/ci-wp-plugin.yml`** — runs the suite on PHP 8.1/8.2/8.3/8.4
  matrix plus a `php -l` syntax-lint sweep over every plugin file.

## Verification
```
$ php git-logs-plugin/tests/run.php
  ok   test_authctx_ed25519_bad_sig_propagates_wp_error
  ok   test_authctx_ed25519_header_routes_to_resolver
  ok   test_authctx_logged_in_user_passes
  ok   test_authctx_no_creds_returns_unauthorized
  ok   test_ed25519_bad_nonce_chars
  ok   test_ed25519_bad_scheme
  ok   test_ed25519_bad_sig_length
  ok   test_ed25519_clock_skew
  ok   test_ed25519_invalid_sig_when_body_tampered
  ok   test_ed25519_invalid_sig_when_path_tampered
  ok   test_ed25519_missing_field
  ok   test_ed25519_replay_rejected
  ok   test_ed25519_resolve_empty_body_uses_sha256_of_empty
  ok   test_ed25519_resolve_success_returns_user_id
  ok   test_ed25519_unknown_key
  ok   test_nonce_first_use_not_seen
  ok   test_nonce_replay_detected
  ok   test_nonce_scoped_per_key_id

Tests: 18 | Passed: 18 | Failed: 0 | Assertions: 22
```

## Not yet covered (deferred)
- REST controllers (`class-rest-events.php`, `class-rest-runs.php`, etc.) —
  need a heavier `WP_REST_Server` shim; better tackled with WP-CLI's official
  test scaffold once the repo grows a real `wp-env`/`docker` harness.
- `db/` storage layer — wpdb-bound; needs sqlite shim or live DB.
- `class-rest-admin-diagrams.php` capability matrix — covered indirectly via
  REST controller harness in a future pass.
