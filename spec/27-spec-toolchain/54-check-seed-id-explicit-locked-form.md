# Slot 54 — `check-seed-id-explicit-locked-form.py`

**Status:** Active gate #32 (Phase-5 T-25)
**Implements:** §23 §00 `### Seed data (lookup tables) — locked-ID parity (AC-ADB-13, T-10 remediation)` (line 199) + PRIMARY lane fence (line 207-214) + REFERENCE lane fence (line 217-223) + Seed-ID parity matrix (line 225) + Forbidden seed shapes block (line 235) + §23 §97 AC-ADB-13 + AC-ADB-11 (closes §27 backlog `seed-id-explicit-locked-form-check` minted T-10)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§23 seed-ID explicit locked-form gate"

## Contract

Walks the §23 §00 seed-data section and asserts every conformant
seed shape carries explicit primary-key literals, the parity matrix
row-set matches both DDL fences, and the forbidden-shape block
remains present and verbatim. Closes the §27 backlog
`seed-id-explicit-locked-form-check` ticket (minted T-10 alongside
the locked-ID remediation itself; paper-only for 13 cycles). Fails
CI when ANY of the following invariants fail:

1. **PRIMARY-lane explicit-PK presence** — the SQLite fence
   following `**PRIMARY lane (SQLite — MATERIALISE):**` MUST
   contain BOTH:
   - `INSERT OR IGNORE INTO AppStatus  (AppStatusId, Name) VALUES (1,'Active'),(2,'Disabled'),(3,'Archived')`
   - `INSERT OR IGNORE INTO AppLinkType(AppLinkTypeId, Name) VALUES (1,'GitProfile'),(2,'Repo')`

   Both literals are matched modulo single ASCII whitespace runs
   (so column-alignment is preserved). Any drop of the explicit
   `AppStatusId` / `AppLinkTypeId` column, any change to the
   ID-tuple order `(1,…),(2,…),(3,…)`, or any rename of the locked
   names fails clause-1. The literal IDs `1`, `2`, `3` for
   `AppStatus` and `1`, `2` for `AppLinkType` are the
   AC-ADB-13 contract — they are LOCKED.
2. **REFERENCE-lane parity-pinned form** — the PostgreSQL fence
   following `**REFERENCE lane (PostgreSQL — DO NOT MATERIALISE; shown for parity audit only):**`
   MUST contain BOTH:
   - `INSERT INTO app_status   (app_status_id, name) VALUES (1,'Active'),(2,'Disabled'),(3,'Archived')` followed within 2 lines by `ON CONFLICT (app_status_id) DO NOTHING`
   - `INSERT INTO app_link_type(app_link_type_id, name) VALUES (1,'GitProfile'),(2,'Repo')` followed within 2 lines by `ON CONFLICT (app_link_type_id) DO NOTHING`

   Same locked-ID literals MUST appear (1/2/3 for app_status,
   1/2 for app_link_type) AND the conflict-target column MUST
   be the explicit PK column name (NOT a bare `DO NOTHING` —
   omitting the conflict target silently degrades to row-level
   conflict resolution and breaks parity with the PRIMARY-lane
   `INSERT OR IGNORE` semantics).
3. **Parity-matrix row coverage** — the `Seed-ID parity matrix
   (binding):` table MUST carry exactly 5 data rows in this fixed
   order: `AppLinkType`/`1`/`GitProfile`, `AppLinkType`/`2`/`Repo`,
   `AppStatus`/`1`/`Active`, `AppStatus`/`2`/`Disabled`,
   `AppStatus`/`3`/`Archived`. The (Lookup table, Locked ID,
   Locked Name) triple set MUST be a subset-superset match
   against the literal tuples extracted from clause-1 + clause-2
   fences (bidirectional coverage — every fence row appears in
   the matrix; every matrix row appears in both fences). An
   asymmetric row (matrix lists `AppStatus`/`4`/`Pending` not
   in the fences, or fences emit a 6th row not in the matrix)
   fails clause-3.
4. **Forbidden-shape block presence + literal pinning** — the
   `**Forbidden seed shapes (binding — emit any of these and the
   CHECK constraint silently de-anchors):**` block MUST be present
   and MUST contain ALL of:
   - the literal `INSERT OR IGNORE INTO AppLinkType(Name) VALUES ('GitProfile'),('Repo')` (forbidden shape #1 — implicit-rowid form)
   - the literal `silently de-anchors` (the load-bearing semantic)
   - the literal `IDs are the contract` (the AC-ADB-13 normative phrase)
   - 3 numbered items (❌ / ⚠ / ❌ status icons present in that order)

   Stripping any literal collapses the forbidden block to
   subjective prose and fails clause-4 — the forbidden-shape
   list IS the negative-fixture corpus the PRIMARY-lane
   regression test keys on.
5. **Locked-ID parity cite chain** — every of the following
   anchor literals MUST appear in §23 §00 within the seed-data
   section span (lines following the `### Seed data` heading
   up to the next `### ` or `---` boundary):
   `AC-ADB-13`, `AC-ADB-11`, `T-10 remediation`, `MATERIALISE`,
   `DO NOT MATERIALISE`, `XOR target invariant`, `Discriminator`,
   `Q1`. Removing the cite chain breaks the §97↔§00 binding for
   AC-ADB-13 and fails clause-5. (Sibling to gate #22 clause-2
   which enforces the AppLink CHECK clause depends on these IDs.)
6. **No restate of locked-ID seed in §22 / §24 / §25** — no
   other `.md` file under `spec/22-git-logs-v2/`,
   `spec/24-app-design-system-and-ui/`, or `spec/25-app-issues/`
   may contain a fenced SQL block including the literal
   `INSERT … VALUES (1,'GitProfile'),(2,'Repo')` (matched as
   regex `INSERT[^;]*VALUES\s*\(\s*1\s*,\s*'GitProfile'\s*\)`).
   Mentions inside backticks/blockquote/inline-prose are
   allowed (per gate #27 evidence-marker contract); only fenced
   ` ```sql ` blocks are forbidden. A duplicate fence is a
   Lesson #36 link-don't-restate violation and fails clause-6
   with the offending file:line.

## Invocation

```bash
python3 linter-scripts/check-seed-id-explicit-locked-form.py --check all
python3 linter-scripts/check-seed-id-explicit-locked-form.py --check primary-lane-explicit-pk
python3 linter-scripts/check-seed-id-explicit-locked-form.py --check reference-lane-parity
python3 linter-scripts/check-seed-id-explicit-locked-form.py --check parity-matrix-coverage
python3 linter-scripts/check-seed-id-explicit-locked-form.py --check forbidden-block-literals
python3 linter-scripts/check-seed-id-explicit-locked-form.py --check locked-id-cite-chain
python3 linter-scripts/check-seed-id-explicit-locked-form.py --check no-restate
python3 linter-scripts/check-seed-id-explicit-locked-form.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if the seed-data section was located in §23 §00
AND both DDL fences contained ≥1 `INSERT` statement matching the
locked-ID regex AND the parity matrix carried ≥5 data rows AND
the forbidden-shape block carried ≥3 numbered items. Zero anchors
→ exit `1` with `vacuous-pass: §23 seed-data section absent /
PRIMARY fence empty / REFERENCE fence empty / parity matrix < 5
rows / forbidden block < 3 items`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-uniform (both fences carry locked-ID explicit
  PK; parity matrix has all 5 rows; forbidden block has 3 items
  with all literals; cite chain present; no §22/§24/§25 restate)
  → passes
- **F-2** PRIMARY fence drops `AppLinkTypeId` column from the
  AppLinkType `INSERT` (implicit-rowid form) → fails clause-1
- **F-3** REFERENCE fence drops `ON CONFLICT (app_link_type_id)`
  conflict target → fails clause-2
- **F-4** parity matrix omits the `AppStatus`/`3`/`Archived` row
  even though both fences emit `(3,'Archived')` → fails clause-3
  (asymmetric coverage)
- **F-5** forbidden-shape block drops the literal
  `silently de-anchors` → fails clause-4
- **F-6** §22 child file `02-database-schema.md` includes a
  fenced `` ```sql `` block with
  `INSERT INTO AppLinkType … VALUES (1,'GitProfile'),(2,'Repo')`
  → fails clause-6 (Lesson #36 restate)

## 5-link self-enforcement chain

1. **AC text** — §23 §00 line 199 (seed-data heading), 207-214
   (PRIMARY fence), 217-223 (REFERENCE fence), 225 (parity matrix),
   235 (forbidden block); §23 §97 AC-ADB-13, AC-ADB-11; §27
   backlog `seed-id-explicit-locked-form-check` (T-10).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (6 short Markdown blobs reproducing seed-data
   section, parity matrix, forbidden block, and §22/§24/§25
   sibling-restate geometry).
3. **Script** — `linter-scripts/check-seed-id-explicit-locked-form.py`.
4. **`--self-test`** — built-in mode, runs 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§23 seed-ID explicit locked-form gate" hard-fails CI.
6. **§00 Walker-Pin row** — §23 §00 Walker-Pin block gains a row
   citing slot 54 + gate #32 + workflow step name (deferred to
   next §23 §00 touch).

## Bindings

- **§27 backlog ticket `seed-id-explicit-locked-form-check`** —
  closes this turn (T-25). Minted T-10 alongside the AC-ADB-13
  locked-ID remediation; paper-only for 13 cycles. Conversion
  to load-proven via this gate.
- **AC-ADB-13** (locked-ID seed parity) — clauses 1/2/3 mechanise
  the explicit-PK seed shape across both lanes; gate IS the cited
  mechanism. Promotes AC-ADB-13 from conditional 20 to
  un-conditional 20.
- **AC-ADB-11** (boolean policy + dialect precedence) — clause-5
  cite-chain enforces the dialect-precedence anchor literals
  (`MATERIALISE` / `DO NOT MATERIALISE`) the AC-ADB-11 dialect-pin
  contract depends on; sibling to forthcoming
  `dialect-precedence-banner-present` gate.
- **AC-ADB-05** (XOR target invariant) — clause-5 cite chain
  binds the AC-ADB-05↔AC-ADB-13 dependency: the AppLink CHECK
  clause depends on the locked literal IDs `1`/`2`. Sibling to
  gate #22 (`check-applink-xor-clause`) which validates the
  CHECK clause itself.
- **Lesson #36 link-don't-restate** — clause-6 is the §22+§24+§25
  surface application of the cross-cutting Lesson #36 rule;
  prevents the seed-shape from being silently duplicated into a
  consumer folder where it could drift.
- **Gate #15 D7-self-enforcement** — clause-4 forbidden-block
  literal pinning extends D7 to the negative-fixture corpus
  (the forbidden block is itself a normative anti-pattern list,
  not subjective prose).

## Scorecard impact (Rubric v2 /120)

- **§23** — C3 (Testability) +2 (locked-ID seed shape now
  mechanised across both lanes; parity matrix and forbidden
  block load-proven); C5 (Implementability) +1 (seed-form
  ambiguity resolved — cite mechanism is gate #32); C4
  (Consistency) +1 (clause-3 bidirectional coverage closes the
  matrix↔fence drift vector). §23 advances toward 19-20
  self-enforcing band (Lovable 116 → 119, Cursor 112 → 116,
  Raw-LLM 106 → 110).
- **§22 / §24 / §25** — C4 (Consistency) +1 each (clause-6
  no-restate surface pulls the locked-ID seed contract into the
  cross-folder negative-coverage net).
- **§27** — C6 (Friction) +1 (one more backlog ticket closed;
  oldest §23-side backlog ticket retired).

## Out of scope

- Runtime seed application (whether `migrate.py` actually emits
  the conformant `INSERT`) — covered by future runtime-fixture
  gate; this gate enforces only the SPEC-SIDE seed shape.
- AppLink CHECK clause syntax (whether the XOR pattern matches
  the locked IDs) — covered by gate #22 (`check-applink-xor-clause`).
- Boolean encoding policy (whether `IsActive` uses INTEGER vs
  boolean) — covered by gate #24 (`check-boolean-uniformity-primary-lane`).
- AppStatus state-transition graph (whether 1→2→3 transitions
  are valid) — application-layer policy, not seed shape.
- Adding/removing locked-ID rows — content decision; gate
  enforces shape and parity, not row inventory beyond the 5-row
  floor (3× AppStatus + 2× AppLinkType).
