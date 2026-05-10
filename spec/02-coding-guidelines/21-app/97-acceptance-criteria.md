# Acceptance Criteria — 21 App

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/02-coding-guidelines/21-app/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

Specifies the placement and organization rules for application-specific implementation details, workflows, and features to keep them distinct from foundational coding guidelines.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

FOLDER_PATH: spec/02-coding-guidelines/21-app/
CORE_GUIDELINES_PATH: spec/02-coding-guidelines/00-overview.md
ISSUE_TRACKING_PATH: spec/25-app-issues/00-overview.md
ALLOWED_RANGE_CORE: 01-20
ALLOWED_RANGE_APP: 21 (current folder)
VERSION: 3.2.0

---

## Acceptance Criteria

### AC-01: Enforce App-Specific Spec Placement  `[high]`
- **Given** A new specification file defining a concrete application feature (e.g., 'User Login')
- **When** A developer adds application-level feature documentation.
- **Then** The file must be placed within the `spec/02-coding-guidelines/21-app/` directory.
- **Verifies:** 00-overview.md (Placement Rule)

### AC-02: Prevent Foundational Specs in App Folder  `[medium]`
- **Given** A proposed specification file for a reusable utility or cross-cutting concern (e.g., 'Logging Framework')
- **When** A developer categorizes a horizontal/reusable principle.
- **Then** The file must NOT be placed in the `21-app` directory and must instead go into the `01–20` foundational range.
- **Verifies:** 00-overview.md (Placement Rule)

### AC-03: Sequential Numbering of App Specs  `[medium]`
- **Given** A new specification file in the `21-app` folder
- **When** A new markdown file is created in this directory.
- **Then** The filename must follow the numbered prefix convention (e.g., `01-feature-name.md`) as per the Contents section.
- **Verifies:** 00-overview.md (Contents)

### AC-04: Cross-Reference to App Issues  `[low]`
- **Given** An existing app specification in the `21-app` folder that has identified bugs or implementation hurdles
- **When** Reviewing the traceability between feature specs and known issues.
- **Then** The documentation must include or link to a corresponding entry in `spec/25-app-issues/00-overview.md`.
- **Verifies:** 00-overview.md (Cross-References)

### AC-05: Inheritance of Core Coding Guidelines  `[high]`
- **Given** An app-level workflow specification file (e.g., `02-checkout-flow.md`)
- **When** Validating the architectural alignment of app-specific workflows.
- **Then** It must reference the core 'Coding Guidelines Spec' at `../00-overview.md` for shared standards.
- **Verifies:** 00-overview.md (Cross-References)

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)