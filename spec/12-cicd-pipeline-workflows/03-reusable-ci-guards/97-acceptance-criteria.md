# Acceptance Criteria — Reusable CI Guards — AI-Implementation Guide

**Version:** 1.2.0  
**Updated:** 2026-05-04 (Phase 153 A24-fu43-fu1: AC-CG-09 archetype runtime GWT — closes parent AC-13 stub mandate for reusable-ci-guards subfolder.)  
**Scope:** `spec/12-cicd-pipeline-workflows/03-reusable-ci-guards/`

---

## Purpose

This document defines testable acceptance criteria for the **Reusable CI Guards — AI-Implementation Guide** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/12-cicd-pipeline-workflows/03-reusable-ci-guards/`
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
- **Given** the module file `spec/12-cicd-pipeline-workflows/03-reusable-ci-guards/00-overview.md`
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

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `01-forbidden-name-guard.md`
- `02-grandfather-baseline-naming.md`
- `03-cross-file-collision-audit.md`
- `04-baseline-diff-lint-gate.md`
- `05-actionable-lint-suggestions.md`
- `06-matrix-test-aggregator.md`
- `07-shared-cli-wrapper.md`
- `08-config-schema.md`
- `09-workflow-templates.md`
- `99-ai-implementation-guide.md`

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

---

## Archetype-Specific Runtime Criteria (Phase 153 A24-fu43-fu1)

> **Namespace note:** This folder uses the `AC-CG-NN` family per parent AC-12 Subfolder Delegation Map. Per parent AC-12 + Core file-slot-immutability rule, this `AC-CG-NN` namespace is collision-free with `spec/02-coding-guidelines/`'s `AC-CG-NN` family because they live in different module slots — references MUST cite the full module path (`spec/12-cicd-pipeline-workflows/03-reusable-ci-guards/97-acceptance-criteria.md#ac-cg-09`) when crossing module boundaries.

### AC-CG-09: Forbidden-name guard runtime contract `[high]`
- **Given** a downstream repo with a flat-namespace package layer (e.g. Go `package x` files, Node `index.{ts,js}` siblings, Python `__init__.py` re-exports) and a `forbidden-names.yaml` file at repo root listing identifiers reserved by the host project,
- **When** the forbidden-name guard pattern declared in `01-forbidden-name-guard.md` runs as a CI step (composite action wrapping the language-specific implementation per Pattern 07 + Pattern 08),
- **Then** ALL of the following invariants MUST hold for the guard's behaviour:
  1. **Diff-scope** — the guard MUST scan ONLY identifiers introduced in the PR (vs the merge-base of the target branch); pre-existing forbidden names in the baseline are grandfathered (Pattern 02). Implementation: `git diff --name-only $(git merge-base origin/<target> HEAD) HEAD` then parse added lines for identifier declarations.
  2. **Exit-code contract** — exit `0` when no new forbidden identifiers found; exit `1` when ≥1 new forbidden identifier detected; exit `2` ONLY for guard-internal errors (missing config, parse failure, `git` unavailable). The runner MUST distinguish `1` (real finding — block PR) from `2` (infrastructure failure — alert maintainers, do not block PR per Pattern 04 baseline-diff discipline).
  3. **Output format** — on exit `1`, the guard MUST print one finding per line in the shape `<file>:<line>:<col>: forbidden identifier '<name>' (declared in forbidden-names.yaml under '<reason>')`. Format MUST be greppable + machine-parseable for Pattern 05 (actionable lint suggestions PR comment).
  4. **Configuration surface** — `forbidden-names.yaml` MUST follow the schema declared in `08-config-schema.md`: top-level `forbidden:` map of `<name>: { reason: <string>, suggested_alternative: <string|null> }`. Unknown top-level keys MUST cause exit `2` (fail-fast on schema drift).
  5. **Language adapter contract** — every language adapter (Go/Node/Python/Rust per `01-forbidden-name-guard.md` §Adaptations) MUST satisfy invariants 1–4 identically; the only adapter-specific code is the identifier-extraction regex/AST-walker. Per Pattern 07 (shared CLI wrapper), all adapters dispatch through a single `--phase check` entry point.
  6. **Baseline regeneration** — the guard MUST support `--regen-baseline` mode that updates the cached baseline of grandfathered identifiers (Pattern 02). The baseline file path MUST be configurable via `forbidden-names.yaml`'s `baseline_path:` key.
- **Source:** `01-forbidden-name-guard.md` §Algorithm + §Inputs/outputs/exit codes; `02-grandfather-baseline-naming.md` §Baseline discipline; `04-baseline-diff-lint-gate.md` §Exit-code separation; `07-shared-cli-wrapper.md` §Phase dispatch; `08-config-schema.md` §Schema.
- **Verifies:** parent `spec/12-cicd-pipeline-workflows/97-acceptance-criteria.md` AC-13 [medium] (per-archetype GWT stub mandate) for the reusable-ci-guards axis. Closes audit-v7 finding `[D2 HIGH] Archetype GWT Stubs` for this subfolder.

**Forbidden patterns** (CI MUST fail-fast):
- Guard scans the whole tree (not just PR diff) — produces noise on pre-existing baseline identifiers + violates Pattern 02 grandfathering.
- Guard returns exit `1` on infrastructure failure (e.g. missing `forbidden-names.yaml`) — masks real findings under tooling errors; MUST be exit `2`.
- Output format that is not greppable (multi-line per finding, ANSI colour codes in non-TTY mode, JSON without `--format json` flag).
- Adapter that diverges from invariants 1–4 to handle "language-specific exception" — exceptions belong in `forbidden-names.yaml`, NOT adapter code.
