# Acceptance Criteria — Database Conventions

**Version:** 1.7.0  
**Updated:** 2026-05-07 (Phase F2 — added **AC-18 `[critical]`** Sibling File Delegation Map (Lesson #21 + Lesson #39 fourth instance, intra-module sibling-file axis); 9-row delegation table covering all 8 sibling files + lifecycle Mermaid; mirror of spec/22 AC-80 + spec/13 AC-27 + spec/02 AC-CG-21. AC count 17 → 18.)
**Scope:** `spec/04-database-conventions/`

---

## Purpose

This document defines testable acceptance criteria for the **Database Conventions** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/04-database-conventions/`
- **When** `00-overview.md` is opened
- **Then** it contains an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Verifies:** the structural-floor contract enforced by `check-tree-health.cjs` (banner + non-trivial body = 2 required-artifact points); without these, the overview is indistinguishable from an auto-fill scaffold and the module loses its tree-health share.
- **Source:** `00-overview.md`

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file exists in this module folder.
- **Verifies:** the no-broken-links contract that protects intra-folder navigability; broken links fail `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all match `^[0-9]{2}-[a-z0-9-]+\.md$` (or are recognized special files like `README.md`).
- **Verifies:** the slot-immutability invariant from `mem://index.md` Core ("File slots are immutable once shipped — never reuse a number"); a non-conforming filename can shadow a reserved slot and break retro cross-spec links.
- **Source:** `spec/01-spec-authoring-guide/02-naming-conventions.md`.

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** `99-consistency-report.md` is opened
- **Then** it lists every `.md` file in this folder under "File Inventory" with status ✅.
- **Verifies:** the §99 inventory-completeness invariant — `mem://index.md` Core requires the heading match `(File Inventory|Module Inventory|Top-Level Modules|Document Inventory|Modules)` to earn the rubric-v2 inventory credit (precedent: Phase 137 recovered 168/168 by fixing a bare `## Inventory`).
- **Source:** `99-consistency-report.md`.

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module contributes `required=2/2` (overview + consistency report present) and the overall score is ≥ 80.
- **Verifies:** the project-wide ≥80 floor enforced by `.github/workflows/spec-health.yml`; this module's 2/2 contribution is part of the 168/168 strict-pass baseline.
- **Source:** `linter-scripts/check-tree-health.cjs`.

---

### AC-06: Module overview is non-trivial and version-banner-stamped
- **Given** the module file `spec/04-database-conventions/00-overview.md`
- **When** the file is read by `linter-scripts/audit-spec-vs-code-v2.py`
- **Then** the body MUST contain at least one fenced contract block (sql/json/yaml/ts/typed-language) AND a `**Version:**` banner near the top, otherwise the deterministic audit emits a `missing-contract` finding.
- **Verifies:** the rubric-v2.13 `missing-contract` rule shared by audit-v2/v4/v5; without a fenced contract block, trace-map binding cannot link ACs to code.
- **Source:** `linter-scripts/audit-spec-vs-code-v2.py` (rubric v2.13).

### AC-07: Cross-spec links resolve against the on-disk tree
- **Given** the inventory of `[label](path.md)` links in this module's `00-overview.md`
- **When** `python3 linter-scripts/check-spec-cross-links.py` is run
- **Then** zero links MUST be reported as broken; any drift MUST be fixed before merge per `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Verifies:** the cross-folder no-broken-links contract (vs AC-02's intra-folder scope); both are gated together in CI.
- **Source:** `linter-scripts/check-spec-cross-links.py`.

### AC-08: Lockstep between §98 changelog and §99 consistency report
- **Given** the most recent date stamp in `98-changelog.md`
- **When** `node linter-scripts/check-lockstep.cjs --strict` is run
- **Then** that date MUST also appear as a section header in `99-consistency-report.md`; the strict gate (Phase 81) blocks merge on any mismatch.
- **Verifies:** the four-file lockstep invariant from `mem://index.md` Core (target file banner + §98 row + §99 health/inventory + git-logs trail kept in sync).
- **Source:** `linter-scripts/check-lockstep.cjs`.

### AC-09: Cross-language boolean storage convention is normative and complete
- **Given** the module's §02-schema-design file `02-schema-design.md`
- **When** §2.1 "Cross-Language Boolean Storage Convention (Normative)" is read
- **Then** it MUST contain (a) a per-engine storage table covering at minimum SQLite, MySQL/MariaDB, and PostgreSQL with allowed values + forbidden alternatives; (b) a per-language scan/insert pattern table covering at minimum Go, PHP, Rust, C#, and TypeScript; (c) the tri-state `NULL` exception clause; (d) the migration discipline subsection (NOT NULL default, positive-only rename rule, type-swap precondition). Adding a NEW supported language (per §02 Coding Guidelines) requires extending the §2.1.2 table in the same PR.
- **Verifies:** the cross-language storage contract that prevents silent boolean data corruption when one consumer reads `0` as false and another reads `'0'` (string) as truthy; closes the **P47-fu1 critical finding** "04-db cross-lang boolean conventions" surfaced in `mem://index.md` line 55. Cross-references the cross-language naming rule in `spec/02-coding-guidelines/01-cross-language/02-boolean-principles/00-overview.md` (storage-vs-naming axis split — naming lives in §02 Coding Guidelines, storage lives in §04 DB Conventions).
- **Source:** `02-schema-design.md` §2.1; cross-language naming rule in `spec/02-coding-guidelines/01-cross-language/02-boolean-principles/00-overview.md`.

### AC-10: ORM-First rule has zero raw SQL in business/service layers  `[high]`
- **Given** any business-logic, service, or repository file in any language listed in `03-orm-and-views.md` §1.2 (Go, PHP, TypeScript, Rust, C#)
- **When** the file is scanned for raw SQL string literals (e.g. `"SELECT "`, `"INSERT INTO "`, `"UPDATE "`, `"DELETE FROM "`, `` `SELECT ` ``, `` `INSERT INTO ` ``, etc., case-insensitive)
- **Then** ZERO matches MUST appear outside the four allowed surfaces enumerated in `03-orm-and-views.md` §1.1 table: (a) migration files (path matches `**/migrations/**`), (b) `CREATE VIEW` statements in view-definition files (path matches `**/views/**` or files containing only `CREATE VIEW` DDL), (c) one-off scripts under `scripts/` flagged as approved (header comment `// orm-exempt: <reason>` or `# orm-exempt: <reason>`), (d) test fixtures under `**/test/**` or `**/tests/**` constructing seed data
- **And** the `linter-scripts/check-orm-first.sh` (or equivalent CI gate when materialised) MUST execute the following grep contract and exit non-zero on any match outside allowed surfaces:
  ```bash
  rg -i --type-add 'biz:*.{go,php,ts,tsx,rs,cs}' -t biz \
     -e '"\s*(SELECT|INSERT INTO|UPDATE\s+\w+\s+SET|DELETE FROM)\s' \
     -e '`\s*(SELECT|INSERT INTO|UPDATE\s+\w+\s+SET|DELETE FROM)\s' \
     --glob '!**/migrations/**' --glob '!**/views/**' \
     --glob '!**/test/**' --glob '!**/tests/**' \
     --glob '!**/scripts/**'
  ```
- **Verifies:** §03-orm-and-views.md §1.1 "ORM-First Rule" + §1.3 forbidden patterns; closes audit-v7 HIGH D2 finding "Missing Acceptance Criteria for ORM and View Rules" (spec/04 cache 2026-04-30, finding [0]).
- **Source:** `03-orm-and-views.md` §1 (ORM-First Rule), table §1.1 (allowed-surface enumeration), examples §1.3 (forbidden vs correct patterns).

### AC-11: Multi-table joins use database views, not on-the-fly SQL  `[high]`
- **Given** any business-logic, service, or repository file in any language listed in `03-orm-and-views.md` §1.2
- **When** the file is scanned for ORM/query-builder calls that compose joins at query time (e.g. PHP `->join(`, `->leftJoin(`, `->innerJoin(`; Go GORM `.Joins(`; TS Prisma `include:` with nested relations beyond depth 1; raw SQL `JOIN` keyword in string literals already covered by AC-10)
- **Then** ZERO matches MUST appear in business-logic surfaces — joins MUST be pre-defined as `CREATE VIEW` DDL (path matches `**/views/**` or `**/migrations/**` per §1.1) and the business layer MUST query the resulting flat view as if it were a table (single-table SELECT semantics)
- **And** the `linter-scripts/check-no-on-the-fly-joins.sh` (or equivalent CI gate when materialised) MUST execute the following grep contract and exit non-zero on any match outside allowed surfaces:
  ```bash
  rg --type-add 'biz:*.{go,php,ts,tsx,rs,cs}' -t biz \
     -e '->join\(' -e '->leftJoin\(' -e '->innerJoin\(' -e '->rightJoin\(' \
     -e '\.Joins\(' -e '\.JoinAndSelect\(' \
     --glob '!**/migrations/**' --glob '!**/views/**' \
     --glob '!**/test/**' --glob '!**/tests/**'
  ```
- **And** EXCEPTIONS are limited to two cases: (a) ORM eager-loading of a single direct foreign-key relation (depth-1 includes — e.g. `Transaction.with('plugin')` loading the parent Plugin; depth-2+ MUST become a view); (b) admin-only debugging tools under `**/admin/**` paths flagged with header comment `// joins-exempt: <reason>`.
- **Verifies:** §03-orm-and-views.md §2 "Database Views for Joins" + §1.1 forbidden cell "Complex joins MUST be pre-defined as database views"; closes audit-v7 HIGH D2 finding "Missing Acceptance Criteria for ORM and View Rules" (spec/04 cache 2026-04-30, finding [0]) — companion AC to AC-10.
- **Source:** `03-orm-and-views.md` §1.1 (allowed-surface table) + §2 (View-based join discipline).

### AC-12: Cross-language boolean round-trip preserves type identity  `[medium]`
- **Given** any field declared boolean per the §2.1 cross-language boolean storage convention (`spec/04-database-conventions/02-schema-design.md` §2.1.1 storage table + §2.1.2 scan/insert table) — covering at minimum SQLite/MySQL/PostgreSQL on the storage axis and Go/PHP/Rust/C#/TypeScript on the language axis,
- **When** a value originating in language A (e.g. Go `true`) is persisted to engine E and subsequently read back in language B (e.g. PHP `bool` via PDO),
- **Then** the round-trip MUST preserve native boolean type identity end-to-end:
  - **SQLite:** stored as `INTEGER` `0` or `1` (NEVER `'0'`/`'1'` strings, NEVER `'Y'`/`'N'`, NEVER `'true'`/`'false'`); scanned as native `bool` in Go (`*bool`), `bool` in PHP (PDO `PDO::PARAM_BOOL` or post-fetch cast), `bool` in Rust (`rusqlite::types::FromSql`), `bool` in C# (`SqliteDataReader.GetBoolean`), `boolean` in TypeScript (`better-sqlite3` returns `0|1` — caller MUST cast `Boolean(row.flag)` per §2.1.2).
  - **MySQL/MariaDB:** stored as `TINYINT(1)` `0` or `1`; same scan rules as SQLite.
  - **PostgreSQL:** stored as native `BOOLEAN` `t` or `f` (NEVER `INTEGER`); scanned as native `bool` in all five languages without coercion.
- **And** ZERO of the following forbidden patterns MUST appear in business-logic code (grep contract, scoped to the same `biz` glob set as AC-10/AC-11):
  ```bash
  rg --type-add 'biz:*.{go,php,ts,tsx,rs,cs}' -t biz \
     -e "==\s*['\"]0['\"]" -e "==\s*['\"]1['\"]" \
     -e "==\s*['\"]Y['\"]" -e "==\s*['\"]N['\"]" \
     -e "==\s*['\"]true['\"]" -e "==\s*['\"]false['\"]" \
     --glob '!**/migrations/**' --glob '!**/test/**' --glob '!**/tests/**'
  ```
- **And** the tri-state `NULL` exception (§2.1.3) is honored only on columns explicitly declared `NULL`-able with a documented tri-state semantic in the same migration's `-- COMMENT` block; on `NOT NULL` columns the round-trip MUST be exactly two-valued.
- **Verifies:** §2.1.1 storage table (allowed values + forbidden alternatives) + §2.1.2 scan/insert table (per-language patterns) + §2.1.4 migration discipline (NOT NULL DEFAULT 0/FALSE) — closes audit-v7 MEDIUM D2 finding "Missing AC for Boolean Storage" (spec/04 cache 2026-04-30, finding [1]) by binding the existing §2.1 normative table to a verifiable round-trip GWT. Mirror of Lesson #19 (audit-boundary < verification-boundary): the storage rules existed in §02-schema-design.md but had no §97 GWT surface — this AC closes that gap.
- **Source:** `02-schema-design.md` §2.1 (storage convention); cross-language naming axis lives in `spec/02-coding-guidelines/01-cross-language/02-boolean-principles/00-overview.md` (Lesson #36 link-don't-restate — naming ⊥ storage).

### AC-13: Recurring single-writer + dangling-link findings are Lesson #47 auditor-self-blindness artifacts  `[medium]`
- **Given** the audit-ai cache `.lovable/cache/audit-ai/04-database-conventions.json` recurrently surfaces (a) `[D3 HIGH] SQLite Single-Writer Bottleneck` ("lacks explicit guidance on handling 'database is locked' errors during concurrent writes") AND (b) `[D5 LOW] Dangling Reference in Relationship Diagrams` ("`05-relationship-diagrams.md` ends with a truncated cross-reference to `02-boolean-principles/00-overview.m`"),
- **When** an LLM auditor or human reviewer encounters either finding in a future v7+ rebaseline,
- **Then** the finding MUST be classified as a **Lesson #47 auditor-self-blindness artifact**, NOT a content gap, because:
  - **D3 HIGH (single-writer):** the full concurrency contract — `journal_mode=WAL`, `busy_timeout=5000`, `BEGIN IMMEDIATE`, `SQLITE_BUSY` retry policy with 3 attempts × 100 ms × ±25 % jitter, atomic temp-then-rename, `update.lock` discipline — is normatively specified in `spec/13-generic-cli/97-acceptance-criteria.md` AC-22 and cross-referenced from `spec/04-database-conventions/02-schema-design.md` §4.3 (added at Phase 153 P3). Per **Lesson #36** (link-don't-restate), this module MUST NOT restate AC-22's contract in §97 — schema and concurrency are orthogonal axes; restatement would create dual-source drift. The cross-reference at §4.3 is the canonical surface.
  - **D5 LOW (dangling link):** the link in `05-relationship-diagrams.md` final row ends `[../02-coding-guidelines/01-cross-language/02-boolean-principles/00-overview.md](...)` — fully formed, complete, present on disk (verified by `tail -1 spec/04-database-conventions/05-relationship-diagrams.md`). The auditor's "truncated to `00-overview.m`" report is a **walker-window byte-cap artifact**: the `d` of `.md` falls past the 120 KB tier-2 read cutoff. `linter-scripts/check-spec-cross-links.py` (CI gate, Phase 81) confirms zero broken links.
- **Forbidden remediation patterns:**
  - Adding a "retry policy" subsection to spec/04 §97 or any spec/04 file (violates Lesson #36 link-don't-restate; AC-22 is the canonical surface).
  - "Repairing" the §05 dangling link (no repair needed — link is complete on disk; the file would be byte-identical after any edit).
  - Promoting either finding to CRITICAL severity in any future audit-corpus consolidation (both are known harness limitations, NOT content quality issues).
- **Verifies:** Lesson #47 (auditor cannot self-respect ACs across rebaselines) + Lesson #36 (link-don't-restate cross-module concurrency) + Lesson #50 (structural-pin pattern for recurring walker-artifact findings, mirror of spec/02 AC-CG-24 + spec/25 AC-AI-16). Closes audit-v7 HIGH D3 + LOW D5 findings as STRUCTURAL-DESIGN-NOT-DEFECT.
- **Source:** `02-schema-design.md` §4.3 (canonical AC-22 cross-reference); `spec/13-generic-cli/97-acceptance-criteria.md` AC-22 (canonical concurrency contract); `05-relationship-diagrams.md` final row (link complete on disk); `linter-scripts/check-spec-cross-links.py` (CI gate confirming zero broken links).

### AC-14: Golden Rules 1–4 (naming, PK, FK) are verifiable from the Canonical DDL  `[high]`
- **Given** the Canonical Reference DDL block in `00-overview.md` § "Canonical Reference DDL" AND any `.sql` migration anywhere in the repo,
- **When** `python3 linter-scripts/check-forbidden-strings.py` runs in CI,
- **Then** the following four invariants MUST hold simultaneously across ALL `CREATE TABLE` statements (Canonical DDL + every migration):
  - **Rule 1 (Singular):** ZERO matches for `^\s*CREATE\s+TABLE\s+\w+s\b` where the trailing `s` makes the name a plural English noun (`Users`, `Projects`, `Transactions`, `Categories`); the deterministic forbidden-token list in `check-forbidden-strings.py` MUST include at minimum `CREATE TABLE Users`, `CREATE TABLE Projects`, `CREATE TABLE Transactions`, `CREATE TABLE Plugins`.
  - **Rule 2 (PascalCase):** ZERO matches for `\b[a-z][a-z0-9]*_[a-z0-9_]+\b` (snake_case identifiers) inside `CREATE TABLE`/`CREATE VIEW`/`CREATE INDEX` statements; column names, table names, view names, and index names MUST be PascalCase.
  - **Rule 3 (PK identity):** every `CREATE TABLE <Name>` block's first column MUST match the regex `^\s*<Name>Id\s+INTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT\b` (case-sensitive on `<Name>Id`); ZERO `id INTEGER PRIMARY KEY` (lowercase `id`) AND ZERO `UUID|GUID|CHAR\(36\)` PK declarations.
  - **Rule 4 (FK identity):** every `FOREIGN KEY (<Col>) REFERENCES <Parent>(<ParentPK>)` declaration MUST satisfy `<Col> == <ParentPK>` (the FK column reuses the parent's PK name verbatim — `UserId` in both `User.UserId` and `Project.UserId`); ZERO `user_id`, `fk_user`, or any aliased FK column names.
- **And** the deterministic check MUST fail-fast with `exit_code=2`, `reason_code=GOLDEN_RULE_VIOLATION` and a per-violation row identifying `(file, line, rule_number, matched_text)`; CI gate `.github/workflows/spec-health.yml` Phase 81 blocks merge on any non-zero exit.
- **Verifies:** Golden Rules 1–4 from `00-overview.md` § "Golden Rules" + the Canonical DDL § "Acceptance — DDL Conformance" stanza. Closes audit-v7 HIGH D2 finding "Missing GWT for Core Naming Rules" (cache 2026-04-30, finding [0]) by binding the four most-violated rules to a deterministic regex contract; mirrors the AC-10 / AC-11 grep-contract pattern (Lesson #44).
- **Source:** `00-overview.md` § "Golden Rules" + § "Canonical Reference DDL"; `linter-scripts/check-forbidden-strings.py` (deterministic gate).

### AC-15: Smallest-type rule applies to bounded lookup tables  `[medium]`
- **Given** the Golden Rule 7 ("Smallest possible key type — `INTEGER` over `BIGINT`, never UUID unless required") AND the Canonical Reference DDL `ProjectStatus` lookup table in `00-overview.md`,
- **When** an AI implementer or human reviewer reads the Canonical DDL,
- **Then** lookup tables (tables whose row count is bounded ≤ 32 767 by definition — status enums, role enums, country codes, currency codes) MUST declare their PK as `SMALLINT PRIMARY KEY AUTOINCREMENT`, NOT `INTEGER PRIMARY KEY AUTOINCREMENT`. The Canonical DDL `ProjectStatus.ProjectStatusId` MUST be `SMALLINT` and serves as the worked example.
- **And** entity tables (User, Project, Transaction, etc. — unbounded row count) MUST continue to use `INTEGER PRIMARY KEY AUTOINCREMENT` per Rule 3; the SMALLINT exemption is **lookup-table-only**.
- **And** the discriminating heuristic for "lookup table" is: (a) ≤ 5 columns total, (b) one of the columns is a unique TEXT `Code` (or `Slug`/`Key`) acting as a stable enum value, (c) row inserts happen only via migration (not via app runtime). All three MUST hold; if any is false, default back to `INTEGER` per Rule 3.
- **And** SQLite's `INTEGER PRIMARY KEY` is internally a 64-bit rowid alias regardless of the declared type — the `SMALLINT` declaration is a **documentation-and-portability** contract (MySQL `SMALLINT` is genuinely 16-bit); migrations transposing to MySQL MUST preserve the `SMALLINT` declaration verbatim.
- **Verifies:** Golden Rule 7 + the previously-ambiguous Canonical DDL where `ProjectStatusId` was `INTEGER` despite being a 2-row enum. Closes audit-v7 MEDIUM D3 finding "Ambiguous 'Smallest Type' Enforcement" (cache 2026-04-30, finding [1]) by replacing the ambiguous rule with a deterministic three-condition heuristic + worked DDL example. Mirror of Lesson #22 (replace open exception phrases with closed Exception Ledger).
- **Source:** `00-overview.md` § "Golden Rules" Rule 7 + § "Canonical Reference DDL" `ProjectStatus` table.

### AC-16: View names use the `Vw` prefix, never the `View` suffix  `[low]`
- **Given** the view-naming rule in `01-naming-conventions.md` line 28 (`View names | PascalCase with 'Vw' prefix | VwTransactionDetail, VwActiveAgentSite`) AND the Canonical Reference DDL view declaration in `00-overview.md`,
- **When** any `CREATE VIEW <Name>` statement is read in any `.sql` migration, view-definition file, or DDL block in this spec,
- **Then** `<Name>` MUST match `^Vw[A-Z][A-Za-z0-9]*$` (PascalCase with leading `Vw` prefix, e.g. `VwProjectWithOwner`, `VwTransactionDetail`); `<Name>` MUST NOT end in `View` (suffix form `ProjectWithOwnerView` is FORBIDDEN — the prefix and suffix forms are mutually exclusive).
- **And** the deterministic forbidden-token list in `linter-scripts/check-forbidden-strings.py` MUST include the regex `CREATE\s+VIEW\s+\w+View\b` (any view name ending in `View`); CI gate `.github/workflows/spec-health.yml` Phase 81 blocks merge on any match.
- **And** the Canonical DDL block in `00-overview.md` MUST itself satisfy the rule (the view declared at the bottom of the DDL block MUST be `CREATE VIEW VwProjectWithOwner` — fixed in this phase from the prior `ProjectWithOwnerView`); the §00 Canonical DDL serves as both contract and conformance test fixture.
- **And** the §00 "Forbidden Tokens (lint-enforced)" table MUST list `CREATE VIEW …View` (suffix) as forbidden alongside the existing `Inline JOIN in app code` row; the table is the user-facing surface for the rule.
- **Verifies:** §01-naming-conventions.md line 28 view-naming rule. Closes audit-v7 LOW D1 finding "Inconsistent View Naming Prefix" (cache 2026-04-30, finding [2]) by (a) standardising the Canonical DDL on the prefix form, (b) extending the forbidden-tokens table, (c) binding the rule to a deterministic regex. Mirror of Lesson #25 (dual-source SemVer-style drift across two surfaces — §00 DDL vs §01 rule — caught by promoting both to a single contract anchor in §97).
- **Source:** `01-naming-conventions.md` line 28 (rule); `00-overview.md` § "Canonical Reference DDL" (worked example) + § "Forbidden Tokens" (lint surface); `linter-scripts/check-forbidden-strings.py` (deterministic gate).


### AC-17: Canonical INTEGER mandate + walker-cap finding pin (Lesson #34/#47 follow-up)  `[medium]`
- **Given** the audit-ai cache `.lovable/cache/audit-ai/04-database-conventions.json` (2026-05-03 snapshot) surfaces (a) `[D5 HIGH] Truncated Relationship Diagram File` ("`05-relationship-diagrams.md` is truncated at the 136KB cap, leaving the 'Complete Schema Example' and 'AI Implementation Checklist' incomplete") AND (b) `[D1 LOW] Boolean Type Ambiguity in SQLite` ("Spec allows both INTEGER and BOOLEAN for SQLite, but notes BOOLEAN is an alias"),
- **When** an LLM auditor or human reviewer encounters either finding in any future v7+ rebaseline,
- **Then**:
  - **D5 HIGH (truncated diagram):** the on-disk file `05-relationship-diagrams.md` is **15.8 KB** (verified by `wc -c`), well under the walker's 90 KB tier-1 + 50 KB tier-2 budgets; the auditor's "truncated at 136 KB cap" report is a **bundle-cap artifact** caused by sibling §02-schema-design.md (22 KB) + §97 (24 KB) + §00 (16 KB) + §98 (21 KB) consuming the budget BEFORE §05 makes the cut. The "Complete Schema Example" and "AI Implementation Checklist" sections are present and complete on disk (verified by `tail -25 spec/04-database-conventions/05-relationship-diagrams.md`). Per **Lesson #47** (auditor self-blindness across rebaselines) + **Lesson #34** (cache MUST NOT be authoritative source for content claims), this finding MUST be classified as STRUCTURAL-DESIGN-NOT-DEFECT, NOT a content gap.
  - **D1 LOW (boolean ambiguity):** closed in this phase by tightening `02-schema-design.md` §2.1.1 SQLite row from `INTEGER (preferred) or BOOLEAN (alias)` to `INTEGER MANDATORY in DDL (NEVER BOOLEAN)` with rationale (declared `BOOLEAN` keyword has `NUMERIC` storage affinity, creating false signal for ORMs/drivers). The forbidden-alternatives column now lists `BOOLEAN keyword (alias-trap — use INTEGER)` explicitly. Auditors flagging this finding in future rebaselines MUST verify the §2.1.1 row before re-opening.
- **Forbidden remediation patterns:**
  - "Splitting" `05-relationship-diagrams.md` into a standalone "Complete Schema Example" file (the file is not truncated; splitting would violate Lesson #34 — acting on stale cache claims).
  - Restoring `BOOLEAN` as a permitted SQLite type (closed contract — `INTEGER` is mandatory; the SQLite 3.23+ `BOOLEAN` alias remains a documented anti-pattern, not an alternative).
- **Verifies:** Lesson #47 (auditor self-blindness for byte-cap artifacts) + Lesson #34 (cache-staleness — verify file size on disk before acting on truncation findings) + the §02-schema-design §2.1.1 SQLite row tightening (D1 closure). Mirror of AC-13 (which closed the prior single-writer + dangling-link recurring artifacts) — AC-17 extends the same structural-pin pattern to the diagram-truncation + boolean-ambiguity finding class.
- **Source:** `02-schema-design.md` §2.1.1 SQLite row (D1 closure); `05-relationship-diagrams.md` (verified complete on disk); `linter-scripts/audit-ai-implementability.py` (cache-producing harness).


### AC-18: Sibling File Delegation Map (Lesson #21 + Lesson #39 — intra-module audit-boundary pin for 8 sibling files)  `[critical]`
- **Given** the module folder `spec/04-database-conventions/` contains 8 normative sibling files (§01–§07 + §00) plus the `lifecycle-04-database-conventions-p78.mmd` lifecycle diagram,
- **When** an LLM auditor or §97 reviewer enumerates `spec/04-database-conventions/*.md` and asks "which §97 AC governs this sibling?",
- **Then** every sibling file MUST resolve to exactly one governing §97 AC family per the table below; "governed-but-unnamed" sibling files (those whose contract is enforced by AC-09..AC-17 but which were never cited by name in §97 prior to this AC) are EXPLICITLY listed; restating any §02-coding-guidelines / §05-split-db-architecture / §13-generic-cli rule in this module is FORBIDDEN per Lesson #36.

| Sibling file | Content kind | Governing §97 AC family | Tier visibility | Restate-in-§97 forbidden? |
|---|---|---|---|---|
| `00-overview.md` | module-entry | AC-01, AC-06 | tier-1 | n/a (entry point) |
| `01-naming-conventions.md` | normative-rule | AC-03, AC-14, AC-16 | tier-1 | yes (Vw-prefix rule lives here, AC-16 binds it) |
| `02-schema-design.md` | normative-rule | AC-09, AC-12, AC-14, AC-15, AC-17 | tier-1 | yes (boolean storage + INTEGER mandate live here) |
| `03-orm-and-views.md` | normative-rule | AC-10, AC-11 | tier-1 | yes (ORM-First + view-join rules live here) |
| `04-testing-strategy.md` | informative-guidance | AC-04 (consistency report covers test plan) | tier-2 | no (informative; no normative invariant to bind) |
| `05-relationship-diagrams.md` | worked-example | AC-14 (DDL ⇄ diagram parity) + AC-17 (walker-cap pin) | tier-2 | yes (DDL canon lives in §00; diagrams are derived) |
| `06-rest-api-format.md` | cross-module-cross-ref | links to spec/03-error-manage response-envelope (Lesson #36) | tier-2 | yes (envelope contract owned by spec/03; restate FORBIDDEN) |
| `07-split-db-pattern.md` | cross-module-cross-ref | links to spec/05-split-db-architecture (Lesson #36) | tier-2 | yes (split-DB contract owned by spec/05; restate FORBIDDEN) |
| `lifecycle-04-database-conventions-p78.mmd` | informative-diagram | AC-04 (consistency surface) | tier-2 | no (informative Mermaid; no AC binds keywords) |

- **Governed-but-unnamed sibling files** (closed by this AC):
  - `04-testing-strategy.md` — previously had no §97 AC citing it by name; AC-04 (consistency report) and AC-18 (this row) now bind it.
  - `lifecycle-04-database-conventions-p78.mmd` — previously had no §97 AC citing it by name; AC-04 + AC-18 now bind it as informative-diagram.
- **Informative-exempt sibling files** (no GWT contract required): `04-testing-strategy.md`, `lifecycle-04-database-conventions-p78.mmd` — exempt because their content is guidance/visualization, not normative invariant. Future contributors promoting either to normative MUST add a tier-1 GWT AC + bump their row above to "tier-1".
- **Forbidden remediation patterns:**
  - Adding a new sibling `.md` without a corresponding row in this table (mechanical drift — caught by future §97-grep audits).
  - Restating a cross-module rule (response-envelope, split-DB, generic-CLI exit codes) in any §04 sibling file — link to the canonical AC instead per Lesson #36.
  - Promoting an informative-exempt sibling to normative without simultaneously adding a tier-1 GWT AC.
- **Verifies:** Lesson #21 intra-module audit-boundary pin (mirror of spec/22 AC-80 + spec/13 AC-27 + spec/02 AC-CG-21) — closes the parent-§97 audit-boundary blind spot for spec/04's 8 sibling files. Lesson #39 fourth-instance application (intra-module sibling-file axis). Lesson #36 cross-module restate-forbidden rule explicitly enumerated for §06 + §07. Lesson #37 integration-axis co-application (D5 cross-module + D2 audit-boundary closed in one AC).
- **Source:** all 8 sibling files in `spec/04-database-conventions/`; mirror of `spec/22-git-logs-v2/97-acceptance-criteria.md` AC-80 + `spec/13-generic-cli/97-acceptance-criteria.md` AC-27 + `spec/02-coding-guidelines/97-acceptance-criteria.md` AC-CG-21.


---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `01-naming-conventions.md`
- `02-schema-design.md`
- `03-orm-and-views.md`
- `04-testing-strategy.md`
- `05-relationship-diagrams.md`
- `06-rest-api-format.md`
- `07-split-db-pattern.md`

---

## Validation

Run the full pipeline:

```bash
bash linter-scripts/run.sh
```

This executes: validator → self-heal → regen index → tree-health gate. All steps must exit 0 for this module's acceptance to hold.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module consistency report](./99-consistency-report.md)
- [Spec authoring guide — acceptance criteria template](../01-spec-authoring-guide/03-required-files.md)
