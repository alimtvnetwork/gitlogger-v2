# 70 — spec-health.yml

**Version:** 1.1.0  
**Updated:** 2026-04-26  
**Source:** [`.github/workflows/spec-health.yml`](../../.github/workflows/spec-health.yml)  
**Category:** CI workflow

---

## Purpose

GitHub Actions workflow wiring three spec-quality gates in series:

1. **Spec tree health gate** (§05) — score threshold.
2. **Spec cross-link gate** (§01) — zero broken internal markdown links.
3. **Trace-map regression gate** (§15) — AC coverage, drift, orphan code.

Triggers on every push to `main` and every pull request that touches `spec/`, any linter script, or this workflow file. Fails the build when any gate reports a regression.

## Trigger surface

- **Push to `main`**, paths:
  - `spec/**`
  - `linter-scripts/check-tree-health.cjs`
  - `linter-scripts/generate-spec-index.cjs`
  - `linter-scripts/check-spec-cross-links.py`
  - `linter-scripts/spec-cross-links.allowlist`
  - `.github/workflows/spec-health.yml`
- **Pull request**, paths:
  - `spec/**`
  - `linter-scripts/check-tree-health.cjs`
  - `linter-scripts/generate-spec-index.cjs`
  - `linter-scripts/check-spec-cross-links.py`
  - `linter-scripts/spec-cross-links.allowlist`

## Job

Single job `health-gate` running:

1. Checkout.
2. Set up Node.
3. Self-heal missing consistency reports, AC, and changelogs (idempotent fillers).
4. Regenerate `spec-index.md` and fail if drift detected.
5. **Spec cross-link gate** — run `python3 linter-scripts/check-spec-cross-links.py --github`. Fails on any broken internal markdown link not in the allowlist.
6. **Spec tree health gate** — run `node linter-scripts/check-tree-health.cjs --min=100 --report`.
7. **Trace-map regression gate** — run `python3 linter-scripts/check-trace-map-regression.py`.
8. Summary to GitHub step summary.

## Acceptance criteria

### AC-70-01 — Workflow file exists at canonical path
- **Given** the repository,
- **When** the path `.github/workflows/spec-health.yml` is checked,
- **Then** it MUST exist (asserted by §31 audit code-mapping).

### AC-70-02 — Trigger paths cover this toolchain module
- **Given** the workflow's `on.push.paths` and `on.pull_request.paths`,
- **When** they are inspected,
- **Then** they MUST include `spec/**`, `linter-scripts/check-spec-cross-links.py`, `linter-scripts/spec-cross-links.allowlist`, `linter-scripts/check-tree-health.cjs`, and `linter-scripts/generate-spec-index.cjs` so changes to any gate re-run the workflow.

### AC-70-03 — Cross-link gate runs before tree-health gate
- **Given** the workflow job steps,
- **When** their order is read,
- **Then** the cross-link gate MUST run before the tree-health gate because it is faster and fails on a narrower class of error.

### AC-70-04 — Tree-health threshold is 100
- **Given** the `health-gate` job step,
- **When** the `check-tree-health.cjs` invocation is read,
- **Then** `--min=` MUST be `100` (locked v3.7.7).

### AC-70-05 — Job name is stable
- **Given** the workflow,
- **When** the `name:` of the only job is read,
- **Then** it MUST be `Spec tree health gate` (used by branch-protection required-checks).

### AC-70-06 — Summary step always runs
- **Given** any preceding gate failure,
- **When** the workflow reaches the Summary step,
- **Then** `if: always()` MUST be present so results are written to the GitHub step summary even when a gate fails.

## Cross-references

- §01 [`01-check-spec-cross-links.md`](./01-check-spec-cross-links.md) — the cross-link gate this workflow invokes.
- §05 [`05-check-tree-health.md`](./05-check-tree-health.md) — the tree-health gate this workflow invokes.
- §10 [`10-generate-spec-index.md`](./10-generate-spec-index.md) — auxiliary trigger path.
- §17 [`17-check-trace-map-regression.md`](./17-check-trace-map-regression.md) — the trace-map regression gate.
