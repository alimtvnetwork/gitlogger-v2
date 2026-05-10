---
kind: index
drift_acknowledged: 2026-04-26
---

# Specification Root

**Version:** 3.5.1  
<!-- h10-verified-phase: 22 -->
**Updated:** 2026-04-27  
**AI Confidence:** Production-Ready  
**Ambiguity:** None

---

## Purpose

Root index for the entire specification tree. Each top-level folder contains a domain-specific specification module with its own overview, acceptance criteria, and consistency report.

---

## Module Inventory

### Core Fundamentals (01–20)

| # | Module | Description |
|---|--------|-------------|
| 01 | [Spec Authoring Guide](./01-spec-authoring-guide/00-overview.md) | Rules for writing and maintaining spec documents |
| 02 | [Coding Guidelines](./02-coding-guidelines/00-overview.md) | Cross-language coding standards (Go, TS, PHP, Rust, C#) |
| 03 | [Error Management](./03-error-manage/00-overview.md) | Error capture, modal UI, and resolution workflows |
| 04 | [Database Conventions](./04-database-conventions/00-overview.md) | Naming, schema design, ORM, REST API format |
| 05 | [Split DB Architecture](./05-split-db-architecture/00-overview.md) | SQLite partitioning and migration patterns |
| 06 | [Seedable Config (CW Config)](./06-seedable-config-architecture/00-overview.md) | Configuration seeding and feature management |
| 07 | [Design System](./07-design-system/00-overview.md) | Theme variables, typography, spacing, and component patterns |
| 08 | _Docs Viewer UI_ | **Locked vacant slot** — never authored |
| 09 | _Code Block System_ | **Locked vacant slot** — never authored |
| 10 | [Research](./10-research/00-overview.md) | Comparative studies, technology evaluations, exploratory notes |
| 11 | [PowerShell Integration](./11-powershell-integration/00-overview.md) | PowerShell scripting conventions, cross-platform automation |
| 12 | [CI/CD Pipeline Workflows](./12-cicd-pipeline-workflows/00-overview.md) | CI/CD pipeline specs, deployment workflows, automation |
| 13 | [Generic CLI](./13-generic-cli/00-overview.md) | Generic CLI architecture and conventions |
| 14 | [Self-Update & App Update](./14-update/00-overview.md) | Rename-first deployment, release pipeline, cross-compilation |
| 15 | [Distribution & Runner](./15-distribution-and-runner/00-overview.md) | Binary distribution and runner script standards |
| 16 | [Generic Release](./16-generic-release/00-overview.md) | Generic release pipeline patterns |
| 17 | [Consolidated Guidelines](./17-consolidated-guidelines/00-overview.md) | AI-readable summaries of every major spec module |
| 18 | [WP Plugin How-To](./18-wp-plugin-how-to/00-overview.md) | WordPress plugin authoring patterns |

### App-Specific (21+)

| # | Module | Description |
|---|--------|-------------|
| 21 | [Git Logs (legacy v1)](./_archive/21-git-logs-v1/00-overview.md) | ⚠️ Deprecated — superseded by `22-git-logs-v2/` |
| 22 | [Git Logs v2](./22-git-logs-v2/00-overview.md) | Authoritative WP plugin spec (v2.8.7+) |
| 23 | [App Database](./23-app-database/00-overview.md) | App-specific data model, table designs, migration strategies |
| 24 | [App Design System & UI](./24-app-design-system-and-ui/00-overview.md) | App-specific design system, theming, component patterns |
| 25 | [App Issues](./25-app-issues/00-overview.md) | App bug analysis, root cause analysis, fix documentation |
| 26 | [Git Logs Diagrams](./26-gitlogs-diagrams/00-overview.md) | Mermaid diagrams + SVG renders for the Git Logs spec |
| 27 | [Spec Toolchain](./27-spec-toolchain/00-overview.md) | Linter scripts, generators, and audit tooling for the spec tree |
| 28 | [Universal CI/CLI](./28-universal-ci-cli/00-overview.md) | Cross-project CI/CLI conventions and runner contracts |

---

## Supporting Files

| File | Purpose |
|------|---------|
| [folder-structure-root.md](./folder-structure-root.md) | Redirect to canonical folder structure spec |
| [spec-index.md](./spec-index.md) | Flat index of all spec files |
| [health-dashboard.md](./health-dashboard.md) | Spec tree health metrics and broken link report |
| [dashboard-data.json](./dashboard-data.json) | Machine-readable health data |

---

## Normative Contract — Spec Tree Index

This module is an **index** spec. Its normative contract is the JSON schema below
that downstream tooling (`linter-scripts/generate-dashboard-data.cjs`,
`linter-scripts/check-spec-cross-links.py`) consumes when emitting
`dashboard-data.json` and `spec-index.md`.

```text
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "spec/00-overview.schema.json",
  "title": "SpecTreeIndex",
  "type": "object",
  "required": ["version", "updated", "modules"],
  "properties": {
    "version":  { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
    "updated":  { "type": "string", "format": "date" },
    "kind":     { "const": "index" },
    "modules": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["number", "slug", "path", "status"],
        "properties": {
          "number": { "type": "integer", "minimum": 0, "maximum": 99 },
          "slug":   { "type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$" },
          "path":   { "type": "string", "pattern": "^\\./[0-9]{2}-[a-z0-9-]+/00-overview\\.md$" },
          "status": { "enum": ["active", "locked-vacant", "deprecated", "slot-collision"] },
          "description": { "type": "string", "minLength": 1 }
        },
        "additionalProperties": false
      }
    }
  }
}
```

> **Enforcement.** The dashboard scanner refuses to emit `dashboard-data.json`
> when this overview violates the schema (missing module row, illegal slug,
> duplicated number unless `status = "slot-collision"`). Slots `08`, `09`
> remain locked-vacant per `spec/01-spec-authoring-guide/02-naming-conventions.md`
> §"Reserved ranges".

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Folder Structure (canonical) | `./01-spec-authoring-guide/01-folder-structure.md` |
| Spec Authoring Guide | `./01-spec-authoring-guide/00-overview.md` |
| Coding Guidelines | `./02-coding-guidelines/00-overview.md` |
| Error Management | `./03-error-manage/00-overview.md` |
| Design System | `./07-design-system/00-overview.md` |

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Severity:** Low — doc-hygiene drift.

`dashboard-data.json` is a generated artifact (output of linter scripts), not a source file. Inventory listing is descriptive of runtime layout.

Tracked under Phase 27d. See `.lovable/memory/index.md`.

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

See [`lifecycle-spec-tree-overview.mmd`](./lifecycle-spec-tree-overview.mmd) for the visual lifecycle.

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
