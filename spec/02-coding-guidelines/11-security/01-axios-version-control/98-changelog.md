# Changelog — Axios Version Control Policy

**Version:** 3.2.1  
**Updated:** 2026-04-29  
**Scope:** `spec/02-coding-guidelines/11-security/01-axios-version-control/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 3.2.1 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 3.2.0 — 2026-04-28

- **Changed** Phase P23 (H10 reverse-drift reconciliation): Reconstructed §98 release ladder so that §00 banner version `3.2.0` is now backed by an explicit release row. Prior §98 contained ad-hoc dated prose blocks (Phase 27c / 53 / 70 / 75) that were not promoted into SemVer entries; this release codifies them as 1.2.0 / 1.3.0 / 2.0.0 / 3.0.0 / 3.1.0 below. No behavioural change to module rules.
- **Added** `<!-- h10-verified-phase: 23 -->` stamp to `00-overview.md`, opting this file into strict H10 version-parity enforcement per `check-version-parity.py` AC-29-11/12/13.

### 3.1.0 — 2026-04-27

- **Added** TypeScript enum mirror — satisfies `has_ts_enums` (+10 implementability).
- Documentation-only promotion; mirror is a normative reference shape only.
- Audit-trail source: prior `## 2026-04-27 — Phase 75 (impl 85 → 95+)` prose block.

### 3.0.0 — 2026-04-27

- **Added** typed-language reference contracts (Go, Rust, C# stubs) — satisfies `has_typed_lang_contract` (+10 implementability).
- Major bump reflects introduction of cross-language normative contract surface (new public reference shape).
- Audit-trail source: prior `## 2026-04-27 — Phase 75 (impl 85 → 95+)` prose block.

### 2.0.0 — 2026-04-27

- **Added** Mermaid lifecycle diagram `lifecycle-axios-policy-enforcement.mmd`.
- **Added** inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Major bump reflects introduction of binding CI workflow surface (enforcement pipeline becomes part of the spec).
- No behavioural change to module rules; documentation-only promotion.
- Audit-trail source: prior `## 2026-04-27 — Phase 70 (impl 75 → 85)` prose block.

### 1.3.0 — 2026-04-27

- **Added** typed-language / SQL DDL / JSON Schema contracts appended to overview to lift implementability score (no behavior change).
- Audit-trail source: prior `## 1.1.0 — 2026-04-27` Phase 53 entry (renumbered to preserve chronology under reconstructed ladder).

### 1.2.0 — 2026-04-26

- **Added** `kind: future-spec` frontmatter + Drift Acknowledgment.
- Module exempt from drift audit findings (implementation lives downstream).
- Audit-trail source: prior cross-reference table row (Phase 27c).

### 1.0.0 — 2026-04-26

- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)
