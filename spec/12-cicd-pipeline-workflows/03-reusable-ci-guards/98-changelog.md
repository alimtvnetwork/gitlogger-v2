# Changelog — Reusable CI Guards — AI-Implementation Guide

**Version:** 1.0.2  
**Updated:** 2026-05-04  
**Scope:** `spec/12-cicd-pipeline-workflows/03-reusable-ci-guards/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 1.0.2 — 2026-05-04 — Phase 153 A24-fu43-fu1: AC-CG-09 archetype runtime GWT
- **Added** §97 v1.1.0 → **v1.2.0**: **AC-CG-09** [high] (forbidden-name guard runtime contract) covering diff-scope, exit-code separation (1=finding, 2=infra), output format, config schema (`forbidden-names.yaml`), language-adapter contract, and baseline regeneration + 4 forbidden patterns. Closes parent `spec/12-cicd-pipeline-workflows/97-acceptance-criteria.md` AC-13 [medium] stub mandate for the reusable-ci-guards axis. Closes audit-v7 finding `[D2 HIGH] Archetype GWT Stubs` for this subfolder.
- **Lockstep**: §00/§98/§99 patch-bump to absorb §97 minor (banner-only).

### 1.0.1 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

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

## 2026-04-27 — Phase 63 impl-sweep

- Phase 63: appended Reusable CI Guards enums TS enum mirror to satisfy `has_ts_enums` rubric (impl 80 → 90).

## 2026-04-27 — Phase 76 (impl 90 → 100)

- Added Mermaid lifecycle diagram — satisfies `has_mermaid` (+5).
- Added SQL DDL audit-log schema — satisfies `has_sql_ddl` (+20).
- Implementability raised 90 → 100 (deterministic audit, capped).

