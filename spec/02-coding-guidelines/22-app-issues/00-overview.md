---
kind: index
description: Placement-rule router for app issue analysis under coding guidelines. Intentionally empty until child specs are added — exempt from missing-contract / untestable rubric findings.
---

# App Issues

**Version:** 3.3.2  
<!-- h10-verified-phase: 30 -->
**Updated:** 2026-04-29

---

## Overview

App-specific issue analysis, root cause analysis, bug documentation, and solution guidance. This folder tracks problems encountered during application development, their diagnosis, and their resolution.

---

## Placement Rule

Any content that analyzes bugs, failures, root causes, or fixes for application-level work belongs here. General coding principle violations or cross-cutting concerns belong in the core fundamentals range (01–20).

---

## Contents

_No content yet. Add app issue analyses as numbered files within this folder._

---

## Cross-References

| Reference | Location |
|-----------|----------|
| App Specs | [../21-app/00-overview.md](../21-app/00-overview.md) |
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

See [`lifecycle-02-coding-guidelines-22-app-issues-lifecycle.mmd`](./lifecycle-02-coding-guidelines-22-app-issues-lifecycle.mmd) for the visual lifecycle.

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
