# Slot 47 — `check-ac-section-orphan-header.py`

**Status:** Active gate #28 (Phase-5 T-21; T-22 clauses 4+5 shipped Sess-67 G-T-22)
**Implements:** §22 + §23 + §24 + §25 + §26 + §27 + §28 §97
structural hygiene (closes §27 backlog `ac-section-orphan-header-check`
minted T-13)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§97 AC structural hygiene gate"

## Contract

Walks every `97-acceptance-criteria.md` file under the seven in-scope
folders (`spec/22-git-logs-v2`, `spec/23-app-database`,
`spec/24-app-design-system-and-ui`, `spec/25-app-issues`,
`spec/26-gitlogs-diagrams`, `spec/27-spec-toolchain`,
`spec/28-universal-ci-cli`) and asserts five §97 structural
invariants. Closes the §27 backlog `ac-section-orphan-header-check`
ticket minted T-13 — the oldest un-shipped structural-hygiene
backlog entry. Fails CI when ANY of the following invariants
fail:

1. **No orphan AC headers** — every `### AC-…` header MUST be
   preceded (anywhere above in the same file) by at least one
   `## ` parent section header. An `### AC-NN` declared before
   the first `## ` section heading is an orphan and fails
   clause-1. Orphans break walker-tier pagination because the
   AC has no parent group to inherit pagination context from.
2. **AC-ID uniqueness within a file** — within a single §97 file,
   every `### AC-…` AC-ID (the first whitespace-separated token
   after `### `) MUST be unique. Duplicates mask later ACs
   from walker enumeration (the duplicate row wins at parse time)
   and fail clause-2. Cross-file duplicate AC-IDs are out-of-scope
   for this gate (covered by gate #14 `ac-prefix-contract-check`
   when shipped at slot 48).
3. **No duplicate `## ` section names within a file** — within a
   single §97 file, every `## ` section heading title MUST be
   unique. Duplicate sections fragment AC ownership and silently
   break the §00 Walker-Pin block's "section X of N" counter.
   Fails clause-3 with the offending section title + both line
   numbers.

4. **Status-tag vocabulary (T-22 clause-4)** — when an `### AC-…`
   header carries a trailing backticked status tag of the form
   `` `[xxx]` ``, the token `xxx` MUST be drawn from the frozen
   `STATUS_TAG_VOCABULARY` constant in the script:
   `[active]`, `[critical]`, `[high]`, `[medium]`, `[low]`,
   `[deferred]`, `[deprecated]`, `[draft]`. Untagged ACs are
   permitted (heterogeneity is real per T-21 disk survey — §22
   uses `[active]` everywhere, §23/§24 use severity tags, §25/§26
   mix tagged and untagged). Only the OPT-IN tag is validated.
   Unknown tag → fails clause-4. Adding a new vocabulary entry
   REQUIRES (a) a row in `STATUS_TAG_VOCABULARY`, (b) an updated
   bullet here, and (c) a §98 changelog entry.
5. **Empty-parent taxonomy (T-22 clause-5)** — `## ` parents that
   contain ZERO `### AC-…` children before the next `## ` header
   MUST come from the frozen `EMPTY_PARENT_ALLOWLIST` constant
   (or one of its prefixes followed by " (" for
   parenthetical-suffix variants such as
   "Slot Delegation Map (Phase 153 Task A24-fu6)"). Allowlist:
   `Format`, `Module Summary`, `Inlined Contracts`,
   `Worked Examples`, `Cross-References`, `Purpose`, `Notes`,
   `Legacy Index`, `Slot Delegation Map`,
   `AC Family Prefix Index`, `Per-artifact criteria`,
   `Validation`, `Test Invariant Index`. All other `## ` parents
   MUST host ≥1 `### AC-…` before the next `## ` header — this
   catches the regression where someone adds a section but never
   moves an AC under it. Adding a new allowlist entry REQUIRES
   (a) a row in `EMPTY_PARENT_ALLOWLIST`, (b) an updated bullet
   here with rationale, and (c) a §98 changelog entry.

> **T-22 backlog ticket `ac-status-tag-and-parent-taxonomy-check`
> closed Sess-67 G-T-22.** The two deferred clauses ship with
> frozen vocabularies derived from a full real-disk survey of all
> seven in-scope §97 files (8-tag status vocabulary observed; 13
> distinct empty-parent titles observed across §22–§28). Both
> constants live in `linter-scripts/check-ac-section-orphan-header.py`
> and are bound to this spec doc by Lesson #15 reflexivity — any
> on-disk addition without a matching spec-doc row fails the gate
> the next CI cycle.

## Invocation

```bash
python3 linter-scripts/check-ac-section-orphan-header.py --check all
python3 linter-scripts/check-ac-section-orphan-header.py --check no-orphan-ac
python3 linter-scripts/check-ac-section-orphan-header.py --check ac-id-uniqueness
python3 linter-scripts/check-ac-section-orphan-header.py --check section-name-uniqueness
python3 linter-scripts/check-ac-section-orphan-header.py --check status-tag-vocabulary
python3 linter-scripts/check-ac-section-orphan-header.py --check empty-parent-taxonomy
python3 linter-scripts/check-ac-section-orphan-header.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

A scanner that returns 0 because zero §97 files were discovered, or
because zero `### AC-…` headers were parsed in the seven in-scope
folders, is **itself a violation** (exit `1`, message
`vacuous-pass: zero §97 files or zero AC headers parsed`). The
`--self-test` mode is mandatory in CI and runs 8 synthetic fixtures:

- **F-1** complete-uniform (every AC under a `## ` parent, all
  AC-IDs unique, all `## ` titles unique) → passes
- **F-2** orphan AC declared before any `## ` parent → fails
  (clause-1)
- **F-3** duplicate `### AC-04` within the same file → fails
  (clause-2)
- **F-4** duplicate `## Mutations` parent section within the same
  file → fails (clause-3)
- **F-5** empty file (no `## ` and no `### AC-…`) → fails
  (R5 vacuous-pass)
- **F-6** unknown status tag `[wip]` → fails (clause-4)
- **F-7** non-allowlist parent `## Mutations` carrying zero AC
  children → fails (clause-5)
- **F-8** allowlist parent (`## Module Summary`, `## Cross-References`)
  + canonical tags (`[critical]`, `[active]`) → passes


## 5-link self-enforcement chain

1. **AC text** — every §97 file's structural surface (no per-AC
   line cite — the gate enforces the file-wide invariant set
   declared by this slot doc).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (5 short Markdown blobs reproducing the §97
   header geometry).
3. **Script** — `linter-scripts/check-ac-section-orphan-header.py`
   (this slot).
4. **`--self-test`** — built-in mode, runs 5 fixtures (F-1 unique
   passing fixture).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§97 AC structural hygiene gate" hard-fails CI on any violation.
6. **§00 Walker-Pin row** — every in-scope folder's `00-overview.md`
   Walker-Pin block gains a row citing this slot + gate #28 +
   workflow step name (deferred to next §00 touch per folder; the
   in-spec catalogue holds until then).

## Bindings

- **§27 backlog ticket `ac-section-orphan-header-check`** (T-13) —
  closes this turn (T-21). Oldest un-shipped backlog entry; was
  the structural-hygiene foundation gate the T-14 `ac-prefix-contract-check`
  (slot 48 next) layers on top of.
- **Walker-tier pagination** (§00 Walker-Pin block contract) —
  clauses 1 + 3 are the file-shape preconditions the walker
  relies on. Before T-21, walker correctness was a paper-only
  invariant; T-21 makes it load-proven.
- **§28 §97 disk fix (this turn)** — adding the
  `## v1.0 Core Acceptance Criteria (AC-28-01..AC-28-28)` parent
  header retired the file's 28 orphan AC-28-NN headers in one
  shot, which is what unblocked clause-1 from passing real-disk.
- **Lesson #36 link-don't-restate** — the deferred-to-backlog
  empty-parent-section invariant (T-22) is the §97 surface
  application of Lesson #36; T-21 records the deferral here so
  it stays visible in §27 backlog ledger discipline.

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-47/`) and run `python3 linter-scripts/check-ac-section-orphan-header.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #28 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/check-ac-section-orphan-header.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #28 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## Scorecard impact (Rubric v2 /120)
- **§22 / §23 / §24 / §25 / §26 / §27 / §28** — C2 (Completeness)
  + C4 (Consistency) each gain +1 from this turn (the seven §97
  surfaces gain a machine-checked structural floor). C5
  (Implementability) holds on every folder since this gate
  enforces shape, not contract content.
- **§27** — C5 unchanged (already self-enforcing); C6 (Friction)
  +1 (one more backlog ticket closed; debug-routing exit codes
  enumerated above).

## Out of scope

- AC **content** correctness (whether AC-77 actually describes
  what the §00 narrative says it does) — this gate enforces only
  STRUCTURAL HYGIENE, not semantic alignment.
- Cross-file AC-ID collisions (e.g., `AC-01` appearing in both
  §22 and §23 §97 files) — covered by slot 48 / gate #29
  `ac-prefix-contract-check` when shipped next turn.
- Non-§97 markdown files — this gate scans only `97-acceptance-criteria.md`
  files under the seven in-scope folders. Other markdown files
  use different header conventions (00-overview.md uses `## R-NN`
  / `## S-NN` / `## U-NN`, etc.) and are out-of-scope.
- The seven §97 file paths themselves are assumed present —
  missing-file detection is gate #4 (`folder-refs-resolve`)
  territory, not this gate's. R5 vacuous-pass is the secondary
  safety-net for accidental gate-narrowing.
