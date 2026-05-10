# 30 — audit-spec-vs-code.py (v1)

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/audit-spec-vs-code.py`](../../linter-scripts/audit-spec-vs-code.py)  
**Category:** Auditor (AI-driven, **deprecated** — kept for diffing)  
**Successor:** §31 [`31-audit-spec-vs-code-v2.md`](./31-audit-spec-vs-code-v2.md)

---

## Purpose

Original 6-dimension spec-vs-code audit. Builds a digest per module (overview + AC + body listing + signal metrics), passes a code-artifact index, asks Gemini to score on Completeness 25, Consistency 25, Alignment 20, Clarity 15, Maintainability 10, Testability 5.

**Status:** Deprecated by v2 (which adds Implementability 35% and deterministic pre-checks). v1 is retained ONLY for diffing v1 vs v2 scores when reasoning about audit methodology changes.

## Inputs

- `LOVABLE_API_KEY` env var.
- Every module under `spec/`.
- `linter-scripts/` + `.github/` — shallow code index.

## Usage

```bash
python3 linter-scripts/audit-spec-vs-code.py
```

## CLI flags

_(none)_

## Outputs

- `.lovable/memory/audit/<module>.md` per module (overwritten).
- `.lovable/memory/audit/00-index.md` summary.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Audit complete |
| 1 | At least one module failed AI scoring |
| 2 | `LOVABLE_API_KEY` missing |

## Acceptance criteria

### AC-30-01 — Output location is `.lovable/memory/audit/` (NOT `v2/`)
- **Given** the script ran,
- **When** the report directory is inspected,
- **Then** v1 reports MUST land at `.lovable/memory/audit/` directly (not the `v2/` subfolder reserved for §31).

### AC-30-02 — Six dimensions present
- **Given** any module report,
- **When** read,
- **Then** the score table MUST list exactly six dimensions with weights summing to 100%.

### AC-30-03 — Deprecation banner
- **Given** the script's docstring or output,
- **When** inspected,
- **Then** a future patch SHOULD add a deprecation notice pointing to §31. (Currently a known gap; tracked here.)

## Cross-references

- §31 [`31-audit-spec-vs-code-v2.md`](./31-audit-spec-vs-code-v2.md) — successor.
