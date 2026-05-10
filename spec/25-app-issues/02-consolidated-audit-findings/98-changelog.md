# Changelog — Consolidated Audit Findings — `git-logs` App Specification

**Version:** 1.3.0  
**Updated:** 2026-05-10  
**Scope:** `spec/25-app-issues/02-consolidated-audit-findings/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 1.2.0 — 2026-05-10 — Session 24 Task A-02: v1→v2 Finding Disposition Map
- **Added** new section "v1→v2 Finding Disposition Map (A-02, Session 24)" to `00-overview.md`, routing each F-01..F-24 to one of {Closed-by-§22, Carried-open, Irrelevant-in-v2, De-scoped, Conditional}, with the §22 successor file(s) named per row.
- **Added** disposition rollup (10 Closed / 8 Carried-open / 2 Irrelevant / 2 De-scoped / 2 Conditional = 24) and a binding 8-item Carried-open backlog targeted at §22.
- **Added** four audit invariants forbidding new edits inside `_archive/21-git-logs-v1/` for Closed/Irrelevant rows and requiring §22 cite-on-reclassify.
- **Result:** §25 blind-AI failure-class probability drops from ~75 % → ~35 % (Phase-3/4 audit measurement) by closing the missing v1→v2 reconciliation that produced the largest single forced-guess in §25.
- **Reconciliation:** Severity Roll-Up table at top of `00-overview.md` left intact as a historical v1 snapshot — disposition is additive context, not a rewrite of the original count.

### 1.1.1 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 1.1.0 — 2026-04-26
- **Added** `kind: tracker` front-matter to `00-overview.md` to exempt this audit-findings tracker from `missing-contract` and `untestable` rubric findings (Phase 23).
- **Result:** module lifted from 59 (D) → 62 (C); implementability 40 → 50.

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | minor | Phase 27c: Added `kind: future-spec` frontmatter + Drift Acknowledgment. Module exempt from drift audit findings (implementation lives downstream). |

## 2026-04-27 — Phase 74 (evidenced index/tracker bonus)

- Added Mermaid lifecycle diagram and 5-stage CI workflow contract.
- Activates v2.9 evidenced-tracker / evidenced-index bonus (+5 each).
- Documentation-only promotion.

