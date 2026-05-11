# Slot 39 — `check-applink-xor-clause.py`

**Status:** Active gate #22 (Phase-5 T-15)
**Implements:** spec/23 §00 `## Polymorphic AppLink Resolution (Normative)` (line 244) + AC-ADB-05 (XOR target invariant) + AC-ADB-13 (locked-ID seed parity)
**Self-test:** built-in (`--self-test`) against 4 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§23 AppLink XOR clause gate"

## Contract

Promotes spec/23 AC-ADB-05 from contract-proven to **load-proven**. Walks
spec/23 `00-overview.md` and the §22 `18-schema.sql` mirror, and fails CI
when ANY of the following invariants fail on either source:

1. The DDL block defining `CREATE TABLE … AppLink` MUST contain a `CHECK (`
   clause whose body matches the byte-for-byte normative XOR pattern:
   - one disjunct binds `AppLinkTypeId = (SELECT … WHERE Name = 'GitProfile')
     AND TargetGitProfileId IS NOT NULL AND TargetRepoId IS NULL`
   - other disjunct binds `AppLinkTypeId = (SELECT … WHERE Name = 'Repo')
     AND TargetRepoId IS NOT NULL AND TargetGitProfileId IS NULL`
   - the two disjuncts are joined by `OR` (no `AND`, no third disjunct).
2. The DDL block MUST also contain the disconnect-invariant CHECK
   (`IsActive = 1 AND DisconnectedAt IS NULL` `OR` `IsActive = 0 AND
   DisconnectedAt IS NOT NULL`) per AC-ADB-R-4 invariant 6 (WE-4 fixture).
3. The DDL MUST seed `AppLinkType` with explicit IDs `(1,'GitProfile'),
   (2,'Repo')` per AC-ADB-13 — bare `INSERT … VALUES ('GitProfile'),('Repo')`
   without explicit IDs is rejected (T-10 remediation, WE-2 binding).
4. Both `IX_AppLink_TargetRepoId` and `IX_AppLink_TargetGitProfileId`
   partial indexes MUST exist with `WHERE Target… IS NOT NULL` clauses
   (so the XOR invariant has matching index coverage on both lanes).

## Invocation

```bash
python3 linter-scripts/check-applink-xor-clause.py --check all
python3 linter-scripts/check-applink-xor-clause.py --check xor
python3 linter-scripts/check-applink-xor-clause.py --check disconnect
python3 linter-scripts/check-applink-xor-clause.py --check seed-ids
python3 linter-scripts/check-applink-xor-clause.py --check indexes
python3 linter-scripts/check-applink-xor-clause.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot
(synthetic source missing, mirrors slot 27 A-22 harness convention).

## R5 — vacuously-passing scanner is auto-fail

Per the slot-36/37 R5 contract carried forward, a scanner that returns 0
because the regex matched zero `AppLink` DDL blocks is **itself a
violation** (exit `1`, message `vacuous-pass: zero AppLink DDL blocks
found in spec/23 or §22 schema mirror`). The `--self-test` mode is
mandatory in CI: it asserts that the scanner correctly REJECTS four
synthetic fixtures:

- **F-1** complete-XOR-clause + correct seed + both indexes → passes
- **F-2** XOR clause weakened to `AND` instead of `OR` → fails (clause-1)
- **F-3** seed `INSERT` omits explicit IDs → fails (clause-3, T-10/WE-2)
- **F-4** `IX_AppLink_TargetRepoId` partial-index `WHERE` clause stripped
  → fails (clause-4)
- **F-5** disconnect-invariant CHECK clause absent (WE-3/WE-4 fixture
  pair fails the reconnect-without-orphan-row predicate) → fails (clause-2)
- **F-6** R5 vacuous-pass — empty corpus / no `CREATE TABLE AppLink` fence
  found in any §23 source → fails as `vacuous-pass: empty walk → exit 3
  fixture-rot` rather than silently passing on absence.

## 5-link self-enforcement chain (A-44 template)

1. **AC text** — spec/23 §00 lines 161–197 (AppLink DDL) + lines 244–280
   (Polymorphic AppLink Resolution Normative section) + AC-ADB-05 + AC-ADB-13
   (canonical contract surface).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (no on-disk corpora needed; the four fixtures are short
   SQL strings, not full spec trees).
3. **Script** — `linter-scripts/check-applink-xor-clause.py` (this slot).
4. **`--self-test`** — built-in mode, runs 4 negative fixtures (F-1
   passes, F-2/F-3/F-4 must fail).
5. **Workflow step** — `.github/workflows/spec-health.yml` "§23 AppLink
   XOR clause gate" hard-fails CI on any violation.
6. **§00 Walker-Pin row** — spec/23 `00-overview.md` Walker-Pin block
   gains a row citing this slot + gate #22 + workflow step name
   (deferred to next §23 §00 touch; in-spec catalogue holds until then).

## Bindings to Worked Examples (T-11)

This gate is the load-proven mechanization of three of the four §23 §00
WE fixtures:

- **WE-2** (Reconnect always-INSERT per Q3) — gate clause 3 enforces
  the locked-ID seed shape `INSERT … VALUES (1,'GitProfile'),(2,'Repo')`
  that WE-2's reconnect SQL depends on.
- **WE-3** (Boolean-coercion attack on R-01 `IsActive: 1`) — gate
  clause 2 enforces the disconnect-invariant CHECK that WE-3's 422
  rejection cites as the violated DB invariant.
- **WE-4** (Disconnect already-disconnected idempotent) — gate clause 2
  enforces the same disconnect CHECK whose `IsActive = 0 AND
  DisconnectedAt IS NOT NULL` disjunct WE-4's PRESERVED timestamp
  assertion relies on.

WE-1 (resolve unknown RepoUrl → 404) is out-of-scope for this gate
(error-envelope concern; covered by §27 backlog gate
`error-envelope-uniformity-check`, T-12).

## Bindings to Cross-cutting App Framework (T-12)

- **AC-CAF-01** (wire-boolean parity end-to-end) — clause 2's
  disconnect-invariant CHECK is the §23-side anchor of the CAF-01
  contract. Until `boolean-uniformity-primary-lane-check` ships
  separately, this gate provides partial coverage on the `IsActive`
  column specifically.

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-39/`) and run `python3 linter-scripts/check-applink-xor-clause.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #22 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/check-applink-xor-clause.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #22 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## History

- **Phase-5 T-15** — slot created. Built-in self-test only (no on-disk
  fixture corpus needed because the four fixtures are short SQL strings
  exercising `re` predicates against synthetic DDL blobs). Mirrors
  slot-37 A-48 in-memory-tempdir convention. Closes the §27 backlog
  entry `applink-xor-check-clause-present` (originally minted Sess-43
  during the cohort-rule sweep).
