# Acceptance Criteria — 04 Code Style

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/02-coding-guidelines/01-cross-language/04-code-style/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

This module defines cross-language coding standards for PHP, TypeScript, and Go, prioritizing flat control flow, strict function size limits (15 lines), and explicit multi-line formatting for complex calls and conditions.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.


Enum/Const Guidelines:
- Switch cases for enums MUST NOT use raw string literals.
- Enums must have defined string constants (e.g., EnvironmentType::Production).

Formatting Logic:
- Rules apply to: PHP, TypeScript, Go.
- Function Body Max: 15 effective lines.
- Type/Class/Struct Max: 120 lines.
- Multi-line threshold: > 2 arguments or > 2 array items.
- Spacing: 1 space after '//' comment markers.
- Error Handling Exemption: 'if err != nil', 'apperror.Wrap', 'FailWrap', and '.WithX()' chains do not count toward the 15-line function limit.


---

## Acceptance Criteria

### AC-01: Enforce Mandatory Braces for All Control Flow  `[high]`
- **Given** A PHP or TypeScript function containing an `if` statement with a single-line body like `if ($init) return;`
- **When** The code is passed through a linter or manual review.
- **Then** The code must be rejected until it uses curly braces `{}` as per Rule 1.
- **Verifies:** 01-braces-and-nesting.md/Rule 1: Always Use Braces — No Single-Line Statements

### AC-02: Zero Tolerance for Nested If Blocks  `[critical]`
- **Given** A Go function with a nested `if` structure like `if err != nil { if resp != nil { ... } }`
- **When** Any nested if-block is detected in PHP, TS, or Go.
- **Then** The code must be rejected and refactored using named booleans (e.g., `hasIssue := hasError && hasResponse`) and flat logic.
- **Verifies:** 01-braces-and-nesting.md/Rule 2: Zero Nested if — Absolute Ban

### AC-03: Extract Complex Multi-Part Conditions  `[medium]`
- **Given** An `if` condition using two or more operators, such as `if ($A && $B || $C)`
- **When** A condition contains &&, ||, or ! in combination.
- **Then** It must be refactored into a named boolean variable (e.g., `$isAuthorized`), a method, or a constant.
- **Verifies:** 02-conditions-and-extraction.md/Rule 3: Extract Complex Conditions

### AC-04: Blank Line Before Return or Throw When Preceded by Statements  `[low]`
- **Given** A function body containing logic followed immediately by a `return` or `throw` without a line break
- **When** There are multiple statements in the block.
- **Then** A blank line must be inserted before the exit statement to separate logic from exit as per Rule 4.
- **Verifies:** 03-blank-lines-and-spacing.md/Rule 4: Blank Line Before return or throw When Preceded by Other Statements

### AC-05: Function Limit Enforcement with Error Handling Exemption  `[medium]`
- **Given** A function exceeding 15 lines of body code
- **When** Calculating the effective length of a business logic function.
- **Then** The line count must exclude lines containing `if err != nil`, `apperror.Wrap()`, or `FailWrap()` chains before being compared against the limit.
- **Verifies:** 04-function-and-type-size.md/Rule 6: Maximum 15 Lines Per Function

### AC-06: Multi-Line Formatting for Functions with >2 Arguments  `[high]`
- **Given** A function signature or call with 3 or more arguments
- **When** Arguments exceed the limit of two.
- **Then** Every argument must be placed on its own line with a trailing comma (syntax permitting).
- **Verifies:** 05-multi-line-formatting.md/Rule 9: Multi-Line Arguments

### AC-07: No Leading Backslash on Global PHP Types  `[low]`
- **Given** A PHP file with a catch block using `\Throwable`
- **When** Catching global exceptions or using global type hints in PHP.
- **Then** The leading backslash must be removed to use `Throwable` directly.
- **Verifies:** 06-comments-and-documentation.md/Rule 8: No Leading Backslash on Global Types

### AC-08: Mandatory Doc Comments for Public API  `[medium]`
- **Given** A public or exported function/method in any supported language
- **When** The function is accessible outside its local scope.
- **Then** A doc comment describing the purpose of the function must be present.
- **Verifies:** 06-comments-and-documentation.md/Rule 16: Method and Function Documentation

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)