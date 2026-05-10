# Acceptance Criteria — 07 Php Standards Reference

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/02-coding-guidelines/04-php/07-php-standards-reference/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

This module establishes strict PHP coding standards for naming (PSR-4/PSR-12), error handling using Throwable and safeExecute wrappers, centralized constant/enum usage, and a zero-tolerance policy for nested if-statements and magic strings. It also mandates the use of a TypedQuery database wrapper and PathHelper for filesystem access.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

{
  "Enums": {
    "HookType": "includes/Enums/HookType.php - Backed Enum (Init, RestApiInit, PluginsLoaded, etc.)",
    "HttpMethodType": "includes/Enums/HttpMethodType.php - Backed Enum (Get, Post, Put, Delete)",
    "CapabilityType": "includes/Enums/CapabilityType.php - Backed Enum (ManageOptions, etc.)",
    "ErrorType": "includes/Enums/ErrorType.php - Enum containing FATAL_TYPES = [E_ERROR, E_CORE_ERROR, E_COMPILE_ERROR]"
  },
  "ErrorChecking": {
    "ErrorChecker::isFatalError($error)": "Checks if error type is in FATAL_TYPES; handles null safely.",
    "ErrorChecker::isInvalidPdoExtension()": "Centralized check for PDO and pdo_sqlite."
  },
  "DatabaseEnvelopes": {
    "DbResult": "Methods: isDefined(), isEmpty(), hasError(), isSafe(), value(), error(), stackTrace()",
    "DbResultSet": "Methods: hasAny(), isEmpty(), count(), items(), first()",
    "DbExecResult": "Methods: affectedRows(), lastInsertId()"
  },
  "ForbiddenStrings": [
    "RISEUP_ prefix in constants",
    "wp_die() in REST (use wp_send_json_error)",
    "error_log() (use FileLogger)",
    "!$obj->isActive() (use $obj->isDisabled())"
  ]
}

---

## Acceptance Criteria

### AC-01: Enum File Naming and Suffixing  `[high]`
- **Given** A class file in the `includes/Enums/` directory
- **When** Implementing a new PHP 8.1+ native backed enum
- **Then** The filename must follow `{PascalCase}Type.php` and contain a backed enum with the same name (e.g., `UploadSourceType.php` contains `enum UploadSourceType: string`)
- **Verifies:** 01-naming-and-errors.md/Naming Conventions

### AC-02: Requirement to Catch Throwable vs Exception  `[critical]`
- **Given** An endpoint handler or business logic function
- **When** Handling potential run-time failures or fatal errors
- **Then** The code must wrap operations in a `try...catch(Throwable $e)` block, specifically catching `Throwable` to include PHP 7+ Errors like `TypeError` or `Error`.
- **Verifies:** 01-naming-and-errors.md/Rule: Catch Throwable, not just Exception

### AC-03: Mandatory Enum Usage for Hooks/Methods  `[high]`
- **Given** A WordPress REST API registration or hook call
- **When** Registering actions, filters, or REST routes
- **Then** Hook names must be accessed via `HookType::{Case}->value` and HTTP methods via `HttpMethodType::{Case}->value`. All magic strings for these are forbidden.
- **Verifies:** 02-constants-and-deps.md/Hook Names — HookType enum

### AC-04: Constant Composition and Naming Prefixes  `[medium]`
- **Given** Definition of constants in `constants.php`
- **When** Defining application-wide identifiers
- **Then** No constant may use the `RISEUP_` prefix, and complex values (URLs/Hook strings) must be pre-composed into named constants rather than concatenated at the call site.
- **Verifies:** 02-constants-and-deps.md/Action Names — Named Composed Constants

### AC-05: Lazy Initialization of WordPress Hooks  `[critical]`
- **Given** A class requiring WordPress registration (e.g., `add_action`)
- **When** Instantiating plugin components
- **Then** The `__construct` method must be empty of WordPress function calls; instead, a public `initialize()` method with an `$isInitialized` guard must be used.
- **Verifies:** 03-initialization-and-booleans.md/Rule: Lazy initialization with HookType enum

### AC-06: Deprecation of Trivial Boolean Wrappers  `[low]`
- **Given** A boolean check on a property or object state
- **When** Evaluating truthiness or nullability
- **Then** The code must use native PHP operators (`!$x`, `empty($x)`) instead of the deprecated `BooleanHelpers::isFalsy()` or `BooleanHelpers::isEmpty()`.
- **Verifies:** 03-initialization-and-booleans.md/Prohibited Trivial Wrappers (deprecated since 1.19.0)

### AC-07: Typed Path Resolution Rule  `[high]`
- **Given** A file path resolution in the codebase
- **When** Accessing the filesystem or database files
- **Then** The path must be retrieved via a typed accessor in `PathHelper` (e.g., `PathHelper::getRootDb()`) which uses `PathConst` internal constants; string concatenation like `$dir . '/file.db'` is prohibited.
- **Verifies:** 02-constants-and-deps.md/Rule: Use fully-typed path accessors backed by PathConst constants

### AC-08: Braces and Zero-Nesting Policy  `[medium]`
- **Given** Logic requiring an `if` statement
- **When** Writing conditional logic
- **Then** The block must always use curly braces `{ }`, even for single-line returns, and must never contain a nested `if` statement (flatten using early returns instead).
- **Verifies:** 04-code-style.md/Rule 1: Always use braces / Rule 2: Zero nested if

### AC-09: Extraction of Multi-part Conditions  `[medium]`
- **Given** A complex conditional with two or more operators (e.g., `&&`, `||`)
- **When** Evaluating complex business rules in a conditional
- **Then** The condition must be extracted into a named boolean variable (e.g., `$isAuthorized`) or a dedicated guard method so the `if` statement reads as a single intent.
- **Verifies:** 04-code-style.md/Rule 3: Extract complex conditions

### AC-10: Typed Database Wrapper Usage  `[high]`
- **Given** A database interaction requiring a single row or multi-row result set
- **When** Executing SQL queries against PDO
- **Then** The code must use `TypedQuery` methods (`queryOne`, `queryMany`) which return `DbResult<T>` or `DbResultSet<T>` envelopes containing state checks like `isDefined()` or `hasError()`.
- **Verifies:** 05-forbidden-and-database.md/Database Wrapper — TypedQuery

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)