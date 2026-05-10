# Bats Test Skeleton (v2)

**Version:** 2.7.0  
**Updated:** 2026-04-25  
**Scope:** Authoritative skeleton for the Bats CLI smoke layer described in §32 stages 5 + 7. Defines directory layout, helper contracts, fixture conventions, and one canonical `.bats` example per category. Does NOT contain implementation — every block is a contract another spec or implementer fills in.

---

## Why Bats (recap from §32)

- Pure-shell tests stay readable in raw CI logs (no JSON test runner output to decode).
- Invokes the real `wp` binary against a real ephemeral WP install — catches regressions PHPUnit can't (CLI flag parsing, output formatting, exit codes).
- Trivial to add new tests: drop a new `*.bats` file, no test-discovery boilerplate.

---

## Directory layout (authoritative)

```
tests/bats/
├── helpers/
│   ├── load.bash               # MUST be sourced first by every .bats file
│   ├── env.bash                # exports BATS_GL_*, fixture paths
│   ├── wp.bash                 # wp_eval, wp_db_query, wp_run_capture
│   ├── ssh.bash                # ssh_keygen_eph, ssh_sign_request, curl_signed
│   ├── http.bash               # curl wrappers w/ TraceId capture
│   ├── db.bash                 # sqlite3 helpers, assert_db_count, assert_audit_row
│   ├── assert.bash             # assert_eq, assert_neq, assert_json_eq, assert_error_code
│   └── trace.bash              # capture+print TraceId on failure (debuggability)
├── fixtures/
│   ├── expected-schema.sql     # diffed in §32 Stage 6 Verify
│   ├── seed-counts.tsv         # one row per lookup table: name<TAB>expected_count
│   ├── canonical-strings/
│   │   ├── append-log.txt      # byte-exact §31 GL-SSHSIG-V1 string for the matching payload
│   │   └── fixed-log.txt
│   └── payloads/
│       ├── append-happy.json
│       ├── append-malformed.json
│       ├── fixed-happy.json
│       └── clear-happy.json
├── 00-bootstrap.bats
├── 10-profile-crud.bats
├── 11-gitprofile-crud.bats
├── 12-repo-crud.bats
├── 13-app-crud.bats
├── 20-ssh-key-register.bats
├── 21-ssh-sign-verify.bats
├── 30-append-log-temptoken.bats
├── 31-append-log-ssh.bats
├── 32-fixed-log-ssh.bats
├── 33-clear-log-ssh.bats
├── 40-error-codes.bats
├── 50-config-kv.bats
├── 60-uninstall.bats
├── 99-multisite.bats
├── e2e-ssh-roundtrip.bats      # Stage 7 only
└── quarantine/                 # flaky tests parked here; warn-only
```

File-number prefix encodes ordering hint, not strict dependency. Bats runs them in lexicographic order by default; `--filter` cherry-picks.

---

## Helper contracts

Every helper MUST be a function in `helpers/*.bash`. No top-level side effects. Sourced once per `.bats` file via:

```bash
load 'helpers/load'
```

`helpers/load.bash` is the only file Bats files load by name; it transitively sources the rest.

### `helpers/env.bash`

Exports (all `readonly` after first set):

| Variable | Purpose | Default |
|----------|---------|---------|
| `BATS_GL_WP_PATH` | Fixture WP root | `/tmp/wp-test` |
| `BATS_GL_BASE_URL` | REST root | `http://localhost:8080/wp-json/git-logs/v2` |
| `BATS_GL_DB_PATH` | SQLite file | `$BATS_GL_WP_PATH/wp-content/uploads/git-logs/db.sqlite` |
| `BATS_GL_TMPDIR` | Per-test scratch | `${BATS_TEST_TMPDIR}` |
| `BATS_GL_NAMESPACE` | SSH sign namespace | `git-logs@v2` (locked by §31) |

### `helpers/wp.bash`

| Function | Contract |
|----------|----------|
| `wp_eval <php-snippet>` | Runs `wp eval` against fixture WP. Echoes stdout. Non-zero exit → test fails. |
| `wp_db_query <sql>` | Runs `sqlite3 -separator $'\t' "$BATS_GL_DB_PATH" "<sql>"`. TSV stdout. |
| `wp_run_capture <args...>` | Runs `wp <args>` and captures stdout, stderr, exit code into `$WP_OUT`, `$WP_ERR`, `$WP_RC`. |
| `wp_reset_fixture` | Drops + re-creates plugin DB; re-runs activator. Used in `setup_file`. |

### `helpers/ssh.bash`

| Function | Contract |
|----------|----------|
| `ssh_keygen_eph <label>` | `ssh-keygen -t ed25519 -f $BATS_GL_TMPDIR/<label>` (no passphrase). Echoes path to private half. |
| `ssh_fingerprint <key-path>` | Echoes `SHA256:…` line from `ssh-keygen -lf`. |
| `ssh_register_key_for_repo <repo-id> <key-pub-path> [label]` | Calls `wp git-logs ssh-key add`. Echoes `SshKeyId`. |
| `ssh_canonical_string <method> <path> <ts> <nonce> <body-file>` | Builds the §31 GL-SSHSIG-V1 string, echoes it (LF-joined, no trailing newline). |
| `ssh_sign_request <method> <path> <body-file> <key-priv-path>` | Generates fresh `ts` + `nonce`, builds canonical string, runs `ssh-keygen -Y sign -n $BATS_GL_NAMESPACE`. Exports `SIG_TS`, `SIG_NONCE`, `SIG_FP`, `SIG_BLOB`. |
| `curl_signed <url> <method> <body-file>` | POSTs with the 5 SSH headers using current `SIG_*`. Echoes response body; exits 0 on 2xx, non-zero otherwise. |

### `helpers/db.bash`

| Function | Contract |
|----------|----------|
| `assert_db_count <where-clause> <expected>` | Fails with diff if `SELECT COUNT(*) FROM <where>` ≠ expected. |
| `assert_audit_row <action-name> [where-extra]` | Asserts at least one `AuditTrail` row with `AuditActionType.Name = ?` (and optional extra WHERE). |
| `last_pipeline_id` | Echoes `MAX(PipelineId)` — for chaining tests. |
| `prune_ssh_nonces` | `DELETE FROM SshNonce` — call in `teardown` of any SSH test. |

### `helpers/assert.bash`

| Function | Contract |
|----------|----------|
| `assert_eq <expected> <actual> [msg]` | Plain string equality. |
| `assert_json_eq <json-string> <jq-path> <expected>` | `jq -r <path>` from `<json-string>` must equal `<expected>`. |
| `assert_error_code <json-string> <code>` | `.ErrorCode` must equal `<code>` (per §15 envelope). |
| `assert_status <expected-rc>` | Asserts `$status` equals expected (Bats run-result var). |

### `helpers/trace.bash`

Single function `print_trace_on_fail` MUST be wired into every file's `teardown`:

```bash
teardown() {
  if [[ "$BATS_TEST_COMPLETED" -ne 1 ]]; then
    print_trace_on_fail
  fi
}
```

It dumps: last response body, last canonical signing string, last 10 `AuditTrail` rows, last 10 `SshNonce` rows. Makes red builds debuggable from CI logs alone (per §32 goal #4).

---

## File template

Every `.bats` file MUST follow this skeleton:

```bash
#!/usr/bin/env bats
bats_require_minimum_version 1.5.0
load 'helpers/load'

setup_file() {
  wp_reset_fixture
  # any one-time fixture rows (Profile, GitProfile, Repo) for this file
}

setup() {
  # per-test fresh state if needed
  :
}

teardown() {
  prune_ssh_nonces  # only in SSH-touching files
  print_trace_on_fail
}

# --- tests below this line ---

@test "DESCRIPTION" {
  # arrange
  # act
  # assert
  :
}
```

Rules:
- Exactly one `@test` per assertion outcome (no chained "and also" assertions).
- Test descriptions in present tense, ≤80 chars: `@test "append-log SSH happy path returns Success"`.
- No `sleep` in any test. If timing matters, poll with a bounded `for i in $(seq 1 N)` loop.
- No network beyond `localhost`. The fixture WP serves on `localhost:8080`; nothing else allowed.

---

## Canonical examples (one per category)

Below are spec-level shapes — implementers expand into runnable files. Each is intentionally minimal to lock the contract, not the implementation.

### `00-bootstrap.bats` — plugin activates and seeds correctly

```bats
@test "plugin activates without error" {
  wp_run_capture plugin activate git-logs
  assert_status 0
}

@test "MigrationState records 2.7.0 after activation" {
  run wp_db_query "SELECT PluginVersion FROM MigrationState ORDER BY MigrationStateId DESC LIMIT 1"
  assert_eq "2.7.0" "$output"
}

@test "all lookup tables seeded with the §16 row counts" {
  while IFS=$'\t' read -r table expected; do
    run wp_db_query "SELECT COUNT(*) FROM $table"
    assert_eq "$expected" "$output" "table=$table"
  done < fixtures/seed-counts.tsv
}

@test "ConfigKv defaults present (SshAuthMode=optional, ReplayWindowSeconds=300)" {
  run wp_db_query "SELECT KeyName,ValueText FROM ConfigKv WHERE KeyName IN ('SshAuthMode','ReplayWindowSeconds') ORDER BY KeyName"
  assert_eq $'ReplayWindowSeconds\t300\nSshAuthMode\toptional' "$output"
}
```

### `21-ssh-sign-verify.bats` — canonical signing string is byte-exact

```bats
@test "canonical signing string for append-log matches fixture" {
  local body=fixtures/payloads/append-happy.json
  local got
  got=$(ssh_canonical_string POST /wp-json/git-logs/v2/append-log 1745568000 'fixed-nonce-AAAA' "$body")
  local want
  want=$(cat fixtures/canonical-strings/append-log.txt)
  assert_eq "$want" "$got"
}
```

> The fixture file `canonical-strings/append-log.txt` is the **spec-of-truth** byte string. PHP server code, Bats, and PHPUnit all compare against it. Any change to §31 must update this file in the same commit.

### `31-append-log-ssh.bats` — happy path + audit row

```bats
@test "append-log SSH happy path writes Success + audit + log entries" {
  local key
  key=$(ssh_keygen_eph k1)
  local kid
  kid=$(ssh_register_key_for_repo "$REPO_ID" "${key}.pub" k1)

  ssh_sign_request POST /wp-json/git-logs/v2/append-log fixtures/payloads/append-happy.json "$key"
  run curl_signed "$BATS_GL_BASE_URL/append-log" POST fixtures/payloads/append-happy.json
  assert_status 0
  assert_json_eq "$output" '.Status' 'Success'

  assert_audit_row 'SshAuthSuccess'
  assert_db_count "LogEntry WHERE PipelineId=$(last_pipeline_id)" 3
}
```

### `40-error-codes.bats` — every GL-* reachable

One `@test` per code in §15. Skeleton (only two shown; full file enumerates all):

```bats
@test "GL-SSH-HEADER-MISSING when X-GL-Signature absent" {
  ssh_sign_request POST /wp-json/git-logs/v2/append-log fixtures/payloads/append-happy.json "$KEY"
  unset SIG_BLOB
  run curl_signed "$BATS_GL_BASE_URL/append-log" POST fixtures/payloads/append-happy.json
  assert_error_code "$output" 'GL-SSH-HEADER-MISSING'
}

@test "GL-SSH-NONCE-REUSED on second submit with same nonce" {
  ssh_sign_request POST /wp-json/git-logs/v2/append-log fixtures/payloads/append-happy.json "$KEY"
  curl_signed "$BATS_GL_BASE_URL/append-log" POST fixtures/payloads/append-happy.json >/dev/null
  run curl_signed "$BATS_GL_BASE_URL/append-log" POST fixtures/payloads/append-happy.json
  assert_error_code "$output" 'GL-SSH-NONCE-REUSED'
}
```

### `50-config-kv.bats` — `SshAuthMode=required` rejects TempToken

```bats
@test "SshAuthMode=required returns GL-AUTH-LANE-DISABLED for TempToken submission" {
  wp_run_capture git-logs config set SshAuthMode required
  run curl -sS -X POST "$BATS_GL_BASE_URL/append-log" \
    -H 'Content-Type: application/json' \
    --data-binary @fixtures/payloads/append-temptoken.json
  assert_error_code "$output" 'GL-AUTH-LANE-DISABLED'
}
```

### `60-uninstall.bats` — UninstallMode contract

```bats
@test "UninstallMode=keep-data preserves SQLite file after deactivation" { : }
@test "UninstallMode=drop-tables removes plugin tables but keeps SQLite file" { : }
@test "UninstallMode=drop-db deletes the SQLite file entirely" { : }
@test "every uninstall path writes one PluginUninstall AuditTrail row before teardown" { : }
```

### `99-multisite.bats` — site isolation

Loaded only when `wp_eval 'echo is_multisite();'` returns `1`. Otherwise the file calls `skip "single-site run"` in `setup_file`.

```bats
@test "each site has its own SQLite file under uploads/git-logs/<blog-id>/" { : }
@test "Profile created on site A is invisible to site B" { : }
```

---

## Fixture file rules

- `expected-schema.sql` — concatenation of `CREATE TABLE …` and `CREATE INDEX …` in the order the activator emits them. Generated by running the activator against a fresh DB and dumping `.schema`. **Never hand-edited.** Updated only when §02 changes; the diff is part of the §02 PR.
- `seed-counts.tsv` — one line per lookup table: `<TableName>\t<row-count>`. Derived from §16. Updated when §16 changes.
- `canonical-strings/*.txt` — byte-exact GL-SSHSIG-V1 strings. Lines joined with LF (`\n`), no trailing newline. The matching payload JSON in `payloads/` MUST hash to the digest embedded in the canonical string.
- All fixtures committed; never generated at test time except via the dedicated regenerate script (`tests/bats/regen-fixtures.sh`, called manually, never in CI).

---

## Coverage targets

- **Every `wp git-logs <subcommand>` MUST have at least one happy-path `@test` and at least one rejection `@test`.**
- **Every GL-* code in §15 MUST be reachable by exactly one `@test` in `40-error-codes.bats`.** Build fails if `40-error-codes.bats` test count < count of rows in §15.
- **Every step in §31 SSH validation order MUST have at least one `@test` in `e2e-ssh-roundtrip.bats` that hits its failure branch.**

A small CI helper (`tests/bats/coverage-check.sh`) counts assertions vs. spec rows and fails Stage 5 if the coverage contract is violated.

---

## Cross-references

- §32 — overall test plan and stage definitions.
- §15 — error-code catalog driving the `40-error-codes.bats` enumeration.
- §16 — seed data driving `seed-counts.tsv`.
- §31 — canonical signing string under fixture lock.
- §34 — PHPUnit skeleton (companion file).
- §35 — reference `ci.yml` that wires `bats tests/bats/` into Stage 5.
