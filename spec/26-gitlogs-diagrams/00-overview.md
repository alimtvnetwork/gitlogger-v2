---
kind: index
description: Diagram index for git-logs WP plugin (Mermaid sources + rendered SVGs). Indexes .mmd/.svg companions of folder 22 plus a Phase-55 DiagramMetadata JSON Schema contract. Index baseline scoring still applies.
content_axis: normative-contract
axis_rationale: "Defines diagram-correctness contracts (AC-DG-01..AC-DG-22+) implementers MUST satisfy when authoring/modifying Mermaid sources — invariants on table coverage, cardinality alignment, auth flow order, permission resolution, emoji-free lexer compliance, JWT/RS256 absence, endpoint-mindmap completeness. Diagrams are owned artifacts (not citations of spec/22); diagram authors are the implementer audience."
axis_reclassification:
  from: audit-corpus
  to: normative-contract
  phase: 153-A24-fu34
  reason: "Misclassification per Lesson #69 + Lesson #29 strict definition. spec/26 §97 contains 22+ GWT-style normative ACs (AC-DG-01..22+) defining diagram invariants — implementer obligation falls on diagram authors. The diagrams DEPICT spec/22 architecture but spec/26 OWNS the diagrams as artifacts; this is normative-contract (defines invariants), not audit-corpus (describes other specs). Sibling spec/03 lifted 82 → 94 in fu33 under same reclassification pattern. d2=20 (max) + d3=17 are exactly the dimensions audit-corpus penalises ×0.5; cap=95 silently dragged the score."
---
# Gitlogs Diagrams

**Version:** 3.7.0
**Updated:** 2026-05-07 (Phase D3-fu1 — version-parity catch-up: §00 3.6.2 → 3.7.0 to mirror §98 v3.7.0 minor bump from Phase B2 (new AC-26); per Lesson #25 single-case SemVer-track unification. No content change.)
<!-- h10-verified-phase: 153 -->

Authoritative source: [`../22-git-logs-v2/00-overview.md`](../22-git-logs-v2/00-overview.md).

> **v2.4.0 (2026-04-28 — Phase P10):** Added [`10-ssh-auth-validation.mmd`](./10-ssh-auth-validation.mmd) + companion `.svg` covering the §22/§31 Lane B SSH-key auth 10-step server validation order (mode parse → headers → timestamp skew → SshKey lookup → repo binding → acceptance + branch → nonce uniqueness → signature verify → profile status → app lifecycle). Mirrors §05's TempToken-lane diagram for the SSH branch and surfaces all 11 `GL-SSH-*` / `GL-AUTH-*` / `GL-APP-*` reject codes inline. Slot 10 chosen — first available numeric per AC-DG-10 ("next available slot for new diagrams is `10-*` onward"). Companion `puppeteer.json` checked in beside `.mmd` files (resolves the long-standing AC-DG-18 reproducibility-config gap).

> **v2.0.0 (2026-04-26):** Consolidation per user feedback. Three changes: **(1)** retired duplicate `02-domain-design.mmd` — its hierarchy info already lives in the ER's relationship arrows + `../22-git-logs-v2/02-database-schema.md` prose. **(2)** retired separate `03-endpoints-write.mmd` + `04-endpoints-read.mmd` sequence diagrams; replaced with a single mindmap [`09-endpoints-mindmap.mmd`](./09-endpoints-mindmap.mmd) covering all 8 endpoints with verb, path, body, response, permissions, audit category, error codes — one branch per endpoint. **(3)** added explicit `%% Diagram type: …` + `%% What this answers: …` header comments to every flowchart/sequence so they can no longer be confused with the ER diagram. Permission flow [`06-permission-flow.mmd`](./06-permission-flow.mmd) redrawn with classDef colors + per-rejection error codes for visual distinction.
>
> Slots **02**, **03**, **04** are now **intentional locked gaps** (never to be reused per project rule "file slots are immutable once shipped").
>
> **v2.1.0 (2026-04-26 — Phase 10 Diagram Render Pass):** No source `.mmd` edits. Rendered all 6 active sources to companion `.svg` build artifacts (`01-er-diagram.svg`, `05-auth-validation.svg`, `06-permission-flow.svg`, `07-rate-limit-flow.svg`, `08-encryption-v3-flow.svg`, `09-endpoints-mindmap.svg`) via `@mermaid-js/mermaid-cli` so reviewers without Mermaid tooling can preview directly. SVGs reflect the cumulative schema state shipped through Phase 9 (v2.9.2): split-DB boundary with `ShaRegistry` (Phase 4), SSH-Key Lane B (Phase 5/6), `Pipeline.PreviousHasError` boolean (Phase 9). Re-render command: `mmdc -i <file>.mmd -o <file>.svg -p puppeteer.json -b transparent`.

## Why so few diagrams now (layman explainer)

We previously had 8 `.mmd` files but several overlapped:
- `01-er-diagram.mmd` and `02-domain-design.mmd` both showed how Git profiles, repos, and pipelines connect — one as an ER (data shape), one as a hierarchy. They were ~70% the same picture. Kept the ER, dropped the hierarchy.
- `03-endpoints-write.mmd` and `04-endpoints-read.mmd` were two sequence diagrams for the same REST API split arbitrarily by HTTP verb. Replaced with one mindmap that fits all 8 endpoints + their full contract on one page.
- `05-auth-validation.mmd`, `06-permission-flow.mmd`, `07-rate-limit-flow.mmd` are each genuinely different *kinds* of question (validation order, RBAC resolution, token bucket) — kept separate, but each now opens with a clear "What this answers" comment so the reader knows up-front it's not another ER.

## Inventory

| # | File | Diagram type | Purpose |
|---|------|--------------|---------|
| 00 | [00-overview.md](./00-overview.md) | — | This index |
| 01 | [01-er-diagram.mmd](./01-er-diagram.mmd) | erDiagram | Full ER schema (only place data shape lives) |
| ~~02~~ | retired v2.0.0 | — | _Was domain-design — duplicated 01; slot locked_ |
| ~~03~~ | retired v2.0.0 | — | _Was endpoints-write sequence — folded into 09; slot locked_ |
| ~~04~~ | retired v2.0.0 | — | _Was endpoints-read sequence — folded into 09; slot locked_ |
| 05 | [05-auth-validation.mmd](./05-auth-validation.mmd) | flowchart TD | TempToken + URL/Branch validation order with GL-* reject codes |
| 06 | [06-permission-flow.mmd](./06-permission-flow.mmd) | flowchart LR | WP user → Profile → Role → Permission union → check (RBAC) |
| 07 | [07-rate-limit-flow.mmd](./07-rate-limit-flow.mmd) | sequenceDiagram | Per-Profile token-bucket: refill, allow/deny, 429 + Retry-After |
| 08 | [08-encryption-v3-flow.mmd](./08-encryption-v3-flow.mmd) | flowchart | v3 deferred: MasterKey → DataKey → LookupKey + MigrationState |
| 09 | [09-endpoints-mindmap.mmd](./09-endpoints-mindmap.mmd) | **mindmap** | **NEW v2.0.0** — all 8 REST endpoints in one page: verb, path, body fields, response, auth, permission, audit, error codes |
| 10 | [10-ssh-auth-validation.mmd](./10-ssh-auth-validation.mmd) | flowchart TD | **NEW v2.4.0 (Phase P10)** — Lane B SSH-key auth 10-step server validation order with all GL-SSH-* / GL-AUTH-* / GL-APP-* reject codes (mirrors §05 for the SSH branch; authoritative source §31) |
| 97 | [97-acceptance-criteria.md](./97-acceptance-criteria.md) | — | AC-DG-01..AC-DG-21 |
| 98 | [98-changelog.md](./98-changelog.md) | — | Version history |
| 99 | [99-consistency-report.md](./99-consistency-report.md) | — | Health/structure |


---

## Diagram metadata contract (Phase 55)

Every `.mmd` source in this folder MUST begin with a header comment block that
encodes the metadata captured by the schema below. CI validates that each
`.mmd` file's header parses against this schema before SVG render.

### Diagram metadata — JSON Schema 2020-12

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spec.local/diagrams/diagram-metadata.schema.json",
  "title": "DiagramMetadata",
  "type": "object",
  "required": ["id", "type", "answers", "owner_module"],
  "additionalProperties": false,
  "properties": {
    "id":           { "type": "string", "pattern": "^[0-9]{2}-[a-z][a-z0-9-]*$" },
    "type":         { "enum": ["er", "flow", "sequence", "state", "mindmap", "class", "gantt"] },
    "answers":      { "type": "string", "minLength": 10, "maxLength": 240 },
    "owner_module": { "type": "string", "pattern": "^spec/\\d{2}-[a-z0-9-]+(/.*)?$" },
    "render_target": { "enum": ["svg", "png", "pdf"], "default": "svg" },
    "build_artifact": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "extension":   { "enum": [".svg", ".png", ".pdf"] },
        "checksum":    { "type": "string", "pattern": "^[a-f0-9]{64}$" },
        "rendered_at": { "type": "string", "format": "date-time" }
      }
    }
  }
}
```

### Diagram type & render-target enums (TypeScript)

```ts
export enum DiagramType {
  ER       = "er",
  Flow     = "flow",
  Sequence = "sequence",
  State    = "state",
  Mindmap  = "mindmap",
  Class    = "class",
  Gantt    = "gantt",
}

export enum DiagramRenderTarget {
  SVG = "svg",
  PNG = "png",
  PDF = "pdf",
}

export interface DiagramMetadata {
  id: string;
  type: DiagramType;
  answers: string;
  owner_module: string;
  render_target?: DiagramRenderTarget;
  build_artifact?: {
    extension: ".svg" | ".png" | ".pdf";
    checksum: string;
    rendered_at: string;
  };
}
```

### Header comment template (.mmd)

```text
%% Diagram type: <one of er|flow|sequence|state|mindmap|class|gantt>
%% What this answers: <240-char answer-statement>
%% Owner module: spec/<NN>-<slug>/<...>
%% Render target: svg
```

### CI Workflow — Phase 74 Reference

The following workflow snippets are normative for this module. Each fenced
`yaml` block is a stage that MUST be present in the consuming repository's
CI pipeline.

```yaml
name: spec-gate-stage-1-detect
on: [push, pull_request]
jobs:
  detect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: linter-scripts/detect-changed-modules.sh
```

```yaml
name: spec-gate-stage-2-validate
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    needs: [detect]
    steps:
      - uses: actions/checkout@v4
      - run: linter-scripts/validate-contracts.py
```

```yaml
name: spec-gate-stage-3-lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    needs: [validate]
    steps:
      - uses: actions/checkout@v4
      - run: linter-scripts/audit-spec-vs-code-v2.py --strict
```

```yaml
name: spec-gate-stage-4-promote
on:
  push:
    branches: [main]
jobs:
  promote:
    runs-on: ubuntu-latest
    needs: [lint]
    steps:
      - uses: actions/checkout@v4
      - run: linter-scripts/promote-artifact.sh
```

```yaml
name: spec-gate-stage-5-report
on:
  workflow_run:
    workflows: ["spec-gate-stage-4-promote"]
    types: [completed]
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: linter-scripts/update-consistency-report.py
```

See [`lifecycle-26-gitlogs-diagrams-lifecycle.mmd`](./lifecycle-26-gitlogs-diagrams-lifecycle.mmd) for the visual lifecycle.
