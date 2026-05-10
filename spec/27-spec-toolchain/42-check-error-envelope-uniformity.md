# Slot 42 — `check-error-envelope-uniformity.py`

**Status:** Active gate #23 (Phase-5 T-16)
**Implements:** §22 `17-openapi.yaml` `ErrorEnvelope` schema (line 219) + §23 §00 R-3 error-envelope (line ~456) + §24 §00 AC-ADS-15 namespace-extension contract (line 53) + cross-cutting **AC-CAF-02** (T-12 — uniform error envelope across DB-fault and UI-render paths)
**Self-test:** built-in (`--self-test`) against 5 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§22+§23+§24 ErrorEnvelope uniformity gate"

## Contract

Promotes AC-CAF-02 from contract-proven (paper-only at T-12 landing) to
**load-proven**. Walks the three error-envelope anchors and fails CI when
ANY of the following uniformity invariants fail:

1. **Schema source-of-truth pin** — §22 `17-openapi.yaml` MUST declare
   exactly one top-level `ErrorEnvelope` schema under `components.schemas`
   (line 219 anchor); duplicate definitions or relocations are rejected.
2. **DB-side mirror (R-3)** — §23 §00 MUST cite `R-3 error envelope` in
   the AppLink CRUD section (line ~456 anchor) AND every R-3 worked
   example (`WE-1..WE-N` introduced T-11) MUST embed an HTTP response
   whose JSON shape conforms to the §22 schema field set
   (`Error.Code`, `Error.Message`, `Error.Field?`, `RequestId`,
   `TraceId?`, `Timestamp`).
3. **UI-side mirror (AC-ADS-15)** — §24 §00 MUST carry the AC-ADS-15
   namespace-extension table row binding `ADS-*` codes to the §22
   `ErrorEnvelope` shape AND the `<AppErrorState/>` component contract
   (line ~352) MUST cite both `Error.Message` AND `TraceId` (or
   `RequestId`) as required render-side fields.
4. **Code-prefix discipline** — every `ErrorEnvelope.Error.Code` literal
   in §22 / §23 / §24 MUST match `^(GL|ADB|ADS|CAF)-[A-Z0-9-]+$` AND
   MUST be declared in at least one §97 AC body across the three
   folders (no orphan codes; no foreign prefixes).
5. **No restate-drift** — neither §23 nor §24 may inline a YAML schema
   block redefining `ErrorEnvelope` field set; both MUST cite §22
   `17-openapi.yaml` line-anchor as the single source per Lesson #36.

## Invocation

```bash
python3 linter-scripts/check-error-envelope-uniformity.py --check all
python3 linter-scripts/check-error-envelope-uniformity.py --check schema-pin
python3 linter-scripts/check-error-envelope-uniformity.py --check db-mirror
python3 linter-scripts/check-error-envelope-uniformity.py --check ui-mirror
python3 linter-scripts/check-error-envelope-uniformity.py --check code-prefix
python3 linter-scripts/check-error-envelope-uniformity.py --check no-restate
python3 linter-scripts/check-error-envelope-uniformity.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3`
fixture-rot (synthetic source missing; mirrors slot 39 / slot 27 A-22
harness convention).

## R5 — vacuously-passing scanner is auto-fail

A scanner that returns 0 because the `ErrorEnvelope` regex matched zero
schema blocks is **itself a violation** (exit `1`, message
`vacuous-pass: zero ErrorEnvelope schema blocks found in §22 17-openapi.yaml`).
The `--self-test` mode is mandatory in CI and asserts that the scanner
correctly REJECTS five synthetic fixtures:

- **F-1** complete-uniform (schema in §22, R-3 cite in §23, AC-ADS-15
  row in §24, all codes prefix-conformant + AC-cited, no restate
  blocks) → passes
- **F-2** §23 R-3 worked-example response missing `RequestId` field →
  fails (clause-2)
- **F-3** §24 `<AppErrorState/>` row drops `TraceId` requirement →
  fails (clause-3)
- **F-4** §23 invents code `DB-FOREIGN-XYZ` (foreign prefix) → fails
  (clause-4)
- **F-5** §23 inlines a YAML `ErrorEnvelope:` block redefining the
  field set → fails (clause-5)

## 5-link self-enforcement chain (A-44 template)

1. **AC text** — §22 `17-openapi.yaml` line 219 (`ErrorEnvelope` schema)
   + §23 §00 line ~456 (R-3 cite + WE-1..WE-N) + §24 §00 line 53
   (AC-ADS-15) + §24 §00 line ~352 (`<AppErrorState/>` contract) +
   AC-CAF-02 (canonical cross-cutting clause).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (5 short YAML + Markdown blobs; no on-disk corpora
   needed).
3. **Script** — `linter-scripts/check-error-envelope-uniformity.py`
   (this slot).
4. **`--self-test`** — built-in mode, runs 5 fixtures (F-1 unique
   passing fixture).
5. **Workflow step** — `.github/workflows/spec-health.yml` "§22+§23+§24
   ErrorEnvelope uniformity gate" hard-fails CI on any violation.
6. **§00 Walker-Pin row** — §22 + §23 + §24 `00-overview.md`
   Walker-Pin blocks each gain a row citing this slot + gate #23 +
   workflow step name (deferred to next §00 touch on each folder; in-spec
   catalogue holds until then).

## Bindings

- **AC-CAF-02** (T-12) — converts from conditional 20 (paper-only;
  3-turn decay clause) to un-conditional 20 (load-proven). This gate
  IS the cited self-enforcing mechanism.
- **AC-ADS-15** (§24) — shipping this gate satisfies the namespace
  extension's "machine-checked" sibling clause without amending
  AC-ADS-15 text.
- **§23 R-3 worked-examples (T-11 WE-1..WE-N)** — clause 2
  cross-validates the WE response bodies against the §22 schema;
  WE-1's 404 envelope is the canonical positive fixture.
- **§22 AC-30** (`ErrorEnvelope` schema canonical cite) — clause 1
  provides the schema-pin verifier this AC has cited as
  "implementation pending" since Sess-43.

## Out of scope

- Field-level value validation (e.g. `RequestId` UUID format) — that
  belongs to gate #18 `request-id-roundtrip-check` (already shipped).
- Localised `Error.Message` text content — §24 i18n concern, not
  envelope uniformity.
- Status-code → envelope-code mapping — covered by gate #17
  `error-envelope-shape-check` (HTTP fixture replay; complementary,
  not duplicate).

## History

- **Phase-5 T-16** — slot created. Built-in self-test only (no on-disk
  fixture corpus needed; the five fixtures are short YAML + Markdown
  strings exercising `re` + `yaml.safe_load` predicates against
  synthetic blobs). Mirrors slot-39 T-15 in-memory-tempdir convention.
  Closes §27 backlog entry `error-envelope-uniformity-check` minted
  T-12. Promotes AC-CAF-02 from conditional to un-conditional self-
  enforcing.
