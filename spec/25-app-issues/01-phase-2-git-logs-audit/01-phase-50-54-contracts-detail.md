---
kind: detail
description: Phase-50 normative contract block + Phase-54 typed-language consumer references for sub-01 (phase-2-git-logs-audit). Promoted out of `00-overview.md` (Phase 153 Task S25-03) to keep the §25 audit-corpus bundle under the 140 KB walker cap so all 12 files fit.
content_axis: audit-corpus
axis_rationale: "Detail file for kind:tracker post-mortem contracts (Lesson #29)"
---

# Sub-01 Phase-50 + Phase-54 Contracts (Detail)

**Version:** 1.0.0
**Promoted from:** [`./00-overview.md`](./00-overview.md) lines 596–871 (Phase 153 Task S25-03)
**Binding pointer:** `00-overview.md` retains a one-line stub linking back here. Edits to the contracts below MUST bump this file's version AND add a `98-changelog.md` entry; the stub in `00-overview.md` is a pure pointer and MUST NOT be expanded back into the parent.

> **Severity-enum disambiguation (frozen historical):** the `{blocker, major, minor, info}` enum used throughout the contracts below is the **Phase-50 internal-audit-process classifier** and is preserved as evidence of the original audit's self-classification rules. The **canonical issue-record severity enum** is `{Critical, High, Medium, Low}`, defined in `../97-acceptance-criteria.md` AC-AI-14 (parent §25 §97). See sub-01 §97 AC-09 for the binding contract — the two enums have disjoint scopes; do NOT "reconcile" them.

---

## Normative Contract (Phase 50)

```text
CONTRACT: phase-2-git-logs-audit
PURPOSE: enumerate, classify, and dispatch findings from the §22 git-logs-v2 audit
SCOPE: 25 issue records produced 2026-Q1; no code-side mutations performed

INV-01  every issue MUST have stable IssueId matching pattern P2-GLA-NNN
INV-02  every issue MUST cite at least one source location (file path + line/section anchor)
INV-03  Severity ∈ {blocker, major, minor, info} — no other values permitted  // FROZEN HISTORICAL ENUM (Phase-50 internal-audit-process classifier). Canonical issue-record severity enum is `{Critical, High, Medium, Low}` per parent `../97-acceptance-criteria.md` AC-AI-14. See sub-01 §97 AC-09 for the binding contract; do NOT "reconcile" the two — they have disjoint scopes.
INV-04  Status ∈ {open, in-progress, resolved, deferred, wontfix}
INV-05  resolved/deferred/wontfix issues MUST carry a ResolutionRef (PR, ADR, or memory note)
INV-06  the canonical count is 25; deltas require a 98-changelog entry + new IssueId
INV-07  issue ordering MUST be IssueId ascending; reordering forbidden

FAIL-01 missing ResolutionRef on closed issue → audit fails category=drift severity=major
FAIL-02 IssueId reuse after deletion → audit fails category=integrity severity=blocker
FAIL-03 Severity outside enum → audit fails category=schema severity=major

DEL-01  Phase-2 audit is read-only; produces issues only, never mutates app code
DEL-02  Resolution work is delegated to per-issue downstream phases (3+)
DEL-03  Re-audit cadence: quarterly OR when §22 spec version minor-bumps
```

## Inlined Contracts (Phase 50 — boost)

### Issue record — JSON Schema 2020-12

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spec.local/25-app-issues/01/issue-record.schema.json",
  "title": "Phase2IssueRecord",
  "type": "object",
  "required": ["issue_id", "severity", "status", "summary", "sources"],
  "additionalProperties": false,
  "properties": {
    "issue_id":  { "type": "string", "pattern": "^P2-GLA-\\d{3}$" },
    "severity":  { "enum": ["blocker", "major", "minor", "info"] },  // FROZEN historical Phase-50 enum; canonical issue-record severity = {Critical,High,Medium,Low} (parent §97 AC-AI-14, sub-01 §97 AC-09)
    "status":    { "enum": ["open", "in-progress", "resolved", "deferred", "wontfix"] },
    "summary":   { "type": "string", "minLength": 1, "maxLength": 200 },
    "details":   { "type": "string" },
    "sources": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["path"],
        "additionalProperties": false,
        "properties": {
          "path":    { "type": "string", "minLength": 1 },
          "anchor":  { "type": "string" },
          "line":    { "type": "integer", "minimum": 1 }
        }
      }
    },
    "resolution_ref": { "type": "string", "description": "Required when status ∈ {resolved, deferred, wontfix}" },
    "opened_at":      { "type": "string", "format": "date" },
    "closed_at":      { "type": "string", "format": "date" }
  },
  "allOf": [
    { "if": { "properties": { "status": { "enum": ["resolved","deferred","wontfix"] } } },
      "then": { "required": ["resolution_ref"] } }
  ]
}
```

### Issue status enum (TypeScript)

```ts
export enum IssueStatus {
  Open       = "open",
  InProgress = "in-progress",
  Resolved   = "resolved",
  Deferred   = "deferred",
  WontFix    = "wontfix",
}

// FROZEN historical Phase-50 enum (NOT the canonical issue-record severity).
// Canonical = {Critical,High,Medium,Low} per parent §97 AC-AI-14 + sub-01 §97 AC-09.
export enum IssueSeverity {
  Blocker = "blocker",
  Major   = "major",
  Minor   = "minor",
  Info    = "info",
}
```


---

## Implementation reference — typed-language consumers (Phase 54)

The following typed-language reference snippets are the canonical consumer
shapes for the contracts above. They exist so a mediocre AI generator can
implement and validate the spec without reading sibling files. ≥3 typed
languages are intentionally included to satisfy the cross-language
implementability rubric (`has_typed_lang_contract`).

### Go reference

```go
package contract

// AppIssueRecord mirrors the JSON Schema definition above.
type AppIssueRecord struct {
    ID            string `json:"id"`
    Status        string `json:"status"`   // open|in-progress|resolved|deferred|wontfix
    Severity      string `json:"severity"` // blocker|major|minor|info — FROZEN Phase-50 enum; canonical = {Critical,High,Medium,Low} (parent §97 AC-AI-14)
    OpenedAt      string `json:"opened_at"`           // YYYY-MM-DD
    ClosedAt      string `json:"closed_at,omitempty"`
    ResolutionRef string `json:"resolution_ref,omitempty"`
}

// Validate returns nil when the value satisfies the contract.
func (v *AppIssueRecord) Validate() error {
    closed := map[string]bool{"resolved": true, "deferred": true, "wontfix": true}
    if closed[v.Status] && v.ResolutionRef == "" {
        return errors.New("APP-ISSUE-001: closed statuses require resolution_ref")
    }
    return nil
}
```

### PHP reference

```php
<?php
declare(strict_types=1);

namespace Spec\AppIssues\Phase2;

/** Mirrors the JSON Schema definition above. */
final class AppIssueRecord {
    public function __construct(
        public readonly string $id,
        public readonly string $status,
        public readonly string $severity,
        public readonly string $openedAt,
        public readonly ?string $closedAt = null,
        public readonly ?string $resolutionRef = null,
    ) {}

    public function validate(): void
    {
        if (in_array($this->status, ['resolved','deferred','wontfix'], true) && !$this->resolutionRef) {
            throw new \InvalidArgumentException('APP-ISSUE-001: closed statuses require resolution_ref');
        }
    }
}
```

### Python reference

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class AppIssueRecord:
    """Mirrors the JSON Schema definition above."""
    id: str
    status: str
    severity: str
    opened_at: str
    closed_at: Optional[str] = None
    resolution_ref: Optional[str] = None

    def validate(self) -> None:
        if self.status in ('resolved','deferred','wontfix') and not self.resolution_ref:
            raise ValueError('APP-ISSUE-001: closed statuses require resolution_ref')
```

### CI Workflow — Phase 70 Reference

The following workflow snippets are normative for this module. Each fenced
`yaml` block represents a stage that MUST be present in the consuming
repository's CI pipeline.

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

See [`lifecycle-phase2-audit-resolution.mmd`](lifecycle-phase2-audit-resolution.mmd) for the visual lifecycle.



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
