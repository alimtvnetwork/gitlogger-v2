---
description: App UI Conventions — content child module of `02-coding-guidelines/24-app-design-system-and-ui/`. Carries an inlined contract, Mermaid lifecycle diagram, and full GWT acceptance criteria.
---

# App UI Conventions

**Version:** 2.0.0
**Updated:** 2026-04-27
**Parent:** [`../00-overview.md`](../00-overview.md)

---

## Overview

App-layer UI naming, composition, and a11y conventions. Enforces PascalCase component names, suffix patterns (Modal, Drawer, Sheet), and WCAG AA baseline.

---

## Inlined Contract

```ts
// App UI convention contract
export type ComponentSuffix = "Modal" | "Drawer" | "Sheet" | "Dialog" | "Popover" | "Toast" | "Banner";

export interface AppComponentConvention {
  /** PascalCase, optionally ending in one of ComponentSuffix */
  name: string;            // ^[A-Z][A-Za-z0-9]*(Modal|Drawer|Sheet|Dialog|Popover|Toast|Banner)?$
  /** WCAG criterion this component must satisfy at minimum */
  wcagBaseline: "AA" | "AAA";
  /** semantic design tokens used (no raw colors permitted) */
  tokens: string[];        // e.g. ["--primary", "--background"]
  /** roving-tabindex required for composite widgets */
  rovingTabindex: boolean;
}

export const APP_UI_NAMING_RX = /^[A-Z][A-Za-z0-9]*(Modal|Drawer|Sheet|Dialog|Popover|Toast|Banner)?$/;
```

---

## Lifecycle Diagram

See [`lifecycle-component-authoring.mmd`](./lifecycle-component-authoring.mmd) for the complete authoring → validation → publication lifecycle.

```mermaid
flowchart TD
    A[New App Component] --> B{Name Matches APP_UI_NAMING_RX?}
    B -- No --> C[Block: APP-UI-001]
    B -- Yes --> D[Use Semantic Tokens Only]
    D --> E{Raw Color Detected?}
    E -- Yes --> C
    E -- No --> F[Apply WCAG Baseline]
    F --> G{Composite Widget?}
    G -- Yes --> H[Add Roving Tabindex]
    G -- No --> I[Done]
    H --> I
```

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Parent index | [`../00-overview.md`](../00-overview.md) |
| Acceptance criteria | [`./97-acceptance-criteria.md`](./97-acceptance-criteria.md) |
| Lifecycle diagram source | [`./lifecycle-component-authoring.mmd`](./lifecycle-component-authoring.mmd) |
| Changelog | [`./98-changelog.md`](./98-changelog.md) |
| Consistency report | [`./99-consistency-report.md`](./99-consistency-report.md) |


---

## Example Payload

A canonical entry/instance conforming to the contract above.

```tsx
// Compliant component example
import { cva } from "class-variance-authority";

const dialogVariants = cva("bg-background text-foreground", {
  variants: { tone: { default: "border-border", critical: "border-destructive" } }
});

export function ConfirmDialog(props: { tone?: "default" | "critical" }) {
  // PascalCase + Dialog suffix ✓, semantic tokens only ✓
  return <div className={dialogVariants({ tone: props.tone ?? "default" })} role="dialog" aria-modal="true" />;
}
```

---

## Tooling Snippet

CLI usage that authors and reviewers can copy-paste verbatim.

```bash
# Lint App UI components for naming + token compliance
bunx eslint 'src/components/**/*.{ts,tsx}' --rule 'app-ui/naming: error'
```

---

## Verification Checklist

```text
[ ] Inlined contract block parses with zero diagnostics
[ ] Example payload validates against the contract
[ ] lifecycle-*.mmd renders without error
[ ] At least 6 GWT acceptance criteria present, each with severity tag
[ ] check-spec-cross-links.py exits 0 for this folder
[ ] check-tree-health.cjs reports no findings against this folder
```


---

## Registry Table (DDL)

The auditor's registry table that tracks each instance produced under this contract:

```sql
-- Forward-only registry table for entries under this convention
CREATE TABLE IF NOT EXISTS RegistryEntry (
    RegistryEntryId INTEGER PRIMARY KEY AUTOINCREMENT,
    EntryId         TEXT    NOT NULL UNIQUE,         -- matches the contract's id pattern
    Status          TEXT    NOT NULL,                -- mirrors contract enum
    AuthoredAt      TEXT    NOT NULL,                -- ISO-8601
    SupersededBy    TEXT    NULL,                    -- nullable per Rule 12
    CreatedAt       TEXT    NOT NULL DEFAULT (datetime('now')),
    UpdatedAt       TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS IX_RegistryEntry_Status   ON RegistryEntry(Status);
CREATE INDEX IF NOT EXISTS IX_RegistryEntry_EntryId  ON RegistryEntry(EntryId);
```


---

## Validation Schema (excerpt)

Cross-validates the registry rows against the contract:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RegistryEntryRow",
  "type": "object",
  "required": ["EntryId", "Status", "AuthoredAt"],
  "properties": {
    "EntryId":      { "type": "string", "minLength": 5 },
    "Status":       { "type": "string" },
    "AuthoredAt":   { "type": "string", "format": "date-time" },
    "SupersededBy": { "type": ["string", "null"] }
  }
}
```

### CI Workflow — Phase 71 Reference

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

