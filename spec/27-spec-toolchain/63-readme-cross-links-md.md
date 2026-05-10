# 63 — readme-cross-links.md

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/readme-cross-links.md`](../../linter-scripts/readme-cross-links.md)  
**Category:** Configuration (registry of sibling-repo readme links)

---

## Purpose

A single markdown registry of sibling-repository readme cross-links used by readme validators (§06–§08). Centralises external readme paths so that a sibling-repo rename only requires editing this one file.

## Format

A simple two-column markdown table:

```markdown
| Sibling repo | Canonical readme URL |
|--------------|----------------------|
| coding-guidelines-v17 | https://github.com/alimtvnetwork/coding-guidelines-v17/blob/main/readme.md |
| ...                   | ...                                                               |
```

## Acceptance criteria

### AC-63-01 — Two-column table
- **Given** the file,
- **When** parsed as markdown,
- **Then** the only data structure MUST be a single 2-column table after the H1.

### AC-63-02 — URLs use `https://`
- **Given** any row,
- **When** the URL column is read,
- **Then** it MUST start with `https://` (no `http://`, no relative paths).

### AC-63-03 — Sibling repo names are unique
- **Given** the full table,
- **When** the first column is collected,
- **Then** there MUST be no duplicates.

## Cross-references

- §06–§08 — readme validators (potential future consumers).
