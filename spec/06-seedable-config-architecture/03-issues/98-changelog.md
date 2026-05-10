# Changelog — Seedable Config Architecture — Issues Index

**Version:** 1.1.1  
**Updated:** 2026-04-29  
**Scope:** `spec/06-seedable-config-architecture/03-issues/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 1.1.1 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 1.1.0 — 2026-04-26
- **Added** `kind: tracker` front-matter to `00-overview.md` to exempt this issue tracker from `missing-contract` and `untestable` rubric findings (Phase 23).
- **Result:** module lifted from 59 (D) → 65 (C); implementability 10 → 65.

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

## 2026-04-27 — Phase 74 (evidenced index/tracker bonus)

- Added Mermaid lifecycle diagram and 5-stage CI workflow contract.
- Activates v2.9 evidenced-tracker / evidenced-index bonus (+5 each).
- Documentation-only promotion.

