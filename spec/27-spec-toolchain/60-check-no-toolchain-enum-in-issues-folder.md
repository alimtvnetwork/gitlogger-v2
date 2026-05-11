# Slot 60 — `check-no-toolchain-enum-in-issues-folder.py`

**Status:** Active gate #38 (Phase-5 T-31)
**Implements:** §25 §00 boundary contract (no toolchain-enum surface) + §25 §97 AC-AI-* scope-lock + locked-7 scope-lock memory invariant + §27 §00 single-source-of-truth-for-toolchain-enumeration claim (closes §27 backlog `no-toolchain-enum-in-issues-folder-check` minted Phase-5 T-09)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§25 no-toolchain-enum boundary gate"

## Contract

Walks every `.md` under `spec/25-app-issues/` and asserts the §25
folder owns ZERO toolchain-enumeration surface — single source of
truth for the linter-script roster + CI gate enumeration is §27
(`00-overview.md` Inventory + Slot Delegation Map + §97
gate-enumeration table). The §25 folder owns issue-audit content
(findings, severities, AC traces) and MAY cite individual gate
names in prose / table cells / backtick spans, but MUST NOT carry
**parallel enumerations** of the gate roster, slot-number range
table, or `linter-scripts/` directory listing. Closes §27 backlog
`no-toolchain-enum-in-issues-folder-check` (the third of 4
boundary-quartet gates). Fails CI when ANY of the following
invariants fail:

1. **No gate-enumeration table** — no `.md` under
   `spec/25-app-issues/` may contain a Markdown table whose header
   row matches the §27 §00 gate enumeration shape: a header row
   containing `Gate` (or `gate #`) AND `Slot` (or `slot`) AND any
   of `Workflow step`/`Status`/`Check` columns, OR a table whose
   body contains ≥3 rows each starting `| #NN |` with `gate #`
   numeric tokens. Hit fails clause-1 with offending file:line +
   matched header tokens. Single-row finding-evidence tables that
   reference ONE gate by name are PERMITTED.
2. **No `linter-scripts/` directory listing** — no `.md` under
   §25 may contain a fenced block (any language) OR a bullet list
   of ≥4 consecutive items each matching
   `linter-scripts/[a-z][a-z0-9-]*\.py` enumerating the script
   roster. Single-script citations in prose (e.g.
   `` `linter-scripts/check-error-envelope-uniformity.py` ``) are
   PERMITTED — the gate fires only on **enumeration shape** (≥4
   consecutive script paths). Tree fences (` ```text ` showing a
   directory tree containing the `linter-scripts/` node and ≥4
   children) also fail.
3. **No slot-number range table** — no `.md` under §25 may
   contain a table whose header row contains `Range` AND
   `Purpose` (matching the §27 §00 Inventory range table shape:
   `01-09`/`10-19`/`20-29`/`30-39`/`40-49`/`50-59`/`60-69`/`70-79`/
   `90-99`), OR a bullet list of ≥3 consecutive items each
   matching the pattern `\d{2}-\d{2}` followed by a colon /
   em-dash / "—" range descriptor. Single-row references citing
   ONE slot range in narrative prose are PERMITTED.
4. **AC-finding cross-refs to single gate names are exempt** —
   §25 findings (`### AC-AI-NN`) frequently cite §27 gate names
   (e.g. `check-error-envelope-uniformity`) and slot numbers
   (e.g. `slot 45`) one-at-a-time. These cross-refs MUST be
   PERMITTED — the gate MUST NOT flag gate-name tokens or single
   slot-number tokens that appear inside backtick spans inside
   `### AC-AI-*` heading sections, NOR inside table cells whose
   row references a single gate / slot. Clause-4 is a positive
   guarantee — failing to honour the exemption produces a
   false-positive and fails the gate's own self-test (F-5).
5. **§25 §00 boundary declaration present** —
   `spec/25-app-issues/00-overview.md` MUST contain the literal
   substring `Toolchain enumeration is owned exclusively by §27`
   (or canonical equivalent
   `single source of truth for the gate roster is §27`) within a
   normative block, AND the literal `Self-enforcing via §27
   backlog gate \`no-toolchain-enum-in-issues-folder-check\``.
   Stripping either literal fails clause-5 (Lesson #15
   reflexivity break).
6. **Scope-lock memory invariant cite** — slot 60 doc Section
   "Bindings" MUST cite `mem://constraints/spec-scope` —
   confirms this gate is the third of 4 on-disk mechanizations
   of the scope-lock rule (boundary quartet 3/4).

## Invocation

```bash
python3 linter-scripts/check-no-toolchain-enum-in-issues-folder.py --check all
python3 linter-scripts/check-no-toolchain-enum-in-issues-folder.py --check no-gate-enum-table
python3 linter-scripts/check-no-toolchain-enum-in-issues-folder.py --check no-script-roster
python3 linter-scripts/check-no-toolchain-enum-in-issues-folder.py --check no-slot-range-table
python3 linter-scripts/check-no-toolchain-enum-in-issues-folder.py --check ac-finding-exemption
python3 linter-scripts/check-no-toolchain-enum-in-issues-folder.py --check boundary-declaration
python3 linter-scripts/check-no-toolchain-enum-in-issues-folder.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if ≥1 `.md` was scanned under §25, the §25 §00
boundary declaration was located (clause-5 anchor), AND the
AC-finding exemption (clause-4) was exercised against ≥1
`### AC-AI-*` section that mentions a §27 gate name OR slot
number in a backtick span. Zero anchors → exit `1` with
`vacuous-pass: §25 has zero .md files / §25 §00 boundary
declaration absent / no ### AC-AI-* section referencing a §27
gate name or slot number in a backtick span (clause-4 exemption
never exercised — gate cannot prove its exemption logic is
wired)`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-clean (§25 §00 carries boundary declaration +
  gate self-citation; ≥1 `### AC-AI-NN` finding cites
  `\`check-error-envelope-uniformity\`` + `slot 45` in backtick
  spans; no enumerations anywhere) → passes
- **F-2** §25 child `06-gate-roster.md` carries a markdown table
  with header `| Gate | Slot | Workflow step | Status |` and
  ≥3 body rows enumerating gates → fails clause-1
- **F-3** §25 child carries a bullet list of 5 consecutive
  `linter-scripts/check-*.py` paths → fails clause-2
- **F-4** §25 child carries a Range/Purpose table mirroring the
  §27 §00 Inventory range table → fails clause-3
- **F-5** Gate flags `\`check-error-envelope-uniformity\``
  inside an `### AC-AI-NN` finding's backtick span (clause-4
  exemption breaks — false-positive) → exposed via F-5 as a
  regression test for the exemption
- **F-6** §25 §00 strips `Self-enforcing via §27 backlog gate
  \`no-toolchain-enum-in-issues-folder-check\`` literal → fails
  clause-5 (Lesson #15 reflexivity break)

## 5-link self-enforcement chain

1. **AC text** — §25 §00 boundary declaration block (carries
   gate self-citation per clause-5); §25 §97 AC-AI-* family
   scope-lock; §27 §00 single-source-of-truth-for-toolchain-
   enumeration claim; §27 backlog
   `no-toolchain-enum-in-issues-folder-check` (Phase-5 T-09).
2. **Fixture surface** — synthetic in-memory tempdirs created
   by `--self-test` (6 short Markdown blobs).
3. **Script** — `linter-scripts/check-no-toolchain-enum-in-issues-folder.py`.
4. **`--self-test`** — built-in mode, 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§25 no-toolchain-enum boundary gate" hard-fails CI.
6. **§00 Walker-Pin row** — §25 §00 Walker-Pin block gains a
   row citing slot 60 + gate #38 + workflow step name
   (deferred to next §25 §00 touch).

## Bindings

- **`mem://constraints/spec-scope`** (locked-7 scope-lock
  memory invariant) — slot 60 is the **third** of 4
  boundary-quartet gates (slots 58/59/60/61) that collectively
  mechanize the scope-lock rule on disk. Slot 58 closed §24
  no-DDL boundary; slot 59 closed §25 no-CI-yaml; slot 60
  closes §25 no-toolchain-enum; slot 61 closes the locked-7
  perimeter.
- **§27 backlog ticket `no-toolchain-enum-in-issues-folder-check`**
  — closes this turn (T-31). Minted Phase-5 T-09 alongside the
  boundary-quartet batch; paper-only for 20 cycles.
- **AC-AI-* family** (§25 audit ACs) — gate #46
  (`check-audit-quoted-evidence-marker`) covers audit-quoting
  discipline INSIDE §25; gate #37 covers no-CI-yaml; gate #38
  covers no-toolchain-enum. Together the §25 boundary triplet
  enforces audit-only surface shape: no executable CI, no
  parallel toolchain enumeration.
- **§27 §00 Inventory + Slot Delegation Map + §97 gate
  enumeration** — single source of truth for the gate roster /
  slot range / script directory. Gate #38 enforces the
  no-competing-enumeration side of that claim by making it a
  CI failure to introduce a parallel roster / range / directory
  listing in §25.
- **Lesson #15 reflexivity** — clause-5 enforces gate name
  remains in §25 §00 boundary declaration block.
- **Slots 58 / 59 siblings** — boundary-quartet pattern reuse
  (boundary-declaration + Lesson #15 self-citation + R5
  exemption-exercised proof).

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-60/`) and run `python3 linter-scripts/check-no-toolchain-enum-in-issues-folder.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #38 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/check-no-toolchain-enum-in-issues-folder.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #38 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## Scorecard impact (Rubric v2 /120)
- **§25** — C4 (Consistency) +1 (boundary now load-proven —
  no smuggled toolchain enumeration in issues folder); C5
  (Implementability) +1 (cite mechanism is gate #38 — issues
  contributor can prove their changes don't violate the
  boundary by running the gate); C6 (Friction) +1 (paper-only
  T-09 backlog ticket retires). §25 advances Lovable 119 →
  120, Cursor 118 → 119, Raw-LLM 113 → 115. §25 reaches the
  120/120 ceiling for Lovable persona.
- **§27** — C6 +1 (boundary-quartet 3 of 4 closed).
- **§28** — C4 +1 (single-source-of-truth-for-toolchain claim
  now bidirectionally enforced — §27 owns the enumeration,
  §28 owns the universal CI CLI, §25 cannot compete).

## Out of scope

- Gate roster in §27 (`spec/27-spec-toolchain/00-overview.md`
  Inventory + §97 gate enumeration — explicitly the source of
  truth, not the boundary).
- Toolchain enumeration in §28 (`spec/28-universal-ci-cli/`
  owns the universal CI CLI surface — explicitly permitted).
- Single-gate citations in §25 prose (gate name in backtick
  span, single slot reference) — gate scope is **enumeration
  shape** only (≥3-row tables, ≥4-item script lists, ≥3-item
  range lists).
- Code fences in other languages (JSON, TypeScript, SQL) —
  unrestricted in §25 except where covered by sibling boundary
  gates (gate #37 CI YAML, future gate #36 sibling DDL).
- §24 / §26 / §27 / §28 boundary contracts — covered by
  sibling slots 58 / 59 / 61.
