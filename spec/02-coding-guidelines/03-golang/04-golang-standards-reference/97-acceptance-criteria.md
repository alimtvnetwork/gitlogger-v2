# Acceptance Criteria — 04 Golang Standards Reference

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/02-coding-guidelines/03-golang/04-golang-standards-reference/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

Strict Golang standards enforcing PascalCase file naming, a 15-line function limit, zero nested 'if' blocks, and mandatory use of the 'apperror' package and 'dbutil' wrappers over raw errors and queries.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

[File Naming Exceptions]
Standard library interfaces: MarshalJSON, UnmarshalJSON, Error, String.

[apperror Result Methods]
- Single result: IsDefined(), IsEmpty(), HasError(), IsSafe(), Value(), AppError(), StackTrace()
- Multi result: HasAny(), IsEmpty(), Count(), HasError(), IsSafe(), Items(), First(), AppError(), StackTrace()

[dbutil Types]
- Result[T], ResultSet[T], ExecResult

[apperror Error Codes examples]
- "E5001" (General failure), "E1001" (Business logic), etc.

[Directory Structure]
- enums: internal/enums/[enumname]type/
- packages: internal/services/[domainname]/ (no underscores, lowercase)
- file suffixes: _crud.go, _helpers.go, _validation.go, _json.go

---

## Acceptance Criteria

### AC-01: File naming must match primary struct  `[high]`
- **Given** A struct named `PluginService` defined in a new file
- **When** Creating or renaming a Go source file
- **Then** The file must be named `PluginService.go` (PascalCase, no underscores) and the package directory must be lowercase (e.g., `pluginservice/`)
- **Verifies:** 01-file-and-function-rules.md, 04-naming-and-organization.md

### AC-02: File size limit and mandatory notation  `[medium]`
- **Given** A Go source file exceeding 300 lines (target) but under 400 lines (hard limit)
- **When** Static analysis or manual review of file length
- **Then** The file must contain the exact comment: `// NOTE: Needs refactor — exceeds 300-line target` at the top.
- **Verifies:** 01-file-and-function-rules.md

### AC-03: Strict function line count limit  `[high]`
- **Given** A function body with more than 15 lines of code
- **When** Implementing function logic
- **Then** The function must be decomposed into small helpers to satisfy the <= 15 line limit.
- **Verifies:** 01-file-and-function-rules.md

### AC-04: Absolute ban on nested if blocks  `[critical]`
- **Given** A conditional check requiring a negative or nested check (e.g., `if err != nil { if resp != nil { ... } }`)
- **When** Writing conditional logic
- **Then** The code must use flat logic with positive named booleans (e.g., `hasIssue := hasError && hasResp; if hasIssue { ... }`) and zero nested `if` blocks.
- **Verifies:** 01-file-and-function-rules.md

### AC-05: Abbreviation casing standardization  `[medium]`
- **Given** An identifier containing an abbreviation like 'URL', 'API', or 'JSON'
- **When** Naming variables, fields, or functions
- **Then** The identifier must use first-letter-only capitalization (e.g., `BaseUrl`, `ApiKey`, `parseJson`) except for standard library interface methods like `MarshalJSON`.
- **Verifies:** 01-file-and-function-rules.md

### AC-06: Mandatory apperror usage for services  `[critical]`
- **Given** A service layer function that can return an error
- **When** Defining error return paths in application code
- **Then** It must return `apperror.Result[T]` or `*apperror.AppError`, use `apperror.New` or `apperror.Wrap` for stack traces, and never return a raw Go `error` except at framework boundaries.
- **Verifies:** 02-type-safety-and-errors.md

### AC-07: Ban on interface{} in exported APIs  `[high]`
- **Given** An exported API function signature
- **When** Defining public-facing function signatures
- **Then** It must not use `interface{}` or `any`; it must use concrete types or Go generics.
- **Verifies:** 02-type-safety-and-errors.md

### AC-08: Omission of redundant JSON tags  `[low]`
- **Given** A struct intended for JSON marshaling where Go field names match the desired JSON keys (PascalCase)
- **When** Defining struct tags for JSON serialization
- **Then** Redundant `json:"FieldName"` tags must be omitted; only `json:",omitempty"` or `json:"-"` are permitted.
- **Verifies:** 03-database-and-structs.md

### AC-09: Enum naming and guard standards  `[medium]`
- **Given** An enum implementation with `variantLabels`
- **When** Creating byte-based enums
- **Then** The labels in the string array must use PascalCase (e.g., `PerTable`) and the code must use positive guard methods (e.g., `v.IsInvalid()`) instead of raw negations (`!v.IsValid()`).
- **Verifies:** 05-enums-and-dry.md, 06-concurrency-and-patterns.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)