# Acceptance Criteria — 09 Templates

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/03-error-manage/03-error-code-registry/09-templates/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

This module provides the standardized templates and structure for generating and maintaining the project-wide error code registry, ensuring consistent status code mapping and naming conventions across services.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

### Error Code Structure
- **Format:** `[PREFIX]-[RANGE]-[SEQUENCE]` (e.g., `XX-000-01`)
- **Prefix:** 2-character project identifier.

### Standard Mappings
| Category | Range | HTTP Default |
| :--- | :--- | :--- |
| Initialization | 000-099 | N/A |
| Authentication | 100-199 | 401 |
| Authorization | 200-299 | 403 |
| Validation | 300-399 | 400 |
| Business Logic | 400-499 | 422 |
| Database | 500-599 | 500 |
| External Services| 600-699 | 502/503 |
| File System | 700-799 | 500/404 |
| Network | 800-899 | 503/504 |

### Implementation Snippets
- **Go:** `errors.New(ErrXX00001, "Description")`
- **TypeScript:** `throw new AppError(ErrorCodes.XX_000_01, "Description")`

---

## Acceptance Criteria

### AC-01: Strict Error Code Prefix Implementation  `[critical]`
- **Given** The template `01-error-codes-template.md` is used for a new project named "Payments" with prefix "PY"
- **When** A developer populates the template for a specific project.
- **Then** The error code format must strictly follow the `XX-000-00` pattern, resulting in codes like `PY-100-01` for Authentication.
- **Verifies:** 01-error-codes-template.md

### AC-02: Standard Authorization HTTP Status Mapping  `[high]`
- **Given** The Authorization block `XX-200: Authorization (X200-X299)` in the template
- **When** Evaluating the HTTP field for codes between X200-X299.
- **Then** Any error code defined within this range must default to an HTTP status of `403`.
- **Verifies:** 01-error-codes-template.md

### AC-03: Standard Validation HTTP Status Mapping  `[high]`
- **Given** The Validation block `XX-300: Validation (X300-X399)` in the template
- **When** Evaluating the HTTP field for codes between X300-X399.
- **Then** Any error code defined within this range must default to an HTTP status of `400`.
- **Verifies:** 01-error-codes-template.md

### AC-04: Business Logic Error Categorization  `[medium]`
- **Given** The Business Logic block `XX-400: Business Logic (X400-X499)` in the template
- **When** Mapping business rule violations in the template.
- **Then** The resulting HTTP status code must be `422` (Unprocessable Entity).
- **Verifies:** 01-error-codes-template.md

### AC-05: Consistent Cross-Language Constant Naming  `[medium]`
- **Given** The Usage section examples for Go and TypeScript in `01-error-codes-template.md`
- **When** Generating client/server SDKs from the registry.
- **Then** The generated code constants must follow the pattern `ErrXX00001` (Go) or `ErrorCodes.XX_000_01` (TS).
- **Verifies:** 01-error-codes-template.md

### AC-06: Network Error Boundary Constraints  `[high]`
- **Given** The Network range `XX-800: Network (X800-X899)`
- **When** Assigning HTTP codes to network-level failures.
- **Then** The template must permit only `503` or `504` status codes for this specific range.
- **Verifies:** 01-error-codes-template.md

### AC-07: Consistency Reporting Requirements  `[low]`
- **Given** The `99-consistency-report.md` file noted in the inventory
- **When** The error registry is audited for compliance with the template.
- **Then** It must document any deviations from the established ranges or duplicate code assignments within the registry.
- **Verifies:** 99-consistency-report.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)