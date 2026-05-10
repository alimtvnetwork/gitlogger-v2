# Slot 43 — `check-boolean-uniformity-primary-lane.py`

**Status:** Active gate #24 (Phase-5 T-17)
**Implements:** §23 §00 R-4 invariant 2 (PRIMARY-lane SQLite `INTEGER` 0/1 + `Is`-prefix discipline) + §22 `17-openapi.yaml` `type: boolean` field set (lines 85, 101, 103, 273, 286) + §24 §00 U-3 boolean rendering parity (line 359) + cross-cutting **AC-CAF-01** (T-12 — wire-boolean parity end-to-end DB ↔ REST ↔ UI)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§22+§23+§24 boolean uniformity gate"

## Contract

Promotes AC-CAF-01 from conditional (paper-only at T-12 landing; partial
`IsActive` coverage via gate #22) to **load-proven** end-to-end. Walks the
three boolean anchors and fails CI when ANY of the following uniformity
invariants fail:

1. **DB primary-lane (R-4 invariant 2)** — every `CREATE TABLE …` block
   in §23 §00 (and the §22 `18-schema.sql` mirror) MUST declare
   boolean-shaped columns as `INTEGER NOT NULL` (or `INTEGER NULL` only
   when paired with a coupled invariant CHECK like AppLink's
   `IsActive=0 ⇒ DisconnectedAt NOT NULL`) AND the column name MUST
   begin with `Is` (e.g. `IsActive`, `IsDeprecated`). Bare `BOOLEAN`,
   `TINYINT`, or non-`Is`-prefixed flag columns are rejected.
2. **REST wire-shape (§22 OpenAPI)** — every `type: boolean` field in
   §22 `17-openapi.yaml` MUST have a property name that either matches
   `^(Is|Has|Was|Can|Should|Truncated|HasError|Deprecated)…$` (the
   approved adjectival/predicate prefix set) AND MUST NOT be
   accompanied by an `enum: [0,1]` or `oneOf: [0,1]` integer-coercion
   construct. The wire shape is JSON `true`/`false` only — never
   `0`/`1` after the DB → REST translation.
3. **UI render-side parity (§24 U-3)** — §24 §00 line 359 MUST carry
   the U-3 rule binding `IsActive: true → "Active" + --app-status-active`
   and `IsActive: false → "Inactive" + --app-status-inactive` AND the
   forbidden-pattern clause MUST list "MUST NOT render raw `0`/`1`
   integers" + "MUST NOT invert the boolean" + an explicit token-leak
   prohibition. Removing or weakening any of those three sub-clauses
   fails this gate.
4. **No coercion-attack surface** — every §23 R-1 endpoint matrix row
   that accepts a boolean field MUST cite §23 R-4 invariant 2 in its
   422 rejection clause (WE-3 fixture is the canonical example:
   `IsActive: 1` integer body → 422 `field.invalid` not silent
   coercion to `true`). REST handlers that silently coerce
   `1`/`"true"`/`"yes"` are rejected at the contract layer.
5. **No restate-drift** — neither §22 nor §24 may inline a parallel
   "boolean encoding table" redefining the DB ↔ wire ↔ UI translation;
   both MUST cite §23 R-4 invariant 2 as the single source per
   Lesson #36. §24 U-3 is a render-side parity rule, not a translation
   redefinition — it MUST remain ≤ 8 lines and MUST cite §23 R-4 by
   name.

## Invocation

```bash
python3 linter-scripts/check-boolean-uniformity-primary-lane.py --check all
python3 linter-scripts/check-boolean-uniformity-primary-lane.py --check db-primary-lane
python3 linter-scripts/check-boolean-uniformity-primary-lane.py --check rest-wire-shape
python3 linter-scripts/check-boolean-uniformity-primary-lane.py --check ui-render-parity
python3 linter-scripts/check-boolean-uniformity-primary-lane.py --check no-coercion
python3 linter-scripts/check-boolean-uniformity-primary-lane.py --check no-restate
python3 linter-scripts/check-boolean-uniformity-primary-lane.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3`
fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

A scanner that returns 0 because the boolean-column regex matched zero
DDL columns is **itself a violation** (exit `1`, message
`vacuous-pass: zero boolean-shaped columns found in §23 §00 or §22 18-schema.sql`).
The `--self-test` mode is mandatory in CI and asserts that the scanner
correctly REJECTS six synthetic fixtures:

- **F-1** complete-uniform (DB `IsActive INTEGER NOT NULL` with
  AppLink-style coupled CHECK, REST `IsActive: { type: boolean }`,
  §24 U-3 with all three forbidden sub-clauses, R-1 matrix cites
  R-4 inv-2 in 422 clause, no parallel encoding table) → passes
- **F-2** §23 declares `IsActive BOOLEAN NOT NULL` (wrong type) →
  fails (clause-1)
- **F-3** §23 declares `Active INTEGER NOT NULL` (missing `Is`
  prefix) → fails (clause-1)
- **F-4** §22 OpenAPI `Active: { type: boolean, enum: [0,1] }`
  (integer-coercion construct) → fails (clause-2)
- **F-5** §24 U-3 drops the "MUST NOT invert" sub-clause → fails
  (clause-3)
- **F-6** §22 inlines a parallel "Boolean encoding" table redefining
  DB ↔ wire translation → fails (clause-5)

## 5-link self-enforcement chain (A-44 template)

1. **AC text** — §23 §00 R-4 invariant 2 + R-1 matrix 422 clauses + §22
   `17-openapi.yaml` boolean field set (lines 85, 101, 103, 273, 286) +
   §24 §00 line 359 U-3 + AC-CAF-01 (canonical cross-cutting clause).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (6 short SQL + YAML + Markdown blobs).
3. **Script** — `linter-scripts/check-boolean-uniformity-primary-lane.py`
   (this slot).
4. **`--self-test`** — built-in mode, runs 6 fixtures (F-1 unique
   passing fixture).
5. **Workflow step** — `.github/workflows/spec-health.yml` "§22+§23+§24
   boolean uniformity gate" hard-fails CI on any violation.
6. **§00 Walker-Pin row** — §22 + §23 + §24 `00-overview.md`
   Walker-Pin blocks each gain a row citing this slot + gate #24 +
   workflow step name (deferred to next §00 touch on each folder;
   in-spec catalogue holds until then).

## Bindings

- **AC-CAF-01** (T-12) — converts from conditional 20 (paper-only;
  3-turn decay clause; partial `IsActive`-only coverage via gate #22)
  to un-conditional 20 (load-proven end-to-end DB ↔ REST ↔ UI). This
  gate IS the cited self-enforcing mechanism.
- **§23 §00 WE-3** (T-11) — clause 4 mechanizes the WE-3 boolean-
  coercion-attack fixture; the gate guarantees every boolean-accepting
  R-1 endpoint cites R-4 inv-2 in its 422 clause.
- **Gate #22 `applink-xor-clause-check`** — partial `IsActive` coverage
  via the disconnect-CHECK; gate #24 is the **superset** that adds REST
  + UI sides + the `Is`-prefix + no-coercion + no-restate clauses.
  Gate #22 remains the load-proof for AppLink's specific coupled-CHECK
  shape; gate #24 is the cross-folder uniformity layer above it.
- **§24 U-3** — gate IS the machine-checked sibling that AC-ADS U-3
  has cited as "implementation pending" since §24 v?.

## Out of scope

- Localised UI labels (e.g. "Active" → "活躍" i18n) — §24 i18n concern,
  not boolean uniformity.
- BOOLEAN columns in non-PRIMARY lanes (e.g. PostgreSQL `BOOLEAN`
  in REFERENCE-lane PostgreSQL ports) — §23 dialect-precedence-banner
  governs lane selection; this gate fires only on the PRIMARY lane.
- Tri-state (`true` / `false` / `null`) semantics — out of AC-CAF-01
  scope; nullable booleans require an explicit coupled CHECK per
  clause-1.

## History

- **Phase-5 T-17** — slot created. Built-in self-test only (no on-disk
  fixture corpus needed; the six fixtures are short SQL + YAML +
  Markdown strings exercising `re` + `yaml.safe_load` predicates
  against synthetic blobs). Mirrors slot-42 T-16 cross-folder
  uniformity convention. Closes §27 backlog entry
  `boolean-uniformity-primary-lane-check` minted Sess-43. Promotes
  AC-CAF-01 from conditional to un-conditional self-enforcing —
  second cross-cutting CAF gate after T-16 gate #23 (CAF-02).
