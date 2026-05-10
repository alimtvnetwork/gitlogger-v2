# 04 — check-forbidden-spec-paths.sh

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/check-forbidden-spec-paths.sh`](../../linter-scripts/check-forbidden-spec-paths.sh)  
**Category:** Validator (read-only)

---

## Purpose

Block three classes of structural violations in a single fast bash check:

1. Re-appearance of deprecated, pre-consolidation update folders (`spec/14-generic-update/`, `spec/15-self-update-app-update/`) that were merged into `spec/14-update/` on 2026-04-17.
2. Any `MERGE-PROPOSAL.md` (any case variant) under `spec/` — a transient planning artefact that must never land.
3. Any uppercase-letter `.md` filename anywhere under `spec/` or `release-artifacts/`.

## Usage

```bash
bash linter-scripts/check-forbidden-spec-paths.sh
```

## CLI flags

_(none)_

## Inputs

The repository working tree.

## Outputs

Human-readable failure messages on stderr per violation.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | No forbidden path / filename present |
| 1 | At least one violation |

## Acceptance criteria

### AC-04-01 — Deprecated update folders are blocked
- **Given** `spec/14-generic-update/` exists on disk,
- **When** the script runs,
- **Then** it MUST exit `1` and reference the consolidation date 2026-04-17.

### AC-04-02 — `MERGE-PROPOSAL.md` (any case) is blocked
- **Given** any of `MERGE-PROPOSAL.md`, `merge-proposal.md`, `Merge-Proposal.md`,
- **When** the script runs,
- **Then** it MUST exit `1`.

### AC-04-03 — Uppercase `.md` filenames are blocked
- **Given** a file `spec/XYZ.md` or `release-artifacts/README.md`,
- **When** the script runs,
- **Then** it MUST exit `1`. (`readme.md` lowercase passes.)

## Cross-references

- [`spec/01-spec-authoring-guide/02-naming-conventions.md`](../01-spec-authoring-guide/02-naming-conventions.md) — naming source of truth.
