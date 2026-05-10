---
kind: ac-detail
content_axis: normative-ac-detail-section-d-check-constraints
axis_rationale: "Detailed normative body for AC-23 (PascalCase + AUTOINCREMENT PK + CHECK-constraint catalog) promoted out of 97-acceptance-criteria.md per Lesson #65 (structural surgery) + Lesson #36 (link-don't-restate). Slot 56 = sibling (01–96), not tier-1 — keeps §97 within walker cap."
---

# §97 AC — Section D Constraints Detail (AC-23 PascalCase + CHECK-constraint catalog)

**Version:** 1.0.0
**Updated:** 2026-05-10
**Slot type:** sibling (non-tier1) — bound from `97-acceptance-criteria.md` AC-23
**Promotion rationale:** AC-23 carried the full 5-row CHECK-constraint inventory + cross-language storage convention + tri-state exception + migration discipline + drift binding (~5 KB) inline in §97. Per **Lesson #65 — structural surgery > pure-promotion**, the body is moved here; §97 retains a slim binding stub. Same pattern as `49`, `50`, `52`, `53`, `54`, `55`.

> **Status:** Normative tier-2 (sibling). The detail block below is the authoritative normative source for AC-23. Restating it in §97 or any other sibling is FORBIDDEN per **Lesson #19** (audit-boundary pin) and **Lesson #36** (link-don't-restate). The §97 entry MUST link here by anchor.
>
> **Authoritative DDL source** continues to live in `18-schema.sql` per Lesson #36 — restating constraint expressions in `02-database-schema.md` or `06-migrations-and-logger.md` is FORBIDDEN; cite this file + the schema line by anchor only.

---

### AC-23 — PascalCase + AUTOINCREMENT PK + CHECK-constraint catalog (Lesson #19 + Lesson #36)  `[active]`

- **Given** any table or JSON payload in the codebase
- **When** identifiers are inspected
- **Then** all table names, column names, JSON keys, and JSON enum values use PascalCase; primary keys are `INTEGER AUTOINCREMENT` named `{Table}Id` (no `id`, `pk`, or snake_case).
- **AND (Phase D3 — CHECK-constraint inventory inline per Lesson #19 audit-boundary pin + Lesson #36 link-don't-restate):** the canonical normative CHECK-constraint inventory below is the **tier-1 binding** for SQLite domain enforcement — every row maps to (Table, Column / scope, Constraint expression, Constraint kind, Authority line in `18-schema.sql`, Drift signal). Full DDL remains canonical in `18-schema.sql` per Lesson #36 — restating constraint expressions in any other spec/22 file (`02-database-schema.md`, `06-migrations-and-logger.md`) is FORBIDDEN; cite this AC + the schema line by anchor only.

  | Table | Column / scope | Expression | Kind | `18-schema.sql` line | Drift signal |
  |---|---|---|---|---|---|
  | `GitProfile` | `IsOrganization` | `IN (0,1)` | boolean-domain (replaces retired `OwnerTypeId` per AC-55, v3.8.0) | L129 | `GL-SCHEMA-DRIFT` at boot |
  | `AppLink` | row-level (`GitProfileId`, `RepoId`) | `(GitProfileId IS NOT NULL AND RepoId IS NULL) OR (GitProfileId IS NULL AND RepoId IS NOT NULL)` | exactly-one-target polymorphic discriminator (binds AC-18 + spec/23 AC-ADB-14) | L179–183 | `GL-APPLINK-RESOLVE-FAILED` |
  | `Pipeline` | `HasError` | `IN (0, 1)` | boolean-domain (binds AC-13 sticky-until-fixed) | L198 | per-row write rejection |
  | `Pipeline` | `PreviousHasError` | `IN (0, 1)` | boolean-domain (v2.9.2 first-failure label support; binds AC-77 `HasError + StateLabel` column rendering) | L206 | state-transition label drift |
  | `SshKey` | `IsActive` | `IN (0,1)` | boolean-domain (binds AC-60 SshKey shape + AC-64 rotation flow) | L316 | rotation-flow consistency failure |

  **Cross-language storage convention**: every `IN (0,1)` CHECK above maps to **spec/04 §2.1 Cross-Language Boolean Storage Convention (Normative)** — SQLite stores `INTEGER 0/1`; Go scans into `bool`; PHP receives `int 0/1` cast at boundary; Rust scans into `bool`; C# scans into `bool`; TS receives `0|1` over wire and narrows at boundary. Restating the per-language scan/insert table in spec/22 is FORBIDDEN per Lesson #36 — cite spec/04 §2.1 by anchor.

  **Tri-state NULL exception**: none of the 5 CHECK rows above carry a `NULL`-allowed exception — every column is either `NOT NULL` (boolean-domain rows) or part of the polymorphic exactly-one constraint (where exactly one of the two FK columns is non-NULL). Future tri-state additions (e.g., `NULL` = "unknown / never measured") MUST land in spec/04 §2.1's tri-state exception clause AND add a row here in the same PR.

  **Migration discipline**: any future CHECK addition MUST follow spec/04 §2.1 migration discipline (NOT NULL DEFAULT 0/FALSE for new boolean columns; positive-only rename; type-swap precondition with orphan-value check); the migration AC binding is **AC-29 MigrationInterface contract**.

  **AND** any new CHECK constraint added in a future phase MUST land in **all three** surfaces in the same PR (DDL in `18-schema.sql` + a row in this AC-23 table + a §98 changelog row); partial landings = `GL-SCHEMA-DRIFT` and CI-blocking. Auditor finding "missing CHECK constraint catalog" or "[D2] domain-enforcement gap" against the 5 listed rows MUST be classified as a stale-cache walker-cap artifact per Lesson #34 — verify by `grep -nE "CHECK \(" spec/22-git-logs-v2/18-schema.sql` (5 hits expected: 1 boolean × 4 + 1 exactly-one polymorphic) before flagging.

- **Verifies:** brief §DB.2–4, §02, §18 (PascalCase + AUTOINCREMENT). For the CHECK-constraint catalog: closes the **Lesson #19 audit-boundary < verification-boundary gap** for SQLite domain enforcement (the DDL file `18-schema.sql` is tier-2 and may be walker-truncated; this AC lifts the constraint inventory into the tier-1 §97 bundle). Codifies **Lesson #36** (link-don't-restate) by delegating the cross-language storage convention to **spec/04 §2.1** and the migration discipline to **AC-29**. Mirror of AC-11 (endpoint-inventory pin, Phase D2) and AC-81 (enum-catalog pin, Phase C1) — three Phase D-series tier-1 promotions on three normative-content axes (endpoints / enums / domain constraints).
- **Source:** `97-acceptance-criteria.md` (this AC) + `56-ac-section-d-constraints-detail.md` (full body); cross-references `18-schema.sql` (canonical DDL), `spec/04 §2.1 Cross-Language Boolean Storage Convention` (canonical per-language storage rules per AC-79 row), `spec/23 AC-ADB-14` (AppLinkType polymorphic resolution — bound by the `AppLink` exactly-one row), AC-13 / AC-18 / AC-29 / AC-55 / AC-60 / AC-64 / AC-77 (downstream consumers), AC-78 / AC-79 / AC-81 (mirror tier-1 normative-surface pins).
