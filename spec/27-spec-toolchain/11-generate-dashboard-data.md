# 11 — generate-dashboard-data.cjs

**Version:** 1.3.0  
**Updated:** 2026-04-28  
**Source:** [`linter-scripts/generate-dashboard-data.cjs`](../../linter-scripts/generate-dashboard-data.cjs)  
**Category:** Generator


**Test pair:** N/A — generator  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

Scan the `spec/` tree and emit `spec/dashboard-data.json` consumed by [`spec/health-dashboard.md`](../health-dashboard.md). Performs:

1. Validate all markdown cross-references (broken-link detection).
2. Check required files (`00-overview.md`, `99-consistency-report.md`).
3. Count files per subfolder.
4. **(v1.1.0, Phase 34)** Compute per-module rubric-v2.0.0 quality credits — mirrors [`05-check-tree-health.md`](./05-check-tree-health.md) so the dashboard score equals the CI gate score.
5. Output a JSON report.

## Rubric v2.0.0 (Phase 34 propagation)

The generator now mirrors the rubric used by `check-tree-health.cjs`:

| Dimension | Weight | Credit |
|-----------|-------:|--------|
| Required | 60 % | 1 per `00-overview.md`, 1 per `99-consistency-report.md` |
| Recommended | 25 % | 1 per `97-acceptance-criteria.md`, 1 per `98-changelog.md` |
| Quality | 15 % | 1 per §99 ≥30 non-blank lines + 1 per Validation History heading + 1 per File/Module Inventory heading |

`Health.Score` and `Health.Grade` are now driven by the rubric. The legacy
deduction-based score is retained as `Health.LegacyScore` for back-compat
with any tooling that depended on the previous behaviour.

## Usage

```bash
node linter-scripts/generate-dashboard-data.cjs
node linter-scripts/generate-dashboard-data.cjs --json
node linter-scripts/generate-dashboard-data.cjs --quiet
```

## CLI flags

| Flag | Purpose |
|------|---------|
| `--json` | Emit only the JSON report on stdout, suppress human summary |
| `--quiet` | Suppress non-error stderr noise |

## Outputs

- `spec/dashboard-data.json` (overwritten)
- Optional human summary on stderr

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Report generated (broken links may still exist; this script reports, doesn't gate) |
| 1 | I/O error |

## Acceptance criteria

### AC-11-01 — JSON schema is stable
- **Given** the generated `spec/dashboard-data.json`,
- **When** parsed,
- **Then** it MUST contain top-level keys `Generated`, `Health`, `RubricV2`, `Links`, `RequiredFiles`, `Inventory` with the same shape across runs.

### AC-11-04 — Rubric parity with `check-tree-health.cjs`
- **Given** a clean spec tree (both linters return success),
- **When** `RubricV2.Score` is read from `dashboard-data.json` and compared to the score reported by `check-tree-health.cjs --report`,
- **Then** the two scores MUST be equal (rubric v2.0.0 is the single source of truth).

### AC-11-02 — `--quiet` produces no stderr
- **Given** a successful run with `--quiet`,
- **When** stderr is captured,
- **Then** it MUST be empty.

### AC-11-03 — Output file ends with newline
- **Given** `spec/dashboard-data.json` after a run,
- **When** read,
- **Then** the final byte MUST be `\n`.

### AC-11-05 — Inline-code blanking parity with `check-spec-cross-links.py` (Phase P44)
- **Given** a markdown narrative line containing an inline-code-wrapped link such as `` [`test-foo.sh`](./test-foo.sh) `` (where the link text is itself an inline-code span and the target is an example pattern, NOT a real file),
- **When** the dashboard generator's `extractLinks()` parses the file,
- **Then** the inline-code span MUST be blanked (same-length space run preserving char offsets) BEFORE `LINK_RE` matches, mirroring `check-spec-cross-links.py:strip_inline_code()` (P0 Python checker, ported from there in Phase P44).
- **AND** the resulting `Links.Total.Broken` count MUST be 0 whenever `python3 linter-scripts/check-spec-cross-links.py` reports `OK All internal spec cross-references resolve.` — the two link counters MUST agree on the broken-set (parity contract; without this AC the JS counter over-reports false positives that the Python gate already correctly suppresses, producing baseline noise like the `./test-foo.sh` row that lingered in `Health.Deductions` from Phase 102 through P43).
- **Verifies:** `linter-scripts/generate-dashboard-data.cjs:137-176` (`INLINE_CODE_RE` constant + `blankInlineCode()` helper + `extractLinks()` invocation); `linter-scripts/check-spec-cross-links.py:57-66` (`strip_inline_code()` reference implementation that this AC ports parity from); [`linter-scripts/test/test-inline-code-blanking-parity.sh`](../../linter-scripts/test/test-inline-code-blanking-parity.sh) — Phase P45 self-test, 8-fixture corpus asserting byte-identical output between the two helpers + length preservation invariant (mechanical lock; without this self-test the parity contract is reviewer-attention-only).

## Cross-references

- [`spec/health-dashboard.md`](../health-dashboard.md) — consumer.
- [`spec/27-spec-toolchain/01-check-spec-cross-links.md`](./01-check-spec-cross-links.md) — Python sibling whose `strip_inline_code` semantics AC-11-05 ports parity from.

## Changelog

### 1.3.0 — 2026-04-28 — Phase P45: AC-11-05 mechanical lock via `test-inline-code-blanking-parity.sh`
- **Action**: Authored [`linter-scripts/test/test-inline-code-blanking-parity.sh`](../../linter-scripts/test/test-inline-code-blanking-parity.sh) (#13 in `linter-scripts/test/README.md` inventory). 8-fixture corpus invokes both `check-spec-cross-links.py::strip_inline_code()` (via `importlib`) and `generate-dashboard-data.cjs::blankInlineCode()` (via `node -e` + helper extraction) on shared inputs and asserts byte-identical output + length preservation per fixture. 17 assertions; runtime ~1 s. Wired into `.github/workflows/spec-health.yml` `Spec cross-link gate` step (folded, not standalone — H1 workflow-step parity rule: single existing gate exercise, no AC-31-31 cascade, gate count stays at 19/19/19).
- **Outcome**: AC-11-05 dual-implementation parity contract is now mechanically enforced — any future divergence between the JS and Python helpers fails CI on PR rather than surfacing as silent dashboard-counter drift (the P44 root-cause class). Extended the AC-11-05 `Verifies:` block to cite the new self-test as third source.
- **Spec**: This file v1.2.0 → **v1.3.0**: extended AC-11-05 `Verifies:` line with self-test pointer + Phase-P45 narrative parenthetical ("mechanical lock; without this self-test the parity contract is reviewer-attention-only"). README inventory totals 12 → 13 scripts, 142+ → 159+ assertions. P45 lesson codified in mem-index: "**graduate parity ACs from review-time to CI-time** — when an AC's `Verifies:` clause cites two sibling implementations of the same logical contract, the natural completion is a self-test that exercises both and asserts equality on a fixture corpus; until then the AC is contract-only and the divergence-detection gradient is reviewer-effort-quadratic. P44→P45 demonstrates the 1-phase graduation cost (single self-test, no CI plumbing change beyond a folded `bash` line)."
- **No new CI workflow step, no RUBRIC_VERSION bump, no AC-31-31 cascade, no gate-count change.** Trace-map rebaseline required (+1 code file, AC-traced delta 0 since AC-11-05 already existed).

### 1.2.0 — 2026-04-28 — Phase P44: inline-code blanking parity with Python cross-link checker
- **Action**: Added `INLINE_CODE_RE` constant + `blankInlineCode()` helper + `extractLinks()` integration in `linter-scripts/generate-dashboard-data.cjs` (lines 137-176). Mirrors `check-spec-cross-links.py:strip_inline_code()` semantics: inline-code spans are replaced with same-length space runs BEFORE `LINK_RE` matches, preserving char offsets so line numbers stay accurate. Closes a parity gap between the JS dashboard generator and the Python strict CI gate that had produced one persistent false-positive (`./test-foo.sh` example pattern in §27 §98 line 501 P102 narrative) lingering in `Health.Deductions` from Phase 102 through P43.
- **Outcome**: `Links.Total.Broken` 1 → **0**; `Links.Total.Checked` 3079 → **3073** (6 inline-code-wrapped example patterns correctly skipped); `Health.LegacyScore` 98 → **100**; `Health.Deductions` `["1 broken links (-2)"]` → **`[]`**. Cross-link gate output unchanged (it was already correct via `strip_inline_code`); only the dashboard JSON aligns now.
- **Spec**: This file v1.1.0 → **v1.2.0**: added AC-11-05 with full GWT body + parity contract + `Verifies:` block citing both the new JS code and the Python reference implementation; added `## Changelog` block; expanded `## Cross-references` with §01 Python-sibling pointer.
- **No CI workflow change, no RUBRIC_VERSION bump, no AC-31-31 cascade, no gate-count change, no trace-map rebaseline** — bug fix in a generator's link counter, contract-tightening only. The new AC documents the parity invariant so future divergences are caught at AC-review time.
