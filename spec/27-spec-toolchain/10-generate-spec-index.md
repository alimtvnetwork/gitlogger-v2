# 10 — generate-spec-index.cjs

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/generate-spec-index.cjs`](../../linter-scripts/generate-spec-index.cjs)  
**Category:** Generator


**Test pair:** N/A — generator  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

Walk `spec/` and rebuild [`spec/spec-index.md`](../spec-index.md) from disk truth. Each top-level module receives a category icon + label and an entry per child file. Idempotent — re-running on an unchanged tree produces a byte-identical output.

## Usage

```bash
node linter-scripts/generate-spec-index.cjs
```

## CLI flags

_(none)_

## Inputs

Every `*.md` under `spec/` (excluding `_archive/`).

## Outputs

`spec/spec-index.md` is overwritten in place.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Index successfully written |
| 1 | I/O error (cannot read `spec/` or write `spec-index.md`) |

## Acceptance criteria

### AC-10-01 — Output is deterministic
- **Given** an unchanged `spec/` tree,
- **When** the script runs twice in succession,
- **Then** `spec/spec-index.md` MUST be byte-identical between runs.

### AC-10-02 — Every module appears
- **Given** the script just ran,
- **When** `spec/spec-index.md` is read,
- **Then** every top-level module folder MUST have an entry.

### AC-10-03 — Category icons are stable
- **Given** the `CATEGORY_ICONS` map in source,
- **When** the index is generated,
- **Then** entries MUST use the exact icon + label from that map (no inference).

## Cross-references

- §70 [`70-spec-health-yml.md`](./70-spec-health-yml.md) — CI re-runs this on every push.
