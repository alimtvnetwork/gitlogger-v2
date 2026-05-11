# Slot 45 — `check-idempotency-observability.py`

**Status:** Active gate #26 (Phase-5 T-19)
**Implements:** §23 §00 R-1 endpoint matrix (line 370) + §23 §00 R-4 invariant 6 (line 445) + §23 §00 WE-4 disconnect-path worked example (line 568) + §24 §00 S-2 settings persistence matrix (line 419) + §24 §00 U-1 component-binding matrix (line 331) + §24 §97 **AC-CAF-03** (line 245 — "Idempotency contract is observable at every layer")
**Self-test:** built-in (`--self-test`) against 5 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§22+§23+§24 idempotency observability gate"

## Contract

Promotes AC-CAF-03 from conditional (paper-only at T-12 landing; 3-turn
decay clause shared with CAF-01/02/04/05 — only CAF-03 + CAF-05 remained
paper-only after T-18) to **load-proven** end-to-end. Walks the
`Idempotent=Yes/No` flag surface across §23 R-1 and §24 S-2, the
AC-CAF-03 declaring text, the §23 WE-4 disconnect-path observability
fixture, and the §24 U-1 component-binding matrix. Fails CI when ANY
of the following observability invariants fail:

1. **Idempotent-set parity (declaring AC ↔ matrix truth)** — the
   AC-CAF-03 declaring text enumerates the **Yes** set
   `{R-02, R-03, R-05, R-06, R-07, R-09, R-11, R-13}` and the **No**
   set `{R-01, R-04, R-08, R-15}`. The union of `Idempotent` columns
   in §23 §00 R-1 (R-01..R-08) and §24 §00 S-2 (R-09..R-15) MUST
   reproduce these two sets exactly. Drift in either direction fails:
   (a) §23/§24 flips a row's flag without amending CAF-03 — fail;
   (b) CAF-03 enumerates an ID absent from R-1∪S-2 — fail (AC-CAF-03
   would silently shadow a non-existent endpoint).
2. **Observability marker discipline (CAF-03 prose-shape lock)** —
   the AC-CAF-03 declaring text (§24 §97 line 245) MUST contain
   ALL FOUR literal tokens: `EXPLAIN QUERY PLAN`, `IDENTICAL body`,
   `modulo TraceId`, and `WE-4`. Removing any single token collapses
   the AC to "subjective prose"; the four-literal marker IS the
   verifiable observability mechanism the AC text promises.
3. **WE-4 disconnect-path observability cite** — §23 §00 WE-4 (line
   568, "Disconnect already-disconnected link → 200 idempotent")
   MUST contain ALL of: the literal `idempotent`, the literal `200`,
   the literal `DisconnectedAt`, and the canonical "second call is a
   no-op" phrasing (`no-op` OR `from the first call` OR
   `read, don't rewrite`). §23 §00 R-4 invariant 6 (line 445) MUST
   contain the literal `Idempotency` AND name `R-07` explicitly as
   the worked-example endpoint.
4. **UI no-aliasing (§24 U-1)** — §24 §00 U-1 row text for any
   component whose `Endpoint(s)` column cites an ID from the
   non-idempotent set `{R-01, R-04, R-08, R-15}` MUST NOT include
   the literal token `Idempotent` (case-insensitive) in its row body
   or surrounding note. Aliasing a non-idempotent POST/INSERT row
   under "Idempotent" in the UI is exactly the failure mode
   AC-CAF-03's last sentence prohibits ("Non-idempotent endpoints
   (R-01, R-04, R-08, R-15) MUST NOT be aliased as Idempotent in
   the UI layer (§24 U-1 binding column)").
5. **No restate-drift** — neither §22 (`17-openapi.yaml` /
   `20-observability.md`) nor §25 may inline a parallel "Idempotency
   contract" matrix redeclaring the per-endpoint Yes/No flag column.
   §22 MAY surface idempotency via OpenAPI extension headers
   (`x-idempotent: true`) — that is wire-shape, not a parallel
   matrix. The R-1 + S-2 columns are the binding source-of-truth
   per AC-CAF-03's `§23 R-1` cite. Inline restate is itself a gate
   #15 `derives-from-restate-check` violation at meta-level.

## Invocation

```bash
python3 linter-scripts/check-idempotency-observability.py --check all
python3 linter-scripts/check-idempotency-observability.py --check set-parity
python3 linter-scripts/check-idempotency-observability.py --check observability-marker
python3 linter-scripts/check-idempotency-observability.py --check we4-cite
python3 linter-scripts/check-idempotency-observability.py --check ui-no-alias
python3 linter-scripts/check-idempotency-observability.py --check no-restate
python3 linter-scripts/check-idempotency-observability.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

A scanner that returns 0 because the §23 R-1 / §24 S-2 / AC-CAF-03
text matched zero rows or zero literals is **itself a violation**
(exit `1`, message `vacuous-pass: zero R-1/S-2 idempotency rows or
zero AC-CAF-03 anchors found`). The `--self-test` mode is mandatory
in CI and asserts that the scanner correctly REJECTS five synthetic
fixtures:

- **F-1** complete-uniform (R-1 8-row matrix with canonical Yes/No
  flags, S-2 7-row matrix with canonical Yes/No flags, AC-CAF-03
  text carrying all four literal markers + correct enumerations,
  WE-4 carrying all four literals + R-4 inv-6 naming R-07, U-1 with
  no `Idempotent` token on R-01/R-04/R-08 rows, no parallel matrix
  in §22 / §25) → passes
- **F-2** §23 R-1 flips R-07's flag from `Yes` to `No` without
  amending AC-CAF-03 → fails (clause-1; set-parity drift)
- **F-3** AC-CAF-03 text drops the `EXPLAIN QUERY PLAN` literal →
  fails (clause-2; observability marker stripped)
- **F-4** §24 U-1 row U-03 (`AppCreateDialog` → R-01) gains the
  inline note `(Idempotent retry)` → fails (clause-4; UI alias of
  non-idempotent POST)
- **F-5** §22 `20-observability.md` inlines a parallel
  "Idempotency contract" matrix re-listing all R-NN flags → fails
  (clause-5; restate-drift)
- **F-6** R5 vacuous-pass — no R-1 8-row matrix found in §23 §00 →
  fails as `vacuous-pass: empty walk → exit 3 fixture-rot` rather than
  silently passing on absence.

## 5-link self-enforcement chain

1. **AC text** — §24 §97 AC-CAF-03 (line 245); §23 §00 R-1 (line
   370) + R-4 invariant 6 (line 445) + WE-4 (line 568); §24 §00 S-2
   (line 419) + U-1 (line 331).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (5 short Markdown blobs reproducing the R-1 / S-2
   / U-1 / WE-4 / AC-CAF-03 anchor geometry).
3. **Script** — `linter-scripts/check-idempotency-observability.py`
   (this slot).
4. **`--self-test`** — built-in mode, runs 5 fixtures (F-1 unique
   passing fixture).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§22+§23+§24 idempotency observability gate" hard-fails CI on
   any violation.
6. **§00 Walker-Pin row** — §24 `00-overview.md` Walker-Pin block
   gains a row citing this slot + gate #26 + workflow step name
   (deferred to next §24 §00 touch; in-spec catalogue holds until
   then).

## Bindings

- **AC-CAF-03** (T-12) — converts from conditional 20 (paper-only;
  3-turn decay clause shared with CAF-01/02/04/05) to un-conditional
  20 (load-proven). This gate IS the cited self-enforcing mechanism.
  **Fourth cross-cutting CAF gate** after T-16 gate #23 (CAF-02),
  T-17 gate #24 (CAF-01), T-18 gate #25 (CAF-04). Only **CAF-05**
  (audit-quoted-evidence marker) remains paper-only after T-19.
- **§23 §00 R-4 invariant 6** (Idempotency, line 445) — gate clause
  3 mechanises the cross-folder cite; the gate guarantees R-07 stays
  named in the invariant body as the canonical worked example.
- **§23 §00 WE-4** (Disconnect already-disconnected, line 568) —
  the canonical fixture for the disconnect path AC-CAF-03 cites by
  name; clause-3 prevents WE-4 from drifting away from its
  observability literals.
- **§24 §00 U-1** (line 331) — gate clause-4 forbids the alias-drift
  pattern AC-CAF-03's last sentence prohibits; first machine check
  on the U-1 binding column's no-alias contract.
- **§24 §00 S-2** (line 419) — settings persistence matrix gains
  bidirectional set-parity coverage with §23 R-1 (clause-1).

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-45/`) and run `python3 linter-scripts/check-idempotency-observability.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #26 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/check-idempotency-observability.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #26 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## Out of scope

- Runtime fixture replay against live HTTP endpoints — owned by
  gate #17 (`error-envelope-shape-check`) + gate #18
  (`request-id-roundtrip-check`) integration-test family. This gate
  is a **static contract-surface gate** (string + matrix predicates),
  not an HTTP harness. The two layers are complementary: this gate
  locks the prose declaration; gates #17/#18 lock the runtime mirror.
- `EXPLAIN QUERY PLAN` execution against an actual SQLite database —
  out of scope (would require shipping a fixture DB; clause-2 only
  asserts the literal token PRESENCE in the AC text). A future
  Wave-3 integration-test gate MAY ship the live `EXPLAIN` walker;
  this slot enforces the contract surface for it.
- §25 audit-finding text rewriting AC-CAF-03 — covered by the
  forthcoming `audit-quoted-evidence-marker-check` (CAF-05 gate),
  not this slot.

## History

- **Phase-5 T-19** — slot created. Built-in self-test only (no
  on-disk fixture corpus needed; the five fixtures are short
  Markdown blobs exercising `re` predicates against synthetic
  R-1/S-2/U-1/WE-4 anchor geometry). Mirrors slot-44 T-18
  cross-folder uniformity convention. Closes §27 backlog entry
  `idempotency-observability-check` minted T-12 (paired with
  `audit-quoted-evidence-marker-check` for CAF-05; the two were
  the only cross-cutting CAF backlog tickets remaining after T-18).
  Promotes AC-CAF-03 from conditional to un-conditional
  self-enforcing — fourth cross-cutting CAF gate after T-16 gate
  #23 (CAF-02), T-17 gate #24 (CAF-01), T-18 gate #25 (CAF-04).
  Four of the five CAF cross-cutting ACs are now load-proven; only
  CAF-05 (audit-finding evidence quoting) remains paper-only.
