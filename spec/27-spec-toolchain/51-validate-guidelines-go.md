# 51 — validate-guidelines.go

**Version:** 1.1.0  
**Updated:** 2026-05-10 (Sess-66 G-6s — paired with slot 50; static-surface probe `linter-scripts/test/test-validate-guidelines-go-surface.sh` shipped + wired as **gate #45**; six clauses including AC-51-01 parity anchor with frozen 10-rule TOLERATED_PY_ONLY baseline-drift set; phantom 8 → 7)  
**Source:** [`linter-scripts/validate-guidelines.go`](../../linter-scripts/validate-guidelines.go)  
**Category:** Source validator (Go port — preferred for speed)  
**Status:** Active gate #45 (load-proven via static-surface probe; no Go runtime in CI per Lesson #36 link-don't-restate — full Go execution lives in §02 coding-guidelines workflow when promoted)

---

## Purpose

Go port of §50 [`validate-guidelines.py`](./50-validate-guidelines-py.md). Provides the same rule set with substantially better performance for large repos. The Go binary is the production validator; the Python version is the reference implementation.

## Rules enforced

Identical to §50:

- CODE-RED-001 No nested if
- CODE-RED-002 Boolean naming
- CODE-RED-003 No magic strings
- CODE-RED-004 Max 15 lines/function
- CODE-RED-005 No `fmt.Errorf` in Go
- CODE-RED-006 No `(T, error)` returns
- CODE-RED-P2/P3/P5/P7 boolean principles

## Usage

```bash
go run linter-scripts/validate-guidelines.go --path src --max-lines 15
go run linter-scripts/validate-guidelines.go --json
go build -o bin/validate-guidelines linter-scripts/validate-guidelines.go
```

## CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--path <dir>` | `src` | Directory to scan |
| `--max-lines <n>` | `15` | CODE-RED-004 threshold |
| `--json` | off | Machine-readable report |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | No violations |
| 1 | At least one violation |
| 2 | Invocation error |

## Acceptance criteria

### AC-51-01 — Parity with Python reference
- **Given** identical input,
- **When** §50 and §51 run,
- **Then** the violation list MUST be identical (modulo line ordering).

### AC-51-02 — `package main`
- **Given** the source file,
- **When** read,
- **Then** the first non-comment line MUST be `package main` (it is a CLI binary, not a library).

### AC-51-03 — Version banner in source comment header
- **Given** the file header,
- **When** read,
- **Then** it MUST include a `Version: X.Y.Z (DATE)` comment matching §50.

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-51/`) and run `python3 linter-scripts/validate-guidelines-go.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #45 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/validate-guidelines-go.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #45 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## Cross-references

- §50 [`50-validate-guidelines-py.md`](./50-validate-guidelines-py.md) — reference implementation.
