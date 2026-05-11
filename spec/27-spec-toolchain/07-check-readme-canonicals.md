# 07 — check-readme-canonicals.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/check-readme-canonicals.py`](../../linter-scripts/check-readme-canonicals.py)  
**Category:** Validator (read-only)


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

Verify the root `readme.md` uses the canonical repo slug and CDN domain in every badge URL, install one-liner, and workflow link. Catches stale references after a major-version rename or domain change.

## Canonical defaults

| Field | Default value |
|-------|---------------|
| owner | `alimtvnetwork` |
| slug  | `coding-guidelines-v17` |
| cdn   | `cdn.riseup.asia` |

Override with CLI flags or environment variables.

## Usage

```bash
python3 linter-scripts/check-readme-canonicals.py
python3 linter-scripts/check-readme-canonicals.py --owner foo --slug bar --cdn cdn.example.com
README_CANON_OWNER=foo python3 linter-scripts/check-readme-canonicals.py
```

## CLI flags

| Flag | Env var | Default |
|------|---------|---------|
| `--owner` | `README_CANON_OWNER` | `alimtvnetwork` |
| `--slug`  | `README_CANON_SLUG`  | `coding-guidelines-v17` |
| `--cdn`   | `README_CANON_CDN`   | `cdn.riseup.asia` |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Every reference matches canonical values |
| 1 | At least one stale reference |
| 2 | `readme.md` not found / unreadable |

## Acceptance criteria

### AC-07-01 — Stale slug is detected
- **Given** a readme containing `coding-guidelines-v16`,
- **When** the script runs with default canonicals,
- **Then** it MUST exit `1`.

### AC-07-02 — Env var overrides default
- **Given** `README_CANON_SLUG=coding-guidelines-v18`,
- **When** the readme uses `v18`,
- **Then** it MUST exit `0`.

## Cross-references

- §06, §08 — sister readme validators.
