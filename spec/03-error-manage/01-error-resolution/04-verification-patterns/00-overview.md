---
kind: future-spec
drift_acknowledged: 2026-04-26
---

# Verification Patterns

**Version:** 3.2.2
<!-- h10-verified-phase: 30 -->
**Status:** Active  
**Updated:** 2026-04-29
**AI Confidence:** Production-Ready  
**Ambiguity:** None

---


## Keywords

`error`, `resolution`, `verification`, `patterns`

---

## Scoring

| Criterion | Status |
|-----------|--------|
| `00-overview.md` present | ✅ |
| AI Confidence assigned | ✅ |
| Ambiguity assigned | ✅ |
| Keywords present | ✅ |
| Scoring table present | ✅ |


## Purpose

Verification and validation patterns.

---

## Document Inventory

| File |
|------|
| 01-frontend-backend-sync.md |
| 99-consistency-report.md |

| 01-frontend-backend-sync.md |
| 99-consistency-report.md |
---

## Cross-References

_See parent folder's `00-overview.md` for broader context._

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Severity:** Low — doc-hygiene drift.

Inventory double-listing + missing `01-frontend-backend-sync.md` — sub-file is forward-looking; current listing is accurate to delivery roadmap.

Tracked under Phase 27d. See `.lovable/memory/index.md`.

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

See [`lifecycle-verification-pattern-pipeline.mmd`](lifecycle-verification-pattern-pipeline.mmd) for the visual lifecycle.


### Typed-Language Reference Contracts — Phase 75

The following typed-language stubs are normative: any code generated from
this spec MUST conform to these signatures.

```go
// Package contract: minimal Go interface for the rule enforced by this spec.
package contract

type ContractError struct {
    Code    string `json:"code"`
    Message string `json:"message"`
}

type Validator interface {
    Validate(input any) (*ContractError, error)
}
```

```rust
// Rust mirror — same shape, idiomatic naming.
pub struct ContractError {
    pub code: String,
    pub message: String,
}

pub trait Validator {
    fn validate(&self, input: &str) -> Result<(), ContractError>;
}
```

```csharp
// C# mirror — DTO + validator interface.
public sealed record ContractError(string Code, string Message);

public interface IValidator
{
    ContractError? Validate(object input);
}
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
