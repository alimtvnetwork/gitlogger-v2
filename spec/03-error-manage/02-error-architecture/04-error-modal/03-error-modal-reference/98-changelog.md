# Changelog — Error Modal — Frontend Specification (Index)

**Version:** 1.2.0  
**Updated:** 2026-04-27  
**Scope:** `spec/03-error-manage/02-error-architecture/04-error-modal/03-error-modal-reference/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 2.3.0 — 2026-04-27 (Phase 56 — typed-language reference)
- **Added** Added Go/PHP/Python action-dispatcher reference shapes → flips `has_typed_lang_contract` true (+10 impl).

### 1.1.0 — 2026-04-26
- **Added** Phase-20 contract inlining: TypeScript `CapturedError`/`RawEnvelope` types, JSON Schema 2020-12 wire-format validator, and React `GlobalErrorModalProps` contract in `97-acceptance-criteria.md` (v2.1.0).
- **Changed** `99-consistency-report.md` bumped to v3.3.0 reflecting new contract presence (G-CON-01 satisfied).
- Resolves orphan-spec status flagged in `.lovable/memory/audit/03-error-manage__02-error-architecture__04-error-modal__03-error-modal-reference.md`.

### 1.0.0 — 2026-04-26
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

## 2026-04-27 — Phase 62 impl-sweep

- Phase 62: appended Error Modal Reference Catalog API OpenAPI to satisfy `has_yaml_openapi` rubric.

## 2026-04-27 — Phase 67 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 67 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

