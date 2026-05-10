# 16 — generate-gate-report.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/generate-gate-report.py`](../../linter-scripts/generate-gate-report.py)  
**Category:** Generator (consumes deterministic audit results, explains hard-gate caps)

---

## Purpose

The v2 auditor (§31) applies a fixed table of **hard scoring gates** that cap individual dimensions when their predicate fires. This script reads the audit's `raw-results.json` and produces a human-readable explanation of:

- Which gate fired on which module (active vs passive).
- How many points each dimension lost to gates across the whole tree.
- A leaderboard showing which gates bite hardest.
- A per-module deep dive: raw rubric → final score, dimension by dimension, with the gate id(s) responsible for each cap.

## Usage

```bash
# 1. Refresh the deterministic audit (gates are applied inside the auditor)
AUDIT_DETERMINISTIC=1 python3 linter-scripts/audit-spec-vs-code-v2.py

# 2. Render the gate-cause report
python3 linter-scripts/generate-gate-report.py
```

## CLI flags

_(none — reads `raw-results.json`, writes both reports unconditionally)_

## Inputs

- `.lovable/memory/audit/v2-deterministic/raw-results.json` — must contain `raw_scores` and `applied_gates` for every module (auditor v1.2.0+).

## Outputs

| Path | Purpose |
|------|---------|
| `.lovable/memory/audit/v2-deterministic/gate-report.md` | Human-readable: leaderboard + per-module breakdown |
| `.lovable/memory/audit/v2-deterministic/gate-report.json` | Machine-readable, sorted, byte-stable |

## Concepts

| Term | Meaning |
|------|---------|
| **Active firing** | Gate predicate is true AND the rubric raw score exceeded the cap → score was actually lowered. |
| **Passive firing** | Gate predicate is true BUT the rubric was already at/below the cap → recorded for transparency, no score change. |
| **Δ (delta)** | `weighted(raw_scores) − weighted(final_scores)`. Total weighted points lost to gates per module. |
| **Dimension-loss** | Sum of `(before − after)` across active firings per dimension. |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Report written |
| 1 | `raw-results.json` not found — run §31 first |
| 2 | Invocation error |

## Acceptance criteria

### AC-16-01 — Report explains every active gate firing
- **Given** any module whose `applied_gates` array contains an entry with `active=true`,
- **When** `gate-report.md` is read,
- **Then** the module's per-module breakdown section MUST list that gate id under "Active gates fired".

### AC-16-02 — Leaderboard is sorted by active firings descending
- **Given** the "Gate firing leaderboard" table,
- **When** rows are read top-to-bottom,
- **Then** the `Active fires` column MUST be monotonically non-increasing.

### AC-16-03 — Dimension-loss totals match per-module sums
- **Given** the "Dimension-loss totals" table,
- **When** values are summed per dimension across `per_module[*].active_gates`,
- **Then** the totals MUST equal the per-dimension `(before − after)` sums.

### AC-16-04 — JSON output is byte-stable across runs
- **Given** an unchanged `raw-results.json`,
- **When** the script is run twice consecutively,
- **Then** `gate-report.json` MUST have identical SHA-256 (sorted keys, modules sorted by name).

### AC-16-05 — Missing audit JSON exits 1
- **Given** `raw-results.json` does not exist,
- **When** the script runs,
- **Then** it MUST exit `1` and print a hint pointing at the auditor command.

### AC-16-06 — Final overall ≤ raw overall for every module
- **Given** any row in the "Per-module gate detail" table,
- **When** `Raw` and `Final` are compared,
- **Then** `Final` MUST be ≤ `Raw` (gates can only lower scores).

## Cross-references

- §31 [`31-audit-spec-vs-code-v2.md`](./31-audit-spec-vs-code-v2.md) — owns the gate definitions in `HARD_GATES`.
- §15 [`15-generate-fix-checklist.md`](./15-generate-fix-checklist.md) — sibling generator that translates gates into fix actions.
