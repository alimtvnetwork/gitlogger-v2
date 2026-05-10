# Changelog — Enum Specification

**Version:** 3.3.3
**Updated:** 2026-04-29
**Scope:** `spec/02-coding-guidelines/03-golang/01-enum-specification/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 3.3.2 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 3.3.1 — 2026-04-28 — Phase P30 batch reconciliation
- §98 header bumped to align with §00 banner; H10 stamp dropped on §00; date sweep `2026-04-27`→`2026-04-28`. Pure metadata patch — no module-rule change.

### 3.3.0 — 2026-04-28 — Phase P30 (P30 batch — dual-stream alignment)
- Reconciles §98 release stream with §00 banner stream (`3.3.0`). Prior §98 ladder ended at `2.0.0` (after promoting any post-footer prose) but §00 banner already tracked `3.3.0` from independent module-version stream (P25 subcase). Per P25 precedent, single alignment row added at §00 banner version; lockstep gate now satisfied.

### 2.0.0 — 2026-04-28 — promoted by Phase P30 (P30 batch — P28-style hybrid)
- Reconstructed from post-footer prose: `## 2026-04-27 — Phase 72 (impl 90 → 95)`. **Minor bump**: additive content (typed contracts, OpenAPI surface, Mermaid diagram, frontmatter, etc.) — no behavior change.

### 1.3.0 — 2026-04-28 — promoted by Phase P30 (P30 batch — P28-style hybrid)
- Reconstructed from post-footer prose: `## 2026-04-27 — Phase 64 (impl 85→90)`. **Minor bump**: additive content (typed contracts, OpenAPI surface, Mermaid diagram, frontmatter, etc.) — no behavior change.

### 1.2.0 — 2026-04-28 — promoted by Phase P30 (P30 batch — P28-style hybrid)
- Reconstructed from post-footer prose: `## 2026-04-27 — Phase 60 impl-sweep`. **Minor bump**: additive content (typed contracts, OpenAPI surface, Mermaid diagram, frontmatter, etc.) — no behavior change.

### 1.1.0 — 2026-04-26 (Phase 20 contract inlining, module #10)
- **Added** normative Reference Implementation block in `00-overview.md`:
  full `internal/enums/providertype/variant.go`, TypeScript wire-format mirror,
  Draft 2020-12 JSON Schema, and a forbidden-shapes table.
- **Added** lockstep cross-language contract: Go + TS + JSON Schema must
  ship in the same commit (G-CON-01 contract requirement).
- **Verified** TS mirror typechecks under `tsc --strict`; JSON Schema rejects
  unknown strings, numbers, and null inputs (`Draft202012Validator`).
- Bumps overview to v3.3.0.

### 1.0.0 — 2026-04-26
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

### 3.3.3 — 2026-04-29 — Phase 153 Task #35-fu2: §98 backfill (parity gate close-out)

- **Action**: Backfilled missing §98 row to match §00 banner v3.3.3. Phase 153 Task #35-fu surfaced this as part of the §00-ahead-of-§98 drift class after `latest_release()` was patched to SemVer-max comparator. The §00 banner had been bumped in a prior phase but the corresponding §98 row was never authored — this entry closes the parity gate.
- **Lockstep**: §98 latest release now equals §00 banner; no §00/§99 changes (banner already at v3.3.3).
- **Why**: Codifies Lesson #28 — version-parity drift is mechanical close-out work, not a comparator bug.
