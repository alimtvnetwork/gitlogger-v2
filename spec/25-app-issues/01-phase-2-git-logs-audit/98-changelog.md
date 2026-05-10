# Changelog — Phase-2 Spec Issues Report — `git-logs` App

**Version:** 1.3.3
**Updated:** 2026-05-03
**Scope:** `spec/25-app-issues/01-phase-2-git-logs-audit/`

---

## 1.4.2 — 2026-05-03 (Task S25-01: dual-severity-enum frozen-historical pin)

- **Added** AC-09 `[high]` to `97-acceptance-criteria.md` (§97 v1.1.0 → **v1.2.0**) declaring the dual severity enum in `00-overview.md` (`{Critical,High,Medium,Low}` at lines 54+/102 vs `{blocker,major,minor,info}` at lines 605/634/673–678/701) as **frozen historical content** per AC-SAG-04 slot-immutability + Phase P11 supersession banner. Canonical issue-record severity enum is `../97-acceptance-criteria.md` AC-AI-14 (parent §25 §97). Closes audit-v6 MEDIUM/D3 finding "Inconsistent Severity Enums between trackers" (the auditor mislocated the drift as sub-01↔sub-02; on disk it's intra-sub-01 and is intentional historical evidence). Applies Lesson #29 (audit-corpus module-kind pin) + Lesson #36 (cross-module link-not-restate).
- **Bumped** §00 v1.4.1 → **v1.4.2**; §97 v1.1.0 → **v1.2.0**; this §98 v1.3.2 → **v1.3.3**; §99 v1.4.2 → **v1.4.3**. h10 stamps refreshed to phase 153 lineage.
- **Verified:** `node linter-scripts/check-lockstep.cjs` ✅; `node linter-scripts/check-tree-health.cjs --strict` ✅; `python3 linter-scripts/check-version-parity.py` ✅.

## 1.4.0 — 2026-04-28 (Phase P11: SUPERSEDED banner)

- **Status banner** rewritten to make supersession by `../02-consolidated-audit-findings/00-overview.md` explicit at top-of-file. Replaces the misleading `Status: Open` (this audit has been frozen since the consolidation pass). Adds a Phase P11 supersession-notice blockquote explaining the false-positive history (this Phase-2 audit reported `02-database-schema-and-erd.md` and parts of `08-allowlist-and-wildcard-matching.md` as "missing" when both files exist) and pointing at 02 as the active tracker.
- **Preserved** for traceability per AC-SAG-04 (slot immutability) + the §22 GAP-V2-01 LEGACY-ledger precedent (Phase P7b). Substantive audit content (25 P2-GL-NN findings) unchanged.
- **Bumped** §00 v1.3.0 → **v1.4.0**; this §98 v1.2.0 → **v1.3.0**; §99 v1.3.0 → **v1.4.0**.
- **Verified:** `node linter-scripts/check-lockstep.cjs` ✅ 87/87; `node linter-scripts/check-tree-health.cjs --strict` ✅ 168/168.

## 1.3.0 — 2026-04-27

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 1.3.1 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 1.3.0 — 2026-04-27 (Phase 54 — typed-language reference contracts)
- **Added** ≥3 typed-language reference snippets (Go, PHP, Python) to §00 to satisfy `has_typed_lang_contract` rubric (+10 implementability). Implements `AppIssueRecord` mirror across 3 typed languages.

### 1.2.0 — 2026-04-27 (Phase 42 — Inlined contract)
- **Added** machine-readable JSON-Schema "Issue Record Contract" block in §00 (`Phase2IssueRecord`). Codifies `P2-GL-NN` ID pattern, required triage fields (reproduction/cause/fix/prevention), severity enum, status enum, and `blocks_phase3` flag. Promotes module from C-tier to B-tier in deterministic audit v2.7.

### 1.1.0 — 2026-04-26
- **Added** §00 — inlined normative `Phase2GitLogsIssue` JSON schema (≥10 lines, `text` fence) immediately after the Issues Inventory totals. Clears the `missing-contract` G-CON-01 blocker (Phase 26).

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

## 2026-04-27 — Phase 70 (impl 75 → 85)

- Added Mermaid lifecycle diagram `lifecycle-phase2-audit-resolution.mmd`.
- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- No behavioural change to module rules; documentation-only promotion.


### 1.4.1 — 2026-04-29 — Phase 153 Task #35-fu2: §98 backfill (parity gate close-out)

- **Action**: Backfilled missing §98 row to match §00 banner v1.4.1. Phase 153 Task #35-fu surfaced this as part of the §00-ahead-of-§98 drift class after `latest_release()` was patched to SemVer-max comparator. The §00 banner had been bumped in a prior phase but the corresponding §98 row was never authored — this entry closes the parity gate.
- **Lockstep**: §98 latest release now equals §00 banner; no §00/§99 changes (banner already at v1.4.1).
- **Why**: Codifies Lesson #28 — version-parity drift is mechanical close-out work, not a comparator bug.
