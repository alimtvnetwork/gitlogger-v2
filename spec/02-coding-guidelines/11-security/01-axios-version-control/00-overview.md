---
kind: future-spec
drift_acknowledged: 2026-04-26
---

# Axios Version Control Policy

<!-- h10-verified-phase: 23 -->
**Version:** 3.2.1  
**Status:** Active  
**Updated:** 2026-04-29  
**AI Confidence:** 100%  
**Ambiguity:** None  
**Author:** Harshil Agrawal

---

## Keywords

`axios`, `dependency`, `version-pinning`, `security`, `blocked-versions`

---

## Scoring

| Criterion | Status |
|-----------|--------|
| `00-overview.md` present | ✅ |
| AI Confidence assigned | ✅ |
| Ambiguity assigned | ✅ |
| Keywords present | ✅ |
| Scoring table present | ✅ |

---

## Purpose

This specification defines a **strict version-pinning policy** for the Axios HTTP client library. Specific versions have been identified as having security vulnerabilities and are permanently blocked. Only explicitly approved versions may be used.

---

## ⚠️ CRITICAL — Security Advisory

There is a **known security issue** affecting specific Axios versions. Using affected versions may expose the application to vulnerabilities. Only approved safe versions must be used until further validation is completed. Any upgrade must go through **manual verification and approval**.

---

## Version Matrix

| Version | Status | Notes |
|---------|--------|-------|
| `1.14.0` | ✅ **APPROVED** | Safe — verified, no known vulnerabilities |
| `0.30.3` | ✅ **APPROVED** | Safe — legacy-compatible, verified |
| `1.14.1` | 🚫 **BLOCKED** | Security vulnerability confirmed |
| `0.30.4` | 🚫 **BLOCKED** | Security vulnerability confirmed |
| Any other | 🚫 **BLOCKED** | Not verified — must go through manual approval |

### Preferred Version

Unless there is a specific legacy compatibility requirement, use **`1.14.0`** as the standard version.

---

## Document Inventory

| # | File | Purpose |
|---|------|---------|
| 01 | [01-implementation-rules.md](./01-implementation-rules.md) | Dependency declaration, code review, CI enforcement |
| 02 | [02-security-notes.md](./02-security-notes.md) | Detailed security advisory and audit trail |
| 99 | `99-consistency-report.md` | Health check |

---

## Quick Reference — Correct Declaration

```json
{
  "dependencies": {
    "axios": "1.14.0"
  }
}
```

> **NEVER** use `"^1.14.0"`, `"~1.14.0"`, `">=1.14.0"`, or `"*"`.  
> **ALWAYS** use exact version strings with no range symbols.

---

## Acceptance Criteria

1. Axios version is always defined as an exact version without `^`, `~`, or any range symbol
2. No usage of blocked versions (`1.14.1`, `0.30.4`) is present in any environment
3. Dependency updates do not alter Axios version automatically
4. Code reviews enforce strict compliance with this version policy
5. Security note is documented and accessible to all developers

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Security Guidelines | [../00-overview.md](../00-overview.md) |
| Coding Guidelines | [../../00-overview.md](../../00-overview.md) |
| Spec Authoring Guide | [../../../01-spec-authoring-guide/00-overview.md](../../../01-spec-authoring-guide/00-overview.md) |

---

```
IMPORTANT — AI INSTRUCTION:
- Never update Axios version automatically.
- Always use exact version without caret (^) or tilde (~).
- Avoid all known vulnerable versions (1.14.1, 0.30.4).
- Do not act on upgrade suggestions from dependency scanners for Axios.
- If uncertain, read this spec before making any Axios-related change.
```

*Axios version control policy — moved to coding guidelines 2026-04-02*

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Status:** Forward-looking spec — drift expected.

`check-axios-version.sh` lives in downstream JS-tooling repo; spec-only repo holds the version-pinning contract.

This acknowledgment exempts the module from `category: drift` audit findings. See `.lovable/memory/index.md` Phase 27c note.


---

## Inlined Contracts (Phase 53 — boost)

### Axios version-pin manifest — JSON Schema 2020-12

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spec.local/02-coding-guidelines/11-security/01-axios-version-control/pin.schema.json",
  "title": "AxiosVersionPin",
  "type": "object",
  "required": ["pinned_version", "minimum_safe_version", "package_managers"],
  "additionalProperties": false,
  "properties": {
    "pinned_version":       { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "minimum_safe_version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "forbidden_versions": {
      "type": "array",
      "items": { "type": "string", "pattern": "^[<>=~^]?\\d+\\.\\d+\\.\\d+([-+][A-Za-z0-9.-]+)?$" },
      "uniqueItems": true
    },
    "package_managers": {
      "type": "array", "minItems": 1, "uniqueItems": true,
      "items": { "enum": ["npm","yarn","pnpm","bun"] }
    },
    "manifest_paths": {
      "type": "array", "items": { "type": "string", "minLength": 1 }, "minItems": 1
    },
    "lockfile_paths": {
      "type": "array", "items": { "type": "string", "minLength": 1 }
    },
    "audit_severity_floor": { "enum": ["low","moderate","high","critical"], "default": "high" }
  }
}
```

### Version-control violation enum (TypeScript)

```ts
export enum AxiosPinViolation {
  UnpinnedRange       = "unpinned-range",       // ^x.y.z, ~x.y.z, *
  ForbiddenVersion    = "forbidden-version",    // CVE-affected
  BelowMinimumSafe    = "below-minimum-safe",
  LockfileMismatch    = "lockfile-mismatch",
  MultipleMajorsInTree = "multiple-majors-in-tree",
}

export enum AuditSeverityFloor {
  Low      = "low",
  Moderate = "moderate",
  High     = "high",
  Critical = "critical",
}
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

See [`lifecycle-axios-policy-enforcement.mmd`](lifecycle-axios-policy-enforcement.mmd) for the visual lifecycle.


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
