# 50 — validate-guidelines.py

**Version:** 1.1.0  
**Updated:** 2026-05-10 (Sess-66 G-6r — added `--self-test` synthetic-fixture probe; wired into `.github/workflows/spec-health.yml` as **gate #41** load-proven check; phantom 9 → 8)  
**Source:** [`linter-scripts/validate-guidelines.py`](../../linter-scripts/validate-guidelines.py)  
**Category:** Source validator (Python)  
**Status:** Active gate #44 (load-proven via `--self-test`; src-tree scan owned by §02 coding-guidelines workflow, not this gate)

---

## Purpose

Cross-language coding-guidelines validator. Validates Go, PHP, TypeScript, and Rust source files against the rules defined in [`spec/02-coding-guidelines/`](../02-coding-guidelines/). Enforces rules ESLint cannot cover (Go, PHP, Rust) and provides a unified report across all languages.

## Rules enforced

| Rule | Description |
|------|-------------|
| CODE-RED-001 | No nested if statements |
| CODE-RED-002 | Boolean naming (`is/has/can/should/was` prefix) [P1] |
| CODE-RED-003 | No magic strings in comparisons |
| CODE-RED-004 | Max 15 lines per function (configurable) |
| CODE-RED-005 | No `fmt.Errorf()` in Go (use apperror) |
| CODE-RED-006 | No `(T, error)` returns in Go services (use `Result[T]`) |
| CODE-RED-P2/P3/P5/P7 | Boolean-principle checks |

## Usage

```bash
python3 linter-scripts/validate-guidelines.py
python3 linter-scripts/validate-guidelines.py --path cmd --max-lines 20
python3 linter-scripts/validate-guidelines.py --json
python3 linter-scripts/validate-guidelines.py --fix
```

## CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--path <dir>` | `src` | Directory to scan |
| `--max-lines <n>` | `15` | CODE-RED-004 threshold |
| `--json` | off | Machine-readable report on stdout |
| `--fix` | off | Auto-fix safe violations |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | No violations |
| 1 | At least one violation |
| 2 | Invocation error (bad path, etc.) |

## Acceptance criteria

### AC-50-01 — Parity with Go port
- **Given** identical input,
- **When** §50 (Python) and §51 (Go) run,
- **Then** the violation list MUST be identical (modulo line ordering).

### AC-50-02 — `--max-lines` overrides default
- **Given** `--max-lines 30` and a 25-line function,
- **When** the script runs,
- **Then** CODE-RED-004 MUST NOT fire for that function.

### AC-50-03 — Version banner present in source
- **Given** the script's docstring,
- **When** read,
- **Then** it MUST include a `Version: X.Y.Z (DATE)` line.

## Cross-references

- §51 [`51-validate-guidelines-go.md`](./51-validate-guidelines-go.md) — Go port (preferred for speed).
- [`spec/02-coding-guidelines/`](../02-coding-guidelines/) — rule sources.
