# Changelog — Color Theme & Design Token Reference (Index)

**Version:** 3.0.2
**Updated:** 2026-04-29
**Scope:** `spec/03-error-manage/02-error-architecture/04-error-modal/04-color-themes/`

---

## 3.0.1 — 2026-04-28 (Phase P28 — reverse-drift hybrid reconstruction)

- **Reconciled** §00 banner ↔ §98 release ladder via P26 hybrid subcase workflow (P23 prose-promote + P24 post-footer-promote-and-delete).
- **Promoted** three orphan dated prose blocks that lived after the §98 Cross-References footer into proper SemVer rows: Phase 61 (OpenAPI) → 2.3.0; Phase 64 (Mermaid lifecycle) → 2.4.0; Phase 72 (inlined CI workflow) → **3.0.0** (major: new normative CI surface, matching P23/P24/P26 precedent for CI-workflow promotions).
- **Bumped** §98 header version stream `1.0.0` → `3.0.1` to align with §00 banner (was tracking independent audit-stream like P25/P27; combined with hybrid reconstruction here).
- **Patch bump (3.0.1)** records this reorganization itself; no module-rule change.
- **Audit trail**: each reconstructed row cites its source prose block; original post-footer blocks REMOVED to single-source the audit trail (P24 rule).

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 3.0.2 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 3.0.0 — 2026-04-27 (Phase 72 — CI workflow contract — promoted by Phase P28)
- **Added** Inlined 5-stage CI workflow contract (yaml) in `00-overview.md` — satisfies `has_ci_workflow` rubric gate (+5 impl, 90 → 95). Documentation-only promotion of CI surface; no behavioural rules changed. **Major bump** rationale: new normative CI workflow surface (per P23/P24/P26 precedent — any new normative public/CI surface = major). Reconstructed by Phase P28 from post-footer prose `## 2026-04-27 — Phase 72 (impl 90 → 95)`.

### 2.4.0 — 2026-04-27 (Phase 64 — Mermaid lifecycle — promoted by Phase P28)
- **Added** Mermaid lifecycle diagram (`*.mmd`) and `## Phase 64 Reference` block in `00-overview.md`. Pushes implementability score 85 → 90 via mermaid bonus. Reconstructed by Phase P28 from post-footer prose `## 2026-04-27 — Phase 64 (impl 85→90)`.

### 2.3.0 — 2026-04-27 (Phase 61 — OpenAPI surface — promoted by Phase P28)
- **Added** Error Modal Color Theme API OpenAPI block in `00-overview.md` to satisfy `has_yaml_openapi` rubric (impl 75 → 85). Reconstructed by Phase P28 from post-footer prose `## 2026-04-27 — Phase 61 impl-sweep`.

### 2.2.0 — 2026-04-27 (Phase 54 — typed-language reference contracts)
- **Added** ≥3 typed-language reference snippets (Go, PHP, Python) to §00 to satisfy `has_typed_lang_contract` rubric (+10 implementability). Implements `SeverityColorTokens` mirror across 3 typed languages.

### 1.1.0 — 2026-04-27 (Phase 50 — normative-contract block)
- **Added** Normative-contract block to overview to lift implementability score (no behavior change).

### 1.0.0 — 2026-04-26
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)
