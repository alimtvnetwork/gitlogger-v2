# Changelog — Research

**Version:** 3.3.5  
**Updated:** 2026-04-30 (Phase 153 Task A24-fu — AC-10 v7-finding tri-closure (D1 CHECK + D3 path-resolution + D5 script-binding); EXCELLENT-band push per Lesson #44 audit-corpus axis multipliers)
**Scope:** `spec/10-research/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 3.3.5 — 2026-04-30 — Phase 153 Task A24-fu (AC-10 v7-finding tri-closure — EXCELLENT-band push)
- **Added** AC-10 `[critical]` to §97 (v1.2.0 → v1.3.0) closing all three v7 audit findings against this module: (a) D1 LOW Registry Table Type Mismatch — adds CHECK constraint enforcing ISO-8601 on `AuthoredAt` + GLOB pin on `Domain`; (b) D3 MEDIUM Ambiguous On-Disk Resolution — defines 5-row normative table covering base path / case sensitivity / symlinks / domain pattern / resolution order; (c) D5 HIGH Unresolved External Script Dependencies — adds 4-row script-binding table delegating each linter contract to its owning spec/27 §97 AC family per Lesson #36 (link-don't-restate). Per Lesson #44 `audit-corpus` axis multipliers (D4×1.5 + D5×1.5), tri-closure projects EXCELLENT-band re-score (87 → 92+ expected). Pre-flight verified per Lesson #45 graduated rule: tier-1 bundle ~12 KB + AC-10 ~3 KB = well under 75 KB saturation threshold; total tree bundle ~36 KB stays under 90 KB walker cap. §00 banner 3.3.4 → 3.3.5; §97 1.2.0 → 1.3.0; §98 release row 3.3.5 added; §99 banner 1.3.2 → 1.3.3 + row added. LLM re-score deferred per Lesson #20 (HTTP 402).

### 3.3.4 — 2026-04-30 — Phase 153 Task A13 (child slot v2.1.0 close-out)
- **Changed (banner-only)** Patch-bump of parent banners (3.3.3 → 3.3.4) catching child slot `01-research-index/` v2.0.0 → v2.1.0 (AC-RESEARCH-05 Verifies + AC-RESEARCH-07 domain-registry validator AC). Closes v6 audit D2 LOW + D3 MEDIUM findings on the child contract (the third v6 finding `lifecycle-*.mmd` D5 HIGH remains pinned upstream by §97 AC-9 — Lesson #29 harness-bundling-cap). Parent §97/§00 surface unchanged.

### 3.3.2 — 2026-04-29 — Phase P48-1-fu1-batch P3 sweep slot 4 (AC-01..AC-08 Verifies clauses)
- **Added** `**Verifies:**` clauses to AC-01 through AC-08 in `97-acceptance-criteria.md` (v1.0.0 → v1.1.0). Each clause cites the precise invariant defended; AC-01 + AC-06 also note this module's `kind: index` YAML exemption (intentionally empty until child specs land — exempt from `missing-contract` but NOT from structural floor). Closes the P3-tier gap (0/8 → 8/8 Verifies) and graduates this module's AC-block from Medium → High AI-confidence per `01-spec-authoring.md` § *AI Confidence Rubric (normative)*. No semantic change to acceptance surface — purely a verifiability uplift. §00 banner 3.3.1 → 3.3.2; §97 1.0.0 → 1.1.0; §99 row added.

### 3.3.1 — 2026-04-28 — Phase P30 batch reconciliation
- §98 header bumped to align with §00 banner; H10 stamp dropped on §00; date sweep `2026-04-27`→`2026-04-28`. Pure metadata patch — no module-rule change.

### 3.3.0 — 2026-04-28 — Phase P30 (P30 batch — dual-stream alignment)
- Reconciles §98 release stream with §00 banner stream (`3.3.0`). Prior §98 ladder ended at `2.0.0` (after promoting any post-footer prose) but §00 banner already tracked `3.3.0` from independent module-version stream (P25 subcase). Per P25 precedent, single alignment row added at §00 banner version; lockstep gate now satisfied.

### 2.0.0 — 2026-04-28 — promoted by Phase P30 (P30 batch — P28-style hybrid)
- Reconstructed from post-footer prose: `## 2026-04-27 — Phase 74 (evidenced index/tracker bonus)`. **Minor bump**: additive content (typed contracts, OpenAPI surface, Mermaid diagram, frontmatter, etc.) — no behavior change.

### 1.2.0 — 2026-04-28
- **Phase 139 — Stale §99 prose refresh.** §99 Summary block carried `Health Score: 60/100 (D — placeholder)` and 2 stale warnings (`missing 97-acceptance-criteria.md`, `missing example/template`) that were already fixed on disk and superseded by the rubric-v2 strict 100/100 (Phase 137). Updated §99 to v1.1.0 with rubric-v2 score, cleared warnings, added Validation History row. No file content moved; pure documentation alignment.

### 1.1.0 — 2026-04-26
- **Phase 24 — `kind: index` exemption.** Added YAML front-matter `kind: index` to `00-overview.md` to mark this module as a placement-rule router (intentionally empty / index-only). Audit script v2.2 honours the exemption, removing `missing-contract` and `untestable` rubric findings. Result: module lifted from C-tier to B-tier in the v2-deterministic audit.

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

## 3.3.3 — 2026-04-30 — Phase 153 (inventory-pin)

- Added **AC-9** (Module asset inventory pin) — Lesson #29 module asset inventory pin. Auditor-authoritative on-disk inventory declaration; closes audit-v6 HIGH [D5] missing-files class as bundling-cap artifact (cache-stale per Lesson #34 until A8 LLM re-score). Lockstep §00/§97/§98/§99 patch+minor coordinated.

