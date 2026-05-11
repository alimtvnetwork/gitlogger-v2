# Slot 53 — `check-appshell-route-matrix.py`

**Status:** Active gate #31 (Phase-5 T-24)
**Implements:** §24 §00 `### AppShell Route Matrix (Normative — Phase-5 T-09)` (line 263) + variant→behaviour binding table (line 283) + invariants 1-4 (line 290) + §24 §97 AC-ADS-UI-04 (line 303) (closes §27 backlog `appshell-route-matrix-check` minted T-09)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§24 AppShell route matrix gate"

## Contract

Walks the §24 §00 AppShell Route Matrix (AS-NN rows) and the
variant→behaviour binding table and asserts route↔variant↔shell
parity. Closes the §27 backlog `appshell-route-matrix-check` ticket
(oldest open §24 backlog ticket, minted Phase-5 T-09). Fails CI when
ANY of the following invariants fail:

1. **AS-NN matrix presence + shape** — `spec/24-app-design-system-and-ui/00-overview.md`
   MUST contain exactly one table headed
   `| ID | Route prefix | AppShellVariant | Auth-gated? | Notes |`
   (AS-NN matrix). The table MUST carry ≥8 `AS-NN` rows (current
   contract: AS-01..AS-08). AS-IDs MUST be globally unique within
   the file and contiguous from AS-01. A missing matrix or a gap
   (e.g. AS-01, AS-02, AS-04) fails clause-1.
2. **Variant enum closed-set discipline** — every `AppShellVariant`
   value in column 3 MUST be one of the closed set
   `{Marketing, Console, Settings, Modal}` OR the literal sentinel
   `(none — no shell)` (reserved for `/api/*` server-only rows).
   A free-form value like `Dashboard` or `Auth` fails clause-2 —
   the variant enum is the §24 file-line 511 surface and cannot
   drift unilaterally without §24 §00 invariant-4 paired update.
3. **Variant→behaviour binding table parity** — `00-overview.md`
   MUST contain the second table headed
   `| Variant | AppToolbar | AppSidebar | AppCanvas padding | Used by |`
   immediately after the AS-NN matrix. Every non-sentinel variant
   value observed in clause-2 MUST appear as a `Variant` column row
   here, and the `Used by` column MUST cite at least one AS-NN ID
   that uses it. An orphan binding row (variant with zero AS-NN
   citations) OR an orphan AS-NN (variant present in matrix but
   missing from binding table) fails clause-3. (Bidirectional
   coverage; mirror of slot 49 clause-1↔clause-2.)
4. **Marketing↔AC-ADS-06 transitive boundary** — every AS-NN row
   whose `AppShellVariant` is `Marketing` MUST carry the literal
   `MUST NOT import` substring in its `Notes` column AND cite
   `AC-ADS-06`. This binds invariant-2 (`Marketing`-variant routes
   MUST NOT import from `src/components/app/**`) at the matrix
   surface so a row author cannot weaken the boundary by editing
   only the matrix without invalidating AC-ADS-06. Sibling to
   gate #19 (`ads-boundaries-check`) which enforces the same rule
   on the runtime AST side.
5. **Invariant-1/2/4 normative literal presence** — the four
   `Invariants (binding):` paragraphs immediately following the
   binding table MUST contain ALL of: `single source of truth`,
   `appshell-route-matrix-check` (this gate, self-citation),
   `MUST NOT import from \`src/components/app/**\``,
   `--app-toolbar-height`, and the literal `5th variant`. Stripping
   any literal collapses the invariant block to subjective prose
   and fails clause-5. (This clause IS the slot 53 self-citation —
   removing the gate name from §24 §00 also fails this gate, per
   Lesson #15 self-enforcement.)
6. **AC-ADS-UI-04 surface presence + cite chain** — §24 §97 MUST
   contain `### AC-ADS-UI-04` AND its body MUST cite all of
   `AppShell route matrix`, `8-row AS-NN matrix`, the literal
   `4-row variant→behaviour binding table`, AND `parity-locked`.
   Removing AC-ADS-UI-04 OR weakening any of these literals fails
   clause-6. AC-ADS-UI-04 status tag MUST be `[active]` per gate
   #28 contract.

## Invocation

```bash
python3 linter-scripts/check-appshell-route-matrix.py --check all
python3 linter-scripts/check-appshell-route-matrix.py --check matrix-shape
python3 linter-scripts/check-appshell-route-matrix.py --check variant-enum
python3 linter-scripts/check-appshell-route-matrix.py --check binding-parity
python3 linter-scripts/check-appshell-route-matrix.py --check marketing-boundary
python3 linter-scripts/check-appshell-route-matrix.py --check invariant-literals
python3 linter-scripts/check-appshell-route-matrix.py --check ac-ads-ui-04-surface
python3 linter-scripts/check-appshell-route-matrix.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if the AS-NN matrix has ≥8 rows, the binding
table has ≥4 variant rows, AND AC-ADS-UI-04 was located in §24
§97 with all four required literals. Zero anchors → exit `1` with
`vacuous-pass: AS-NN matrix < 8 rows / binding table < 4 rows /
AC-ADS-UI-04 surface absent`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-uniform (8 AS-NN rows, 4 binding rows, full
  invariant block, AC-ADS-UI-04 with all literals) → passes
- **F-2** AS-NN matrix gaps AS-03 (rows AS-01, AS-02, AS-04..AS-08)
  → fails clause-1
- **F-3** AS-04 variant set to `Dashboard` (free-form) → fails
  clause-2
- **F-4** binding table omits the `Settings` row even though
  AS-06 still uses it → fails clause-3
- **F-5** AS-01 variant `Marketing` notes column drops the
  `MUST NOT import` literal → fails clause-4
- **F-6** §24 §97 AC-ADS-UI-04 body drops the literal
  `parity-locked` → fails clause-6

## 5-link self-enforcement chain

1. **AC text** — §24 §00 lines 263 (matrix header), 270 (matrix),
   283 (binding table), 290 (invariants); §24 §97 AC-ADS-UI-04
   (line 303).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (6 short Markdown blobs reproducing AS-NN matrix
   + binding table + AC-ADS-UI-04 geometry).
3. **Script** — `linter-scripts/check-appshell-route-matrix.py`.
4. **`--self-test`** — built-in mode, runs 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§24 AppShell route matrix gate" hard-fails CI.
6. **§00 Walker-Pin row** — §24 §00 Walker-Pin block gains a row
   citing slot 53 + gate #31 + workflow step name (deferred to
   next §24 §00 touch).

## Bindings

- **§27 backlog ticket `appshell-route-matrix-check`** — closes
  this turn (T-24). Oldest §24-side backlog ticket, minted Phase-5
  T-09 alongside the AS-NN matrix itself; the matrix has been
  paper-only for 15 cycles. Conversion to load-proven via this
  gate.
- **AC-ADS-UI-04** (AppShell route matrix present and parity-locked)
  — clauses 1/3/6 mechanise the structural presence; gate IS the
  cited mechanism. Promotes AC-ADS-UI-04 from conditional 20 to
  un-conditional 20 (last AC-ADS-UI-* family member to convert).
- **AC-ADS-06** (marketing routes MUST NOT import `AppShell`) —
  clause-4 binds the matrix-surface citation; sibling to gate #19
  which covers the runtime AST side. Together they form a
  spec-side + code-side parity pair.
- **§24 §00 invariant-4** (5th variant requires paired binding
  table row) — clause-2 + clause-3 enforce the variant↔binding
  parity that invariant-4 declares; adding a 5th variant without
  the paired row fails clause-3 immediately.
- **Lesson #15 self-enforcement** — clause-5 cites the gate name
  inside the very prose it validates; stripping the citation
  breaks the gate, breaking the strip.

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-53/`) and run `python3 linter-scripts/check-appshell-route-matrix.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #31 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/check-appshell-route-matrix.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #31 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## Scorecard impact (Rubric v2 /120)
- **§24** — C3 (Testability) +1 (AppShell matrix now mechanised);
  C5 (Implementability) +1 (AS-NN ↔ variant ↔ shell binding
  self-enforcing via this gate; cite mechanism is gate #31 itself);
  C6 (Friction) +1 (last §24-backlog ticket closed, route-matrix
  navigation now first-class). §24 reaches the 120/120 ceiling
  for Lovable+Cursor personas (audit baseline 119/119); Raw-LLM
  +1 (114 → 115).
- **§27** — C6 (Friction) +1 (one more backlog ticket closed;
  oldest §24-side backlog ticket retired).

## Out of scope

- Runtime route existence (whether `src/routes/apps.tsx` actually
  exists) — covered by future P9 boundary scanner; this gate
  enforces only the SPEC-SIDE matrix shape.
- AppShell component implementation (whether `AppShell.tsx` renders
  the right toolbar+sidebar combination) — covered by gate #19
  (`ads-boundaries-check`) and would require AST scan; out-of-scope
  for this static gate.
- Auth-gating policy correctness (whether `/resolve` is the right
  surface for `svc/admin`) — security policy, not matrix shape.
- Adding/removing AS-NN rows — content decision; gate enforces
  shape and parity, not row inventory beyond the ≥8 floor.
