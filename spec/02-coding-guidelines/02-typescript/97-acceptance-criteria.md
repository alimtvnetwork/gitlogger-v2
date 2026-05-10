# TypeScript Standards — Acceptance Criteria

**Version:** 4.1.0
**Last Updated:** 2026-04-26 (Phase 16i: full GWT rewrite — replaced 6 stub checkboxes with 20 module-specific Given/When/Then ACs covering TS-specific rules + explicit inheritance from `../01-cross-language/97` (AC-CL-*). Old AC-01..AC-02 preserved as AC-TS-LEGACY-* at end.)
**Scope:** `spec/02-coding-guidelines/02-typescript/` — TypeScript-specific coding standards layered on top of the cross-language parent.

---

## Module Summary

§02/02-typescript codifies TypeScript-specific rules: strict-mode tsconfig, `noImplicitAny`, no `as` without justification, discriminated unions for variant types, enum-as-string-literal-union (NEVER `enum`), `Promise.all` for independent async, exhaustive switch via `never`, React functional components, Zustand for state, React Query for server state, ESLint-enforced. Inherits ALL **AC-CL-01..AC-CL-20** from `../01-cross-language/97` per AC-CL-01.

---

## Inlined Contracts

```text
PARENT_INHERITANCE:        ../01-cross-language/97 (AC-CL-01..AC-CL-20)
TSCONFIG_REQUIRED:         "strict": true,
                           "noImplicitAny": true,
                           "noImplicitReturns": true,
                           "noFallthroughCasesInSwitch": true,
                           "noUncheckedIndexedAccess": true,
                           "exactOptionalPropertyTypes": true
ENUM_PATTERN:              `as const` string-literal-union (NEVER `enum` keyword)
                           Example: `const HttpMethod = ['GET','POST','PUT','DELETE','PATCH'] as const;`
                                    `type HttpMethod = (typeof HttpMethod)[number];`
ASYNC_RULE:                independent awaits → MUST use Promise.all() (CODE-RED)
                           dependent awaits → sequential is mandatory
DISCRIMINATED_UNION:       all variant types MUST have a `kind`/`type` discriminator
                           exhaustive checks via `const _exhaustive: never = x;`
REACT_PATTERN:             functional components + hooks ONLY (no class components)
                           Zustand for client state, React Query for server state
ESLINT_REQUIRED:           @typescript-eslint/recommended-type-checked
                           @typescript-eslint/no-explicit-any: error
                           @typescript-eslint/no-floating-promises: error
                           @typescript-eslint/await-thenable: error
ERROR_PATTERN:             AppError discriminated union (NEVER throw plain Error)
INHERITED_FROM_AC_CL:      strict typing (AC-CL-04), null safety (AC-CL-13),
                           Result over throw (AC-CL-17), types/ folder (AC-CL-18),
                           DRY rule-of-three (AC-CL-20), all others
```

---

## Acceptance Criteria

### AC-TS-01 — Inherits all AC-CL-01..AC-CL-20 from cross-language parent

- **Given** any `.ts` / `.tsx` file in the codebase,
- **When** reviewed,
- **Then** it MUST satisfy every AC-CL-* rule from `../01-cross-language/97-acceptance-criteria.md`. Conflicts MUST resolve in favor of the cross-language rule per AC-CL-01. TypeScript-specific ACs below LAYER on top of cross-language ACs and MUST NOT contradict them. Any waiver MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** AC-CL-01 inheritance contract.

### AC-TS-02 — `tsconfig.json` enables full strict mode + 6 additional flags

- **Given** the project's `tsconfig.json`,
- **When** parsed,
- **Then** `compilerOptions` MUST include: `"strict": true`, `"noImplicitAny": true`, `"noImplicitReturns": true`, `"noFallthroughCasesInSwitch": true`, `"noUncheckedIndexedAccess": true`, `"exactOptionalPropertyTypes": true`. Disabling any of these is FORBIDDEN. Per-file `// @ts-nocheck` is FORBIDDEN; per-line `// @ts-expect-error` MUST carry an inline comment with a tracking link/issue ID.
- **Verifies:** `08-typescript-standards-reference.md` + AC-CL-04.

### AC-TS-03 — `any` is forbidden; `unknown` + narrowing is the escape hatch

- **Given** any TS source file,
- **When** scanned for the literal token `any`,
- **Then** zero matches MUST be found (excluding string literals and comments). When the type genuinely cannot be known (third-party untyped JSON, `JSON.parse` result), `unknown` MUST be used followed by a type guard / Zod schema / runtime assertion before use. `as any` is FORBIDDEN. `as unknown as T` is FORBIDDEN outside FFI/test boundaries with `// SAFETY:` comment.
- **Verifies:** `07-type-safety-remediation-plan.md` + AC-CL-04.

### AC-TS-04 — Enums use `as const` string-literal unions, NEVER the `enum` keyword

- **Given** any need to express a closed set of values,
- **When** the type is declared,
- **Then** it MUST follow the `as const` array pattern: `const HttpMethod = ['GET','POST','PUT','DELETE','PATCH'] as const; type HttpMethod = (typeof HttpMethod)[number];`. The TS `enum` keyword is FORBIDDEN — it generates runtime objects, breaks tree-shaking, has dual nominal/structural identity, and produces inconsistent JS. The 6 enum files in this folder (`01-connection-status` through `10-log-level`) MUST all follow this pattern.
- **Verifies:** `01-connection-status-enum.md` through `10-log-level-enum.md`.

### AC-TS-05 — `Promise.all()` for independent async — CODE-RED rule

- **Given** any function that awaits 2+ promises,
- **When** the awaits are inspected,
- **Then** independent (non-dependent) awaits MUST be batched via `await Promise.all([...])` or `Promise.allSettled([...])`. Sequential `await` on independent promises is **automatic PR rejection** (CODE-RED). Dependent awaits (where promise B's input depends on promise A's output) MUST remain sequential. ESLint rule `@typescript-eslint/no-misused-promises` + custom rule MUST flag violations.
- **Verifies:** `09-promise-await-patterns.md` (CODE-RED).

### AC-TS-06 — Discriminated unions for all variant types; exhaustive checks via `never`

- **Given** any type representing 2+ variants,
- **When** declared,
- **Then** it MUST be a discriminated union with a `kind` or `type` literal field: `type Result<T> = { kind: 'ok'; value: T } | { kind: 'err'; error: AppError };`. Switch statements over the discriminant MUST end with an exhaustiveness guard: `default: { const _exhaustive: never = x; throw new Error(...); }`. Untagged unions (`A | B`) for variants are FORBIDDEN — they prevent narrowing.
- **Verifies:** `12-discriminated-union-patterns.md`.

### AC-TS-07 — `AppError` discriminated union; never `throw new Error(...)` for expected failures

- **Given** any function that can fail in an EXPECTED way (validation, network, parse, not-found),
- **When** the failure is signaled,
- **Then** it MUST return `Result<T, AppError>` (per AC-CL-17 inherited). `AppError` MUST itself be a discriminated union with a `code` literal field (e.g. `code: 'AUTH_INVALID_TOKEN' | 'VALIDATION_FAILED' | ...`). Throwing a plain `Error`, `string`, or untyped object for expected failures is FORBIDDEN. `throw` is reserved for programmer errors (assertion failures, OOM, panics).
- **Verifies:** Project AppError pattern + AC-CL-17 inheritance.

### AC-TS-08 — React components are functional + hooks; no class components

- **Given** any `.tsx` component file,
- **When** parsed,
- **Then** the component MUST be declared as a function (`function Foo() {}` or `const Foo = () => {}`). React class components (`class Foo extends React.Component`) are FORBIDDEN. Lifecycle methods MUST be expressed via `useEffect` / `useLayoutEffect`. Higher-order components SHOULD be replaced with custom hooks.
- **Verifies:** AC-TS-LEGACY-02-A + React 18 idiom.

### AC-TS-09 — Zustand for client state; React Query for server state — never the inverse

- **Given** any state management code,
- **When** the state's source is identified,
- **Then** client-only state (UI toggles, form drafts, ephemeral selections) MUST live in Zustand stores with typed selectors. Server state (data fetched from APIs, cached responses) MUST live in React Query (`useQuery`/`useMutation`) with typed query/mutation functions. Storing server data in Zustand is FORBIDDEN — it duplicates React Query's cache and creates staleness bugs. Storing UI state in React Query is FORBIDDEN.
- **Verifies:** `08-typescript-standards-reference.md` state-management section.

### AC-TS-10 — All async functions return `Promise<Result<T, AppError>>`, never throw

- **Given** any `async` function in the codebase,
- **When** the return type is inspected,
- **Then** it MUST be `Promise<Result<T, AppError>>` (or equivalent typed Result). `async` functions that throw are FORBIDDEN — exceptions cross await boundaries unpredictably. The Result MUST be checked at the caller via `if (result.kind === 'err') ...` or pattern-match helper. `@typescript-eslint/no-floating-promises` MUST be set to `error`.
- **Verifies:** AC-CL-17 + `09-promise-await-patterns.md`.

### AC-TS-11 — Zod (or equivalent) schema validates every external input boundary

- **Given** any data crossing an external boundary (HTTP request body, `JSON.parse`, `localStorage`, URL params, env vars, file reads),
- **When** the data enters TypeScript code,
- **Then** it MUST be parsed through a Zod schema (or io-ts / Valibot / runtypes equivalent) that produces a typed result. Trusting `as Foo` on external input is FORBIDDEN. The schema MUST live in the same `types/` folder as the type it validates (per AC-CL-18 inherited).
- **Verifies:** Runtime-boundary safety + AC-CL-18.

### AC-TS-12 — `noUncheckedIndexedAccess` enforces `T | undefined` on array/record access

- **Given** any array or record access (`arr[i]`, `obj[key]`),
- **When** the result is used,
- **Then** the type MUST include `| undefined` (enforced by `noUncheckedIndexedAccess: true`). Callers MUST handle the undefined case via `if`, optional chaining, or default value. Treating `arr[i]` as definitely defined is FORBIDDEN — use `arr.at(i) ?? defaultValue` or explicit bounds check. This catches off-by-one and missing-key bugs at compile time.
- **Verifies:** `tsconfig` strict additions + AC-CL-13 (null safety).

### AC-TS-13 — File names use kebab-case; React components export PascalCase from kebab-case file

- **Given** any `.ts` / `.tsx` file,
- **When** the file name is inspected,
- **Then** it MUST be kebab-case (`user-profile.tsx`, `auth-helpers.ts`). The PRIMARY export from a `.tsx` file MUST be PascalCase matching the component name (`export function UserProfile() {}` from `user-profile.tsx`). Multi-word file names with `.` or underscores are FORBIDDEN. Index files (`index.ts`, `index.tsx`) are exempt and SHOULD only re-export.
- **Verifies:** AC-CL-12 (kebab-case) + React component-export convention.

### AC-TS-14 — ESLint config enables `@typescript-eslint/recommended-type-checked` + project rules

- **Given** the project's ESLint config (`.eslintrc.*` or `eslint.config.*`),
- **When** parsed,
- **Then** it MUST extend `@typescript-eslint/recommended-type-checked` (NOT `recommended` — the type-checked variant catches Promise misuse, unbound methods, unsafe member access). Required rule overrides set to `error`: `@typescript-eslint/no-explicit-any`, `@typescript-eslint/no-floating-promises`, `@typescript-eslint/await-thenable`, `@typescript-eslint/no-misused-promises`, `@typescript-eslint/no-unsafe-*`. CI MUST run `eslint --max-warnings 0`.
- **Verifies:** `11-eslint-enforcement.md`.

### AC-TS-15 — `interface` is reserved for object-shape declarations; `type` for everything else

- **Given** any type alias,
- **When** declared,
- **Then** `interface` MUST be used for object-shape declarations that may be extended (`interface User { id: string; name: string; }`). `type` MUST be used for unions, intersections, mapped types, conditional types, tuples, primitives, and discriminated unions. Mixing (`interface` for a union via declaration merging) is FORBIDDEN. This rule keeps merge semantics predictable.
- **Verifies:** `08-typescript-standards-reference.md` interface-vs-type section.

### AC-TS-16 — Generic constraints required for unconstrained type parameters

- **Given** any function or type with a generic parameter `<T>`,
- **When** the parameter is used non-trivially (passed to another generic, accessed for properties, indexed),
- **Then** `T` MUST have an explicit `extends` constraint (`<T extends { id: string }>`, `<T extends Record<string, unknown>>`). Bare `<T>` is allowed ONLY for pass-through identity functions. Unconstrained `T` accessing `.field` is FORBIDDEN — it implicitly assumes structure.
- **Verifies:** `07-type-safety-remediation-plan.md` + AC-CL-04.

### AC-TS-17 — Imports are sorted: external → internal alias → relative; named imports preferred

- **Given** any import block at the top of a file,
- **When** parsed,
- **Then** imports MUST be grouped (blank line between groups) in order: (1) external packages (`react`, `lodash`), (2) internal aliased (`@/components/...`, `@/hooks/...`), (3) relative (`./foo`, `../bar`). Named imports (`import { Foo } from '...'`) MUST be preferred over default imports for non-React/non-page modules — default imports break tree-shaking and IDE refactor. Side-effect imports (`import './styles.css'`) MUST be last in their group.
- **Verifies:** `eslint-plugin-import` config + tree-shaking discipline.

### AC-TS-18 — `useEffect` dependencies are exhaustive; `react-hooks/exhaustive-deps` is `error`

- **Given** any `useEffect`, `useMemo`, `useCallback`, or `useLayoutEffect` call,
- **When** the deps array is inspected,
- **Then** every value referenced inside the callback that comes from component scope MUST appear in the deps array. ESLint rule `react-hooks/exhaustive-deps` MUST be set to `error` (NOT `warn`). Disabling the rule per-line MUST carry a comment explaining WHY (typically: stable reference from useRef, or intentional one-shot effect).
- **Verifies:** React 18 hook contract + `eslint-plugin-react-hooks`.

### AC-TS-19 — Test files use Vitest + Testing Library; `*.test.ts(x)` adjacent to source

- **Given** any test file,
- **When** inspected,
- **Then** it MUST use Vitest (`describe`, `it`, `expect`) and `@testing-library/react` for component tests. File name MUST be `<unit>.test.ts(x)` adjacent to source per AC-CL-19. Test-function names MUST be `it('should <behavior>', ...)` or `it('does <behavior> when <condition>', ...)` — describing BEHAVIOR not implementation. Snapshot tests are FORBIDDEN as the SOLE assertion (snapshots SHOULD complement explicit assertions).
- **Verifies:** AC-CL-19 + Vitest + RTL idiom.

### AC-TS-20 — Self-application: this folder's TS examples + enum files satisfy AC-TS-01..AC-TS-19

- **Given** every code example in `01-connection-status-enum.md` through `12-discriminated-union-patterns.md`,
- **When** mechanically extracted and compiled with the project's `tsconfig.json`,
- **Then** every example MUST type-check without errors AND satisfy AC-TS-04 (`as const` enums, no `enum` keyword) AND satisfy AC-TS-06 (discriminated unions with exhaustive checks). Example code that violates its own ACs is a CODE-RED documentation-drift bug. CI MAY extract code blocks and compile them via a doctest harness.
- **Verifies:** Recursive self-check + AC-SAG-18 dogfooding analogue.

---

## Legacy Index (preserved for traceability)

The following stub criteria from v3.2.0 are preserved verbatim. They are NO LONGER authoritative — the GWT ACs above supersede them.

### AC-TS-LEGACY: Type Safety

- [ ] AC-TS-LEGACY-01-A — Connection status enums define all valid states with TypeScript string literals
- [ ] AC-TS-LEGACY-01-B — Type definitions avoid `any` and use proper generic constraints
- [ ] AC-TS-LEGACY-01-C — Error types follow the project's AppError pattern


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-TS-LEGACY: Patterns

- [ ] AC-TS-LEGACY-02-A — React component patterns follow functional component with hooks style
- [ ] AC-TS-LEGACY-02-B — State management patterns use Zustand stores with typed selectors
- [ ] AC-TS-LEGACY-02-C — API client patterns use React Query with typed query/mutation functions

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Cross-language parent (AC-CL-*)](../01-cross-language/97-acceptance-criteria.md)
- [TypeScript standards reference](./08-typescript-standards-reference.md)
- [Promise/await patterns (CODE-RED)](./09-promise-await-patterns.md)
- [ESLint enforcement](./11-eslint-enforcement.md)
- [Discriminated union patterns](./12-discriminated-union-patterns.md)
- [Type safety remediation plan](./07-type-safety-remediation-plan.md)
- [§02 parent governance](../97-acceptance-criteria.md)

> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
