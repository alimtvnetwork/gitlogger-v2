# Acceptance Criteria — 15 Master Coding Guidelines

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/02-coding-guidelines/01-cross-language/15-master-coding-guidelines/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

This module defines the universal naming, logic, and structural standards across PHP, Go, and TypeScript. It enforces positive boolean patterns, single-return values in Go, strict abbreviation formatting, and the elimination of magic strings and nested logic.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

ENUMS:
- StatusType: { Success, Pending, Error }
- EntityStatus: { Active, Inactive, Deleted }
- HttpMethodType: { Get, Post, Put, Delete }
- ResponseKeyType: { SnapshotId, PluginSlug, SiteId }

ERROR CODES:
- E{category}xxx (e.g., EDB001 for database error)
- apperror.ErrDatabase
- apperror.ErrUploadFailed

NAMING:
- Abbreviations: Id, Url, Md5, Json, Api, Ip, Sql, Http, Html, Yaml, Xml, Css, Db.
- Exceptions: MarshalJSON, UnmarshalJSON, r.URL.Path (stdlib).

GO WRAPPERS (Single Return):
- apperror.Result[T] (Methods: .Value(), .HasError(), .AppError())
- apperror.Ok(payload)
- apperror.Fail(err)

GUARDS:
- isDefined(), isDefinedAndValid(), isEmpty(), isInvalid()

LINT LIMITS:
- Go file: max 300 lines
- Function body: max 15 lines
- Nesting: 0 nested ifs allowed (use early returns)

---

## Acceptance Criteria

### AC-01: Abbreviation Capitalization Consistency  `[high]`
- **Given** An abbreviation like 'JSON' or 'API' in a custom Go struct field or PHP variable name
- **When** Defining a new identifier in any language
- **Then** The identifier MUST be formatted with only the first letter capitalized (e.g., 'Json', 'Api'), except for Go standard library overrides like 'MarshalJSON'
- **Verifies:** 01-naming-and-database.md#12-abbreviation-standard-all-languages

### AC-02: Go Single Return Value Enforcement  `[critical]`
- **Given** A Go function signature that needs to return both data and an error status
- **When** Defining custom function signatures in Go code
- **Then** The function MUST return exactly one value using 'apperror.Result[T]' or a custom 'Outcome' struct; multiple returns like '(T, error)' are prohibited
- **Verifies:** 04-type-safety.md#71-single-return-value-rule-go

### AC-03: Positive Boolean Logic Prefixing  `[high]`
- **Given** A boolean variable or function name
- **When** Naming logic-carrying variables or functions
- **Then** It MUST start with 'is' or 'has' and MUST NOT contain negative words such as 'not', 'no', or 'non' (e.g., use 'isPending' instead of 'isNotReady')
- **Verifies:** 02-boolean-and-enum.md#6-non-negotiable-principles

### AC-04: Positive Null Guard Usage  `[medium]`
- **Given** A complex condition requiring a null check and a validity check (e.g., '$x !== null && $x->isValid()')
- **When** Implementing existence checks for objects or pointers
- **Then** It MUST be replaced by a single positive guard method like 'isDefinedAndValid()' or 'isDefined()'
- **Verifies:** 02-boolean-and-enum.md#31-isdefined--isdefinedandvalid--positive-nullexistence-guards

### AC-05: Function Length and Nesting Limits  `[medium]`
- **Given** A Go function body or PHP method body
- **When** Refactoring or writing logic blocks
- **Then** The body MUST NOT exceed 15 lines of code and MUST NOT contain any nested 'if' statements (nesting level 0)
- **Verifies:** 03-code-style-and-errors.md#5-code-style--formatting-rules

### AC-06: Magic String Elimination for Statuses  `[high]`
- **Given** A status comparison like 'if (status === "active")' or 'if (participant.Status == "active")'
- **When** Comparing variables against categorical string values
- **Then** The string literal MUST be replaced with a reference to a domain enum (e.g., 'EntityStatus.Active' or 'entitystatus.Active')
- **Verifies:** 05-magic-strings-and-organization.md#82-domain-status-comparisons

### AC-07: PascalCase File Naming for Types  `[medium]`
- **Given** A source file defining a single primary class or struct like 'SnapshotManager'
- **When** Creating new source code files
- **Then** The file MUST be named 'SnapshotManager.go' or 'SnapshotManager.php' using PascalCase, matching the type definition exactly
- **Verifies:** 01-naming-and-database.md#13-source-file-naming-pascalcase-all-languages

### AC-08: Context and API Key Casing Rules  `[medium]`
- **Given** A log context array in PHP or an API response key
- **When** Returning JSON responses or logging events
- **Then** Log keys MUST use camelCase (e.g., 'postId') while API/JSON keys MUST use PascalCase (e.g., 'PluginSlug')
- **Verifies:** 05-magic-strings-and-organization.md#10-array-key-conventions-php-specific

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)