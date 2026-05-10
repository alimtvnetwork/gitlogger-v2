# Migrations and Logger (v2)

**Version:** 2.0.0  
**Updated:** 2026-04-25

---

## Migrations

### Storage of marker

Primary: `MigrationState` table (preferred — single source of truth, transactional).  
Fallback (if DB not yet writable on first boot): JSON file at `{wp-content}/uploads/git-logs/migration-state.json`. The fallback is reconciled into `MigrationState` once the table exists.

### Boot algorithm

```text
on plugin_loaded:
  current = read_plugin_version()              // from main plugin file header
  if MigrationState exists:
    if row(PluginVersion=current) exists: return    // skip
  run_migrations_for(current)                  // idempotent; wraps in tx
  insert MigrationState(PluginVersion=current, AppliedAt=now)
  emit AuditTrail(AuditActionType=MigrationRun, Outcome=Success)
```

### Rules

- One row per plugin version. New deploy → new version → new marker absent → migration runs once.
- Migrations must be idempotent (CREATE TABLE IF NOT EXISTS, ALTER guarded by pragma checks).
- Failures: do not insert marker; raise; log `MigrationRun` with `Outcome=Error`.
- Lookup tables (enums) are seeded inside the same migration transaction.

---

## Logger

### Levels

`Trace(10)` < `Debug(20)` < `Info(30)` < `Warn(40)` < `Error(50)` < `Fatal(60)`.

### Runtime configuration

- Stored in `ConfigKv` under `KeyName='LogLevelMin'`.
- Default: `Info`.
- Setting `LogLevelMin='Warn'` disables Info and Debug at runtime (and Trace).

### Writer

- Internal diagnostic logs go to `wp-content/uploads/git-logs/diagnostic-{YYYY-MM-DD}.log`.
- CI/CD log entries (LogEntry / ErrorLogEntry tables) are **separate** from diagnostic logs.

### Deduplication

- In-process LRU keyed by `(LevelId, MessageHash, Source)` with TTL 60s.
- If the same key reoccurs within TTL, increment a `RepeatCount` on the existing record instead of writing a new line.

### No-swallow rule

Every caught exception must be logged at `Error` or `Fatal` and re-raised or converted into a structured response. No silent `catch {}`.
