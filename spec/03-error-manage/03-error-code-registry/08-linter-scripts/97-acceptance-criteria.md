# Acceptance Criteria — 08 Linter Scripts

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/03-error-manage/03-error-code-registry/08-linter-scripts/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

This module defines the requirements for automated linter scripts that maintain the integrity and consistency of the Error Code Registry, ensuring no duplicates or formatting errors exist across the documentation.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

### Error Code Format Contract
- Format: `ERR-[GROUP]-[ID]` (e.g., `ERR-AUTH-0001`)
- Group: 4-character uppercase alphanumeric.
- ID: 4-digit zero-padded integer.

### Consistency Report Schema (99-consistency-report.md)
| Column | Description |
|--------|-------------|
| Code | The error code string (ERR-XXXX-XXXX) |
| Status | [PASS|FAIL|MISSING] |
| Message | Description of the linting violation |
| File Path | Path to the file containing the error |

### Linter Exit Codes
- `0`: Success, no violations found.
- `1`: High/Critical violations found (Duplicates, Missing Codes).
- `2`: Script execution error (I/O, Permissions).

---

## Acceptance Criteria

### AC-01: Detection of Duplicate or Missing Error Codes  `[critical]`
- **Given** A set of error codes defined in the parent Error Code Registry.
- **When** Running the consistency linter script.
- **Then** The linter must identify any gaps in the numerical sequence or duplicate code assignments.
- **Verifies:** Purpose: Error code registry automation scripts

### AC-02: Formatting Validation for Error Identifiers  `[high]`
- **Given** The `99-consistency-report.md` template.
- **When** The linter script executes against the registry directory.
- **Then** The script must generate a report that lists every file from the registry not following the `ERR-VVV-XXXX` naming convention.
- **Verifies:** 99-consistency-report.md

### AC-03: Cross-Reference Validation Between Registry and Code  `[high]`
- **Given** A registered error code that is referenced in source code but missing from the Markdown registry files.
- **When** The linter performs a project-wide scan.
- **Then** The script must flag a 'Dangling Reference' error in the consistency report.
- **Verifies:** 99-consistency-report.md

### AC-04: Schema Compliance for Registry Entries  `[medium]`
- **Given** An error code entry in the registry that lacks a 'Resolution' or 'Severity' field.
- **When** Validating individual error definition files.
- **Then** The linter must mark the entry as 'Incomplete Metadata' in the final report.
- **Verifies:** Purpose: Error code registry automation scripts

### AC-05: Automated Report Summary Generation  `[medium]`
- **Given** The `99-consistency-report.md` output file.
- **When** The linter script completes its execution cycle.
- **Then** The file must include a summary section detailing: Total Errors, Validated, and Failed, along with a timestamp of the run.
- **Verifies:** 99-consistency-report.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)