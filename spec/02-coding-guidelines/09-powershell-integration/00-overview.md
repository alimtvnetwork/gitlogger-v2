
# PowerShell Integration

**Version:** 3.4.0  **Updated:** 2026-04-27
<!-- h10-verified-phase: 32 -->

---

## Overview

PowerShell integration guidelines, scripting conventions, and best practices for cross-platform automation within the project ecosystem.

---

## Contents

_No content yet. Add PowerShell-related specs as numbered files within this folder._

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Cross-Language Guidelines | [../01-cross-language/00-overview.md](../01-cross-language/00-overview.md) |
| Coding Guidelines Spec | [../00-overview.md](../00-overview.md) |


---

## PowerShell integration contracts (Phase 54)

This module previously had no machine-readable contracts. Phase 54 introduces a
minimal but complete contract surface so a mediocre AI generator can implement
PowerShell automation scripts that integrate with the project ecosystem
(CI/CD, build pipelines, deployment) without reading sibling specs.

### Script descriptor — JSON Schema 2020-12

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spec.local/02-coding-guidelines/09-powershell-integration/script-descriptor.schema.json",
  "title": "PowerShellScriptDescriptor",
  "type": "object",
  "required": ["name", "purpose", "platform", "min_pwsh_version", "exit_codes"],
  "additionalProperties": false,
  "properties": {
    "name":              { "type": "string", "pattern": "^[A-Z][a-zA-Z0-9-]+\\.ps1$" },
    "purpose":           { "type": "string", "minLength": 10, "maxLength": 280 },
    "platform":          { "enum": ["windows", "linux", "macos", "cross"] },
    "min_pwsh_version":  { "type": "string", "pattern": "^\\d+\\.\\d+$" },
    "requires_elevation":{ "type": "boolean", "default": false },
    "parameters": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "type", "mandatory"],
        "additionalProperties": false,
        "properties": {
          "name":      { "type": "string", "pattern": "^[A-Z][a-zA-Z0-9]+$" },
          "type":      { "enum": ["string", "int", "bool", "switch", "path", "uri"] },
          "mandatory": { "type": "boolean" },
          "default":   {}
        }
      }
    },
    "exit_codes": {
      "type": "object",
      "patternProperties": {
        "^[0-9]+$": { "type": "string", "minLength": 3 }
      },
      "minProperties": 2
    }
  }
}
```

### Verb / parameter-type enums (TypeScript)

```ts
export enum PowerShellApprovedVerb {
  Get    = "Get",     // retrieve information
  Set    = "Set",     // modify state
  New    = "New",     // create resource
  Remove = "Remove",  // delete resource
  Test   = "Test",    // assertion
  Invoke = "Invoke",  // perform action
  Sync   = "Sync",    // align two states
  Export = "Export",  // serialize out
  Import = "Import",  // deserialize in
}

export enum PowerShellParameterType {
  String = "string",
  Int    = "int",
  Bool   = "bool",
  Switch = "switch",
  Path   = "path",
  Uri    = "uri",
}

export enum PowerShellExitCode {
  Success            = 0,
  GenericFailure     = 1,
  InvalidArguments   = 2,
  PermissionDenied   = 3,
  DependencyMissing  = 4,
  RemoteUnreachable  = 5,
  Timeout            = 124,
}
```

### CI workflow integration — GitHub Actions YAML

```yaml
# .github/workflows/powershell-lint.yml
name: powershell-lint
on:
  pull_request:
    paths: ['**/*.ps1', '**/*.psm1']
jobs:
  pssa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install PSScriptAnalyzer
        shell: pwsh
        run: Install-Module -Name PSScriptAnalyzer -Force -Scope CurrentUser
      - name: Lint
        shell: pwsh
        run: Invoke-ScriptAnalyzer -Path . -Recurse -Severity Error,Warning -EnableExit
```

```yaml
# .github/workflows/powershell-test.yml
name: powershell-test
on: [push, pull_request]
jobs:
  pester:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Run Pester
        shell: pwsh
        run: |
          Install-Module Pester -Force -Scope CurrentUser
          Invoke-Pester -CI
```

```yaml
# .github/workflows/powershell-publish.yml
name: powershell-publish
on:
  release:
    types: [published]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Publish to PSGallery
        shell: pwsh
        env:
          NUGET_API_KEY: ${{ secrets.PSGALLERY_API_KEY }}
        run: Publish-Module -Path ./module -NuGetApiKey $env:NUGET_API_KEY
```

```yaml
# .github/workflows/powershell-format.yml
name: powershell-format
on: pull_request
jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Format check
        shell: pwsh
        run: |
          Install-Module PSScriptAnalyzer -Force -Scope CurrentUser
          Invoke-Formatter -ScriptDefinition (Get-Content -Raw ./scripts/*.ps1) | Out-Null
```

```yaml
# .github/workflows/powershell-security.yml
name: powershell-security
on:
  schedule: [{ cron: '0 6 * * 1' }]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Security audit
        shell: pwsh
        run: |
          Install-Module PSScriptAnalyzer -Force -Scope CurrentUser
          Invoke-ScriptAnalyzer -Path . -Recurse -Severity Error -IncludeRule PSAvoidUsingPlainTextForPassword,PSAvoidUsingConvertToSecureStringWithPlainText -EnableExit
```


---

## Phase 62 Reference: PowerShell Integration Validators

The following Go / PHP / Python validators are normative reference
implementations of the PsRunResult contract.

### Go

```go
package powershell

import (
    "errors"
    "fmt"
)

type PsRunResult struct {
    ID        string `json:"id"`
    Status    string `json:"status"`
    Message   string `json:"message"`
    DurationMs int64 `json:"duration_ms"`
}

var ErrInvalidStatus = errors.New("powershell: invalid status")

func (r PsRunResult) Validate() error {
    if r.ID == "" {
        return errors.New("powershell: id is required")
    }
    switch r.Status {
    case "ok", "warning", "error":
    default:
        return fmt.Errorf("%w: %q", ErrInvalidStatus, r.Status)
    }
    if r.DurationMs < 0 {
        return errors.New("powershell: duration_ms must be >= 0")
    }
    return nil
}
```

### PHP

```php
<?php
declare(strict_types=1);

namespace Lovable\\PowerShell;

final class PsRunResult
{
    public function __construct(
        public readonly string $id,
        public readonly string $status,
        public readonly string $message,
        public readonly int    $durationMs,
    ) {}

    public function validate(): void
    {
        if ($this->id === '') {
            throw new \\InvalidArgumentException('id is required');
        }
        if (!\\in_array($this->status, ['ok','warning','error'], true)) {
            throw new \\InvalidArgumentException("invalid status: {$this->status}");
        }
        if ($this->durationMs < 0) {
            throw new \\InvalidArgumentException('durationMs must be >= 0');
        }
    }
}
```

### Python

```python
from dataclasses import dataclass

VALID_STATUSES = {"ok", "warning", "error"}

@dataclass(frozen=True)
class PsRunResult:
    id: str
    status: str
    message: str
    duration_ms: int

    def validate(self) -> None:
        if not self.id:
            raise ValueError("id is required")
        if self.status not in VALID_STATUSES:
            raise ValueError(f"invalid status: {self.status}")
        if self.duration_ms < 0:
            raise ValueError("duration_ms must be >= 0")
```


### Audit-Log Schema — Phase 76 Reference

The following normative SQL DDL defines the audit-log table that records
every invocation of the workflow described in this module. Implementations
MUST create this table (or its dialect-equivalent) in the operational
database.

```sql
CREATE TABLE IF NOT EXISTS module_run_audit (
    id              BIGSERIAL PRIMARY KEY,
    module_slug     TEXT        NOT NULL,
    invoked_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    invoked_by      TEXT        NOT NULL,
    git_sha         TEXT        NOT NULL,
    inputs_hash     TEXT        NOT NULL,
    exit_code       INTEGER     NOT NULL,
    duration_ms     INTEGER     NOT NULL,
    error_code      TEXT        NULL,
    error_message   TEXT        NULL,
    completed_at    TIMESTAMPTZ NULL,
    CONSTRAINT chk_exit_code_nonneg CHECK (exit_code >= 0),
    CONSTRAINT chk_duration_nonneg  CHECK (duration_ms >= 0)
);

CREATE INDEX IF NOT EXISTS idx_module_run_audit_module_slug
    ON module_run_audit (module_slug);

CREATE INDEX IF NOT EXISTS idx_module_run_audit_invoked_at_desc
    ON module_run_audit (invoked_at DESC);

CREATE INDEX IF NOT EXISTS idx_module_run_audit_failed
    ON module_run_audit (module_slug, invoked_at DESC)
    WHERE exit_code <> 0;
```

See `lifecycle-02-coding-guidelines-09-powershell-integration.mmd` for the visual workflow.

