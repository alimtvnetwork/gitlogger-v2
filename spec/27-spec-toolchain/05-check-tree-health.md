# 05 — check-tree-health.cjs

**Version:** 2.0.0
**Updated:** 2026-04-26
**Source:** [`linter-scripts/check-tree-health.cjs`](../../linter-scripts/check-tree-health.cjs)
**Category:** Validator (gate)

---

## Purpose

Compute a `spec/` tree health score from disk truth and fail (exit `1`) when below threshold. This is the **CI gate** that locks progress and prevents regressions in basic structural compliance.

## Rubric (v2.0.0, Phase 30)

For each module folder under `spec/`:

| Dimension | Weight | Credit |
|-----------|-------:|--------|
| **Required** | 60 % | +1 `00-overview.md` present, +1 `99-consistency-report.md` present |
| **Recommended** | 25 % | +1 `97-acceptance-criteria.md` present, +1 `98-changelog.md` present |
| **Quality** (§99 depth) | 15 % | +1 §99 ≥ 30 non-blank lines; +1 §99 has Validation History/Findings/Audit History/Change History heading; +1 §99 has File/Module/Document Inventory/Top-Level Modules/Modules heading |

`score = required_pct + recommended_pct + quality_pct` (rounded, max 100)

## Usage

```bash
node linter-scripts/check-tree-health.cjs                # default --min=75
node linter-scripts/check-tree-health.cjs --min=80       # custom threshold
node linter-scripts/check-tree-health.cjs --strict       # threshold 100 + ALL modules at full marks
node linter-scripts/check-tree-health.cjs --report       # per-module breakdown
```

## CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--min=<n>` | `75` | Minimum acceptable composite score (0–100) |
| `--strict` | off | Phase 36 — equivalent to `--min=100` AND additionally fails if any single module has missing files or quality < max |
| `--report` | off | Print every module's credit breakdown |

`--strict` exists because the composite score can round to 100 while individual modules slip credits. CI workflows that must enforce zero regression should pass `--strict`; the default 75 threshold is preserved for ad-hoc local runs.

## Outputs

Header block + per-module table when `--report`. Final line: `✓ PASS:` or `✗ FAIL:` with reason.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Score ≥ `--min`; if `--strict`, also every module at full marks |
| 1 | Score below threshold, OR (`--strict` only) any module below full marks |

## Acceptance criteria

### AC-05-01 — Default threshold is 75
- **Given** the script invoked with no arguments,
- **When** the spec tree scores 74,
- **Then** it MUST exit `1`.

### AC-05-02 — Missing required file decreases score
- **Given** a module without `00-overview.md`,
- **When** the script runs,
- **Then** the missing file MUST decrement the Required dimension score, potentially pushing composite below `--min`.

### AC-05-03 — `--report` lists every module
- **Given** `--report`,
- **When** the script runs,
- **Then** every module folder MUST appear with its `req=X/Y rec=A/B q=C/3[hits]` breakdown.

### AC-05-04 — Rubric v2.0.0 weighting
- **Given** any spec tree,
- **When** the score is computed,
- **Then** Required MUST contribute up to 60 points, Recommended up to 25 points, and Quality up to 15 points (sum ≤ 100, with rounding).

### AC-05-05 — `--strict` enforces module-level perfection
- **Given** a tree with composite score 100 but at least one module missing a quality credit,
- **When** the script runs with `--strict`,
- **Then** it MUST exit `1` and list each below-full-marks module with its specific gap (`missing: <files>` and/or `quality N/3`).

### AC-05-06 — `--strict` is implied threshold 100
- **Given** the script invoked with `--strict` but no `--min`,
- **When** the threshold is reported,
- **Then** it MUST be `100` (overriding the default `75`).

## Cross-references

- §20–§22 fillers raise the score by scaffolding missing files.
- §70 [`70-spec-health-yml.md`](./70-spec-health-yml.md) wires this into the event-driven CI workflow (uses `--min=100`).
- §71 [`71-spec-monthly-audit-yml.md`](./71-spec-monthly-audit-yml.md) wires this into the monthly cadence audit (uses `--strict`, Phase 36).
- §11 [`11-generate-dashboard-data.md`](./11-generate-dashboard-data.md) mirrors this rubric for the dashboard scorer (Phase 34 parity).
