# 17 — check-trace-map-regression.py

**Version:** 1.0.0  
**Updated:** 2026-04-26  
**Source:** [`linter-scripts/check-trace-map-regression.py`](../../linter-scripts/check-trace-map-regression.py)  
**Category:** Gate (CI-only — fails the build on regression)


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

CI gate that runs the [`generate-trace-map.py`](./14-generate-trace-map.md) generator and then **compares the resulting `summary` block against a committed baseline** at `.lovable/memory/audit/trace-map-baseline.json`.

The build fails when **any** of these regress:

| Metric | Direction | Why it matters |
|--------|-----------|----------------|
| `ac_traced` | dropped | An AC lost its code link (was traced, now isn't) |
| `ac_drifted` | grew | Number of un-traced ACs went up |
| `code_orphan` | grew | New code landed without an AC pointer |
| `missing_ac` | > 0 | `trace-map.toml` references an AC id that no longer exists |
| `missing_file` | > 0 | `trace-map.toml` references a deleted file |

`ac_total`, `code_total`, and other absolute counters are **not** gated — they grow naturally as the spec/codebase grow.

## Usage

```bash
# CI (default): exit 1 if any tracked metric regresses against baseline
python3 linter-scripts/check-trace-map-regression.py

# After intentionally widening trace coverage (more ACs traced) — refresh baseline
python3 linter-scripts/check-trace-map-regression.py --update-baseline

# Allow ac_traced to drop by up to N during a refactor
python3 linter-scripts/check-trace-map-regression.py --tolerance 3

# Print regressions but never exit non-zero (dry-run / advisory mode)
python3 linter-scripts/check-trace-map-regression.py --report-only

# Machine-readable JSON
python3 linter-scripts/check-trace-map-regression.py --json
```

## CLI flags

| Flag | Default | Effect |
|------|---------|--------|
| `--update-baseline` | off | Overwrite baseline with current summary, exit 0 |
| `--tolerance N` | 0 | Allow `ac_traced` to drop by up to N |
| `--report-only` | off | Always exit 0 (advisory) |
| `--json` | off | Single-line JSON on stdout |

## Inputs

- `linter-scripts/generate-trace-map.py` (executed as a subprocess each run).
- `.lovable/memory/audit/trace-map.json` (produced by the generator).
- `.lovable/memory/audit/trace-map-baseline.json` (committed; the contract).

## Outputs

- Stdout: human or JSON regression report.
- No file writes unless `--update-baseline` is passed (then writes baseline).

## Baseline file format

```json
{
  "summary": {
    "ac_drifted": 471,
    "ac_total": 487,
    "ac_traced": 16,
    "code_orphan": 26,
    "code_referenced": 6,
    "code_total": 32,
    "missing_ac": 0,
    "missing_file": 0,
    "trace_entries": 16
  }
}
```

Sorted keys + 2-space indent + trailing newline → byte-stable diffs.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Healthy AND no regression |
| 1 | Regression detected OR generator returned 1 (`missing_ac` / `missing_file`) |
| 2 | Invocation/IO error (generator missing, JSON parse fail, …) |

## Acceptance criteria

### AC-17-01 — Healthy run with unchanged baseline exits 0
- **Given** `.lovable/memory/audit/trace-map.json` and `.lovable/memory/audit/trace-map-baseline.json` have identical `summary` blocks,
- **When** the script is invoked with no flags,
- **Then** it MUST exit `0` AND stdout MUST contain `✅ No regression`.

### AC-17-02 — AC coverage drop fails the build
- **Given** `current.ac_traced < baseline.ac_traced` AND `--tolerance` is unset,
- **When** the script runs,
- **Then** it MUST exit `1` AND stdout MUST contain `AC coverage regressed`.

### AC-17-03 — Drift growth fails the build
- **Given** `current.ac_drifted > baseline.ac_drifted`,
- **When** the script runs,
- **Then** it MUST exit `1` AND stdout MUST contain `Drift grew`.

### AC-17-04 — Orphan growth fails the build
- **Given** `current.code_orphan > baseline.code_orphan`,
- **When** the script runs,
- **Then** it MUST exit `1` AND stdout MUST contain `Orphan code grew`.

### AC-17-05 — `--update-baseline` rewrites the file deterministically
- **Given** any current state,
- **When** the script is run twice consecutively with `--update-baseline`,
- **Then** `.lovable/memory/audit/trace-map-baseline.json` MUST have identical SHA-256 between the two runs (sorted keys, fixed indent, trailing newline).

### AC-17-06 — `--report-only` never exits non-zero
- **Given** a regression that would normally fire exit `1`,
- **When** `--report-only` is passed,
- **Then** the script MUST still print the regression list AND MUST exit `0`.

### AC-17-07 — Generator's missing-* findings are propagated
- **Given** `trace-map.toml` references a non-existent file,
- **When** the script runs,
- **Then** it MUST exit `1` even if no regression is otherwise detected.

### AC-17-08 — CI workflow invokes the gate on every push and PR
- **Given** the `.github/workflows/spec-health.yml` workflow,
- **When** a push or PR touches `spec/`, `linter-scripts/`, or `.github/workflows/`,
- **Then** the workflow MUST run `python3 linter-scripts/check-trace-map-regression.py` AND fail the run if it exits non-zero.

## Cross-references

- §14 [`14-generate-trace-map.md`](./14-generate-trace-map.md) — the generator this gate wraps.
- §16 [`16-generate-gate-report.md`](./16-generate-gate-report.md) — the audit-side gate report (different gates, same philosophy).
- §70 [`70-spec-health-yml.md`](./70-spec-health-yml.md) — workflow that hosts this gate.
