# Changelog — Templates

**Version:** 3.4.2
**Updated:** 2026-04-29
**Scope:** `spec/03-error-manage/03-error-code-registry/09-templates/`

---

### 3.4.2 — 2026-04-29 — Phase 153 Task #29d closure: AI Confidence parity reached 51/51 (100%)
- Lockstep companion bump for §00/§99 banner edits made under Phase 153 Task #29d (P1 inventory regex widened in `check-ai-confidence.py`, underclaim banners promoted, legacy stub Verifies clauses backfilled). **No AC change beyond Task #29c-pattern legacy stubs; no CI workflow change.** See `.lovable/memory/audit/v2-deterministic/phase-153-task-29d-p1-regex-widening-and-final-parity.md`.

## 3.4.1 — 2026-04-28 — Phase P29: P25-pure dual-stream reconciliation (batch)

- **Reconciled** §98 header version stream `1.2.0` → `3.4.1` to align with §00 banner stream (`3.4.0`). Prior §98 header tracked an independent audit-stream version decoupled from the SemVer ladder, which already contained `3.4.0` (matching §00 banner). Per Phase P25 precedent (subcase: clean ladder + decoupled header stream), §98 header is patch-bumped to `3.4.1` to align with banner; §00 banner also bumped to `3.4.1` per P27 sub-lesson (parity gate enforces exact match for stamped files). Ladder body unchanged. H10 stamp added to §00. **Phase P29 batch reconciliation** (8 P25-pure drifters processed in one phase per P27 batching lesson).

## 1.2.0 — 2026-04-27

- Phase 51: appended JSON Schema + typed enum contracts to overview to lift implementability score (no behavior change).

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 3.4.0 — 2026-04-27 (Phase 56 — typed-language reference)
- **Added** Added PHP + Python template renderers (already had 1 Go); brings typed-lang count to ≥3 → flips `has_typed_lang_contract` true (+10 impl).

### 1.1.0 — 2026-04-27 (Phase 42 — Inlined contract + cleanup)
- **Added** machine-readable JSON-Schema "Template Envelope" block in §00 (`ErrorCodeTemplate`). Codifies error-code regex, domain enum, severity enum, message/remediation min-lengths, and SemVer `since` field. Promotes module from C-tier to B-tier in deterministic audit v2.7.
- **Fixed** §00 Document Inventory had a duplicated table; collapsed to a single canonical inventory.
- **Bumped** §00 banner v3.2.0 → v3.3.0 (synchronized with new contract content).

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

- Phase 62: appended Error Code Template Library API OpenAPI to satisfy `has_yaml_openapi` rubric.

## 2026-04-27 — Phase 67 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 67 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

