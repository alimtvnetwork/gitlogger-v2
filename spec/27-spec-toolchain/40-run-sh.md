# 40 — run.sh

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/run.sh`](../../linter-scripts/run.sh)  
**Category:** Runner (bash entry point)


**Test pair:** N/A — scaffold  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

The bash entry point for the local validation pipeline. Performs `git pull` then runs the coding-guidelines validator (Go binary if present, else Python). The Windows mirror is §41 [`run.ps1`](./41-run-ps1.md).

## Usage

```bash
./linter-scripts/run.sh                          # scan src/ (default)
./linter-scripts/run.sh -d                       # git pull only, skip validation
./linter-scripts/run.sh --path cmd --max-lines 20
./linter-scripts/run.sh --json
```

## CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--path <dir>` | `src` | Directory to scan |
| `--max-lines <n>` | `15` | Max lines per function (CODE-RED-004) |
| `--json` | off | Emit JSON report on stdout |
| `-d` | off | Skip validation (pull only) |

## Behaviour

1. `set -euo pipefail` (fail-fast).
2. `git pull` (warn but continue if not a git repo).
3. Invoke validator §50 / §51.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Pull + validation passed |
| 1 | Validation reported violations |
| 2 | Invocation error (bad flag, validator missing) |

## Acceptance criteria

### AC-40-01 — `-d` skips validation
- **Given** `-d`,
- **When** the script runs,
- **Then** the validator MUST NOT be invoked.

### AC-40-02 — `--json` is forwarded to the validator
- **Given** `--json`,
- **When** the validator is invoked,
- **Then** the validator's CLI MUST receive `--json`.

### AC-40-03 — Mirror parity with `run.ps1`
- **Given** the same flags,
- **When** §40 and §41 are run on identical inputs,
- **Then** their exit codes MUST match.

## Cross-references

- §41 [`41-run-ps1.md`](./41-run-ps1.md) — Windows mirror.
- §50, §51 — invoked validators.
