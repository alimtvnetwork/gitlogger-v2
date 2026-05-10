---
content_axis: audit-corpus
axis_rationale: "Index of historical scorecard rebaseline snapshots; delegates to physical baseline directories under .lovable/memory/audit/ per Lesson #36 (link, never restate)"
kind: tracker
---

# Audit Rebaselines — Index

**Version:** 1.0.1
**Updated:** 2026-05-06 (Phase 154 Task #6 — initial rebaselines index under No-Questions Mode Prompt 04 counter 7/40; classifies 4 frozen baseline subdirectories + auditor-output snapshots without physical migration. Per Lesson #36 link-don't-restate + Lesson #41 binding-mechanism survey precondition. Sister to `01-findings/00-overview.md` v1.0.0 from Task #5b.)
**Status:** Active (delegated)
**AI Confidence:** Low
**Ambiguity:** Low
**Module Kind:** tracker (audit-corpus, inherited from parent `spec/29-audits/`)

---

## Overview

This file is the **canonical index** of historical scorecard rebaseline snapshots — frozen `.lovable/memory/audit/v2*/` subdirectories captured at distinct cut points (audit-v2 release, pre-Phase-16r recovery, pre-Phase-20 reorg, Phase 152 audit-v6 baseline). Per Lesson #36, the index **delegates** to the physical snapshot directories rather than copying them — preserving the immutable historical record that drives `mem://specs/full-tree-audit-v4` reference contracts.

**Why no physical migration?** Per Lesson #41 (binding-mechanism survey precondition): historical baselines are **referenced by name** from `mem://specs/full-tree-audit-v4` and predecessor memos. Renaming or moving them would break those reference contracts and provide no implementation benefit. Delegation gives spec/29-audits a discoverable rebaseline-history surface at zero ripple cost.

---

## Module Kind Declaration (Inherited)

This file inherits `kind: tracker` from `spec/29-audits/00-overview.md`. All cited scores, AC-IDs, file paths, and audit findings inside snapshot directories are **auditor-quoted evidence** from prior audit passes, not normative contract for spec/29 itself. See spec/25 AC-AI-09/10/11 for the disambiguation pattern.

---

## Rebaseline Snapshots

| Snapshot Directory | Cut Point | Phase | Driver | Referenced From |
|--------------------|-----------|-------|--------|-----------------|
| `.lovable/memory/audit/v2/` | audit-v2 initial release | (early Phase 153 predecessor) | First deterministic pass over the spec tree | `mem://specs/full-tree-audit-v4` (predecessor lineage) |
| `.lovable/memory/audit/v2-deterministic-pre-16r-baseline/` | Pre-Phase 16r recovery | Phase 16r | Captured spec-tree state before Phase 16r recovery edits | `mem://specs/full-tree-audit-v4` (predecessor lineage) |
| `.lovable/memory/audit/v2-deterministic-pre-phase20-baseline/` | Pre-Phase 20 reorg | Phase 20 | Captured state before Phase 20 module reorg | `mem://specs/full-tree-audit-v4` (predecessor lineage) |
| `.lovable/memory/audit/v2-deterministic/` | Phase 152 audit-v6 baseline | Phase 152 | Current canonical deterministic baseline (168/168 strict, lockstep 87/87, freshness 81+6+0) | `mem://specs/full-tree-audit-v4` (live), `spec/17-consolidated-guidelines/34-full-tree-ai-audit-v6.md`, `phase-152-audit-v6-baseline.md` |

**Total:** 4 frozen snapshots covering the audit-v2 → audit-v6 deterministic-track lineage.

---

## Live Auditor Outputs

The current LLM-driven AI-Implementability auditor (`linter-scripts/audit-ai-implementability.py`, slot 34) writes its latest report to:

| Artifact | Path | Notes |
|----------|------|-------|
| Latest report | `.lovable/memory/audit/v2-deterministic/audit-ai-implementability-latest.md` | Overwritten on every successful run; gateway-bounded (Lesson #20 / Lesson #86). Current cut: v4 baseline (Phase 153 Task A7), tree avg ~82.3/100. |

**Future v5 / v6 / v7 rebaseline events** will land here as new files (per Phase 154 Task #4 plan). Trigger conditions per `mem://specs/full-tree-audit-v4`: R1 unblocks OR 7 cosmetic stamp refreshes land OR new contract-depth driver emerges.

---

## Phase H1 Rebaseline (Trace-Map Lineage)

The Phase H1 trace-map rebaseline (`{ac_total:1304, ac_traced:74, code_total:48, code_orphan:25}`) is documented in:

- `mem://index.md` Core block (line 18 of memory index, "Phase H1 rebaseline 2026-04-28").
- `mem://specs/full-tree-audit-v4` (live reference contract).

This rebaseline is **trace-map-class** (G-series mechanical AC↔code binding), distinct from the LLM-driven AI-implementability rebaseline class. Both classes are tracked under spec/29-audits/03-rebaselines/ for completeness.

---

## Cross-References

- **Parent:** `spec/29-audits/00-overview.md` — module shell + module-kind contract.
- **Sister:** `spec/29-audits/01-findings/00-overview.md` — cross-spec audit findings index (Phase 154 Task #5b).
- **Lesson #29** (`mem://process/phase-153-lessons` §F): Audit-corpus pattern.
- **Lesson #36** (`mem://process/phase-153-lessons` §C): Cross-module references MUST link, never restate.
- **Lesson #41** (`mem://process/phase-153-lessons` §B): Binding-mechanism survey precondition.
- `mem://specs/full-tree-audit-v4`: live audit-v6 baseline contract.
- `spec/17-consolidated-guidelines/34-full-tree-ai-audit-v6.md`: spec-side audit-v6 codification.

---

## Status

**Active (delegated).** This file is the second substantive child for `spec/29-audits` (after `01-findings/`). `02-post-mortems/` SKIPPED in Phase 154 Task #6 — survey found 0 genuine drift post-mortems (Lesson #41 unbound-survey: phase-closing memos and retrospective audits are not post-mortem-class material per Lesson #36 canonical-surface principle).
