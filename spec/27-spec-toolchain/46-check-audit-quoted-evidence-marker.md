# Slot 46 — `check-audit-quoted-evidence-marker.py`

**Status:** Active gate #27 (Phase-5 T-20)
**Implements:** §24 §97 **AC-CAF-05** (line 257 — "Audit-finding strings cite, never restate") + §25 §97 AC-AI-10 (line 94 — auditor-quoted evidence) + AC-AI-11 (line 103 — missing-file findings target audited corpus) + AC-AI-14 rule 4 (line 155 — verbatim-quote rule) + scope-lock memory clause (`mem://constraints/spec-scope`)
**Self-test:** built-in (`--self-test`) against 5 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§24+§25 audit-quoted-evidence marker gate"

## Contract

Promotes AC-CAF-05 from conditional (paper-only at T-12 landing; decay
clause shared with CAF-01/02/03/04) to **load-proven** end-to-end.
**Last** of the five cross-cutting CAF ACs to convert; with T-20 the
entire CAF-01..05 family is un-conditionally load-proven by §27 gates
#23, #24, #25, #26, #27. Walks the AC-CAF-05 declaring text, the §25
AC-AI-10/11/14 surface, and every foreign-AC mention inside §25 finding
bodies + §23/§24 prose. Fails CI when ANY of the following
audit-quoting invariants fail:

1. **AC-CAF-05 declaring text marker discipline** — §24 §97 AC-CAF-05
   text (line 257) MUST contain ALL FOUR literal tokens:
   `auditor-quoted evidence`, `spec/_archive/21-git-logs-v1/`,
   `AC-AI-10/11`, `cross-cutting status`. Stripping any single
   literal collapses the AC to subjective prose; the four-literal
   marker IS the verifiable disambiguation mechanism the AC promises.
2. **§25 AC-AI-10 + AC-AI-11 surface presence** —
   `spec/25-app-issues/97-acceptance-criteria.md` MUST carry both
   `### AC-AI-10:` (containing literal `auditor-quoted evidence` AND
   `evidence under analysis`) AND `### AC-AI-11:` (containing literal
   `audited corpus` AND `spec/_archive/21-git-logs-v1/`). Removing or
   weakening either AC breaks the §25 surface CAF-05 lifts to
   cross-cutting.
3. **AC-AI-14 verbatim-quote rule (the underlying mechanism)** — §25
   §97 AC-AI-14 rule 4 (line 155) MUST contain ALL THREE literals:
   `Evidence snippets MUST be backticked or fenced`,
   `paraphrased evidence is FORBIDDEN`, and `AC-AI-10`. This is the
   actual machine-checkable rule that CAF-05 leans on; collapsing it
   leaves CAF-05 paper-only at the disambiguation surface.
4. **Foreign-AC quoting in §25 finding bodies** — every occurrence
   of an AC-ID matching `AC-(ALW|ERR|JWT|CG|SAG|TOK)-\d+` inside
   `spec/25-app-issues/02-consolidated-audit-findings/00-overview.md`
   AND `spec/25-app-issues/01-phase-2-git-logs-audit/00-overview.md`
   MUST appear inside backticks (`` `AC-ALW-12` ``) OR inside a
   fenced code block (` ``` ` … ` ``` `) OR inside a markdown
   blockquote line (`> `). Bare prose mention of a foreign AC-ID
   without quoting is the exact restate-drift pattern AC-CAF-05
   prohibits — the finding body would then read as a §25-owned
   contract rather than auditor-quoted evidence.
5. **No restate-drift in §23 / §24** — any line in `spec/23-app-database/`
   or `spec/24-app-design-system-and-ui/` that mentions a foreign-AC
   prefix `AC-(ALW|ERR|JWT|CG|SAG|TOK)-\d+` MUST satisfy BOTH:
   (a) the AC-ID appears inside backticks or a fenced block, AND
   (b) the surrounding paragraph (within 2 lines above or below)
   contains at least one of the marker words `evidence`, `quote`,
   `audit`, `_archive`, or `audit-corpus`. Either condition failing
   means §23/§24 is restating a §25 finding's foreign claim as if
   it were a live cross-spec dependency — the precise leak Lesson
   #36 + AC-CAF-05 forbid.

## Invocation

```bash
python3 linter-scripts/check-audit-quoted-evidence-marker.py --check all
python3 linter-scripts/check-audit-quoted-evidence-marker.py --check caf05-marker
python3 linter-scripts/check-audit-quoted-evidence-marker.py --check ai-10-11-surface
python3 linter-scripts/check-audit-quoted-evidence-marker.py --check ai-14-rule
python3 linter-scripts/check-audit-quoted-evidence-marker.py --check finding-body-quoting
python3 linter-scripts/check-audit-quoted-evidence-marker.py --check no-restate-23-24
python3 linter-scripts/check-audit-quoted-evidence-marker.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

A scanner that returns 0 because the §24 §97 AC-CAF-05 / §25 §97
AC-AI-10/11/14 anchors matched zero rows or zero literals is **itself
a violation** (exit `1`, message `vacuous-pass: zero AC-CAF-05 or
AC-AI-10/11/14 anchors found`). The `--self-test` mode is mandatory
in CI and asserts that the scanner correctly REJECTS five synthetic
fixtures:

- **F-1** complete-uniform (AC-CAF-05 with all four literals,
  AC-AI-10 + AC-AI-11 + AC-AI-14 rule 4 with all literals, every
  foreign-AC in §25 finding bodies backticked, no foreign-AC in
  §23/§24 outside backticked + evidence-marker context) → passes
- **F-2** AC-CAF-05 text drops the literal `cross-cutting status` →
  fails (clause-1; marker discipline)
- **F-3** §25 AC-AI-14 rule 4 drops `paraphrased evidence is FORBIDDEN`
  → fails (clause-3; underlying mechanism collapsed)
- **F-4** §25 finding body mentions `AC-ALW-12` without backticks
  in prose ("the AC-ALW-12 contract requires…") → fails (clause-4;
  restate-drift inside §25)
- **F-5** §23 §00 mentions `AC-JWT-09` in a paragraph with no
  surrounding `evidence` / `audit` / `_archive` marker word →
  fails (clause-5; restate-drift inside §23)
- **F-6** R5 vacuous-pass — no `AC-CAF-05` audit-quoted-evidence
  literal found in any in-scope §97 → fails as `vacuous-pass: empty
  walk → exit 3 fixture-rot` rather than silently passing on absence.

## 5-link self-enforcement chain

1. **AC text** — §24 §97 AC-CAF-05 (line 257); §25 §97 AC-AI-10
   (line 94) + AC-AI-11 (line 103) + AC-AI-14 rule 4 (line 155);
   scope-lock memory clause (`mem://constraints/spec-scope`).
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (5 short Markdown blobs reproducing the AC-CAF-05
   declaring text + AC-AI-10/11/14 surface + §25 finding-body
   quoting geometry + §23/§24 no-restate context).
3. **Script** — `linter-scripts/check-audit-quoted-evidence-marker.py`
   (this slot).
4. **`--self-test`** — built-in mode, runs 5 fixtures (F-1 unique
   passing fixture).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§24+§25 audit-quoted-evidence marker gate" hard-fails CI on
   any violation.
6. **§00 Walker-Pin row** — §24 + §25 `00-overview.md` Walker-Pin
   blocks gain a row citing this slot + gate #27 + workflow step
   name (deferred to next §24 / §25 §00 touch; in-spec catalogue
   holds until then).

## Bindings

- **AC-CAF-05** (T-12) — converts from conditional 20 (paper-only;
  decay clause shared with CAF-01/02/03/04) to un-conditional 20
  (load-proven cross-folder audit-quoting contract). This gate IS
  the cited self-enforcing mechanism. **Fifth and final
  cross-cutting CAF gate** after T-16 gate #23 (CAF-02), T-17 gate
  #24 (CAF-01), T-18 gate #25 (CAF-04), T-19 gate #26 (CAF-03).
  With T-20, the **entire CAF-01..05 family is un-conditionally
  load-proven** — first time since T-12 minted the namespace.
- **§25 AC-AI-10** (line 94) — gate clause 2 mechanises the §25
  surface presence; clause 4 mechanises the verbatim-quote rule
  AC-AI-10 declares (via AC-AI-14 rule 4).
- **§25 AC-AI-11** (line 103) — gate clause 2 mechanises §25
  inventory-finding boundary contract.
- **§25 AC-AI-14 rule 4** (line 155) — gate clause 3 mechanises
  the actual verbatim-quote enforcement rule; AC-AI-14 is the
  finding-body schema CAF-05's lift relies on.
- **Scope-lock memory clause** (`mem://constraints/spec-scope`) —
  clause 5 mechanises the §23/§24 no-restate side; foreign-AC
  prefixes belong to out-of-scope folders, so any in-scope mention
  must be evidence-marked. This gate IS the §27 mechanism the
  scope-lock memory clause cites.

## Out of scope

- Audit-finding **content** correctness (whether `AC-ALW-12` is a
  real archive AC) — this gate enforces only the QUOTING DISCIPLINE,
  not the underlying claim. The audited corpus
  `spec/_archive/21-git-logs-v1/` is OUT-of-scope per spec-scope
  memory; this gate never reads the archive.
- §22 + §26 + §27 + §28 prose — clause 5 scopes only §23 and §24
  per AC-CAF-05's "lifts to cross-cutting status so §23 + §24
  walkers also apply the rule" wording. §22 inherits via OpenAPI
  schema gates (#17/#23); §26 diagrams cite by visual reference,
  not prose; §27 specs ARE the toolchain meta; §28 has no §25
  finding overlap surface.
- Future §25 finding additions using new foreign-AC prefixes — the
  regex `AC-(ALW|ERR|JWT|CG|SAG|TOK)-\d+` is the closed set as of
  T-20. Adding a new foreign prefix (e.g. `AC-FOO-`) MUST update
  the regex in this slot's Section "Contract" clause 4 + clause 5
  AND ship in the same PR as the foreign-prefix-introducing finding.

## History

- **Phase-5 T-20** — slot created. Built-in self-test only (no
  on-disk fixture corpus needed; the five fixtures are short
  Markdown blobs exercising `re` predicates against synthetic
  AC-CAF-05 / AC-AI-10/11/14 / finding-body / §23-§24 anchor
  geometry). Mirrors slot-44 T-18 + slot-45 T-19 cross-folder
  uniformity convention. Closes §27 backlog entry
  `audit-quoted-evidence-marker-check` minted T-12 — the **last
  remaining CAF backlog ticket** from the original T-12 cluster.
  Promotes AC-CAF-05 from conditional to un-conditional
  self-enforcing — fifth and final cross-cutting CAF gate. With
  T-20 close, **all five CAF cross-cutting ACs are un-conditionally
  load-proven** for the first time since T-12.
