# Slot 61 — `check-no-out-of-scope-spec-folder-link.py`

**Status:** Active gate #39 (Phase-5 T-32)
**Implements:** locked-7 perimeter on disk + `mem://constraints/spec-scope` invariant + §27 §00 in-scope-folder enumeration claim (closes §27 backlog `no-out-of-scope-spec-folder-link-in-locked-7` minted Phase-5 T-09 — **FINAL §27 backlog ticket**, completes boundary-quartet 4/4)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "locked-7 perimeter gate"

## Contract

Walks every `.md` file under the 7 in-scope folders
(`spec/22-git-logs-v2`, `spec/23-app-database`,
`spec/24-app-design-system-and-ui`, `spec/25-app-issues`,
`spec/26-gitlogs-diagrams`, `spec/27-spec-toolchain`,
`spec/28-universal-ci-cli`) and asserts NO content reference
crosses the locked-7 perimeter. Out-of-scope spec folders
(`spec/00-…` through `spec/21-…`, `spec/29-…`, and
`spec/_archive/…`) are quarantined: in-scope `.md` files MUST
NOT link to them, cite their paths as authoritative, embed
their fences, or imply they are part of the active spec surface.
This is the on-disk mechanization of the `mem://constraints/spec-scope`
memory invariant. Closes §27 backlog
`no-out-of-scope-spec-folder-link-in-locked-7` (the **fourth and
final** boundary-quartet gate; **last §27 backlog ticket**).
Fails CI when ANY of the following invariants fail:

1. **No out-of-scope `spec/NN-…` path references** — no `.md`
   under the 7 in-scope folders may contain a path token
   matching `spec/(?:0\d|1\d|20|21|29)-[a-z0-9-]+/` (covers
   `spec/00-…` through `spec/21-…` and `spec/29-…`). Hits fail
   clause-1 with offending file:line + matched path. Backticked
   single-token references (e.g. `` `spec/15-legacy/` ``) inside
   archival-mention prose are PERMITTED only when adjacent to
   the literal token `out-of-scope` OR `archived` OR `superseded`
   within the same line (the gate detects the adjacency window
   and exempts those mentions).
2. **No `spec/_archive/` path references** — no `.md` under the
   7 in-scope folders may contain a path token matching
   `spec/_archive/`. Hits fail clause-2 with offending file:line.
   Backticked single-token references are PERMITTED only when
   the same line carries the literal `archived` OR
   `out-of-scope` adjacency marker (same exemption shape as
   clause-1).
3. **No Markdown links to out-of-scope spec paths** — no `.md`
   under the 7 in-scope folders may contain a Markdown link
   `[text](path)` whose `path` matches the clause-1 OR clause-2
   patterns. Adjacency-marker exemption from clauses 1/2 does
   NOT apply to Markdown links — links assert active
   referenceability and break the perimeter regardless of
   surrounding prose. Hits fail clause-3.
4. **No fenced embeds from out-of-scope folders** — no `.md`
   under the 7 in-scope folders may contain a fenced block
   whose language tag carries an `# from spec/NN-…/…` source-
   attribution comment matching clause-1/2 patterns, NOR a
   fence-preceding line `Source: spec/NN-…/…` matching the
   same. Embedding archived fence content into the active
   surface breaks the perimeter even without a link. Hits fail
   clause-4.
5. **§27 §00 in-scope folder enumeration cite** — `spec/27-spec-toolchain/00-overview.md`
   MUST contain the literal substring
   `Locked-7 in-scope folders: §22, §23, §24, §25, §26, §27, §28`
   (or canonical equivalent
   `7 in-scope folders are §22–§28; all others (00–21, 29, _archive) are out-of-scope`)
   within a normative block, AND the literal `Self-enforcing
   via §27 backlog gate \`no-out-of-scope-spec-folder-link-in-locked-7\``.
   Stripping either literal fails clause-5 (Lesson #15
   reflexivity break).
6. **Scope-lock memory invariant cite** — slot 61 doc Section
   "Bindings" MUST cite `mem://constraints/spec-scope` —
   confirms this gate is the **fourth and final** of 4 on-disk
   mechanizations of the scope-lock rule (boundary quartet
   4/4 — completes the perimeter).

## Invocation

```bash
python3 linter-scripts/check-no-out-of-scope-spec-folder-link.py --check all
python3 linter-scripts/check-no-out-of-scope-spec-folder-link.py --check no-numbered-out-of-scope-paths
python3 linter-scripts/check-no-out-of-scope-spec-folder-link.py --check no-archive-paths
python3 linter-scripts/check-no-out-of-scope-spec-folder-link.py --check no-markdown-links
python3 linter-scripts/check-no-out-of-scope-spec-folder-link.py --check no-fenced-embeds
python3 linter-scripts/check-no-out-of-scope-spec-folder-link.py --check in-scope-enumeration
python3 linter-scripts/check-no-out-of-scope-spec-folder-link.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if ALL 7 in-scope folders were walked (≥1 `.md`
each), the §27 §00 in-scope enumeration block was located
(clause-5 anchor), AND the adjacency-marker exemption (clauses
1/2) was exercised against ≥1 archival mention carrying the
`out-of-scope`/`archived`/`superseded` adjacency marker. Zero
anchors → exit `1` with `vacuous-pass: <reason>`. Specific
reasons: `<folder> has zero .md files`, `§27 §00 in-scope
enumeration absent`, or `no archival mention with adjacency
marker observed (clauses 1/2 exemption never exercised — gate
cannot prove its exemption logic is wired)`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-clean (7 folders each with ≥1 `.md`; §27 §00
  carries enumeration + gate self-citation; ≥1 archival mention
  cites `` `spec/15-legacy/` `` adjacent to `out-of-scope` literal;
  no out-of-scope links / embeds / unmarked path tokens) → passes
- **F-2** §22 child carries unfenced prose
  `See spec/15-legacy/00-overview.md for prior contract` (no
  adjacency marker) → fails clause-1
- **F-3** §24 child carries unfenced prose
  `Migrated from spec/_archive/old-ui/notes.md` (no adjacency
  marker) → fails clause-2
- **F-4** §27 child carries Markdown link
  `[old contract](../15-legacy/00-overview.md)` (links break
  perimeter regardless of prose) → fails clause-3
- **F-5** §23 child carries fenced block with preceding
  `Source: spec/_archive/old-schema.sql` attribution → fails
  clause-4
- **F-6** §27 §00 strips `Self-enforcing via §27 backlog gate
  \`no-out-of-scope-spec-folder-link-in-locked-7\`` literal
  → fails clause-5 (Lesson #15 reflexivity break)

## 5-link self-enforcement chain

1. **AC text** — §27 §00 in-scope folder enumeration block
   (carries gate self-citation per clause-5);
   `mem://constraints/spec-scope` memory invariant; §27 backlog
   `no-out-of-scope-spec-folder-link-in-locked-7` (Phase-5 T-09).
2. **Fixture surface** — synthetic in-memory tempdirs created
   by `--self-test` (6 short Markdown blobs across 7 folders).
3. **Script** — `linter-scripts/check-no-out-of-scope-spec-folder-link.py`.
4. **`--self-test`** — built-in mode, 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "locked-7 perimeter gate" hard-fails CI.
6. **§00 Walker-Pin row** — §27 §00 Walker-Pin block gains a
   row citing slot 61 + gate #39 + workflow step name
   (deferred to next §27 §00 touch).

## Bindings

- **`mem://constraints/spec-scope`** (locked-7 scope-lock
  memory invariant) — slot 61 is the **fourth and final** of 4
  boundary-quartet gates (slots 58/59/60/61) that collectively
  mechanize the scope-lock rule on disk. Slot 58 closed §24
  no-DDL boundary; slot 59 closed §25 no-CI-yaml; slot 60
  closed §25 no-toolchain-enum; slot 61 closes the locked-7
  perimeter. With slot 61, the memory invariant is fully
  load-proven — any future drift toward out-of-scope folders
  triggers a CI failure.
- **§27 backlog ticket `no-out-of-scope-spec-folder-link-in-locked-7`**
  — closes this turn (T-32). Minted Phase-5 T-09 alongside the
  boundary-quartet batch; paper-only for 21 cycles. **FINAL §27
  backlog ticket** — with this close, §27 backlog reaches zero.
- **Slots 58 / 59 / 60 siblings** — boundary-quartet pattern
  reuse (boundary-declaration + Lesson #15 self-citation + R5
  exemption-exercised proof). Slot 61 differs in that its scan
  surface is **all 7 folders** (not a single-folder boundary
  like 58/59/60) — enforces the perimeter from inside, not the
  surface shape of any one folder.
- **§27 §00 Inventory + Slot Delegation Map** — single source
  of truth for the locked-7 enumeration. Gate #39 enforces no
  in-scope `.md` references an out-of-scope sibling.
- **Lesson #15 reflexivity** — clause-5 enforces gate name
  remains in §27 §00 in-scope enumeration block.

## Scorecard impact (Rubric v2 /120)

- **§27** — C4 (Consistency) +1 (perimeter now load-proven —
  no in-scope `.md` references an out-of-scope sibling); C5
  (Implementability) +1 (cite mechanism is gate #39 — any
  contributor can prove their changes don't break the
  perimeter); C6 (Friction) +2 (final §27 backlog ticket
  retires; boundary-quartet 4/4 closed). §27 advances Cursor
  118 → 120, Raw-LLM 116 → 119; Lovable 120 carried. **§27
  reaches the 120/120 ceiling for Lovable + Cursor personas**.
- **§22 / §23 / §24 / §25 / §26 / §28** — C4 +1 each (in-scope
  status now load-proven from inside via the perimeter scan).
- **All 7 folders** — perimeter contract bidirectionally
  enforced: memory invariant (`mem://constraints/spec-scope`)
  declares the perimeter; gate #39 mechanizes it on disk.

## Out of scope

- Out-of-scope `spec/00–21/`, `spec/29/`, `spec/_archive/`
  internal references to one another — those folders are
  quarantined but the gate does NOT walk them; only their
  appearance INSIDE the 7 in-scope folders triggers a
  violation.
- `mem://` URI references — orthogonal namespace; not on
  disk; not perimeter-relevant.
- Code fences in TypeScript / SQL / JSON inside the 7 in-scope
  folders — unrestricted unless they carry an out-of-scope
  source attribution (clause-4 covers that case only).
- Other boundary contracts (§24 no-DDL, §25 no-CI-yaml, §25
  no-toolchain-enum) — covered by sibling slots 58 / 59 / 60.
