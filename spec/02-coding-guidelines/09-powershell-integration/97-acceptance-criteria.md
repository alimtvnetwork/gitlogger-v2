# Acceptance Criteria — 09 Powershell Integration

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/02-coding-guidelines/09-powershell-integration/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

Defines the standards for PowerShell scripting within the project, focusing on cross-platform compatibility, naming conventions, and robust error handling to ensure seamless integration with the broader software ecosystem.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

### PowerShell Integration Standards
- **Runtime:** PowerShell Core 7.x (pwsh)
- **Error Action:** MUST use `$ErrorActionPreference = 'Stop'`
- **Naming Conventions:**
  - Functions: `Verb-Noun` (PascalCase, e.g., `Get-ProjectConfig`)
  - Variables: `$camelCase` (e.g., `$targetPath`)
- **Required Param Attributes:** `[Parameter(Mandatory=$true)]`
- **Output:** MUST use `Write-Output` for data and `Write-Error` for failures; `Write-Host` is prohibited except for UI-only scripts.

---

## Acceptance Criteria

### AC-01: Naming Convention Enforcement  `[high]`
- **Given** A PowerShell script within the project repository
- **When** The script is submitted for integration into the ecosystem
- **Then** The script must utilize 'PascalCase' for function names and 'camelCase' for private variables, adhering to the Project Coding Guidelines.
- **Verifies:** 00-overview.md

### AC-02: Cross-Platform Compatibility Compliance  `[critical]`
- **Given** A cross-platform automation task requiring PowerShell
- **When** Targeting multiple operating systems as defined in the project ecosystem
- **Then** The script must strictly use PowerShell Core (pwsh) syntax to ensure compatibility with both Linux (bash-like environments) and Windows.
- **Verifies:** 00-overview.md

### AC-03: Safe Execution with ShouldProcess  `[high]`
- **Given** A PowerShell script performing data mutations or system changes
- **When** The function impacts system state or persistent data
- **Then** The script must implement SupportsShouldProcess and honor the '-WhatIf' and '-Confirm' parameters to prevent accidental side effects.
- **Verifies:** 00-overview.md

### AC-04: Standardized Parameter Validation  `[medium]`
- **Given** A script requiring external configuration or environment variables
- **When** Inputs are passed to the PowerShell integration module
- **Then** Validation must happen via 'Param()' blocks using '[ValidateSet()]' or '[ValidateRange()]' instead of manual 'if' checks.
- **Verifies:** 00-overview.md

### AC-05: Error Handling and Termination Control  `[high]`
- **Given** A PowerShell module or script encountering a failure (e.g., file not found)
- **When** An exception occurs during automated execution
- **Then** The script must use '$ErrorActionPreference = "Stop"' and 'try/catch' blocks to ensure compatibility with the project's global error handling strategy.
- **Verifies:** 00-overview.md

### AC-06: In-Script Documentation Standards  `[low]`
- **Given** The PowerShell integration module version 3.2.0
- **When** Inspecting script source code for developer maintainability
- **Then** Help documentation MUST be provided via Comment-Based Help (CBH) including '.SYNOPSIS' and '.EXAMPLE' sections.
- **Verifies:** 00-overview.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)