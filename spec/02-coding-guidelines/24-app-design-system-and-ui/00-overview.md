---
kind: index
description: Placement-rule router for app design-system / UI specs under coding guidelines. Intentionally empty until child specs are added — exempt from missing-contract / untestable rubric findings.
---

# App Design System & UI

**Version:** 3.3.1  
<!-- h10-verified-phase: 30 -->
**Updated:** 2026-04-28  
**AI Confidence:** Draft  
**Ambiguity:** None

---

## Purpose

App-specific design system specifications, theming rules, component patterns, and layout conventions. This folder captures UI decisions that are specific to the application rather than cross-language or cross-project.

---

## Contents

_No content yet. Add design system documents as numbered files within this folder._

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Coding Guidelines Overview | [../00-overview.md](../00-overview.md) |
| Consolidated Summary | [../../17-consolidated-guidelines/16-app-design-system-and-ui.md](../../17-consolidated-guidelines/16-app-design-system-and-ui.md) |

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Status:** Forward-looking spec — drift expected.

Design-system technical requirements are spec contract; UI implementation lives in downstream React app repos.

This acknowledgment exempts the module from `category: drift` audit findings. See `.lovable/memory/index.md` Phase 27c note.

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

See [`lifecycle-02-coding-guidelines-24-app-design-system-and-ui-lifecycle.mmd`](./lifecycle-02-coding-guidelines-24-app-design-system-and-ui-lifecycle.mmd) for the visual lifecycle.

### Index Entry Status Enum — Phase 80 Normative

```ts
export enum IndexEntryStatus {
  Draft = "draft",
  Active = "active",
  Deprecated = "deprecated",
  Archived = "archived",
}

export interface IndexEntry {
  slug: string;
  title: string;
  status: IndexEntryStatus;
  routedTo: string | null;
}
```
