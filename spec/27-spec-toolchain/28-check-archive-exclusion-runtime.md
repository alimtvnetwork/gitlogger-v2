---
title: "Runtime archive-exclusion gate"
slot: 28
kind: validator
band: 20-29
script: linter-scripts/test/test-archive-exclusion-runtime.sh
status: active
---

# 28 — `test-archive-exclusion-runtime.sh`

**Phase:** H7 (2026-04-28)
**Type:** validator (self-test that IS the gate; no separate production validator)
**Band:** 20-29 (validators on §99 / spec-traversal hygiene)

## Purpose

**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->

Codify the **H6 lesson** "runtime > source verification" as a standing CI gate.

Phase H3 audited 12 spec-traversing linters by **source-reading** (`grep`-ing for
`_archive` exclusion guards) and concluded they all properly skip
`spec/_archive/`. Phase H6 elevated 3 critical ones to **runtime** verification by
`importlib`-loading each module and calling its enumerator on the live tree —
catching any divergence between "source says it excludes" and "runtime
actually excludes". H7 freezes that runtime probe into a CI gate so a future
contributor cannot silently regress the H3 convention by dropping the
`if "_archive" not in p.parts` guard during a refactor.

## Why this matters

Source-reading audits have a known failure mode: a refactor that **moves** the
exclusion check (e.g. into a helper function that is then accidentally not
called) can pass `grep` but fail at runtime. Only a runtime probe — load the
actual module, call the actual enumerator, inspect the actual results —
catches this class of regression.

This is the **17th strict CI gate** and the only one that exercises **runtime
behavior of other linters** as its assertion target.

## Probes (Phase H7 baseline; floor ≥ 3)

| Linter | Enumerator | Expected archive-leaked |
|---|---|---|
| `linter-scripts/check-99-summary-freshness.py` | `find_99_files()` | **0** (of ~87) |
| `linter-scripts/audit-spec-vs-code-v2.py` | `ALL_MODULES` (module-level) | **0** (of ~87) |
| `linter-scripts/generate-trace-map.py` | `collect_ac_ids()` | **0** (of ~1315) |

The self-test enforces a floor of **≥ 3 active probes** so a future
contributor cannot accidentally drop coverage by deleting probe blocks.

## CLI

```
bash linter-scripts/test/test-archive-exclusion-runtime.sh
```

No flags. Pure runtime probe. Exits 0 on all-green, 1 on any leakage.

## How to add a new probe

When you add a new spec-traversing linter, add a runtime probe in
`linter-scripts/test/test-archive-exclusion-runtime.sh`:

```python
# ── Probe N: <linter-name>.<enumerator>() ────────────────────────
try:
    m = load('<short-name>', 'linter-scripts/<linter>.py')
    items = list(m.<enumerator>())
    leaked = [x for x in items if '_archive' in str(x).split('/')]
    results['<short-name>'] = (len(items), len(leaked))
except Exception as e:
    results['<short-name>'] = ('ERR', str(e))
```

The bash assertions auto-extend via the `get_total` / `get_leaked` parsers.

## Acceptance criteria

### AC-28-01 — All baseline probes load successfully
- **Given** the 3 baseline linters exist and import cleanly,
- **When** the self-test runs,
- **Then** each probe MUST return a non-`ERR` total count.

### AC-28-02 — Zero archive leakage in all probes
- **Given** the 3 baseline enumerators are called on the live spec tree,
- **When** the results are filtered for `_archive` in path components,
- **Then** the leaked count MUST be 0 for every probe.

### AC-28-03 — Sanity floors on enumerator output
- **Given** the spec tree contains ≥ 80 §99 files / ≥ 80 modules / ≥ 1000 ACs,
- **When** each probe runs,
- **Then** the total counts MUST satisfy these floors (catches a probe that
  silently returns `[]` due to a refactor breaking the enumerator's
  signature — e.g. `find_99_files()` renamed without updating the probe).

### AC-28-04 — Probe count floor ≥ 3
- **Given** the self-test inventory of probes,
- **When** the self-test runs,
- **Then** the number of active probes (lines matching `^[a-z]+\|` in
  the probe output) MUST be ≥ 3. Codifies "you cannot remove the H7 baseline".

### AC-28-05 — Self-test exits 0 on all-green; 1 on any leakage
- **Given** all assertions pass,
- **When** the self-test exits,
- **Then** exit code MUST be 0 with the success banner.
- **Given** any assertion fails,
- **When** the self-test exits,
- **Then** exit code MUST be 1 (CI failure).

## Cross-references

- §26 [`26-check-99-summary-freshness.md`](./26-check-99-summary-freshness.md) — `find_99_files()` is one of the probed enumerators.
- §27 [`27-check-99-stamp-bump.md`](./27-check-99-stamp-bump.md) — sister `_archive/`-aware gate (Phase H3 convention).
- §31 [`31-audit-spec-vs-code-v2.md`](./31-audit-spec-vs-code-v2.md) — `ALL_MODULES` is one of the probed enumerators; AC-31-31 cascade contract.
- §99 [`99-consistency-report.md`](./99-consistency-report.md) — health/inventory; this gate is itself listed in §99's File Inventory.
- §00 [`00-overview.md`](./00-overview.md) — Phase H7 adds the Validators-band row for slot 28.
- `mem://index.md` — Core rules around `_archive/` exclusion (Phase H3) and runtime > source verification (Phase H6 → H7).

## Slot-range note

Slot 28 is a clean fit in the 20-29 validator/filler band (no exception
needed, unlike slots 18/19 in the 10-19 generator band per AC-T-22/AC-T-23).
Adjacent to slot 27 (`check-99-stamp-bump.py`); both are H-series validators
on `_archive/`-aware spec traversal.

## Self-test note (no separate production validator)

Unlike slots 26 / 27 which have a production `.py` validator paired with a
`test-*.sh` self-test, slot 28's "validator" IS the self-test. The probe
logic is too thin to justify a separate production script — there is nothing
for the validator to do except load other modules and assert on their
enumerator output, which IS what self-tests do. This is why the workflow step
collapses to a single `bash linter-scripts/test/test-archive-exclusion-runtime.sh`
invocation (no separate `python3 linter-scripts/<some-validator>.py` line).

This is a sanctioned exception to the F3 rule "self-tests SHOULD be `.sh`":
the file IS a `.sh` self-test, but it occupies a §27 slot as a validator
because that is its functional role in CI. Future contributors MUST NOT
"correct" this by inventing a thin `.py` wrapper just to fit the
"validator = `.py` script" pattern; the empty wrapper would be ceremony
without value.

## Changelog

### 1.0.0 — 2026-04-28 — Phase H7
- Initial version. Codifies H6 lesson "runtime > source verification" as a CI gate.
- 3 baseline probes (`check-99-summary-freshness.find_99_files`, `audit-spec-vs-code-v2.ALL_MODULES`, `generate-trace-map.collect_ac_ids`) with floor ≥ 3.
- Wired into `.github/workflows/spec-health.yml` between H5 stamp-bump and Trace-map regression as the **17th strict CI gate**.
- AC-31-31 cascade: RUBRIC v2.25 → v2.26; gate count 16 → 17; footer entry #17; EXECUTIVE-SUMMARY back-ref; qa-baseline-footer awk +1.
