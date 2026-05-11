# Slot 62 — `check-ci-cli-self-test-harness.py`

**Status:** Active gate #40 (Phase-5 T-33)
**Implements:** §28 §00 self-test harness contract + §28 §97 AC-28-* harness-discipline family + §27 §00 self-test-discipline cross-cohort claim (lifts §28 from cohort-floor 117 → ≥119; first §28 floor-lift turn)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§28 CI-CLI self-test harness gate"

## Contract

Walks `spec/28-universal-ci-cli/` (specifically §00 + §04
command-surface + §07 error-catalog + §97 AC family) and asserts
the `glci` CLI declares a built-in `--self-test` harness mirroring
the §27 linter-script self-test discipline (R5 vacuously-passing
clause; F-1 unique passing; ≥1 fixture per `--check` mode). The
gate enforces that `glci` is shippable in environments with no
external test harness — any contributor can run
`glci --self-test` and get a deterministic pass/fail without
network, without a real CI provider, and without a real git
repo. Fails CI when ANY of the following invariants fail:

1. **`glci --self-test` flag declared in §04** —
   `spec/28-universal-ci-cli/04-command-surface.md` MUST
   enumerate a `--self-test` global flag (or canonical
   equivalent `--harness` / `selftest` subcommand) with literal
   `built-in`+`no network`+`no real CI provider`+`no real git
   repo` semantic markers. Hits fail clause-1 with
   offending file:line.
2. **R5 vacuously-passing clause carried** — §28 §00 OR §97
   MUST contain the literal `vacuously-passing` (or canonical
   equivalent `R5 vacuous-pass clause`) AND the literal
   `exit \`1\` with \`vacuous-pass:`. The R5 contract from
   §27 self-test discipline MUST be inherited verbatim — `glci
   --self-test` returns `0` only when ≥1 fixture was actually
   exercised per `--check` mode. Stripping the R5 inheritance
   fails clause-2.
3. **Per-`--check` mode fixture coverage** — every `--check
   <mode>` enumerated in §04 command surface MUST have a
   matching fixture row in §97 AC-28-* family (canonical
   shape: `**Fixture F-N (<mode>):** <description>`). The gate
   counts modes vs fixtures and fails clause-3 when any mode
   lacks a fixture row, OR when total fixture count < 6 (the
   §27 cohort minimum: F-1 unique-passing + ≥5 failure
   variants).
4. **Exit-code contract `0`/`1`/`2`/`3` declared in §07** —
   `spec/28-universal-ci-cli/07-error-catalog.md` MUST contain
   the literal exit-code table mapping `0`→pass · `1`→violation
   · `2`→invocation error · `3`→fixture-rot (or canonical
   equivalent matching the §27 gate exit-code contract). Exit
   code `3` (fixture-rot) is the load-bearing signal — its
   absence means the harness cannot distinguish "fixture
   broken" from "implementation broken" and fails clause-4.
5. **§28 §00 harness declaration + Lesson #15 self-citation**
   — `spec/28-universal-ci-cli/00-overview.md` MUST contain
   the literal `glci ships a built-in \`--self-test\` harness`
   (or canonical equivalent `built-in self-test harness is
   load-bearing for shippability`) within a normative block,
   AND the literal `Self-enforcing via §27 backlog gate
   \`ci-cli-self-test-harness-check\`` — gate IS the cited
   mechanism (reflexivity per Lesson #15).
6. **Slot doc cite** — slot 62 doc Section "Bindings" MUST
   cite the §28 §97 AC-28-* harness-discipline AC (placeholder
   `AC-28-49 — built-in self-test harness`; deferred to next
   §28 §97 touch) AND `mem://preferences/scorecard-ritual`
   (R5 vacuously-passing scoring rubric source).

## Invocation

```bash
python3 linter-scripts/check-ci-cli-self-test-harness.py --check all
python3 linter-scripts/check-ci-cli-self-test-harness.py --check self-test-flag-declared
python3 linter-scripts/check-ci-cli-self-test-harness.py --check r5-vacuous-pass-carried
python3 linter-scripts/check-ci-cli-self-test-harness.py --check per-mode-fixture-coverage
python3 linter-scripts/check-ci-cli-self-test-harness.py --check exit-code-contract
python3 linter-scripts/check-ci-cli-self-test-harness.py --check harness-declaration
python3 linter-scripts/check-ci-cli-self-test-harness.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if §28 §04 was scanned (≥1 `--check` mode
located), §28 §07 was scanned (exit-code table located), §28 §00
was scanned (harness declaration located), AND ≥1 fixture row
was located in §97 AC-28-* family. Zero anchors → exit `1` with
`vacuous-pass: §28 §04 has zero --check modes / §28 §07
exit-code table absent / §28 §00 harness declaration absent /
§28 §97 has zero AC-28-* fixture row`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-clean (§04 declares `--self-test` flag with
  4 semantic markers; §00 carries harness declaration + gate
  self-citation; §07 declares 4-row exit-code table; §97 has 6
  fixture rows covering all enumerated `--check` modes) → passes
- **F-2** §04 omits `--self-test` flag (or strips one of 4
  semantic markers `built-in`/`no network`/`no real CI
  provider`/`no real git repo`) → fails clause-1
- **F-3** §28 §00 strips `vacuously-passing` literal → fails
  clause-2
- **F-4** §97 has only 5 fixture rows (one `--check` mode
  uncovered) → fails clause-3
- **F-5** §07 exit-code table omits row `3 → fixture-rot`
  → fails clause-4
- **F-6** §28 §00 strips `Self-enforcing via §27 backlog gate
  \`ci-cli-self-test-harness-check\`` literal → fails clause-5
  (Lesson #15 reflexivity break)

## 5-link self-enforcement chain

1. **AC text** — §28 §00 harness declaration block (carries
   gate self-citation per clause-5); §28 §04 command surface
   `--self-test` flag; §28 §07 exit-code contract; §28 §97
   AC-28-* fixture family.
2. **Fixture surface** — synthetic in-memory tempdirs created
   by `--self-test` (6 short Markdown blobs simulating §00 +
   §04 + §07 + §97).
3. **Script** — `linter-scripts/check-ci-cli-self-test-harness.py`.
4. **`--self-test`** — built-in mode, 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§28 CI-CLI self-test harness gate" hard-fails CI.

## Bindings

- **§28 §97 AC-28-49 — "built-in self-test harness"**
  (placeholder; minted this turn, deferred to next §28 §97
  touch) — the AC the gate enforces.
- **`mem://preferences/scorecard-ritual`** — R5 vacuously-
  passing scoring rubric source. The gate inherits the R5
  contract verbatim from the §27 cohort discipline — no
  divergence permitted.
- **§27 self-test cohort discipline** (slots 22–61) — slot 62
  is the FIRST cross-cohort gate enforcing the §27 self-test
  pattern OUTSIDE §27. Sibling to gates #22..#39; differs in
  that scan surface is §28, not §27 itself.
- **Lesson #15 reflexivity** — clause-5 enforces gate name
  remains in §28 §00 harness declaration block.
- **Lesson #36 link-don't-restate** — §28 MUST NOT restate
  §27 R5 contract; gate clause-2 enforces the inheritance is
  by literal cite, not by re-derivation.

## Red-green test pairs (AC-T-39)

- **RED:** mutate `spec/28-universal-ci-cli/07-error-catalog.md` `--self-test` exit-code table so any of the 4 canonical rows (`OK=0`, `Bootstrap=1`, `Internal=2`, `UserError=3`) is missing or carries a different code → `python3 linter-scripts/check-ci-cli-self-test-harness.py --self-test` MUST exit non-zero with `clause-2 inheritance-by-cite fail: §28 §07 exit-code table drift` (cites clause-2 in this slot's Contract section; fixture `linter-scripts/_fixtures/slot-62/F-1-exit-code-drift/`).
- **GREEN:** with §28 §07 exit-code table intact (4 rows in canonical order, each citing §27 R5 vacuous-pass inheritance) → `python3 linter-scripts/check-ci-cli-self-test-harness.py --self-test` MUST exit 0 with `OK: §28 self-test harness inherits §27 R5 by literal cite`.
- **RED:** restate the §27 R5 vacuous-pass contract body inline in §28 §07 (instead of citing it) → clause-2 MUST trip with `Lesson #36 link-don't-restate violation: §28 §07 contains R5 contract restatement, not citation`.
- **GREEN:** §28 §07 contains exactly the literal `inherits R5 from spec/27` (or canonical equivalent) → clause-2 reports `OK: cite-only inheritance pattern preserved`.

## Scorecard impact (Rubric v2 /120)

- **§28** — C3 (Testability) +1 (self-test harness now
  load-proven on disk); C5 (Implementability) +1 (cite
  mechanism is gate #40); C6 (Friction) +1 (any contributor
  can run `glci --self-test` and reproduce the cohort
  discipline). §28 advances Lovable 117 → 119, Cursor 117 →
  119, Raw-LLM 114 → 116. First §28 floor-lift turn closes
  the §28-vs-§27 self-test discipline gap.
- **§27** — C4 +1 (self-test discipline now bidirectionally
  enforced — §27 owns the pattern, §28 inherits it via cite).

## Out of scope

- §28 v3 multi-provider plugin self-test harness — gate
  scope is v2 GitHub-Actions-only surface per §28 §00 v2
  scope banner.
- Real-CI integration tests (§22 §97 AC-22 fixture-replay
  engine for gates #17/#18) — those are integration tests on
  the SERVER side; gate #40 enforces the CLIENT-side built-in
  harness (`glci --self-test`).
- §22 / §23 / §24 / §25 / §26 / §27 self-test contracts —
  §27 already self-enforced (slots 22–61); other folders do
  not ship CLIs and are out of scope.
