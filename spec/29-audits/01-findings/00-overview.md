---
content_axis: audit-corpus
axis_rationale: "Index of cross-spec audit findings; delegates to physical memo files under .lovable/memory/audit/ per Lesson #36 (link, never restate)"
kind: tracker
---

# Audit Findings — Index

**Version:** 1.0.2
**Updated:** 2026-05-06 (Phase 154 Task #6 — recommended-file completeness pass: added `97-acceptance-criteria.md` v1.0.0 delegated-governance stub + `98-changelog.md` v1.0.1 to satisfy strict tree-health rubric for delegated-index submodules. Index content unchanged. Phase 154 Task #5 — initial findings index under No-Questions Mode Prompt 04; classifies 80 module-named audit memos by target spec module without physical migration, per Lesson #36 link-don't-restate + Lesson #41 binding-survey precondition. Physical files remain at `.lovable/memory/audit/` to preserve 200+ cross-references in `mem://index.md` narrative trail.)
**Status:** Active (delegated)
**AI Confidence:** Low
**Ambiguity:** Low
**Module Kind:** tracker (audit-corpus, inherited from parent `spec/29-audits/`)

---

## Overview

This file is the **canonical index** of cross-spec audit findings. Each row classifies one or more memo files under `.lovable/memory/audit/` by the spec module they audit. Per Lesson #36, the index **delegates** to the physical files rather than copying or restating their contents — eliminating dual-source drift and preserving the historical narrative trail referenced from `mem://index.md`, §98 changelogs, and closing memos.

**Why no physical migration?** Per Lesson #41 (binding-survey precondition before mass-mechanical sweeps): physically relocating 80+ memos would require updating 200+ inbound references across the memory tree and several §98 rows — high blast-radius work with no implementation benefit. Delegation gives spec/29-audits a discoverable surface at zero ripple cost.

---

## Module Kind Declaration (Inherited)

This file inherits `kind: tracker` from `spec/29-audits/00-overview.md`. All cited findings, AC-IDs, file paths, and configuration values are **auditor-quoted evidence** from the audited specs (or their archives), not normative contract for spec/29 itself. See spec/25 AC-AI-09/10/11 for the disambiguation pattern.

---

## Findings by Target Spec Module

| Target Spec | Memo Count | Memo Glob (under `.lovable/memory/audit/`) | Era / Driver |
|-------------|-----------:|--------------------------------------------|--------------|
| spec/01-spec-authoring-guide | 1 | `01-spec-authoring-guide.md` | v2-deterministic baseline |
| spec/02-coding-guidelines | 24 | `02-coding-guidelines*.md` | v2-deterministic baseline + Phase 153 Task A10 sweep |
| spec/03-error-manage | 19 | `03-error-manage*.md` | v2-deterministic baseline (deepest sub-tree) |
| spec/04-database-conventions | 1 | `04-database-conventions.md` | v2-deterministic baseline |
| spec/05-split-db-architecture | 2 | `05-split-db-architecture*.md` | v2-deterministic baseline |
| spec/06-seedable-config-architecture | 2 | `06-seedable-config-architecture*.md` | v2-deterministic baseline |
| spec/07-design-system | 1 | `07-design-system.md` | v2-deterministic baseline |
| spec/10-research | 1 | `10-research.md` | v2-deterministic baseline |
| spec/11-powershell-integration | 1 | `11-powershell-integration.md` | v2-deterministic baseline |
| spec/12-cicd-pipeline-workflows | 3 | `12-cicd-pipeline-workflows*.md` | v2-deterministic baseline + Phase 153 Task A24-fu4 |
| spec/13-generic-cli | 1 | `13-generic-cli.md` | v2-deterministic baseline |
| spec/14-update | 2 | `14-update*.md` | v2-deterministic baseline |
| spec/15-distribution-and-runner | 1 | `15-distribution-and-runner.md` | v2-deterministic baseline |
| spec/16-generic-release | 1 | `16-generic-release.md` | v2-deterministic baseline |
| spec/17-consolidated-guidelines | 1 | `17-consolidated-guidelines.md` | v2-deterministic baseline |
| spec/18-wp-plugin-how-to | 2 | `18-wp-plugin-how-to*.md` | v2-deterministic baseline |
| spec/22-git-logs-v2 | 1 | `22-git-logs-v2.md` | Phase H1 / Phase 154 Task #1 |
| spec/23-app-database | 1 | `23-app-database.md` | v2-deterministic baseline |
| spec/24-app-design-system-and-ui | 1 | `24-app-design-system-and-ui.md` | v2-deterministic baseline |
| spec/25-app-issues | 2 | `25-app-issues*.md` | v2-deterministic baseline + Phase 153 Task A11c |
| spec/26-gitlogs-diagrams | 1 | `26-gitlogs-diagrams.md` | v2-deterministic baseline |
| **Total module-named memos** | **80** | — | — |

---

## Phase-Closing Memos (Narrative Trail)

23 additional memos under `.lovable/memory/audit/phase-*.md` are **session narrative**, not audit findings. They document the closure of individual phases (e.g. `phase-153-task-A11g-spec13-spec28-v5-closeout.md`) and remain under `.lovable/memory/audit/` indefinitely as contributor-private session trails. They are NOT mirrored here — per Lesson #36, the §98 row + closing memo IS the canonical surface; copying summaries into spec/29 would create a second authoritative copy.

---

## Historical Audit Baselines

The following subdirectories under `.lovable/memory/audit/` are **frozen snapshots** of the v2 deterministic audit at distinct cut points. They are referenced from `mem://specs/full-tree-audit-v4` (and predecessors) and MUST NOT be migrated:

| Snapshot | Cut Point | Referenced From |
|----------|-----------|-----------------|
| `v2-deterministic/` | Phase 152 audit-v6 baseline | `mem://specs/full-tree-audit-v4` |
| `v2-deterministic-pre-16r-baseline/` | Pre-Phase 16r recovery | `mem://specs/full-tree-audit-v4` (predecessor) |
| `v2-deterministic-pre-phase20-baseline/` | Pre-Phase 20 reorg | `mem://specs/full-tree-audit-v4` (predecessor) |
| `v2/` | v2 initial release | `mem://specs/full-tree-audit-v4` (predecessor) |

Future scorecard rebaselines (Phase H2+ / v7) will land under `spec/29-audits/03-rebaselines/` per Phase 154 Task #4 plan, not under `.lovable/memory/audit/v2-deterministic/`.

---

## Cross-References

- **Parent:** `spec/29-audits/00-overview.md` — module shell + module-kind contract.
- **Lesson #29** (`mem://process/phase-153-lessons` §F): Audit-corpus pattern.
- **Lesson #36** (`mem://process/phase-153-lessons` §C): Cross-module references MUST link, never restate.
- **Lesson #41** (`mem://process/phase-153-lessons` §B): Binding-mechanism survey precondition.
- **spec/25-app-issues** AC-AI-09/10/11: precedent for module-kind pin in §97.

---

## Status

**Active (delegated).** This file is the substantive child for `spec/29-audits` until Phase 155+ authors per-finding ACs binding individual memos to their target specs. No physical files were moved in this phase.
