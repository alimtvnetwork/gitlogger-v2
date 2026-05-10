# Seed Data (v2)

**Version:** 2.7.2  
**Updated:** 2026-04-27  
**Scope:** Authoritative initial-row content for every lookup table and `ConfigKv` default. Loaded by the activator on fresh install and by `MigrationState` upgrade steps. Idempotent: every seed insert MUST use `INSERT OR IGNORE` keyed on the natural unique column (`Name` or `KeyName`).

---

## Conventions

- All `Id` values are **fixed** and stable across releases. New rows append at the next free `Id`. Removed rows are tombstoned (kept in DB) and deprecated here, never re-numbered.
- `Name` columns are PascalCase, matching the enum codes in §01.
- Seeds are version-gated: each block lists the plugin version that introduced it. The activator skips seeds whose introducing version ≤ `MigrationState.PluginVersion`.
- Cross-reference: enum semantics live in §01; this file only carries Id ↔ Name bindings + version provenance.

---

## UserStatus (introduced 2.0.0)

| Id | Name |
|----|------|
| 1 | Active |
| 2 | Suspended |
| 3 | Revoked |

---

## Role (introduced 2.0.0)

| Id | Name |
|----|------|
| 1 | Admin |
| 2 | Editor |

---

## Permission (introduced 2.0.0)

| Id | Name |
|----|------|
| 1 | AppCreate |
| 2 | AppView |
| 3 | AppModify |
| 4 | AppDelete |
| 5 | ProfileCreate |
| 6 | ProfileView |
| 7 | ProfileModify |
| 8 | ProfileDelete |
| 9 | GitProfileCreate |
| 10 | GitProfileView |
| 11 | GitProfileModify |
| 12 | GitProfileDelete |
| 13 | RepoView |
| 14 | RepoModify |
| 15 | RepoDelete |
| 16 | HistoryView |
| 17 | LogPush |

### RolePermission seed (introduced 2.0.0)

- **Admin** (RoleId=1): bound to **every** PermissionId 1–17.
- **Editor** (RoleId=2): bound to PermissionIds { 2, 3, 6, 10, 13, 14, 16 } (View + Modify scope, no destructive ops, no LogPush).

Seed insert idempotency uses unique `(RoleId, PermissionId)`.

---

## Provider (introduced 2.0.0)

| Id | Name |
|----|------|
| 1 | GitHub |
| 2 | GitLab |

---

## OwnerType (retired in v3.8.0)

> **Retired** — replaced by `GitProfile.IsOrganization` boolean (0/1). No seed rows; the `OwnerType` lookup table is dropped from §18 schema. Tombstone kept here so historical migrations and §01 glossary cross-refs still resolve.

---

## Acceptance (introduced 2.0.0)

| Id | Name |
|----|------|
| 1 | AcceptAllRepos |
| 2 | AcceptSelectedRepoOnly |
| 3 | AcceptSelectedRepoInAllVersions |

---

## AppStatus (introduced 2.0.0)

| Id | Name |
|----|------|
| 1 | Active |
| 2 | Disabled |
| 3 | Archived |

---

## AppLinkType (introduced 2.0.0)

| Id | Name |
|----|------|
| 1 | GitProfile |
| 2 | Repo |

---

## LogSeverity (introduced 2.0.0)

| Id | Name | Numeric |
|----|------|---------|
| 1 | Trace | 10 |
| 2 | Debug | 20 |
| 3 | Info | 30 |
| 4 | Warn | 40 |
| 5 | Error | 50 |
| 6 | Fatal | 60 |

---

## ActionType (introduced 2.0.0)

| Id | Name |
|----|------|
| 1 | Append |
| 2 | Fixed |
| 3 | Clear |
| 4 | ClearAll |

---

## AuditActionType

| Id | Name | Introduced |
|----|------|-----------|
| 1 | ProfileCreate | 2.0.0 |
| 2 | ProfileUpdate | 2.0.0 |
| 3 | ProfileDelete | 2.0.0 |
| 4 | GitProfileCreate | 2.0.0 |
| 5 | GitProfileUpdate | 2.0.0 |
| 6 | GitProfileDelete | 2.0.0 |
| 7 | RepoCreate | 2.0.0 |
| 8 | RepoUpdate | 2.0.0 |
| 9 | RepoDelete | 2.0.0 |
| 10 | AppCreate | 2.0.0 |
| 11 | AppUpdate | 2.0.0 |
| 12 | AppDelete | 2.0.0 |
| 13 | AppLinkChange | 2.0.0 |
| 14 | LogPush | 2.0.0 |
| 15 | LogQuery | 2.0.0 |
| 16 | AuthSuccess | 2.0.0 |
| 17 | AuthFail | 2.0.0 |
| 18 | MigrationRun | 2.0.0 |
| 19 | RoleAssignmentChange | 2.5.0 |
| 20 | ConfigKvUpdate | 2.5.0 |
| 21 | PluginUninstall | 2.7.0 |
| 22 | SshAuthSuccess | 2.7.0 |
| 23 | SshAuthFail | 2.7.0 |
| 24 | SshKeyRotated | 2.7.0 |
| 25 | ConfigChange | 2.8.0 |

> Ids 19–20 reflect rows already shipped in 2.5.0; listed here for completeness and migration order. Activator on a fresh install inserts 1–25 in one pass; upgrade from 2.6.x inserts 21–24, upgrade from 2.7.x inserts 25.

---

## AuditOutcome (introduced 2.0.0)

| Id | Name |
|----|------|
| 1 | Success |
| 2 | Rejected |
| 3 | Error |

---

## ConfigKv Defaults

Single-row settings consumed at runtime. Activator inserts only rows whose `KeyName` doesn't already exist (admin-edited values are preserved).

| KeyName | ValueText | Introduced | Purpose |
|---------|-----------|-----------|---------|
| LogLevelMin | `Info` | 2.0.0 | Minimum `LogSeverity` retained on `/append-log`. Set to `Warn` to drop Info/Debug. |
| AppendLineLimit | `5000` | 2.0.0 | Max `Lines[]` per `/append-log` call. Exceed → `GL-VALIDATION-LINE-LIMIT`. |
| MaxPushPayloadBytes | `1048576` | 2.5.0 | 1 MiB cap on POST body. Exceed → `GL-PAYLOAD-TOO-LARGE`. |
| MaintenanceMode | `0` | 2.5.0 | When `1`, all write endpoints respond `503 GL-DB-UNAVAILABLE`. |
| SshAuthMode | `optional` | 2.7.0 | Lane B gate ∈ { `optional`, `preferred`, `required` }. See §31. |
| ReplayWindowSeconds | `300` | 2.7.0 | SSH timestamp tolerance and `SshNonce` retention window. |
| SshNonceJanitorBatch | `100` | 2.7.0 | Rows pruned per request from `SshNonce`. |
| UninstallMode | `keep-data` | 2.7.0 | WP uninstaller behavior ∈ { `keep-data`, `drop-tables`, `drop-db` }. Determines whether `AuditTrail.PluginUninstall` is the last row written. |

---

## Tombstones

Removed seeds remain in the DB to preserve referential integrity but are documented here as deprecated:

| Table | Id | Name | Removed in | Replacement |
|-------|----|------|-----------|-------------|
| _(none)_ | — | — | — | — |

---

## Seed Loader Contract

Pseudocode the activator MUST follow (PHP-shaped, not implementation):

```text
foreach (lookupTable in [UserStatus, Role, Permission, Provider, …, AuditOutcome]):
    foreach (row in seeds[lookupTable]):
        INSERT OR IGNORE INTO {lookupTable} ({lookupTable}Id, Name [, Numeric]) VALUES (...)

foreach (rp in rolePermissionSeeds):
    INSERT OR IGNORE INTO RolePermission (RoleId, PermissionId) VALUES (...)

foreach (kv in configKvDefaults):
    INSERT OR IGNORE INTO ConfigKv (KeyName, ValueText, UpdatedAt) VALUES (?, ?, now())
```

- No `UPDATE` paths in the seeder. Admin-edited rows never overwritten.
- Seeder runs inside the same transaction that bumps `MigrationState.PluginVersion`.
- On failure: rollback whole transaction; activator surfaces `GL-MIGRATION-PENDING` on next request.

---

## Cross-references

- §01 — enum semantics (Name ↔ meaning).
- §02 — table definitions (PK widths, FK targets).
- §06 — migration runner that invokes this seeder.
- §15 — error codes raised when seed assumptions break (`GL-CONFIG-MISSING`, `GL-MIGRATION-PENDING`).
- §31 — SSH lane that consumes `SshAuthMode`, `ReplayWindowSeconds`, `SshNonceJanitorBatch`.
