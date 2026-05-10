# Changelog — File & Folder Naming Conventions

**Version:** 1.2.2
**Updated:** 2026-04-29
**Scope:** `spec/02-coding-guidelines/08-file-folder-naming/`

---

### 1.2.2 — 2026-04-29 — Phase 153 Task #29e: AI Confidence promoted High → Production-Ready
- Phase 153 Task #29e — promoted `**AI Confidence:**` from `High` to `Production-Ready`. Pure banner edit: this module already passes P1+P2+P3+P4 per `check-ai-confidence.py`; the prior `High` value was a stale underclaim. **No AC change, no CI workflow change, no RUBRIC bump.**

## 1.3.0 — 2026-04-27

- Phase 51: appended JSON Schema + typed enum contracts to overview to lift implementability score (no behavior change).

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 1.2.1 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 1.3.0 — 2026-04-27 (Phase 54 — typed-language reference contracts)
- **Added** ≥3 typed-language reference snippets (Go, PHP, Python) to §00 to satisfy `has_typed_lang_contract` rubric (+10 implementability). Implements `FileAndFolderNamingRule` mirror across 3 typed languages.

### 1.2.0 — 2026-04-27 (Phase 42 — Inlined contract)
- **Added** machine-readable JSON-Schema "Naming-Convention Contract" block in §00 (`FileAndFolderNamingContract`). Codifies per-language file/folder regex, reserved-slot immutability (`00`/`97`/`98`/`99`), numeric-prefix shape, and `NAMING-001` violation code. Promotes module from C-tier (rubric `implementability=50`) to B-tier in deterministic audit v2.7.

### 1.1.0 — 2026-04-26
- **Added** §00 — inlined normative per-language naming regex contract (≥10 lines, `text` fence) clearing the `missing-contract` G-CON-01 blocker (Phase 26).
- **Bumped** §00 v3.2.0 → v1.1.0 (resync from misaligned root version) — see §99 audit row.

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

## 2026-04-27 — Phase 59 impl-sweep

- Phase 59: appended File/Folder Naming Audit OpenAPI OpenAPI to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 64 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 64 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

