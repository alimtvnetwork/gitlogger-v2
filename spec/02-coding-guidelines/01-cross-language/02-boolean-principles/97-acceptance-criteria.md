# Acceptance Criteria — 02 Boolean Principles

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/02-coding-guidelines/01-cross-language/02-boolean-principles/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

This module defines architectural standards for boolean logic, focusing on naming prefixes (is/has), elimination of negative semantic words, and the extraction of complex logical expressions into named guards. It enforces explicit parameter passing and prohibits inline assignments or raw system calls within conditions.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

{
  "Linter_Codes": {
    "BOOL-NEG-001": "Rejects 'Not'/'No'-prefixed database column names at CI time.",
    "CODE-RED-002": "Linter rule enforcing boolean naming prefixes with specific allowlists."
  },
  "Universal_Exempt_Names": ["ok", "err", "error", "true", "false"],
  "Go_Only_Exempt_Names": ["done", "found", "exists"],
  "Database_Rule": "Rule 9: Inverted sibling fields (e.g., IsInactive) must be computed in code, never stored as a second DB column.",
  "P4_Limits": {
    "Max_Operands": 2,
    "Mixing": "Forbidden (&& with ||, or positive with negative)"
  }
}

---

## Acceptance Criteria

### AC-01: Mandatory Boolean Naming Prefixes (P1)  `[high]`
- **Given** A boolean variable, property, or method name such as '$active', 'loading', or 'blocked'
- **When** Defined in PHP, TypeScript, or Go (excluding Go-specific exemptions like 'ok')
- **Then** The linter or reviewer must flag it for missing the mandatory 'is' or 'has' prefix required by P1.
- **Verifies:** 01-naming-prefixes.md

### AC-02: Banned Negative Words in Booleans (P2)  `[critical]`
- **Given** A boolean identifier containing negative words like 'isNotReady', 'hasNoPermission', or 'isNotBlocked'
- **When** Naming variables, functions, or methods in any supported language
- **Then** Reject the name and require a positive semantic synonym like 'isPending', 'isUnauthorized', or 'isActive' as per P2.
- **Verifies:** 01-naming-prefixes.md

### AC-03: Replace Raw Negation with Named Guards (P3)  `[high]`
- **Given** A raw negation on a function call or existence check (e.g., '!$order->isValid()')
- **When** Performing negative checks at call sites
- **Then** The code must be refactored to use a named guard (e.g., '$order->isInvalid()') as required by P3.
- **Verifies:** 02-guards-and-extraction.md

### AC-04: Decompose Complex Boolean Expressions (P4a)  `[medium]`
- **Given** A boolean expression containing 3 or more operands (e.g., 'a && b && c')
- **When** Evaluating logic in control flow statements
- **Then** The logic must be decomposed into intermediate named booleans with a maximum of two conditions per expression (P4a).
- **Verifies:** 02-guards-and-extraction.md

### AC-05: No Mixed Logical Operators (P4b)  `[high]`
- **Given** A boolean expression mixing operators (e.g., 'isAdmin && hasPermission || isSuperUser')
- **When** Combining '&&' and '||' in a single expression
- **Then** Reject the expression and require extraction into named variables to resolve ambiguity (P4b).
- **Verifies:** 02-guards-and-extraction.md

### AC-06: Explicit Boolean Parameters (P5)  `[high]`
- **Given** A function call using a bare boolean literal like 'fetchData(userId, true)'
- **When** Passing boolean arguments to functions or methods
- **Then** Require refactoring to named methods or an options object (e.g., '{ isUseCache: true }') as per P5.
- **Verifies:** 03-parameters-and-conditions.md

### AC-07: No Mixed Polarity in Conditions (P6)  `[medium]`
- **Given** An 'if' condition combining a positive and negative boolean (e.g., 'isReady && !isOverwrite')
- **When** Writing complex 'if' statements with mixed '!isX' patterns
- **Then** The condition must be extracted into a single named boolean with positive intent like 'isConflict' (P6).
- **Verifies:** 03-parameters-and-conditions.md

### AC-08: No Inline Statements in Conditions (P7)  `[high]`
- **Given** An inline assignment inside a control flow condition (e.g., 'if x := fn(); x > 0') in PHP or TypeScript
- **When** Defining logic in 'if' or 'while' blocks
- **Then** The linter must reject it; assignments must be separate from conditions except for Go's comma-ok pattern (P7).
- **Verifies:** 03-parameters-and-conditions.md

### AC-09: No Raw System/Filesystem Calls (P8)  `[high]`
- **Given** Raw filesystem calls like 'os.Stat' or 'os.MkdirAll' in Go source code
- **When** Performing IO or environment-level boolean checks
- **Then** The code must be replaced with 'pathutil' wrappers (e.g., 'pathutil.IsDir', 'pathutil.EnsureDir') and 'apperror' for errors (P8).
- **Verifies:** 03-parameters-and-conditions.md

### AC-10: Static Factory Constructor Exemption  `[low]`
- **Given** Static factory constructor methods like 'DbResult::empty()'
- **When** Creating new instances vs querying state
- **Then** These must be permitted without 'is'/'has' prefixes, while 'isEmpty()' query methods must still follow P1.
- **Verifies:** 05-exemptions-and-api.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)