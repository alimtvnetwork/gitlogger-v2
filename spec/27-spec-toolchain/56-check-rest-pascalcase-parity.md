# Slot 56 — `check-rest-pascalcase-parity.py`

**Status:** Active gate #34 (Phase-5 T-27)
**Implements:** §23 §00 `## REST / RPC Contract (Normative — Phase-5 T-06)` (line 361) + R-1 endpoint matrix (line 370) + R-2 JSON schemas (line 384) + R-4 invariant 1 PascalCase parity (line 440) + §23 §97 AC-ADB-REST-01 (line 454) + §23 PRIMARY-lane DDL column-name set (line 116 + DDL fences under "Inlined Contracts") (closes §27 backlog `rest-pascalcase-parity-check` minted Phase-5 T-06)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§23 REST PascalCase parity gate"

## Contract

Walks `spec/23-app-database/00-overview.md` and asserts the
on-the-wire JSON key set in the R-2 sample bodies is bijectively
1:1 with the PRIMARY-lane DDL column-name set declared in the
inlined `App` / `AppLink` SQLite DDL fences (and the small set of
synthetic request-only fields explicitly whitelisted below).
Materialises the AC-ADB-REST-01 invariant 1 (PascalCase parity)
that the §23 R-4 block cites self-referentially as "self-enforcing
via §27 backlog gate `rest-pascalcase-parity-check`". Fails CI when
ANY of the following invariants fail:

1. **PascalCase shape on every wire key** — every JSON key extracted
   from any ` ```jsonc ` or ` ```json ` fence inside the §23 §00
   "REST / RPC Contract" section MUST match the regex
   `^[A-Z][A-Za-z0-9]*$` (PascalCase, no underscore, no leading
   lowercase). camelCase (`appId`), snake_case (`app_id`), and
   kebab-case keys all fail clause-1 with the offending key + line.
   Top-level wrapper keys `Error`, `items` are explicitly
   whitelisted (the wrapper `items` is the only exception and is
   pinned in R-2 line 376).
2. **Wire ↔ DDL bijection** — the union of JSON keys observed in
   R-2 response shapes (`App`, `AppLink`) MUST equal the union of
   PRIMARY-lane DDL column names declared in the §23 §00
   `## Inlined Contracts` `App` + `AppLink` SQLite fences, modulo
   the request-only whitelist `{RepoUrl, ResolutionState}` (R-06
   request body + R-2 enum field) and the response-only whitelist
   `{}`. Adding a wire key with no DDL backing column (or vice
   versa) fails clause-2 with the offending side + key.
3. **Boolean key `Is`-prefix discipline** — every JSON key whose
   sample value is the literal `true` or `false` in any R-2 fence
   MUST start with the prefix `Is`. Conversely every DDL column
   declared `INTEGER` with a `CHECK (... IN (0,1))` constraint or
   sourced from the AC-ADB-11 boolean policy MUST be `Is`-prefixed.
   A `true`/`false` sample value on a non-`Is` key fails clause-3.
4. **R-4 invariant 1 literal preservation** — the §23 §00 R-4
   block MUST contain the literal substrings `PascalCase parity`,
   `1:1`, `No camelCase`, `no snake_case on the wire`, AND the
   self-citation `Self-enforcing via §27 backlog gate
   \`rest-pascalcase-parity-check\``. Stripping the self-citation
   converts R-4 invariant 1 back to subjective prose and fails
   clause-4 (Lesson #15 reflexivity — gate name must remain in the
   normative text it enforces).
5. **AC-ADB-REST-01 surface presence** — §23 §97 MUST contain the
   literal heading `### AC-ADB-REST-01 — REST/RPC contract present
   and parity-pinned` (or the §00-mirrored variant on line 454)
   AND its body MUST cite the literal `8-row R-1 endpoint matrix`
   AND `R-4 invariants 1–7` AND end with an `[active]` /
   `[deferred]` / `[archived]` status tag (per gate #28 contract).
6. **No-restate in §22/§24/§25** — no `.md` under
   `spec/22-git-logs-v2/`, `spec/24-app-design-system-and-ui/`, or
   `spec/25-app-issues/` may carry a parallel
   `## REST / RPC Contract` heading or restate the App-side R-1
   endpoint matrix as a fenced table (Lesson #36 — single source
   of truth for the App REST contract is §23 §00). The §22-side
   git-logs OpenAPI (`17-openapi.yaml`) is exempt — it owns the
   git-logs surface, not the App surface.

## Invocation

```bash
python3 linter-scripts/check-rest-pascalcase-parity.py --check all
python3 linter-scripts/check-rest-pascalcase-parity.py --check pascalcase-shape
python3 linter-scripts/check-rest-pascalcase-parity.py --check wire-ddl-bijection
python3 linter-scripts/check-rest-pascalcase-parity.py --check boolean-is-prefix
python3 linter-scripts/check-rest-pascalcase-parity.py --check r4-invariant-literals
python3 linter-scripts/check-rest-pascalcase-parity.py --check ac-rest-01-surface
python3 linter-scripts/check-rest-pascalcase-parity.py --check no-restate
python3 linter-scripts/check-rest-pascalcase-parity.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3`
fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if the §23 §00 REST section heading was located,
≥1 R-2 JSON fence was parsed, ≥6 wire keys were extracted, ≥1
PRIMARY-lane DDL fence was parsed, the R-4 block was located, AND
the AC-ADB-REST-01 surface was located in §23 §97. Zero anchors
→ exit `1` with `vacuous-pass: §23 §00 REST section absent / R-2
JSON fence absent / wire-key set < 6 / PRIMARY-lane DDL fence
absent / R-4 block absent / AC-ADB-REST-01 surface absent`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-uniform (R-2 fences present with PascalCase keys
  matching DDL columns 1:1; R-4 block carries all literals + gate
  self-citation; AC-ADB-REST-01 surface present and `[active]`)
  → passes
- **F-2** R-2 `App` fence ships key `appId` (camelCase) → fails
  clause-1
- **F-3** R-2 `AppLink` fence introduces wire-only key
  `LinkLabel` with no PRIMARY-lane DDL backing column → fails
  clause-2
- **F-4** R-2 `App` fence carries `Active: true` (boolean sample
  value on non-`Is`-prefixed key) → fails clause-3
- **F-5** R-4 invariant 1 stripped of `Self-enforcing via §27
  backlog gate \`rest-pascalcase-parity-check\`` self-citation
  → fails clause-4 (Lesson #15 reflexivity)
- **F-6** §24 child `04-rest-mirror.md` introduced with parallel
  `## REST / RPC Contract` heading restating R-1 → fails clause-6

## 5-link self-enforcement chain

1. **AC text** — §23 §00 lines 361 (heading), 370 (R-1 matrix),
   384 (R-2 schemas), 440 (R-4 invariant 1 with self-citation),
   454 (AC-ADB-REST-01); §23 §00 line 116 (PascalCase DDL naming);
   §27 backlog `rest-pascalcase-parity-check` (Phase-5 T-06).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (6 short Markdown blobs reproducing R-2 JSON
   fences, PRIMARY-lane DDL fences, R-4 block, AC-ADB-REST-01
   surface, and §24-side restate fixture).
3. **Script** — `linter-scripts/check-rest-pascalcase-parity.py`.
4. **`--self-test`** — built-in mode, runs 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§23 REST PascalCase parity gate" hard-fails CI.
6. **§00 Walker-Pin row** — §23 §00 Walker-Pin block gains a row
   citing slot 56 + gate #34 + workflow step name (deferred to
   next §23 §00 touch).

## Bindings

- **§27 backlog ticket `rest-pascalcase-parity-check`** — closes
  this turn (T-27). Minted Phase-5 T-06 alongside the REST/RPC
  contract section; paper-only for 21 cycles. Conversion to
  load-proven via this gate.
- **AC-ADB-REST-01** (REST/RPC contract present + parity-pinned)
  — clauses 1/2/3/4/5 mechanise the parity invariant; gate IS
  the cited mechanism. Promotes AC-ADB-REST-01 from conditional
  20 to un-conditional 20.
- **Slot 55 / Gate #33** (`check-dialect-precedence-banner-present`)
  — clause-3 boolean-`Is`-prefix discipline mirrors gate #33
  cross-cuts literal `Boolean policy (AC-ADB-11)`; together they
  form the dialect-banner ↔ wire-shape parity pair.
- **Gate #24** (`check-boolean-uniformity-primary-lane`) — clause-3
  `Is`-prefix scan is the wire-side mirror of gate #24's DB-side
  primary-lane boolean scan. Together they form a 3-surface
  boolean parity triple (DB / wire / UI) when combined with §24
  U-3 binding.
- **Gate #28** (`check-ac-section-orphan-header`) — clause-5
  status-tag requirement piggybacks on gate #28's
  `[active]`/`[deferred]`/`[archived]` enforcement.
- **Lesson #15 reflexivity** — clause-4 enforces the gate name
  remains in R-4 invariant 1's self-citation; if the §23 §00 text
  is rewritten without re-citing the gate, the gate fails itself.

## Scorecard impact (Rubric v2 /120)

- **§23** — C3 (Testability) +1 (REST contract now load-proven —
  no silent wire-key drift); C4 (Consistency) +1 (wire ↔ DDL
  bijection mechanised); C5 (Implementability) +1 (R-4 invariant 1
  un-ambiguous — cite mechanism is gate #34); C6 (Friction) +1
  (the long-paper-only Phase-5 T-06 backlog ticket retires).
  §23 advances toward 120/120 ceiling on Cursor (117 → 118) and
  Raw-LLM (112 → 114) personas; Lovable already at 120 carried.
- **§22 / §24 / §25** — C4 (Consistency) +1 each (no-restate
  clause forbids parallel App-REST surfaces in any of the three
  sibling folders).
- **§27** — C6 (Friction) +1 (oldest Phase-5 T-06 backlog ticket
  retired — paper-only for 21 cycles, longest-aged §23 backlog
  entry).

## Out of scope

- OpenAPI schema correctness for the §22 git-logs surface
  (`17-openapi.yaml`) — covered by §22-side gates; this gate is
  scoped to the App REST contract under §23 §00 only.
- HTTP-status-code parity (whether 422 vs 400 is appropriate) —
  covered by R-3 error envelope contract + gate #23
  (`check-error-envelope-uniformity`).
- Idempotency-flag parity (R-1 column "Idempotent") — covered by
  gate #26 (`check-idempotency-observability`).
- Authentication / role / scope columns of R-1 — out of
  locked-7 scope; live cross-refs forbidden per scope-lock.
- Field-level type validation (whether `AppId` is INTEGER vs
  string) — type-shape parity is left to a future SQL-parser-plus-
  JSON-schema gate; this gate enforces NAMING parity, not TYPE
  parity.
