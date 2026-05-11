# 33 — check-ai-confidence.py

**Version:** 1.3.0  
**Updated:** 2026-04-29  
**Source:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py)  
**Self-test:** [`linter-scripts/test/test-check-ai-confidence.sh`](../../linter-scripts/test/test-check-ai-confidence.sh)  
**Category:** Validator (read-only)


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Slot-range note

Slot **33** sits in the 30-39 auditor band, but `check-ai-confidence.py` is a deterministic read-only validator (not AI-driven). Validator slots 01-09, 17-19, 24-29 are full as of Phase P48-1-fu1; renaming would break P107/H1/P47-fu0 retros and the Phase 31 lockstep. Placement follows the precedent codified for slots 18/19/32 (validators in non-validator bands). Future contributors MUST NOT "correct" the band.

---

## Purpose

Mechanizes the **`AI Confidence` four-gate rubric (P1 → P4)** defined in [`spec/17-consolidated-guidelines/01-spec-authoring.md`](../17-consolidated-guidelines/01-spec-authoring.md) § *AI Confidence Rubric (normative)* and bound by [AC-09 in §17 §97](../17-consolidated-guidelines/97-acceptance-criteria.md).

Closes **P48-1-fu1**, the open follow-up logged in P48-1's §99 row: prior to this linter, the `AI Confidence` field was author-judgement; after this linter, it is machine-derived from on-disk signals so the entire class of author-drift is eliminated. The first run on the live tree (Phase P48-1-fu1) found **13/15 modules drifting** — concrete, actionable findings (5 P1 inventory gaps, 5 P3 `**Verifies:**` coverage gaps, 3 deeper P3/P4 issues), each with a deterministic reason chain.

---

## Inputs

- `spec/<module>/00-overview.md` — declared `**AI Confidence:**` value.
- `spec/<module>/97-acceptance-criteria.md` — GWT presence, `**Verifies:**` coverage.
- `spec/<module>/99-consistency-report.md` — H1 stamp freshness.
- `spec/<module>/*.md` — truncation tail scan.
- `.github/workflows/spec-health.yml` — CI-gate references.

## Usage

```bash
python3 linter-scripts/check-ai-confidence.py
python3 linter-scripts/check-ai-confidence.py --strict
python3 linter-scripts/check-ai-confidence.py --report-only
python3 linter-scripts/check-ai-confidence.py --json
```

## CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--strict` | off | Exit 1 on ANY drift (tree-wide CI gate once adoption matures) |
| `--report-only` | off | Never fail; overrides `--strict` and per-file stamps; for dashboards |
| `--json` | off | Machine-readable JSON output (includes `stamped`, `stamped_failed`, `rows[]`) |

## Detection rules (a module's row is `match` iff)

The script computes a **derived** tier by walking gates P1 → P4 in order; the highest gate that passes wins. The declared banner value MUST equal the derived tier.

| Gate | Passes when |
|------|-------------|
| **P1** | §00 lists every sibling `.md` (excluding meta-slots `97`/`98`/`99`) AND `**Updated:**` year matches current calendar year. **Inventory regex** matches any `](./<basename>.md)` reference where the basename starts with an alphanumeric character (e.g. `01-foo.md`, `consolidated-review-guide.md`, `readme.md`, `changelog.md`, `structure.md`) — non-numeric-prefix siblings ARE legitimate inventory entries (precedent: §02 review-guide files, §03 `structure.md`, §12/§14 `readme.md`, §18 `readme.md`/`changelog.md`). |
| **P2** | P1 holds AND §97 contains ≥1 `**Given**`/`**When**`/`**Then**` marker AND no `*.md` in the module ends with a truncation marker (`...`, `…`, bare `TODO`/`TBD`/`FIXME`). |
| **P3** | P2 holds AND every `### AC-…` heading in §97 has a `**Verifies:**` clause. |
| **P4** | P3 holds AND the module is referenced by `.github/workflows/spec-health.yml` (either the leaf dir name appears verbatim, the module's `spec/<rel-path>` is mentioned, OR the workflow uses a `spec/**` glob that transitively covers the module) AND §99 carries a `<!-- verified-phase: NNN -->` stamp ≤ 30 phases stale relative to the highest stamp anywhere in the tree. |

A module with `unset`/blank `AI Confidence` is **skipped** (matches the rubric's "omit rather than guess" rule — no drift can be computed).

## Per-file opt-in stamp

Authors who have verified their banner matches the rubric-derived tier add inside the first 40 lines of `00-overview.md`:

```markdown
<!-- ai-confidence-verified-phase: NNN -->
```

Once stamped, ANY future drift on that file fails the gate even in default (advisory-tree) mode. This per-file strict promotion mirrors the H1 / P20 pattern, letting modules opt in one at a time without waiting for the whole tree to converge. The stamp name is deliberately distinct from `verified-phase` (H1 §99 freshness) and `h10-verified-phase` (P20 version parity) so the three opt-in gates remain independently trackable per file.

## Outputs

```
AI-Confidence rubric parity: scanned=N; eligible=N; matches=N; mismatches=N; stamped=N; stamped_failed=N; h1_horizon=N
  (DRIFT) spec/<module>: declared='X' derived='Y' [stamped]
      reason: P3: §97 has 8 ACs but only 0 `**Verifies:**` clauses
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All matches OR only unstamped drifts (default advisory mode) |
| 1 | `--strict` flag set AND ≥1 mismatch, OR ≥1 stamped file drifting (default mode) |

## Acceptance criteria

### AC-33-01 — Drift detected on stamped banner
- **Given** a module whose §00 carries an `<!-- ai-confidence-verified-phase: NNN -->` stamp AND a declared tier different from the derived tier,
- **When** the validator runs in default mode,
- **Then** exit code MUST be 1 and the row MUST be marked `[stamped]` in stdout.
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) per-file strict promotion path.

### AC-33-02 — Drift on unstamped banner is advisory
- **Given** a module whose §00 has NO `ai-confidence-verified-phase` stamp AND a declared tier different from the derived tier,
- **When** the validator runs in default mode,
- **Then** exit code MUST be 0 (advisory) and the drift MUST still appear in stdout for visibility.
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) advisory-by-default contract (mirrors P20 H10 pattern).

### AC-33-03 — `--strict` flips advisory to blocking
- **Given** any drift exists in the tree,
- **When** the validator runs with `--strict`,
- **Then** exit code MUST be 1 regardless of stamp status.
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) `--strict` flag.

### AC-33-04 — Lowest-passing gate wins
- **Given** a module passing P1 + P2 but failing P3,
- **When** the validator runs,
- **Then** the derived tier MUST be `Medium` (not `High`), and a module declaring `Production-Ready` MUST report a drift.
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) `derive_tier()` walk order.

### AC-33-05 — `unset` declared value is skipped
- **Given** a module whose §00 does not carry an `**AI Confidence:**` banner OR whose value is not in `{Production-Ready, High, Medium, Low}`,
- **When** the validator runs,
- **Then** the module MUST NOT appear in `rows[]` and MUST NOT contribute to `eligible`/`matches`/`mismatches`.
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) `parse_banner()` filter.

### AC-33-06 — Self-test parity
- **Given** the self-test [`test/test-check-ai-confidence.sh`](../../linter-scripts/test/test-check-ai-confidence.sh),
- **When** it runs,
- **Then** all assertions MUST pass.
- **Verifies:** [`linter-scripts/test/test-check-ai-confidence.sh`](../../linter-scripts/test/test-check-ai-confidence.sh).

### AC-33-07 — P1 inventory regex matches non-numeric-prefix siblings
- **Given** a sibling `.md` file in a module directory whose basename does NOT start with a `\d{2}-` prefix (e.g. `consolidated-review-guide.md`, `structure.md`, `readme.md`, `changelog.md`),
- **When** that file is referenced from §00 inventory as `](./basename.md)`,
- **Then** `INVENTORY_LINK_RE` MUST match the reference and `gate_p1()` MUST count the file as listed.
- **Why:** P1's intent is "every sibling `.md` is in §00 inventory" — independent of filename shape. The pre-v1.1.0 regex `\d{2}[-…].md` produced false-positive drift findings on §02/§03/§12/§14/§18 (5 of the 13 first-run drifters were this regex bug, not real spec drift). Codified at v1.1.0 (Phase P48-1-fu1-batch slot 3) after the §02 sweep surfaced both review-guide files as legitimately listed in §00 inventory at lines 191-192 yet flagged as "not in inventory".
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) `INVENTORY_LINK_RE` (line 102).

### AC-33-08 — Recursive module discovery (no nested-overview blind spot)
- **Given** a nested sub-module under `spec/<top>/<sub>/.../00-overview.md` (depth ≥ 3) carrying its own `**AI Confidence:**` banner,
- **When** the validator runs,
- **Then** the module MUST appear in `rows[]` with `module` set to the slash-joined path relative to `spec/` (e.g. `02-coding-guidelines/01-cross-language/16-static-analysis`).
- **Why:** Pre-v1.2.0 `list_modules()` only walked top-level `spec/<dir>/00-overview.md`, silently skipping ~40 of 55 banner-carrying overviews (15 visible / 56 total). Phase 153 Task #29b widened the walker via `SPEC_ROOT.rglob("00-overview.md")` and surfaced 27 latent drifts on first re-run — including 15 P3 `**Verifies:**` coverage gaps under nested sub-modules that the boilerplate-bulk Task #31 sweep could not see. Codified at v1.2.0 (Phase 153 slot, post-Task #31).
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) `list_modules()` (recursive `rglob` walk, line ~105).

### AC-33-09 — Workflow glob coverage satisfies P4
- **Given** a module whose leaf directory name does NOT appear verbatim in `.github/workflows/spec-health.yml` but the workflow declares a `spec/**` path glob,
- **When** P4 evaluates,
- **Then** the workflow-reference signal MUST be considered satisfied (P4 evaluates the §99 stamp freshness check next).
- **Why:** `spec-health.yml` triggers on `spec/**` rather than enumerating every nested module; the v1.0.0 substring check produced false-negative P4 fails on every nested module. Codified at v1.2.0 alongside AC-33-08; the two changes are coupled — widening `list_modules()` without widening P4 would have flipped most nested modules from `derived=Production-Ready` to `derived=High` purely as a workflow-coverage-detection artifact.
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) `gate_p4()` (covered = leaf-name OR rel-path OR `spec/**` glob).

### AC-33-10 — Multi-section inventory scan
- **Given** a §00 overview that carries MORE THAN ONE inventory-style section (e.g. both `## Full Document Inventory` near the top AND `## Document Inventory` near the bottom — observed in `spec/00` at Phase 153 Task #29d),
- **When** `gate_p1()` enumerates listed siblings,
- **Then** the validator MUST iterate ALL matching headings via `inv_heading_re.finditer()` and union every section's entries into the `listed` set (NOT stop at the first match).
- **Why:** Pre-v1.3.0 used `re.search()` which returned only the first heading; siblings listed exclusively in a second/third inventory section appeared "missing" even though they were present on disk and in §00. Codified at v1.3.0 (Phase 153 Task #29d) after `spec/00` cascade-fix surfaced the multi-section pattern as legitimate spec authoring (one section may enumerate top-level docs, another may enumerate sub-folders).
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) `gate_p1()` `inv_heading_re.finditer(ov_text)` loop (line ~162).

### AC-33-11 — Heading-name tolerance for inventory sections
- **Given** a §00 overview whose inventory section is titled `## Inventory`, `## Index`, `## Modules`, `## Files`, or `## Contents` (case-insensitive, optionally with leading/trailing words such as `## Full Document Inventory` or `## Module Inventory`),
- **When** `gate_p1()` searches for the inventory heading,
- **Then** `inv_heading_re` MUST match all five canonical heading names (the `(Inventory|Index|Modules|Files|Contents)` alternation, `re.M | re.I` flags).
- **Why:** Inventory-section heading names are heterogeneous across the tree by design — historic precedent supports at least five forms. Pre-v1.3.0 only matched `Inventory`, producing false-positive P1 drift on modules using `Index`/`Modules`/`Files`/`Contents`. Codified at v1.3.0 (Phase 153 Task #29d) after the cascade sweep surfaced the heterogeneity as an authoring rule, not an inconsistency.
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) `inv_heading_re` pattern (line 160).

### AC-33-12 — Bare-filename inventory entries (table cells & list items)
- **Given** a sibling `.md` referenced inside an inventory section as a bare filename (e.g. `| 01-foo.md | …description… |` table cell, `- 01-foo.md — description` list item, or any non-link mention surrounded by row/list whitespace),
- **When** `gate_p1()` parses the inventory section after locating the heading,
- **Then** `INVENTORY_BARE_RE` MUST match the bare filename and union it into `listed` alongside `INVENTORY_LINK_RE` markdown-link matches.
- **Why:** Three legitimate authoring forms coexist in the tree: (1) markdown link `[01-foo.md](./01-foo.md)`, (2) bare table cell `| 01-foo.md |`, (3) bare list item `- 01-foo.md`. Pre-v1.3.0 only counted form (1), producing false-positive P1 drift on every module using forms (2)/(3). Codified at v1.3.0 (Phase 153 Task #29d) — final regex widening that closed the AI-confidence drift class tree-wide (51/51 matches).
- **Verifies:** [`linter-scripts/check-ai-confidence.py`](../../linter-scripts/check-ai-confidence.py) `INVENTORY_BARE_RE` (line 109) + `gate_p1()` bare-filename union (line ~166).

## Cross-references

- §17 [`17-consolidated-guidelines/01-spec-authoring.md`](../17-consolidated-guidelines/01-spec-authoring.md) — *AI Confidence Rubric (normative)* (the contract this linter mechanizes).
- §17 [`17-consolidated-guidelines/97-acceptance-criteria.md`](../17-consolidated-guidelines/97-acceptance-criteria.md) — AC-09 binding.
- §17 [`17-consolidated-guidelines/98-changelog.md`](../17-consolidated-guidelines/98-changelog.md) — release rows 3.4.0 (P48-1) + 3.5.0 (P48-1-fu1).
- §27 [`29-check-version-parity.md`](./29-check-version-parity.md) — P20/P31 pattern this gate mirrors.
- §27 [`26-check-99-summary-freshness.md`](./26-check-99-summary-freshness.md) — H1 stamp pattern this gate reuses for P4 freshness.
