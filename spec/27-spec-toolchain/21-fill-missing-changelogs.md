# 21 — fill-missing-changelogs.cjs

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/fill-missing-changelogs.cjs`](../../linter-scripts/fill-missing-changelogs.cjs)  
**Category:** Filler (idempotent scaffolder)

---

## Purpose

Auto-generate `98-changelog.md` for every module under `spec/` (excluding `_archive/`) that has `00-overview.md` but no changelog.

**Idempotency:** re-runs on a satisfied tree are no-ops.

## Usage

```bash
node linter-scripts/fill-missing-changelogs.cjs
```

## CLI flags

_(none)_

## Outputs

New `spec/<module>/98-changelog.md` per missing module — contains v1.0.0 entry crediting this script.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All missing changelogs scaffolded (or none missing) |
| 1 | I/O error |

## Acceptance criteria

### AC-21-01 — Idempotency
- **Given** every module already has `98-changelog.md`,
- **When** the script runs,
- **Then** zero files MUST be written and exit code MUST be `0`.

### AC-21-02 — Scaffold contains today's date
- **Given** a scaffolded file,
- **When** read,
- **Then** the v1.0.0 entry MUST be dated with `new Date().toISOString().slice(0,10)`.

### AC-21-03 — Standard categories listed
- **Given** the scaffold's "Format" section,
- **When** read,
- **Then** it MUST list at minimum: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

## Cross-references

- §22 sister filler.
