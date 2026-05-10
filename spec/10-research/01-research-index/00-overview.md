---
description: Top-Level Research Index — content child module of `10-research/`. Carries an inlined contract, Mermaid lifecycle diagram, and full GWT acceptance criteria.
---

# Top-Level Research Index

**Version:** 2.0.0
**Updated:** 2026-04-27
**Parent:** [`../00-overview.md`](../00-overview.md)

---

## Overview

Top-level research entries that span multiple coding-guideline domains (e.g., game-engine evaluations, framework comparisons). Same schema as the coding-guideline-scoped research index.

---

## Inlined Contract

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TopLevelResearchEntry",
  "type": "object",
  "required": ["id", "title", "domains", "owner", "status", "openedAt"],
  "properties": {
    "id":       { "type": "string", "pattern": "^TOP-RES-\\d{4}-\\d{3}$" },
    "title":    { "type": "string", "minLength": 5 },
    "domains":  { "type": "array", "minItems": 2, "items": { "type": "string" }, "description": "MUST be at least 2 spec module relpaths to qualify as top-level" },
    "owner":    { "type": "string" },
    "status":   { "type": "string", "enum": ["proposed", "active", "completed", "withdrawn", "promoted"] },
    "openedAt": { "type": "string", "format": "date" },
    "promotedTo": { "type": ["string", "null"] }
  }
}
```

---

## Lifecycle Diagram

See [`lifecycle-top-research.mmd`](./lifecycle-top-research.mmd) for the complete authoring → validation → publication lifecycle.

```mermaid
flowchart TD
    A[Cross-Domain Research Proposed] --> B{Spans 2+ Domains?}
    B -- No --> C[Reject: belongs in domain-scoped index]
    B -- Yes --> D[Allocate TOP-RES-NNNN-NNN]
    D --> E[Active]
    E --> F[Completed]
    F --> G{Promotable?}
    G -- Yes --> H[Promote to New Spec Module]
    G -- No --> I[Archive]
```

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Parent index | [`../00-overview.md`](../00-overview.md) |
| Acceptance criteria | [`./97-acceptance-criteria.md`](./97-acceptance-criteria.md) |
| Lifecycle diagram source | [`./lifecycle-top-research.mmd`](./lifecycle-top-research.mmd) |
| Changelog | [`./98-changelog.md`](./98-changelog.md) |
| Consistency report | [`./99-consistency-report.md`](./99-consistency-report.md) |


---

## Example Payload

A canonical entry/instance conforming to the contract above.

```json
{
  "id": "TOP-RES-2026-001",
  "title": "Rust async runtime comparison: tokio vs smol vs glommio",
  "domains": ["02-coding-guidelines/05-rust", "13-generic-cli"],
  "owner": "platform-team",
  "status": "active",
  "openedAt": "2026-04-27"
}
```

---

## Tooling Snippet

CLI usage that authors and reviewers can copy-paste verbatim.

```bash
# List top-level research spanning multiple domains
ls 10-research/ | grep -v '^00\|^9'
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

### CI Workflow — Phase 73 Reference

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



### Module Run Audit Schema — Phase 78 Normative

The following SQL DDL is normative for any consumer that persists per-module
execution telemetry. It MUST be applied verbatim (column names, types,
constraints) so downstream dashboards remain comparable across modules.

```sql
CREATE TABLE IF NOT EXISTS module_run_audit_p78 (
    run_id           BIGSERIAL PRIMARY KEY,
    module_slug      TEXT        NOT NULL,
    phase_label      TEXT        NOT NULL DEFAULT 'phase-78',
    started_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at      TIMESTAMPTZ NULL,
    duration_ms      INTEGER     NULL CHECK (duration_ms IS NULL OR duration_ms >= 0),
    exit_code        SMALLINT    NOT NULL DEFAULT 0,
    contract_hash    CHAR(64)    NOT NULL,
    implementability SMALLINT    NOT NULL CHECK (implementability BETWEEN 0 AND 100),
    UNIQUE (module_slug, contract_hash)
);

CREATE INDEX IF NOT EXISTS idx_mra_p78_slug_started
    ON module_run_audit_p78 (module_slug, started_at DESC);

CREATE INDEX IF NOT EXISTS idx_mra_p78_exit
    ON module_run_audit_p78 (exit_code)
    WHERE exit_code <> 0;
```

This contract enables AI agents to generate idempotent migrations and
verification queries directly from the spec.

### Research Index Status Enum — Phase 78 Normative

```ts
export enum ResearchEntryStatus {
  Draft = "draft",
  UnderReview = "under_review",
  Published = "published",
  Archived = "archived",
}

export interface ResearchIndexEntry {
  slug: string;
  title: string;
  status: ResearchEntryStatus;
  publishedAt: string | null;
}
```
