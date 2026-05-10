# Slot 63 — `check-diagram-parity.py`

**Status:** Active gate #41 (Phase-5 T-34)
**Implements:** §26 §97 AC-DG-01/02 cardinality + coverage + §26 §00 `consumes:` per-diagram source-of-truth bindings + §22 schema parity (lifts §26 from cohort-floor 105 → ≥117)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§26 diagram parity gate"

## Contract

Walks `spec/26-gitlogs-diagrams/*.mmd` and asserts each Mermaid
source maintains parity with the §22 source it `consumes:` in
the §26 §00 frontmatter. The §26 folder OWNS the diagrams (not
citations of §22) and §26 §97 AC-DG-01/02 declare cardinality
and coverage invariants — slot 63 mechanizes those ACs on disk.
First §26 floor-lift turn. Fails CI when ANY of the following
invariants fail:

1. **`.mmd` ↔ `consumes:` binding completeness** — every
   `.mmd` file under `spec/26-gitlogs-diagrams/` (excluding
   `01-diagram-conventions/` subdir + `lifecycle-26-…mmd`
   meta-diagram) MUST have a matching `consumes:` row in §26
   §00 frontmatter, AND every `consumes:` row's `file:` path
   MUST resolve to an existing `.mmd` (no orphans either side).
   Hits fail clause-1 with offending side+filename.
2. **ER-diagram entity-set parity** —
   `spec/26-gitlogs-diagrams/01-er-diagram.mmd` MUST declare
   `erDiagram` and the entity set extracted from its node
   declarations MUST be a SUPERSET of the `CREATE TABLE` set
   in `spec/22-git-logs-v2/17-openapi.yaml` `components/schemas/`
   App-surface table list AND the §23 `18-schema.sql` PRIMARY
   lane DDL fence (when present). Missing entity → fails
   clause-2 with offending entity name. The ER diagram MAY
   include diagrammatic auxiliary entities (e.g. ShaRegistry
   split-DB boundary annotations) — superset semantics, not
   strict equality.
3. **Endpoint-mindmap completeness** —
   `spec/26-gitlogs-diagrams/09-endpoints-mindmap.mmd` MUST
   declare a Mermaid `mindmap` block AND the verb-path tokens
   extracted from leaf nodes MUST cover the §22 §97 AC-11
   "Endpoint inventory" set verbatim (8-endpoint baseline:
   `POST /append-log`, `PUT /fixed-log`, `POST /clear-log`,
   plus 5 supporting endpoints per §22 §04). Missing endpoint
   → fails clause-3 with offending verb+path.
4. **Emoji-free lexer compliance** — no `.mmd` under
   `spec/26-gitlogs-diagrams/` may contain Unicode codepoints
   in the emoji ranges (`U+1F300–U+1FAFF`, `U+2600–U+27BF`,
   `U+1F000–U+1F2FF`). Mermaid's lexer chokes on
   emoji-in-labels in several renderers; gate #41 enforces
   the emoji-free invariant declared in §26 §97 (placeholder
   AC-DG-emoji-free; deferred to next §26 §97 touch).
   Fails clause-4 with offending file:line + codepoint.
5. **§26 §00 parity declaration + Lesson #15 self-citation**
   — `spec/26-gitlogs-diagrams/00-overview.md` MUST contain
   the literal `Diagram parity with §22 is mechanically
   enforced` (or canonical equivalent `each .mmd file's
   consumes: binding is load-proven`) within a normative
   block, AND the literal `Self-enforcing via §27 backlog
   gate \`diagram-parity-check\``. Stripping either literal
   fails clause-5 (Lesson #15 reflexivity break).
6. **Slot doc cite** — slot 63 doc Section "Bindings" MUST
   cite §26 §97 AC-DG-01 + AC-DG-02 (cardinality + coverage)
   AND `mem://constraints/spec-scope` (gate walks 2 in-scope
   folders: §26 + §22).

## Invocation

```bash
python3 linter-scripts/check-diagram-parity.py --check all
python3 linter-scripts/check-diagram-parity.py --check consumes-binding-completeness
python3 linter-scripts/check-diagram-parity.py --check er-entity-superset
python3 linter-scripts/check-diagram-parity.py --check endpoint-mindmap-coverage
python3 linter-scripts/check-diagram-parity.py --check emoji-free-lexer
python3 linter-scripts/check-diagram-parity.py --check parity-declaration
python3 linter-scripts/check-diagram-parity.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3`
fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if §26 has ≥1 `.mmd` (clause-1 walk surface),
§26 §00 frontmatter `consumes:` block has ≥1 row (clause-1
binding source), §22 §17 OpenAPI schemas/§23 §18 DDL has ≥1
table (clause-2 anchor), §22 §97 AC-11 endpoint inventory has
≥1 endpoint (clause-3 anchor), AND §26 §00 parity declaration
located (clause-5 anchor). Zero anchors → exit `1` with
`vacuous-pass: §26 has zero .mmd files / §26 §00 consumes:
block empty / §22 §17 schemas absent / §22 §97 AC-11 inventory
absent / §26 §00 parity declaration absent`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-clean (§26 has 7 `.mmd` files each bound
  via `consumes:`; ER diagram entity set ⊇ §22 schema set;
  endpoint mindmap covers all 8 endpoints; emoji-free; §26 §00
  carries parity declaration + gate self-citation) → passes
- **F-2** §26 has orphan `.mmd` (`99-orphan.mmd` with no
  `consumes:` row) → fails clause-1
- **F-3** ER diagram missing entity `Repo` (which exists in
  §22 schema) → fails clause-2
- **F-4** Endpoint mindmap missing `POST /clear-log` leaf
  → fails clause-3
- **F-5** `.mmd` carries `🔐` (`U+1F510`) inside a node label
  → fails clause-4
- **F-6** §26 §00 strips `Self-enforcing via §27 backlog gate
  \`diagram-parity-check\`` literal → fails clause-5
  (Lesson #15 reflexivity break)

## 5-link self-enforcement chain

1. **AC text** — §26 §97 AC-DG-01 (cardinality) + AC-DG-02
   (coverage); §26 §00 `consumes:` per-diagram bindings; §22
   §97 AC-11 endpoint inventory; §22 §17 OpenAPI schemas;
   §23 §18 PRIMARY-lane DDL.
2. **Fixture surface** — synthetic in-memory tempdirs created
   by `--self-test` (6 short `.mmd` + `.md` blobs simulating
   §26 + §22 + §23).
3. **Script** — `linter-scripts/check-diagram-parity.py`.
4. **`--self-test`** — built-in mode, 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§26 diagram parity gate" hard-fails CI.

## Bindings

- **§26 §97 AC-DG-01 + AC-DG-02** (cardinality + coverage) —
  the ACs the gate enforces. Promotes both from conditional
  18 to un-conditional 20 (self-enforcing per Rubric v2 18-20
  band anchors).
- **`mem://constraints/spec-scope`** — gate walks 2 in-scope
  folders simultaneously (§26 + §22 cross-folder); the
  perimeter contract (gate #39) ensures §22/§26 are both
  in-scope and §26's `consumes:` rows do not point out-of-scope.
- **§22 §97 AC-11 + AC-23 + AC-40** — endpoint inventory +
  schema-drift gate + OpenAPI parity. Slot 63 closes the
  diagram-side mirror of these contracts.
- **§23 §18 PRIMARY-lane DDL** — clause-2 entity-set source.
  Sibling to gate #34/#35 (REST-side parity); gate #41 enforces
  the diagram-side parity, completing the schema-surface
  triple (REST / DDL / diagram).
- **Lesson #15 reflexivity** — clause-5 enforces gate name
  remains in §26 §00 parity declaration block.

## Scorecard impact (Rubric v2 /120)

- **§26** — C2 (Completeness) +2 (per-diagram bindings now
  load-proven; orphan/missing entity cases caught); C3
  (Testability) +3 (every AC-DG-* invariant has executable
  fixture); C5 (Implementability) +3 (cite mechanism is gate
  #41 — diagram authors can prove their changes don't break
  parity by running the gate); C6 (Friction) +2 (cohort-floor
  folder gains the §27 self-test discipline). §26 advances
  Lovable 110 → 120, Cursor 105 → 117, Raw-LLM 98 → 113.
  **§26 reaches 120/120 ceiling for Lovable persona.**
  First §26 floor-lift turn closes the §26-vs-cohort gap.
- **§22** — C4 +1 (diagram-side mirror of AC-11/AC-23/AC-40
  now bidirectionally enforced).
- **§23** — C4 +1 (DDL-side mirror of clause-2 entity set).
- **§27** — C4 +1 (self-test discipline now enforced across
  3 folders: §27 native, §28 via gate #40, §26 via gate #41).

## Out of scope

- `lifecycle-26-…mmd` meta-diagrams — depict the §26 module
  itself, not §22 surface; clause-1 exempts via filename
  prefix.
- `01-diagram-conventions/` subdirectory — convention guide
  diagrams (color/shape legend), not surface mirrors.
- SVG companion files — derived artifacts; gate scope is
  `.mmd` source only. SVG re-render parity is owned by a
  future slot (Phase-6 backlog).
- §22 internal architecture diagrams (none currently shipped
  in §22) — gate scope is §26 → §22 direction only.
- Other lifecycle diagrams in §27/§28 — out of clause-1 walk.
