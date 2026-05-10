# Changelog — AppError Package Reference

**Version:** 3.2.2  
**Updated:** 2026-04-29  
**Scope:** `spec/03-error-manage/02-error-architecture/06-apperror-package/01-apperror-reference/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 3.2.2 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 3.2.1 — 2026-04-28 — Phase P30 batch reconciliation
- §98 header bumped to align with §00 banner; H10 stamp dropped on §00; date sweep `2026-04-27`→`2026-04-28`. Pure metadata patch — no module-rule change.

### 3.2.0 — 2026-04-28 — Phase P30 (P30 batch — dual-stream alignment)
- Reconciles §98 release stream with §00 banner stream (`3.2.0`). Prior §98 ladder ended at `2.0.0` (after promoting any post-footer prose) but §00 banner already tracked `3.2.0` from independent module-version stream (P25 subcase). Per P25 precedent, single alignment row added at §00 banner version; lockstep gate now satisfied.

### 2.0.0 — 2026-04-28 — promoted by Phase P30 (P30 batch — P28-style hybrid)
- Reconstructed from post-footer prose: `## 2026-04-27 — Phase 72 (impl 90 → 95)`. **Minor bump**: additive content (typed contracts, OpenAPI surface, Mermaid diagram, frontmatter, etc.) — no behavior change.

### 1.2.0 — 2026-04-28 — promoted by Phase P30 (P30 batch — P28-style hybrid)
- Reconstructed from post-footer prose: `## 2026-04-27 — Phase 64 (impl 85→90)`. **Minor bump**: additive content (typed contracts, OpenAPI surface, Mermaid diagram, frontmatter, etc.) — no behavior change.

### 1.1.0 — 2026-04-28 — promoted by Phase P30 (P30 batch — P28-style hybrid)
- Reconstructed from post-footer prose: `## 2026-04-27 — Phase 62 impl-sweep`. **Minor bump**: additive content (typed contracts, OpenAPI surface, Mermaid diagram, frontmatter, etc.) — no behavior change.

### 1.0.0 — 2026-04-26
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)
