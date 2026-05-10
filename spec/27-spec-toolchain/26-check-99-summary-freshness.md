---
title: "§99 Summary freshness gate"
slot: 26
kind: validator
band: 20-29
script: linter-scripts/check-99-summary-freshness.py
status: active
---

# 26 — `check-99-summary-freshness.py`

**Phase:** H1 (2026-04-28)
**Type:** validator (advisory-then-strict)
**Band:** 20-29 (fillers/validators on §99)

## Purpose

Codify the Phase 136/139 lesson into a CI gate: §99 `## Summary` narrative claims
(counts, versions, status flags) accumulate stale assertions over time and
diverged from the source-of-truth (§97 ACs, §00 inventory) by 19 modules in
Phase 136 before a manual sweep caught it.

This validator detects §99 modules whose tracked block carries a
`<!-- verified-phase: NNN -->` stamp older than `--max-age` phases (default 20).

**Phase H2 (2026-04-28)** widened the tracked-heading set from `## Summary`
only to also accept inventory-rubric headings — the 35 §99 files that ship a
`## File Inventory` / `## Module Health` table instead of a narrative Summary.
The same stamp convention applies under any of these headings:

- `## Summary` (narrative claims — the H1 original)
- `## Module Health` (root `spec/02/99` style)
- `## File Inventory`, `## Module Inventory`, `## Top-Level Modules`,
  `## Document Inventory`, `## Modules` (inventory-table styles)

H2 also excludes `spec/_archive/**` from the scan — archived modules are
intentionally frozen and stamping them would create false freshness signals.

## Stamp convention (opt-in, per file)

```markdown
## Summary
<!-- verified-phase: 147 -->

…narrative claims about counts, versions, status flags…
```

or for inventory-rubric files:

```markdown
## File Inventory
<!-- verified-phase: 147 -->

| File | Present |
|------|---------|
| 00-overview.md | ✅ |
```

Files **without** the stamp emit a per-file `info` line and do **not** fail —
the gate is advisory until project-wide stamp adoption is decided in a future
phase or via R1 (real-AI re-audit).

## Exempt-marker convention (Phase H8)

Some §99 files have no narrative claims and no inventory rubric — only
date-anchored audit-log subsections (e.g. `## 2026-04-27 — Phase 69 audit`).
Stamping such files makes no sense (there's nothing to verify). They declare
their freshness posture via a whole-file marker:

```markdown
# Consistency Report — …
<!-- freshness-exempt: audit-log-only -->

## 2026-04-27 — Phase 69 audit
…
```

Recognized format: `<!--\s*freshness-exempt:\s*([a-z0-9_\-]+)\s*-->` — anywhere
in the file (NOT heading-scoped, unlike `verified-phase`). The reason token is
informational; canonical first reason is `audit-log-only`. Exempt files are
counted under `exempt:` and skipped before the find-stamp pass — they never
increment the unstamped advisory count.

After Phase H8: **87/87 §99 files declare a posture** (81 stamped + 6 exempt).

## CLI

```
python3 linter-scripts/check-99-summary-freshness.py [--report-only] [--max-age N]
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | All stamped §99 Summary blocks within budget (or `--report-only`) |
| 1 | At least one stamped §99 file is stale beyond `--max-age` |
| 2 | Structural error (cannot determine current phase) |

## Current-phase detection

Scans the highest `Phase NNN` token visible in:
1. `mem://index.md` (.lovable/memory/index.md)
2. `spec/27-spec-toolchain/98-changelog.md`

Whichever yields the highest integer wins.

## Why the slot is 26

- Slots 20-29 are the validator/filler band on §99 / §97 / §98 lifecycle. §26
  fits naturally between `25-deepen-consistency-reports` (filler) and the
  audit-tooling slots starting at §30.
- No slot-range exception needed.

## Acceptance criteria

### AC-26-01 — Unstamped §99 files do not fail the gate
- **Given** a §99 file with no `<!-- verified-phase: NNN -->` stamp under its `## Summary`,
- **When** `check-99-summary-freshness.py` runs (default mode, no flags),
- **Then** the file MUST be reported as `(info) … unstamped` AND MUST NOT cause exit 1.

### AC-26-02 — Stamped fresh files pass
- **Given** a §99 file whose `## Summary` carries a `<!-- verified-phase: NNN -->` stamp where `current_phase - NNN <= --max-age`,
- **When** the gate runs,
- **Then** exit 0 with the file counted under `stamped:` and not in the `stale` list.

### AC-26-03 — Stamped stale files fail in strict mode
- **Given** a §99 file whose stamp delta `> --max-age`,
- **When** the gate runs WITHOUT `--report-only`,
- **Then** exit 1 with the file in the stale list AND with `[stamp: Phase NNN, delta: D]` in the output.

### AC-26-04 — `--report-only` never fails
- **Given** any combination of stale stamps,
- **When** the gate runs WITH `--report-only`,
- **Then** exit 0 with the same stale list printed but a `--report-only: not failing.` footer.

### AC-26-05 — Missing current-phase source exits 2
- **Given** neither `mem://index.md` nor `spec/27-spec-toolchain/98-changelog.md` contains a `Phase NNN` token,
- **When** the gate runs,
- **Then** exit 2 with `ERROR: cannot determine current phase` on stderr.

### AC-26-06 — Inventory-rubric headings accepted (Phase H2)
- **Given** a §99 file whose `## File Inventory` (or `## Module Health` / `## Module Inventory` / `## Top-Level Modules` / `## Document Inventory` / `## Modules`) carries a fresh `<!-- verified-phase: NNN -->` stamp,
- **When** the gate runs,
- **Then** exit 0 with the file counted under `stamped:` — same as if the stamp lived under `## Summary`.

### AC-26-07 — `spec/_archive/**` excluded from scan (Phase H2)
- **Given** any `99-consistency-report.md` under `spec/_archive/`,
- **When** the gate runs,
- **Then** the file MUST NOT appear in scan/stamped/unstamped counts — archived modules are frozen and excluded by design.

### AC-26-08 — Multi-block stamp scan (Phase H2)
- **Given** a §99 file with multiple tracked headings (e.g. `## File Inventory` followed by `## Summary`) where the stamp lives under the second heading,
- **When** the gate runs,
- **Then** the stamp MUST be found and the file counted as `stamped:` (highest phase number wins if multiple stamps exist).

### AC-26-09 — Freshness-exempt marker honored (Phase H8)
- **Given** a §99 file carrying `<!-- freshness-exempt: <reason> -->` anywhere in its body (not heading-scoped),
- **When** the gate runs,
- **Then** the file MUST be counted under `exempt:` AND MUST NOT increment `unstamped:` AND MUST NOT cause exit 1, regardless of whether any tracked heading is present or any stamp exists.

### AC-26-10 — Misplaced stamp detection (Phase H9)
- **Given** a §99 file containing `<!-- verified-phase: NNN -->` OUTSIDE any tracked-heading body AND followed within ≤3 non-empty lines by a tracked heading,
- **When** the gate runs in default mode,
- **Then** an advisory warning MUST be emitted (`stamp(s) placed immediately BEFORE a tracked heading`) AND exit code MUST remain 0.
- **When** the gate runs with `--strict-position`,
- **Then** the same finding MUST cause exit 1 (unless `--report-only` is also set).
- **Negative case**: a stamp inside a blockquote or other narrative far from any tracked heading (e.g. §27's Validation History referencing past phases) MUST NOT be flagged — only adjacency to a tracked heading constitutes misplacement.

## Cross-references

- §99 [`99-consistency-report.md`](./99-consistency-report.md) — health/inventory; this gate is itself listed in §99's File Inventory.
- §00 [`00-overview.md`](./00-overview.md) — Phase H1 adds the Validators-band row for slot 26.
- `mem://index.md` — Core rules around stale-prose §99 sweeps (Phase 136/139 precedent) which this gate codifies.
- Phase 136 retrospective (`.lovable/memory/audit/v2-deterministic/phase-136-stale-prose-sweep.md` if present).
- Phase 139 retrospective (similar).

## Slot-range note

Slot 26 is a clean fit in the 20-29 validator/filler band (no exception needed,
unlike slots 18/19 in the 10-19 generator band per AC-T-22/AC-T-23).

## Changelog

### 1.3.0 — 2026-04-28 — Phase H9 (stamp-position structural enforcement)
- **Promoted H8 stamp-position precedent to lint check.** New `find_misplaced_stamps()` detects `<!-- verified-phase: NNN -->` placed OUTSIDE any tracked-heading body but immediately ABOVE a tracked heading (within ≤3 non-empty lines). Runs on every non-exempt §99 file each invocation.
- **New `--strict-position` flag**: turns the misplaced-stamp finding into an exit-1 failure. Without the flag, advisory warning only.
- **CI wired strict immediately**: `.github/workflows/spec-health.yml` step `§99 Summary freshness gate (Phase H1 / H8 / H9)` now passes `--strict-position` because the real tree has 0 misplaced findings post-H8 — flipping strict immediately locks the gain (no risk of false positives, no migration window needed).
- **Adjacency-only rule** (vs whole-file outside-body): chosen because §27's own §99 legitimately documents past stamps inside Validation History blockquotes (lines 6, 24). Whole-file rule would emit false positives; adjacency rule (`stamp → ≤3 non-empty lines → tracked heading`) catches the real H8 failure mode (`stamp\n\n## Summary`) without flagging documentation references.
- Self-test extended 20 → **27 assertions** (T12 misplaced advisory mode, T13 `--strict-position` exits 1, T14 blockquote-buried stamp not flagged).
- Acceptance criteria addition: AC-26-10 (misplaced stamp detection — both modes + negative case).
- **No AC-31-31 cascade, no rubric bump, no new gate**: same slot-26 gate, tighter contract within existing CI step.

### 1.2.0 — 2026-04-28 — Phase H8 (freshness coverage closure)
- **New `<!-- freshness-exempt: <reason> -->` marker** recognized anywhere in file body (not heading-scoped). Files matching are counted under `exempt:` and skipped before the find-stamp pass.
- **Output line shape changed**: `§99 files scanned: N; stamped: N; exempt: N; unstamped: N` (added `exempt:` field between stamped and unstamped).
- **Output line shape changed**: `§99 files scanned: N; stamped: N; exempt: N; unstamped: N` (added `exempt:` field between stamped and unstamped).
- **Coverage closure**: 75 stamped + 12 unstamped → **81 stamped + 6 exempt + 0 unstamped** (87/87 declare a posture). The 6 exempt files are audit-log-only — no `## Summary` and no inventory rubric, only date-anchored audit-log subsections.
- **Stamp-position fix sweep** (one-time): 5 files carried the stamp BEFORE `## Summary` rather than under it; repositioned. Precedent codified — stamps MUST live inside a tracked-heading body, not adjacent.
- **§27's own §99**: stamp tokens were only inside Validation History blockquotes (not under any tracked heading); added `<!-- verified-phase: 147 -->` under `## File Inventory`.
- Self-test extended 12 → **20 assertions** (T1 counts-line shape requires `exempt:` field; new T11 verifies exempt-marker behavior in 3 sub-asserts).
- Acceptance criteria addition: AC-26-09 (freshness-exempt marker honored).

### 1.1.0 — 2026-04-28 — Phase H2
- **Widened tracked-heading set** from `## Summary` only to also accept inventory-rubric headings (`## Module Health`, `## File Inventory`, `## Module Inventory`, `## Top-Level Modules`, `## Document Inventory`, `## Modules`). Previously-exempt 35 inventory-rubric §99 files are now stampable.
- **Excluded `spec/_archive/**`** from scan — archived modules are frozen.
- **Multi-block scan**: stamp under ANY tracked heading is accepted (highest stamp wins). Previously only the FIRST tracked heading was checked, which broke files where File Inventory appeared before Summary.
- Added 3 new self-test cases (T8 stamp under Module Health, T9 stamp under File Inventory, T10 _archive/ exclusion).
- Adoption sweep: 46/89 → **75/87** stamped (~86%); remaining 12 are audit-log-style §99 files with no inventory or summary heading (structurally exempt — no claims to drift).
- Acceptance criteria additions: AC-26-06 (inventory-rubric headings accepted), AC-26-07 (`_archive/` excluded), AC-26-08 (multi-block scan).

### 1.0.0 — 2026-04-28 — Phase H1
- Initial version. Advisory-mode gate with opt-in `<!-- verified-phase: NNN -->` stamps.
- Default `--max-age = 20` (≈ 2-3 weeks of typical phase cadence).
- CI wired into `.github/workflows/spec-health.yml` after the folder-refs gate (15th strict gate); runs in default mode (advisory — exits 0 because zero §99 files are stamped at H1 close).
