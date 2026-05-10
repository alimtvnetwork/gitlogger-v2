# Acceptance Criteria — Consolidated Audit Findings — `git-logs` App Specification

**Version:** 1.2.0  
**Updated:** 2026-05-10  
**Scope:** `spec/25-app-issues/02-consolidated-audit-findings/`

---

## Purpose

This document defines testable acceptance criteria for the **Consolidated Audit Findings — `git-logs` App Specification** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/25-app-issues/02-consolidated-audit-findings/`
- **When** `00-overview.md` is opened
- **Then** it contains an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Source:** `00-overview.md`
- **Verifies:** §00 Module overview baseline (H1 + Version + Updated banner)

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file exists in this module folder.
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.
- **Verifies:** §00 cross-reference inventory; `linter-scripts/check-spec-cross-links.py`

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all match `^[0-9]{2}-[a-z0-9-]+\.md$` (or are recognized special files like `README.md`).
- **Source:** `../../01-spec-authoring-guide/02-naming-conventions.md`.
- **Verifies:** `spec/01-spec-authoring-guide/02-naming-conventions.md` §Filename pattern

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** `99-consistency-report.md` is opened
- **Then** it lists every `.md` file in this folder under "File Inventory" with status ✅.
- **Source:** `99-consistency-report.md`.
- **Verifies:** §99 File Inventory rubric

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module contributes `required=2/2` (overview + consistency report present) and the overall score is ≥ 80.
- **Source:** `linter-scripts/check-tree-health.cjs`.
- **Verifies:** `linter-scripts/check-tree-health.cjs` §required=2/2 contribution

---

### AC-06: Module overview is non-trivial and version-banner-stamped
- **Given** the module file `spec/25-app-issues/02-consolidated-audit-findings/00-overview.md`
- **When** the file is read by `linter-scripts/audit-spec-vs-code-v2.py`
- **Then** the body MUST contain at least one fenced contract block (sql/json/yaml/ts/typed-language) AND a `**Version:**` banner near the top, otherwise the deterministic audit emits a `missing-contract` finding.
- **Source:** `linter-scripts/audit-spec-vs-code-v2.py` (rubric v2.13).
- **Verifies:** `linter-scripts/audit-spec-vs-code-v2.py` rubric v2.13 (G-CON-01 contract gate)

### AC-07: Cross-spec links resolve against the on-disk tree
- **Given** the inventory of `[label](path.md)` links in this module's `00-overview.md`
- **When** `python3 linter-scripts/check-spec-cross-links.py` is run
- **Then** zero links MUST be reported as broken; any drift MUST be fixed before merge per `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Source:** `linter-scripts/check-spec-cross-links.py`.
- **Verifies:** `linter-scripts/check-spec-cross-links.py` §Phase 81 strict gate

### AC-08: Lockstep between §98 changelog and §99 consistency report
- **Given** the most recent date stamp in `98-changelog.md`
- **When** `node linter-scripts/check-lockstep.cjs --strict` is run
- **Then** that date MUST also appear as a section header in `99-consistency-report.md`; the strict gate (Phase 81) blocks merge on any mismatch.
- **Source:** `linter-scripts/check-lockstep.cjs`.
- **Verifies:** `linter-scripts/check-lockstep.cjs` §strict date+phase parity


---

### AC-09: Finding `Status` field is a closed enum (A-04, Session 26)

- **Given** every `F-NN` finding row in `00-overview.md` (active table + Appendix Z stubs)
- **When** the `Status` field is parsed
- **Then** its value MUST be one of the four enum members declared in the canonical contract block below — no free-form strings, no aliases, no synonyms. Any other value is a `finding-status-enum-violation` lint failure (blocks merge).

**Canonical contract — `FindingStatus` enum** (kind: contract; source-of-truth for §27 lint rule `finding-status-enum-check`):

```yaml
# Closed enum — extending requires §25 §97 AC-09 amendment + §98 changelog entry + §99 lockstep.
FindingStatus:
  - Open                       # default — awaiting remediation
  - InProgress                 # PR open or active work; rendered as "In progress" in markdown prose
  - Resolved                   # fix landed; row retained for traceability with closing-commit link
  - DeScopedArchiveOnly        # target lives under spec/_archive/ and outside scope-lock; rendered as "De-scoped (archive-only)"
```

**Markdown ↔ enum mapping** (the markdown prose label is the human-readable form; the enum member is the lint key):

| Markdown label (prose) | Enum member (lint key) | Counts toward active rollup? |
|---|---|---:|
| `Open` | `Open` | Yes |
| `In progress` | `InProgress` | Yes |
| `Resolved` | `Resolved` | Yes (kept for traceability; severity unchanged) |
| `De-scoped (archive-only)` | `DeScopedArchiveOnly` | **No** (collapses to 1-line stub per §00 "How to Use" table) |

**Detection.** §27 toolchain rule `finding-status-enum-check` parses every `**Status:**` line under an `F-NN` heading in `00-overview.md` and asserts `value ∈ {Open, In progress, Resolved, De-scoped (archive-only)}`. Disposition values from the v1→v2 disposition map (A-02) are scoped to the disposition table only and are NOT counted as `Status` values — the lint rule MUST scope its parse to `## F-NN` sections.

**Reconciliation.** Supersedes the prior F-16 prose-table treatment (now de-scoped in Appendix Z). The "How to Use This Document" table in `00-overview.md` (line 27) describes the same four values in prose; this AC promotes that prose to a machine-checkable contract.

- **Source:** `00-overview.md` `## How to Use This Document` Status row · `00-overview.md` `## v1→v2 Finding Disposition Map` (A-02) · §27 toolchain `finding-status-enum-check` lint rule (to be implemented).
- **Verifies:** §00 Status enum (4 members, closed) · §27 `finding-status-enum-check` lint rule · A-02 disposition-map scoping invariant.

---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`

---

## Validation

Run the full pipeline:

```bash
bash linter-scripts/run.sh
```

This executes: validator → self-heal → regen index → tree-health gate. All steps must exit 0 for this module's acceptance to hold.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module consistency report](./99-consistency-report.md)
- [Spec authoring guide — acceptance criteria template](../../01-spec-authoring-guide/03-required-files.md)
