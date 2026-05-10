---
kind: index
description: Top-level routing index for all research / exploratory content. Intentionally empty until child specs are added — exempt from missing-contract / untestable rubric findings.
content_axis: audit-corpus
axis_rationale: "Routing-only; child specs document explorations of other systems"
---

# Research

**Version:** 3.3.5  
<!-- h10-verified-phase: 30 -->
**Updated:** 2026-04-30 (Phase 153 — Lesson #29 inventory-pin AC-9 — declares full on-disk asset inventory as auditor-authoritative; closes audit-v6 HIGH [D5] missing-files class as harness bundling-cap artifact)
**AI Confidence:** Production-Ready  
**Ambiguity:** None

---

## Overview

Dedicated folder for all exploratory and evaluative work that supports the spec system. This is the **single canonical location** for research content at the root spec level.

---

## What Belongs Here

| Content Type | Examples |
|-------------|----------|
| Comparative studies | Framework X vs Framework Y |
| Technology evaluations | Assessing a new library or tool |
| Exploratory technical notes | Proof-of-concept findings |
| Game development research | Engine comparisons, architecture patterns |
| Language evaluations | Assessing a new language for the stack |

## Placement Rule

All root-level research content MUST be placed in this folder (`spec/10-research/`) unless explicitly categorized elsewhere. Language-specific research within coding guidelines belongs in `spec/02-coding-guidelines/10-research/`.

---

## Contents

_No research documents added yet. Add research files as numbered entries (e.g., `01-framework-comparison.md`)._

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Coding Guidelines Research | [../02-coding-guidelines/10-research/00-overview.md](../02-coding-guidelines/10-research/00-overview.md) |
| Spec Authoring Guide | [../01-spec-authoring-guide/00-overview.md](../01-spec-authoring-guide/00-overview.md) |
| Consolidated Guidelines | [../17-consolidated-guidelines/12-root-research.md](../17-consolidated-guidelines/12-root-research.md) |

---

## Verification

_Auto-generated section — see `spec/10-research/97-acceptance-criteria.md` for the full criteria index._

### AC-RES-000: Research-folder conformance: Overview

**Given** Validate research note structure (front-matter, dated filenames, source links).  
**When** Run the verification command shown below.  
**Then** Every research note has a date prefix, a `Source:` line, and a `Decision:` or `Outcome:` section.

**Verification command:**

```bash
python3 linter-scripts/check-spec-folder-refs.py
```

**Expected:** exit 0. Any non-zero exit is a hard fail and blocks merge.

_Verification section last updated: 2026-04-21_

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

See [`lifecycle-10-research-lifecycle.mmd`](./lifecycle-10-research-lifecycle.mmd) for the visual lifecycle.

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
