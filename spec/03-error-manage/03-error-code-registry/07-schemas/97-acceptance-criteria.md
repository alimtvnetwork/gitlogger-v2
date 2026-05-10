# Acceptance Criteria — 07 Schemas

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/03-error-manage/03-error-code-registry/07-schemas/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

Defined JSON schema specifications for the Error Code Registry to ensure consistent error data structures, including severity enums, regex-validated codes, and HTTP mappings.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

### Error Code Registry Schema Constraints
- **Validation Constants**: 
    - `ErrorCodeRegex`: `^[A-Z]{2,4}-[0-9]{4}$`
    - `SeverityEnum`: `["FATAL", "ERROR", "WARN", "INFO", "DEBUG"]`
    - `HTTPRange`: `400` to `599` inclusive
- **Required Fields (Error Definition)**:
    - `code`: string (unique identifier)
    - `message_template`: string (ICU MessageFormat recommended)
    - `severity`: enum
    - `category`: string (foreign key to Categories)
- **Required Fields (Category Definition)**:
    - `id`: string (uppercase, no spaces)
    - `description`: string (min 10 chars)
- **JSON Schema Versions**: Targeting Draft 7 or 2020-12 compat.

---

## Acceptance Criteria

### AC-01: Validate error code string format  `[critical]`
- **Given** A JSON instance representing an error code definition
- **When** Processed by the registry schema validator
- **Then** The instance must validate against a required 'code' field following the regex pattern '^[A-Z]{2,4}-[0-9]{4}$' (e.g., AUTH-0401)
- **Verifies:** Error code registry JSON schemas

### AC-02: Mandatory severity enum validation  `[high]`
- **Given** An error definition JSON object
- **When** The registry schema is applied to a new error entry
- **Then** The schema must enforce a mandatory 'severity' field restricted to enum values [FATAL, ERROR, WARN, INFO, DEBUG]
- **Verifies:** Error code registry JSON schemas

### AC-03: HTTP status code range constraint  `[medium]`
- **Given** The 'http_mapping' property in the error schema
- **When** Mapping internal errors to outward facing HTTP responses
- **Then** The value must be a valid RFC 9110 HTTP status code within the range 400-599
- **Verifies:** Error code registry JSON schemas

### AC-04: Ensure minimum documentation length  `[medium]`
- **Given** A JSON object representing an error category
- **When** Registering a new error category in the schema
- **Then** The schema must require a 'description' field with a minimum length of 10 characters to ensure meaningful documentation
- **Verifies:** Error code registry JSON schemas

### AC-05: Standardize dynamic error parameters  `[high]`
- **Given** An error schema definition with parameters
- **When** The template engine parses valid error data against the schema
- **Then** The 'parameters' object must define keys as strings and values must specify a 'type' from [string, number, boolean] for dynamic message injection
- **Verifies:** Error code registry JSON schemas

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)