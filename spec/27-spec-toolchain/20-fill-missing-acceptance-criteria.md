# 20 — fill-missing-acceptance-criteria.cjs

**Version:** 1.1.0  
**Updated:** 2026-04-29  
**Source:** [`linter-scripts/fill-missing-acceptance-criteria.cjs`](../../linter-scripts/fill-missing-acceptance-criteria.cjs)  
**Category:** Filler (idempotent scaffolder)

---

## Purpose

Auto-generate `97-acceptance-criteria.md` for every module under `spec/` (excluding `_archive/`) that has `00-overview.md` but no AC file. Scaffolds 5 generic, testable criteria pulled from module structure + H1 + sibling files.

**Idempotency:** re-runs on a satisfied tree are no-ops — modules already containing an AC file MUST NOT be touched.

## Usage

```bash
node linter-scripts/fill-missing-acceptance-criteria.cjs
```

## CLI flags

_(none)_

## Inputs

`spec/**/00-overview.md`.

## Outputs

New `spec/<module>/97-acceptance-criteria.md` per missing module.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All missing files scaffolded (or none were missing) |
| 1 | I/O error |

## Acceptance criteria

### AC-20-01 — Idempotency
- **Given** every module already has `97-acceptance-criteria.md`,
- **When** the script runs,
- **Then** zero files MUST be written and exit code MUST be `0`.
- **Verifies:** `linter-scripts/fill-missing-acceptance-criteria.cjs` §`main()` `fs.existsSync(target)` short-circuit

### AC-20-02 — Generated AC contains AC-NN-01 placeholder
- **Given** a freshly scaffolded file,
- **When** it is read,
- **Then** it MUST contain at least one `### AC-` heading.
- **Verifies:** `linter-scripts/fill-missing-acceptance-criteria.cjs` §`buildAC()` template (5 boilerplate ACs always emitted)

### AC-20-03 — Existing AC files are not overwritten
- **Given** an existing AC file with custom content,
- **When** the script runs,
- **Then** that file MUST be untouched (verify by mtime).
- **Verifies:** §Idempotency clause (`fs.existsSync(target)` short-circuit in `main()`)

### AC-20-04 — Boilerplate ACs carry **Verifies:** clauses (Phase 153)
- **Given** a freshly scaffolded `97-acceptance-criteria.md`,
- **When** it is read,
- **Then** every boilerplate AC (AC-01..AC-05) MUST contain BOTH a `**Source:**` line AND a `**Verifies:**` line, so the module satisfies the tree-wide P3 Verifies-coverage rule from `mem://process/verifies-clause-authoring` without manual follow-up.
- **Verifies:** `linter-scripts/fill-missing-acceptance-criteria.cjs` §`buildAC()` template; closes the audit-v6 boilerplate blind spot discovered in Phase 153.

### AC-20-05 — `upToSpec` relative-path computation is depth-aware
- **Given** a module nested at any depth under `spec/` (e.g. `spec/a/b/c/`),
- **When** `buildAC()` emits cross-links to `01-spec-authoring-guide/`,
- **Then** the relative prefix MUST equal `'../'.repeat(depth)` so generated links resolve from the module folder; the previously undefined `upToSpec` identifier (latent ReferenceError) MUST NOT recur.
- **Verifies:** `linter-scripts/fill-missing-acceptance-criteria.cjs` §`buildAC()` `depth`/`upToSpec` derivation.

## Cross-references

- §13 [`13-generate-gwt-acceptance.md`](./13-generate-gwt-acceptance.md) — *replaces* scaffolds with module-specific ACs (AI-driven).
