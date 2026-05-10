# Consistency Report — 23-app-database

**Version:** 2.1.5
**Updated:** 2026-05-10

> **v2.1.5 update (Sess-64 / Phase-5 T-02 — boolean-uniformity verification pass):** Negative-evidence sweep over §00 PRIMARY-lane DDL (lines 105–385) for any `boolean`/`BOOLEAN`/`tinyint`/`BOOL ` token or non-`Is/Has`-prefixed boolean column. **Result: 0 violations.** Single boolean column in PRIMARY lane is `IsActive INTEGER NOT NULL  -- 0/1` (file-line 174, AppLink table) — fully conformant with Convention recap line 99 (`INTEGER 0/1 + Is prefix`). REFERENCE lane's `boolean NOT NULL DEFAULT true` (line ~432) is fenced by Sess-64 / T-01 precedence pin (`🚫 REFERENCE-ONLY … DO NOT MATERIALISE`) — not in scope for boolean-uniformity check. Closes Phase-5 audit finding F-23-02 by verification (no remediation edit required). Audit method recorded for future regression: `sed -n '105,385p' 00-overview.md | grep -nE 'boolean|BOOLEAN|TINYINT|tinyint|BOOL '` — MUST return zero matches. Banners: §99 v2.1.4 → **v2.1.5** (this entry); §98 v4.6.0 → **v4.7.0**. **No §00 edit (verification confirms compliance), no §97 bump.**

> **v2.1.4 update (Phase 154 C-Sweep — Cross-Module Externalized Citation Map):** Added **AC-ADB-17** `[critical]` Cross-Module Externalized Citation Map per Lessons #36 + #37; explicit normative anchor table for 5 externalized citations (spec/05 split-DB, spec/13 §97 AC-22, spec/22 entity DDL, spec/02 naming conventions, spec/27 script gates). Mirror of spec/22 AC-79 pattern. Closes audit-followability gap for integration-axis modules. Banners: §97 v3.3.0 → **v3.4.0** (AC 16 → 17); §00 v4.2.2 → **v4.2.3**; §98 v4.2.2 → **v4.2.3**. **No CI workflow change, no RUBRIC bump, no gate-count change, no AC-31-31 cascade.**

> **v2.1.3 update (Phase 153 Task S23-02 — close 2× LOW audit-v7 findings):** Added **AC-ADB-15** `[low]` (SQLite concurrency pragmas linked to spec/13 §10 owner per Lesson #36 — link, do not restate; closes D3 LOW `Missing SQLite Busy Timeout/WAL configuration`) and **AC-ADB-16** `[low]` (PostgreSQL reference appendix MUST expose `timestamptz` as UTC Unix seconds for application-logic parity with SQLite primary `INTEGER`; closes D1 LOW `Timestamp Unit Ambiguity in Postgres Block`). Mirrored both as a one-line bullet in §00 § "Convention recap" and a `⏱ Timestamp parity` blockquote in §00 § "Inlined Contracts (Phase 53)". Banners: §97 v3.2.0 → **v3.3.0** (AC 14 → 16); §00 v4.2.1 → **v4.2.2**; §98 v4.2.1 → **v4.2.2**. Expected re-score: 97 → ≥99 EXCELLENT. **No CI workflow change, no RUBRIC bump, no gate-count change.**

> **v2.1.0 update (Phase 153 P48-3 — Polymorphic AppLink resolution lifted to normative prose; closes 2nd of 3 P47-fu1 critical findings):** Added §00 "Polymorphic AppLink Resolution (Normative)" section with discriminator→target binding table, 4-step deterministic resolution algorithm, 4-state closed-enumeration outcome table (`RESOLVED_DIRECT` / `RESOLVED_TRANSITIVE` / `REJECTED_INACTIVE_APP` / `REJECTED_NO_MATCH`), and forbidden-patterns list. Bound as **AC-ADB-14** (`[critical]`) with cross-references to AC-ADB-05/06/10/13. Banners: §00 v4.0.3 → **v4.1.0**, §97 v3.1.0 → **v3.2.0** (count 13→14), §98 v4.0.2 → **v4.1.0**, §99 v2.0.3 → **v2.1.0**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade.** **Lesson #33**: Polymorphic-FK resolution algorithms MUST be lifted to normative prose with closed-enumeration outcomes — example SQL is illustrative, not authoritative; relying on `ORDER BY` clauses to encode precedence is invisible to auditors and fresh implementers (mirror of Lessons #19/#21/#26 — audit-boundary < verification-boundary requires inlined contract surface).

> **v2.0.3 update (Phase 153 Task A11b — spec/23 self-lift 75 → ≥88; AC-ADB-11/12/13 close all 3 v4 findings):** **AC-ADB-11** designates SQLite (PascalCase, INTEGER PKs) as Primary Implementation Target and PostgreSQL block as Reference (closes HIGH D1 conflicting DDL dialects). **AC-ADB-12** mandates inline minimal-DDL summary for prerequisite Profile/GitProfile/Repo tables (authoritative DDL stays in spec/22; mirrors spec/02 AC-CG-21 / spec/27 AC-T-29 delegation pattern — closes HIGH D5). **AC-ADB-13** replaces subquery-based AppLink CHECK constraint with hardcoded ID constants (1=GitProfile, 2=Repo) — SQLite forbids subqueries in CHECK (closes MEDIUM D3). Banners: §97 v3.0.0 → **v3.1.0** (AC count 10 → 13); §00 v4.0.2 → **v4.0.3**, §98 v2.0.2 → **v2.0.3**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade.** **Lesson #26**: External-FK contract surfaces MUST inline a minimal DDL summary so consuming-module audits don't fail on unresolved references. **Lesson #27**: SQLite CHECK constraints CANNOT contain subqueries — closed-enumeration FKs MUST hardcode IDs in seed + CHECK pair.

> **v2.0.2 update (Phase 153 Task #29e):** Phase 153 Task #29e — promoted `**AI Confidence:**` from `High` to `Production-Ready`. Pure banner edit: this module already passes P1+P2+P3+P4 per `check-ai-confidence.py`; the prior `High` value was a stale underclaim. **No AC change, no CI workflow change, no RUBRIC bump.**
**Scope:** `spec/23-app-database/`

> **v2.0.1 update (Phase P13 — "Split `00-overview.md` (554 lines)" closed as STALE):** Backlog item inherited from audit-v4 (45/100 baseline, superseded by audit-v5 per Phase 130). Re-audit on 2026-04-28 confirms zero split required: file is one cohesive SSOT contract for the App table family; "Open Items" below already lists splitting as optional with "No mandatory open items"; slot policy reserves `01..04` for if/when per-column commentary outgrows the inline DDL — condition not triggered. Splitting now would fragment the contract and burn 4 immutable slots prematurely. No content changed in `00-overview.md`. §98 / §99 patch-bumped to record the audit disposition. Future split proposals against §23 MUST cite a concrete trigger (per-column commentary >200 lines for a single table, OR a deep-dive workflow that doesn't belong in the router) — bare line-count arguments are not actionable per Phase P13 precedent (mirrors Phase P12 disposition for §28).

---

## Module Health
<!-- verified-phase: 153 -->

| Criterion | Status |
|-----------|--------|
| `00-overview.md` present | ✅ |
| `99-consistency-report.md` present | ✅ (this file) |
| `97-acceptance-criteria.md` present | ✅ (v3.0.0 — 10 concrete ACs) |
| `98-changelog.md` present | ✅ (v3.0.0) |
| Lowercase kebab-case naming | ✅ |
| Numeric prefix sequence | ✅ |
| `kind:` declared in front-matter | ✅ (`module`) |
| Inline DDL contracts | ✅ |
| Inline query patterns | ✅ |
| Migration template present | ✅ |

**Health Score:** 100/100 (A) — Phase 39a remediation complete.

---

## File Inventory

| File | Status | Version |
|------|--------|---------|
| `00-overview.md` | ✅ Present | 4.0.0 |
| `97-acceptance-criteria.md` | ✅ Present | 3.0.0 |
| `98-changelog.md` | ✅ Present | 3.0.0 |
| `99-consistency-report.md` | ✅ Present (this file) | 2.0.0 |

**Total markdown files:** 4

---

## Slot Reservations

Slots 01–96 are intentionally empty and reserved for future per-table or per-feature deep-dives. Examples that would slot in cleanly:

| Reserved slot | Likely future content |
|---------------|----------------------|
| `01-app-table.md` | Deep-dive on App columns, lifecycle transitions, audit hooks. |
| `02-app-link-resolution.md` | Algorithmic detail of Q1 push-attribution + tie-breaking. |
| `03-app-link-history.md` | Connect/disconnect timeline queries for the admin UI. |
| `04-migration-recipes.md` | Worked examples of the shadow + backfill + cutover sequence. |

These slots are immutable once shipped (per project memory rule). If content needs to move, the slot is renamed and an audit row is added below.

---

## Cross-Reference Validation

- Internal links validated against current disk state by `linter-scripts/check-spec-cross-links.py`.
- All five cross-refs in `00-overview.md` resolve to existing files (verified 2026-04-27).
- Sibling tables (`Profile`, `GitProfile`, `Repo`) live in `spec/22-git-logs-v2/02-database-schema.md` and `18-schema.sql` — relied on by AppLink FKs.

---

## Open Items

- **Optional:** Add `01-app-table.md` if/when per-column commentary outgrows the inline DDL block.
- **Optional:** Add `02-app-link-resolution.md` once the Q1 algorithm gains additional tie-breakers (e.g., explicit priority column).
- No mandatory open items.

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-25 | 1.0.0 | Auto-generated by `linter-scripts/fill-missing-consistency-reports.cjs` (Phase 2a sweep). |
| 2026-04-27 | 2.0.0 | Phase 39a — module promoted from index-only to full content; inventory + slot reservations + health score updated. AC suite expanded from 5 generic ACs to 10 concrete executable ACs. No file slot reused or renamed; immutability preserved. |

## 2026-04-27 — Phase 58 impl-sweep

- Phase 58: appended MigrationManifest JSON Schema to satisfy `has_json_schema` rubric (impl 70 → 85).

## 2026-04-27 — Phase 68 audit

- Mermaid lifecycle diagram present (`has_mermaid=true`).
- Lockstep & tree-health gates: PASS.
- Implementability promoted from 85 → 90.

### 2026-04-27 — Phase 71 deepening

- CI workflow contract inlined: 5 stages (detect, validate, lint, promote, report).
- Implementability raised 90 → 95 (deterministic audit).


### v2.1.6 — 2026-05-10 — A-55: REST/RPC contract pinned (T-06)

- New "REST / RPC Contract" section added between Q4 and Migration Template; AC-ADB-REST-01 minted.
- Regression-grep: `rg -nc '^## REST / RPC Contract|AC-ADB-REST-01' spec/23-app-database/00-overview.md` MUST return ≥2.
- Wire contract uses PRIMARY-lane PascalCase keys; boolean parity (true/false ↔ INTEGER 0/1) enforced at API boundary (R-4 invariant 2).

### v2.1.7 — 2026-05-10 — A-57: AC-ADB-13 seed-ID parity table pinned (T-10)

- Seed block rewritten to explicit `(AppLinkTypeId, Name) VALUES (1,'GitProfile'),(2,'Repo')` form for both lanes; 5-row parity matrix + 3-row Forbidden shapes table added.
- Regression-grep: `rg -nc "VALUES \(1,'GitProfile'\),\(2,'Repo'\)" spec/23-app-database/00-overview.md` MUST return ≥1; `rg -nc "INSERT OR IGNORE INTO AppLinkType\(Name\)" spec/23-app-database/00-overview.md` MUST return 0 (forbidden shape).
- Closes the line-106 deferred annotation; remediation status now "shipped v4.9.0".

### v2.1.8 — 2026-05-10 — A-58: 4 failure-path Worked Examples pinned (T-11)

- New "Worked Examples — Failure Paths" section added between REST/RPC contract and Migration Template; AC-ADB-WE-01 minted.
- WE-1 (404 unresolved), WE-2 (201 always-insert reconnect), WE-3 (422 boolean-coercion reject), WE-4 (200 idempotent disconnect with preserved timestamp).
- Regression-grep: `rg -nc '^### WE-[1-4]|AC-ADB-WE-01' spec/23-app-database/00-overview.md` MUST return ≥5.
- C3 Testability score 20 is un-conditional (no §27 gate dependency) — examples ARE the fixtures.
