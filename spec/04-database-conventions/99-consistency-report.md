# Consistency Report — Database Conventions

**Version:** 3.9.3  
**Updated:** 2026-05-07  

> **v3.9.3 update (Phase F2 — Sibling File Delegation Map):** Added **AC-18 `[critical]`** to §97 — 9-row delegation table mapping all 8 spec/04 sibling files + lifecycle Mermaid to their governing §97 AC family, tier visibility, and restate-forbidden flag. Closes parent-§97 audit-boundary blind spot per Lesson #21 (intra-module axis, Lesson #39 fourth instance after spec/22 AC-80, spec/13 AC-27, spec/02 AC-CG-21). Two governed-but-unnamed siblings (`04-testing-strategy.md`, `lifecycle-04-database-conventions-p78.mmd`) classified informative-exempt with future-promotion rule. Banners: §97 v1.6.0 → **v1.7.0** (AC count 17 → 18); §00 v3.8.1 → **v3.8.2**; §98 v3.8.1 → **v3.9.0**; this file v3.9.2 → **v3.9.3**. **No CI / RUBRIC / AC-31-31 / gate-count change.** All 4 strict gates expected GREEN.

> **v3.9.2 update (Phase 153 Task F-05 — §01-naming-conventions storage-vs-naming axis cross-reference banner):** Closed audit-v8 LOW-D1 "Boolean Type Ambiguity in SQLite" finding (cache 2026-05-03) via a single Normative cross-reference banner at the top of `01-naming-conventions.md` § "Boolean Column Rules" pinning the `BOOLEAN` keyword as DDL pseudo-syntax for the naming axis only — production storage MUST follow §2.1 (AC-09) + §2.1.1 SQLite-INTEGER mandate (AC-17). No mass `BOOLEAN→INTEGER` sed (would corrupt the 50-snippet naming-axis pedagogy). HIGH-D5 NOT remediated (LLM hallucination class per Lesson #74 — file 15.8 KB on disk, "136 KB cap" is bundle-budget artifact); MEDIUM-D3 NOT remediated (would violate Lesson #36 — auditor recommends restating spec/13 AC-22 inline, the dual-source drift class is forbidden). Banners: §01-naming-conventions v3.5.0 → **v3.5.1**; §00 v3.8.0 → **v3.8.1**; §98 v3.8.0 → **v3.8.1**; this file v3.9.1 → **v3.9.2**. **No §97 change** (banner is implementer-facing prose mirror, not new contract); **no CI / RUBRIC / AC-31-31 / gate-count change**. All 5 strict gates expected GREEN. Lesson #36 (Nth instance) + Lesson #74 (1st full-baseline reinforcement) reinforced.

> **v3.9.1 update (Phase 153 Task A18-fu1 #5 — spec/04 walker-cap structural-pin + SQLite INTEGER mandate):** Closed all 3 audit-v7 cache findings (cache snapshot 2026-05-03; gateway 402 active so re-score deferred per Lesson #20). **HIGH D5 "Truncated Relationship Diagram File"**: classified STRUCTURAL-DESIGN-NOT-DEFECT — `05-relationship-diagrams.md` is **15.8 KB on disk** (verified `wc -c`), the "truncated at 136KB cap" auditor report is a Lesson #47 walker-window byte-cap artifact (sibling §02 + §97 + §00 + §98 = 83 KB consume the bundle BEFORE §05 is reached). **MEDIUM D3 "SQLite Concurrency Logic Externalized"**: already canonically closed at AC-13 + §02 §4.3 cross-ref to spec/13 AC-22 per Lesson #36 (link-don't-restate). **LOW D1 "Boolean Type Ambiguity in SQLite"**: tightened `02-schema-design.md` §2.1.1 SQLite row from `INTEGER (preferred) or BOOLEAN (alias)` to `INTEGER MANDATORY in DDL (NEVER BOOLEAN)` with rationale (declared `BOOLEAN` keyword has `NUMERIC` storage affinity); forbidden-alternatives column lists `BOOLEAN keyword (alias-trap — use INTEGER)` explicitly. Both bound by new **AC-17 `[medium]`** Lesson #34/#47 structural-pin AC. **Lesson #51 reinforced (4th instance)**: structural-pin AC pattern stable across spec/02 AC-CG-24 + spec/25 AC-AI-16 + spec/04 AC-13 + spec/04 AC-17 for recurring walker-window byte-cap artifacts. Banners: §97 v1.5.0 → **v1.6.0** (AC count 16 → 17); §00 v3.7.0 → **v3.7.1**; §02-schema-design v3.4.1 → **v3.4.2**; §98 v3.7.0 → **v3.8.0**; this file v3.9.0 → **v3.9.1**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade, no gate-count change.** All 4 strict gates expected GREEN.

> **v3.8.0 update (Phase 153 Task A24-fu13 — AC-12 boolean round-trip + AC-13 Lesson #47 structural-pin):** Closed audit-v7 MEDIUM D2 "Missing AC for Boolean Storage" via **AC-12 `[medium]`** binding §2.1 storage convention to a verifiable round-trip GWT (per-language native-bool identity + ZERO string-coercion patterns via `rg` grep-contract scoped to `biz` glob set, mirroring AC-10/AC-11). Closed recurring audit-v7 HIGH D3 "SQLite Single-Writer Bottleneck" + LOW D5 "Dangling Reference in Relationship Diagrams" via **AC-13 `[medium]`** structural-pin AC declaring both findings STRUCTURAL-DESIGN-NOT-DEFECT — HIGH D3 already canonically closed at Phase 153 P3 §4.3 cross-ref to spec/13 AC-22 (Lesson #36 link-don't-restate); LOW D5 is walker-window byte-cap artifact (link complete on disk, CI gate `check-spec-cross-links.py` confirms zero broken). AC count §97 v1.3.0 → **v1.4.0** (11 → 13). §00 v3.5.0 → **v3.6.0**; §98 v3.5.0 → **v3.6.0**; this file v3.7.0 → **v3.8.0**. **NEW Lesson #51 codified at §98 v3.6.0 row**: when the same audit-v7 HIGH recurs across rebaselines despite a prior phase canonically closing the contract elsewhere, ship a structural-pin AC locally (NOT a restatement — forbidden by Lesson #36) that cites the canonical surface, declares STRUCTURAL-DESIGN-NOT-DEFECT, and enumerates forbidden remediation patterns. Cross-axis-applicable mirror of Lesson #50 — third instance of the pattern (spec/02 AC-CG-24 + spec/25 AC-AI-16 + spec/04 AC-13). All 5 strict gates expected GREEN.


> **v3.6.2 update (Phase 153 P3 — §4.3 Concurrency Posture cross-reference):** Added `### 4.3 Concurrency Posture (Normative cross-reference)` to `02-schema-design.md`, cross-linking to spec/13 § AC-22 (canonical) + spec/13/10 § "Concurrency & Locking" + spec/13/18 § "Concurrency Discipline" — explicitly NOT re-stating the concurrency rules (schema ⊥ runtime concurrency; dual-source would drift). Companion to spec/13 §00/§98/§99 v1.1.4 which carries the implementer prose. §02-schema-design v3.4.0 → v3.4.1; §00 v3.4.0 → v3.4.1; §98 v3.4.1 → v3.4.2; §99 v3.6.1 → v3.6.2. **No §97 / AC / CI / RUBRIC / gate-count change.** Codifies Lesson #36 (cross-module cross-references MUST link, never restate — restatement is a dual-source drift class).

> **v3.6.1 update (Phase 153 Task A11a-fu3 — P1-verify HIGH sweep + spec/04 §98 path disambiguation):** Applied Lesson #34 to all 26 cache HIGHs: 10 already contract-closed; 16 remain (12 D5). Deterministic gate `check-spec-folder-refs.py` ground-truthed D5 cluster to **only 2 stale refs tree-wide** (cache overcount ≥6×). Both fixed: spec/04 §98 line 28 path widened to `02-error-architecture/05-response-envelope/`; memo `phase-153-task-A4-...md` rewrote `spec/11-style` → `spec-11-style`. §98 v3.4.0 → **v3.4.1**; §99 v3.6.0 → **v3.6.1**. No §97/AC/CI/RUBRIC change. All 4 strict gates GREEN. **Lesson #35**: never use `.../<leaf>/` shorthand when `<leaf>` matches `\d{2}-[a-z0-9-]+` — spell out the deep path so the gate's display can't mislead.


> **v3.6.0 update (Phase 153 P48-2 — Cross-Language Boolean Storage Convention):** Closes the **P47-fu1 critical finding** "04-db cross-lang boolean conventions" (surfaced in `mem://index.md` line 55 as one of 5 critical findings carried into the P48 backlog). Added `## 2.1 Cross-Language Boolean Storage Convention (Normative)` to `02-schema-design.md` with four normative subsections: per-engine storage table (SQLite / MySQL/MariaDB / PostgreSQL × allowed values × forbidden alternatives); per-language scan/insert pattern table (Go / PHP / Rust / C# / TypeScript × scan target × insert literal × notes); tri-state `NULL` exception clause (only when modelling genuine three-valued logic); migration discipline (NOT NULL DEFAULT 0 / FALSE, positive-only rename rule, type-swap precondition with orphan-value check). Bound as **AC-09** in §97 (count 8 → 9). Cross-references `spec/02-coding-guidelines/01-cross-language/02-boolean-principles/00-overview.md` (storage-vs-naming axis split — naming = §02 CG, storage = §04 DB-conv). Banners: §00 v3.3.3 → **v3.4.0**; §97 v1.1.0 → **v1.2.0**; §02-schema-design v3.3.0 → **v3.4.0**; §98 v3.3.3 → **v3.4.0**; §99 v3.5.1 → **v3.6.0**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade, no gate-count change.** Lockstep 87/87 · tree-health 168/168 strict · version-parity 74/74 — all GREEN. **Lesson #32** (codified inside §98 P48-2 row): P47-fu1 backlog items survived 7+ phases without resolution because findings were buried in a single index-line memo with no per-finding tracker; future phase-spanning audit findings MUST get one-finding-per-file trackers under `.lovable/memory/audit/` so individual closures are discoverable (mirror of Lesson #30 — #30 is "verify before opening" while #32 is "anchor at source so verification is possible").

> **v3.5.1 update (Phase 153 Task A2 — envelope inlining):** Closes audit-v2 D5 finding "cross-module response-envelope dependency" by inlining a verbatim envelope summary at the end of §00 (top-level field table + reference JSON + Go `omitempty` note). Upstream `spec/03-error-manage/.../04-response-envelope-reference.md` remains the source of truth; the inlined block is a courtesy copy for context-bounded AIs. §00 banner v3.3.2 → v3.3.3 (h10 30 → 153); §98 release row 3.3.3 added. No AC change, no CI gate change.


> **v3.5.0 update (Phase P48-1-fu1-batch P3 sweep slot 3 — AC-01..AC-08 Verifies clauses):** Closes the P3-tier `**Verifies:**` gap for this module (0 → 8 clauses). Each AC now declares the invariant or precedent it defends, completing the contract graduation from Medium → High AI-confidence per `01-spec-authoring.md` § *AI Confidence Rubric (normative)* gate P3. Lockstep: §00 banner 3.3.1 → 3.3.2 (date 2026-04-28 → 2026-04-29), §97 banner 1.0.0 → 1.1.0, §98 release row 3.3.2 added, §99 banner 3.4.0 → 3.5.0. No score change to tree-health (168/168 strict-pass holds); P3 contribution to AC-09's four-gate derivation now passes. Pattern reused verbatim from slot 2 (`spec/17-consolidated-guidelines`) — see Core memory entry on `**Verifies:**` as the highest-leverage AI-implementability uplift.

> **v3.4.0 update (Phase P30 — P28-style hybrid batch reconciliation):** §98 reconstructed from 0 post-footer prose block(s) + 1 dual-stream alignment row + 1 final patch reconciliation row. §98 header `1.1.0`→`3.3.1`; §00 banner `3.3.0`→`3.3.1`; H10 stamp added; date sync `→2026-04-28`. Part of Phase P30 batch (23 modules).
**Last Updated:** 2026-04-30

---

## Module Health
<!-- verified-phase: 153 -->

| Criterion | Status |
|-----------|--------|
| `00-overview.md` present | ✅ |
| `99-consistency-report.md` present | ✅ |
| Lowercase kebab-case naming | ✅ |
| Unique numeric sequence prefixes | ✅ |
| Canonical reference DDL inlined (Phase 20 G-CON-01) | ✅ |
| Changelog row matches overview version | ✅ |

**Health Score:** 100/100 (A+)

---

## File Inventory

| # | File | Status |
|---|------|--------|
| 00 | `00-overview.md` | ✅ Present (v3.3.0) |
| 01 | `01-naming-conventions.md` | ✅ Present |
| 02 | `02-schema-design.md` | ✅ Present |
| 03 | `03-orm-and-views.md` | ✅ Present |
| 04 | `04-testing-strategy.md` | ✅ Present |
| 05 | `05-relationship-diagrams.md` | ✅ Present |
| 06 | `06-rest-api-format.md` | ✅ Present |
| 07 | `07-split-db-pattern.md` | ✅ Present |
| 97 | `97-acceptance-criteria.md` | ✅ Present |
| 98 | `98-changelog.md` | ✅ Present (v1.1.0) |
| 99 | `99-consistency-report.md` | ✅ Present (v3.3.0) |

**Total:** 11 files

---

## Cross-Reference Validation

All internal links verified valid. ✅

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-26 | 3.3.0 | Phase 20 Module #6 — inlined canonical DDL contract, fixed inventory to include slots 07/97/98, audit medium-priority issue cleared. |
| 2026-04-30 | 3.7.0 | Phase 153 Task A21 — added AC-10 (ORM-First) + AC-11 (View-based joins) closing audit-v7 HIGH D2; banners §97 1.3.0 / §00 3.5.0 / §98 3.5.0 / §99 3.7.0; Lesson #44 codified. |
| 2026-04-02 | 1.0.0 | Initial module created with 5 spec files. |
