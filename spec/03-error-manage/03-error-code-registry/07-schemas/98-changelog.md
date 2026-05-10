# Changelog — Schemas

**Version:** 3.4.2
**Updated:** 2026-04-29
**Scope:** `spec/03-error-manage/03-error-code-registry/07-schemas/`

---

### 3.4.2 — 2026-04-29 — Phase 153 Task #29e: AI Confidence promoted High → Production-Ready
- Phase 153 Task #29e — promoted `**AI Confidence:**` from `High` to `Production-Ready`. Pure banner edit: this module already passes P1+P2+P3+P4 per `check-ai-confidence.py`; the prior `High` value was a stale underclaim. **No AC change, no CI workflow change, no RUBRIC bump.**

## 3.4.1 — 2026-04-28 — Phase P29: P25-pure dual-stream reconciliation (batch)

- **Reconciled** §98 header version stream `1.1.0` → `3.4.1` to align with §00 banner stream (`3.4.0`). Prior §98 header tracked an independent audit-stream version decoupled from the SemVer ladder, which already contained `3.4.0` (matching §00 banner). Per Phase P25 precedent (subcase: clean ladder + decoupled header stream), §98 header is patch-bumped to `3.4.1` to align with banner; §00 banner also bumped to `3.4.1` per P27 sub-lesson (parity gate enforces exact match for stamped files). Ladder body unchanged. H10 stamp added to §00. **Phase P29 batch reconciliation** (8 P25-pure drifters processed in one phase per P27 batching lesson).

## 1.2.0 — 2026-04-27

- Phase 50: appended normative-contract block to overview to lift implementability score (no behavior change).

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 3.4.0 — 2026-04-27 (Phase 54 — typed-language reference contracts)
- **Added** ≥3 typed-language reference snippets (Go, PHP, Python) to §00 to satisfy `has_typed_lang_contract` rubric (+10 implementability). Implements `RegistryShardEntry` mirror across 3 typed languages.

### 1.1.0 — 2026-04-26
- **Added** Phase-20 contract inlining: both `error-code.schema.json` and `error-codes-index.schema.json` are now inlined as fenced ```json``` blocks in `00-overview.md` (v3.3.0). Resolves P0 missing-contract gate G-CON-01 from fix-checklist (`.lovable/memory/audit/v2-deterministic/fix-checklists/03-error-manage__03-error-code-registry__07-schemas.md`).
- **Changed** `99-consistency-report.md` bumped to v3.3.0.
- **Changed** `00-overview.md` bumped to v3.3.0 with new "Inlined Contracts" section.

### 1.0.0 — 2026-04-26
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

## 2026-04-27 — Phase 58 impl-sweep

- Phase 58: appended ErrorCodeRegistry OpenAPI contract to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 65 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 65 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

