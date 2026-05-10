# Changelog — Linter Scripts

**Version:** 1.2.1
**Updated:** 2026-04-29
**Scope:** `spec/03-error-manage/03-error-code-registry/08-linter-scripts/`

---

### 1.2.1 — 2026-04-29 — Phase 153 Task #29e: AI Confidence promoted High → Production-Ready
- Phase 153 Task #29e — promoted `**AI Confidence:**` from `High` to `Production-Ready`. Pure banner edit: this module already passes P1+P2+P3+P4 per `check-ai-confidence.py`; the prior `High` value was a stale underclaim. **No AC change, no CI workflow change, no RUBRIC bump.**

## 1.3.0 — 2026-04-27
- **P22 sync** (2026-04-28): §00 banner version field bumped 1.2.0 → 1.3.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 22 -->` stamp added under §00 banner; no spec content change).

- Phase 50: appended normative-contract block to overview to lift implementability score (no behavior change).

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 1.2.0 — 2026-04-27 (Phase 42 — Inlined contract)
- **Added** machine-readable JSON-Schema "Linter-Output Contract" block in §00 (`LinterReport`). Codifies stdout shape (script enum, exit-code range, summary fields, finding records with code-id pattern). Promotes module from C-tier to B-tier in deterministic audit v2.7.

### 1.1.0 — 2026-04-26
- **Added** §00 — inlined normative `ErrorCodeRegistry` JSON schema (≥10 lines, `text` fence), expanded Document Inventory with the four `.mjs` scripts, deduplicated the broken table row, and added Cross-References. Clears the `missing-contract` G-CON-01 blocker (Phase 26).

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

## 2026-04-27 — Phase 57 impl-sweep

- Phase 57: appended Go/PHP/Python LinterResult validator references to satisfy `has_typed_lang_contract` rubric (impl 65 → 75).

## 2026-04-27 — Phase 62 impl-sweep

- Phase 62: appended Error Code Linter Scripts API OpenAPI to satisfy `has_yaml_openapi` rubric.

## 2026-04-27 — Phase 65 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 65 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.


### 1.3.1 — 2026-04-29 — Phase 153 Task #35-fu2: §98 backfill (parity gate close-out)

- **Action**: Backfilled missing §98 row to match §00 banner v1.3.1. Phase 153 Task #35-fu surfaced this as part of the §00-ahead-of-§98 drift class after `latest_release()` was patched to SemVer-max comparator. The §00 banner had been bumped in a prior phase but the corresponding §98 row was never authored — this entry closes the parity gate.
- **Lockstep**: §98 latest release now equals §00 banner; no §00/§99 changes (banner already at v1.3.1).
- **Why**: Codifies Lesson #28 — version-parity drift is mechanical close-out work, not a comparator bug.
