# Slot 49 — `check-ui-component-binding-matrix.py`

**Status:** Active gate #30 (Phase-5 T-23)
**Implements:** §24 §00 `## UI Contract (Normative — Phase-5 T-07)` U-1 / U-2 / U-3 (line 322+) + §23 §00 R-1 endpoint matrix (line 370) + §24 §97 AC-ADS-UI-01 / AC-ADS-UI-02 (closes §27 backlog `ui-component-binding-matrix-check`)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§24 U-1 component binding gate"

## Contract

Walks the §24 §00 U-1 / U-2 / U-3 matrices and the §23 §00 R-1
endpoint matrix and asserts the cross-folder binding contract.
Closes the §27 backlog `ui-component-binding-matrix-check` ticket.
Fails CI when ANY of the following invariants fail:

1. **U-1 endpoint references resolve in §23 R-1** — every `R-NN`
   token in the U-1 `Endpoint(s)` column MUST appear as a row ID
   in §23 §00 R-1 endpoint matrix (line 370). An orphan `R-99` in
   U-1 is a foreign-endpoint binding and fails clause-1 with the
   offending U-N row + R-NN.
2. **No orphan §23 R-NN endpoints** — every `R-NN` in §23 R-1 with
   role-tag matching `user` or `admin` (UI-consumable) MUST be
   referenced by at least one U-1 row's `Endpoint(s)` column.
   Service-only endpoints (role-tag `svc` or explicit
   `<!-- svc-only -->` comment) are exempt. An orphan UI-consumable
   `R-NN` is an unbound endpoint and fails clause-2 with the
   offending R-NN. (Reverse coverage of clause-1.)
3. **U-2 four-state contract literal presence** — §24 §00 U-2 table
   MUST contain all four state rows with literal slot components
   `<AppSkeleton/>`, `<AppEmptyState/>`, `<AppErrorState/>`, and
   the literal `(the component body)` for the `ready` state. AND
   the U-2 prose paragraph below the table MUST contain literals
   `data-error-code`, `Error.TraceId`, and `copy-to-clipboard`.
   Stripping any literal collapses U-2 to subjective prose and
   fails clause-3.
4. **U-1 role-gate enum discipline** — every U-1 `Role gate` column
   value MUST be one of the closed set
   `{user, admin, svc, svc/admin, admin/svc}`. A free-form value
   like `editor` or `power-user` fails clause-4 — the role enum
   is the §22 ALW namespace surface and cannot drift unilaterally.
5. **U-3 boolean parity literal presence** — §24 §00 U-3 paragraph
   MUST contain ALL of: `IsActive: true`, `IsActive: false`,
   `--app-status-active`, `--app-status-inactive`, `MUST NOT render
   raw 0/1`, `MUST NOT invert`, `MUST NOT introduce a third`, and
   `Mirrors §23 R-4 invariant 2`. Stripping any literal breaks the
   §23↔§24 boolean parity contract gate #24 already enforces on
   the §23 side; clause-5 closes the §24-prose side. Mirrors
   gate #24 clause-3 (UI render parity).
6. **No restate of §23 R-1 matrix in §24** — no other table in
   `spec/24-app-design-system-and-ui/**/*.md` may declare a column
   header set matching `{ID, Endpoint, Method, Path}` (the §23 R-1
   shape). Any duplicate is a Lesson #36 link-don't-restate
   violation and fails clause-6 with the offending file:line.

## Invocation

```bash
python3 linter-scripts/check-ui-component-binding-matrix.py --check all
python3 linter-scripts/check-ui-component-binding-matrix.py --check u1-endpoints-resolve
python3 linter-scripts/check-ui-component-binding-matrix.py --check no-orphan-r-endpoints
python3 linter-scripts/check-ui-component-binding-matrix.py --check u2-four-state-literals
python3 linter-scripts/check-ui-component-binding-matrix.py --check u1-role-enum
python3 linter-scripts/check-ui-component-binding-matrix.py --check u3-boolean-literals
python3 linter-scripts/check-ui-component-binding-matrix.py --check no-restate-r1
python3 linter-scripts/check-ui-component-binding-matrix.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if §24 U-1 has ≥1 row, §23 R-1 has ≥1 row, and
the U-2 four-state slot literals + U-3 boolean literals were
walked. Zero anchors → exit `1` with `vacuous-pass: zero U-1 / R-1
rows or zero U-2 / U-3 literals parsed`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-uniform → passes
- **F-2** U-01 binds `R-99` (not in §23 R-1) → fails clause-1
- **F-3** §23 R-1 lists `R-12` with role `user` but no U-1 row
  references it → fails clause-2
- **F-4** U-2 table omits `<AppErrorState/>` row → fails clause-3
- **F-5** U-04 sets `Role gate` to `editor` → fails clause-4
- **F-6** §24 child file `02-routes.md` declares a duplicate
  `| ID | Endpoint | Method | Path |` table → fails clause-6

## 5-link self-enforcement chain

1. **AC text** — §24 §00 U-1 (line 322), U-2 (line 339), U-3
   (line 358); §23 §00 R-1 (line 370); §24 §97 AC-ADS-UI-01 +
   AC-ADS-UI-02 + AC-ADS-UI-03.
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (6 short Markdown blobs reproducing U-1 / U-2 /
   U-3 / R-1 geometry).
3. **Script** — `linter-scripts/check-ui-component-binding-matrix.py`.
4. **`--self-test`** — built-in mode, runs 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§24 U-1 component binding gate" hard-fails CI.
6. **§00 Walker-Pin row** — §24 §00 Walker-Pin block gains a row
   citing slot 49 + gate #30 + workflow step name (deferred to
   next §24 §00 touch).

## Bindings

- **§27 backlog ticket `ui-component-binding-matrix-check`** —
  closes this turn (T-23). The §24 U-1 first-class structural
  gate; the §24 first-class C5 self-enforce mechanism for the
  UI ↔ REST binding contract.
- **AC-ADS-UI-01** (component registry) — clause-1 + clause-2
  mechanise the bidirectional UI↔REST binding; gate IS the cited
  mechanism.
- **AC-ADS-UI-02** (async-state accessibility) — clause-3
  mechanises the four-state slot literal + accessibility
  attribute presence.
- **AC-ADS-UI-03** (boolean rendering parity) — clause-5
  mechanises the §24-prose side of the §23↔§24 boolean parity
  contract; sibling to gate #24 clause-3 (which covers the §23
  R-4 inv-2 + §22 OpenAPI + §24 prose `IsActive` keys).
- **Gate #15 D7-self-enforcement** (`derives-from-restate-check`)
  — clause-6 extends D7 to the U-1 matrix shape; sibling to
  gate #25 clause-6 (no parallel persistence matrix in §22/§23).
- **Lesson #36 link-don't-restate** — clause-6 is the §24 surface
  application of the cross-cutting Lesson #36 rule.

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-49/`) and run `python3 linter-scripts/check-ui-component-binding-matrix.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #30 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/check-ui-component-binding-matrix.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #30 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## Scorecard impact (Rubric v2 /120)
- **§24** — C3 (Testability) +1 (U-1 binding now mechanised);
  C5 (Implementability) +1 (UI↔REST binding self-enforcing
  via this gate; cite mechanism is gate #30 itself); C4 +1
  (clause-6 closes the U-1 restate vector). §24 advances
  toward the 19-20 self-enforcing band.
- **§23** — C4 +1 (R-1 matrix gains its first reverse-coverage
  consumer-side gate; orphan-endpoint detection load-proven).
- **§27** — C6 (Friction) +1 (one more backlog ticket closed;
  ownership-map round-trip from slot 48 extends naturally).

## Out of scope

- Runtime component existence (whether `AppList.tsx` actually
  exists in `src/components/`) — covered by gate #19
  (`ads-boundaries-check`) and would require AST scan; this gate
  enforces only the SPEC-SIDE binding matrix.
- Network-call shape (whether `AppList` actually issues `GET /apps`)
  — runtime concern; out-of-scope for this static gate.
- Role-gate semantic correctness (whether `admin` is the right
  gate for `AppCreateDialog`) — security policy, not binding
  shape.
