# 03 — check-forbidden-strings.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/check-forbidden-strings.py`](../../linter-scripts/check-forbidden-strings.py)  
**Category:** Validator (read-only)


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

Generic, TOML-driven scanner that fails CI when forbidden patterns appear outside of allowlisted paths. Used to enforce naming bans, deprecated terminology, removed acronyms (e.g. `JWT`, `RS256`, `JWKS` in Git Logs v2), and any future cross-cutting prohibition.

## Usage

```bash
python3 linter-scripts/check-forbidden-strings.py
```

## CLI flags

_(none — all configuration lives in the TOML)_

## Inputs

- [`linter-scripts/forbidden-strings.toml`](../../linter-scripts/forbidden-strings.toml) (see §60) — defines patterns + allowlist globs.
- Every tracked file matching the include globs in the TOML.

## Outputs

Human report on stderr listing each forbidden hit with `file:line: pattern: matched-text`.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | No forbidden patterns matched outside allowlists |
| 1 | At least one forbidden hit |
| 2 | TOML missing or malformed |

## Acceptance criteria

### AC-03-01 — Pattern from TOML is enforced
- **Given** a pattern in `forbidden-strings.toml` and a file containing that exact text,
- **When** the script runs,
- **Then** it MUST exit `1` with the matching line reported.

### AC-03-02 — Allowlist glob suppresses matches
- **Given** the same pattern appears in a file matching an allowlist glob,
- **When** the script runs,
- **Then** the match MUST NOT be reported.

### AC-03-03 — Missing TOML is a hard error
- **Given** `forbidden-strings.toml` is absent,
- **When** the script runs,
- **Then** it MUST exit `2` (not `0` and not `1`).

## Cross-references

- §60 [`60-forbidden-strings-toml.md`](./60-forbidden-strings-toml.md) — TOML schema.
