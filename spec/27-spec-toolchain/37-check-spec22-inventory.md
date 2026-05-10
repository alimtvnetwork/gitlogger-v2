# Slot 37 — `check-spec22-inventory.py`

**Status:** Active gate #20 (Sess-56 A-48)
**Implements:** spec/22 §97 AC-78 (Module asset inventory pin) + AC-22-LV1 (locked-vacant slots 09..13)
**Self-test:** built-in (`--self-test`) against 3 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§22 module asset inventory gate"

## Contract

Promotes spec/22 AC-78 from contract-proven to **load-proven**. Walks the
canonical spec/22 inventory and fails CI when:

1. Any required tier-1 file is missing or empty:
   `00-overview.md`, `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md`.
2. Any required normative non-`.md` fixture is missing or empty:
   `18-schema.sql`, `33-bats-test-skeleton.md`, `34-phpunit-test-skeleton.md`, `35-reference-ci-yml.md`.
3. Any locked-vacant slot in the range `09..13` is occupied (AC-22-LV1 violation).

## Invocation

```bash
python3 linter-scripts/check-spec22-inventory.py --check all
python3 linter-scripts/check-spec22-inventory.py --check inventory
python3 linter-scripts/check-spec22-inventory.py --check locked-vacant
python3 linter-scripts/check-spec22-inventory.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Per the slot-36 R5 contract carried forward to slot 37, a scanner that
returns 0 because it found no files to inspect is **itself a violation**.
The `--self-test` mode is mandatory in CI: it asserts that the scanner
correctly REJECTS three synthetic fixtures (complete-inventory passes;
missing-`18-schema.sql` fails; locked-vacant slot 11 occupied fails).

## 5-link self-enforcement chain (A-44 template)

1. **AC text** — spec/22 §97 AC-78 + AC-22-LV1 (canonical contract).
2. **Fixture surface** — synthetic in-memory tempdirs created by `--self-test`
   (no on-disk corpora needed; faster than fixture trees).
3. **Script** — `linter-scripts/check-spec22-inventory.py` (this slot).
4. **`--self-test`** — built-in mode, runs 3 negative fixtures.
5. **Workflow step** — `.github/workflows/spec-health.yml` "§22 module asset
   inventory gate" hard-fails CI on any violation.
6. **§00 Walker-Pin row** — spec/22 `00-overview.md` Walker-Pin block carries
   a row citing this slot + gate #20 + workflow step name (Sess-56 A-49).

## History

- **Sess-56 A-48** — slot created. Built-in self-test only (no on-disk
  fixture corpus needed because the inventory check is a pure file-existence
  predicate; in-memory tempdirs suffice).
