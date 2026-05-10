# CLI Test Plan (v2)

**Version:** 2.7.1  
**Updated:** 2026-04-27  
**Scope:** End-to-end test strategy for the WP-CLI surface (`wp git-logs *`) and the PHP code that backs it. Provider-agnostic stages with a GitHub Actions reference implementation.

---

## Goals

1. Catch regressions in `wp git-logs` subcommands before they reach WP.org.
2. Lock the **canonical signing string** (§31) and **validation order** (§05) under automated assertion — these are the spec's load-bearing contracts.
3. Verify schema migrations across the supported PHP × WP matrix without human re-runs.
4. Keep failures debuggable from CI logs alone (no "works on my machine" round trips).
5. Stay portable: stages described abstractly so GitLab CI, CircleCI, Jenkins can adopt without rewriting tests.

---

## Non-goals

- UI/visual regression of the WP admin pages (deferred; would need Playwright + a hosted WP).
- Fuzz/property testing of the JSON parser (covered by PHP core).
- Performance benchmarks (D4 in §30 — separate effort).

---

## Two-layer test architecture

| Layer | Tool | What it owns | Where it runs |
|-------|------|--------------|---------------|
| **Unit** | PHPUnit | Pure PHP: mappers, validators, signing-string builder, ErrorResponder, ConfigKv loader, seed loader | `tests/phpunit/` next to `inc/` |
| **CLI smoke** | Bats | Real `wp git-logs` invocations against a live ephemeral WP install with an in-memory plugin DB | `tests/bats/` |

This split intentionally matches §13-generic-cli/§12-testing principle: unit tests live next to source, integration tests live in a dedicated `tests/` directory.

---

## Test matrix

12 combinations per push to `main`; 3 combinations on PR (PHP latest × WP latest × { single, multisite, sqlite-only }).

| Axis | Values |
|------|--------|
| PHP | 8.1, 8.2, 8.3 |
| WordPress | latest (6.x), previous (6.x − 1) |
| Mode | single-site, multisite |

Total = 3 × 2 × 2 = 12 jobs. Multisite jobs run a reduced Bats suite (multisite-specific flows only); unit suite runs unchanged.

---

## Provider-agnostic stages

Every test run progresses through these stages in order. A failed stage stops the pipeline; a stage MUST emit machine-readable status to its CI's native format (annotations, junit, etc.) but the stage definition itself is portable.

| # | Stage | Purpose | Inputs | Outputs |
|---|-------|---------|--------|---------|
| 1 | **Preflight** | Validate runner has required binaries: `php`, `composer`, `wp`, `bats`, `jq`, `ssh-keygen`, `sqlite3`. Print versions. Fail fast on any missing tool. | runner image | `preflight.txt` |
| 2 | **Setup** | Provision throwaway WP install at `/tmp/wp-test`. Install + activate the plugin from the workspace. Run activator (seeds + migrations). | plugin tarball, WP version | `wp-cli.yml`, fixture WP at `/tmp/wp-test` |
| 3 | **Build** | Composer install (no-dev for prod sanity check, then dev for tests). Static analyze (`phpstan --level=max`). Lint (`phpcs` against WP coding standards, plugin-relevant subset). | source tree | `vendor/`, `phpstan.json`, `phpcs.json` |
| 4 | **Unit** | `vendor/bin/phpunit --testsuite=plugin --log-junit junit.xml`. Coverage report optional. | built source | `junit.xml`, `coverage.xml` |
| 5 | **Integration** | `bats tests/bats/` against the fixture WP. Each `.bats` file represents one `wp git-logs` subcommand or one HTTP endpoint. | fixture WP, plugin source | `bats.tap` |
| 6 | **Verify** | Schema introspection: `sqlite3 wp-content/uploads/git-logs/db.sqlite '.schema'` diffed against `tests/fixtures/expected-schema.sql`. Seed introspection: row counts per lookup table match §16. ConfigKv defaults present. | fixture DB | `schema.diff`, `seeds.diff` |
| 7 | **E2E** | Full SSH push → query → fixed-log round-trip using a real ephemeral SSH key. Asserts §31 happy path AND every GL-SSH-* error code at least once. | fixture WP + signing key | `e2e.tap` |

Stages 1–4 run in parallel across matrix legs; 5–7 run sequentially within each leg (need the fixture WP).

---

## Bats layer (CLI smoke)

### Layout

```
tests/bats/
├── helpers/
│   ├── load.bash            # source common helpers, exit-on-undefined-var
│   ├── wp.bash              # `wp_eval`, `wp_db_query` wrappers
│   ├── ssh.bash             # generate keypair, build canonical signing string, curl wrapper
│   └── assert.bash          # `assert_eq`, `assert_json_eq`, `assert_audit_row`
├── fixtures/
│   ├── expected-schema.sql  # canonical CREATE TABLE statements (used in Verify stage)
│   └── payloads/
│       ├── append-happy.json
│       └── append-malformed.json
├── 00-bootstrap.bats        # plugin activates cleanly, MigrationState=2.7.0
├── 10-profile-crud.bats     # wp git-logs profile create/list/show/delete
├── 11-gitprofile-crud.bats
├── 12-repo-crud.bats
├── 13-app-crud.bats
├── 20-ssh-key-register.bats # wp git-logs ssh-key add/list/disable/rotate
├── 21-ssh-sign-verify.bats  # signing-string builder matches what server expects
├── 30-append-log-temptoken.bats
├── 31-append-log-ssh.bats
├── 32-fixed-log-ssh.bats
├── 33-clear-log-ssh.bats
├── 40-error-codes.bats      # every GL-* code reachable via crafted input
├── 50-config-kv.bats        # wp git-logs config get/set + SshAuthMode gating
├── 60-uninstall.bats        # UninstallMode=keep-data | drop-tables | drop-db
└── 99-multisite.bats        # only loaded when WP is multisite
```

### Conventions

- One `@test` per assertion; no shared mutable state across tests in a file (each `setup` re-creates the fixture row).
- Helpers MUST be sourced via `load 'helpers/load'`; never source by relative path.
- `wp_db_query 'SELECT …'` returns TSV; tests parse with `cut`/`awk`, not `jq` (faster for tabular).
- Each `.bats` file MUST set `bats_require_minimum_version 1.5.0` to guarantee `--filter` semantics.
- A test that exercises an SSH endpoint MUST clean up its `SshNonce` rows in `teardown` (replay-window pollution).

### Example assertion shape (illustrative, not implementation)

```bats
@test "append-log SSH happy path writes Audit + LogEntry + History" {
  ssh_register_key_for_repo "$REPO_ID" my-key
  payload=$(cat fixtures/payloads/append-happy.json)
  signed=$(ssh_sign_request POST /wp-json/git-logs/v2/append-log "$payload")

  run curl_signed "$signed"
  assert_eq "$status" 0
  assert_json_eq "$output" '.Status' 'Success'

  assert_audit_row 'SshAuthSuccess' "$REPO_ID"
  assert_db_count "LogEntry WHERE PipelineId=$(last_pipeline_id)" 3
  assert_db_count "History WHERE RepoVersionId=$(repo_version_id) AND ActionTypeId=1" 1
}
```

---

## PHPUnit layer (unit)

### Layout

```
tests/phpunit/
├── bootstrap.php                     # autoload, in-memory SQLite, run migrations + seeds
├── phpunit.xml.dist                  # testsuite=plugin, coverage filter on inc/
├── Db/
│   └── ConnectionTest.php            # prepared-statement enforcement, FK pragma on
├── Auth/
│   ├── TempTokenValidatorTest.php    # validation order steps 1–8 (one test per step)
│   └── SshSignatureValidatorTest.php # canonical signing string + namespace + verify
├── Mappers/
│   ├── RepoUrlParserTest.php         # provider/owner/repo/versionSuffix split
│   └── LogLineMapperTest.php
├── Migrations/
│   ├── ActivatorTest.php             # idempotent on second run, MigrationState row written
│   └── SeedLoaderTest.php            # §16 row counts, INSERT OR IGNORE preserves edits
├── Config/
│   └── ConfigKvTest.php              # defaults loaded, admin edits not overwritten
├── Logging/
│   └── RedactorTest.php              # TempToken/Token/Fingerprint redacted in error_log
└── Support/
    └── ErrorResponderTest.php        # every GL-* code maps to documented HttpStatus
```

### What each test owns

| Class under test | What is asserted |
|------------------|------------------|
| `RepoUrlParser` | `(provider, owner, repoName, versionSuffix)` for 12+ URL shapes incl. `.git`, no-`.git`, `-vN`, trailing slash, SSH form. |
| `TempTokenValidator` | Each step (2–7) exits with the documented `GL-*` code; later steps not reached on early failure. |
| `SshSignatureValidator` | Canonical string byte-equality with `tests/fixtures/canonical-strings/*.txt`; verify passes for known-good fixture; fails on body byte change, namespace change, timestamp skew, nonce reuse. |
| `Activator` | Two consecutive runs leave one row per lookup value; `MigrationState.PluginVersion='2.7.0'` after run. |
| `SeedLoader` | Admin-edited `ConfigKv.SshAuthMode='required'` survives a second seed pass. |
| `ErrorResponder` | Map of `GL-*` → HttpStatus matches §15 verbatim (data-driven from a fixture). |
| `Redactor` | Substrings `TempToken=`, `Token=`, `X-GL-Signature:` removed from any string passed to `error_log`. |

### Bootstrap rules

- One in-memory SQLite per test (`new SQLite3(':memory:')`); never share a DB across tests.
- Migrations + seeds run in `setUp()` via the same loader the activator uses (no parallel "test schema" file — keeps spec-of-truth singular).
- WP core is **not** loaded for unit tests; the plugin's `inc/` namespace is autoloaded standalone. This forces the PHP code to be WP-decoupled at the layer being tested (mappers/validators/parsers).

---

## E2E SSH round-trip (Stage 7)

Single Bats file `tests/bats/e2e-ssh-roundtrip.bats` that:

1. Generates a fresh ed25519 keypair in `$BATS_TMPDIR`.
2. Registers public key against a fixture Repo via `wp git-logs ssh-key add`.
3. Captures the assigned `SshKeyId` and `Fingerprint`.
4. Runs the §28 SSH workflow steps locally (signing string, `ssh-keygen -Y sign`, curl with all 5 SSH headers).
5. Asserts:
   - `Status=Success`, `PipelineId` returned.
   - `AuditTrail` has one `SshAuthSuccess` row with the right `RouteName` and `ActorIp=127.0.0.1`.
   - `SshKey.LastUsedAt` updated to within 5s of test start.
6. Repeats the request with the same nonce → expects `GL-SSH-NONCE-REUSED`.
7. Tampers one byte in the body, re-signs the **original** string → expects `GL-SSH-SIGNATURE-INVALID`.
8. Sets `X-GL-Timestamp` to `now-3600` → expects `GL-SSH-TIMESTAMP-SKEW`.
9. Disables the key (`wp git-logs ssh-key disable`) → expects `GL-SSH-KEY-INACTIVE`.
10. Tears down: deletes the key, prunes `SshNonce`.

Steps 6–9 collectively guarantee every SSH-lane GL-* code from §15 is exercised at least once per CI run.

---

## Failure-handling rules

- **Flaky test ⇒ quarantine, not retry.** Move the `@test` to `tests/bats/quarantine/` with a tracking comment of the form `# QUARANTINE(<issue-ref>): <reason>` (e.g., `# QUARANTINE(GH-142): race in CI runner`). The tracking-comment format is mandatory so `linter-scripts/check-quarantine-tracking.py` (Phase 39b) can verify every quarantined test references a real issue. Quarantine directory is run with `--no-tempdir-cleanup` and reports as warning, not failure.
- **Seed mismatch in Verify stage ⇒ build red.** Never auto-update `expected-schema.sql`; the spec drives the schema, not the test fixture.
- **Skipped tests must be visible.** `bats` `skip "reason"` allowed only with a JIRA/issue reference in the reason string.

---

## CI provider mapping

The spec is provider-agnostic. The ships-with implementation is GitHub Actions; one `ci.yml` (separate spec file) maps stages 1–7 to jobs. Other providers can re-use the stage names verbatim.

| Stage | GitHub Actions job key | GitLab CI stage | CircleCI workflow step |
|-------|-----------------------|-----------------|------------------------|
| 1 Preflight | `preflight` | `preflight` | `preflight` |
| 2 Setup | `setup` | `setup` | `setup` |
| 3 Build | `build` (matrix) | `build` (parallel) | `build` |
| 4 Unit | `unit` (matrix) | `test:unit` | `unit` |
| 5 Integration | `integration` (matrix) | `test:integration` | `integration` |
| 6 Verify | `verify` (matrix) | `verify` | `verify` |
| 7 E2E | `e2e` (matrix) | `e2e` | `e2e` |

---

## Cross-references

- §05 — validation order under test (TempToken steps + SSH steps).
- §15 — error codes the test suite asserts, one per GL-*.
- §16 — seed data validated by Stage 6.
- §28 — workflow snippet that the E2E stage replays in Bats.
- §31 — canonical signing string under test.
- §13-generic-cli/§12-testing — parent testing philosophy (unit-near-source, integration-in-tests/).
- §33 — Bats skeleton (next file).
- §34 — PHPUnit skeleton (next file).
- §35 — reference `ci.yml` (next file).
