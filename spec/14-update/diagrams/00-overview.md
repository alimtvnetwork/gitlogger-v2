---
kind: index
description: Diagram index for self-update / app-update workflows. Indexes Mermaid (.mmd) files and a Phase-55 DiagramMetadata JSON Schema contract. Index baseline scoring still applies.
---
# Diagrams — Self-Update & App Update

**Version:** 3.4.0  
**Updated:** 2026-04-27
<!-- h10-verified-phase: 32 -->

---

## Purpose

Index of all Mermaid diagrams supporting the self-update and app update specifications. These diagrams visualize decision trees and workflows described in the parent module.

---

## Diagram Inventory

| # | File | Description | Format |
|---|------|-------------|--------|
| 01 | [01-self-update-workflow.mmd](./01-self-update-workflow.mmd) | Full 9-step `<binary> update` command decision tree with error handling and rollback paths | Mermaid |
| 02 | [02-update-cleanup-workflow.mmd](./02-update-cleanup-workflow.mmd) | 2-phase `<binary> update-cleanup` workflow covering temp copies and `.old` backup removal | Mermaid |

**Total:** 2 diagrams

---

## Rendering

These `.mmd` files use Mermaid flowchart syntax. To render:

- **VS Code**: Install the "Mermaid Preview" extension
- **GitHub**: Mermaid blocks render natively in `.md` files (wrap in ` ```mermaid ` fences)
- **CLI**: Use `mmdc` from `@mermaid-js/mermaid-cli`

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Update Command Workflow (references these diagrams) | [../16-update-command-workflow.md](../22-update-command-workflow.md) |
| Self-Update Overview | [../01-self-update-overview.md](../01-self-update-overview.md) |
| Cleanup Specification | [../06-cleanup.md](../06-cleanup.md) |

---

*Diagrams Overview — v3.2.0 — 2026-04-15*


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

See [`lifecycle-14-update-diagrams-lifecycle.mmd`](./lifecycle-14-update-diagrams-lifecycle.mmd) for the visual lifecycle.
