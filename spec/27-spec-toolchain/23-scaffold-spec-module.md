# 23 — scaffold-spec-module.cjs

**Version:** 1.0.0
**Updated:** 2026-04-26
**Source:** [`linter-scripts/scaffold-spec-module.cjs`](../../linter-scripts/scaffold-spec-module.cjs)
**Category:** Filler / scaffolder

---

## Purpose

Emit a v2.0.0-rubric-compliant spec module skeleton (§00, §97, §98, §99) so a freshly created module passes `check-tree-health.cjs --strict` on its very first run.

Phase 37 — prevents the next thin-§99 wave (cf. Phase 31, where 9 modules needed deepening) by making "do it right" the path of least resistance. New modules start at 100/100 quality credits instead of needing remediation later.

## Companion to §20–§22 fillers

| Filler | When it fires |
|--------|---------------|
| §20 `fill-missing-acceptance-criteria` | Existing module is missing §97 |
| §21 `fill-missing-changelogs` | Existing module is missing §98 |
| §22 `fill-missing-consistency-reports` | Existing module is missing §99 |
| **§23 `scaffold-spec-module`** (this) | **New module being created from scratch** |

The §20–§22 fillers heal existing modules; this scaffolder prevents new modules from ever needing healing.

## Usage

```bash
node linter-scripts/scaffold-spec-module.cjs <slot> <slug> [--title="..."] [--force]
```

### Examples

```bash
node linter-scripts/scaffold-spec-module.cjs 29 spec-toolchain-extras
node linter-scripts/scaffold-spec-module.cjs 30 telemetry --title="Telemetry Pipeline"
node linter-scripts/scaffold-spec-module.cjs 31 audit-cadence --title="Audit Cadence" --force
```

## Arguments

| Arg | Format | Notes |
|-----|--------|-------|
| `<slot>` | 2-digit (00–99) | Must not collide with existing folder. File slots are immutable per project memory rule. |
| `<slug>` | kebab-case lowercase | Combined into folder name `spec/<slot>-<slug>/`. |

## Flags

| Flag | Purpose |
|------|---------|
| `--title="..."` | Human-readable title (defaults to slug title-cased). |
| `--force` | Overwrite existing files. Use sparingly; usually you want the per-file skip behaviour. |

## What gets written

| File | Contents |
|------|----------|
| `00-overview.md` | H1 title, version banner v1.0.0, Updated date, Scope, Purpose/Scope/Out-of-scope sections marked TODO, cross-references block. |
| `97-acceptance-criteria.md` | 5 baseline ACs (AC-01..AC-05) covering structural compliance: entry point exists, sibling links resolve, naming convention, §99 present, passes `--strict`. |
| `98-changelog.md` | v1.0.0 baseline release row + format guide. |
| `99-consistency-report.md` | Health score table (100/100 baseline), File Inventory table, **Validation History** section, Outstanding TODOs, cross-references. ≥30 non-blank lines guaranteed. |

The §99 template intentionally hits all 3 quality-credit anchors (≥30 non-blank lines, "Validation History" heading, "File Inventory" heading) so a fresh scaffold scores 3/3 quality without further work.

## Slot collision safety

Before writing anything, the script enumerates `spec/` and refuses if any other folder starts with `<slot>-`. This enforces the project memory rule: **"File slots are immutable once shipped — never reuse a number."**

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Module scaffolded (or all files already existed without `--force`) |
| 1 | Invalid args, slot collision, or write error |

## Acceptance criteria

### AC-23-01 — Fresh scaffold passes `--strict`
- **Given** a slot with no existing folder,
- **When** `node linter-scripts/scaffold-spec-module.cjs <slot> <slug>` runs,
- **Then** the resulting module MUST score `req=2/2 rec=2/2 q=3/3` under `check-tree-health.cjs --strict --report`.

### AC-23-02 — Slot-collision refusal
- **Given** a slot already taken by another folder,
- **When** the script runs with that slot and a different slug,
- **Then** it MUST exit `1` and print the conflicting folder name without writing any file.

### AC-23-03 — Idempotency (no `--force`)
- **Given** a module folder already populated by a previous run,
- **When** the script runs again without `--force`,
- **Then** existing files MUST be skipped (with a per-file `· skip` log line) and exit code MUST be `0`.

### AC-23-04 — Slug + slot validation
- **Given** invalid input (slug with uppercase / spaces / underscores, or slot with non-digits),
- **When** the script runs,
- **Then** it MUST exit `1` with a clear "must be kebab-case" or "must be 2-digit" error message.

### AC-23-05 — Quality-credit anchors present in template
- **Given** the generated `99-consistency-report.md`,
- **When** it is inspected,
- **Then** it MUST contain a `## Validation History` heading, a `## File Inventory` heading, and ≥30 non-blank lines — i.e., all 3 quality credits the v2.0.0 rubric scores.

## Cross-references

- §05 [`05-check-tree-health.md`](./05-check-tree-health.md) — rubric v2.0.0 the scaffold targets.
- §20 [`20-fill-missing-acceptance-criteria.md`](./20-fill-missing-acceptance-criteria.md) — companion healer.
- §21 [`21-fill-missing-changelogs.md`](./21-fill-missing-changelogs.md) — companion healer.
- §22 [`22-fill-missing-consistency-reports.md`](./22-fill-missing-consistency-reports.md) — companion healer.
- [Spec authoring guide — required files](../01-spec-authoring-guide/03-required-files.md).
