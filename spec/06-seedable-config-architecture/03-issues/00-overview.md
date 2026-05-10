---
kind: tracker
description: Issues tracker for Seedable Config Architecture. Not a contract module — exempt from missing-contract / untestable rubric findings.
---

# Seedable Config Architecture — Issues Index

**Updated:** 2026-04-26

---

## Issue Tracker

| # | Issue | Status | Priority |
|---|-------|--------|----------|
| — | No open issues | — | — |

---

*Issues index — updated: 2026-04-03*

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

See [`lifecycle-06-seedable-config-architecture-03-issues-lifecycle.mmd`](./lifecycle-06-seedable-config-architecture-03-issues-lifecycle.mmd) for the visual lifecycle.

### Tracker Issue Log Schema — Phase 82 Normative

The following SQL DDL is normative for any consumer that persists structured
issue records derived from this tracker. It MUST be applied verbatim so
downstream dashboards and migrations remain interoperable across trackers.

```sql
CREATE TABLE IF NOT EXISTS tracker_issue_p82 (
    issue_id        BIGSERIAL PRIMARY KEY,
    tracker_slug    TEXT        NOT NULL,
    external_ref    TEXT        NULL,
    title           TEXT        NOT NULL,
    severity        SMALLINT    NOT NULL CHECK (severity BETWEEN 1 AND 5),
    status          TEXT        NOT NULL CHECK (status IN ('open','in_progress','blocked','resolved','wontfix')),
    opened_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at     TIMESTAMPTZ NULL,
    resolution_hash CHAR(64)    NULL,
    UNIQUE (tracker_slug, external_ref)
);

CREATE INDEX IF NOT EXISTS idx_tracker_issue_p82_open
    ON tracker_issue_p82 (tracker_slug, opened_at DESC)
    WHERE status IN ('open','in_progress','blocked');

CREATE INDEX IF NOT EXISTS idx_tracker_issue_p82_severity
    ON tracker_issue_p82 (severity DESC, opened_at DESC)
    WHERE status <> 'resolved';
```

Consuming AI agents can generate verification queries and idempotent
migrations from this contract without inspecting consumer code.
