# WP-CLI Reference (v2)

**Version:** 2.5.0  
**Updated:** 2026-04-25

Consolidated catalog of every `wp git-logs *` subcommand. Each command lives in `inc/Cli/<Command>Command.php` and is registered via `inc/Cli/Registrar.php` on the `cli_init` hook.

---

## Subcommand index

| Subcommand | Purpose | Spec source |
|------------|---------|-------------|
| `prune`    | Delete old log/error rows; optional pipeline sweep | §22 |
| `backup`   | Hot-copy SQLite via Online Backup API + manifest    | §23 |
| `restore`  | Restore from a backup file with safety checks       | §23 |
| `verify`   | Integrity + FK + Profile + migration parity check   | §23, §20 |
| `bootstrap`| Force-show first-run bootstrap form (admin-only)    | §03 |
| `migrate`  | Force-run pending migrations (idempotent)           | §06 |
| `config`   | Read/write `ConfigKv` keys                          | §10 |
| `prune-counters` | Reset transient metric counters               | §20 |
| `seed-test` | Emit fake Pipelines + log lines for screenshots    | §26 |

---

## Common conventions

- Every command accepts `--url=<site>` (multisite) and standard WP-CLI flags (`--quiet`, `--debug`, etc).
- Exit codes are uniform:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Validation / argument error |
| 2 | Resource busy (DB lock, migration running) |
| 3 | Operator abort (SIGINT) |
| 4 | Refused by safety check (e.g. downgrade restore) |
| 10 | Unexpected error (stack written to WP error log) |

- Every command emits an `AuditTrail` row when it mutates state. Read-only commands (`verify`, `config get`, `prune --dry-run`) do not.

---

## `wp git-logs prune`

Delete `LogEntry` and `ErrorLogEntry` rows older than the cutoff. See §22 for full semantics.

```
wp git-logs prune \
  --older-than=<duration>     # required; e.g. 30d, 12w, 6mo, 1y; floor 7d
  [--include-errors]          # also prune lines from HasError pipelines
  [--include-pipelines]       # phase-2: drop now-empty Pipeline rows
  [--app=<AppSlug>]           # scope to one App
  [--repo=<RepoUrl>]          # scope to one Repo
  [--dry-run]
  [--batch=<n>]               # default 1000
```

Refused while a migration is pending (`MigrationState.PluginVersion != ConfigKv.PluginVersion`) → exit 4.

---

## `wp git-logs backup`

```
wp git-logs backup \
  --to=<path>                 # required; absolute path
  [--checkpoint]              # PRAGMA wal_checkpoint(TRUNCATE) before copy (recommended)
  [--gzip]                    # gzip after copy; manifest stays uncompressed
```

Writes `<path>` plus `<path>.json` manifest. See §23 for manifest schema.

---

## `wp git-logs restore`

```
wp git-logs restore \
  --from=<path>               # required
  [--force]                   # bypass maintenance-mode + schema-checksum checks
```

Pre-flight:
1. `ConfigKv.MaintenanceMode = '1'` required (or `--force`).
2. `PRAGMA integrity_check` on source.
3. Manifest `SchemaChecksum` must match (or `--force`).
4. Major-version downgrade → exit 4 always (no override).

Post-restore: runs migrator + `verify` automatically.

---

## `wp git-logs verify`

Read-only. Runs every check from §23 + §20:

```
wp git-logs verify [--format=table|json|yaml]
```

Output rows: integrity_check, foreign_key_check, profile_count, migration_parity, latest_audit_event. Exit 1 on any failure with the failing check name.

---

## `wp git-logs bootstrap`

Force-renders the first-run bootstrap form for the current admin user. Useful when:
- `Profile` table is non-empty but operator wants to create an additional Admin Profile via the same one-time-credential flow.
- Recovering from a deleted-last-Profile situation without going through the UI.

```
wp git-logs bootstrap [--print-credentials]
```

`--print-credentials` writes the generated `TempToken` + `Token` to stdout — required because there is no UI session to display them. Treat stdout as sensitive.

---

## `wp git-logs migrate`

```
wp git-logs migrate [--dry-run]
```

Runs every `inc/Migrations/V*_*_*` whose `PluginVersion` is not yet in `MigrationState`. Idempotent. Useful when admin has not visited the plugin page and operator wants to apply pending migrations explicitly (e.g. after a `composer install` deploy).

---

## `wp git-logs config`

Read/write `ConfigKv` rows.

```
wp git-logs config get <KeyName>
wp git-logs config set <KeyName> <ValueText>
wp git-logs config list [--format=table|json]
wp git-logs config delete <KeyName>      # only for non-required keys
```

Required keys (`PluginVersion`, `LogLevelMin`, `RatePerMinPerProfile`, `MaxPushPayloadBytes`, `MaxLinesPerPush`, `MaxLineBytes`) cannot be deleted — `delete` returns exit 1.

---

## `wp git-logs prune-counters`

Reset the in-process metric transients (counters surfaced by `/metrics`). Useful before a benchmark run.

```
wp git-logs prune-counters [--yes]
```

`--yes` skips the confirmation prompt.

---

## `wp git-logs seed-test`

Emit fake data for screenshot generation (§26). Refuses to run if `Profile` count > 0 unless `--allow-non-empty`.

```
wp git-logs seed-test \
  [--profiles=3] [--git-profiles=2] [--apps=4] \
  [--pipelines=6] [--log-lines=50] \
  [--allow-non-empty]
```

Generated rows are tagged with `AuditTrail.Detail.SeedRun=true` so operators can purge them later via `prune --include-pipelines` scoped to seed apps.

---

## Adding a new subcommand

1. Create `inc/Cli/<Name>Command.php` implementing `__invoke`.
2. Register in `inc/Cli/Registrar.php`.
3. Append a row to the index above + a section here.
4. Add an integration test under `tests/Integration/Cli/`.
5. Bump `98-changelog.md`.
