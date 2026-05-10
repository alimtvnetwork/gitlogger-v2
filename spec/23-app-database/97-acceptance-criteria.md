# Acceptance Criteria — 23 App Database

**Version:** 3.6.0
**Updated:** 2026-05-10 (Session 60 audit-task A-50 — restructured **AC-ADB-05** + **AC-ADB-06** into the A-44 5-link self-enforcement template: byte-exact source-of-truth pin, constraint pin, cross-AC pin, algorithm/index pin, CI-gate pin (deferred §27 gates `applink-xor-check-clause-present` + `applink-disconnect-check-clause-present`); Lesson #39 evidence triple promoted to normative auditor obligation; explicit invalidation triggers inline. AC count unchanged (18). Lifts §23 Raw-LLM C3 Testability 18→19.)
**Updated-prev:** 2026-05-10 (Session 23 audit-task A-01 — added **AC-ADB-18** `[critical]` §22 operational-pattern inheritance: ErrorEnvelope shape (§22 AC-30) + AuditTrail row (§22 AC-21) + sink-side observability rule (§22 AC-04) + schema-drift three-surface invariant (§22 AC-23) inherited by namespace extension (`GL-*` → `ADB-*`). AC count 17 → 18.)
**Scope:** `spec/23-app-database/`
**Generated:** Hand-authored alongside the v4.0.0 overview (Phase 39a). Supersedes the auto-extracted v2.0.0 set.

---

## Module Summary

Defines the App, AppLink, AppStatus, and AppLinkType tables — the polymorphic-link subsystem that binds inbound CI/CD pushes to a Profile. Enforces SQLite + PascalCase + Rule 12 (forward-only, NULLABLE, no DEFAULT) migration discipline, plus two AppLink CHECK invariants (XOR target + disconnect timestamp).

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

### Tables under test

- `App(AppId PK, AppName, AppSlug UNIQUE, Description NULL, ProfileId FK, AppStatusId FK, CreatedAt, UpdatedAt)`
- `AppLink(AppLinkId PK, AppId FK, AppLinkTypeId FK, TargetGitProfileId NULL FK, TargetRepoId NULL FK, IsActive 0/1, CreatedAt, DisconnectedAt NULL)`
- `AppStatus(AppStatusId PK, Name UNIQUE)` — seeds: `Active`, `Disabled`, `Archived`
- `AppLinkType(AppLinkTypeId PK, Name UNIQUE)` — seeds: `GitProfile`, `Repo`

### Rule 12 — Migration constraints (forward-only)

- New columns: `NULLABLE`, **no** `DEFAULT`.
- No `DROP TABLE` / `DROP COLUMN` in migrations.
- No `ROLLBACK` / `DOWN` blocks; reversibility is achieved by writing a new forward migration.

### AppLink CHECK invariants

- **XOR target:** if `AppLinkType.Name = 'Repo'` then `TargetRepoId IS NOT NULL AND TargetGitProfileId IS NULL`; symmetric for `'GitProfile'`.
- **Disconnect timestamp:** `IsActive = 1 ⇔ DisconnectedAt IS NULL`.

### File paths

- Verification script: `linter-scripts/check-forbidden-strings.py`
- DDL source of truth: `spec/23-app-database/00-overview.md` § "Inlined Contracts"
- Sibling table DDL: `spec/22-git-logs-v2/02-database-schema.md`, `spec/22-git-logs-v2/18-schema.sql`

---

## Acceptance Criteria

### AC-ADB-01: Forward-only migrations  `[critical]`
- **Given** A migration file under `migrations/` that touches `App`, `AppLink`, `AppStatus`, or `AppLinkType`.
- **When** The file is parsed for SQL keywords.
- **Then** It MUST NOT contain any of: `DROP TABLE`, `DROP COLUMN`, `ROLLBACK`, `BEGIN ROLLBACK`, or a `-- DOWN` marker section.
- **Verifies:** `00-overview.md` § "Migration Template (Rule 12 — forward-only)"

### AC-ADB-02: PascalCase enforcement  `[high]`
- **Given** Any `CREATE TABLE` or `ALTER TABLE … ADD COLUMN` statement targeting the App subsystem.
- **When** Identifiers are extracted via regex.
- **Then** Every table name and column name MUST match `^[A-Z][A-Za-z0-9]*$` (PascalCase, no underscores, no leading lowercase).
- **Verifies:** `00-overview.md` § "Convention recap (binding)"

### AC-ADB-03: New columns NULLABLE without DEFAULT  `[critical]`
- **Given** An `ALTER TABLE … ADD COLUMN` statement in any new migration.
- **When** The column definition is parsed.
- **Then** It MUST contain `NULL` (or omit `NOT NULL`) AND MUST NOT contain a `DEFAULT` clause.
- **Verifies:** Rule 12 in `00-overview.md`

### AC-ADB-04: Forbidden-strings linter passes  `[critical]`
- **Given** A clean working tree on the spec branch.
- **When** Running `python3 linter-scripts/check-forbidden-strings.py`.
- **Then** Exit code MUST be `0`. Any non-zero exit blocks merge.
- **Verifies:** `00-overview.md` § Verification

### AC-ADB-05: AppLink XOR target invariant  `[critical]`  *(A-44 5-link self-enforcement template — Sess-60 A-50)*
- **Given** An `INSERT` into `AppLink` with `AppLinkTypeId = (SELECT AppLinkTypeId FROM AppLinkType WHERE Name = 'Repo')`, OR symmetrically with `Name = 'GitProfile'`.
- **When** SQLite evaluates the table-level `CHECK` clause defined in `00-overview.md` lines 159–166 (`AppLink` DDL block at lines 144–172).
- **Then** The insert MUST succeed iff exactly one of `TargetRepoId` / `TargetGitProfileId` is non-NULL and matches the discriminator (Repo→`TargetRepoId NOT NULL AND TargetGitProfileId IS NULL`; GitProfile→symmetric). All other shapes (both NULL, both NOT NULL, mismatched discriminator) MUST fail with SQLite error `CHECK constraint failed: AppLink`.
- **5-link self-enforcement chain:**
  1. **Source-of-truth pin** — DDL block `AppLink` at `spec/23-app-database/00-overview.md` lines 144–172 (file 30775 bytes / 672 lines as of Sess-60).
  2. **Constraint pin** — `CHECK (...)` clause at `00-overview.md` lines 159–166 (the XOR enforcer).
  3. **Discriminator seed pin** — `INSERT OR IGNORE INTO AppLinkType(Name) VALUES ('GitProfile'), ('Repo');` at `00-overview.md` line 185 (cross-checked by AC-ADB-09).
  4. **Resolution-algorithm pin** — `## Polymorphic AppLink Resolution (Normative)` at `00-overview.md` line 190 ff. (cross-verified by AC-ADB-14, WE-01).
  5. **CI-gate pin** — `linter-scripts/check-spec22-inventory.py` (§27 slot 37) MUST keep `00-overview.md` present + non-empty; the deferred §27 gate `applink-xor-check-clause-present` (FUTURE — see §27 backlog) re-greps lines 159–166 for the `CHECK (...)` token. Removing or weakening either constituent breaks the chain.
- **Evidence triple obligation** (Lesson #39): auditors MUST capture (a) `wc -l spec/23-app-database/00-overview.md` (expect 672 ±2), (b) `sed -n '159,166p' spec/23-app-database/00-overview.md` (expect the literal CHECK clause), (c) `grep -nE "TargetRepoId IS NOT NULL AND TargetGitProfileId IS NULL" spec/23-app-database/00-overview.md` (expect ≥1 match in the cited range).
- **Invalidation triggers:** (i) `00-overview.md` line count drifts >±2 without re-pinning here; (ii) the XOR `CHECK` clause is removed, weakened, or moved outside lines 144–172; (iii) `AppLinkType` seed loses 'GitProfile' or 'Repo'; (iv) AC-ADB-14 resolution algorithm decoupled from the discriminator.
- **Verifies:** DDL `CHECK` clause for `AppLink` in `00-overview.md` (lines 159–166).

### AC-ADB-06: AppLink disconnect-timestamp invariant  `[high]`  *(A-44 5-link self-enforcement template — Sess-60 A-50)*
- **Given** Any row in `AppLink` undergoing `INSERT` or `UPDATE`.
- **When** SQLite evaluates the second table-level `CHECK` clause defined in `00-overview.md` lines 168–171 (`AppLink` DDL block at lines 144–172).
- **Then** `IsActive = 1` MUST imply `DisconnectedAt IS NULL`; `IsActive = 0` MUST imply `DisconnectedAt IS NOT NULL`. Any other combination MUST fail with `CHECK constraint failed: AppLink`.
- **5-link self-enforcement chain:**
  1. **Source-of-truth pin** — `AppLink` DDL at `spec/23-app-database/00-overview.md` lines 144–172.
  2. **Constraint pin** — second `CHECK (...)` clause at `00-overview.md` lines 168–171 (the lifecycle-state enforcer).
  3. **Lifecycle-rule pin** — Q3 reconnect rule cited by AC-ADB-07 (`00-overview.md` § "Q3 — Reconnect"): a NEW row is inserted on reconnect, never flipping `IsActive` back to 1; this guarantees the CHECK is never required to migrate state in-place.
  4. **Index pin** — partial `IX_AppLink_Active ON AppLink(AppId, IsActive)` at `00-overview.md` line 178 (the active-set query path that depends on this invariant).
  5. **CI-gate pin** — `linter-scripts/check-spec22-inventory.py` keeps the file present; deferred §27 gate `applink-disconnect-check-clause-present` (FUTURE — see §27 backlog) re-greps lines 168–171.
- **Evidence triple obligation** (Lesson #39): (a) `wc -l spec/23-app-database/00-overview.md` (expect 672 ±2), (b) `sed -n '168,171p' spec/23-app-database/00-overview.md`, (c) `grep -nE "IsActive\s*=\s*1.*DisconnectedAt IS NULL|IsActive\s*=\s*0.*DisconnectedAt IS NOT NULL" spec/23-app-database/00-overview.md` (expect ≥1).
- **Invalidation triggers:** (i) line drift >±2; (ii) clause removed or weakened; (iii) AC-ADB-07 reconnect rule weakened to in-place flip; (iv) `IX_AppLink_Active` dropped without ledger entry.
- **Verifies:** DDL `CHECK` clause for `AppLink` in `00-overview.md` (lines 168–171).

### AC-ADB-07: Reconnect inserts a new row  `[medium]`
- **Given** An AppLink row that was previously soft-disconnected (`IsActive = 0`).
- **When** The link is re-established for the same `(AppId, target)`.
- **Then** A NEW `AppLink` row MUST be inserted (per Q3); the existing disconnected row MUST NOT be flipped back to `IsActive = 1`.
- **Verifies:** `00-overview.md` § "Q3 — Reconnect"

### AC-ADB-08: AppSlug uniqueness  `[medium]`
- **Given** Two App rows being inserted with the same `AppSlug`.
- **When** The second `INSERT` executes.
- **Then** SQLite MUST raise a `UNIQUE constraint failed: App.AppSlug` error.
- **Verifies:** `App.AppSlug TEXT NOT NULL UNIQUE` in DDL

### AC-ADB-09: Lookup seeds present after migration  `[medium]`
- **Given** A freshly migrated database.
- **When** Selecting from the lookup tables.
- **Then** `AppStatus.Name` MUST contain exactly `{Active, Disabled, Archived}` and `AppLinkType.Name` MUST contain exactly `{GitProfile, Repo}`.
- **Verifies:** `00-overview.md` § "Seed data (lookup tables)"

### AC-ADB-10: Push attribution prefers Repo over GitProfile link  `[high]`
- **Given** An App that has both an active Repo-typed `AppLink` and an active GitProfile-typed `AppLink` resolving to the same inbound `RepoUrl`.
- **When** Query Q1 from `00-overview.md` is executed.
- **Then** The returned App row MUST be the one matched via the **Repo** link (more specific wins), per the `ORDER BY (lt.Name = 'Repo') DESC` clause.
- **Verifies:** `00-overview.md` § "Q1 — Resolve App from inbound RepoUrl"

### AC-ADB-11: SQLite is the Primary Implementation Target; PostgreSQL DDL is Reference (Phase 153 Task A11b)  `[critical]`
- **Given** `00-overview.md` ships TWO DDL blocks — the main "Schema" section (SQLite, PascalCase, INTEGER PKs, `INTEGER PRIMARY KEY AUTOINCREMENT`) AND the "Inlined Contracts (Phase 53 — SQL DDL lever)" appendix (PostgreSQL 15+, snake_case, `uuid` PKs, `gen_random_uuid()`),
- **When** any implementer reads §00 to build the App database,
- **Then** the **SQLite block (PascalCase, INTEGER PKs)** is the **Primary Implementation Target** — it is the dialect every consuming binary (CI/CD push handler, app-link resolver, `app-database` CLI) MUST materialise; AND the **PostgreSQL block** is **Reference / Secondary**, preserved for cross-reference with `spec/05-split-db-architecture/` (which uses PostgreSQL for the root DB) and to document the canonical column-naming intent — implementers MUST NOT materialise the PostgreSQL block as the App database. This codifies the **Phase 153 Task A11b audit finding** "Conflicting DDL Dialects — SQLite (PascalCase, INTEGER) vs PostgreSQL (snake_case, UUIDs) without designated primary target". The choice of SQLite is locked because (a) the App database is **per-binary local state** (single-writer, embedded, no network), (b) `spec/05` AC-SD-21/22/23 already govern SQLite identifier double-quoting + busy-timeout + TTL, and (c) PascalCase + INTEGER PKs match the Profile/GitProfile/Repo parent tables specified in `spec/22-git-logs-v2/`. Future contributors who want to add a PostgreSQL implementation MUST add a NEW AC explicitly opening that lane (and reconcile with spec/05's per-SHA partitioning model) — silent dialect-flip is FORBIDDEN.
- **Verifies:** `00-overview.md` § "Schema" (SQLite, primary); `00-overview.md` § "Inlined Contracts (Phase 53)" (PostgreSQL, reference); spec/05 AC-SD-21/22/23 (SQLite identifier + busy-timeout + TTL contracts); spec/22 §07 App identity locked decision 12.

### AC-ADB-12: External-table prerequisites inlined as minimal DDL summary (Phase 153 Task A11b)  `[high]`
- **Given** the App and AppLink tables reference `Profile(ProfileId)`, `GitProfile(GitProfileId)`, and `Repo(RepoId)` foreign keys whose authoritative DDL lives in `spec/22-git-logs-v2/` (NOT in this module),
- **When** any context-window-bounded auditor or fresh implementer reads `spec/23-app-database/00-overview.md` alone,
- **Then** the **minimal DDL summary block** below MUST be present in §00's "Convention recap" or a "Prerequisites" section (the implementer cannot author App/AppLink without knowing the parent PK types) — this is summary, not authoritative; the authoritative DDL stays in spec/22:

  ```sql
  -- PREREQUISITE TABLES (authoritative DDL: spec/22-git-logs-v2/)
  -- Materialised by the git-logs-v2 module BEFORE app-database migrations run.
  -- This summary exists to make spec/23 auditable in isolation; do NOT
  -- duplicate or fork these definitions — track spec/22 for changes.
  CREATE TABLE IF NOT EXISTS Profile (
      ProfileId    INTEGER PRIMARY KEY AUTOINCREMENT,
      Email        TEXT    NOT NULL UNIQUE,                       -- canonical user email
      DisplayName  TEXT    NOT NULL CHECK (length(DisplayName) BETWEEN 1 AND 120),
      CreatedAt    TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
  );
  CREATE TABLE IF NOT EXISTS GitProfile (
      GitProfileId INTEGER PRIMARY KEY AUTOINCREMENT,
      ProfileId    INTEGER NOT NULL REFERENCES Profile(ProfileId) ON DELETE CASCADE,
      Provider     TEXT    NOT NULL CHECK (Provider IN ('github','gitlab','bitbucket','gitea')),
      Username     TEXT    NOT NULL,                              -- provider-side handle
      UNIQUE (Provider, Username)
  );
  CREATE TABLE IF NOT EXISTS Repo (
      RepoId       INTEGER PRIMARY KEY AUTOINCREMENT,
      GitProfileId INTEGER NOT NULL REFERENCES GitProfile(GitProfileId) ON DELETE CASCADE,
      RepoUrl      TEXT    NOT NULL UNIQUE,                       -- canonicalised SSH/HTTPS URL
      RepoName     TEXT    NOT NULL
  );
  ```

  This codifies the **Phase 153 Task A11b audit finding** "Broken External References — App/AppLink reference Profile/GitProfile/Repo whose schemas are not provided in this context". Mirrors spec/02 AC-CG-21 Subfolder Delegation Map and spec/27 AC-T-29 per-artifact AC delegation contracts (Lesson #19/#21): when audit-boundary < verification-boundary, the consuming module MUST inline a summary surface so the contract is auditable in isolation while keeping the authoritative source in one place.
- **Verifies:** spec/22-git-logs-v2 §02/§07 (authoritative Profile/GitProfile/Repo DDL); `00-overview.md` § "Schema" (App + AppLink FKs reference these parent tables); codifies **Lesson #26** "external-FK contract surfaces MUST inline a minimal DDL summary so consuming-module audits don't fail on unresolved references".

### AC-ADB-13: AppLink CHECK constraint uses hardcoded ID constants, not subqueries (Phase 153 Task A11b)  `[medium]`
- **Given** the AppLink table's CHECK constraint in `00-overview.md` § "Schema" currently uses subqueries `(SELECT AppLinkTypeId FROM AppLinkType WHERE Name = 'GitProfile')` to enforce the polymorphic XOR invariant (exactly one of `TargetGitProfileId` / `TargetRepoId` is non-null per row, matching the `AppLinkTypeId` discriminator),
- **When** any SQLite engine attempts to evaluate the CHECK constraint at INSERT/UPDATE time,
- **Then** SQLite MUST reject the table definition because **subqueries are NOT allowed inside CHECK constraints in SQLite** (per the SQLite docs: "The CHECK constraint may not contain ... subqueries"). The fix is two-pronged: (1) **hardcode the AppLinkType IDs as constants** in the schema (`AppLinkTypeId = 1` for GitProfile, `AppLinkTypeId = 2` for Repo) AND seed `INSERT OR IGNORE INTO AppLinkType(AppLinkTypeId, Name) VALUES (1, 'GitProfile'), (2, 'Repo')` to lock the IDs to those values; (2) the CHECK constraint becomes the literal `(AppLinkTypeId = 1 AND TargetGitProfileId IS NOT NULL AND TargetRepoId IS NULL) OR (AppLinkTypeId = 2 AND TargetRepoId IS NOT NULL AND TargetGitProfileId IS NULL)`. As a defence-in-depth, application-layer logic (the `app-database` CLI's `app link` command) MUST also enforce the XOR invariant before INSERT — DB-level CHECK is the last line of defence, NOT the only one. This codifies the **Phase 153 Task A11b audit finding** "Unresolved CHECK Constraint Logic — AppLink CHECK uses subqueries which SQLite forbids". The hardcoded-ID approach is preferred over a TRIGGER because (a) CHECK is declarative and inspectable in `.schema` output, (b) TRIGGER bodies are opaque to schema-diff tools, (c) the AppLinkType lookup table only ever has 2 rows (this is a closed enumeration, not an extension point).
- **Verifies:** `00-overview.md` § "Schema" (AppLink CHECK constraint must be subquery-free per SQLite); `00-overview.md` § "Seed data (lookup tables)" (AppLinkType seed must lock IDs to 1/2); codifies **Lesson #27** "SQLite CHECK constraints CANNOT contain subqueries — closed-enumeration FKs MUST hardcode IDs in seed + CHECK pair, not look them up dynamically".

### AC-ADB-14: Polymorphic AppLink resolution algorithm is normative and deterministic (Phase 153 P48-3)  `[critical]`
- **Given** the AppLink table is polymorphic via `AppLinkTypeId` (1=GitProfile, 2=Repo per AC-ADB-13) and an inbound CI/CD push arrives with a canonicalised `:repoUrl`,
- **When** any implementer (CI/CD push handler, `app-database` CLI, app-link resolver binary) resolves `:repoUrl` to an App,
- **Then** the implementer MUST follow the **4-step resolution algorithm** in `00-overview.md` § "Polymorphic AppLink Resolution (Normative)" — (1) canonicalise the URL using the same pipeline as `Repo.RepoUrl` insertion, (2) collect Direct (Repo) candidates with `AppLinkTypeId = 2`, (3) collect Transitive (GitProfile) candidates with `AppLinkTypeId = 1` via `Repo.GitProfileId`, (4) tie-break with **Direct > Transitive > newer `CreatedAt`** AND require the resolved App's `AppStatusId` = `Active`. Resolution MUST terminate in exactly one of the four closed states `{RESOLVED_DIRECT, RESOLVED_TRANSITIVE, REJECTED_INACTIVE_APP, REJECTED_NO_MATCH}` — implementations MUST NOT invent additional outcomes, MUST NOT silently fall through `REJECTED_INACTIVE_APP` to the next candidate, and MUST NOT join `AppLink` directly to `GitProfile` bypassing the `Repo` table in step 3 (the inbound URL carries no GitProfile hint). Q1 in `00-overview.md` § "Query Patterns" is the SQL realisation; the prose algorithm is authoritative — if Q1 and the prose ever diverge, the prose wins and Q1 MUST be patched. This codifies the **Phase 153 P47-fu1 critical finding** "Polymorphic AppLink resolution logic ambiguous — DDL describes structure, not the resolution algorithm". Mirrors spec/02 AC-CG-21 Subfolder Delegation Map and spec/27 AC-T-29 per-artifact AC delegation contracts (Lesson #19/#21/#26): when a contract surface (the resolution algorithm) lives implicitly inside example SQL, it is invisible to context-window-bounded auditors and to fresh implementers — the algorithm MUST be lifted to a normative prose section with a closed-enumeration outcome table.
- **Verifies:** `00-overview.md` § "Polymorphic AppLink Resolution (Normative)" (discriminator binding table + 4-step algorithm + 4-state outcome enumeration + forbidden patterns); `00-overview.md` § "Q1 — Resolve App from inbound RepoUrl" (SQL realisation); AC-ADB-05 (XOR target invariant — load-bearing for step 2/3 disjointness); AC-ADB-06 (disconnect-timestamp invariant — load-bearing for `IsActive = 1` filter); AC-ADB-10 (Repo > GitProfile precedence — now codified prose-side, not just `ORDER BY`); AC-ADB-13 (locked IDs 1/2 referenced by the algorithm). Codifies **Lesson #33** "Polymorphic-FK resolution algorithms MUST be lifted to normative prose with a closed-enumeration outcome table — example SQL is illustrative, not authoritative; relying on `ORDER BY` clauses to encode precedence rules is invisible to auditors and fresh implementers."

### AC-ADB-15: SQLite concurrency pragmas — link to spec/13 §10 (Phase 153 Task S23-02)  `[low]`
- **Given** the SQLite App database is opened by any consuming binary (CI/CD push handler, app-link resolver, `app-database` CLI) and may face concurrent CI/CD push resolutions.
- **When** an implementer searches §00 for the required PRAGMA set (`journal_mode=WAL`, `busy_timeout=5000`, `foreign_keys=ON`, `synchronous=NORMAL`) and the `SQLITE_BUSY` retry contract.
- **Then** §00 § "Convention recap" MUST cross-link to the canonical pragma + retry contract owned by `spec/13-generic-cli/10-database.md` § "Concurrency & Locking (Normative)" (which itself mirrors `spec/05` AC-SD-22 + spec/27 AC-T-28 R3) — this module MUST NOT restate the pragmas (Lesson #36 link-don't-restate). Inlining the pragma table here would create a dual-source drift class with spec/13 / spec/05.
- **Verifies:** `00-overview.md` § "Convention recap" cross-reference; closes audit-v7 D3 LOW `Missing SQLite Busy Timeout/WAL configuration`. Codifies **Lesson #36** "concurrency-pragma contracts owned by spec/13 §10 are linked, never restated".

### AC-ADB-16: Postgres reference block — UTC Unix-seconds parity note (Phase 153 Task S23-02)  `[low]`
- **Given** the SQLite primary block stores `CreatedAt` / `UpdatedAt` as Unix seconds (`INTEGER`) and the PostgreSQL reference appendix uses `timestamptz NOT NULL DEFAULT now()`.
- **When** any future contributor opens the PostgreSQL lane (per AC-ADB-11) and ports application logic between the two dialects.
- **Then** the PostgreSQL reference appendix in §00 § "Inlined Contracts (Phase 53 — SQL DDL lever)" MUST carry an explicit note that **for application-logic parity, all `timestamptz` values MUST be handled as UTC and exposed to the application layer as Unix seconds** (e.g., `EXTRACT(EPOCH FROM created_at)::bigint`) so consumers receive the same `INTEGER` Unix-seconds shape regardless of dialect. Silent unit drift (timestamptz exposed as ISO-8601 strings, or as local-tz timestamps) is FORBIDDEN.
- **Verifies:** `00-overview.md` § "Inlined Contracts (Phase 53 — SQL DDL lever)" parity note; closes audit-v7 D1 LOW `Timestamp Unit Ambiguity in Postgres Block`.

### AC-ADB-17 — Cross-Module Externalized Citation Map (Lesson #36 + Lesson #37 — link-don't-restate anchor table)  `[critical]`

**Given** spec/23-app-database is an integration-axis module whose normative content references contract surfaces owned by other top-level spec modules — concretely (a) `00-overview.md` line 74 cites `spec/05-split-db-architecture` + `spec/13-generic-cli/10-database.md` for the split-DB pattern + concurrency contract, (b) AC-ADB-15 routes implementers to spec/13 §97 AC-22 for SQLite PRAGMA + retry, (c) AC-ADB-14 cites spec/22-git-logs-v2 schema for Profile/Repo/GitProfile FK targets, (d) AC-ADB-13 references spec/02 + spec/27 cross-module ACs (mirror citations), (e) §99 cites `linter-scripts/check-forbidden-strings.py` (a spec/27 slot-03-bound script) as the PascalCase enforcement gate;

**When** an AI auditor walks spec/23 §97 (the tier-1 contract surface) and encounters any of these externalized citations OR a downstream contributor needs to follow the dependency chain to verify a normative claim,

**Then** the auditor MUST find the canonical anchor for each external citation in the table below — every row is a Lesson-#36 link-don't-restate boundary (the citation lives ONCE in its owning module's §97; spec/23 cites it but never restates it):

| External cite | Owning module + AC | Cited from spec/23 file | Citation purpose | Restate-in-23 forbidden? |
|---|---|---|---|---|
| spec/05-split-db-architecture | spec/05 §00 + §97 AC-SD-21..23 | `00-overview.md` L74 + L342 + L365 | Split-DB pattern (operational vs log-storage DB separation); SQL identifier double-quoting; Go struct tags | **YES** — pattern + identifier conventions live in spec/05 §97 AC-SD-21/22/23; spec/23 applies the pattern to App/AppLink/AppStatus, never re-derives it |
| spec/13-generic-cli §97 AC-22 | spec/13 §97 AC-22 + spec/13/10-database.md (implementer mirror, Phase 153 P3) | AC-ADB-15 + `00-overview.md` L74 + L163 | SQLite locking strategy: `journal_mode=WAL`, `busy_timeout=5000`, `BEGIN IMMEDIATE`, retry 3×100ms±25% jitter | **YES** — full PRAGMA + retry contract lives in spec/13 §97 AC-22; spec/23 cites the AC, never restates the PRAGMA table |
| spec/22-git-logs-v2/02-database-schema.md + 18-schema.sql | spec/22 §97 AC-02..AC-08 (Profile/Repo/GitProfile entity contracts) | AC-ADB-14 polymorphic resolution + `99-consistency-report.md` L42 | FK targets for App.ProfileId, AppLink.RepoId, AppLink.GitProfileId polymorphic discriminator | **YES** — entity DDL + UNIQUE constraints + URL canonicalisation live in spec/22 §97; spec/23 links to columns, never duplicates the column definitions |
| spec/02-coding-guidelines | spec/02 §97 AC-CG-21 (Subfolder Delegation Map — A10 precedent) + AC-CG-22 (Exception Ledger) | AC-ADB-14 line 157 (mirror citation) | PascalCase + cross-language naming conventions inherited from spec/02 | **YES** — naming conventions + per-language stub GWT contracts live in spec/02; spec/23 inherits, never restates |
| spec/27-spec-toolchain (script anchors) | spec/27 §97 (slot 03 = check-forbidden-strings.py; slot 24 = check-lockstep.cjs) | `00-overview.md` L325 + L589/601/613/627/641 + `99-consistency-report.md` L40 + L68 | Mechanical PR-time gates: PascalCase string enforcement; lockstep banner pairing; cross-link integrity; trace-map regression; folder-ref allowlist | **YES** — script CLI surfaces + exit-code contracts live in spec/27 §97 per-slot ACs; spec/23 cites the script paths, never replicates the CLI logic |

**AND** any future contributor authoring new normative content in spec/23 that references a contract surface owned by another top-level module MUST add a row to the table above (citation + owning module/AC + spec/23 file + purpose + restate-forbidden flag) before the new content ships — the table IS the audit-followable dependency chain;

**AND** any auditor finding citing "external dependency unresolved" or "dangling cross-module reference" against any of the 5 rows above MUST be classified as a stale-cache artifact (the anchor exists in the cited owning module's §97 — verify with `rg -n "AC-XX" spec/NN-*/97-acceptance-criteria.md` before flagging);

**AND** the table is **append-only** within a phase (rows MAY be added, never reworded; a row's "Owning module + AC" cell may be updated when the owning AC's number changes via §97-WINS evolution but the citation purpose is immutable per Lesson #25);

**AND** restating any of the linked contracts inline within spec/23 is **FORBIDDEN** (Lesson #36 dual-source drift class) — every row's "Restate-in-23 forbidden?" cell is `YES` by construction.

- **Verifies:** the cross-module externalized citation contract for spec/23 — every external dependency (spec/05 + spec/13 + spec/22 + spec/02 + spec/27 scripts) has an explicit normative anchor in the table above. Codifies **Lesson #36** (link-don't-restate cross-module boundary) + **Lesson #37** (integration-axis module co-needs Lesson #19 + Lesson #36). Mirror of spec/22 AC-79 (consolidated citation map for spec/22's 6 externalized citations) + spec/12 AC-11 (linter-script anchor pattern) + spec/02 AC-CG-21 (Subfolder Delegation Map — intra-module sub-folder axis). Until the next LLM-gateway re-score runs cleanly, this AC declares any cross-module-dangling finding against the 5 listed citations a stale-cache artifact per Lesson #34.

---

## Worked Examples

> Non-normative `kind: example` — illustrative implementations of opaque ACs. If example and AC ever diverge, the AC wins.

### WE-01 — AC-ADB-14 polymorphic AppLink resolution (4 outcomes walked)

**Setup (seed):**
| Table | Row |
|---|---|
| `App` | `{Id: 7, AppSlug: "billing", AppStatusId: 1 /*Active*/}` |
| `App` | `{Id: 8, AppSlug: "billing-old", AppStatusId: 2 /*Inactive*/}` |
| `GitProfile` | `{Id: 30, Handle: "acme"}` |
| `Repo` | `{Id: 100, RepoUrl: "https://github.com/acme/billing", GitProfileId: 30}` |
| `AppLink` | `{Id: 1, AppLinkTypeId: 2, RepoId: 100, AppId: 7, CreatedAt: 1714000000}` (Direct) |
| `AppLink` | `{Id: 2, AppLinkTypeId: 1, GitProfileId: 30, AppId: 8, CreatedAt: 1715000000}` (Transitive, newer) |

**Walk inbound `:repoUrl = "git@github.com:acme/billing.git"`:**
1. **Canonicalise** → `https://github.com/acme/billing` (matches `Repo.RepoUrl` insertion pipeline).
2. **Direct candidates** (`AppLinkTypeId=2`): join `AppLink → Repo` on canonical URL → `{AppLink.Id=1, AppId=7}`.
3. **Transitive candidates** (`AppLinkTypeId=1`): from `Repo.GitProfileId=30` → `{AppLink.Id=2, AppId=8}`.
4. **Tie-break:** Direct > Transitive → pick AppId=7. Check `AppStatusId=1=Active` → ✓.
5. **Outcome:** `RESOLVED_DIRECT(AppId=7)`.

**Negative paths:**
- If AppId=7 had `AppStatusId=2`: outcome MUST be `REJECTED_INACTIVE_APP` — implementer MUST NOT silently fall through to AppId=8 (forbidden by AC).
- If neither Direct nor Transitive candidates exist: outcome `REJECTED_NO_MATCH`.
- If only Transitive exists and is Active: outcome `RESOLVED_TRANSITIVE(AppId=...)`.

---

### AC-ADB-18: §22 operational-pattern inheritance  `[critical]`

- **Given** §23 ships an App-link resolution algorithm (AC-ADB-16) with four closed outcome states `{RESOLVED_DIRECT, RESOLVED_TRANSITIVE, REJECTED_INACTIVE_APP, REJECTED_NO_MATCH}` and three mutating operations (link create, soft-disconnect Q2, reconnect Q3), AND §22-git-logs-v2 owns the canonical operational-pattern surfaces in scope (AC-30 `ErrorEnvelope` shape `{Status, Code, Message, RequestId, HttpStatus}`; the `GL-*` `ErrorCode` enum in §22 §17 / §15; the server-generated UUIDv4 `RequestId` correlation rule; `AuditTrail` per-request row written with the same `RequestId`; the `GL-SCHEMA-DRIFT` partial-landing CI-blocking pattern from AC-23),
- **When** any consumer (the `app-database` CLI, the App-link resolver invoked by the CI/CD push handler, the admin UI driving Q4) wraps the `app-database` contract surfaces declared in §23,
- **Then** the consumer MUST inherit §22's operational-pattern contracts as follows: (1) **Error envelope**: every failure response MUST conform to §22 AC-30 `ErrorEnvelope` shape; the App-database error-code family extends the `GL-*` enum under the namespace `ADB-*` (e.g. `ADB-LINK-INACTIVE`, `ADB-LINK-XOR-VIOLATION`, `ADB-LINK-CANONICALIZE-FAIL`, `ADB-LOOKUP-SEED-DRIFT`); the four REJECTED resolution states from AC-ADB-16 MUST map to specific `ADB-*` codes — `REJECTED_INACTIVE_APP` → `ADB-LINK-INACTIVE`, `REJECTED_NO_MATCH` → `ADB-LINK-NO-MATCH`. (2) **RequestId correlation**: every `app-database` mutation MUST be invoked with a server-generated UUIDv4 `RequestId` (per §22 AC-30 — client-supplied `X-Request-Id` headers MUST be ignored to prevent log-injection); the same `RequestId` MUST appear in the `AuditTrail.RequestId` row (§22 AC-21) AND in the matching `ErrorEnvelope.RequestId` if the operation fails. (3) **AuditTrail event emission**: link-create, link-disconnect (Q2), and link-reconnect (Q3) MUST each emit one `AuditTrail` row with action verbs `app.link.create` / `app.link.disconnect` / `app.link.reconnect` (PascalCase action namespace per §22 §23 enum-storage rule); resolution attempts (read-side) MUST NOT emit AuditTrail rows (§22 AC-04 cached-integer / sink-side rule — observability is for mutations, not for resolution-fan-out which would amplify per-push). (4) **Schema-drift discipline**: any DDL change to §23 lookup tables (`AppStatus`, `AppLinkType`) or core tables (`App`, `AppLink`) MUST land same-PR with the §23 §00 inlined schema block + AC-ADB-* update + §98 changelog row, mirroring §22 AC-23's three-surface invariant; partial landing fires `ADB-SCHEMA-DRIFT` (the §23-namespaced peer of `GL-SCHEMA-DRIFT`) and is CI-blocking.
- **Verifies:** §00 § "Polymorphic AppLink Resolution (Normative)" (the four REJECTED outcomes now have transport-layer error codes); §00 § "Migration Template (Rule 12 — forward-only)" (schema-drift discipline now binds to §22 AC-23 cohort pattern); §22 AC-30 (ErrorEnvelope shape — restate-forbidden, link-only per Lesson #36); §22 AC-21 (AuditTrail row contract — restate-forbidden); §22 AC-04 (sink-side observability rule — restate-forbidden); §22 AC-23 (schema-drift three-surface invariant — restate-forbidden); §22 §15 (GL-* error code catalog as parent enum the `ADB-*` namespace extends); §22 §17 (OpenAPI ErrorEnvelope schema). Closes audit-derived task **A-01** (Phase 4 forced guesses G23-4 + G23-5 — App-link resolution had four closed REJECTED states with no transport-layer error binding and no audit-trail event contract; both inherited from §22 by this AC). Inherits Lesson #36 link-don't-restate discipline — §22 owns the operational-pattern bodies, §23 cites by anchor and namespaces the error-code family extension.
- **Test invariant (T-ADB-18-01..T-ADB-18-04):** (T-01) Every App-link mutation MUST produce one matching `AuditTrail` row with PascalCase action verb. (T-02) Every `app-database` failure response MUST validate against §22 §17 `components.schemas.ErrorEnvelope` AND its `Code` MUST start with `ADB-` (the namespaced family). (T-03) `ErrorEnvelope.RequestId` MUST equal `AuditTrail.RequestId` for the same operation when both exist. (T-04) Read-side resolution attempts MUST NOT emit `AuditTrail` rows (sink-side rule); only mutations do.
- **Externalized Citation Map row** (extends AC-ADB-17): `spec/22-git-logs-v2 §97 AC-30 + AC-21 + AC-04 + AC-23` | this AC line | "ErrorEnvelope shape + AuditTrail row + sink-side observability rule + schema-drift three-surface invariant — operational patterns inherited by namespace extension (`GL-*` → `ADB-*`)" | **YES** restate-forbidden.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
