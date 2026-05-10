# C# Coding Standards — Acceptance Criteria

**Version:** 4.1.0
**Last Updated:** 2026-04-26 (Phase 16m: full GWT rewrite — replaced 38 stub checkboxes (AC-01..AC-07) with 20 module-specific Given/When/Then ACs covering C#-specific rules + explicit inheritance from `../01-cross-language/97` (AC-CL-*). Old AC-01..AC-07 preserved as AC-CS-LEGACY-* at end.)
**Scope:** `spec/02-coding-guidelines/07-csharp/` — C# 12 / .NET 8+ coding standards layered on the cross-language parent.

---

## Module Summary

§02/07-csharp codifies C#-specific rules: PascalCase types/methods/properties, camelCase locals/params, `_camelCase` private fields, `I`-prefixed interfaces, first-letter-only acronym casing (`UserId` not `UserID`), boolean prefix `Is`/`Has`/`Can`/`Should`/`Was`, `record` for immutable DTOs, nullable reference types enabled project-wide, `Result<T>` / `OneOf<T,Err>` over throwing for expected failures, no bare `catch (Exception)`, async-all-the-way (no `.Result`/`.GetAwaiter().GetResult()`), `Task.WhenAll` for independent awaits, `Async` suffix on async methods, `CancellationToken` last parameter, no boolean flag parameters that branch (split methods), method body ≤15 lines + ≤3 params, `switch` expressions with exhaustive matching, generics over `object` returns, `nameof()` for arg names, `LangVersion=latest` + `Nullable=enable` + `TreatWarningsAsErrors=true`, Roslyn analyzers + StyleCop + EditorConfig enforced. Inherits ALL **AC-CL-01..AC-CL-20** per AC-CL-01.

---

## Inlined Contracts

```text
PARENT_INHERITANCE:        ../01-cross-language/97 (AC-CL-01..AC-CL-20)
MIN_DOTNET:                .NET 8 (LTS) — TargetFramework: net8.0 minimum
                           .NET 9 STS allowed for non-prod tooling
LANG_VERSION:              <LangVersion>latest</LangVersion>  (C# 12+)
                           NEVER pin LangVersion to a specific number
NULLABILITY:               <Nullable>enable</Nullable>  (project-wide)
                           Per-file #nullable disable FORBIDDEN without 99 waiver
WARNINGS:                  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
                           <AnalysisLevel>latest-recommended</AnalysisLevel>
                           <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
ERROR_PATTERN:             Expected failures:  Result<T> or OneOf<T, Error>
                                               (preferred) — implements AC-CL-17
                           Exceptional only:   throw <SpecificException>(...)
                           NEVER:              throw new Exception(...) — too generic
                           NEVER:              catch (Exception) — too broad
                           NEVER:              empty catch blocks (silent swallow)
                           Argument guards:    ArgumentNullException.ThrowIfNull(x)
                                               or guard clauses with nameof()
NAMING:                    Classes/Structs/Records:  PascalCase  (UserProfile)
                           Interfaces:               IPascalCase (IUserRepository)
                           Methods:                  PascalCase  (GetActiveUsers)
                           Public properties:        PascalCase  (FullName)
                           Public fields:            PascalCase  (rare; prefer props)
                           Private fields:           _camelCase  (_logger)
                           Private static fields:    s_camelCase (s_cache)
                           Constants:                PascalCase  (DefaultTimeout)
                                                     NOT SCREAMING_SNAKE_CASE
                           Local variables:          camelCase   (userId)
                           Parameters:               camelCase   (cancellationToken)
                           Type parameters:          T or TPascalCase (TKey, TValue)
                           Acronyms ≥3 letters:      first-letter only (HtmlParser)
                           Acronyms 2 letters:       both letters caps (DbContext, IOStream)
                           Files:                    PascalCase.cs matching primary type
ASYNC:                     Async methods MUST end with Async suffix
                           Async methods MUST take CancellationToken as LAST parameter
                           NEVER: .Result, .Wait(), .GetAwaiter().GetResult()
                                  (deadlock risk in sync contexts)
                           Independent awaits → Task.WhenAll(...)
                           Sync over async (Task.Run on UI thread): FORBIDDEN
                           ConfigureAwait(false) at library boundaries
METHOD_LIMITS:             Body ≤ 15 lines (excluding error handling + braces)
                           Parameters ≤ 3 — use options class/record for 4+
                           Boolean flag params that BRANCH: FORBIDDEN — split methods
                           Boolean flag params for TOGGLE state: ALLOWED
                                  (e.g. SetEnabled(bool))
                           Boolean props on options records: ALLOWED
TYPE_SAFETY:               object returns: FORBIDDEN — use generics T GetValue<T>()
                           Explicit casts in business logic: FORBIDDEN — pattern match
                           switch expressions: prefer over switch statements
                           switch MUST be exhaustive (compiler-enforced for enums)
                           switch on open hierarchies MUST end with _ throw
                           record over class for DTOs (immutable + value equality)
                           init-only setters for partially-mutable DTOs
LINQ:                      LINQ method syntax preferred (.Select, .Where, .Any)
                           Query syntax allowed for complex multi-from joins
                           Predicate complexity > 3 lines → extract named method
                           Nested LINQ depth ≤ 2
                           ToList()/ToArray() at consumption boundary, not mid-pipeline
ANALYZERS:                 Roslyn analyzers (latest)
                           StyleCop.Analyzers
                           Microsoft.CodeAnalysis.NetAnalyzers
                           SonarAnalyzer.CSharp (recommended)
                           .editorconfig at repo root with C# rules
INHERITED_FROM_AC_CL:      strict typing (AC-CL-04), Result over panic (AC-CL-17),
                           PascalCase wire (AC-CL-09 — natural fit for C#),
                           kebab-case files (AC-CL-12 — DOCUMENTED OVERRIDE: C#
                           uses PascalCase.cs per .NET convention; see AC-CS-07)
```

---

## Acceptance Criteria

### AC-CS-01 — Inherits all AC-CL-01..AC-CL-20 from cross-language parent

- **Given** any `.cs` file in the codebase,
- **When** reviewed,
- **Then** it MUST satisfy every AC-CL-* rule from `../01-cross-language/97-acceptance-criteria.md`. Conflicts MUST resolve in favor of the cross-language rule per AC-CL-01, with the documented exception of AC-CL-12 file-naming — C# uses `PascalCase.cs` per the .NET convention; see AC-CS-07. Any other waiver MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** AC-CL-01 inheritance contract.

### AC-CS-02 — Target .NET 8+ (LTS); `LangVersion=latest`; `Nullable=enable`; `TreatWarningsAsErrors=true`

- **Given** every `.csproj` file in the project,
- **When** parsed,
- **Then** `<TargetFramework>` MUST be `net8.0` (or later LTS). The project MUST set `<LangVersion>latest</LangVersion>`, `<Nullable>enable</Nullable>`, `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`, `<AnalysisLevel>latest-recommended</AnalysisLevel>`, AND `<EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>`. Pinning `LangVersion` to a specific number (e.g. `12`) is FORBIDDEN — it freezes language progress. Per-file `#nullable disable` requires a `99` waiver.
- **Verifies:** Project baseline + AC-CL-04.

### AC-CS-03 — Naming: types PascalCase, interfaces `IPascalCase`, locals camelCase, private fields `_camelCase`

- **Given** any C# identifier,
- **When** declared,
- **Then** it MUST follow .NET naming: `class`/`struct`/`record`/`enum` = PascalCase (`UserProfile`); `interface` = `I` + PascalCase (`IUserRepository`); methods + public properties + public fields + constants = PascalCase (`GetActiveUsers`, `DefaultTimeout`); local variables + parameters = camelCase (`userId`); private instance fields = `_camelCase` (`_logger`); private static fields = `s_camelCase` (`s_cache`); type parameters = `T` or `TPascalCase` (`TKey`). SCREAMING_SNAKE_CASE for constants is FORBIDDEN — that's a Java/Go convention. snake_case is FORBIDDEN in any role.
- **Verifies:** `01-naming-and-conventions.md` + .NET naming guidelines.

### AC-CS-04 — Acronym casing: ≥3 letters first-letter-only (`UserId`/`HtmlParser`); 2 letters both-caps (`DbContext`/`IOStream`)

- **Given** any identifier containing an acronym,
- **When** the identifier is parsed,
- **Then** acronyms of 3+ letters MUST be first-letter-only PascalCase: `UserId` (not `UserID`), `HtmlParser` (not `HTMLParser`), `ApiClient` (not `APIClient`), `XmlReader`, `JsonSerializer`. Acronyms of EXACTLY 2 letters MUST keep both letters capitalized: `DbContext`, `IOStream`, `IPAddress`, `UIControl`. This is the standard .NET Framework Design Guidelines rule and explicitly DIFFERS from the Go all-caps rule (AC-GO-03).
- **Verifies:** `01-naming-and-conventions.md` + .NET FDG.

### AC-CS-05 — Boolean identifiers prefixed `Is`/`Has`/`Can`/`Should`/`Was`; no negative polarity

- **Given** any boolean property, field, parameter, local, or method return,
- **When** named,
- **Then** it MUST be PascalCase (or camelCase for locals/params) with prefix `Is` / `Has` / `Can` / `Should` / `Was` (e.g. `IsActive`, `HasPermission`, `CanEdit`, `ShouldRetry`, `WasModified`). Negative-polarity names (`IsNotReady`, `HasNoErrors`, `CannotEdit`) are FORBIDDEN per AC-CL-02 — invert the meaning instead (`IsReady` checked with `!`). Boolean methods follow the same prefix rule.
- **Verifies:** `01-naming-and-conventions.md` + AC-CL-02 + AC-CL-03.

### AC-CS-06 — Boolean flag PARAMETERS that BRANCH method behavior FORBIDDEN; split into named methods

- **Given** any method that accepts a `bool` parameter,
- **When** the method body is parsed,
- **Then** the bool MUST NOT be used to branch into two materially different code paths. Such methods MUST be split: `Save(doc, isDraft)` → `SaveDraft(doc)` + `PublishDocument(doc)`. EXEMPTIONS: (a) toggle methods setting state (`SetEnabled(bool enabled)`); (b) bool properties on an options record/class (`new ExportOptions { Verbose = true }`); (c) bool that filters but doesn't branch into different control flow. Shared logic between split methods MUST be extracted into a private helper to avoid duplication per AC-CL-20.
- **Verifies:** `02-method-design.md` + `../01-cross-language/24-boolean-flag-methods.md`.

### AC-CS-07 — File naming: one type per file, file basename = primary type's PascalCase name (DOCUMENTED AC-CL-12 OVERRIDE)

- **Given** any `.cs` source file,
- **When** the file is opened,
- **Then** it MUST contain EXACTLY ONE top-level type declaration (class/struct/record/interface/enum/delegate) AND the file basename MUST equal that type's name in PascalCase (`SnapshotManager.cs` contains `SnapshotManager`). This is the SOLE documented waiver of AC-CL-12 (kebab-case files) — `.NET` and Roslyn navigation tooling require this convention. Multi-type files are FORBIDDEN. Nested types inside the primary type are allowed; partial classes are allowed (each part still in a separate file named `SnapshotManager.Foo.cs`).
- **Verifies:** `01-naming-and-conventions.md` + .NET file convention + AC-CL-12 documented override.

### AC-CS-08 — Method body ≤ 15 lines (excluding error handling + braces); parameters ≤ 3

- **Given** any method declaration,
- **When** measured,
- **Then** the body MUST be ≤ 15 LOC excluding `{`/`}` braces, blank lines, and pure-error-handling try/catch shells. Parameters MUST be ≤ 3 — methods needing 4+ MUST accept an options `record`/class. Constructors that pass-through to a base ctor are exempt. Public APIs that fundamentally need more parameters require a `99` waiver justifying why options object is not idiomatic.
- **Verifies:** `02-method-design.md` + AC-CL-06 (cyclomatic complexity proxy).

### AC-CS-09 — Async methods end with `Async` suffix + take `CancellationToken` as LAST parameter

- **Given** any method returning `Task` / `Task<T>` / `ValueTask` / `ValueTask<T>` / `IAsyncEnumerable<T>`,
- **When** the signature is parsed,
- **Then** the method name MUST end with `Async` (`GetUsersAsync`) AND `CancellationToken cancellationToken = default` MUST be the LAST parameter. Sync methods MUST NOT use the `Async` suffix. The CT parameter is mandatory even when the body doesn't currently observe it — future authors MUST be able to plumb cancellation without a breaking signature change. Event handlers (`async void`) and top-level program entry points are exempt from CT requirement.
- **Verifies:** `02-method-design.md` + .NET async guidelines.

### AC-CS-10 — `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` FORBIDDEN; async-all-the-way

- **Given** any non-test code calling an async API,
- **When** scanned,
- **Then** zero matches MUST be found for `.Result`, `.Wait()`, `.GetAwaiter().GetResult()`, `Task.WaitAll`, `Task.WaitAny`. These cause deadlocks in synchronization-context environments (UI, classic ASP.NET) and exhaust the thread pool elsewhere. The caller MUST be `async` and use `await`. The ONLY exemption is `Main()` in console apps (use `static async Task Main` instead) and synchronous test setup helpers in unit tests.
- **Verifies:** `02-method-design.md`.

### AC-CS-11 — Independent awaits MUST use `Task.WhenAll`; sequential `await` for unrelated tasks FORBIDDEN

- **Given** two or more `await` statements with no data dependency between them,
- **When** the code is reviewed,
- **Then** they MUST be combined: `var (a, b) = await (TaskA(), TaskB()).WhenAll();` or equivalent. Sequential `await` of independent operations is FORBIDDEN — it serializes wall-clock latency unnecessarily. Mirrors AC-TS-* TypeScript Promise.all rule. Use `Task.WhenAll` for fire-all-then-collect; `await foreach` over `IAsyncEnumerable` for streaming.
- **Verifies:** `02-method-design.md` + concurrency hygiene.

### AC-CS-12 — `Result<T>` / `OneOf<T, Error>` for expected failures; throw only for exceptional cases

- **Given** any method that can fail in an EXPECTED way (validation, "not found", permission denial),
- **When** the return type is designed,
- **Then** it MUST return `Result<T>` (project type) or `OneOf<T, Error>` (third-party). Throwing exceptions for expected failures is FORBIDDEN per AC-CL-17 — exceptions are for genuinely exceptional, unrecoverable conditions. Boundary methods MAY catch low-level exceptions and convert to `Result<T>`. Domain methods MUST NOT throw on validation failures.
- **Verifies:** AC-CL-17 + `03-error-handling.md`.

### AC-CS-13 — `catch (Exception)` FORBIDDEN; catch specific types; never silent swallow

- **Given** any `catch` clause,
- **When** parsed,
- **Then** it MUST catch a SPECIFIC exception type (`catch (HttpRequestException)`, `catch (JsonException)`). Bare `catch (Exception)` and parameterless `catch` are FORBIDDEN — they hide real bugs. Empty catch bodies (silent swallow) are FORBIDDEN — every catch MUST log + rethrow OR convert to `Result<T>`. The ONE exemption: top-level "process boundary" handlers (e.g. ASP.NET middleware, console `Main`) may catch `Exception` to log + return 500/exit code, AND MUST log full stack via `ILogger.LogError(ex, ...)`.
- **Verifies:** `03-error-handling.md`.

### AC-CS-14 — Argument guards via `ArgumentNullException.ThrowIfNull(x)` + `nameof()`; early-return guard clauses

- **Given** any public method accepting reference-type or nullable parameters,
- **When** the body begins,
- **Then** null guards MUST use `ArgumentNullException.ThrowIfNull(parameter);` (.NET 6+) or guard clauses using `nameof(parameter)`. Hard-coded parameter-name strings (`throw new ArgumentNullException("foo")`) are FORBIDDEN — they break under rename. Validation logic MUST use early-return guard clauses, not nested `if` blocks per AC-CL-07 (nesting ≤ 3 inherited).
- **Verifies:** `03-error-handling.md` + AC-CL-07.

### AC-CS-15 — `record` for immutable DTOs; `class` only for behavior-bearing types; `init` setters for partial mutability

- **Given** any data-transfer object / value type,
- **When** the type is declared,
- **Then** it MUST be a `record` (preferred) or `record struct` (for small, frequently-allocated values). `class` is reserved for types with significant behavior (services, managers, controllers). DTOs declared as mutable `class` with public setters are FORBIDDEN — they invite shared-state bugs. Partial mutability uses `init`-only setters: `public string Name { get; init; }`. Use positional records for small DTOs (`public record UserId(Guid Value);`).
- **Verifies:** `04-type-safety.md`.

### AC-CS-16 — `object` returns FORBIDDEN; use generics; explicit casts in business logic FORBIDDEN; pattern matching only

- **Given** any method declaration,
- **When** parsed,
- **Then** the return type MUST NOT be `object` — use generics (`T GetValue<T>(string key)` or `Result<T>`). In business logic, explicit cast expressions (`(User)obj`, `obj as User` followed by null-check) are FORBIDDEN — use pattern matching: `if (obj is User user) { ... }` or `obj switch { User u => ..., _ => ... }`. The cast-and-throw `(T)obj` is allowed ONLY at framework boundaries with documented invariants.
- **Verifies:** `04-type-safety.md` + `../01-cross-language/25-generic-return-types.md`.

### AC-CS-17 — `switch` expressions over `switch` statements; exhaustive matching with `_` default

- **Given** any pattern dispatch in the codebase,
- **When** the code is reviewed,
- **Then** `switch` EXPRESSIONS MUST be preferred over `switch` STATEMENTS for value production. Every `switch` (statement or expression) over a closed type (enum, sealed hierarchy) MUST be exhaustive — the compiler MUST NOT emit `CS8509` (non-exhaustive switch). Switches over open types MUST end with `_ => throw new UnreachableException(...)` (or similar) — silent fall-through to default is FORBIDDEN. Mirrors AC-TS-08 exhaustive `never` check.
- **Verifies:** `04-type-safety.md` + AC-TS-08 parallel.

### AC-CS-18 — Magic strings/numbers FORBIDDEN; use enums, typed constants, or `record` value types

- **Given** any literal value used more than once OR appearing in a public API surface,
- **When** the code is reviewed,
- **Then** it MUST be extracted to one of: an `enum` (for closed sets of named values), a `public const` PascalCase constant (for genuine constants), a `static readonly` field (for non-`const`-eligible types like `TimeSpan`), or a strongly-typed value-`record` (`public record UserId(Guid Value);`). Inline duplicated string literals like HTTP method names, header names, error codes are FORBIDDEN — they create silent drift. Mirrors AC-CL-08 magic-value extraction on second use.
- **Verifies:** `04-type-safety.md` + AC-CL-08.

### AC-CS-19 — Roslyn + StyleCop + Net analyzers enabled; `.editorconfig` at repo root; CI fails on any warning

- **Given** the workspace,
- **When** CI runs `dotnet build -warnaserror`,
- **Then** zero warnings MUST be reported. The project MUST reference `Microsoft.CodeAnalysis.NetAnalyzers`, `StyleCop.Analyzers`, and SHOULD reference `SonarAnalyzer.CSharp`. A `.editorconfig` at the repo root MUST encode the C# style rules from `01-naming-and-conventions.md`. Per-file `#pragma warning disable` is FORBIDDEN without an inline comment explaining why AND a `99` waiver row.
- **Verifies:** AC-CL-06 + linter contract.

### AC-CS-20 — Self-application: this folder's C# examples compile with `-warnaserror` + analyzers clean

- **Given** every code example in `01-naming-and-conventions.md`, `02-method-design.md`, `03-error-handling.md`, `04-type-safety.md`,
- **When** mechanically extracted into a `dotnet build -warnaserror` harness,
- **Then** every example MUST compile with zero warnings AND satisfy AC-CS-03 (naming), AC-CS-09 (Async suffix + CT last), AC-CS-13 (no bare catch), AC-CS-17 (exhaustive switch). Example code that violates its own ACs is a CODE-RED documentation-drift bug.
- **Verifies:** Recursive self-check + AC-SAG-18 dogfooding analogue.

---

## Legacy Index (preserved for traceability)

The following 38 stub criteria from v3.2.0 are preserved verbatim. They are NO LONGER authoritative — the GWT ACs above supersede them.

### AC-CS-LEGACY-01: Naming & Conventions

- [ ] All classes, structs, records use PascalCase → superseded by AC-CS-03.
- [ ] Interfaces prefixed with `I` → superseded by AC-CS-03.
- [ ] Methods use PascalCase → superseded by AC-CS-03.
- [ ] Local variables and parameters use camelCase → superseded by AC-CS-03.
- [ ] Private fields use `_camelCase` → superseded by AC-CS-03.
- [ ] Abbreviations: first-letter-only caps → superseded by AC-CS-04.
- [ ] All booleans prefixed with `Is`/`Has`/`Can`/`Should`/`Was` → superseded by AC-CS-05.
- [ ] No negative boolean names → superseded by AC-CS-05.
- [ ] File names match primary type in PascalCase → superseded by AC-CS-07.
- [ ] One type per file → superseded by AC-CS-07.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-CS-LEGACY-02: Method Design

- [ ] No boolean flag parameters that branch method behavior → superseded by AC-CS-06.
- [ ] Method bodies ≤15 lines → superseded by AC-CS-08.
- [ ] Method parameters ≤3 → superseded by AC-CS-08.
- [ ] Shared logic between split methods extracted into private helpers → superseded by AC-CS-06 + AC-CL-20.
- [ ] Async methods suffixed with `Async` → superseded by AC-CS-09.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-CS-LEGACY-03: Boolean Flag Splitting

- [ ] `Save(doc, isDraft)` → `SaveDraft(doc)` + `PublishDocument(doc)` → superseded by AC-CS-06.
- [ ] `Process(data, isVerbose)` → `ProcessCompact(data)` + `ProcessVerbose(data)` → superseded by AC-CS-06.
- [ ] Options objects with named bool properties are exempt → superseded by AC-CS-06.
- [ ] Toggle methods are exempt → superseded by AC-CS-06.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-CS-LEGACY-04: Error Handling

- [ ] Catch specific exceptions, never bare `catch (Exception)` → superseded by AC-CS-13.
- [ ] No silently swallowed exceptions → superseded by AC-CS-13.
- [ ] Guard clauses with early return instead of nested `if` blocks → superseded by AC-CS-14.
- [ ] `ArgumentNullException` with `nameof()` for null parameter guards → superseded by AC-CS-14.
- [ ] Nullable reference types enabled project-wide → superseded by AC-CS-02.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-CS-LEGACY-05: Type Safety

- [ ] No `object` returns — use generics → superseded by AC-CS-16.
- [ ] No explicit type casts in business logic → superseded by AC-CS-16.
- [ ] Records used for immutable data transfer objects → superseded by AC-CS-15.
- [ ] No magic strings — use enums or typed constants → superseded by AC-CS-18.
- [ ] `switch` expressions with exhaustive matching and `_` default case → superseded by AC-CS-17.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-CS-LEGACY-06: Async Patterns

- [ ] No `.Result` or `.GetAwaiter().GetResult()` → superseded by AC-CS-10.
- [ ] Independent async calls use `Task.WhenAll()` → superseded by AC-CS-11.
- [ ] Async method naming ends with `Async` suffix → superseded by AC-CS-09.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-CS-LEGACY-07: LINQ Usage

- [ ] LINQ preferred over manual loops for transforms → superseded by AC-CS-19 analyzers + idiom.
- [ ] Complex LINQ predicates extracted to named methods → superseded by AC-CS-19 + AC-CL-06.
- [ ] No nested LINQ deeper than 2 levels → superseded by AC-CL-07 nesting ≤ 3.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Cross-language parent (AC-CL-*)](../01-cross-language/97-acceptance-criteria.md)
- [Naming and conventions](./01-naming-and-conventions.md)
- [Method design](./02-method-design.md)
- [Error handling](./03-error-handling.md)
- [Type safety](./04-type-safety.md)
- [Boolean flag methods (cross-language)](../01-cross-language/24-boolean-flag-methods.md)
- [Generic return types (cross-language)](../01-cross-language/25-generic-return-types.md)
- [§02 parent governance](../97-acceptance-criteria.md)
- [TypeScript sibling](../02-typescript/97-acceptance-criteria.md)
- [Golang sibling](../03-golang/97-acceptance-criteria.md)
- [PHP sibling](../04-php/97-acceptance-criteria.md)
- [Rust sibling](../05-rust/97-acceptance-criteria.md)

> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
