---
kind: interface-contract
---

# Runner Interface Contract — `run.ps1` & `powershell.json`

> **Version:** 1.0.0
> **Created:** 2026-04-27
> **Status:** Active
> **Parent:** [00-overview.md](./00-overview.md)
> **Related:** [01-configuration-schema.md](./01-configuration-schema.md), [04-error-codes.md](./04-error-codes.md)

---

## Purpose

Closes the audit gap **CRITICAL — Missing Interface Definition (JSON & CLI)** by
defining, in one place, the *exact* CLI surface, exit codes, and dependency
toolchain contract for the PowerShell runner. A mediocre AI implementing this
script must not need to guess any of: parameter names, types, defaults, exit
codes, or which package manager to use to bootstrap missing tools.

---

## 1. PowerShell `Param()` Block (Authoritative)

The runner script MUST declare its CLI surface using exactly this `Param()`
block at the top of `run.ps1`:

```powershell
[CmdletBinding()]
Param(
    # Path to powershell.json. Defaults to script directory.
    [Parameter(Mandatory=$false)]
    [string]$ConfigPath = "$PSScriptRoot/powershell.json",

    # Wipe pnpm store, node_modules, Go cache, and dist before building.
    [Parameter(Mandatory=$false)]
    [switch]$Force,

    # Skip launching processes after build (CI / pre-flight use).
    [Parameter(Mandatory=$false)]
    [switch]$BuildOnly,

    # Skip the build phase, run only.
    [Parameter(Mandatory=$false)]
    [switch]$RunOnly,

    # Override port from config (single port only; multi-port stays in JSON).
    [Parameter(Mandatory=$false)]
    [ValidateRange(1,65535)]
    [int]$Port = 0,

    # One of: Debug | Info | Warn | Error. Default: Info.
    [Parameter(Mandatory=$false)]
    [ValidateSet("Debug","Info","Warn","Error")]
    [string]$LogLevel = "Info",

    # Skip the firewall-rule step (requires admin). CI default.
    [Parameter(Mandatory=$false)]
    [switch]$NoFirewall,

    # Skip auto-install of missing dependencies; fail fast instead.
    [Parameter(Mandatory=$false)]
    [switch]$NoBootstrap
)
```

Mutual-exclusion rules (enforced in script body):

| Combination            | Behavior                                                |
|------------------------|---------------------------------------------------------|
| `-BuildOnly -RunOnly`  | Exit `2` with message `BuildOnly and RunOnly are mutually exclusive`. |
| `-Force -RunOnly`      | Exit `2` — `-Force` requires the build phase.            |

---

## 2. Exit Code Contract

| Code | Meaning                                                           |
|-----:|-------------------------------------------------------------------|
| `0`  | Success — all phases (or selected phases) completed.               |
| `2`  | Invalid CLI arguments (mutually exclusive flags, bad port, etc.).  |
| `3`  | `powershell.json` missing or fails JSON-Schema validation.         |
| `4`  | Required dependency missing AND `-NoBootstrap` was set.            |
| `5`  | Dependency bootstrap attempted but failed (network, permission).   |
| `10` | Backend (Go) build failed — `go build` returned non-zero.          |
| `11` | Frontend (pnpm) install failed.                                    |
| `12` | Frontend build (`pnpm build` / `vite build`) failed.               |
| `20` | Firewall rule creation failed AND `-NoFirewall` was NOT set.       |
| `30` | Backend process exited non-zero during run phase.                  |
| `40` | Port already in use AND no fallback port defined.                  |
| `99` | Unhandled exception — full stack trace written to `run.log`.       |

> Codes `1` and `6–9` are reserved; do not emit them.

---

## 3. Dependency Toolchain (Pinned)

The runner MUST treat the following minimum versions as the contract.
On a fresh machine with `-NoBootstrap` absent, missing tools are
installed via the listed provider in priority order.

| Tool   | Min Version | Provider Priority                     | Verification Command         |
|--------|-------------|----------------------------------------|------------------------------|
| Go     | `1.22.0`    | `winget` → direct MSI from go.dev      | `go version`                 |
| Node   | `20.11.0`   | `winget` → `nvm-windows` → direct MSI  | `node --version`             |
| pnpm   | `9.0.0`     | `corepack enable && corepack prepare`  | `pnpm --version`             |
| Git    | `2.40.0`    | `winget`                               | `git --version`              |

Bootstrap rules:

1. Always check `winget --version` first; if absent, fall back to the next
   provider in the list.
2. Never invoke `Set-ExecutionPolicy` globally — use `-Scope Process` if a
   policy change is required.
3. Bootstrap MUST NOT require `Run-As-Administrator` for Go, Node, or pnpm
   (use user-scope installs). Firewall-rule creation is the only admin step
   and is gated behind `-NoFirewall:$false`.
4. If a tool exists but is below the minimum version, log a warning at
   `Warn` level and continue — do not auto-upgrade existing user installs.

---

## 4. JSON Schema Reference

The full `powershell.json` JSON Schema (Draft-07) is owned by
[`schemas/powershell.schema.json`](./schemas/powershell.schema.json).
Validation is mandatory; failures emit exit code `3`.

The runner MUST run validation before any side-effect (no directory
creation, no install, no port binding) so misconfigured projects fail
fast and idempotently.

---

## 5. Cross-References

- [01-configuration-schema.md](./01-configuration-schema.md) — human prose around the JSON Schema
- [04-error-codes.md](./04-error-codes.md) — narrative for each exit code
- [97-acceptance-criteria.md](./97-acceptance-criteria.md) — GWT tests that exercise this contract

---

*Runner Interface Contract — v1.0.0 — 2026-04-27*
