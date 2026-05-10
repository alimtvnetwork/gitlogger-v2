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
consumes:
  # Per-diagram source-of-truth bindings. Each .mmd DEPICTS the listed §22 AC(s);
  # mismatch between diagram and cited AC = AC-DG-01/02 (cardinality/coverage) breach.
  # See A-11 (Session 32) — mirror of §28→§27 (A-09) and §25→§27 (A-10) binding pattern.
  - file: 01-er-diagram.mmd
    source: spec/22-git-logs-v2/02-database-schema.md "ER + ShaRegistry split-DB boundary"
  - file: 05-auth-validation.mmd
    source: spec/22-git-logs-v2/05-auth-tempttoken.md "TempToken Lane A 10-step validation"
  - file: 06-permission-flow.mmd
    source: spec/22-git-logs-v2/06-rbac-permissions.md "Profile→Role→Permission union resolution"
  - file: 07-rate-limit-flow.mmd
    source: spec/22-git-logs-v2/07-rate-limiting.md "per-Profile token-bucket + 429/Retry-After"
  - file: 08-encryption-v3-flow.mmd
    source: spec/22-git-logs-v2/08-encryption-v3.md "MasterKey→DataKey→LookupKey + MigrationState (deferred)"
  - file: 09-endpoints-mindmap.mmd
    source: spec/22-git-logs-v2/04-rest-api.md "all 8 endpoints — verb/path/body/response/perms/audit/errors"
  - file: 10-ssh-auth-validation.mmd
    source: spec/22-git-logs-v2/60-app-cohort-integration.md "Lane B SSH-key 10-step validation + GL-SSH-*/GL-AUTH-*/GL-APP-* rejects"
produced_for:
  # Producer-side index — mirror of §24 producer-side (A-12, Sess-33). Each row
  # declares which §22 AC the diagram is the canonical depiction for. Closes the
  # bidirectional link begun by A-11 (consumes:) — readers of §22 ACs can now
  # resolve forward to the depicting diagram via this block.
  # See A-27 (Session 47) — pairs with A-11 to satisfy gate #10
  # (consumes-frontmatter-resolves) producer/consumer reciprocity.
  - file: 01-er-diagram.mmd
    fulfills: spec/22-git-logs-v2 §97 AC-23 "PascalCase + AUTOINCREMENT PK + CHECK-constraint catalog (schema canonical depiction)"
  - file: 05-auth-validation.mmd
    fulfills: spec/22-git-logs-v2 §97 AC-08 "TempToken Lane A 10-step validation order (canonical flowchart)"
  - file: 06-permission-flow.mmd
    fulfills: spec/22-git-logs-v2 §97 AC-11 "Profile→Role→Permission union resolution (RBAC canonical flowchart)"
  - file: 07-rate-limit-flow.mmd
    fulfills: spec/22-git-logs-v2 §97 AC-13 "per-Profile token-bucket + 429/Retry-After (canonical sequence diagram)"
  - file: 08-encryption-v3-flow.mmd
    fulfills: spec/22-git-logs-v2 §97 AC-15 "MasterKey→DataKey→LookupKey + MigrationState v3 (deferred — canonical depiction tracks the deferred state)"
  - file: 09-endpoints-mindmap.mmd
    fulfills: spec/22-git-logs-v2 §97 AC-04 "all 8 REST endpoints — verb/path/body/response/perms/audit/errors (canonical mindmap)"
  - file: 10-ssh-auth-validation.mmd
    fulfills: spec/22-git-logs-v2 §97 AC-09 "Lane B SSH-key 10-step server validation order + reject codes (canonical flowchart)"
---
# Gitlogs Diagrams

**Version:** 3.10.0
**Updated:** 2026-05-10 (Session 58 audit-task A-47 — `## §22 Enum Catalog Mirror — 12 enum types (Lesson #36 inline pin)` section added between Inventory and Diagram metadata contract. Inlines the 12 enum-type **names** (11 active + 1 forbidden-deprecated) pinned by §22 §97 AC-81, with cardinality, diagram-relevance, and authority columns. Codes remain single-source in §22 AC-81 + `18-schema.sql` per Lesson #36. Adds AC-DG-23 binding — diagram authors MUST cite enum values by PascalCase codes from this table; free-text synonyms = breach. Establishes §26 as the fifth landing surface for new enum types (mirror of AC-81's four-surface rule). Drift-check command pinned for future §27 gate `enum-mirror-26-vs-22-aligned`. Closes Raw-LLM Implementability gap: diagram authors without §22 in context window can now cite by enum-type name + cardinality without traversing 14 KB glossary. Prior: Sess-47 A-27 produced_for: bidirectional binding.)
<!-- h10-verified-phase: 153 -->

Authoritative source: [`../22-git-logs-v2/00-overview.md`](../22-git-logs-v2/00-overview.md).

> **v2.4.0 (2026-04-28 — Phase P10):** Added [`10-ssh-auth-validation.mmd`](./10-ssh-auth-validation.mmd) + companion `.svg` covering the §22/§31 Lane B SSH-key auth 10-step server validation order (mode parse → headers → timestamp skew → SshKey lookup → repo binding → acceptance + branch → nonce uniqueness → signature verify → profile status → app lifecycle). Mirrors §05's TempToken-lane diagram for the SSH branch and surfaces all 11 `GL-SSH-*` / `GL-AUTH-*` / `GL-APP-*` reject codes inline. Slot 10 chosen — first available numeric per AC-DG-10 ("next available slot for new diagrams is `10-*` onward"). Companion `puppeteer.json` checked in beside `.mmd` files (resolves the long-standing AC-DG-18 reproducibility-config gap).

> **v2.0.0 (2026-04-26):** Consolidation per user feedback. Three changes: **(1)** retired duplicate `02-domain-design.mmd` — its hierarchy info already lives in the ER's relationship arrows + `../22-git-logs-v2/02-database-schema.md` prose. **(2)** retired separate `03-endpoints-write.mmd` + `04-endpoints-read.mmd` sequence diagrams; replaced with a single mindmap [`09-endpoints-mindmap.mmd`](./09-endpoints-mindmap.mmd) covering all 8 endpoints with verb, path, body, response, permissions, audit category, error codes — one branch per endpoint. **(3)** added explicit `%% Diagram type: …` + `%% What this answers: …` header comments to every flowchart/sequence so they can no longer be confused with the ER diagram. Permission flow [`06-permission-flow.mmd`](./06-permission-flow.mmd) redrawn with classDef colors + per-rejection error codes for visual distinction.
>
> Slots **02**, **03**, **04** are now **intentional locked gaps** (never to be reused per project rule "file slots are immutable once shipped").
>
> **v2.1.0 (2026-04-26 — Phase 10 Diagram Render Pass):** No source `.mmd` edits. Rendered all 6 active sources to companion `.svg` build artifacts (`01-er-diagram.svg`, `05-auth-validation.svg`, `06-permission-flow.svg`, `07-rate-limit-flow.svg`, `08-encryption-v3-flow.svg`, `09-endpoints-mindmap.svg`) via `@mermaid-js/mermaid-cli` so reviewers without Mermaid tooling can preview directly. SVGs reflect the cumulative schema state shipped through Phase 9 (v2.9.2): split-DB boundary with `ShaRegistry` (Phase 4), SSH-Key Lane B (Phase 5/6), `Pipeline.PreviousHasError` boolean (Phase 9). Re-render command: `mmdc -i <file>.mmd -o <file>.svg -p puppeteer.json -b transparent`.

## AI Implementer Quickstart

**You are authoring/modifying Mermaid `.mmd` sources. Diagrams are owned artifacts — they DEPICT §22 but this folder OWNS the invariants.**

1. **Contracts first** — [`97-acceptance-criteria.md`](./97-acceptance-criteria.md): AC-DG-01..AC-DG-22+ (table coverage, cardinality alignment, auth-flow order, permission resolution, emoji-free lexer, no JWT/RS256, mindmap completeness).
2. **Header every `.mmd`** — start with `%% Diagram type: …` + `%% What this answers: …` + `%% Source spec: …` + `%% Audience: …` (per AC-DG-19/20).
3. **Slot rule** — file slots are immutable; next new diagram = next free numeric prefix (currently `11-*`). Slots `02/03/04` are intentional locked gaps.
4. **Re-render** — `mmdc -i <file>.mmd -o <file>.svg -p puppeteer.json -b transparent`. Commit `.mmd` + `.svg` together.
5. **Touched §22 schema/auth/perms?** Re-render the affected diagram in the same commit; stale SVG = AC-DG breach.

**Hard rules:** no emoji in `.mmd` · no JWT/RS256 references · ER is the only place data shape lives (no parallel domain hierarchy diagrams) · `puppeteer.json` MUST be checked in beside `.mmd` (AC-DG-18).

---

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

## §22 Enum Catalog Mirror — 12 enum types (Lesson #36 inline pin)

> **v3.10.0 (2026-05-10 — Session 58 audit-task A-47):** Inline mirror of the
> 12 enum types pinned by **spec/22 §97 AC-81** (11 active + 1 deprecated). Diagram
> authors MUST cite enum **values** in `.mmd` node labels by the PascalCase codes
> below (byte-identical to SQLite `{EnumName}.Name`, PHP `{EnumName}Type::cases()`,
> TS `enum {EnumName}` member). This block is a **Lesson #36 link-don't-restate
> mirror**: full code lists + drift contract live in
> [`../22-git-logs-v2/51-ac-enum-catalog-detail.md`](../22-git-logs-v2/51-ac-enum-catalog-detail.md)
> (AC-81) and [`../22-git-logs-v2/01-glossary-and-enums.md`](../22-git-logs-v2/01-glossary-and-enums.md)
> (canonical mirror). Restating per-code semantics here is **FORBIDDEN** —
> only enum-type names + cardinality + diagram-relevance are pinned.

| # | Enum type | Card. | Diagrams that may cite values | Authority |
|---|-----------|-------|-------------------------------|-----------|
| 1 | `UserStatus` | 3 | 06-permission-flow (gate node) | §22 AC-81 / `18-schema.sql` |
| 2 | `Role` | 2 | 06-permission-flow (Profile→Role edge label) | §22 AC-81 / `19-permission-matrix.md` |
| 3 | `Permission` | 17 | 06-permission-flow (terminal check); 09-endpoints-mindmap (per-endpoint perm leaf) | §22 AC-81 / `19-permission-matrix.md` |
| 4 | `Provider` | 2 (1 active) | 01-er-diagram (GitProfile.Provider column note) | §22 AC-81 |
| 5 | `Acceptance` | 3 | 05-auth-validation (URL-canon branch); 09-endpoints-mindmap (LogPush precondition) | §22 AC-81 / AC-08 |
| 6 | `AppStatus` | 3 | 09-endpoints-mindmap (LogPush precondition); 10-ssh-auth-validation (`GL-APP-*` reject branch) | §22 AC-81 / AC-20 |
| 7 | `AppLinkType` | 2 (exhaustive) | 01-er-diagram (polymorphic discriminator note) | §22 AC-81 / spec/23 AC-ADB-14 |
| 8 | `LogSeverity` | 6 (numeric weights) | (no current diagram cites — reserved for future per-SHA log flowchart) | §22 AC-81 / §39 |
| 9 | `PipelineActionType` | 4 | (no current diagram cites — reserved for future state diagram on `HasError` transitions) | §22 AC-81 / AC-13 |
| 10 | `SystemEventType` | 16 | (no current diagram cites — reserved for future audit-event mindmap) | §22 AC-81 / §20 |
| 11 | `AuditActionType` | 19 | (no current diagram cites — reserved) | §22 AC-81 |
| 12 | `AuditOutcome` | 3 (exhaustive) | 07-rate-limit-flow (audit-row outcome at terminal); 10-ssh-auth-validation (terminal node) | §22 AC-81 |
| — | `OwnerType_DEPRECATED_v380` | 2 (RETIRED) | **MUST NOT** appear in any new `.mmd` — retired v3.8.0; new citations = `GL-SCHEMA-DRIFT` | §22 AC-81 (deprecated stub) |

**Diagram-author obligations (normative; AC-DG-23 binding — see §97):**
1. Any `.mmd` node/edge label citing an enum value MUST use a code from the
   13-row table above (12 active + 1 forbidden-deprecated). Free-text synonyms
   (e.g., `"approved"` for `AcceptAllRepos`, `"banned"` for `Suspended`) =
   AC-DG-23 breach.
2. When a future enum type is added in spec/22 §97 AC-81, this table MUST gain
   a row in the same PR — partial landings = `GL-SCHEMA-DRIFT` and CI-blocking
   (mirror of AC-81's four-surface landing rule, extended to §26 as the fifth
   surface for diagrams).
3. Drift detection between this mirror and AC-81: `diff <(grep -oE '\| \`[A-Z][A-Za-z_0-9]*\` \|' spec/26-gitlogs-diagrams/00-overview.md) <(grep -oE '\| \`[A-Z][A-Za-z_0-9]*\` \|' spec/22-git-logs-v2/51-ac-enum-catalog-detail.md)` MUST return empty (gate
   `enum-mirror-26-vs-22-aligned` — deferred to §27, ships next phase).
4. Restating per-code semantics inline here = Lesson #36 violation. This block
   pins **type names + cardinality + diagram-relevance** only; codes live in §22.

**Why inline (not pure citation):** Raw-LLM auditors authoring a new diagram
without §22 in their context window otherwise produce free-text node labels
(empirical: Sess-32 baseline). Inlining the 12 type names with cardinality +
authority gives them enough surface to cite by name without traversing 14 KB
of `01-glossary-and-enums.md` (Lesson #16 tier-cap class). Codes themselves
remain single-source in §22 AC-81 + `18-schema.sql`.

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
