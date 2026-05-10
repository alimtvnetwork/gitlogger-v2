# PHP Standards — Acceptance Criteria

**Version:** 4.1.0
**Last Updated:** 2026-04-29
**Scope:** `spec/02-coding-guidelines/04-php/` — PHP 8.1+ coding standards layered on the cross-language parent.

---

## Module Summary

§02/04-php codifies PHP-specific rules: PHP 8.1+ string-backed enums with required `isEqual()`, `RiseupAsia\Enums` / `RiseupAsia\Helpers` namespaces, `ResultHelper::ok|failed|error|errorWithCode|errorFromException` for service results, `ResponseKeyType` PascalCase enum keys, camelCase methods/variables, PascalCase classes/enums/cases, UPPER_SNAKE_CASE constants, `declare(strict_types=1)` at every file top, no leading-backslash global types (must `use`-import), `safeExecute(fn() => ...)` wrapping for REST handlers, `wp_die()` FORBIDDEN in REST context, blank-line discipline before `if`/`throw`. Inherits ALL **AC-CL-01..AC-CL-20** per AC-CL-01.

---

## Inlined Contracts

```text
PARENT_INHERITANCE:        ../01-cross-language/97 (AC-CL-01..AC-CL-20)
MIN_PHP_VERSION:           8.1 (string-backed enums + readonly + never type)
                           PHP 8.2+ recommended (readonly classes + DNF types)
NAMESPACE_ROOTS:           RiseupAsia\Enums   → includes/Enums/
                           RiseupAsia\Helpers → includes/Helpers/
                           RiseupAsia\Services → includes/Services/
ENUM_PATTERN:              enum X: string { case CaseName = 'CaseName'; ... }
                           MUST implement isEqual(self $other): bool
                           Cases PascalCase; values PascalCase
                           SCREAMING_SNAKE_CASE FORBIDDEN
                           Untyped (pure) enums FORBIDDEN — must be string-backed
RESULT_HELPER:             ResultHelper::ok(array $extra = [])
                           ResultHelper::failed(array $extra = [])
                           ResultHelper::error(string $msg, array $extra = [])
                           ResultHelper::errorWithCode(string $msg, string $code, array $extra = [])
                           ResultHelper::errorFromException(Throwable $e, array $extra = [])
RESPONSE_KEY_TYPE:         enum ResponseKeyType: string {
                             case Success = 'Success';
                             case Error = 'Error';
                             case Message = 'Message';
                             case Data = 'Data';
                             case Code = 'Code';
                             case Valid = 'Valid';
                             case Rows = 'Rows';
                             case Size = 'Size';
                             // ...
                           }
                           Array keys MUST use ResponseKeyType::Foo->value
NAMING:                    Class/Enum/Interface/Trait: PascalCase
                           Enum cases:                 PascalCase
                           Enum case values:           PascalCase
                           Methods/Functions:          camelCase
                           Variables:                  camelCase ($isActive, $hasErrors)
                           Constants:                  UPPER_SNAKE_CASE
                           Boolean prefix:             is / has / can / should
                           snake_case in PHP code:     FORBIDDEN
STRICT_TYPES:              declare(strict_types=1); MUST be the first statement
                           in every .php file. CI fails if missing.
IMPORTS:                   use Throwable;  (NOT \Throwable in catch)
                           use RuntimeException;  (NOT \RuntimeException)
                           Group `use` lines by: PSR\, RiseupAsia\, then 3rd-party
REST_GUARDRAILS:           wp_die(...) FORBIDDEN in REST handlers
                           MUST wrap: $this->safeExecute(fn() => $this->handle($req));
                           Returns structured JSON via ResultHelper
LINTER:                    phpstan --level=8 (max strictness)
                           php-cs-fixer with @PSR12 + @PHP81Migration
                           psalm --show-info=true (zero issues)
INHERITED_FROM_AC_CL:      strict typing (AC-CL-04), boolean-positive (AC-CL-02),
                           PascalCase wire format (AC-CL-09), kebab-case files
                           (AC-CL-12), DRY rule-of-three (AC-CL-20)
```

---

## Acceptance Criteria

### AC-PHP-01 — Inherits all AC-CL-01..AC-CL-20 from cross-language parent

- **Given** any `.php` file in the codebase,
- **When** reviewed,
- **Then** it MUST satisfy every AC-CL-* rule from `../01-cross-language/97-acceptance-criteria.md`. Conflicts MUST resolve in favor of the cross-language rule per AC-CL-01. PHP-specific ACs below LAYER on top of cross-language ACs and MUST NOT contradict them. Any waiver MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** AC-CL-01 inheritance contract.

### AC-PHP-02 — Minimum PHP 8.1; `declare(strict_types=1)` is the first statement of every file

- **Given** any `.php` file in the project,
- **When** parsed,
- **Then** the project's `composer.json` `require.php` MUST be `>=8.1` AND `declare(strict_types=1);` MUST be the FIRST statement (before `namespace`, after the opening `<?php` tag — separated by exactly one blank line). Files without strict types are FORBIDDEN — they silently coerce types and break AC-CL-04. CI MUST grep all `.php` files and fail on any missing declaration.
- **Verifies:** AC-CL-04 + PHP 8.1+ baseline.

### AC-PHP-03 — Enums are string-backed with PascalCase cases AND PascalCase values

- **Given** any PHP enum in the `RiseupAsia\Enums` namespace,
- **When** declared,
- **Then** it MUST be string-backed (`enum X: string`), each case MUST use PascalCase (`case Success`), and each case value MUST also be PascalCase (`case Success = 'Success';`). `SCREAMING_SNAKE_CASE` cases (`case SUCCESS`) are FORBIDDEN. Untyped (pure) enums are FORBIDDEN — they cannot survive serialization and break AC-CL-09 wire-format. Integer-backed enums are FORBIDDEN for wire types (unstable across reorders).
- **Verifies:** `01-enums.md` + `03-naming-conventions.md` + AC-CL-09.

### AC-PHP-04 — Every enum implements `isEqual(self $other): bool`

- **Given** any enum in the `RiseupAsia\Enums` namespace,
- **When** the enum body is parsed,
- **Then** it MUST implement: `public function isEqual(self $other): bool { return $this === $other; }`. Direct `===` comparison in calling code is allowed AND `->isEqual()` is preferred for readability. The signature MUST be exactly `isEqual(self $other): bool` — variants like `equals()`, `is()`, `matches()` are FORBIDDEN to keep the contract uniform across all enums.
- **Verifies:** `01-enums.md`.

### AC-PHP-05 — Service methods return `ResultHelper::ok|failed|error|errorWithCode|errorFromException` only

- **Given** any service method in `RiseupAsia\Services\` returning a result,
- **When** the return statement is parsed,
- **Then** it MUST return the result of one of: `ResultHelper::ok($extra)`, `ResultHelper::failed($extra)`, `ResultHelper::error($msg, $extra)`, `ResultHelper::errorWithCode($msg, $code, $extra)`, `ResultHelper::errorFromException($e, $extra)`. Returning raw arrays, `null`, `bool`, or domain objects from a service public method is FORBIDDEN. Helpers and pure-compute private methods are exempt. This implements AC-CL-17 (`Result`/`Option` over throwing).
- **Verifies:** `05-response-array-standard.md` + AC-CL-17.

### AC-PHP-06 — Array keys returned to wire MUST be `ResponseKeyType::Foo->value`, never string literals

- **Given** any array returned via `ResultHelper`,
- **When** the array literal is parsed,
- **Then** every key MUST be `ResponseKeyType::Foo->value` (e.g. `[ResponseKeyType::Rows->value => $rows]`). String-literal keys (`'Rows' => $rows`) are FORBIDDEN at the service layer — they bypass the enum registry and silently drift from the wire contract. The exception: `$extra` arrays from external libraries may pass through unchanged; they MUST be merged via `array_merge`, not key-by-key copying that re-introduces literals.
- **Verifies:** `09-response-key-type-inventory.md` + AC-CL-09.

### AC-PHP-07 — Identifier casing per role (Class/Enum=PascalCase, method/var=camelCase, const=UPPER_SNAKE_CASE)

- **Given** any PHP identifier,
- **When** declared,
- **Then** it MUST follow the role-based casing: Classes/Enums/Interfaces/Traits = PascalCase; methods + functions + variables + parameters = camelCase; class/global constants = UPPER_SNAKE_CASE; enum cases + their string values = PascalCase. snake_case in any role is FORBIDDEN — it's a WordPress convention that does NOT apply inside the `RiseupAsia\` namespace. The one allowed exception: WordPress hook callbacks named to mirror the hook (`my_plugin_init`) — these MUST be wrapped in a class method calling a camelCase implementation.
- **Verifies:** `03-naming-conventions.md`.

### AC-PHP-08 — Boolean variables MUST use `is`/`has`/`can`/`should` prefix in camelCase

- **Given** any boolean variable, parameter, or method return,
- **When** named,
- **Then** it MUST be camelCase with prefix `is` / `has` / `can` / `should` (e.g. `$isActive`, `$hasErrors`, `$canEdit`, `$shouldRetry`). Snake_case (`$is_active`) is FORBIDDEN. Negative-polarity names (`$isNotActive`, `$hasNoErrors`) are FORBIDDEN per AC-CL-02 — invert the meaning instead. Boolean methods follow the same prefix rule (`isReady()`, `hasPermission()`).
- **Verifies:** `03-naming-conventions.md` + AC-CL-02 + AC-CL-03.

### AC-PHP-09 — Global types are imported via `use`; leading-backslash references FORBIDDEN

- **Given** any reference to a global PHP class (`Throwable`, `RuntimeException`, `DateTimeImmutable`, `Closure`, etc.) from inside a namespaced file,
- **When** the reference is parsed,
- **Then** the class MUST be added to the `use` block at the top of the file AND referenced WITHOUT a leading backslash. `catch (\Throwable $e)` is FORBIDDEN; `use Throwable;` + `catch (Throwable $e)` is REQUIRED. Inline FQCN like `\RuntimeException::class` is FORBIDDEN. The `use` block MUST be ordered: PSR\... → RiseupAsia\... → third-party, blank line between groups.
- **Verifies:** `08-spacing-and-imports.md`.

### AC-PHP-10 — REST handlers MUST wrap execution in `$this->safeExecute(fn() => ...)`; `wp_die()` FORBIDDEN

- **Given** any method registered as a REST endpoint callback (`register_rest_route` callback or `permission_callback`),
- **When** the body is parsed,
- **Then** the executable logic MUST be wrapped: `return $this->safeExecute(fn() => $this->doWork($request));`. Calling `wp_die(...)` anywhere in the REST execution path is FORBIDDEN — it kills the response and produces unparseable HTML instead of a structured JSON error. `safeExecute` MUST catch `Throwable` and return `ResultHelper::errorFromException($e)`.
- **Verifies:** `02-forbidden-patterns.md` + REST guardrails.

### AC-PHP-11 — Blank-line discipline: blank line BEFORE `if`/`throw`/`return` when preceded by other statements

- **Given** any control-flow statement (`if`, `throw`, `return`),
- **When** the surrounding lines are inspected,
- **Then** there MUST be exactly one blank line BEFORE the statement when preceded by non-control statements. Exceptions: (a) at the very start of a function body, (b) immediately after a closing brace `}`, (c) when chaining multiple `if` / `return` of the same shape (early-returns guard pattern). This makes guard clauses visually scannable.
- **Verifies:** `08-spacing-and-imports.md`.

### AC-PHP-12 — Constructor property promotion + `readonly` for value objects (PHP 8.1+)

- **Given** any value object / DTO class,
- **When** the constructor is parsed,
- **Then** properties MUST be declared via constructor property promotion AND marked `readonly` where applicable: `public function __construct(public readonly string $id, public readonly UploadStatusType $status) {}`. Separate property declarations + manual assignment in constructor is FORBIDDEN for DTOs — it doubles the surface area for typos. Mutable DTOs require a `99` waiver explaining why immutability is impractical.
- **Verifies:** PHP 8.1 readonly idiom + AC-CL-04.

### AC-PHP-13 — Type declarations on EVERY method parameter and return; no untyped signatures

- **Given** any function or method,
- **When** the signature is parsed,
- **Then** every parameter MUST have a type declaration AND the return MUST have a type declaration (including `: void`, `: never`, `: self`, `: static` where applicable). Untyped parameters or missing return types are FORBIDDEN. Union types (`string|int`), intersection types (`Countable&Iterator`), and DNF types (`(A&B)|null` PHP 8.2+) are encouraged where they improve precision. `mixed` requires a `99` waiver per AC-CL-04.
- **Verifies:** AC-CL-04.

### AC-PHP-14 — Exceptions inherit from `RiseupAsia\Exceptions\BaseException`; SPL exceptions only at boundaries

- **Given** any custom exception thrown from `RiseupAsia\` code,
- **When** the class hierarchy is parsed,
- **Then** the exception MUST extend `RiseupAsia\Exceptions\BaseException` (which itself extends `\RuntimeException`). SPL exceptions (`InvalidArgumentException`, `LogicException`) are allowed ONLY at framework boundaries (e.g. WordPress hook validation). All exceptions from service methods MUST be caught at the service boundary and converted via `ResultHelper::errorFromException` per AC-PHP-05.
- **Verifies:** AC-CL-17 + exception hierarchy.

### AC-PHP-15 — Static analysis: `phpstan --level=8` + `psalm --show-info=true` MUST pass with zero issues

- **Given** the project's PHP source,
- **When** CI runs `composer run phpstan` and `composer run psalm`,
- **Then** BOTH MUST exit with zero issues. `phpstan` baseline files (`phpstan-baseline.neon`) are FORBIDDEN — every issue MUST be fixed at source. Per-file `@phpstan-ignore-*` annotations are allowed only with a comment explaining why AND a `99` waiver row. `php-cs-fixer` MUST run with `@PSR12` + `@PHP81Migration` rulesets.
- **Verifies:** AC-CL-06 + linter contract.

### AC-PHP-16 — File-per-class (PSR-4 autoloading); no multi-class files

- **Given** any `.php` file containing a class/enum/interface/trait declaration,
- **When** the file is parsed,
- **Then** it MUST contain EXACTLY ONE top-level type declaration AND the file basename MUST match the type name exactly (case-sensitive). `Foo.php` MUST contain `class Foo`. Multi-class files are FORBIDDEN — they break PSR-4 autoloading and IDE navigation. Anonymous classes inside the file body are allowed for one-off callbacks.
- **Verifies:** PSR-4 + AC-CL-12 file naming.

### AC-PHP-17 — Tests use PHPUnit 10+ with `#[Test]` attribute; `@test` PHPDoc FORBIDDEN

- **Given** any test method in `tests/`,
- **When** the method is parsed,
- **Then** it MUST be marked with the `#[Test]` attribute (PHPUnit 10+) OR follow the `testFoo` naming prefix. The legacy `@test` PHPDoc annotation is FORBIDDEN — attributes are the modern, IDE-aware idiom. Test method names MUST describe BEHAVIOR per AC-CL-19 inherited (e.g. `#[Test] public function it_returns_failed_when_user_is_inactive(): void` — snake_case allowed in test names ONLY).
- **Verifies:** AC-CL-19 + PHPUnit 10+ attribute idiom.

### AC-PHP-18 — Composer dependencies pinned to exact patch range; `composer.lock` checked in

- **Given** the project's `composer.json` and `composer.lock`,
- **When** reviewed,
- **Then** `require` and `require-dev` versions MUST use caret-with-patch (`^1.2.3` not `^1.2`) AND `composer.lock` MUST be committed (it's the source of truth for production installs). `dev-master` / `dev-main` references are FORBIDDEN in production deps. Abandoned packages (per `composer audit`) MUST trigger a migration ticket within 1 sprint.
- **Verifies:** Dependency hygiene.

### AC-PHP-19 — Logging uses Monolog (or PSR-3 LoggerInterface) with structured context; `error_log()` FORBIDDEN

- **Given** any logging call in non-test code,
- **When** inspected,
- **Then** it MUST use `LoggerInterface` (PSR-3) injected via constructor, with structured context array: `$this->logger->info('user authenticated', ['userId' => $id, 'method' => $method]);`. `error_log()` is FORBIDDEN — no level, no destination control. `var_dump()`, `print_r()`, `echo` for logging are FORBIDDEN. Context keys MUST use camelCase (or `ResponseKeyType::Foo->value` for cross-cut keys per AC-PHP-06). PII MUST be redacted.
- **Verifies:** AC-CL-* observability + PSR-3.

### AC-PHP-20 — Self-application: this folder's PHP examples + enum patterns satisfy AC-PHP-01..AC-PHP-19

- **Given** every code example in `01-enums.md`, `02-forbidden-patterns.md`, `03-naming-conventions.md`, `05-response-array-standard.md`, `07-php-standards-reference.md`, `08-spacing-and-imports.md`, `09-response-key-type-inventory.md`, `10-php-go-consistency-audit.md`, and the `07-php-standards-reference/` subfolder,
- **When** mechanically extracted and run through `phpstan --level=8` + `php-cs-fixer --dry-run`,
- **Then** every example MUST pass without errors AND satisfy AC-PHP-02 (`declare(strict_types=1)` present), AC-PHP-03 (string-backed enums with PascalCase), AC-PHP-09 (no leading-backslash globals). Example code that violates its own ACs is a CODE-RED documentation-drift bug.
- **Verifies:** Recursive self-check + AC-SAG-18 dogfooding analogue.

---

## Legacy Index (preserved for traceability)

The following 7 criteria from v2.0.0 are preserved verbatim. They are NO LONGER authoritative — the GWT ACs above supersede them.

### AC-PHP-LEGACY-01: Enum Naming and Required Structure  `[critical]`
- Given a new PHP enum being created for 'Upload Status' in `includes/Enums/`, when defining the enum name and class body, then the enum MUST be named `UploadStatusType`, use the `RiseupAsia\Enums` namespace, be string-backed, and implement the `isEqual(self $other): bool` method. → superseded by AC-PHP-03 + AC-PHP-04.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-PHP-LEGACY-02: Enum Case Casing Convention  `[high]`
- Given any PHP backed enum in the `RiseupAsia` namespace, when declaring enum cases, then individual cases MUST use PascalCase (e.g., `case RestApi`), NOT SCREAMING_SNAKE_CASE. → superseded by AC-PHP-03.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-PHP-LEGACY-03: Internal Service Result Standardization  `[critical]`
- Given an internal service method returning a result in the `RiseupAsia` namespace, when returning data or status, then it MUST return a structured array via `ResultHelper::ok()`, `error()`, or `failed()`, with keys using `ResponseKeyType` cases. → superseded by AC-PHP-05 + AC-PHP-06.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-PHP-LEGACY-04: Spacing for Control Flow and Exceptions  `[medium]`
- Given a line of code inside a class method using `if` or `throw`, when writing control flow logic, then there MUST be a blank line before the keyword if preceded by other statements. → superseded by AC-PHP-11.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-PHP-LEGACY-05: No Leading Backslash for Global Types  `[high]`
- Given a PHP file within the `RiseupAsia` namespace using global PHP types, when referencing them, then code MUST use `use` imports without leading backslash. → superseded by AC-PHP-09.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-PHP-LEGACY-06: REST Error Handling Guardrails  `[critical]`
- Given a REST API handler in WordPress companion plugin, when implementing endpoint logic, then handler MUST NOT use `wp_die()` and MUST wrap execution in `$this->safeExecute(fn() => ...)`. → superseded by AC-PHP-10.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-PHP-LEGACY-07: Boolean Variable Naming Convention  `[medium]`
- Given a boolean variable being declared in PHP, when declaring, then it MUST use camelCase with `is`/`has` prefix, forbidding snake_case. → superseded by AC-PHP-08.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Cross-language parent (AC-CL-*)](../01-cross-language/97-acceptance-criteria.md)
- [Enums](./01-enums.md)
- [Forbidden patterns](./02-forbidden-patterns.md)
- [Naming conventions](./03-naming-conventions.md)
- [Response array standard](./05-response-array-standard.md)
- [PHP standards reference](./07-php-standards-reference.md)
- [Spacing and imports](./08-spacing-and-imports.md)
- [Response key type inventory](./09-response-key-type-inventory.md)
- [PHP/Go consistency audit](./10-php-go-consistency-audit.md)
- [§02 parent governance](../97-acceptance-criteria.md)
- [TypeScript sibling](../02-typescript/97-acceptance-criteria.md)
- [Golang sibling](../03-golang/97-acceptance-criteria.md)

> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
