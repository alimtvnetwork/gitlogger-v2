---
title: "§99 stamp-bump enforcement gate"
slot: 27
kind: validator
band: 20-29
script: linter-scripts/check-99-stamp-bump.py
status: active
---

# 27 — `check-99-stamp-bump.py`

**Phase:** H4 (2026-04-28)
**Type:** validator (event-based; advisory-then-strict)
**Band:** 20-29 (validators on §99)

## Purpose

**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->

Turn the H1/H2 honor-system into a CI check: when a `99-consistency-report.md`
file is materially edited (any non-stamp line changed in the diff), the
`<!-- verified-phase: NNN -->` stamp MUST be bumped to the current phase
in the same diff. Catches the failure mode where an author edits a §99
narrative claim or inventory row but forgets to bump the stamp, silently
leaving the file's claim of freshness misleading.

## Two-layer defense

| Gate | Style | Trigger | Budget |
|---|---|---|---|
| `check-99-summary-freshness.py` (slot 26) | snapshot | always | `--max-age 20` phases |
| **`check-99-stamp-bump.py` (slot 27)** | **event-based** | **on §99 edit** | **0 (must bump)** |

Together they enforce: "stamps must be bumped on edit, AND must not decay
past 20 phases without re-verification".

## Stamp convention

Same as slot 26 (Phase H1/H2): `<!-- verified-phase: NNN -->` under any of
`## Summary`, `## Module Health`, `## File Inventory`, `## Module Inventory`,
`## Top-Level Modules`, `## Document Inventory`, `## Modules`. Multi-block
scan; highest stamp wins.

## CLI

```
python3 linter-scripts/check-99-stamp-bump.py \
  [--base-ref REF] [--report-only] \
  [--changed-files FILE] [--treat-as-stamp-only]
```

- `--base-ref REF` — git ref to diff against (default: `$STAMP_BUMP_BASE_REF` or `origin/main`).
- `--report-only` — never exit 1; print findings and exit 0.
- `--changed-files FILE` — **test injection only**: read newline-separated list of §99 paths instead of running `git diff`. Bypasses git entirely. Used by self-test sandboxes.
- `--treat-as-stamp-only` — **test injection only**: paired with `--changed-files`, treat all listed files as stamp-only diffs (skip).

## Exit codes

| Code | Meaning |
|---|---|
| 0 | All materially-edited stamped §99 files have a bumped stamp (or `--report-only`) |
| 1 | At least one materially-edited stamped §99 file has a stale stamp |
| 2 | Structural error (cannot determine phase, git diff failed, etc.) |

## Skip-rules

A changed §99 file is SKIPPED (not failed) when:

1. **Unstamped** — file has no `<!-- verified-phase: NNN -->` under any tracked
   heading. Adoption is opt-in per file (per H1/H2 design); this gate only
   enforces "if you stamped, you must keep it fresh on edit". Becomes a
   ratchet — once stamped, this gate begins enforcing.
2. **Stamp-only diff** — the only changed lines (additions/deletions) are
   stamp lines. That IS the bump; no failure.
3. **`spec/_archive/**`** — Phase H3 convention. Archived modules are frozen.

## CI integration

Wired into `.github/workflows/spec-health.yml` after the slot-26 freshness
gate. Runs in default mode against `origin/main` as the base ref. PRs that
edit §99 files must bump the stamp or the gate fails.

For local pre-commit usage: `STAMP_BUMP_BASE_REF=HEAD~1 python3 linter-scripts/check-99-stamp-bump.py`.

## Why slot 27

Slot 27 is the next sequential slot in the 20-29 validator/filler band
(slots 20-26 occupied; 27/28/29 free; 30+ is the audit-tooling band). No
slot-range exception needed — this is a clean adjacent fit to slot 26 (the
sister freshness gate it complements).

## Acceptance criteria

### AC-27-01 — Empty diff exits 0
- **Given** no §99 files appear in the git diff against the base ref,
- **When** the gate runs,
- **Then** exit 0 with `No §99 files changed in diff. ✅`.

### AC-27-02 — Unstamped §99 edits are skipped
- **Given** a changed §99 file with no stamp under any tracked heading,
- **When** the gate runs,
- **Then** the file MUST be counted under `unstamped (skip)` AND MUST NOT cause exit 1.

### AC-27-03 — Stamp-only diffs are skipped
- **Given** a changed §99 file whose ONLY changed lines (additions/deletions) are stamp comment lines,
- **When** the gate runs,
- **Then** the file MUST be counted under `stamp-only diff` AND MUST NOT cause exit 1.

### AC-27-04 — Materially-edited stamped files MUST bump
- **Given** a changed §99 file whose stamp is NOT equal to the current phase AND whose diff contains non-stamp changes,
- **When** the gate runs WITHOUT `--report-only`,
- **Then** exit 1 with the file in the `unbumped` list and `[stamp: Phase NNN, current: Phase MMM]` in the output.

### AC-27-05 — `--report-only` never fails
- **Given** any combination of unbumped files,
- **When** the gate runs WITH `--report-only`,
- **Then** exit 0 with the same unbumped list printed but a `--report-only: not failing.` footer.

### AC-27-06 — `_archive/` excluded from diff scan
- **Given** a §99 file under `spec/_archive/**` appears in the git diff,
- **When** the gate runs,
- **Then** the archived file MUST NOT count in `Changed §99 files`. (Phase H3 convention.)

### AC-27-07 — Bad base-ref exits 2
- **Given** `--base-ref` points to a nonexistent git ref,
- **When** the gate runs,
- **Then** exit 2 with `git diff failed against base '...'` on stderr.

### AC-27-08 — Missing phase token exits 2
- **Given** neither `mem://index.md` nor `spec/27-spec-toolchain/98-changelog.md` contains a `Phase NNN` token,
- **When** the gate runs,
- **Then** exit 2 with `cannot determine current phase` on stderr.

## Cross-references

- §26 [`26-check-99-summary-freshness.md`](./26-check-99-summary-freshness.md) — sister freshness gate (snapshot mode); both share the same stamp grammar.
- §99 [`99-consistency-report.md`](./99-consistency-report.md) — health/inventory; this gate is itself listed in §99's File Inventory.
- §00 [`00-overview.md`](./00-overview.md) — Phase H4 adds the Validators-band row for slot 27.
- `mem://index.md` — Core rules around §99 freshness (Phase H1/H2/H3 lineage).

## Slot-range note

Slot 27 is a clean fit in the 20-29 validator/filler band (no exception needed,
unlike slots 18/19 in the 10-19 generator band per AC-T-22/AC-T-23). Adjacent
to slot 26 (`check-99-summary-freshness.py`), its semantic sibling.

## Changelog

### 1.0.0 — 2026-04-28 — Phase H4
- Initial version. Event-based validator complementing slot-26 snapshot gate.
- Default base ref `origin/main` (overridable via `--base-ref` or `STAMP_BUMP_BASE_REF`).
- Test-injection flags `--changed-files` and `--treat-as-stamp-only` to bypass git for sandboxed self-tests.
- CI wired into `.github/workflows/spec-health.yml` after slot-26 freshness gate as the **16th strict gate**.
