# 25 — deepen-consistency-reports.py

**Version:** 1.0.0
**Updated:** 2026-04-28
**Source:** [`linter-scripts/deepen-consistency-reports.py`](../../linter-scripts/deepen-consistency-reports.py)
**Category:** Filler / one-shot maintenance (Phase 21; migrated from Phase 107 orphan ledger by Phase 108-full)

---

## Purpose

Scans `spec/**/99-consistency-report.md` and rewrites any **thin** report (<1500 bytes OR missing the canonical 5-section structure) into the gold-standard shape used by [`spec/02-coding-guidelines/03-golang/01-enum-specification/99-consistency-report.md`](../02-coding-guidelines/03-golang/01-enum-specification/99-consistency-report.md):

1. Header (title, version, date, health score)
2. File Inventory (auto-detected from sibling `.md` files)
3. Naming Convention Compliance
4. Cross-Reference Validation
5. Summary
6. Validation History

### Skips

- `spec/_archive/**` (frozen reference)
- Any report that already has all 5 canonical sections **and** is ≥1500 bytes.

### Preserves

- Existing version line if present (bumped `+0.1.0`).
- Any custom prose in a `## Notes` or `## Custom` trailing block.

## Usage

```bash
# Dry-run (default in CI contexts)
python3 linter-scripts/deepen-consistency-reports.py --dry-run

# Apply rewrites
python3 linter-scripts/deepen-consistency-reports.py

# Custom root
python3 linter-scripts/deepen-consistency-reports.py --root spec
```

## CLI flags

| Flag | Default | Effect |
|------|---------|--------|
| `--dry-run` | off | Print intended changes; do not write |
| `--root <path>` | `spec` | Override scan root |

## Inputs

- `spec/**/99-consistency-report.md` (excluding `spec/_archive/**`).

## Outputs

- Rewritten `99-consistency-report.md` files (in-place) when not `--dry-run`.
- stdout: per-file action log (`rewrote`, `skipped (already deep)`, `skipped (archive)`).

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Scan complete (regardless of how many files were rewritten) |
| 1 | Reserved for future "thin report still found after rewrite" health check |
| 2 | Infrastructure failure (root missing, write error, etc.) |

## Slot-range note

Slot **25** sits in the `20-29` filler range per the §27 §00 Normative Contract — this script is a **filler/idempotent maintenance** tool, so kind and range agree. AC-T-24 verifies this slot's INV-01/INV-02 satisfaction.

## Cross-references

- [`22-fill-missing-consistency-reports.md`](./22-fill-missing-consistency-reports.md) — sibling scaffolder (creates a missing report; this script *deepens* an existing thin one).
- Phase 21 retrospective — original sweep that produced this tool.
- Phase 107 orphan ledger — drift detection.
- Phase 108-full retrospective — migration to this slot.
