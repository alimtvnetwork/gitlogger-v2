# 41 — run.ps1

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/run.ps1`](../../linter-scripts/run.ps1)  
**Category:** Runner (PowerShell entry point — Windows mirror of §40)


**Test pair:** N/A — scaffold  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

Windows mirror of §40 [`run.sh`](./40-run-sh.md). Performs `git pull` then runs the Go-based coding-guidelines validator against the specified path.

## Usage

```powershell
.\linter-scripts\run.ps1
.\linter-scripts\run.ps1 -Path cmd -MaxLines 20
.\linter-scripts\run.ps1 -Json
.\linter-scripts\run.ps1 -d                 # pull only
```

## CLI parameters

| Param | Default | Purpose |
|-------|---------|---------|
| `-Path <string>` | `src` | Directory to scan |
| `-MaxLines <int>` | `15` | Max lines per function |
| `-Json` | switch | Emit JSON report |
| `-d` | switch | Skip validation (pull only) |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Pull + validation passed |
| 1 | Validation reported violations |
| 2 | Invocation error |

## Acceptance criteria

### AC-41-01 — Mirror parity with `run.sh`
- **Given** the same logical flags,
- **When** §40 and §41 are run on identical inputs,
- **Then** their exit codes MUST match (AC-40-03).

### AC-41-02 — `-d` skips validation
- **Given** `-d`,
- **When** the script runs,
- **Then** the validator MUST NOT be invoked.

### AC-41-03 — PowerShell `[CmdletBinding()]` parameters
- **Given** the script source,
- **When** parsed,
- **Then** parameters MUST be declared via `[CmdletBinding()]` + `param(...)` block, not via inline `$args` parsing.

## Cross-references

- §40 [`40-run-sh.md`](./40-run-sh.md) — bash counterpart.
