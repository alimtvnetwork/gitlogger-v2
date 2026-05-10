# Cross-Language Coding Guidelines — Acceptance Criteria

**Version:** 4.1.0
**Last Updated:** 2026-04-29
**Scope:** `spec/02-coding-guidelines/01-cross-language/` — the parent contract that every language-specific subfolder (`02-typescript/`, `03-golang/`, `04-php/`, `05-rust/`, `07-csharp/`) MUST inherit and implement.

---

## Module Summary

§01 cross-language is the **parent contract for every language guideline subfolder under §02**. It codifies the rules that hold true across all 5 supported languages: boolean principles, no-negative naming, strict typing, DRY, SOLID, cyclomatic complexity, magic-value immutability, function/variable/key naming, regex usage, null safety, lazy evaluation, generic return types, types-folder convention, slug conventions, test naming, and database naming. Language subfolders inherit ALL of these and extend with language-specific syntax. Conflicts MUST be resolved in favor of the cross-language rule unless explicitly waived in the language subfolder's `00-overview.md`.

---

## Inlined Contracts

```text
PARENT_FOLDER:             spec/02-coding-guidelines/01-cross-language/
INHERITED_BY:              02-typescript/, 03-golang/, 04-php/, 05-rust/, 07-csharp/
NORMATIVE_FILES:           02-boolean-principles, 03-casting-elimination,
                           04-code-style, 05-cross-spec-contradiction-checks,
                           06-cyclomatic-complexity, 07-database-naming,
                           08-dry-principles, 09-dry-refactoring-summary,
                           10-function-naming, 11-key-naming-pascalcase,
                           12-no-negatives, 13-strict-typing,
                           14-test-naming-and-structure, 15-master-coding-guidelines,
                           16-lazy-evaluation-patterns, 17-regex-usage-guidelines,
                           18-code-mutation-avoidance, 19-null-pointer-safety,
                           20-nesting-resolution-patterns, 21-newline-styling-examples,
                           22-variable-naming-conventions, 23-solid-principles,
                           24-boolean-flag-methods, 25-generic-return-types,
                           26-magic-values-and-immutability, 27-types-folder-convention,
                           28-slug-conventions
KEY_NAMING:                JSON/object keys → PascalCase (NOT camelCase)
                           Function/variable names → language-idiomatic
                           (TS/PHP/C# → camelCase; Go → MixedCaps; Rust → snake_case)
DB_NAMING:                 tables singular PascalCase, columns PascalCase
SLUG_NAMING:               kebab-case ASCII for URL slugs and file names
CYCLOMATIC_COMPLEXITY:     ≤ 10 per function (hard); ≤ 5 preferred
NESTING:                   ≤ 3 levels of conditional/loop nesting per function
MAGIC_VALUES:              all literal strings/numbers used > 1 time MUST be named constants
NEGATIVES:                 boolean names use positive form (`isEnabled` not `isNotDisabled`)
NULL_SAFETY:               every nullable return type explicitly typed (Option/Result/?T/null-union)
TYPES_FOLDER:              shared types → `types/` folder (NOT `interfaces/` or `models/`)
TEST_NAMING:               `<unit>.test.<ext>` adjacent to source OR `tests/` mirror tree
```

---

## Acceptance Criteria

### AC-CL-01 — Every language subfolder under §02 inherits this parent's rules

- **Given** any language subfolder (`02-typescript/`, `03-golang/`, `04-php/`, `05-rust/`, `07-csharp/`),
- **When** its `00-overview.md` is parsed,
- **Then** it MUST contain a "Cross-Language Inheritance" section declaring it inherits all rules from `../01-cross-language/`. Conflicts MUST be resolved in favor of the cross-language rule unless an explicit waiver row appears in the subfolder's `99-consistency-report.md` with justification + date. Subfolders MUST NOT silently override cross-language rules.
- **Verifies:** Inheritance contract + `15-master-coding-guidelines.md`.

### AC-CL-02 — Boolean variable and function names use positive form

- **Given** any boolean variable, function, or class member declaration,
- **When** the name is inspected,
- **Then** it MUST express the positive condition (`isEnabled`, `hasAccess`, `canEdit`, `shouldRetry`). Double-negative names (`isNotDisabled`, `hasNoErrors`, `cannotFail`) are FORBIDDEN. The single exception is when negation reflects an external API contract (e.g. `is_deleted` column on a soft-delete table); the naming MUST then mirror the external contract verbatim with a comment explaining the inheritance.
- **Verifies:** `12-no-negatives.md` + `02-boolean-principles.md`.

### AC-CL-03 — Boolean flag method names ask a question; non-boolean methods describe an action

- **Given** any method or function returning `bool` / `boolean`,
- **When** the name is parsed,
- **Then** it MUST start with one of: `is`, `has`, `can`, `should`, `will`, `was`, `did` (e.g. `isReady()`, `hasPermission()`). Methods returning non-boolean values MUST NOT use these prefixes. Mixing (e.g. a `isUser()` that returns the User object) is FORBIDDEN.
- **Verifies:** `24-boolean-flag-methods.md`.

### AC-CL-04 — Strict typing: no implicit `any`/`interface{}`/`mixed`/`dynamic`

- **Given** any function signature, variable declaration, or struct field,
- **When** type-checked,
- **Then** the type MUST be explicit. Implicit-any (TS without `--strict`), Go `interface{}` without justification, PHP `mixed`, C# `dynamic`, Rust `Box<dyn Any>` are FORBIDDEN unless a code comment cites a specific inability to type the value (e.g. third-party untyped JSON). The waiver MUST be documented inline AND in the file's local README/changelog.
- **Verifies:** `13-strict-typing.md`.

### AC-CL-05 — Casting is replaced by typed conversion or parsing

- **Given** any need to change a value's static type,
- **When** the code is written,
- **Then** it MUST use a typed conversion function (`Number.parseInt`, `strconv.Atoi`, `(int)$x`, `i32::from_str`, `int.Parse`) — NOT a raw cast (`x as Y`, `(Y)x` in TS). Casts that bypass the type system (TS `as unknown as Y`, Go `unsafe.Pointer` reinterpret) are FORBIDDEN outside of FFI boundaries documented with a `// SAFETY:` comment.
- **Verifies:** `03-casting-elimination-patterns.md`.

### AC-CL-06 — Cyclomatic complexity ≤ 10 per function (hard); ≤ 5 preferred

- **Given** any function or method,
- **When** measured by a static-analysis tool (eslint-complexity / gocyclo / phpstan / clippy / sonar),
- **Then** the cyclomatic complexity MUST be ≤ 10. Values 6–10 SHOULD trigger a refactoring discussion in PR review; values > 10 MUST block merge. The preferred ceiling is 5. CI MUST report violations with file + line + measured score.
- **Verifies:** `06-cyclomatic-complexity.md`.

### AC-CL-07 — Conditional/loop nesting ≤ 3 levels per function

- **Given** any function,
- **When** the AST is walked,
- **Then** nested conditionals or loops MUST NOT exceed depth 3. Deeper nesting MUST be refactored using early returns, guard clauses, extract-method, or strategy/lookup tables. The early-return pattern (guard clauses at the top, happy path flat) is preferred over deeply nested `if`/`else`.
- **Verifies:** `20-nesting-resolution-patterns.md`.

### AC-CL-08 — Magic values are extracted to named constants when used > once

- **Given** any literal string or number used in 2+ places within the same module,
- **When** the code is reviewed,
- **Then** it MUST be extracted to a named constant (`const MAX_RETRIES = 3`, `const DEFAULT_TIMEOUT_MS = 5000`). Single-use literals are exempt. Configuration values (timeouts, URLs, limits) MUST always be named, even on first use. Hard-coded environment-specific values (URLs, secrets) are FORBIDDEN — they MUST come from config/env.
- **Verifies:** `26-magic-values-and-immutability.md`.

### AC-CL-09 — Object/JSON keys use PascalCase across all languages

- **Given** any JSON payload, struct field tag, or serialized object key,
- **When** the wire format is inspected,
- **Then** keys MUST be PascalCase (`UserId`, `CreatedAt`, `IsEnabled`). camelCase (`userId`), snake_case (`user_id`), and kebab-case (`user-id`) are FORBIDDEN on the wire. Language-side struct field names MAY follow language idiom (Go `MixedCaps`, Rust `snake_case`) but the JSON tag / serialization attribute MUST emit PascalCase.
- **Verifies:** `11-key-naming-pascalcase.md`.

### AC-CL-10 — Function names follow language idiom; cross-language semantic verbs are consistent

- **Given** any function or method,
- **When** the name is parsed,
- **Then** TS/PHP/C#/Java MUST use `camelCase`, Go MUST use `MixedCaps` (exported `PascalCase`, unexported `camelCase`), Rust MUST use `snake_case`. Across languages, the SAME semantic operation MUST use the SAME verb (a function that fetches a user is `fetchUser` / `FetchUser` / `fetch_user` — never a mix of `getUser`, `loadUser`, `findUser` for the same operation across modules).
- **Verifies:** `10-function-naming.md` + `22-variable-naming-conventions.md`.

### AC-CL-11 — Database tables are singular PascalCase; columns are PascalCase

- **Given** any DDL (`CREATE TABLE`, schema migration),
- **When** the table name and column names are inspected,
- **Then** the table name MUST be singular PascalCase (`User`, `OrderLine` — NOT `users`, `order_lines`). Column names MUST be PascalCase (`Id`, `CreatedAt`, `UserId`). FK columns MUST follow `<TargetTable>Id` (e.g. `UserId` references `User.Id`). Snake_case columns are FORBIDDEN. Lookup tables follow the same rule.
- **Verifies:** `07-database-naming.md`.

### AC-CL-12 — URL slugs and file names use kebab-case ASCII

- **Given** any URL slug, route segment, or file name (other than language-mandated formats),
- **When** the string is inspected,
- **Then** it MUST be kebab-case ASCII (`user-profile`, `forgot-password`). Underscores, dots (other than file extensions), spaces, and uppercase are FORBIDDEN in slugs. Non-ASCII chars MUST be transliterated. The slug MUST match `^[a-z0-9]+(-[a-z0-9]+)*$`.
- **Verifies:** `28-slug-conventions.md`.

### AC-CL-13 — Null safety: every nullable return is explicitly typed

- **Given** any function that may return `null`/`nil`/`None`/missing,
- **When** the signature is parsed,
- **Then** the return type MUST express nullability explicitly: TS `T | null` or `T | undefined`, Go `(T, error)` or pointer `*T`, Rust `Option<T>` or `Result<T, E>`, PHP `?T`, C# `T?`. Returning a nullable value with a non-nullable type is FORBIDDEN. Callers MUST handle the nullable case (no implicit unwrap; Rust `unwrap()` outside test/prototype is FORBIDDEN).
- **Verifies:** `19-null-pointer-safety.md`.

### AC-CL-14 — Lazy evaluation for expensive computations and side-effecting branches

- **Given** any expression that performs I/O, allocates, or runs > O(n),
- **When** it appears inside a conditional branch,
- **Then** it MUST be lazily evaluated (only computed if its branch is taken). Eager evaluation that always pays the cost is FORBIDDEN. Languages: TS `() => expensive()` thunk, Go closures, Rust `||` lazy iterators / `Lazy<T>`, PHP closures, C# `Lazy<T>`. Boolean short-circuit (`&&` / `||`) is the simplest form and MUST be preferred.
- **Verifies:** `16-lazy-evaluation-patterns.md`.

### AC-CL-15 — Regex usage: documented intent, anchored, no catastrophic backtracking

- **Given** any regex literal in source code,
- **When** the regex is reviewed,
- **Then** it MUST: (a) carry an inline comment explaining what it matches and why, (b) be anchored with `^` and `$` (or explicit `\b` word-boundary) when matching whole strings, (c) be tested for catastrophic-backtracking patterns (no nested unbounded quantifiers like `(a+)+`), (d) prefer explicit character classes over `.`, (e) be compiled-once when used in hot paths. Regex without explanation MUST fail PR review.
- **Verifies:** `17-regex-usage-guidelines.md`.

### AC-CL-16 — Code mutation avoidance: prefer immutable data + pure functions

- **Given** any function that takes a parameter,
- **When** the function body is inspected,
- **Then** it MUST NOT mutate the parameter (no `arr.push()` on input array, no `obj.field = x` on input object, no Go slice append that aliases the input). Returning a new value is mandatory. Exceptions: explicit "in-place" functions MUST be named with `mutate*`/`update*In*Place` prefix and MUST document the mutation in the function comment. Variables declared with `let`/`var` SHOULD be re-evaluated; `const`/`final`/`readonly` is preferred.
- **Verifies:** `18-code-mutation-avoidance.md`.

### AC-CL-17 — Generic return types: prefer Result/Option/Either over throwing

- **Given** any function that can fail,
- **When** the signature is designed,
- **Then** it MUST return a generic Result-like type (`Result<T, E>` in Rust, `(T, error)` in Go, custom `Result<T>` in TS/PHP/C#) — NOT throw an exception for expected failures. Exceptions are reserved for truly exceptional conditions (programmer errors, OOM, panic). Network errors, validation errors, parse errors are EXPECTED → MUST use Result.
- **Verifies:** `25-generic-return-types.md`.

### AC-CL-18 — Shared types live in a `types/` folder (NOT `interfaces/` or `models/`)

- **Given** any folder containing shared type/interface/struct definitions,
- **When** the folder is named,
- **Then** it MUST be named `types/`. The names `interfaces/`, `models/`, `dto/`, `entities/` are FORBIDDEN as folder names. Inside `types/`, files SHOULD be grouped by domain (`types/user.ts`, `types/order.ts`) — NOT by category (`types/interfaces.ts`, `types/types.ts`). Type definitions colocated with their primary consumer are exempt from this rule.
- **Verifies:** `27-types-folder-convention.md`.

### AC-CL-19 — Tests are named `<unit>.test.<ext>` and live adjacent to source OR in mirror `tests/` tree

- **Given** any test file,
- **When** the file path is inspected,
- **Then** the file name MUST end with `.test.<ext>` (TS `.test.ts`, Go `_test.go`, PHP `Test.php`, Rust `#[cfg(test)] mod tests` inline, C# `.Tests.cs`). Tests MUST live adjacent to the source file (`user.ts` ↔ `user.test.ts`) OR in a mirror `tests/` tree that preserves the source path. Test functions MUST be named `test_<behavior>` / `it_<behavior>` / `Test<Behavior>` describing the BEHAVIOR being tested, not the function name.
- **Verifies:** `14-test-naming-and-structure.md`.

### AC-CL-20 — DRY without premature abstraction: extract on rule-of-three, not first duplication

- **Given** any code duplication observed across the codebase,
- **When** the third instance of the duplication appears,
- **Then** the shared logic MUST be extracted into a reusable function/module. Extracting on the FIRST or SECOND instance is FORBIDDEN as premature abstraction (creates wrong abstractions). Once extracted, all 3+ call sites MUST use the shared function. The `08-dry-principles.md` "rule of three" is binding. Re-duplication after extraction MUST be flagged in PR review.
- **Verifies:** `08-dry-principles.md` + `09-dry-refactoring-summary.md` + `23-solid-principles.md` (favors composition).

---

## Legacy Index (preserved for traceability)

The following stub criteria from v3.2.0 are preserved verbatim. They are NO LONGER authoritative — the GWT ACs above supersede them.

### AC-CL-LEGACY: Guideline Coverage

- [ ] AC-CL-LEGACY-01-A — Boolean principles define naming, evaluation, and composition patterns
- [ ] AC-CL-LEGACY-01-B — Casting elimination patterns cover type-safe alternatives to type assertions
- [ ] AC-CL-LEGACY-01-C — Code style defines formatting, naming, and structural conventions


> **Verifies:** Legacy stub preserved for traceability; live contract is asserted by **the modern numeric-ID ACs in this same §97**. Phase 153 Task #29d.
### AC-CL-LEGACY: Enforcement

- [ ] AC-CL-LEGACY-02-A — All guidelines include ❌ (forbidden) and ✅ (compliant) code examples
- [ ] AC-CL-LEGACY-02-B — ESLint/linter rules are documented for automated enforcement
- [ ] AC-CL-LEGACY-02-C — Master guidelines document consolidates all standards for AI reference

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Master coding guidelines](./15-master-coding-guidelines.md)
- [Boolean principles](./02-boolean-principles.md)
- [Strict typing](./13-strict-typing.md)
- [DRY principles](./08-dry-principles.md)
- [SOLID principles](./23-solid-principles.md)
- [Parent §02 governance](../97-acceptance-criteria.md)
- [TypeScript subfolder](../02-typescript/)
- [Go subfolder](../03-golang/)
- [PHP subfolder](../04-php/)
- [Rust subfolder](../05-rust/)
- [C# subfolder](../07-csharp/)

> **Verifies:** Legacy stub preserved for traceability; live contract is asserted by **the modern numeric-ID ACs in this same §97**. Phase 153 Task #29d.
