# 22 — fill-missing-consistency-reports.cjs

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/fill-missing-consistency-reports.cjs`](../../linter-scripts/fill-missing-consistency-reports.cjs)  
**Category:** Filler (idempotent scaffolder)

---

## Purpose

Auto-generate `99-consistency-report.md` for every module under `spec/` (excluding `_archive/`) that has `00-overview.md` but no consistency report.

**Idempotency:** re-runs on a satisfied tree are no-ops. Safe to invoke from CI repeatedly.

## Usage

```bash
node linter-scripts/fill-missing-consistency-reports.cjs
```

## CLI flags

_(none)_

## Outputs

New `spec/<module>/99-consistency-report.md` per missing module — pre-fills the file inventory table from disk.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All missing consistency reports scaffolded (or none missing) |
| 1 | I/O error |

## Acceptance criteria

### AC-22-01 — Idempotency
- **Given** every module already has `99-consistency-report.md`,
- **When** the script runs,
- **Then** zero files MUST be written and exit code MUST be `0`.

### AC-22-02 — Inventory pre-populated from disk
- **Given** a freshly scaffolded report,
- **When** read,
- **Then** every `*.md` file in the module folder MUST appear in the inventory table with status ✅.

### AC-22-03 — Existing reports are not overwritten
- **Given** an existing consistency report,
- **When** the script runs,
- **Then** that file MUST be untouched.

## Cross-references

- §05 [`05-check-tree-health.md`](./05-check-tree-health.md) — gate that benefits from this filler.
