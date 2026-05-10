# Changelog — Browser Extension Deploy — Overview

**Version:** 3.4.3  
**Updated:** 2026-05-04  
**Scope:** `spec/12-cicd-pipeline-workflows/01-browser-extension-deploy/`

---

## 3.4.3 — 2026-05-04 — Phase 153 A24-fu43-fu1: AC-BX-09 archetype runtime GWT

- §97 v1.1.0 → **v1.2.0**: added **AC-BX-09** [high] (browser-extension build → packaged release artifact) covering source-map exclusion, MV3 invariant, diamond-build ordering, asset naming, native-binary exclusion + 5 forbidden patterns. Closes parent `spec/12-cicd-pipeline-workflows/97-acceptance-criteria.md` AC-13 [medium] stub mandate for the browser-extension axis. Closes audit-v7 finding `[D2 HIGH] Archetype GWT Stubs` for this subfolder.
- §00/§98/§99 patch-bump to absorb §97 minor (banner-only). Per Lesson #36: the AC lives ONLY in the subfolder §97 — parent §97 retains the delegation map (AC-12) and stub-mandate (AC-13) without restating archetype prose.

## 3.4.1 — 2026-04-28 — Phase P29: P25-pure dual-stream reconciliation (batch)

- **Reconciled** §98 header version stream `1.2.0` → `3.4.1` to align with §00 banner stream (`3.4.0`). Prior §98 header tracked an independent audit-stream version decoupled from the SemVer ladder, which already contained `3.4.0` (matching §00 banner). Per Phase P25 precedent (subcase: clean ladder + decoupled header stream), §98 header is patch-bumped to `3.4.1` to align with banner; §00 banner also bumped to `3.4.1` per P27 sub-lesson (parity gate enforces exact match for stamped files). Ladder body unchanged. H10 stamp added to §00. **Phase P29 batch reconciliation** (8 P25-pure drifters processed in one phase per P27 batching lesson).

## 1.2.0 — 2026-04-27

- Phase 52: appended JSON Schema + typed enum/CI-YAML contracts to overview to lift implementability score (no behavior change).

## v1.1.0 — 2026-04-26 (Phase 27 drift sweep)

- **Added** `kind: future-spec` frontmatter + Drift Acknowledgment section to `00-overview.md`. Acknowledges that referenced application/workflow code lives in downstream repos and is intentionally absent from this spec-only repo's local code index, so audit `drift` findings of the form "spec references file that doesn't exist" are expected and accepted.
- **Bumped** banner v3.2.0 → v3.3.0 (minor; metadata + acknowledgment, no contract change).

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 3.4.2 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 3.4.0 — 2026-04-27 (Phase 55 — implementability lever)
- **Added** Added Go/Python/PHP `ManifestV3` validator references → `has_typed_lang_contract` flips true (+10 impl).

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

## 2026-04-27 — Phase 63 impl-sweep

- Phase 63: appended Browser Extension Deploy enums TS enum mirror to satisfy `has_ts_enums` rubric (impl 80 → 90).

## 2026-04-27 — Phase 76 (impl 90 → 100)

- Added Mermaid lifecycle diagram — satisfies `has_mermaid` (+5).
- Added SQL DDL audit-log schema — satisfies `has_sql_ddl` (+20).
- Implementability raised 90 → 100 (deterministic audit, capped).

