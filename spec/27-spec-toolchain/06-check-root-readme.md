# 06 — check-root-readme.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/check-root-readme.py`](../../linter-scripts/check-root-readme.py)  
**Category:** Validator (read-only)


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

Enforce §9 of [`spec/01-spec-authoring-guide/11-root-readme-conventions.md`](../01-spec-authoring-guide/11-root-readme-conventions.md) against the repo's root `readme.md`.

## Usage

```bash
python3 linter-scripts/check-root-readme.py
python3 linter-scripts/check-root-readme.py --readme path/to/readme.md
```

## CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--readme <path>` | `readme.md` | Override target file |

## Outputs

Human report listing each missing or malformed required element.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Every required element present |
| 1 | At least one element missing or malformed |
| 2 | `readme.md` not found / unreadable |

## Acceptance criteria

### AC-06-01 — Missing required element fails
- **Given** the readme is missing the platform-badges block,
- **When** the script runs,
- **Then** it MUST exit `1` and name the missing element.

### AC-06-02 — Override path works
- **Given** `--readme test/fixture.md`,
- **When** the script runs,
- **Then** it MUST validate the override file, not the root one.

### AC-06-03 — Missing file is exit 2
- **Given** the target file does not exist,
- **When** the script runs,
- **Then** it MUST exit `2` (distinguishing infra error from policy failure).

## Cross-references

- [`spec/01-spec-authoring-guide/11-root-readme-conventions.md`](../01-spec-authoring-guide/11-root-readme-conventions.md) §9 — source of truth.
- §07 + §08 enforce other readme invariants.
