# Slot 47 — `check-ac-section-orphan-header.py`

**Status:** Active gate #28 (Phase-5 T-21)
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
2. **No empty `## ` parent sections** — every `## ` section
   header in a §97 file MUST contain at least one `### AC-…`
   child header before the next `## ` section (or EOF). An
   empty `## ` section is a stale split-point left over from
   AC migration and fails clause-2 — Lesson #36 link-don't-restate
   forbids retaining empty pedagogical scaffolding once it has
   no live referents.
3. **Every AC carries a status tag** — every `### AC-…` header
   MUST end with one of the literal trailing tokens `` `[active]` ``,
   `` `[deferred]` ``, or `` `[archived]` `` (backticked, with the
   exact lowercase spelling). A status-less AC header is paper-only
   and cannot route through the §27 gate-15 D7-self-enforcement
   discipline (which keys on the status tag for its qualifier-strip
   contract). Fails clause-3 with the offending AC-ID + line.
4. **AC-ID uniqueness within a file** — within a single §97 file,
   every `### AC-…` AC-ID (everything between `### ` and the first
   ` —` or ` ` or `  `) MUST be unique. Duplicates mask later ACs
   from walker enumeration (the duplicate row wins at parse time)
   and fail clause-4. Cross-file duplicate AC-IDs are out-of-scope
   for this gate (covered by gate #14 `ac-prefix-contract-check`
   when shipped at slot 48).
5. **No duplicate `## ` section names within a file** — within a
   single §97 file, every `## ` section heading title MUST be
   unique. Duplicate sections fragment AC ownership and silently
   break the §00 Walker-Pin block's "section X of N" counter.
   Fails clause-5 with the offending section title + both line
   numbers.

## Invocation

```bash
python3 linter-scripts/check-ac-section-orphan-header.py --check all
python3 linter-scripts/check-ac-section-orphan-header.py --check no-orphan-ac
python3 linter-scripts/check-ac-section-orphan-header.py --check no-empty-section
python3 linter-scripts/check-ac-section-orphan-header.py --check status-tag-present
python3 linter-scripts/check-ac-section-orphan-header.py --check ac-id-uniqueness
python3 linter-scripts/check-ac-section-orphan-header.py --check section-name-uniqueness
python3 linter-scripts/check-ac-section-orphan-header.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

A scanner that returns 0 because zero §97 files were discovered, or
because zero `### AC-…` headers were parsed in the seven in-scope
folders, is **itself a violation** (exit `1`, message
`vacuous-pass: zero §97 files or zero AC headers parsed`). The
`--self-test` mode is mandatory in CI and asserts the scanner
correctly REJECTS six synthetic fixtures:

- **F-1** complete-uniform (every AC under a `## ` parent, every
  parent has ≥1 child, every AC carries `[active]`, all AC-IDs
  unique, all `## ` titles unique) → passes
- **F-2** orphan AC declared before any `## ` parent → fails
  (clause-1)
- **F-3** `## ` parent with zero `### AC-…` children before EOF
  → fails (clause-2)
- **F-4** `### AC-99` with no trailing `[active]/[deferred]/[archived]`
  status tag → fails (clause-3)
- **F-5** duplicate `### AC-04` within the same file → fails
  (clause-4)
- **F-6** duplicate `## Mutations` parent section within the same
  file → fails (clause-5)

## 5-link self-enforcement chain

1. **AC text** — every §97 file's structural surface (no per-AC
   line cite — the gate enforces the file-wide invariant set
   declared by this slot doc).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (6 short Markdown blobs reproducing the §97
   header geometry).
3. **Script** — `linter-scripts/check-ac-section-orphan-header.py`
   (this slot).
4. **`--self-test`** — built-in mode, runs 6 fixtures (F-1 unique
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
  clause-1 + clause-2 + clause-5 are the file-shape preconditions
  the walker relies on. Before T-21, walker correctness was a
  paper-only invariant; T-21 makes it load-proven.
- **§27 gate #15 D7-self-enforcement** (`derives-from-restate-check`) —
  clause-3's status-tag presence is the load-bearing token gate
  #15 keys on for its qualifier-strip lockstep. Before T-21, a
  malformed status tag bypassed gate #15 silently; T-21 closes
  that escape hatch.
- **Lesson #36 link-don't-restate** — clause-2 (no empty parents)
  is the §97 surface application of the cross-cutting Lesson #36
  rule against retained pedagogical scaffolding.

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
