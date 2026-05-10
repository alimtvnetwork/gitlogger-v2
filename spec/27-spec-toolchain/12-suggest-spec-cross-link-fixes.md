# 12 — suggest-spec-cross-link-fixes.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/suggest-spec-cross-link-fixes.py`](../../linter-scripts/suggest-spec-cross-link-fixes.py)  
**Category:** Generator (advisory + optional `--apply`)

---

## Purpose

Companion to §01 [`check-spec-cross-links.py`](./01-check-spec-cross-links.md). For every broken internal markdown link, propose the closest matching fix by fuzzy-matching against existing files (for `missing-file`) or existing headings inside the resolved target (for `missing-section`).

## Modes

- `--report` (default) — print suggestions, never touch files. Always exits `0` (advisory).
- `--apply` — rewrite files in place when a suggestion meets `--min-confidence`.

## Usage

```bash
python3 linter-scripts/suggest-spec-cross-link-fixes.py
python3 linter-scripts/suggest-spec-cross-link-fixes.py --apply --min-confidence 90
```

## CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--report` | on | Print suggestions only |
| `--apply` | off | Rewrite files when confidence ≥ threshold |
| `--min-confidence <n>` | `85` | 0–100 fuzzy-match threshold |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Report mode (always); or `--apply` succeeded |
| 1 | `--apply` mode and at least one rewrite failed |
| 2 | Invocation error |

## Acceptance criteria

### AC-12-01 — Report mode never modifies files
- **Given** `--report` (default),
- **When** the script runs,
- **Then** no file under `spec/` MUST be written, and the script MUST exit `0`.

### AC-12-02 — `--apply` respects confidence threshold
- **Given** `--apply --min-confidence 90` and a suggestion at confidence 80,
- **When** the script runs,
- **Then** that suggestion MUST NOT be applied.

### AC-12-03 — Output is parseable
- **Given** report mode,
- **When** stdout is captured,
- **Then** every suggestion MUST appear on a single line `file:line: OLD → NEW (confidence=NN)`.

## Cross-references

- §01 [`01-check-spec-cross-links.md`](./01-check-spec-cross-links.md) — broken-link detector.
