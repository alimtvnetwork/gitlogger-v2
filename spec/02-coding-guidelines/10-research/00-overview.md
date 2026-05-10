---
kind: index
description: Placement-rule router for research specs under coding guidelines. Intentionally empty until child specs are added — exempt from missing-contract / untestable rubric findings.
---

# Research

**Version:** 3.3.2  
<!-- h10-verified-phase: 30 -->
**Updated:** 2026-04-29

---

## Overview

Dedicated folder for comparative studies, technology evaluations, exploratory technical notes, and research that supports foundational coding guidelines. This includes game development research, framework comparisons, language evaluations, and any other exploratory work categorized as part of the foundational system.

---

## Placement Rule

All research content — including comparative studies, technology evaluations, and exploratory technical notes — MUST be placed in this folder (`10-research/`) unless explicitly categorized elsewhere by the spec authoring guide.

---

## Contents

_No content yet. Add research documents as numbered files within this folder._

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Coding Guidelines Spec | [../00-overview.md](../00-overview.md) |

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

See [`lifecycle-02-coding-guidelines-10-research-lifecycle.mmd`](./lifecycle-02-coding-guidelines-10-research-lifecycle.mmd) for the visual lifecycle.

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
