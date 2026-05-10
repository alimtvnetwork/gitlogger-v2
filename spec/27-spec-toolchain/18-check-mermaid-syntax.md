# 18 — check-mermaid-syntax.mjs

**Version:** 1.0.0
**Updated:** 2026-04-28
**Source:** [`linter-scripts/check-mermaid-syntax.mjs`](../../linter-scripts/check-mermaid-syntax.mjs)
**Category:** Validator (Phase 97; migrated from Phase 107 orphan ledger by Phase 108-full)

---

## Purpose

Pure-parser invocation of every `spec/**/*.mmd` file via the mermaid library to catch broken diagram syntax pre-merge. No rendering, no Chromium, no network. Each file MUST parse cleanly; any parse error fails the gate with the file path + first error line.

This locks **AC-SAG-24** in [`spec/01-spec-authoring-guide/97-acceptance-criteria.md`](../01-spec-authoring-guide/97-acceptance-criteria.md).

## Usage

```bash
node linter-scripts/check-mermaid-syntax.mjs
```

No flags — single-purpose validator, runs over the entire `spec/` tree.

## Inputs

- `spec/**/*.mmd` (all mermaid diagram source files).
- `mermaid` npm package (parser only).

## Outputs

- stdout: `✓ <relpath>` per file on success, `✗ <relpath>: <first-error-line>` on failure.
- Exit code per the contract below.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All `.mmd` files parsed cleanly |
| 1 | One or more parse failures (details printed) |
| 2 | Infrastructure failure (mermaid lib missing, no files found, etc.) |

## Slot-range note

Slot **18** sits in the `10-19` generator range per the §27 §00 Normative Contract bijection table, but the file is a **validator** by behavior. This is one of three explicit Phase 108-full exceptions (slots 18, 19, 25) where the "named-slot continuity" wins over the kind-range mapping — the contract's range bands are advisory for *new* slot allocation, but file-naming `check-*` semantics dominate. See Phase 108-full retrospective for rationale; AC-T-22 verifies this slot's INV-01/INV-02 satisfaction.

## Cross-references

- [`05-check-tree-health.md`](./05-check-tree-health.md) — bijection enforcer (now sees this script via §00 inventory).
- [`spec/01-spec-authoring-guide/97-acceptance-criteria.md`](../01-spec-authoring-guide/97-acceptance-criteria.md) — AC-SAG-24 (the rule this script enforces).
- Phase 97 retrospective — origin of this script.
- Phase 107 orphan ledger — original drift detection.
- Phase 108-full retrospective — migration to this slot.
