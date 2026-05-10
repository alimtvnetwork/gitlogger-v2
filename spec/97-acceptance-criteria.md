# Acceptance Criteria — Specification Root

**Version:** 1.0.0  
**Updated:** 2026-04-27  
**Scope:** `spec/` (root index module)  
**Generated:** Phase 46 — root D-tier cleanup

---

## Module Summary

This module is the **root index** for the entire specification tree. It declares the canonical inventory of top-level spec modules (01–28+), enforces slot immutability, and is consumed by `linter-scripts/generate-dashboard-data.cjs` and `linter-scripts/check-spec-cross-links.py` when emitting `spec/dashboard-data.json` and `spec/spec-index.md`.

---

## Inlined Contracts

> The normative `SpecTreeIndex` JSON Schema is inlined verbatim in [`./00-overview.md`](./00-overview.md) §"Normative Contract — Spec Tree Index" so each AC below is self-contained.

```text
ENUM Status: ["active", "locked-vacant", "deprecated", "slot-collision"]
RANGE Number: integer 0..99
PATTERN Slug: ^[a-z0-9]+(-[a-z0-9]+)*$
PATTERN Path: ^\./[0-9]{2}-[a-z0-9-]+/00-overview\.md$
LOCKED-VACANT SLOTS: {08, 09}  // never authored, never reused
```

---

## Acceptance Criteria

### AC-ROOT-01: Module inventory bijection  `[critical]`
- **Given** the root `spec/00-overview.md` "Module Inventory" tables (Core 01–20 + App-Specific 21+),
- **When** the spec tree is scanned by `linter-scripts/check-spec-cross-links.py`,
- **Then** every directory matching `spec/[0-9]{2}-*/00-overview.md` MUST appear exactly once in the inventory tables, AND every inventory row MUST resolve to an existing `00-overview.md` (or be marked `**Locked vacant slot**` for slots 08, 09).
- **Verifies:** `00-overview.md` §Module Inventory.

### AC-ROOT-02: Locked-vacant slot immutability  `[high]`
- **Given** slot numbers 08 (`Docs Viewer UI`) and 09 (`Code Block System`),
- **When** a developer attempts to author `spec/08-*/` or `spec/09-*/`,
- **Then** the addition MUST be rejected by `linter-scripts/check-tree-health.cjs --strict`, AND the inventory row MUST continue to read `**Locked vacant slot** — never authored`.
- **Verifies:** `00-overview.md` §Module Inventory; `spec/01-spec-authoring-guide/02-naming-conventions.md` §Reserved ranges.

### AC-ROOT-03: SpecTreeIndex schema validity  `[critical]`
- **Given** the normative `text`-fenced JSON-Schema block in `00-overview.md` §"Normative Contract",
- **When** `linter-scripts/generate-dashboard-data.cjs` validates a synthesised module list against it,
- **Then** every emitted module entry MUST satisfy `required: [number, slug, path, status]` AND `additionalProperties: false`. A row that violates the schema MUST cause the script to exit non-zero and refuse to write `dashboard-data.json`.
- **Verifies:** `00-overview.md` §Normative Contract; `spec/27-spec-toolchain/11-generate-dashboard-data.md`.

### AC-ROOT-04: Slug + path pattern enforcement  `[high]`
- **Given** any inventory row,
- **When** validated against `PATTERN Slug = ^[a-z0-9]+(-[a-z0-9]+)*$` and `PATTERN Path = ^\./[0-9]{2}-[a-z0-9-]+/00-overview\.md$`,
- **Then** uppercase letters, underscores, double-dashes, and paths missing the leading `./` MUST fail validation.
- **Verifies:** `00-overview.md` §Normative Contract.

### AC-ROOT-05: Status enum closed set  `[medium]`
- **Given** the `Status` enum `["active", "locked-vacant", "deprecated", "slot-collision"]`,
- **When** a module declares any other value (e.g. `wip`, `planned`, `draft`),
- **Then** the dashboard generator MUST reject it. Slot collisions (two modules sharing one number) are only legal when both rows declare `status = "slot-collision"` — single-occupant rows MUST use `active`, `locked-vacant`, or `deprecated`.
- **Verifies:** `00-overview.md` §Normative Contract enforcement note.

### AC-ROOT-06: Supporting-files presence  `[medium]`
- **Given** the §"Supporting Files" table,
- **When** the spec tree is rendered,
- **Then** `folder-structure-root.md`, `spec-index.md`, `health-dashboard.md`, and `dashboard-data.json` MUST all exist at `spec/` root. Missing entries MUST cause `check-tree-health.cjs --strict` to fail.
- **Verifies:** `00-overview.md` §Supporting Files.

### AC-ROOT-07: Frontmatter `kind: index` declaration  `[high]`
- **Given** the root `spec/00-overview.md`,
- **When** read by the deterministic auditor (`linter-scripts/audit-spec-vs-code-v2.py` v2.9+),
- **Then** the YAML frontmatter MUST declare `kind: index` so the rubric applies the index-router baseline (impl=70, +10 child bonus → 80) and exempts the module from the `G-CON-01` contract gate. Other `kind` values (`future-spec`, `tracker`, `meta-toolchain`) are rejected for this module.
- **Verifies:** `00-overview.md` frontmatter; `spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md` AC-31-15.

### AC-ROOT-08: Lockstep enforcement  `[medium]`
- **Given** the root module ships `spec/00-overview.md`, `spec/97-acceptance-criteria.md`, `spec/98-changelog.md`, `spec/99-consistency-report.md`,
- **When** any of these files is edited,
- **Then** `linter-scripts/check-lockstep.cjs` MUST report 0 findings: the §00 banner version, the topmost §98 row, and the topmost §99 banner-update row MUST share the same date AND mention the same phase.
- **Verifies:** `spec/27-spec-toolchain/24-check-lockstep.md`.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Spec Authoring Guide](./01-spec-authoring-guide/00-overview.md) — naming + folder-structure rules.
- [Spec Toolchain — Audit v2](./27-spec-toolchain/31-audit-spec-vs-code-v2.md) — rubric this module is scored against.
