---
title: "§00 ↔ §98 Version-field parity gate"
slot: 29
kind: validator
band: 20-29
script: linter-scripts/check-version-parity.py
status: active
---

# 29 — `check-version-parity.py`

**Phase:** P15 / H10 landed advisory; **Phase P31** flipped to strict tree-wide (2026-04-28).
**Type:** validator (**strict tree-wide** as of P31; was advisory-by-default P15→P30)
**Band:** 20-29 (validators on §99/§97/§98 lifecycle)

## Purpose

**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->

Codify the **Phase 21 lesson** as a CI gate: when a spec module's
`00-overview.md` carries a `**Version:** vX.Y.Z` banner AND a sibling
`98-changelog.md` ships a parseable release line, the §00 banner version
SHOULD equal the latest §98 release version. The lockstep gate (§24)
only checks **date relations** (L1: §98 latest date ≥ §00 Updated date)
— it does NOT check version strings, so the §00 banner can drift many
releases behind §98 while lockstep stays green.

**Phase 21 precedent**: `spec/27-spec-toolchain/00-overview.md` was
discovered at v1.7.0 while §98 was at v2.46.2 — ~39 patch releases
behind, lockstep-invisible.

**Phase P15 baseline sweep (2026-04-28)**: validator's first run
discovered **59 / 74 eligible modules** carry a §00 ↔ §98 version-field
mismatch. The Phase 21 disposition note ("1/3 historical incident, low
surface") was a vast under-count — the surface is systemic, not
incidental. Advisory mode chosen so adoption can proceed PR-by-PR
without blocking 59 unrelated modules in a single sweep.

## Scope and skip rules

The gate scans every `spec/**/00-overview.md` (recursive), with these
skip rules:

1. **`spec/_archive/**` excluded** — archived modules are frozen by
   design (H2 lesson, mirrors slot 26 freshness gate).
2. **No `**Version:**` banner in §00** → counted under
   `skipped(no-banner)`. Opt-in: a module without a banner version cannot
   drift, so it cannot be flagged.
3. **No sibling `98-changelog.md`** → silently skipped (the module isn't
   under lockstep at all).
4. **Sibling `98-changelog.md` with no parseable release line** →
   counted under `skipped(no-release)`. Accepts four release shapes:
   - `## 1.2.0 — 2026-04-28` (heading)
   - `### v4.0.0 — 2026-04-26` (heading)
   - `## [4.1.0] — 2026-04-26` (bracketed heading)
   - `| 3.9.8 | 2026-04-28 | … |` (table-row format, folder 22 style)

## CLI

```
python3 linter-scripts/check-version-parity.py [--strict] [--report-only] [--json] [--spec-root PATH]
```

| Flag | Behavior |
|---|---|
| _(default)_ | Advisory tree-wide; exit 0 even on mismatch — UNLESS the mismatched §00 carries a Phase P20 `<!-- h10-verified-phase: NNN -->` stamp, in which case that file fails per-file strict and the gate exits 1. (Script-level default unchanged at P31; CI now invokes `--strict` — see Phase P31 row in Changelog.) |
| `--strict` | Exit 1 on any mismatch. **As of Phase P31, the CI workflow invokes the gate with `--strict` since the reverse-drift backlog cleared at P30 (matches=74/74).** |
| `--report-only` | Never fails (overrides `--strict` AND per-file stamps). Useful for dashboards. |
| `--json` | Machine-readable output with `details[]` array (each entry includes `stamped: <int|null>`); top-level `stamped` and `stamped_failed` counts. |
| `--spec-root PATH` | Override scan root (used by self-test sandboxes). |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Default mode with zero stamped failures, OR `--strict` with zero mismatches, OR `--report-only` |
| 1 | `--strict` mode AND any mismatch present (CI default as of Phase P31), OR default mode AND any STAMPED §00 has a mismatch (per-file strict promotion) |
| 2 | Structural error (spec root not found) |

## Output line shape

```
§00 ↔ §98 Version-field parity: scanned=87; eligible=74; matches=17; mismatches=57; skipped(no-banner)=5; skipped(no-release)=8; stamped=0; stamped_failed=0
  (info) spec/01-spec-authoring-guide: §00=3.7.0 vs §98 latest=4.13.0
  (FAIL) spec/22-git-logs-v2: §00=3.9.11 vs §98 latest=3.9.12 [stamped phase 200]
  …
```

The shape is asserted by self-test T1 (`scanned=` / `eligible=` /
`matches=` / `mismatches=` / `skipped(no-banner)=` / `skipped(no-release)=`
all present). Phase P20 added trailing `stamped=` / `stamped_failed=`
tokens AND the `(FAIL)` tag with optional `[stamped phase NNN]` suffix
for stamped-and-drifting modules. Future field additions MUST extend T1.

## Per-file opt-in stamp (Phase P20)

Once a module's `00-overview.md` banner has been brought back in lockstep
with its `98-changelog.md` latest release, authors MAY add a stamp inside
the first 40 lines of `00-overview.md`:

```markdown
<!-- h10-verified-phase: 200 -->
```

Effects (mirrors H1 / `check-99-summary-freshness.py`):

- The stamp itself does NOT prove the parity — the gate re-checks `bv == lr`
  every run. The stamp **promotes that file to per-file strict**: any future
  drift (e.g. someone bumps §98 without bumping §00) fails the gate even in
  default tree-wide-advisory mode.
- Multiple `<!-- h10-verified-phase: NNN -->` comments in one file → the
  highest phase number wins (defensive parsing for incremental bumps).
- Stamps under removable scopes (fenced code blocks, blockquotes) are
  **NOT** filtered today — keep stamps as plain top-of-file comments.
  If false positives appear, this gate will adopt the §99-freshness gate's
  block-stripping rules in a follow-up.
- `--report-only` overrides per-file stamp failures (escape hatch for
  dashboards / CI bisect).

This pattern lets adoption proceed PR-by-PR: each module that catches up
opts itself into strict enforcement individually, instead of waiting for
all 57 drifters to be fixed before flipping `--strict` tree-wide.

## Why the slot is 29

- Slots 20-29 are the validator/filler band on §99 / §97 / §98 lifecycle.
  §29 sits cleanly between `28-check-archive-exclusion-runtime` (validator)
  and the auditor band starting at §30.
- Slots 25–28 are occupied; 29 is the next free position in-band.
- **No slot-range exception needed** (mirrors slot 26's clean fit, unlike
  slots 18/19 in the 10-19 generator band per AC-T-22/AC-T-23).

## Why advisory-by-default at P15 — and strict-flip at P31 (AC-T-25 dispensation)

AC-T-25 (Phase 30) requires "advisory CI gates require explicit
phased-rollout justification or they ship strict from day 1." The
P15 dispensation, and its P31 retirement:

- **Surface size at P15 landing**: 59/74 mismatches. Flipping strict
  immediately would have blocked 59 unrelated PRs OR required a single
  sweep PR touching every module's §00 banner.
- **Phased-rollout execution**: contributors reconciled `§00 Version` ↔
  `§98 latest release` PR-by-PR through Phases P22→P30 (per-module
  forensic reconstructions + P29/P30 batched sweeps). At P30 close:
  matches=74/74, mismatches=0, stamped=57/74, stamped_failed=0 — the
  tree-wide invariant was achieved.
- **P31 strict-flip**: with the backlog cleared, the AC-T-25 dispensation
  no longer applies — `check-version-parity.py` runs in `--strict` mode
  by default and the gate becomes a hard CI block (exit 1 on any drift).
  Stamped count is no longer the gating factor; the remaining 17
  unstamped modules are matches-by-default and the strict gate locks
  them at parity going forward. Mirrors H1→H8 stamp adoption pattern
  (0/89 → 87/87 → strict; H8 locked the gain).
- **Visibility**: every CI run continues to print counts and per-module
  details in the workflow log; failures now block the merge instead of
  surfacing as advisory info lines.

## Acceptance criteria

### AC-29-01 — Mismatched §00↔§98 in default mode does not fail
- **Given** a module with `**Version:** 1.0.0` in `00-overview.md` and `## 2.0.0 — …` in `98-changelog.md`,
- **When** `check-version-parity.py` runs (default mode, no flags),
- **Then** the file MUST be reported as `(info) … §00=1.0.0 vs §98 latest=2.0.0` AND exit code MUST be 0.

### AC-29-02 — Matched §00↔§98 counts as match
- **Given** a module with `**Version:** 1.2.3` in `00-overview.md` and `## 1.2.3 — …` in `98-changelog.md`,
- **When** the gate runs,
- **Then** the file MUST contribute to `matches=N` AND MUST NOT appear in the `(info)` mismatch list.

### AC-29-03 — Strict mode exits 1 on mismatch
- **Given** at least one mismatch in scope,
- **When** the gate runs WITH `--strict` (and WITHOUT `--report-only`),
- **Then** exit code MUST be 1.

### AC-29-04 — `--report-only` overrides `--strict`
- **Given** any combination of mismatches,
- **When** the gate runs WITH both `--strict` and `--report-only`,
- **Then** exit code MUST be 0 with a `--report-only: not failing.` footer line.

### AC-29-05 — Module without §00 Version banner is skipped
- **Given** a module whose `00-overview.md` carries no `**Version:**` line in its first 40 lines,
- **When** the gate runs,
- **Then** the file MUST contribute to `skipped(no-banner)=N` AND MUST NOT appear under `eligible` or `mismatches`.

### AC-29-06 — Changelog without parseable release is skipped
- **Given** a module whose `98-changelog.md` matches none of the four accepted release shapes (heading / bracketed heading / `vX.Y.Z` heading / table-row),
- **When** the gate runs,
- **Then** the file MUST contribute to `skipped(no-release)=N` AND MUST NOT appear under `eligible` or `mismatches`.

### AC-29-07 — Table-row §98 format (folder 22 style) parsed
- **Given** a `98-changelog.md` whose latest release is `| 3.9.8 | 2026-04-28 | … |`,
- **When** the gate runs against a sibling `00-overview.md` with `**Version:** 3.9.8`,
- **Then** the file MUST contribute to `matches=N` (the table-row format is a first-class release shape).

### AC-29-08 — `spec/_archive/**` excluded from scan
- **Given** any `00-overview.md` under `spec/_archive/`,
- **When** the gate runs,
- **Then** the file MUST NOT contribute to any counter (scanned/eligible/skipped/mismatches) — archived modules are frozen by design.

### AC-29-09 — `--json` output schema
- **Given** the gate runs with `--json`,
- **When** the output is parsed,
- **Then** the JSON object MUST contain top-level keys `scanned`, `eligible`, `matches`, `mismatches`, `skipped_no_banner`, `skipped_no_release`, `stamped`, `stamped_failed`, `details` (array of `{module, banner, latest_release, stamped}` objects, where `stamped` is the integer phase number or `null`).

### AC-29-10 — Output line shape contract
- **Given** the gate runs in default text mode,
- **When** the first non-empty stdout line is inspected,
- **Then** it MUST contain all eight tokens: `scanned=`, `eligible=`, `matches=`, `mismatches=`, `skipped(no-banner)=`, `skipped(no-release)=`, `stamped=`, `stamped_failed=`. Self-test T1 enforces the original six; future field additions MUST extend T1 and bump this AC.

### AC-29-11 — Per-file stamp promotes mismatch to FAIL in default mode
- **Given** a module whose `00-overview.md` carries `**Version:** 1.0.0` AND a `<!-- h10-verified-phase: 200 -->` stamp inside the first 40 lines, AND whose `98-changelog.md` latest release is `1.0.1`,
- **When** the gate runs in default mode (no flags),
- **Then** exit code MUST be 1, the per-file line MUST be tagged `(FAIL)` with `[stamped phase 200]` suffix, and `stamped_failed=1` MUST appear in the summary line.

### AC-29-12 — Stamped + matched module counts as both stamped and match
- **Given** a stamped `00-overview.md` whose banner version equals the §98 latest release,
- **When** the gate runs,
- **Then** the file MUST contribute `+1` to `matches=` AND `+1` to `stamped=`, MUST contribute `0` to `stamped_failed=`, and the gate MUST exit 0.

### AC-29-13 — `--report-only` overrides per-file stamp failure
- **Given** a stamped §00 with a §00 ↔ §98 mismatch (would FAIL in default mode per AC-29-11),
- **When** the gate runs WITH `--report-only`,
- **Then** exit code MUST be 0 (`--report-only` is the strongest escape hatch — overrides both `--strict` and per-file stamps).

### AC-29-14 — CI workflow invokes `--strict` (Phase P31)
- **Given** the CI workflow `.github/workflows/spec-health.yml`,
- **When** the §00 ↔ §98 Version-field parity step is inspected,
- **Then** the invocation MUST be `python3 linter-scripts/check-version-parity.py --strict` (any mismatch fails the build). The script-level default remains advisory-by-default for local invocations and backward compatibility; the strict enforcement is encoded at the workflow layer per the P31 advisory→strict transition documented under "Why advisory-by-default at P15 — and strict-flip at P31".
- **Verifies:** §29 CI strict-flip contract.

### AC-29-15 — `latest_release()` returns SemVer-MAX, not positional-first (Phase 153 Task #35-fu)
- **Given** a `98-changelog.md` containing TWO release rows where row order does NOT equal SemVer order — e.g. `### 4.0.1 — 2026-04-29 — Phase 153 Task #29d` appears ABOVE `## 4.1.0 — 2026-04-27` (a patch reconciliation prepended above an older minor release),
- **When** `latest_release(text)` is called,
- **Then** the returned version MUST be `4.1.0` (the SemVer-maximum), NOT `4.0.1` (the positional-first). The comparator MUST parse each candidate as `(major, minor, patch)` integers and return the lexicographic max. Rationale: §00 banners track the SemVer maximum (which equals "highest semantic release shipped"), so the gate's comparator must match the same semantic — positional-first reads the wrong row whenever Phase 153–style patch reconciliation rows are prepended above older higher-minor releases. **Lesson #28 (Phase 153 Task #35)**: when a versioning gate flags wide drift (≥10 modules in a single class), inspect the gate's comparator BEFORE mass-patching the tree — the bug may be in the comparator, not the data.
- **Verifies:** §29 `latest_release()` SemVer-max comparator (`linter-scripts/check-version-parity.py:_semver_key` + `latest_release`).

### AC-29-16 — Blockquote release prose `> **vX.Y.Z` is a first-class release shape (Phase J3-fu / Lesson #28-fu)
- **Given** a `98-changelog.md` whose latest release is published only as a blockquote prose entry of shape `> **v3.22.0 update (Phase J15 — …):** …` (used by spec/22 and any module whose archive-pruned changelog leads with blockquote update prose above the table-row index), AND a sibling `00-overview.md` carrying `**Version:** 3.22.0`,
- **When** `latest_release(text)` is called,
- **Then** the returned version MUST be `3.22.0` (the blockquote shape MUST contribute to the release-version candidate set alongside `RELEASE_HEADING_RE` and `RELEASE_ROW_RE`), AND the file MUST contribute to `matches=N` (NOT to `skipped(no-release)=N`). The blockquote shape is anchored as `^>\s*\*\*v?(\d+\.\d+\.\d+)\b`. Rationale: when an archive prune moves all heading + table-row releases out of `98-changelog.md` and only the most recent update prose remains as a blockquote, the prior comparator silently saw "no release" and skipped the file, masking real §00↔§98 drift. **Lesson #28-fu (Phase J3)** reinforcement of Lesson #28: when the parity gate flags drift (or silently skips a known-shipped release), inspect both (a) the COMPARATOR semantics AND (b) the SCANNED-shape regex set BEFORE patching data.
- **Verifies:** §29 `RELEASE_BLOCKQUOTE_RE` + `latest_release()` blockquote-shape contribution (`linter-scripts/check-version-parity.py:RELEASE_BLOCKQUOTE_RE`).

## Self-test

`linter-scripts/test/test-check-version-parity.sh` exercises 15 assertions
(T1–T15) covering: banner shape, default vs strict exit codes,
`--report-only` override, sandboxed match/no-banner/no-release/table-row
modules, `--json` schema, `_archive/` exclusion, the Phase P20 per-file
stamp lifecycle (T11 stamped+drift fails default; T12 stamped+match
passes; T13 `--report-only` overrides stamp failure), the Phase 153
SemVer-max comparator (T14: SemVer-LOWER patch row prepended above
SemVer-HIGHER minor row → `matches=1`), and the Phase J3-fu blockquote
release shape (T15: `> **v2.0.0 update …` recognised, NOT skipped). Per
the H1 lesson on workflow-step parity, the self-test is **collapsed into
the gate's own workflow step** (no standalone self-test step) — the gate
runs the self-test first, then runs against the real tree. This
preserves AC-31-28 gate-count parity at 19/19/19. **Phase P31 update**:
T3 was rewritten to inject drift in a sandbox instead of relying on
real-tree mismatches (which dropped to 0 at P30 backlog clearance) —
codifies the lesson "self-tests asserting strict-mode failure paths
must own their own drift, not borrow from the real tree."

## Cross-references

- §24 [`24-check-lockstep.md`](./24-check-lockstep.md) — sibling lockstep
  gate that polices DATE relations (L1/L2/L3); H10 polices VERSION strings
  in the same §00 ↔ §98 surface but cannot reuse §24's machinery because
  date arithmetic is a different invariant from version-string equality.
- §26 [`26-check-99-summary-freshness.md`](./26-check-99-summary-freshness.md)
  — H1 lesson source: advisory-then-strict pattern + workflow-step
  collapse for self-tests + per-file `<!-- verified-phase: NNN -->` stamp
  precedent that Phase P20's `<!-- h10-verified-phase: NNN -->` mirrors.
- §27 [`27-check-99-stamp-bump.md`](./27-check-99-stamp-bump.md) — H4/H5
  sibling pattern (event-based stamp gate vs snapshot freshness gate).
- §97 `97-acceptance-criteria.md` — AC-T-26 codifies H10's CI integration
  + AC-T-25 dispensation rationale.
- Phase 21 retrospective (Phase 21 §27 §00-overview stale-prose sweep
  in `spec/27-spec-toolchain/98-changelog.md` row v2.46.3) — H10 origin.

## Slot-range note

Slot 29 is a clean fit in the 20-29 validator/filler band — no exception
needed (unlike slots 18/19 in the 10-19 generator band per AC-T-22/AC-T-23).
The next free slot in this band after H10 is 32 (slots 30/31 are auditors).

## Changelog

### 1.4.0 — 2026-05-07 — Phase J3-fu (Lesson #28-fu blockquote release shape)
- **Bug fix in `latest_release()`**: added `RELEASE_BLOCKQUOTE_RE = ^>\s*\*\*v?(\d+\.\d+\.\d+)\b` as a third release-shape regex alongside `RELEASE_HEADING_RE` and `RELEASE_ROW_RE`. `latest_release()` now scans heading + row + blockquote per line and returns SemVer-MAX of the unioned candidate set. Closes a silent skip class observed in spec/22 where archive prune (Phase fu29) moved all heading + table-row releases out of `98-changelog.md` and the most recent release shipped only as `> **v3.22.0 update (Phase J15 — …):** …` blockquote prose — the prior comparator scanned this file as `skipped(no-release)` even though §00 banner correctly tracked v3.22.0.
- **New AC**: AC-29-16 codifies the blockquote shape contract with the spec/22 worked example; AC count 15 → 16.
- **Self-test grew T15**: synthetic sandbox module ships only a blockquote release (`> **v2.0.0 update (Phase X — blockquote release):** …`) and a matching `**Version:** 2.0.0` banner; asserts `matches=1, mismatches=0` AND that the file does NOT enter `skipped(no-release)`. Self-test: **14/14 → 15/15** ✅.
- **Lesson #28-fu** (codified inside AC-29-16): when the parity gate flags drift OR silently skips a known-shipped release, inspect both (a) the COMPARATOR semantics AND (b) the SCANNED-shape regex set BEFORE patching data. Reinforcement of Lesson #28 — the Phase 153 #35 lesson covered comparator semantics; Phase J3-fu extends it to the regex-coverage axis.
- **No CI workflow change, no AC-31-31 cascade, no RUBRIC bump, no gate-count change** (gate #19 contract preserved; only the scanned-shape regex set was widened).

### 1.3.0 — 2026-04-29 — Phase 153 Task #35-fu (SemVer-max comparator)
- **Bug fix in `latest_release()`**: switched return semantics from positional-first to **SemVer-MAXIMUM**. Added `_semver_key(v)` helper that parses `X.Y.Z` into a comparable `(int, int, int)` tuple; `latest_release()` now collects ALL release rows and returns `max(versions, key=_semver_key)` instead of the first one matched. Closes 15 false-positive parity FAILs accumulated during Phase 153 Tasks #29c/d/e/#31 — those sub-tasks prepended SemVer-LOWER patch reconciliation rows above older SemVer-HIGHER minor releases (e.g. `### 4.0.1` above `## 4.1.0`), and the prior positional-first comparator returned `4.0.1` while §00 banners correctly tracked the SemVer max (`4.1.0` or `4.1.1`). SemVer is the source of truth, not row position.
- **New AC**: AC-29-15 codifies the SemVer-max contract with a worked example.
- **Self-test grew T14**: builds a §98 with a SemVer-LOWER row prepended above a SemVer-HIGHER row and asserts `matches=1, mismatches=0`. T2 + T9 also moved from real-tree to sandbox (real tree is now 74/74 stamped, so per-file strict promotion fires whenever any drift exists, breaking the "advisory exits 0" + "JSON parses cleanly" assertions). Self-test: **13/13 → 14/14** ✅.
- **Lesson #28** (codified inside AC-29-15): when a versioning gate flags wide drift, inspect the gate's COMPARATOR before mass-patching the tree.
- **No CI workflow change, no AC-31-31 cascade, no RUBRIC bump, no gate-count change** (gate #19 contract preserved; only the comparator was sharpened).

### 1.2.0 — 2026-04-28 — Phase P31 (CI strict-flip)
- **Workflow change**: `.github/workflows/spec-health.yml` step "§00 ↔ §98 Version-field parity gate" now invokes `python3 linter-scripts/check-version-parity.py --strict`. Any §00 ↔ §98 version drift now blocks the build (gate #19 is now a hard CI block; was advisory P15→P30).
- **Script unchanged**: `check-version-parity.py` keeps its advisory-by-default semantics for local/backward-compat invocations. The strict enforcement is encoded at the workflow layer (Option A — minimal blast radius). Self-test 13/13 unchanged.
- **Why now**: P30 cleared the reverse-drift backlog (74/74 matches, 0 mismatches, 57 stamped, 0 stamped_failed). The AC-T-25 dispensation that justified advisory-by-default no longer applies — the tree-wide invariant is locked.
- **AC-31-31 cascade**: `RUBRIC_VERSION` v2.28 → **v2.29** (rubric semantics tightened — gate #19 is now strict, not advisory). `00-index.md` footer 19 production gates **unchanged** (no new gate added; gate #19 contract tightened in place). `EXECUTIVE-SUMMARY.md` does not reference per-gate semantics. Slot 70's `00-overview.md` description "19 production gates" unchanged.
- **New AC**: AC-29-14 (CI workflow invocation contract).
- **No spec slot bump beyond minor** (1.1.0 → 1.2.0 — workflow contract change, not a new gate).

### 1.1.0 — 2026-04-28 — Phase P20
- Added per-file opt-in `<!-- h10-verified-phase: NNN -->` stamp pattern
  (mirrors H1 / `check-99-summary-freshness.py`).
- A stamped §00 with a §00 ↔ §98 mismatch now fails the gate even in
  default tree-wide-advisory mode (per-file strict promotion). Lets
  modules opt into strict enforcement one at a time without waiting for
  all 57 drifters to catch up.
- Output shape extended: trailing `stamped=` / `stamped_failed=` tokens
  on the summary line; per-file lines tagged `(FAIL)` with optional
  `[stamped phase NNN]` suffix when stamp present.
- `--json` schema extended: top-level `stamped` + `stamped_failed`
  counts; each `details[]` entry now carries a `stamped: <int|null>` field.
- `--report-only` remains the strongest escape hatch (overrides both
  `--strict` and per-file stamp failures).
- Self-test grew T11/T12/T13 (stamp lifecycle): 10/10 → **13/13** ✅.
- 3 new ACs: AC-29-11, AC-29-12, AC-29-13.
- Bug fix: `--spec-root` pointing outside the repo now degrades
  gracefully (was raising `ValueError` in `relative_to`); module path
  falls back to absolute when sandboxed.
- No CI workflow change: the gate stays advisory tree-wide; the new
  strict promotion is per-file and triggers only on stamps.

### 1.0.0 — 2026-04-28 — Phase P15 / H10
- Initial version. Advisory-by-default §00 ↔ §98 Version-field parity gate.
- Baseline sweep at landing: 87 scanned, 74 eligible, 15 matches, 59
  mismatches (the Phase 21 surface estimate of "1/3 historical incident,
  low surface" was a vast under-count — actual surface is 59/74 ≈ 80%).
- CI wired into `.github/workflows/spec-health.yml` after the §99
  freshness gate (gate #19); runs in default advisory mode (exits 0).
- Self-test 10/10 ✅.
- AC-31-31 cascade: gate count 18 → **19**; `RUBRIC_VERSION` v2.27 → **v2.28**.
