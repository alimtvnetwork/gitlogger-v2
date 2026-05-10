# Acceptance Criteria — 11 Security

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/02-coding-guidelines/11-security/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

This module establishes security coding guidelines and strict dependency version control policies, specifically mandating pinning for the Axios library to prevent the use of versions with known vulnerabilities (1.14.1 and 0.30.4).

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

### Axios Version Matrix
| Version Category | Exact Version | Status |
| :--- | :--- | :--- |
| Preferred | 1.14.0 | APPROVED |
| Legacy | 0.30.3 | APPROVED |
| Vulnerable | 1.14.1 | BLOCKED |
| Vulnerable | 0.30.4 | BLOCKED |
| Other | Any other | BLOCKED (Pending Manual Approval) |

### Security Document Structure
Required files for subfolders:
1. 00-overview.md
2. 01-implementation-rules.md
3. 02-security-notes.md
4. 99-consistency-report.md

---

## Acceptance Criteria

### AC-01: Strict Axios Version Pinning  `[critical]`
- **Given** A project `package.json` file or dependency manifest
- **When** The AI or developer adds or updates the Axios library
- **Then** The Axios dependency MUST be pinned exactly to either `1.14.0` or `0.30.3` with no range operators (e.g., no `^` or `~`).
- **Verifies:** 01-axios-version-control/00-overview.md

### AC-02: Blocked Vulnerable Version 1.14.1  `[critical]`
- **Given** A requirement to update dependencies to the latest patch version
- **When** Version 1.14.1 is proposed or found in the codebase
- **Then** The version `1.14.1` MUST be rejected and flagged as blocked due to confirmed security vulnerabilities.
- **Verifies:** 01-axios-version-control/00-overview.md

### AC-03: Blocked Vulnerable Version 0.30.4  `[critical]`
- **Given** A legacy project requiring a 0.x.x version of Axios
- **When** Version 0.30.4 is proposed or found in the codebase
- **Then** The version `0.30.4` MUST be rejected and flagged as blocked due to confirmed security vulnerabilities.
- **Verifies:** 01-axios-version-control/00-overview.md

### AC-04: Security Subfolder Template Compliance  `[medium]`
- **Given** A new subfolder creation within `11-security/` for a new security topic
- **When** A new security policy (e.g., input sanitization) is added
- **Then** The subfolder MUST contain at least four specific files: `00-overview.md`, `01-implementation-rules.md`, `02-security-notes.md`, and `99-consistency-report.md`.
- **Verifies:** 00-overview.md

### AC-05: Unverified Version Default Deny  `[high]`
- **Given** A developer attempting to use an unlisted version of Axios (e.g., 1.15.0)
- **When** An unlisted version is detected in configuration
- **Then** The version MUST be treated as `BLOCKED` until it undergoes manual verification and is added to the Version Matrix.
- **Verifies:** 01-axios-version-control/00-overview.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)