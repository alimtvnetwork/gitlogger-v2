# Database Schema — UpdateChecker & UpdateStatus

> **Version:** 1.1.0
> **Parent:** [00-overview.md](./00-overview.md)

---

## Purpose

Defines the SQLite tables that persist update-check results. PascalCase
naming throughout — table names, column names, enum values. Default
backend is SQLite via the project ORM; when no database exists the same
data is written to JSON (see [09-json-fallback-store.md](./09-json-fallback-store.md)).

---

## 1. Table: `UpdateChecker`

Singleton-style row table — typically one row per CLI install, updated
in place on every successful check. (Implementations MAY append rows
for audit history; the service always reads `WHERE Id = (SELECT MAX(Id))`.)

| FieldName            | Type     | Null | Default | Notes |
|----------------------|----------|------|---------|-------|
| `UpdateCheckerId`    | INTEGER  | no   | AUTOINCREMENT | Primary key |
| `CurrentVersion`     | TEXT     | no   | —       | Installed CLI version, e.g., `V1.5.0` |
| `LatestVersion`      | TEXT     | yes  | NULL    | Highest version found via discovery |
| `HasUpdate`          | BOOLEAN  | no   | 0       | True if `LatestVersion > CurrentVersion` |
| `UpdateStatusId`     | TINYINT  | no   | 1       | FK → `UpdateStatus.UpdateStatusId` |
| `OwnerKind`          | TEXT     | yes  | NULL    | `User` or `Organization` |
| `Owner`              | TEXT     | yes  | NULL    | GitHub login |
| `CurrentRepo`        | TEXT     | yes  | NULL    | e.g., `repo-v15` |
| `LatestReleaseUrl`   | TEXT     | yes  | NULL    | GitHub release page URL |
| `WindowsInstallUrl`  | TEXT     | yes  | NULL    | Pinned installer URL (Windows) |
| `WindowsInstallCmd`  | TEXT     | yes  | NULL    | One-liner (Windows) |
| `UnixInstallUrl`     | TEXT     | yes  | NULL    | Pinned installer URL (Unix) |
| `UnixInstallCmd`     | TEXT     | yes  | NULL    | One-liner (Unix) |
| `Checksum`           | TEXT     | yes  | NULL    | `Sha256:Hex` of the installer |
| `PublishedAt`        | DATETIME | yes  | NULL    | Release publish time (UTC) |
| `MinSupportedFrom`   | TEXT     | yes  | NULL    | Lowest version that can directly upgrade |
| `NewRepoUrl`         | TEXT     | yes  | NULL    | Migration target repo, when set |
| `Notes`              | TEXT     | yes  | NULL    | Release-notes summary |
| `RawJson`            | TEXT     | yes  | NULL    | Full combined JSON (see `03-combined-json.md`) |
| `LastCheckedAt`      | DATETIME | yes  | NULL    | UTC timestamp of last successful check |
| `NextCheckDueAt`     | DATETIME | yes  | NULL    | `LastCheckedAt + CheckIntervalHours` |
| `CheckIntervalHours` | SMALLINT | no   | 12      | Configured interval |
| `ErrorMessage`       | TEXT     | yes  | NULL    | Last error message |
| `ErrorAt`            | DATETIME | yes  | NULL    | UTC timestamp of last error |
| `Description`        | TEXT     | yes  | NULL    | Schema Rule 10 — entity description |
| `CreatedAt`          | DATETIME | no   | CURRENT_TIMESTAMP | Row creation |
| `UpdatedAt`          | DATETIME | no   | CURRENT_TIMESTAMP | Row update |

> **Schema Rule 10/11/12 compliance:** `UpdateChecker` is a transactional
> table; `Description`, plus `Notes` (already present) and `ErrorMessage`
> satisfy the free-text requirement. All free-text columns are nullable
> with no `DEFAULT`.

---

## 2. Table: `UpdateStatus` (Lookup)

| FieldName        | Type    | Null | Notes |
|------------------|---------|------|-------|
| `UpdateStatusId` | TINYINT | no   | Primary key (smallest int — cardinality ≤ 8) |
| `Name`           | TEXT    | no   | Enum value (PascalCase) |
| `Label`          | TEXT    | no   | Human-readable label |
| `Description`    | TEXT    | yes  | Schema Rule 10 |

### Seed rows

| UpdateStatusId | Name             | Label                       |
|----------------|------------------|-----------------------------|
| 1              | `UpToDate`       | Up to date                  |
| 2              | `UpdateFound`    | Update available            |
| 3              | `UpdateApplied`  | Update applied              |
| 4              | `Failed`         | Last check failed           |
| 5              | `Migrated`       | Project moved to a new repo |

> The enum is mirrored in code as `UpdateStatusEnum` (PascalCase, see
> Enum Standards) with strict `ParseUpdateStatus()` parsing.

---

## 3. Relationships

```
UpdateChecker.UpdateStatusId  ──►  UpdateStatus.UpdateStatusId   (Many-to-One)
```

No other foreign keys. The table is intentionally self-contained so the
update subsystem has zero coupling to user/session tables.

---

## 4. DDL (SQLite)

```sql
CREATE TABLE IF NOT EXISTS UpdateStatus (
  UpdateStatusId TINYINT PRIMARY KEY,
  Name           TEXT    NOT NULL UNIQUE,
  Label          TEXT    NOT NULL,
  Description    TEXT    NULL
);

CREATE TABLE IF NOT EXISTS UpdateChecker (
  UpdateCheckerId    INTEGER PRIMARY KEY AUTOINCREMENT,
  CurrentVersion     TEXT     NOT NULL,
  LatestVersion      TEXT     NULL,
  HasUpdate          BOOLEAN  NOT NULL DEFAULT 0,
  UpdateStatusId     TINYINT  NOT NULL DEFAULT 1
                     REFERENCES UpdateStatus(UpdateStatusId),
  OwnerKind          TEXT     NULL,
  Owner              TEXT     NULL,
  CurrentRepo        TEXT     NULL,
  LatestReleaseUrl   TEXT     NULL,
  WindowsInstallUrl  TEXT     NULL,
  WindowsInstallCmd  TEXT     NULL,
  UnixInstallUrl     TEXT     NULL,
  UnixInstallCmd     TEXT     NULL,
  Checksum           TEXT     NULL,
  PublishedAt        DATETIME NULL,
  MinSupportedFrom   TEXT     NULL,
  NewRepoUrl         TEXT     NULL,
  Notes              TEXT     NULL,
  RawJson            TEXT     NULL,
  LastCheckedAt      DATETIME NULL,
  NextCheckDueAt     DATETIME NULL,
  CheckIntervalHours SMALLINT NOT NULL DEFAULT 12,
  ErrorMessage       TEXT     NULL,
  ErrorAt            DATETIME NULL,
  Description        TEXT     NULL,
  CreatedAt          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS IxUpdateCheckerNextCheckDueAt
  ON UpdateChecker(NextCheckDueAt);
```

---

## 5. Migration Note

The DDL is idempotent. The service runs it on first call to
`UpdateCheckerService.Initialize()`. Lookup rows are upserted by
`UpdateStatusId`.

---

## 6. Code Mirror — `UpdateStatusEnum` (Phase 20 normative)

> **Status:** Normative. Section §2 declares the lookup table is
> "mirrored in code as `UpdateStatusEnum`". The two reference
> implementations below ARE that mirror — they MUST stay in lockstep
> with the seed rows in §2 (same id ↔ same name ↔ same label).
> Adding a sixth status means: insert seed row → add enum case in
> BOTH languages → bump module version → §98 changelog row.

### 6.1 TypeScript reference (numeric enum, 1-based to match `UpdateStatusId`)

```typescript
// src/update/UpdateStatusEnum.ts
// Source-of-truth pairing: spec/14-update/24-update-check-mechanism/04-database-schema.md §2

export enum UpdateStatus {
  UpToDate      = 1,
  UpdateFound   = 2,
  UpdateApplied = 3,
  Failed        = 4,
  Migrated      = 5,
}

export const UpdateStatusName = {
  [UpdateStatus.UpToDate]:      "UpToDate",
  [UpdateStatus.UpdateFound]:   "UpdateFound",
  [UpdateStatus.UpdateApplied]: "UpdateApplied",
  [UpdateStatus.Failed]:        "Failed",
  [UpdateStatus.Migrated]:      "Migrated",
} as const satisfies Record<UpdateStatus, string>;

export const UpdateStatusLabel = {
  [UpdateStatus.UpToDate]:      "Up to date",
  [UpdateStatus.UpdateFound]:   "Update available",
  [UpdateStatus.UpdateApplied]: "Update applied",
  [UpdateStatus.Failed]:        "Last check failed",
  [UpdateStatus.Migrated]:      "Project moved to a new repo",
} as const satisfies Record<UpdateStatus, string>;

/** Strict parse — throws on unknown name (no silent fallback). */
export function parseUpdateStatus(name: string): UpdateStatus {
  const entry = Object.entries(UpdateStatusName).find(([, n]) => n === name);
  if (!entry) {
    throw new Error(`Unknown UpdateStatus: ${JSON.stringify(name)}`);
  }
  return Number(entry[0]) as UpdateStatus;
}
```

### 6.2 Go reference (typed alias, same numeric pairing)

```go
// internal/update/update_status_enum.go
// Source-of-truth pairing: spec/14-update/24-update-check-mechanism/04-database-schema.md §2

package update

import "fmt"

type UpdateStatus uint8

const (
    UpdateStatusUpToDate      UpdateStatus = 1
    UpdateStatusUpdateFound   UpdateStatus = 2
    UpdateStatusUpdateApplied UpdateStatus = 3
    UpdateStatusFailed        UpdateStatus = 4
    UpdateStatusMigrated      UpdateStatus = 5
)

func (s UpdateStatus) Name() string {
    switch s {
    case UpdateStatusUpToDate:      return "UpToDate"
    case UpdateStatusUpdateFound:   return "UpdateFound"
    case UpdateStatusUpdateApplied: return "UpdateApplied"
    case UpdateStatusFailed:        return "Failed"
    case UpdateStatusMigrated:      return "Migrated"
    default: return fmt.Sprintf("UpdateStatus(%d)", s)
    }
}

func (s UpdateStatus) Label() string {
    switch s {
    case UpdateStatusUpToDate:      return "Up to date"
    case UpdateStatusUpdateFound:   return "Update available"
    case UpdateStatusUpdateApplied: return "Update applied"
    case UpdateStatusFailed:        return "Last check failed"
    case UpdateStatusMigrated:      return "Project moved to a new repo"
    default: return ""
    }
}

// ParseUpdateStatus — strict, no silent fallback.
func ParseUpdateStatus(name string) (UpdateStatus, error) {
    switch name {
    case "UpToDate":      return UpdateStatusUpToDate,      nil
    case "UpdateFound":   return UpdateStatusUpdateFound,   nil
    case "UpdateApplied": return UpdateStatusUpdateApplied, nil
    case "Failed":        return UpdateStatusFailed,        nil
    case "Migrated":      return UpdateStatusMigrated,      nil
    default:
        return 0, fmt.Errorf("unknown UpdateStatus: %q", name)
    }
}
```

---

## 7. Wire-Format JSON Schema 2020-12 (`UpdateChecker` row → JSON)

> Used by `09-json-fallback-store.md` AND by the optional `--json` output
> of the `update-check` CLI command. Field set is a 1-to-1 projection of
> the SQL columns in §1, with PascalCase keys preserved.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://specs.local/14-update/24-update-check-mechanism/update-checker.schema.json",
  "title": "UpdateCheckerRow",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "CurrentVersion",
    "HasUpdate",
    "UpdateStatusId",
    "CheckIntervalHours"
  ],
  "properties": {
    "UpdateCheckerId":    { "type": "integer", "minimum": 1 },
    "CurrentVersion":     { "type": "string",  "pattern": "^V\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?$" },
    "LatestVersion":      { "type": ["string", "null"], "pattern": "^V\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?$" },
    "HasUpdate":          { "type": "boolean" },
    "UpdateStatusId":     { "type": "integer", "enum": [1, 2, 3, 4, 5] },
    "OwnerKind":          { "type": ["string", "null"], "enum": ["User", "Organization", null] },
    "Owner":              { "type": ["string", "null"] },
    "CurrentRepo":        { "type": ["string", "null"], "pattern": "^[A-Za-z0-9._-]+(?:-v\\d+)?$" },
    "LatestReleaseUrl":   { "type": ["string", "null"], "format": "uri" },
    "WindowsInstallUrl":  { "type": ["string", "null"], "format": "uri" },
    "WindowsInstallCmd":  { "type": ["string", "null"] },
    "UnixInstallUrl":     { "type": ["string", "null"], "format": "uri" },
    "UnixInstallCmd":     { "type": ["string", "null"] },
    "Checksum":           { "type": ["string", "null"], "pattern": "^[Ss]ha256:[0-9a-fA-F]{64}$" },
    "PublishedAt":        { "type": ["string", "null"], "format": "date-time" },
    "MinSupportedFrom":   { "type": ["string", "null"], "pattern": "^V\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?$" },
    "NewRepoUrl":         { "type": ["string", "null"], "format": "uri" },
    "Notes":              { "type": ["string", "null"] },
    "RawJson":            { "type": ["string", "null"] },
    "LastCheckedAt":      { "type": ["string", "null"], "format": "date-time" },
    "NextCheckDueAt":     { "type": ["string", "null"], "format": "date-time" },
    "CheckIntervalHours": { "type": "integer", "minimum": 1, "maximum": 168, "default": 12 },
    "ErrorMessage":       { "type": ["string", "null"] },
    "ErrorAt":            { "type": ["string", "null"], "format": "date-time" },
    "Description":        { "type": ["string", "null"] },
    "CreatedAt":          { "type": "string", "format": "date-time" },
    "UpdatedAt":          { "type": "string", "format": "date-time" }
  },
  "allOf": [
    {
      "if":   { "properties": { "HasUpdate": { "const": true } } },
      "then": { "required":   ["LatestVersion"] }
    },
    {
      "if":   { "properties": { "UpdateStatusId": { "const": 4 } } },
      "then": { "required":   ["ErrorMessage", "ErrorAt"] }
    }
  ]
}
```

---

## 8. Acceptance — Code/Schema/Seed Conformance

**Given** a contributor adds, removes, or renames a row in the §2
`UpdateStatus` seed table,  
**When** CI runs the conformance check (`linter-scripts/check-update-status-mirror.py`),  
**Then** the test MUST pass only if (a) `UpdateStatusEnum` cases in
TypeScript and Go each contain exactly the same `(id, name, label)`
triples, (b) the JSON-Schema `UpdateStatusId.enum` array matches the
seed-row id set, and (c) `parseUpdateStatus` / `ParseUpdateStatus`
round-trip every name without silent fallback.

---

*Database Schema — v1.1.0 — 2026-04-26*
