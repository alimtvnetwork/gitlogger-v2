# 09 — check-memory-mirror-drift.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/check-memory-mirror-drift.py`](../../linter-scripts/check-memory-mirror-drift.py)  
**Category:** Validator (read-only)


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

Detect drift between the `Core` section of `.lovable/memory/index.md` and its public mirror at `spec/17-consolidated-guidelines/21-lovable-folder-structure.md` §X. This is a presence check (not a verbatim diff) — it extracts distinctive keywords from each Core bullet and asserts each appears in §X.

## Usage

```bash
python3 linter-scripts/check-memory-mirror-drift.py
```

## CLI flags

_(none)_

## Inputs

- `.lovable/memory/index.md` (private memory)
- `spec/17-consolidated-guidelines/21-lovable-folder-structure.md` (mirror)

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | No drift — every Core keyword present in mirror |
| 1 | Drift detected — Core rule added/changed without updating mirror |
| 2 | Structural error — file missing or section markers absent |

## Acceptance criteria

### AC-09-01 — New Core keyword without mirror update fails
- **Given** a new keyword in Core that is absent from §X,
- **When** the script runs,
- **Then** it MUST exit `1` and name the missing keyword.

### AC-09-02 — Missing section marker is exit 2
- **Given** the mirror file is missing the literal `## §X Project Memory` marker,
- **When** the script runs,
- **Then** it MUST exit `2`.

## Cross-references

- [`spec/17-consolidated-guidelines/21-lovable-folder-structure.md`](../17-consolidated-guidelines/21-lovable-folder-structure.md) §X — mirror target.
