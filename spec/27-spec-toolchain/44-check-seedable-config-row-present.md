# Slot 44 — `check-seedable-config-row-present.py`

**Status:** Active gate #25 (Phase-5 T-18)
**Implements:** §24 §00 `## Settings Surface (Normative — Phase-5 T-08)` S-1 (5-row route matrix, line 407) + S-2 (7-row persistence matrix, line 417) + S-3 (4-invariant seedable-config binding, line 434) + §24 §97 AC-ADS-UI-03 (line 461) + cross-cutting **AC-CAF-04** (T-12 — seed-row/override separation extends seedable-config to App-layer)
**Self-test:** built-in (`--self-test`) against 5 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§24 seedable-config row gate"

## Contract

Promotes AC-CAF-04 from conditional (paper-only at T-12 landing; 3-turn
decay clause shared with CAF-01/02/03) to **load-proven** end-to-end.
Walks the §24 Settings Surface anchors and fails CI when ANY of the
following separation invariants fail:

1. **S-1 ↔ S-2 endpoint coverage** — every route row in §24 §00 S-1
   (S-01..S-05, line 411..415) MUST cite at least one R-NN endpoint
   from the S-2 matrix (R-09..R-15, line 421..427) in its `Endpoint(s)`
   column, AND every R-NN row in S-2 MUST be cited by at least one
   S-1 row. Orphan endpoints (declared but not bound to a panel) and
   orphan panels (declared but not bound to an endpoint) both fail.
2. **Seed-row presence (S-3 invariant 1)** — every PATCH endpoint in
   S-2 (R-10, R-12, R-14) MUST cite the `Setting` table by name in
   its row notes OR the surrounding S-3 prose MUST list the seed-row
   key it mutates. The row note `partial body; never overwrites seed row`
   on R-10 is the byte-for-byte canonical form and MUST appear verbatim;
   weakening the clause (e.g. dropping `never overwrites seed row`)
   fails this gate.
3. **Override-table separation (S-3 invariant 2)** — S-3 invariant 2
   MUST contain the literal string `UserSettingOverride` AND the literal
   `INSERT … ON CONFLICT(UserId,Key) DO UPDATE` clause AND the literal
   `MUST NOT mutate the seed row`. All three sub-clauses are required;
   removing any one fails the gate (the invariant collapses to a single
   point of mutation if any is missing — collapsing the override-table
   to the seed table is the exact failure mode AC-CAF-04 prohibits).
4. **R-09 merged-view contract (S-3 invariant 3)** — the R-09 row note
   MUST contain `merged seed + per-user override` AND S-3 invariant 3
   MUST express the merge as `COALESCE(override.Value, seed.Value)`
   (not `COALESCE(seed, override)` — order matters; inverting it
   silently overrides user choice with the default and is itself a
   CAF-04 violation pattern).
5. **Forward-only removal (S-3 invariant 4 + §23 Rule 12 cite)** — S-3
   invariant 4 MUST cite `§23 Rule 12` by name AND MUST require
   removal of BOTH the seed row AND user overrides in the SAME
   migration. Splitting the removal into two migrations is rejected
   (creates a window where overrides reference a non-existent seed
   key — orphan-override class).
6. **No restate-drift** — neither §23 nor §22 may inline a parallel
   "settings persistence" matrix redefining the merge order, override-
   table name, or seed-row immutability. S-1/S-2/S-3 are §24-owned
   per AC-CAF-04 declaring AC; §23 owns the underlying `Setting` +
   `UserSettingOverride` DDL only (cited from S-5 line 456 as the
   T-08 follow-up materialisation ticket). Inline restate is itself a
   gate #15 `derives-from-restate-check` violation at meta-level.

## Invocation

```bash
python3 linter-scripts/check-seedable-config-row-present.py --check all
python3 linter-scripts/check-seedable-config-row-present.py --check s1-s2-coverage
python3 linter-scripts/check-seedable-config-row-present.py --check seed-row-presence
python3 linter-scripts/check-seedable-config-row-present.py --check override-table-separation
python3 linter-scripts/check-seedable-config-row-present.py --check r09-merged-view
python3 linter-scripts/check-seedable-config-row-present.py --check forward-only-removal
python3 linter-scripts/check-seedable-config-row-present.py --check no-restate
python3 linter-scripts/check-seedable-config-row-present.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

A scanner that returns 0 because the S-1 / S-2 / S-3 markdown headers
matched zero rows or zero invariants is **itself a violation** (exit
`1`, message `vacuous-pass: zero S-1/S-2/S-3 anchors found in §24 §00`).
The `--self-test` mode is mandatory in CI and asserts that the scanner
correctly REJECTS five synthetic fixtures:

- **F-1** complete-uniform (S-1 5-row matrix, S-2 7-row matrix, S-3
  4 invariants with all required literals, AC-ADS-UI-03 present,
  no parallel restate in §22 or §23) → passes
- **F-2** S-2 declares R-12 with note `partial body` (drops
  `never overwrites seed row` sub-clause) → fails (clause-2)
- **F-3** S-3 invariant 2 omits the literal `UserSettingOverride`
  (collapses override into seed table) → fails (clause-3)
- **F-4** S-3 invariant 3 expresses merge as
  `COALESCE(seed.Value, override.Value)` (inverted COALESCE order
  — overrides silently lose to defaults) → fails (clause-4)
- **F-5** §23 §00 inlines a parallel "Settings persistence" matrix
  redefining the merge order → fails (clause-6)
- **F-6** R5 vacuous-pass — no S-1/S-2/S-3 matrix found in §23 §00 →
  fails as `vacuous-pass: empty walk → exit 3 fixture-rot` rather than
  silently passing on absence.

## 5-link self-enforcement chain (A-44 template)

1. **AC text** — §24 §00 S-1 (line 407) + S-2 (line 417) + S-3 (line
   434) + §24 §97 AC-ADS-UI-03 (line 461) + AC-CAF-04 (canonical
   cross-cutting clause, §24 §97 line 251).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (5 short Markdown blobs reproducing the S-1/S-2/S-3
   anchor geometry).
3. **Script** — `linter-scripts/check-seedable-config-row-present.py`
   (this slot).
4. **`--self-test`** — built-in mode, runs 5 fixtures (F-1 unique
   passing fixture).
5. **Workflow step** — `.github/workflows/spec-health.yml` "§24
   seedable-config row gate" hard-fails CI on any violation.
6. **§00 Walker-Pin row** — §24 `00-overview.md` Walker-Pin block
   gains a row citing this slot + gate #25 + workflow step name
   (deferred to next §24 §00 touch; in-spec catalogue holds until then).

## Bindings

- **AC-CAF-04** (T-12) — converts from conditional 20 (paper-only;
  3-turn decay clause shared with CAF-01/02/03/05) to un-conditional
  20 (load-proven). This gate IS the cited self-enforcing mechanism.
- **AC-ADS-UI-03** (§24 §97 line 461) — gate IS the machine-checked
  sibling that AC-ADS-UI-03 has cited as `seedable-config-row-present-check`
  (NEW backlog from T-08) since §24 §00 S-5 line 459.
- **§23 §00 Rule 12** (forward-only migrations) — clause 5 mechanizes
  the cross-folder cite; the gate guarantees S-3 invariant 4 cannot
  drift to a two-migration removal pattern.
- **§24 §00 S-5 line 456** — the `Setting` + `UserSettingOverride`
  DDL materialisation in §23 remains the OUT-OF-SCOPE follow-up; this
  gate enforces the §24-side surface contract independently of §23
  DDL landing (separation of concerns: §24 owns the surface, §23
  owns the storage).

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-44/`) and run `python3 linter-scripts/check-seedable-config-row-present.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #25 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/check-seedable-config-row-present.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #25 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## Out of scope

- Actual `Setting` + `UserSettingOverride` DDL — owned by §23 (S-5
  line 456 follow-up). This gate fires on §24 surface contract drift
  only; §23 DDL drift is covered by the existing §27 gate family
  (`check-applink-xor-clause` shape; new §23 DDL gate to be specced
  when the table lands).
- Settings export/import format — deferred per S-5 line 458; out of
  AC-CAF-04 scope.
- Auth role definitions on the S-1 `Role gate` column (`user`/`admin`/`svc`
  literals) — S-5 line 457 marks role definitions out-of-locked-7-scope;
  this gate accepts the literals as opaque tokens.

## History

- **Phase-5 T-18** — slot created. Built-in self-test only (no on-disk
  fixture corpus needed; the five fixtures are short Markdown blobs
  exercising `re` predicates against synthetic anchor geometry).
  Mirrors slot-43 T-17 cross-folder uniformity convention. Closes §27
  backlog entry `seedable-config-row-present-check` minted T-08.
  Promotes AC-CAF-04 from conditional to un-conditional self-enforcing
  — third cross-cutting CAF gate after T-16 gate #23 (CAF-02) and T-17
  gate #24 (CAF-01).
