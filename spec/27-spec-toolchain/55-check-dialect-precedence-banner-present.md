# Slot 55 — `check-dialect-precedence-banner-present.py`

**Status:** Active gate #33 (Phase-5 T-26)
**Implements:** §23 §00 `## Implementation Target Precedence (Normative — read before any DDL block)` (line 94) + dialect lane table (line 99-101) + cross-cuts pin block (line 103-106) + AI-walker contract (line 108) + every `**PRIMARY lane …**` / `**REFERENCE lane …**` machine-restate marker in §23 children + §22 §00 line 129 single-dialect declaration + §23 §97 AC-ADB-11 (closes §27 backlog `dialect-precedence-banner-present` minted T-08)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§22+§23 dialect-precedence banner gate"

## Contract

Walks every `.md` under `spec/22-git-logs-v2/` and
`spec/23-app-database/` and asserts the dialect-precedence banner
contract: (a) §23 §00 ships the precedence pin BEFORE any DDL fence,
(b) every dialect-bearing section header machine-restates the lane
marker, (c) §22 declares its single-dialect lane explicitly, (d) no
unlabelled DDL fence exists in either folder. Closes the §27 backlog
`dialect-precedence-banner-present` ticket (minted T-08; paper-only
for 14 cycles). Fails CI when ANY of the following invariants fail:

1. **§23 §00 precedence-banner presence + position** — §23 §00 MUST
   contain the literal heading
   `## Implementation Target Precedence (Normative — read before any DDL block)`
   AND the heading MUST appear on a line BEFORE the first SQL fence
   (` ```sql ` or ` ```sqlite `) in the file. A precedence pin
   that follows a DDL fence fails clause-1 — the load-bearing
   "BEFORE either DDL block" semantic is positional and a
   reordering silently invalidates the AI-walker contract.
2. **Lane table closed-set discipline** — the dialect lane table
   immediately following the heading MUST contain exactly 2 data
   rows with `Lane` column values `**PRIMARY**` and `**REFERENCE**`
   (in that order). PRIMARY row MUST cite `SQLite` AND
   `PascalCase` AND `INTEGER` AND `ACTIVE` AND `✅ YES` (Materialise
   column). REFERENCE row MUST cite `PostgreSQL` AND `snake_case`
   AND `boolean` AND `REFERENCE ONLY` AND `❌ NO` AND
   `silent dialect-flip is FORBIDDEN`. Adding a 3rd lane, dropping
   either lane, or weakening any literal fails clause-2.
3. **Cross-cuts pin literal presence** — the bulleted cross-cuts
   block immediately following the lane table MUST contain ALL
   of: `Boolean policy (AC-ADB-11`, `Timestamp parity (AC-ADB-16)`,
   `Seed ID parity (AC-ADB-13)`, the literal
   `Any code emitting \`boolean\` on the App database is a violation`,
   the literal `EXTRACT(EPOCH FROM …)::bigint`, AND the literal
   `INSERT … VALUES (1,'GitProfile'),(2,'Repo')`. The cross-cuts
   block IS the 1-section-read guarantee that the AI-walker
   contract relies on; stripping any literal collapses it to
   subjective prose and fails clause-3.
4. **AI-walker contract literal** — the precedence section MUST
   contain the literal sentence-fragments
   `partial-context violation` AND `re-anchor` AND
   `§00 Quick-Nav guarantees this pin is reached on a TOC walk`.
   Removing the AI-walker contract paragraph fails clause-4 —
   this is the load-bearing instruction that turns the banner
   into a re-entry pin for context-bounded readers.
5. **Machine-restate at every dialect-bearing section header
   in §23** — every `.md` under `spec/23-app-database/` MUST
   satisfy: any ` ```sql ` or ` ```sqlite ` fence MUST be
   preceded within the prior 30 lines (same section) by ONE of
   the following lane markers (matched as a complete bold-line):
   - `**PRIMARY lane (SQLite — MATERIALISE):**`
   - `**REFERENCE lane (PostgreSQL — DO NOT MATERIALISE; shown for parity audit only):**`
   - the prose marker `### 🚫 REFERENCE-ONLY` (header form)
   - the inline blockquote marker `> **⚠️ Reference / Secondary dialect (per AC-ADB-11).**`

   An unlabelled SQL fence (no marker within 30 lines preceding)
   fails clause-5 with the offending file:line. Fences inside
   `_archive/` subdirectories are exempt (read-only history).
6. **§22 single-dialect declaration** — `spec/22-git-logs-v2/00-overview.md`
   MUST contain a row in the Decisions Matrix declaring the database
   engine. Specifically the file MUST contain the literal substring
   `Database engine` followed within 5 lines by `SQLite` (the
   §22 v2 contract is single-dialect SQLite per Decisions Matrix
   row 1 / line 129). Removing the declaration or introducing a
   second dialect without paired AC fails clause-6. (§22 does NOT
   need the §23-style 2-lane precedence banner because it has only
   one lane — but the single-lane declaration is the
   precedence-pin-equivalent and MUST be machine-checkable.)

## Invocation

```bash
python3 linter-scripts/check-dialect-precedence-banner-present.py --check all
python3 linter-scripts/check-dialect-precedence-banner-present.py --check banner-position
python3 linter-scripts/check-dialect-precedence-banner-present.py --check lane-table-literals
python3 linter-scripts/check-dialect-precedence-banner-present.py --check cross-cuts-literals
python3 linter-scripts/check-dialect-precedence-banner-present.py --check ai-walker-contract
python3 linter-scripts/check-dialect-precedence-banner-present.py --check fence-restate-markers
python3 linter-scripts/check-dialect-precedence-banner-present.py --check spec22-single-dialect
python3 linter-scripts/check-dialect-precedence-banner-present.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if the §23 §00 precedence section was located,
the lane table carried exactly 2 rows, the cross-cuts block
carried ≥3 bulleted items, ≥1 dialect-bearing fence was scanned
across the §23 walk, AND the §22 single-dialect declaration row
was located. Zero anchors → exit `1` with `vacuous-pass: §23 §00
precedence section absent / lane table row count ≠ 2 / cross-cuts
block < 3 items / zero SQL fences scanned in §23 / §22 §00
Database-engine row absent`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-uniform (precedence banner present at top of §23
  §00; lane table has both rows with all literals; cross-cuts block
  has all 6 literals; AI-walker contract paragraph present; every
  §23 SQL fence preceded by a lane marker; §22 §00 declares SQLite)
  → passes
- **F-2** §23 §00 precedence heading appears AFTER the first SQL
  fence (positional reorder) → fails clause-1
- **F-3** lane table REFERENCE row drops literal
  `silent dialect-flip is FORBIDDEN` → fails clause-2
- **F-4** cross-cuts block omits the
  `EXTRACT(EPOCH FROM …)::bigint` literal → fails clause-3
- **F-5** §23 child file `02-queries.md` includes a bare
  ` ```sql ` fence with NO lane marker in the prior 30 lines
  → fails clause-5
- **F-6** §22 §00 Decisions Matrix row 1 sets
  `Database engine` → `MariaDB` (no `SQLite` literal within 5
  lines) → fails clause-6

## 5-link self-enforcement chain

1. **AC text** — §23 §00 line 94 (precedence heading), 96 (single
   source of truth blockquote), 99-101 (lane table), 104-106
   (cross-cuts pin), 108 (AI-walker contract); §23 §97 AC-ADB-11
   (dialect precedence + boolean policy); §22 §00 line 129
   (Database engine declaration); §27 backlog
   `dialect-precedence-banner-present` (T-08).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (6 short Markdown blobs reproducing precedence
   banner, lane table, cross-cuts block, AI-walker contract,
   dialect-bearing fences, and §22 single-dialect row geometry).
3. **Script** — `linter-scripts/check-dialect-precedence-banner-present.py`.
4. **`--self-test`** — built-in mode, runs 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§22+§23 dialect-precedence banner gate" hard-fails CI.
6. **§00 Walker-Pin row** — §23 §00 Walker-Pin block gains a row
   citing slot 55 + gate #33 + workflow step name (deferred to
   next §23 §00 touch).

## Bindings

- **§27 backlog ticket `dialect-precedence-banner-present`** —
  closes this turn (T-26). Minted Phase-5 T-08 alongside the
  AC-ADB-11 dialect-precedence remediation; paper-only for 14
  cycles. Conversion to load-proven via this gate.
- **AC-ADB-11** (boolean policy + dialect precedence) — clauses
  1/2/3/4 mechanise the precedence banner; gate IS the cited
  mechanism. Promotes AC-ADB-11 from conditional 20 to
  un-conditional 20.
- **Slot 54 / Gate #32** (`check-seed-id-explicit-locked-form`)
  — clause-3 Seed ID parity literal mirrors slot 54 clause-5
  cite chain; together they form the dialect-banner ↔ seed-shape
  parity pair. Slot 54 clause-5 cited `MATERIALISE` and
  `DO NOT MATERIALISE`; slot 55 clause-5 enforces those literals
  exist as fence markers, not just prose mentions.
- **AC-ADB-16** (timestamp parity) — clause-3 timestamp literal
  ensures the timestamp-cross-cut survives prose drift.
- **§22 single-dialect contract** (Decisions Matrix row 1) —
  clause-6 binds the §22 SQLite-only declaration to the same
  gate, so cross-folder dialect drift (e.g. §22 silently adopting
  PostgreSQL) becomes a CI failure.
- **AI-walker contract / Lesson #55+#61** — clause-4 enforces
  the partial-context-violation re-anchor instruction; the
  precedence pin IS the load-bearing context-recovery surface
  for bundle-bounded auditors.

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-55/`) and run `python3 linter-scripts/check-dialect-precedence-banner-present.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #33 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/check-dialect-precedence-banner-present.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #33 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## Scorecard impact (Rubric v2 /120)
- **§23** — C1 (Clarity) +1 (precedence banner now load-proven —
  no silent reorder); C3 (Testability) +1 (lane markers and
  cross-cuts mechanised); C5 (Implementability) +1 (dialect
  precedence un-ambiguous — cite mechanism is gate #33); C6
  (Friction) +1 (AI-walker contract enforced — re-entry pin
  guaranteed). §23 advances toward 120/120 ceiling (Lovable
  119 → 120, Cursor 116 → 117, Raw-LLM 110 → 112).
- **§22** — C4 (Consistency) +1 (single-dialect declaration
  load-proven via clause-6).
- **§27** — C6 (Friction) +1 (one more backlog ticket closed;
  another paper-only-since-T-08 ticket retired).

## Out of scope

- DDL syntax correctness (whether the SQLite or PostgreSQL fence
  parses) — covered by future SQL-parser gate; this gate enforces
  only the LANE MARKER discipline.
- Dialect implementation choice (whether SQLite is the right
  PRIMARY lane) — design decision pinned in AC-ADB-11; this
  gate enforces the BANNER, not the choice.
- Boolean policy enforcement (whether `IsActive` uses INTEGER vs
  boolean) — covered by gate #24 (`check-boolean-uniformity-primary-lane`).
- Seed shape enforcement (whether the locked-ID INSERT carries
  explicit PKs) — covered by gate #32 (slot 54).
- §24/§25/§26/§27/§28 dialect declaration — those folders do
  not own DDL surfaces; clause-5/clause-6 walks are scoped to
  §22+§23 only.
