# Slot 59 — `check-no-ci-yaml-in-issues-folder.py`

**Status:** Active gate #37 (Phase-5 T-30)
**Implements:** §25 §00 boundary contract (no CI yaml surface) + §25 §97 AC-AI-* scope-lock + locked-7 scope-lock memory invariant + §27 §00 single-source-of-truth-for-CI-workflows claim (closes §27 backlog `no-ci-yaml-in-issues-folder-check` minted Phase-5 T-09)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§25 no-CI-yaml boundary gate"

## Contract

Walks every `.md` under `spec/25-app-issues/` and asserts the §25
folder owns ZERO CI workflow surface — single source of truth for
CI-runner spec is §27 (`linter-scripts/` + `.github/workflows/`)
and §28 (universal CI CLI). The §25 folder owns issue-audit
content (findings, severities, AC traces) and MAY mention CI
gates in prose but MUST NOT carry executable CI workflow YAML.
Closes §27 backlog `no-ci-yaml-in-issues-folder-check` (the
second of 4 boundary-quartet gates). Fails CI when ANY of the
following invariants fail:

1. **No CI YAML fences in §25** — no `.md` under
   `spec/25-app-issues/` may contain a fence opened with
   ` ```yaml ` or ` ```yml ` whose body matches the CI-workflow
   shape detector: contains the literal token `runs-on:` OR
   `uses: actions/` OR `jobs:` (top-level key) OR
   `on: push` / `on: pull_request` / `on: schedule`. Hit fails
   clause-1 with offending file:line + matched token. Plain
   YAML fences without CI-workflow tokens (e.g. config-shape
   examples) are PERMITTED.
2. **No `.yml` / `.yaml` path references claimed authoritative**
   — no `.md` under §25 may contain a path reference matching
   `spec/25-…/(workflows|ci|github)/.*\.ya?ml` or claim
   ownership of `.github/workflows/*.yml` files. References to
   §27-owned workflow filenames (e.g. `spec-health.yml`) in
   prose are PERMITTED only inside backtick spans AND only as
   READ references (not as authoritative ownership claims —
   detected by adjacent verb `owned by §25`, `defined in §25`,
   `ships from §25`).
3. **No bare CI keywords in unfenced prose** — no `.md` under
   §25 may contain unfenced literal substrings
   `runs-on: ubuntu-latest`, `uses: actions/checkout@`,
   `jobs:\n  ` (with trailing newline+2-space indent),
   `on:\n  push:`, or `on:\n  pull_request:`. Bare CI keywords
   in prose suggest an attempt to smuggle a workflow without a
   fence. Backticked single-token references like `\`runs-on\``
   (without trailing literal-value structure) are exempt.
4. **AC-finding cross-refs to CI gates are exempt** — §25
   findings (`### AC-AI-NN`) frequently cite §27 gate names
   (e.g. `check-error-envelope-uniformity`) and §27 workflow
   step names (e.g. "§22+§23 dialect-precedence banner gate").
   These cross-refs MUST be PERMITTED — the gate MUST NOT flag
   gate-name tokens that appear inside markdown table cells
   (rows starting with `|`) or inside backtick spans inside
   `### AC-AI-*` heading sections. Clause-4 is a positive
   guarantee — failing to honour the exemption produces a
   false-positive and fails the gate's own self-test (F-1).
5. **§25 §00 boundary declaration present** — `spec/25-app-issues/00-overview.md`
   MUST contain the literal substring `CI-workflow YAML is
   owned exclusively by §27` (or canonical equivalent
   `single source of truth for CI workflows is §27 + §28`)
   within a normative block, AND the literal `Self-enforcing
   via §27 backlog gate \`no-ci-yaml-in-issues-folder-check\``.
   Stripping either literal fails clause-5 (Lesson #15
   reflexivity break).
6. **Scope-lock memory invariant cite** — slot 59 doc Section
   "Bindings" MUST cite `mem://constraints/spec-scope` —
   confirms this gate is the second of 4 on-disk mechanizations
   of the scope-lock rule (boundary quartet 2/4).

## Invocation

```bash
python3 linter-scripts/check-no-ci-yaml-in-issues-folder.py --check all
python3 linter-scripts/check-no-ci-yaml-in-issues-folder.py --check no-ci-yaml-fences
python3 linter-scripts/check-no-ci-yaml-in-issues-folder.py --check no-authoritative-yml-paths
python3 linter-scripts/check-no-ci-yaml-in-issues-folder.py --check no-bare-ci-keywords
python3 linter-scripts/check-no-ci-yaml-in-issues-folder.py --check ac-finding-exemption
python3 linter-scripts/check-no-ci-yaml-in-issues-folder.py --check boundary-declaration
python3 linter-scripts/check-no-ci-yaml-in-issues-folder.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3`
fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if ≥1 `.md` was scanned under §25, the §25 §00
boundary declaration was located (clause-5 anchor), AND the
AC-finding exemption (clause-4) was exercised against ≥1
`### AC-AI-*` section that mentions a §27 gate name in a
backtick span. Zero anchors → exit `1` with `vacuous-pass: §25
has zero .md files / §25 §00 boundary declaration absent / no
### AC-AI-* section referencing a §27 gate name in a backtick
span (clause-4 exemption never exercised — gate cannot prove
its exemption logic is wired)`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-clean (§25 §00 carries boundary declaration +
  gate self-citation; ≥1 `### AC-AI-NN` finding cites
  `\`check-error-envelope-uniformity\`` in backtick span; no
  CI-workflow YAML fences anywhere) → passes
- **F-2** §25 child `06-ci-mirror.md` opens a ` ```yaml ` fence
  with `jobs:\n  test:\n    runs-on: ubuntu-latest` → fails
  clause-1
- **F-3** §25 child references `spec/25-…/workflows/audit.yml`
  as authoritative (`workflow defined in §25 ships from §25`)
  → fails clause-2
- **F-4** §25 child carries unfenced prose
  `Trigger with on:\n  push:\n    branches: [main]` → fails
  clause-3
- **F-5** Gate flags `\`check-error-envelope-uniformity\``
  inside an `### AC-AI-NN` finding's backtick span (clause-4
  exemption breaks — false-positive) → exposed via F-5 as a
  regression test for the exemption
- **F-6** §25 §00 strips `Self-enforcing via §27 backlog gate
  \`no-ci-yaml-in-issues-folder-check\`` literal → fails
  clause-5 (Lesson #15 reflexivity break)

## 5-link self-enforcement chain

1. **AC text** — §25 §00 boundary declaration block (carries
   gate self-citation per clause-5); §25 §97 AC-AI-* family
   scope-lock; §27 §00 single-source-of-truth-for-CI-workflows
   claim; §27 backlog `no-ci-yaml-in-issues-folder-check`
   (Phase-5 T-09).
2. **Fixture surface** — synthetic in-memory tempdirs created
   by `--self-test` (6 short Markdown blobs).
3. **Script** — `linter-scripts/check-no-ci-yaml-in-issues-folder.py`.
4. **`--self-test`** — built-in mode, 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§25 no-CI-yaml boundary gate" hard-fails CI.
6. **§00 Walker-Pin row** — §25 §00 Walker-Pin block gains a
   row citing slot 59 + gate #37 + workflow step name
   (deferred to next §25 §00 touch).

## Bindings

- **`mem://constraints/spec-scope`** (locked-7 scope-lock
  memory invariant) — slot 59 is the **second** of 4
  boundary-quartet gates (slots 58/59/60/61) that collectively
  mechanize the scope-lock rule on disk. Slot 58 closed §24
  no-DDL boundary; slot 59 closes §25 no-CI-yaml; slot 60
  closes §25 no-toolchain-enum; slot 61 closes the locked-7
  perimeter.
- **§27 backlog ticket `no-ci-yaml-in-issues-folder-check`** —
  closes this turn (T-30). Minted Phase-5 T-09 alongside the
  boundary-quartet batch; paper-only for 19 cycles.
- **AC-AI-* family** (§25 audit ACs) — gate #46 (`check-audit-
  quoted-evidence-marker`) covers the audit-quoting discipline
  inside §25; gate #37 covers the no-CI-yaml boundary OUTSIDE
  the audit content. Together they enforce the §25 surface
  shape: audit-only, no executable CI surface.
- **§27 §00 + §28 §00** — single source of truth for CI
  workflows. Gate #37 enforces the no-competing-CI-surface
  side of that claim by making it a CI failure to introduce
  a competing CI workflow surface in §25.
- **Lesson #15 reflexivity** — clause-5 enforces gate name
  remains in §25 §00 boundary declaration block.
- **Slot 58 sibling** (`check-no-sql-ddl-in-ui-folder`) — slot
  58 enforced the §24 no-DDL boundary using the same
  pattern (boundary-declaration + Lesson #15 self-citation +
  R5 exemption-exercised proof). Slot 59 reuses the pattern
  for §25 / CI-yaml.

## Scorecard impact (Rubric v2 /120)

- **§25** — C4 (Consistency) +1 (boundary now load-proven —
  no smuggled CI workflow in issues folder); C5
  (Implementability) +1 (cite mechanism is gate #37 — issues
  contributor can prove their changes don't violate the
  boundary by running the gate); C6 (Friction) +1
  (paper-only T-09 backlog ticket retires). §25 advances
  Lovable 118 → 119, Cursor 116 → 118, Raw-LLM 111 → 113.
- **§27** — C6 +1 (boundary-quartet 2 of 4 closed).
- **§28** — C4 +1 (single-source-of-truth-for-CI claim now
  bidirectionally enforced — §28 owns the universal CI CLI,
  §27 owns workflow-step wiring, §25 cannot compete).

## Out of scope

- CI YAML in §27 (`spec/27-spec-toolchain/` ships
  `.github/workflows/spec-health.yml` — explicitly the source
  of truth, not the boundary).
- CI YAML in §28 (`spec/28-universal-ci-cli/` owns the
  universal CI CLI surface — explicitly permitted).
- Other YAML in §25 (e.g. config-shape examples, OpenAPI
  fragments) — gate scope is CI-workflow-shape YAML only.
- Code fences in other languages (Markdown, JSON, TypeScript)
  — unrestricted in §25; gate scope is CI YAML only.
- §24 / §26 / §27 / §28 boundary contracts — covered by
  sibling slots 58 / 60 / 61.
