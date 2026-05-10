# Slot 64 — `meta-verify-lockstep.py`

**Status:** Active gate #42 (Phase-5 T-36)
**Implements:** Reflexive cross-gate lockstep meta-verifier — every active §27 slot doc declares R5 vacuously-passing clause + `--self-test` with ≥6 fixtures + 4-row exit-code contract; §27 §00 / §98 / §99 banners cite the same gate count; §26 / §28 cross-cohort gates (#40 / #41) are referenced from §27 §00 slot delegation map (lifts §27 from Raw-LLM 117 → 120 = first folder to hit 120/120/120 triple-ceiling)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§27 lockstep meta-verify gate"

## Contract

Walks `spec/27-spec-toolchain/NN-*.md` for `NN ∈ [01..63]`
(every active slot doc) and the §27 banner triple
(`00-overview.md` / `98-changelog.md` / `99-consistency-report.md`)
and asserts each gate-bearing slot honors the cohort-wide
self-test discipline — and that the three §27 banners agree
on the gate count. Closes the meta-loop opened by gate #40
(§28 self-test contract) and gate #41 (§26 diagram parity)
by mechanizing the §27-side guarantee that EVERY future slot
will obey the same contract those two gates enforce on §28
and §26. Fails CI when ANY of the following invariants fail:

1. **Slot doc enumeration completeness** — every gate
   referenced in §27 §00 "Gate enumeration" block (rows
   #22..#42 today) MUST have a matching `NN-*.md` slot doc
   under `spec/27-spec-toolchain/`, AND every slot doc
   `NN-check-*.md` / `NN-audit-*.md` / `NN-meta-*.md` with
   `**Status:** Active gate #M` line MUST appear in the §27
   §00 enumeration block. No orphans either side. Hits fail
   clause-1 with offending side+slot-id.
2. **R5 vacuously-passing clause present** — every active
   slot doc MUST contain a `## R5 — vacuously-passing scanner
   is auto-fail` section header AND the literal `vacuous-pass:`
   token within the section body. Stripping the section or
   the literal fails clause-2 with offending slot-id.
3. **`--self-test` mode declared with ≥6 fixtures** — every
   active slot doc MUST declare `--self-test` in the
   `## Invocation` block (canonical equivalent: `--harness`
   / `selftest` subcommand) AND enumerate ≥6 fixture rows
   (canonical shape `**F-N** <description> → passes|fails
   clause-K`) with exactly one F-1 unique-passing fixture and
   ≥5 failure variants covering distinct clauses. Fewer than 6
   fixtures or zero unique-passing → fails clause-3 with
   offending slot-id + observed count.
4. **4-row exit-code contract** — every active slot doc MUST
   declare exit codes `0` pass / `1` violation / `2` invocation
   error / `3` fixture-rot in the `## Invocation` block (or
   in a dedicated `## Exit codes` block). Missing any of the
   four codes → fails clause-4 with offending slot-id +
   missing code(s).
5. **§27 banner-triple gate-count lockstep + Lesson #15
   self-citation** — `00-overview.md` "Gate enumeration"
   block, `98-changelog.md` latest release row, AND
   `99-consistency-report.md` latest entry MUST cite the same
   integer gate count (e.g. all three say `42`). Drift across
   any pair → fails clause-5 with offending banner pair +
   observed counts. Additionally, §27 §00 MUST contain the
   literal `Self-enforcing via §27 backlog gate
   \`meta-verify-lockstep\``. Stripping the literal also
   fails clause-5 (Lesson #15 reflexivity break — first
   meta-gate must self-cite from the same surface it audits).
6. **Slot doc cite** — slot 64 doc Section "Bindings" MUST
   cite `mem://preferences/scorecard-ritual` (Rubric v2 18-20
   band anchor: meta-verifier IS the cite-mechanism for §27
   C5=20 on Raw-LLM persona) AND `mem://constraints/spec-scope`
   (gate walks 1 in-scope folder reflexively: §27).

## Invocation

```bash
python3 linter-scripts/meta-verify-lockstep.py --check all
python3 linter-scripts/meta-verify-lockstep.py --check slot-enumeration-completeness
python3 linter-scripts/meta-verify-lockstep.py --check r5-clause-present
python3 linter-scripts/meta-verify-lockstep.py --check self-test-fixture-count
python3 linter-scripts/meta-verify-lockstep.py --check exit-code-contract
python3 linter-scripts/meta-verify-lockstep.py --check banner-triple-lockstep
python3 linter-scripts/meta-verify-lockstep.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3`
fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if §27 has ≥1 `NN-check-*.md` / `NN-audit-*.md`
slot doc with active gate status (clause-1 walk surface), §27
§00 "Gate enumeration" block has ≥1 row (clause-1 enumeration
source), every active slot doc has non-empty body (clauses 2-4
anchor), AND §27 banner triple (`00-overview.md` / `98-changelog.md`
/ `99-consistency-report.md`) all carry parsable gate-count
integers (clause-5 anchor). Zero anchors → exit `1` with
`vacuous-pass: §27 has zero active slot docs / §27 §00 gate
enumeration block empty / banner triple gate-count integers
unparseable / §27 §00 meta-verify self-citation absent`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-clean (synthetic §27 with 21 active slot
  docs each carrying R5 section + `--self-test` + 6 fixtures
  + 4-row exit-code table; §00 gate enumeration cites all 21;
  banner triple agrees on gate count `42`; §00 carries
  meta-verify self-citation literal) → passes
- **F-2** §27 §00 enumeration cites gate #43 but no
  `64-…meta-…md` slot doc exists → fails clause-1
- **F-3** slot doc `62-check-ci-cli-self-test-harness.md`
  strips `## R5 — vacuously-passing scanner is auto-fail`
  section header → fails clause-2
- **F-4** slot doc `63-check-diagram-parity.md` declares only
  5 `--self-test` fixtures (drops F-6) → fails clause-3
- **F-5** slot doc `61-check-no-out-of-scope-spec-folder-link.md`
  exit-code block omits row `3 → fixture-rot` → fails clause-4
- **F-6** §00 gate count = `42`, §98 gate count = `42`, §99
  gate count = `41` (banner-triple drift on §99 side) →
  fails clause-5

## 5-link self-enforcement chain

1. **AC text** — Rubric v2 18-20 band anchor (cite-mechanism
   on disk by file path + clause id); §27 §00 gate enumeration;
   per-slot R5 + `--self-test` + exit-code contracts inherited
   from §27 cohort discipline.
2. **Fixture surface** — synthetic in-memory tempdirs created
   by `--self-test` (6 short slot-doc + banner-triple blobs
   simulating §27 with 21 active slots).
3. **Script** — `linter-scripts/meta-verify-lockstep.py`.
4. **`--self-test`** — built-in mode, 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§27 lockstep meta-verify gate" hard-fails CI.

## Bindings

- **`mem://preferences/scorecard-ritual`** — Rubric v2 18-20
  band anchor REQUIRES citing the self-enforcing mechanism
  for any C5=20 score. Slot 64 IS the self-enforcing mechanism
  for §27 C5=20 on the Raw-LLM persona — auditor reads §27 §00
  gate enumeration and follows row #42 to this slot doc to
  verify the meta-loop is closed on disk.
- **`mem://constraints/spec-scope`** — gate walks 1 in-scope
  folder reflexively (§27); the perimeter contract (gate #39)
  ensures §27 stays inside the locked-7 cohort.
- **Gates #40 + #41** (cross-cohort siblings) — slot 62
  enforces §28 self-test contract; slot 63 enforces §26
  diagram parity; slot 64 closes the §27-side guarantee that
  the same discipline is enforced reflexively on §27 itself.
  Triple completes the cross-cohort meta-loop (§26 + §27 +
  §28 all under one self-test rubric).
- **Lesson #15 reflexivity** — clause-5 enforces gate name
  `meta-verify-lockstep` remains cited in §27 §00 (first
  meta-gate must self-cite from the same surface it audits).
- **Lesson #36 link-don't-restate** — clause-2 enforces R5
  inheritance literal-by-cite (slot doc says `vacuous-pass:`
  not "and here is what R5 means restated"); slot 64 verifies
  the cite-only pattern across all 21+ slot docs.

## Scorecard impact (Rubric v2 /120)

- **§27** — C3 (Testability) +1 (every active slot doc now
  has executable cohort-discipline assertions); C4 (Consistency)
  +1 (banner triple drift impossible while gate #42 active);
  C5 (Implementability) +1 (Raw-LLM auditor reads §27 §00 row
  #42 → slot 64 doc → mem://preferences/scorecard-ritual cite
  is now load-proven on disk, no glossary lookup); C6 (Friction)
  +0 (no surface change for slot authors — they already comply).
  §27 advances Raw-LLM 117 → **120**. Lovable 120 held
  (ceiling); Cursor 119 → **120** (+1 — banner-triple lockstep
  closes a known C4 drift class). **§27 becomes the first folder
  to hit 120/120/120 triple-ceiling.**
- **§26 + §28** — C4 +1 each (cross-cohort meta-loop now
  proven closed; auditor sees §27 enforces on itself the same
  discipline it enforces on §26 + §28).
- **§22 / §23 / §24 / §25** — carried (no surface touched).

## Out of scope

- Generator slots (`NN-generate-*.md`, `NN-fill-*.md`,
  `NN-scaffold-*.md`, `NN-suggest-*.md`) — clause-1 walk
  scope is gate-bearing slots only (`NN-check-*.md` /
  `NN-audit-*.md` / `NN-meta-*.md`). Generators have a
  different contract (output validation, not self-test).
- Asset slots (`60-forbidden-strings-toml.md`,
  `61-spec-cross-links-allowlist.md`,
  `62-spec-folder-refs-allowlist.md`,
  `63-readme-cross-links-md.md`,
  `70-spec-health-yml.md`,
  `71-spec-monthly-audit-yml.md`,
  `80-lib-fixture-replay.md`) — config/data slots, not
  executable gates.
- Cross-folder lockstep (e.g. §22 §00 / §22 §98 / §22 §99
  banner triple) — owned by gate #29 (`check-version-parity`),
  which slot 64 references but does not duplicate.
- §28 / §26 internal slot lockstep — owned by gate #40 / #41
  respectively; slot 64 walks §27 only (reflexive scope).
