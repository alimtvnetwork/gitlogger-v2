# 19 — check-memo-retrospective-headings.py

**Version:** 1.0.0
**Updated:** 2026-04-28
**Source:** [`linter-scripts/check-memo-retrospective-headings.py`](../../linter-scripts/check-memo-retrospective-headings.py)
**Category:** Validator (Phase 104; migrated from Phase 107 orphan ledger by Phase 108-full)

---

## Purpose

Scans phase memos under `.lovable/memory/audit/v2-deterministic/phase-NNN-*.md` and **fails** if any memo at or above the cutoff phase contains a forward-looking H2/H3 section heading (`Next phases`, `Next iteration`, `Remaining Tasks`, `Future work`, `TODO`, `Upcoming`, `Roadmap`).

### Why this matters

Phase 100 retired the freshness-sweep + "Next phases" cadence. Forward-looking sections inside phase memos cause:

1. **Drift** — a "Next phases" list inside a memo for Phase N becomes stale the moment Phase N+1 lands.
2. **Authority confusion** — there is exactly ONE place where pending work belongs: the chat reply's "Remaining Tasks" table. A second list inside a memo competes with that single source of truth.

A memo's purpose is to record what happened, why, and what it mechanically locked. Predictions about future phases belong in chat (and in the AC's `Verifies` clause if they were locked in by code), not in the memo.

## Usage

```bash
python3 linter-scripts/check-memo-retrospective-headings.py
```

Cutoff: **Phase 100** (configurable via constant in source). Phases 100, 101, 102, 103 deliberately ship as the first compliant memos.

## Inputs

- `.lovable/memory/audit/v2-deterministic/phase-NNN-*.md` (all memo files).

## Outputs

- stdout: per-violation report with file path + offending heading + line number.
- Exit code per the contract below.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | No forward-looking headings at or above cutoff |
| 1 | One or more memos contain forbidden headings |
| 2 | Infrastructure failure (memo dir missing, etc.) |

## Slot-range note

Slot **19** sits in the `10-19` generator range per the §27 §00 Normative Contract, but this is a **validator** by behavior. See [`18-check-mermaid-syntax.md`](./18-check-mermaid-syntax.md) for the Phase 108-full exception rationale; AC-T-23 verifies this slot's INV-01/INV-02 satisfaction.

## Cross-references

- [`05-check-tree-health.md`](./05-check-tree-health.md) — bijection enforcer.
- Phase 100 retrospective — cadence retirement that this script enforces.
- Phase 104 retrospective — origin of this script.
- Phase 107 orphan ledger — original drift detection.
- Phase 108-full retrospective — migration to this slot.
