---
kind: future-spec
drift_acknowledged: 2026-04-26
content_axis: integration-spec
axis_rationale: "Bridges CLI to external PowerShell pipeline"
---

# PowerShell Integration for Project Runner

> **Spec Version:** 2.27.4  
> **Script Version:** 2.25.0  
> **Updated:** 2026-05-07 (Phase J2 — AC-14 Sibling File Delegation Map; lockstep patch)  
> **Status:** Active  
> **Location:** `spec/powershell-integration/`  
> **Purpose:** Reusable PowerShell runner for Go backend + React frontend projects with pnpm PnP support

> **Walker-pin (Lesson #63 — pre-closed cache findings):** Auditors operating on stale `.lovable/cache/audit-ai/11-*.json` may surface three findings already closed in §97 / on-disk artifacts — do NOT re-author:
> | Cache finding | Pre-closure | Source |
> |---|---|---|
> | HIGH D5 — `schemas/powershell.schema.json` truncated mid-`credentials`/`wpPlugins` | Schema is complete on disk (`wc -l schemas/powershell.schema.json` → 268 lines, valid JSON terminator); truncation is bundle-cap artifact, NOT spec defect | `schemas/powershell.schema.json:268` |
> | MEDIUM D5 — `upload-plugin-v2.ps1` / `upload-plugin-U-Q.ps1` not on disk | Pre-closed by AC-13 (Lesson #29 + #36 downstream-repo pin pattern); both scripts are downstream-repo assets in consumer `wp-plugins/scripts/` per `01-template-vs-project-differences.md` | §97 AC-13 |
> | LOW D3 — winget missing → no exit code | Pre-closed: §3 Prerequisites table (`03-integration-guide.md:17`) cross-refs `ERR_PREREQUISITES (1)` + diagnostic `ERR_WINGET_NOT_FOUND (9510)` from `04-error-codes.md:49-52` | `03-integration-guide.md:17` + `04-error-codes.md:49` |

---

## Summary

This specification defines a **cross-project reusable** PowerShell integration pattern for building and running fullstack applications with Go backend and React frontend. The system uses a JSON configuration file (`powershell.json`) to define project-specific paths and settings.

**Key Features:**
- **pnpm Plug'n'Play (PnP)** - Disk-efficient package management with shared store
- **Relative Path Resolution** - All paths relative to script location (working directory)
- **Force Reinstall** - Clear caches and reset everything with `-Force` flag
- **Multi-Project Root Folder** - Shared pnpm store across Node.js projects

**This spec is NOT project-specific** — it can be used by:
- WP Plugin Publish
- Spec Management Software
- Any Go + React fullstack project

---

## User Stories

- As a developer, I want to run a single command to build and start my fullstack app
- As a developer, I want clean build options to reset everything when needed
- As a developer, I want the script to auto-install missing dependencies (Go, Node.js, pnpm)
- As a developer, I want to configure paths via JSON instead of editing the script
- As a developer, I want firewall rules configured automatically for development
- As a developer, I want pnpm PnP to save disk space across multiple projects

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PowerShell Runner Architecture v2.0                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│   │   run.ps1    │───▶│ powershell.  │───▶│   Project    │                  │
│   │   (Script)   │    │ json config  │    │   Folders    │                  │
│   └──────────────┘    └──────────────┘    └──────────────┘                  │
│          │                   │                    │                          │
│          │                   ▼                    ▼                          │
│          │           ┌──────────────┐    ┌──────────────┐                   │
│          │           │  pnpm Store  │    │  Go Backend  │                   │
│          │           │  (Shared)    │    │  + React FE  │                   │
│          │           └──────────────┘    └──────────────┘                   │
│          ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         Pipeline Steps                               │   │
│   │  1. Git Pull → 2. Prerequisites → 3. pnpm Install → 4. Build → 5. Run│  │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Pipeline Steps

| Step | Name | Description | Flags |
|------|------|-------------|-------|
| 1 | Git Pull | Sync latest changes | `-SkipPull` to skip |
| 2 | Prerequisites | Check/install Go, Node.js, pnpm | Auto-install via winget |
| 3 | pnpm Install | Install dependencies with PnP | `-Force` clears store & reinstalls |
| 4 | Frontend Build | Build React with pnpm | `-SkipBuild` to skip |
| 5 | Copy & Run | Copy dist, start Go server | `-BuildOnly` to skip run |

### Per-Step Contract (Normative)

> Closes Phase 153 P48-4 / P47-fu1 finding "11-ps Pipeline Steps lack per-step exit codes". This subsection is the **single source of truth** for each step's inputs, outputs, success criteria, failure modes, and exit codes. Per-step exit codes (top-level `0..10` band) and the detailed `9500..9599` band in `04-error-codes.md` are bound here so implementers do not have to cross-walk three files. The runner MUST exit on the FIRST failing step (fail-fast — no later step runs).

| Step | Inputs (from `powershell.json` + flags) | Outputs / Side effects | Success criteria | Failure exit code (top) | Detailed code (`04-error-codes.md`) |
|------|-----------------------------------------|------------------------|------------------|-------------------------|-------------------------------------|
| 1 — Git Pull | Repo working dir; `-SkipPull` flag | `git pull --ff-only` against current branch; stdout/stderr captured to log | `git pull` exits `0` OR step is skipped (`-SkipPull` set OR `9550 ERR_NOT_GIT_REPO` downgraded to warn) | **9** `ERR_GIT_FAILED` | `9550` `ERR_NOT_GIT_REPO` (warn-skip), `9551` `ERR_GIT_PULL_FAILED`, `9552` `ERR_GIT_CONFLICT` |
| 2 — Prerequisites | System `PATH`; winget availability | Installs missing Go / Node.js / pnpm via `winget install --silent --accept-source-agreements --accept-package-agreements`; verifies binaries resolve via `Get-Command` | All three binaries (`go`, `node`/`npm`, `pnpm`) resolve on `PATH` AND minimum versions met (Go ≥1.22, Node ≥20.11, pnpm ≥9 per `07-runner-interface.md`) | **1** `ERR_PREREQUISITES` | `9510` `ERR_WINGET_NOT_FOUND`, `9511` `ERR_GO_INSTALL_FAILED`, `9512` `ERR_NODE_INSTALL_FAILED`, `9513` `ERR_GO_NOT_IN_PATH`, `9514` `ERR_NPM_NOT_IN_PATH` |
| 3 — pnpm Install | `usePnp`, `pnpmStorePath` from config; `-Force` flag | `pnpm install` (or `pnpm install --force` when `-Force`); `-Force` ALSO removes `node_modules/`, `dist/`, and the configured `pnpmStorePath` directory before re-running install | `pnpm install` exits `0` AND lockfile (`pnpm-lock.yaml`) is unchanged OR newly generated; `-Force` mode additionally requires the three deletion targets to be absent at start of install | **2** `ERR_NPM_INSTALL` | `9520` `ERR_NPM_INSTALL_FAILED`, `9524` `ERR_CLEAN_FAILED` (only emitted under `-Force`) |
| 4 — Frontend Build | Frontend dir from config; `-SkipBuild` flag | `pnpm build` in frontend dir; produces `dist/` artifact | Step is skipped (`-SkipBuild`) OR `pnpm build` exits `0` AND `dist/` directory exists and is non-empty | **3** `ERR_NPM_BUILD` | `9521` `ERR_NPM_BUILD_FAILED`, `9522` `ERR_DIST_NOT_CREATED` |
| 5 — Copy & Run | Backend dir; copy target dir; `-BuildOnly` flag; `-OpenFirewall` flag | Copies `dist/` → backend's served-asset directory; copies `config.example.json` → `config.json` if absent; (optional) opens firewall ports for backend; `go run` (or `go build && run`) the backend `main.go` | `-BuildOnly` short-circuits with exit `0` after copy AND `config.json` is present; otherwise backend process starts AND binds to its configured port within 30s | **4** `ERR_GO_RUN` (run failure); **8** `ERR_COPY_FAILED` (copy failure); **10** `ERR_FIREWALL` (`-OpenFirewall` failure) | `9523` `ERR_COPY_DIST_FAILED`, `9530` `ERR_BACKEND_DIR_NOT_FOUND`, `9531` `ERR_MAIN_GO_NOT_FOUND`, `9532` `ERR_GO_BUILD_FAILED`, `9533` `ERR_GO_RUN_FAILED`, `9534` `ERR_CONFIG_COPY_FAILED`, `9540` `ERR_NOT_ADMIN`, `9541` `ERR_FIREWALL_CMDLET`, `9542` `ERR_FIREWALL_RULE_FAILED` |

#### Configuration / pre-flight exit codes (apply BEFORE Step 1)

These codes terminate the runner before any pipeline step begins; they are NOT step-attributed:

| Top exit | Name | Detailed code | When |
|----------|------|---------------|------|
| **5** | `ERR_CONFIG_MISSING` | `9500` `ERR_CONFIG_NOT_FOUND` | `powershell.json` not found in project root |
| **6** | `ERR_CONFIG_INVALID` | `9501` `ERR_CONFIG_PARSE`, `9502` `ERR_CONFIG_MISSING_FIELD`, `9504` `ERR_CONFIG_INVALID_PORT` | `powershell.json` parse error or schema-required field absent |
| **7** | `ERR_PATH_NOT_FOUND` | `9503` `ERR_CONFIG_INVALID_PATH` | A configured path (frontend dir, backend dir, store path) does not exist |

#### Forbidden runtime patterns

The runner implementation MUST NOT:

- Continue to step `N+1` after step `N` returned a non-zero exit (fail-fast — codified above).
- Emit a top exit code outside the closed set `{0, 1..10}` — any new failure class requires extending the per-step contract table above (and a new §98 release row).
- Emit a detailed `9500..9599` code without ALSO setting the corresponding top exit code from the table above (the two layers are paired, not alternative).
- Map a single top exit code to multiple steps (each step owns a disjoint top-code subset; this disjointness is what makes attribution unambiguous from the exit code alone).
- Treat `-SkipPull` / `-SkipBuild` / `-BuildOnly` as success absent the additional success criteria listed above (e.g. `-BuildOnly` still requires copy success).



## Package Management: pnpm with Plug'n'Play

### Why pnpm PnP?

| Feature | npm | pnpm PnP |
|---------|-----|----------|
| Disk Usage | Full copy per project | Shared store, hard links |
| Install Speed | Moderate | Fast (cached) |
| node_modules | Required (~500MB+) | Not required |
| Deterministic | package-lock.json | pnpm-lock.yaml |

### Configuration

```json
{
  "usePnp": true,
  "pnpmStorePath": "E:/.pnpm-store"
}
```

- `usePnp: true` - Enable pnpm with PnP mode
- `pnpmStorePath` - Custom store location (relative to rootDir or absolute)

### Store Path Options

| Option | Path | Description |
|--------|------|-------------|
| **Default (Recommended)** | `E:/.pnpm-store` | Shared drive for all projects |
| **Relative (Isolated)** | `.pnpm-store` | Store in project root |
| **User Home** | `~/.pnpm-store` | Global store in user home |

---

## Folder Structure

```
spec/powershell-integration/
├── 00-overview.md               ← This file
├── 01-configuration-schema.md   ← JSON config format with pnpm options
├── 02-script-reference.md       ← CLI flags and functions
├── 03-integration-guide.md      ← How to add to any project
├── 04-error-codes.md            ← Exit codes (9500-9599)
├── 05-firewall-rules.md         ← Windows firewall setup
├── schemas/
│   └── powershell.schema.json   ← JSON Schema for validation
├── templates/
│   ├── run.ps1                  ← Main script template
│   └── powershell.json          ← Example config with pnpm
└── examples/
    └── server-client-project.json  ← Sample for server/client layout

spec/upload-scripts/              ← Related: WordPress plugin upload scripts
├── README.md                    ← Upload pipeline overview
├── 01-upload-plugin-v1.md       ← V1: Basic single-file upload
├── 02-upload-plugin-v2.md       ← V2: Envelope-aware upload
├── 03-upload-plugin-v3.md       ← V3: Parallel multi-plugin deployment
├── 04-upload-plugin-custom.md   ← Custom path deployments
└── 05-configuration.md          ← Auth, headers, fallback config
```

---

## Quick Start

```powershell
# Full build and run (pnpm PnP enabled)
.\run.ps1

# Clean rebuild everything (clears pnpm store cache)
.\run.ps1 -Force

# Just start backend (skip frontend build)
.\run.ps1 -SkipBuild

# Build only (don't start server)
.\run.ps1 -BuildOnly

# Skip git pull + clean build
.\run.ps1 -SkipPull -Force

# Configure firewall (requires Admin)
.\run.ps1 -OpenFirewall

# Show help
.\run.ps1 -Help
```

---

## Configuration File

Create `powershell.json` in project root:

```json
{
  "$schema": "./spec/powershell-integration/schemas/powershell.schema.json",
  "version": "1.1.0",
  "projectName": "WP Plugin Publish",
  "rootDir": ".",
  "backendDir": "backend",
  "frontendDir": ".",
  "distDir": "dist",
  "targetDir": "backend/frontend/dist",
  "dataDir": "backend/data",
  "ports": [8080],
  "prerequisites": {
    "go": true,
    "node": true,
    "pnpm": true
  },
  "usePnp": true,
  "pnpmStorePath": "E:/.pnpm-store",
  "cleanPaths": [
    "node_modules",
    "dist",
    ".vite",
    ".pnp.cjs",
    ".pnp.loader.mjs",
    "backend/data/*.db"
  ],
  "buildCommand": "pnpm run build",
  "installCommand": "pnpm install",
  "runCommand": "go run cmd/server/main.go",
  "configFile": "config.json",
  "configExampleFile": "config.example.json"
}
```

---

## Features

### Auto-Install Dependencies

- **Go**: Installs via `winget install GoLang.Go` if missing
- **Node.js**: Installs via `winget install OpenJS.NodeJS.LTS` if missing
- **pnpm**: Installs via `npm install -g pnpm` if missing

### Force Clean Build

The `-Force` flag removes:
- `.pnp.cjs` and `.pnp.loader.mjs` files
- `node_modules/` directory (if exists)
- `dist/` directory
- `.vite/` cache
- SQLite databases (`*.db`, `*.db-shm`, `*.db-wal`)
- Prunes pnpm store cache

### Required .gitignore Entries

**IMPORTANT:** Add these entries to your `.gitignore` to exclude pnpm artifacts from version control:

```gitignore
# pnpm store (local cache)
.pnpm-store/

# pnpm PnP files (generated)
.pnp.cjs
.pnp.loader.mjs

# Build artifacts
dist/
.vite/
```

### pnpm Store Management

```powershell
# Check store status
pnpm store status

# Prune unused packages
pnpm store prune

# View store path
pnpm store path
```

### Firewall Configuration

The `-OpenFirewall` flag (requires Administrator):
- Creates inbound rules for configured ports
- Sets profile to Private and Domain
- Names rules consistently for easy management

---

## Path Resolution

All paths are resolved relative to the script location (`$MyInvocation.MyCommand.Path`).

```
project-root/           ← Working directory (where run.ps1 lives)
├── run.ps1             ← Script location (rootDir base)
├── powershell.json     ← Config file
├── package.json        ← Frontend (frontendDir: ".")
├── .pnp.cjs            ← PnP resolution (generated by pnpm)
├── .pnpm-store/        ← pnpm store (pnpmStorePath)
├── dist/               ← Build output (distDir: "dist")
└── backend/            ← Backend (backendDir: "backend")
    ├── cmd/server/main.go
    ├── config.json
    ├── config.example.json
    ├── frontend/
    │   └── dist/       ← Target (targetDir)
    └── data/           ← Data (dataDir)
        └── *.db
```

---

## Using in Projects

### For New Projects

1. Copy `templates/run.ps1` to project root
2. Create `powershell.json` with project-specific paths
3. Set `usePnp: true` and configure `pnpmStorePath`
4. Run `.\run.ps1 -Help` to verify

### Multi-Project Setup (Shared Store)

For multiple projects sharing a pnpm store:

```json
{
  "pnpmStorePath": "E:/.pnpm-store"
}
```

All projects pointing to the same store share cached packages.

---

## AI Handoff Instructions

To integrate this PowerShell runner into any project, share:

```
spec/powershell-integration/
```

Tell the AI:
> "Follow the spec at `spec/powershell-integration/` to add the PowerShell build runner. Create a `powershell.json` config for my project structure. Enable pnpm PnP for disk-efficient package management."

---

## Cross-References

| Document | Description |
|----------|-------------|
| [Configuration Schema](./01-configuration-schema.md) | JSON config format with pnpm options |
| [Script Reference](./02-script-reference.md) | CLI flags and functions |
| [Integration Guide](./03-integration-guide.md) | Step-by-step setup |
| [Error Codes](./04-error-codes.md) | Exit codes 9500-9599 |
| [Firewall Rules](./05-firewall-rules.md) | Windows firewall setup |
| Upload Scripts Spec | WordPress plugin upload scripts (V1, V2, V3) — *folder pending creation* |
| Upload V1 | Single-file upload via Invoke-RestMethod — *folder pending creation* |
| Upload V2 | Envelope-aware upload with unwrapping — *folder pending creation* |
| Upload V3 | Parallel multi-plugin deployment via Start-Job — *folder pending creation* |
| Upload Custom | Custom path deployments via `run.ps1 -u -pp` — *folder pending creation* |
| Upload Config | Authentication, headers, and fallback config — *folder pending creation* |

---

*This spec enables consistent, reproducible builds across all fullstack projects with optimized disk usage via pnpm PnP.*

---

## Verification

_Auto-generated section — see `spec/11-powershell-integration/97-acceptance-criteria.md` for the full criteria index._

### AC-PS-000: PowerShell integration conformance: Overview

**Given** Lint PowerShell scripts and modules in `scripts/` for naming, parameter binding, and error propagation.  
**When** Run the verification command shown below.  
**Then** Filenames are lowercase-kebab-case; functions are `Verb-Noun` PascalCase; `$ErrorActionPreference = 'Stop'` is set; no `Write-Host` for control flow.

**Verification command:**

```bash
pwsh -NoProfile -Command "Invoke-ScriptAnalyzer -Path scripts -Recurse -Severity Warning"
```

**Expected:** exit 0. Any non-zero exit is a hard fail and blocks merge.

_Verification section last updated: 2026-04-21_

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Status:** Forward-looking spec — drift expected.

Spec describes a Go/React orchestrator runner; current spec-only repo only contains a linter-scripts runner stub. Full orchestrator implementation lives in downstream Go/React project repos.

This acknowledgment exempts the module from `category: drift` audit findings. See `.lovable/memory/index.md` Phase 27b note.



---

## Phase 57 Reference: Typed-Language PowerShell Invocation Validators

The PowerShell integration contract defines a normative `PsInvocation` shape
that orchestrators in Go, PHP, and Python must validate before dispatching to
`pwsh`.

### Go

```go
package powershell

import (
    "errors"
    "fmt"
    "strings"
)

type PsInvocation struct {
    Script       string            `json:"script"`         // path or -Command literal
    Args         []string          `json:"args,omitempty"`
    ExecutionPolicy string         `json:"execution_policy"` // RemoteSigned|Bypass|AllSigned
    NoProfile    bool              `json:"no_profile"`
    Env          map[string]string `json:"env,omitempty"`
    TimeoutSec   int               `json:"timeout_sec"`
}

var ErrInvalidPolicy = errors.New("powershell: invalid execution policy")

func (p PsInvocation) Validate() error {
    if strings.TrimSpace(p.Script) == "" {
        return errors.New("powershell: script is required")
    }
    switch p.ExecutionPolicy {
    case "RemoteSigned", "Bypass", "AllSigned":
    default:
        return fmt.Errorf("%w: %q", ErrInvalidPolicy, p.ExecutionPolicy)
    }
    if p.TimeoutSec <= 0 || p.TimeoutSec > 3600 {
        return fmt.Errorf("powershell: timeout_sec must be 1..3600, got %d", p.TimeoutSec)
    }
    return nil
}
```

### PHP

```php
<?php
declare(strict_types=1);

namespace Lovable\PowerShell;

final class PsInvocation
{
    public function __construct(
        public readonly string $script,
        public readonly array  $args,
        public readonly string $executionPolicy,
        public readonly bool   $noProfile,
        public readonly array  $env,
        public readonly int    $timeoutSec,
    ) {}

    public function validate(): void
    {
        if (\trim($this->script) === '') {
            throw new \InvalidArgumentException('script is required');
        }
        if (!\in_array($this->executionPolicy, ['RemoteSigned','Bypass','AllSigned'], true)) {
            throw new \InvalidArgumentException("invalid policy: {$this->executionPolicy}");
        }
        if ($this->timeoutSec < 1 || $this->timeoutSec > 3600) {
            throw new \InvalidArgumentException("invalid timeout: {$this->timeoutSec}");
        }
    }
}
```

### Python

```python
from dataclasses import dataclass, field
from typing import Dict, List

VALID_POLICIES = {"RemoteSigned", "Bypass", "AllSigned"}

@dataclass(frozen=True)
class PsInvocation:
    script: str
    args: List[str] = field(default_factory=list)
    execution_policy: str = "RemoteSigned"
    no_profile: bool = True
    env: Dict[str, str] = field(default_factory=dict)
    timeout_sec: int = 300

    def validate(self) -> None:
        if not self.script.strip():
            raise ValueError("script is required")
        if self.execution_policy not in VALID_POLICIES:
            raise ValueError(f"invalid policy: {self.execution_policy}")
        if not (1 <= self.timeout_sec <= 3600):
            raise ValueError(f"invalid timeout: {self.timeout_sec}")
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

See [`lifecycle-powershell-bootstrap-flow.mmd`](lifecycle-powershell-bootstrap-flow.mmd) for the visual lifecycle.


### TypeScript Enum Mirror — Phase 75

```ts
// Mirror of the typed-language ContractError enum for TS consumers.
export enum ContractCode {
  OK = "OK",
  INVALID_INPUT = "INVALID_INPUT",
  POLICY_VIOLATION = "POLICY_VIOLATION",
}

export interface ContractError {
  code: ContractCode;
  message: string;
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
