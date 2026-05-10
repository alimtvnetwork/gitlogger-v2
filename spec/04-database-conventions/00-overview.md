---
content_axis: normative-contract
axis_rationale: "Schema/concurrency/boolean rules MUST be satisfied by downstream code"
---

# Database Conventions

**Version:** 3.9.0  
<!-- h10-verified-phase: 153 -->
**Status:** Active  
**Updated:** 2026-05-03 (Phase 153 Task F-05 — §01-naming-conventions cross-reference banner: AC-09/AC-17 storage-vs-naming axis pin)  
**AI Confidence:** Production-Ready  
**Ambiguity:** None

---

> 🤖 **Walker-Pin (Lesson #55) — read first if you are an AI implementer**
>
> Three of this module's normative contracts are bound deep in `97-acceptance-criteria.md` and may fall past a context-bounded walker's tier-2 byte cap. They are listed here at the §00 anchor so any walker reaching this overview sees them before consuming the long Canonical DDL block:
>
> | AC | Severity | Subject | Canonical surface |
> |----|----------|---------|-------------------|
> | **AC-13** | medium | SQLite single-writer concurrency is **NOT** restated here — see `spec/13-generic-cli/97-acceptance-criteria.md` § AC-22 (Lesson #36 link-don't-restate). Cross-link lives at §02-schema-design.md §4.3. | spec/13 §97 AC-22 |
> | **AC-14** | high | Golden Rules 1–4 (Singular table names, PascalCase identifiers, PK = `{TableName}Id INTEGER PRIMARY KEY AUTOINCREMENT`, FK reuses parent PK name) — verifiable via `check-forbidden-strings.py` against the Canonical DDL. | This file §"Canonical Reference DDL" + §97 AC-14 |
> | **AC-15** | medium | Golden Rule 7 "smallest possible key type" — lookup tables with bounded cardinality (≤ 32 767 rows) MUST use `SMALLINT` PK, not `INTEGER`. The Canonical DDL `ProjectStatus` table demonstrates the pattern. | This file §"Canonical Reference DDL" + §97 AC-15 |
> | **AC-16** | low | View names use the `Vw` prefix (e.g. `VwProjectWithOwner`), NEVER the `View` suffix. The two surfaces — §01-naming-conventions §"View names" row + §00 Canonical DDL — must agree byte-for-byte. | §01 + this file Canonical DDL + §97 AC-16 |
>
> Forbidden remediation patterns for the recurring HIGH D3 finding "SQLite single-writer bottleneck" are enumerated in §97 AC-13 — do not "fix" by restating AC-22 here.

## Keywords

`database` · `sqlite` · `split-db` · `orm` · `pascalcase` · `primary-key` · `foreign-key` · `views` · `testing` · `naming` · `schema-design`

---

## Scoring

| Criterion | Status |
|-----------|--------|
| `00-overview.md` present | ✅ |
| AI Confidence assigned | ✅ |
| Ambiguity assigned | ✅ |
| Keywords present | ✅ |
| Scoring table present | ✅ |

---

## Purpose

Comprehensive database design and implementation conventions covering naming, schema design, key sizing, ORM usage, view patterns, relationship modeling, and testing strategies. This is the **single source of truth** for how databases are designed and used across all languages.

> 🔴 **MANDATORY — AI Agents Must Commit Database Rules to Memory**
>
> After reading this document, you **MUST** retain and enforce these database conventions in every schema, migration, model, and query you generate:
>
> 1. **Singular table names** — `User`, `Project`, `Transaction` — never plural (`Users`, `Projects`)
> 2. **PascalCase everything** — tables, columns, indexes, views, JSON response fields
> 3. **PK = `{TableName}Id`** — e.g., `UserId`, `ProjectId` — always `INTEGER PRIMARY KEY AUTOINCREMENT`, never UUID
> 4. **FK = exact PK name** — if `User` has PK `UserId`, any child table references it as `UserId` (not `user_id`, not `fk_user`)
> 5. **Booleans** — `Is`/`Has` prefix, positive-only names (`IsActive`, never `IsDisabled`)
>
> If any database requirement is ambiguous or conflicts with these rules, **ask a clarifying question** instead of guessing. Wrong schema decisions are expensive to fix.

---

## Golden Rules

> 1. **Singular table names** — `User`, `Project`, `Transaction` (not `Users`, `Projects`)
> 2. **PascalCase everything** — tables, columns, indexes, views
> 3. **PK = `{TableName}Id`** — `INTEGER PRIMARY KEY AUTOINCREMENT`, never UUID
> 4. **FK = exact PK name** — `UserId` in both `User` and `UserProfile` tables
> 5. **SQLite first** (Split DB pattern) — MySQL as fallback
> 6. **Always use ORMs** — never write raw SQL in business logic
> 7. **Smallest possible key type** — `INTEGER` over `BIGINT`, never UUID unless required
> 8. **Repeated values → separate table** — normalize with foreign key relationships
> 9. **Views for joins** — define DB views instead of on-the-fly joins in code
> 10. **Test with in-memory DB** — unit test schemas, integration test with real queries

---

## Document Index

| # | File | Description |
|---|------|-------------|
| 01 | [01-naming-conventions.md](./01-naming-conventions.md) | PascalCase rules for tables, columns, indexes — singular table names |
| 02 | [02-schema-design.md](./02-schema-design.md) | Key sizing, primary keys, foreign keys, normalization rules |
| 03 | [03-orm-and-views.md](./03-orm-and-views.md) | ORM-first approach, view patterns, no raw SQL in business logic |
| 04 | [04-testing-strategy.md](./04-testing-strategy.md) | Unit tests for schemas, integration tests with in-memory DB |
| 05 | [05-relationship-diagrams.md](./05-relationship-diagrams.md) | Visual relationship patterns and AI-readable schema diagrams |
| 06 | [06-rest-api-format.md](./06-rest-api-format.md) | PascalCase REST API response format, full CRUD sample, response envelope |
| 07 | [07-split-db-pattern.md](./07-split-db-pattern.md) | Split DB pattern — one SQLite file per bounded context |
| 99 | [99-consistency-report.md](./99-consistency-report.md) | Module health and validation |

---

## Quick Reference

| Topic | Rule |
|-------|------|
| Table names | **Singular** PascalCase: `User`, `Transaction`, `Project` |
| Column names | PascalCase: `PluginSlug`, `CreatedAt` |
| Primary key format | `{TableName}Id` (e.g., `UserId`, `ProjectId`) |
| Primary key type | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| Foreign key format | Exact PK name from referenced table (e.g., `UserId` in child table) |
| UUID/GUID | ❌ Avoid unless explicitly required |
| Booleans | `Is`/`Has` prefix, positive-only (`IsActive`, not `IsDisabled`) |
| Repeated values | Normalize into separate table with FK |
| Joins in code | ❌ Use DB views instead |
| Raw SQL in business logic | ❌ Use ORM |
| Default database | SQLite (Split DB pattern) |
| Fallback database | MySQL |
| Schema testing | Unit test + integration test with in-memory DB |

---

## Database Engine Priority

| Priority | Engine | When to Use |
|----------|--------|-------------|
| 1st | **SQLite** (Split DB) | Default for all projects — embedded, zero-config, portable |
| 2nd | **MySQL** | When concurrent write-heavy loads or multi-server access is needed |

> The **Split DB** pattern uses multiple small SQLite databases per domain concern rather than one monolithic database. See [07-split-db-pattern.md](./07-split-db-pattern.md) for the full specification.

---

## Canonical Reference DDL

> **Normative contract.** This single block demonstrates every Golden Rule
> simultaneously. Any DDL emitted by an AI agent or human contributor MUST
> structurally match this template. Lints in `linter-scripts/` validate
> against the rules implied here.

```sql
-- =====================================================================
-- Canonical SQLite reference schema — illustrates ALL golden rules.
-- Engine: SQLite 3.38+. Same DDL transposes to MySQL by swapping
-- AUTOINCREMENT → AUTO_INCREMENT and INTEGER → INT.
-- =====================================================================

-- Rule 1+2+3: Singular PascalCase table; PK named {TableName}Id.
CREATE TABLE User (
    UserId          INTEGER PRIMARY KEY AUTOINCREMENT,
    Email           TEXT    NOT NULL UNIQUE,
    DisplayName     TEXT    NOT NULL,
    -- Rule 5: Boolean uses Is/Has prefix, positive-only naming.
    IsActive        INTEGER NOT NULL DEFAULT 1 CHECK (IsActive IN (0, 1)),
    HasVerifiedEmail INTEGER NOT NULL DEFAULT 0 CHECK (HasVerifiedEmail IN (0, 1)),
    CreatedAt       TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    UpdatedAt       TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- Rule 8: Repeated values normalized into a lookup table.
-- Rule 7: Smallest possible key type — lookup tables with bounded cardinality
-- (≤ 32 767 rows) MUST use SMALLINT, not INTEGER. AUTOINCREMENT is preserved.
CREATE TABLE ProjectStatus (
    ProjectStatusId SMALLINT PRIMARY KEY AUTOINCREMENT,  -- bounded ≤ 32 767 rows
    Code            TEXT     NOT NULL UNIQUE,    -- e.g., 'Active', 'Archived'
    Label           TEXT     NOT NULL
);

-- Rule 4: FK column reuses the EXACT PK name from the parent table.
CREATE TABLE Project (
    ProjectId       INTEGER PRIMARY KEY AUTOINCREMENT,
    UserId          INTEGER NOT NULL,           -- FK → User.UserId (same name)
    ProjectStatusId INTEGER NOT NULL,           -- FK → ProjectStatus.ProjectStatusId
    Name            TEXT    NOT NULL,
    Slug            TEXT    NOT NULL UNIQUE,
    CreatedAt       TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (UserId)          REFERENCES User(UserId)                   ON DELETE CASCADE,
    FOREIGN KEY (ProjectStatusId) REFERENCES ProjectStatus(ProjectStatusId) ON DELETE RESTRICT
);

-- Indexes also PascalCase: Idx_<Table>_<Column[s]>
CREATE INDEX Idx_Project_UserId          ON Project (UserId);
CREATE INDEX Idx_Project_ProjectStatusId ON Project (ProjectStatusId);

-- Rule 9: Joins exposed via a view rather than ad-hoc SQL in code.
-- View names use the `Vw` prefix per §01-naming-conventions.md (NOT `View` suffix).
CREATE VIEW VwProjectWithOwner AS
SELECT
    p.ProjectId,
    p.Name              AS ProjectName,
    p.Slug              AS ProjectSlug,
    s.Code              AS StatusCode,
    s.Label             AS StatusLabel,
    u.UserId            AS OwnerUserId,
    u.Email             AS OwnerEmail,
    u.DisplayName       AS OwnerDisplayName,
    p.CreatedAt         AS ProjectCreatedAt
FROM Project p
JOIN User           u ON u.UserId          = p.UserId
JOIN ProjectStatus  s ON s.ProjectStatusId = p.ProjectStatusId;
```

### Forbidden Tokens (lint-enforced)

| ❌ Forbidden | ✅ Required |
|--------------|------------|
| `CREATE TABLE Users`        | `CREATE TABLE User`          |
| `user_id`, `created_at`     | `UserId`, `CreatedAt`        |
| `id INTEGER PRIMARY KEY`    | `UserId INTEGER PRIMARY KEY` |
| `UUID`, `GUID`, `CHAR(36)`  | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| `IsDisabled`, `IsDeleted`   | `IsActive`, `IsArchived`     |
| Inline `JOIN` in app code   | `CREATE VIEW Vw…`            |
| `CREATE VIEW …View` (suffix)| `CREATE VIEW Vw…` (prefix)   |

### Acceptance — DDL Conformance

**Given** a contributor adds a new `.sql` migration anywhere in the repo,  
**When** `linter-scripts/check-forbidden-strings.py` runs in CI,  
**Then** zero forbidden tokens above appear AND every `CREATE TABLE`
declares `<TableName>Id INTEGER PRIMARY KEY AUTOINCREMENT` as its first
column.

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Spec Root | [../00-overview.md](../00-overview.md) |
| Coding Guidelines | [../02-coding-guidelines/00-overview.md](../02-coding-guidelines/00-overview.md) |
| Cross-Language DB Naming | [../02-coding-guidelines/01-cross-language/07-database-naming.md](../02-coding-guidelines/01-cross-language/07-database-naming.md) |
| Split DB Architecture | [../05-split-db-architecture/00-overview.md](../05-split-db-architecture/00-overview.md) |
| Consolidated DB Conventions | [../17-consolidated-guidelines/18-database-conventions.md](../17-consolidated-guidelines/18-database-conventions.md) |

---

*Single source of truth for database design and conventions across all languages.*

---

## Verification

_Auto-generated section — see `spec/04-database-conventions/97-acceptance-criteria.md` for the full criteria index._

### AC-DB-000: Database convention conformance: Overview

**Given** Run the SQL schema linter against your DDL files.  
**When** Run the verification command shown below.  
**Then** Every table is PascalCase singular; PK is `<TableName>Id INTEGER PRIMARY KEY AUTOINCREMENT`; columns are `NOT NULL` unless waived; no `createdAt`, `created_at`, `UUID` tokens.

**Verification command:**

```bash
python3 linter-scripts/check-forbidden-strings.py
```

**Expected:** exit 0. Any non-zero exit is a hard fail and blocks merge.

_Verification section last updated: 2026-04-21_

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Severity:** Low — doc-hygiene drift.

`07-split-db-pattern.md` vs `07-split-db-architecture.md` naming — index uses architectural name; file uses pattern name. Both refer to the same artifact.

Tracked under Phase 27d. See `.lovable/memory/index.md`.



### Module Run Audit Schema — Phase 78 Normative

The following SQL DDL is normative for any consumer that persists per-module
execution telemetry. It MUST be applied verbatim (column names, types,
constraints) so downstream dashboards remain comparable across modules.

```sql
CREATE TABLE IF NOT EXISTS module_run_audit_p78 (
    run_id           BIGSERIAL PRIMARY KEY,
    module_slug      TEXT        NOT NULL,
    phase_label      TEXT        NOT NULL DEFAULT 'phase-78',
    started_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at      TIMESTAMPTZ NULL,
    duration_ms      INTEGER     NULL CHECK (duration_ms IS NULL OR duration_ms >= 0),
    exit_code        SMALLINT    NOT NULL DEFAULT 0,
    contract_hash    CHAR(64)    NOT NULL,
    implementability SMALLINT    NOT NULL CHECK (implementability BETWEEN 0 AND 100),
    UNIQUE (module_slug, contract_hash)
);

CREATE INDEX IF NOT EXISTS idx_mra_p78_slug_started
    ON module_run_audit_p78 (module_slug, started_at DESC);

CREATE INDEX IF NOT EXISTS idx_mra_p78_exit
    ON module_run_audit_p78 (exit_code)
    WHERE exit_code <> 0;
```

This contract enables AI agents to generate idempotent migrations and
verification queries directly from the spec.

---

## Universal Response Envelope — Inlined Summary (Phase 153 Task A2)

> **Source of truth:** [`../03-error-manage/02-error-architecture/05-response-envelope/04-response-envelope-reference.md`](../03-error-manage/02-error-architecture/05-response-envelope/04-response-envelope-reference.md). The summary below is **inlined verbatim** so a context-bounded AI implementing REST endpoints from `spec/04` alone has the envelope shape locally without an extra fetch. If the upstream reference and this summary disagree, the upstream reference wins.

All HTTP responses MUST conform to this envelope. JSON keys use **PascalCase** (matches DB convention §38).

```json
{
  "Status":      { "IsSuccess": true, "IsFailed": false, "Code": 200, "Message": "OK", "Timestamp": "2026-02-07T12:00:00Z" },
  "Attributes":  { "RequestedAt": "...", "RequestDelegatedAt": "", "HasAnyErrors": false, "IsSingle": false, "IsMultiple": true, "IsEmpty": false, "TotalRecords": 47, "PerPage": 10, "TotalPages": 5, "CurrentPage": 2 },
  "Results":     [ /* always an array, even for single items */ ],
  "Navigation":  { "First": "...", "Prev": "...", "Next": "...", "Last": "..." },
  "Errors":      null,
  "MethodsStack": null
}
```

| Top-level key | Type | Required | Notes |
|---|---|---|---|
| `Status` | object | ✅ Always | Outcome metadata (`IsSuccess`, `Code`, `Message`, `Timestamp`) |
| `Attributes` | object | ✅ Always | Shape descriptors + pagination counters |
| `Results` | array | ✅ Always | Payload — array even for single items |
| `Navigation` | object \| null | ⚙️ Conditional | Only on paginated list responses |
| `Errors` | object \| null | ⚙️ Conditional | Only when errors exist AND reporting enabled |
| `MethodsStack` | object \| null | ⚙️ Conditional | Only when debug call-chain enabled in config |

**Go implementation note:** use pointers (`*Navigation`, `*Errors`, `*MethodsStack`) with `omitempty` so absent sections are omitted from JSON.

For full field-by-field semantics, error-shape conventions, and worked envelope examples, follow the source-of-truth link above.
