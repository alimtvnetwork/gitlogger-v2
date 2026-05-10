# 08 — check-readme-install-section.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/check-readme-install-section.py`](../../linter-scripts/check-readme-install-section.py)  
**Category:** Validator (read-only)

---

## Purpose

Enforce three install-section invariants on the root `readme.md`:

1. The "Install in One Line" section is the FIRST `<h2>` after the `<!-- /STAMP:PLATFORM_BADGES -->` marker.
2. The "Bundle Installers" section appears immediately after install and before the Table of Contents.
3. Every install code fence (`powershell` / `bash` / `sh` / `pwsh`) inside those sections contains EXACTLY ONE non-empty command line, with NO inline `#` comments, NO blank lines, NO `\` continuations.

## Usage

```bash
python3 linter-scripts/check-readme-install-section.py
```

## CLI flags

_(none)_

## Inputs

- `readme.md` at repo root.
- Spec sources of truth (referenced from the script's docstring):
  - `.lovable/memory/constraints/install-command-formatting.md` (memory-only — not a spec file; create on demand)
  - [`spec/01-spec-authoring-guide/11-root-readme-conventions.md`](../01-spec-authoring-guide/11-root-readme-conventions.md)

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Position correct AND every install fence is a single bare command |
| 1 | At least one violation (each printed with `file:line`) |
| 2 | `readme.md` not found / unreadable |

## Acceptance criteria

### AC-08-01 — Install section out of position fails
- **Given** another `<h2>` between the badges marker and the install section,
- **When** the script runs,
- **Then** it MUST exit `1`.

### AC-08-02 — Multi-line install fence fails
- **Given** an install fence containing two non-empty command lines,
- **When** the script runs,
- **Then** it MUST exit `1` and report the line of the second command.

### AC-08-03 — Inline comment in install fence fails
- **Given** `iwr ... # comment` inside an install fence,
- **When** the script runs,
- **Then** it MUST exit `1`.

## Cross-references

- §06, §07 — sister readme validators.
