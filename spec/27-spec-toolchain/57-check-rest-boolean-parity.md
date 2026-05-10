# Slot 57 — `check-rest-boolean-parity.py`

**Status:** Active gate #35 (Phase-5 T-28)
**Implements:** §23 §00 `## REST / RPC Contract` (line 361) R-2 JSON schemas (line 384) + R-4 invariant 2 boolean parity (line 441) + §23 §97 AC-ADB-REST-01 + AC-ADB-11 (boolean policy) + §22 `17-openapi.yaml` boolean field set (lines 85, 101, 103, 273, 286) + §24 §00 U-3 boolean render parity (closes §27 backlog `rest-boolean-parity-check` minted Phase-5 T-06; final REST-side backlog ticket)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§23 REST boolean parity gate"

## Contract

Walks `spec/23-app-database/00-overview.md` R-2 JSON sample fences,
R-4 invariant 2, and §22 `17-openapi.yaml` boolean field declarations,
and asserts the wire-side boolean lane is bijectively parity-pinned
to the DB-side INTEGER 0/1 lane (gate #24) and the UI-side boolean
render lane (§24 U-3). Materialises the 3-surface boolean parity
triple (DB / wire / UI) cited cross-referentially by gates #24 +
#34. Final REST-side §27 backlog ticket. Fails CI when ANY of the
following invariants fail:

1. **Wire boolean sample value discipline** — every JSON value in
   any ` ```jsonc ` / ` ```json ` fence inside the §23 §00 REST
   section that is the literal `true` or `false` MUST appear on a
   key matching `^Is[A-Z][A-Za-z0-9]*$`. Conversely, no key
   matching that regex may carry a non-boolean sample value (e.g.
   string `"yes"`, integer `1`, integer `0`). Mismatch fails
   clause-1 with offending key + line.
2. **R-4 invariant 2 literal preservation** — §23 §00 R-4
   invariant 2 (line 441) MUST contain literals
   `wire \`true\`/\`false\` ↔ DB \`1\`/\`0\``,
   `Never accept \`0\`/\`1\` integers in request bodies`, AND
   `reject with 422 \`field.invalid\``, AND the Lesson #15
   self-citation `Self-enforcing via §27 backlog gate
   \`rest-boolean-parity-check\``. Stripping any literal or
   the gate self-citation fails clause-2 (reflexivity break).
3. **OpenAPI ↔ wire bijection** — every field in
   `spec/22-git-logs-v2/17-openapi.yaml` declared `type: boolean`
   MUST have an `Is`-prefixed name (App surface) OR be explicitly
   whitelisted in the §22 git-logs-only set
   `{HasError, Truncated}` (legacy git-logs surface, not App —
   matches `spec/22-git-logs-v2/17-openapi.yaml` lines 85, 101,
   103, 273, 286). For the App surface (§23) every R-2 boolean key
   MUST round-trip via OpenAPI `type: boolean` with no `format:` coercion.
4. **No integer-coercion attack surface** — no R-2 fence may
   declare a boolean field with sample values `0` or `1`; no
   OpenAPI App-surface field may declare `type: integer` with
   `enum: [0, 1]` as a stand-in for boolean. Coercion patterns
   open a parsing-ambiguity attack surface and fail clause-4.
5. **§24 U-3 surface presence** — `spec/24-app-design-system-and-ui/00-overview.md`
   line ~359 MUST contain the U-3 boolean render parity sub-clause
   with literals `boolean` AND `true`/`false` AND `IsActive`
   (canonical example) AND a back-reference to either AC-ADB-11
   or AC-CAF-01. Stripping U-3 collapses the UI side of the
   triple and fails clause-5.
6. **No-restate in §22/§24/§25** — no `.md` under §22 (excluding
   `17-openapi.yaml` git-logs source), §24 (excluding the U-3
   binding row), or §25 may carry a parallel boolean encoding
   table for App-surface fields. Single source of truth for the
   App boolean lane is §23 §00 R-4 invariant 2 + AC-ADB-11
   (Lesson #36).

## Invocation

```bash
python3 linter-scripts/check-rest-boolean-parity.py --check all
python3 linter-scripts/check-rest-boolean-parity.py --check wire-sample-shape
python3 linter-scripts/check-rest-boolean-parity.py --check r4-invariant-literals
python3 linter-scripts/check-rest-boolean-parity.py --check openapi-bijection
python3 linter-scripts/check-rest-boolean-parity.py --check no-integer-coercion
python3 linter-scripts/check-rest-boolean-parity.py --check u3-surface-presence
python3 linter-scripts/check-rest-boolean-parity.py --check no-restate
python3 linter-scripts/check-rest-boolean-parity.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if the §23 §00 REST section was located, ≥1 R-2
JSON fence parsed, ≥1 boolean sample value observed, R-4 invariant
2 located, ≥1 OpenAPI `type: boolean` field parsed, AND §24 U-3
surface located. Zero anchors → exit `1` with `vacuous-pass`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-uniform (R-2 fences carry `IsActive: true` /
  `IsActive: false` only on `Is`-prefixed keys; R-4 invariant 2
  carries all literals + gate self-citation; OpenAPI fields are
  `type: boolean` with `Is`-prefix; §24 U-3 present) → passes
- **F-2** R-2 `App` fence ships `Active: true` (boolean on
  non-`Is` key) → fails clause-1
- **F-3** R-4 invariant 2 stripped of gate self-citation
  `rest-boolean-parity-check` → fails clause-2
- **F-4** OpenAPI declares `IsActive: type: integer, enum: [0,1]`
  (integer-coercion stand-in) → fails clause-4
- **F-5** §24 §00 U-3 sub-clause stripped of `IsActive` literal
  → fails clause-5
- **F-6** §25 child introduces parallel boolean encoding table
  for App-surface fields → fails clause-6

## 5-link self-enforcement chain

1. **AC text** — §23 §00 line 361 (REST heading), 384 (R-2 schemas),
   441 (R-4 invariant 2 with gate self-citation); §23 §97
   AC-ADB-REST-01 + AC-ADB-11; §22 `17-openapi.yaml` boolean fields
   (lines 85, 101, 103, 273, 286); §24 §00 U-3 (~line 359); §27
   backlog `rest-boolean-parity-check` (Phase-5 T-06).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (6 short Markdown + YAML blobs).
3. **Script** — `linter-scripts/check-rest-boolean-parity.py`.
4. **`--self-test`** — built-in mode, 6 fixtures (F-1 unique passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§23 REST boolean parity gate" hard-fails CI.
6. **§00 Walker-Pin row** — §23 §00 Walker-Pin block gains a row
   citing slot 57 + gate #35 + workflow step name (deferred to
   next §23 §00 touch).

## Bindings

- **§27 backlog ticket `rest-boolean-parity-check`** — closes this
  turn (T-28). Minted Phase-5 T-06; paper-only for 22 cycles.
  **Final REST-side §27 backlog ticket** retired; with this close
  the §23 REST contract is fully load-proven on naming + boolean
  surfaces.
- **AC-ADB-REST-01** + **AC-ADB-11** — clauses 1/2/4 mechanise the
  wire-side boolean policy; gate IS the cited mechanism.
- **Gate #24** (`check-boolean-uniformity-primary-lane`) — DB-side
  boolean lane. Gate #34 (`check-rest-pascalcase-parity`) clause-3
  — wire-side `Is`-prefix discipline. Slot 57 / gate #35 — wire-side
  boolean VALUE discipline + OpenAPI bijection + §24 U-3 surface
  pin. Together gates #24 + #34 + #35 form the **3-surface boolean
  parity triple (DB / wire / UI)** the cross-cuts block of slot 55
  cited as `Boolean policy (AC-ADB-11`.
- **Lesson #15 reflexivity** — clause-2 enforces gate name remains
  in R-4 invariant 2 normative text.

## Scorecard impact (Rubric v2 /120)

- **§23** — C3 +1 (boolean lane wire-side load-proven); C5 +1
  (cite mechanism is gate #35); C6 +1 (final REST-side backlog
  ticket retires — 22-cycle conversion). Cursor 118 → 119,
  Raw-LLM 114 → 115; Lovable 120 carried.
- **§22 / §24 / §25** — C4 +1 each (no-restate; OpenAPI bijection
  binds §22 git-logs-only whitelist; §24 U-3 surface pinned).
- **§27** — C6 +1 (final REST-side backlog ticket retired).

## Out of scope

- Tri-state boolean (NULL handling) — closed enumeration is
  `{true, false}`; NULL on a boolean column is a separate AC.
- Backward-compatibility shims for legacy `0`/`1` body acceptance
  — explicitly forbidden by clause-4; no exemption path.
- Non-App OpenAPI surfaces — §22 git-logs whitelist
  `{enabled, allowed, success}` is closed; new entries require
  paired §22 §97 AC.
- Field-level type validation — covered by future SQL-parser-plus-
  JSON-schema gate; this gate enforces VALUE + NAMING parity.
