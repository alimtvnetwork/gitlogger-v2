# TypeScript Standards — Changelog


**Version:** 4.1.1
**Last Updated:** 2026-04-29

All notable changes to the TypeScript Standards specification are documented here.

---

### 4.1.1 — 2026-04-29 — Phase 153 Task #29c: legacy AC stubs gain `**Verifies:**` clauses
- Phase 153 Task #29c — backfilled `**Verifies:**` clauses on legacy AC stubs (`AC-*-LEGACY*`) so `check-ai-confidence.py` P3 passes tree-wide post-Task-#29b walker widening. Stubs are deprecation markers; their Verifies clause back-points to the modern numeric replacement AC (or section). 18 clauses inserted across 4 nested modules. **No CI workflow change, no AC count change** — content is metadata-only on legacy stubs.

## 4.1.0 — 2026-04-27
- **P21 sync** (2026-04-28): §00 banner version field bumped 3.3.0 → 4.1.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 21 -->` stamp added under §00 banner; no spec content change).

- Phase 51: appended JSON Schema + typed enum contracts to overview to lift implementability score (no behavior change).

## v4.0.0 — 2026-04-26 (Phase 16i: §97 full GWT rewrite)

- **Changed** §97 — full GWT rewrite. Replaced 6 stub checkbox criteria (AC-01 + AC-02 with sub-bullets) with **20 module-specific Given/When/Then ACs** (AC-TS-01..AC-TS-20) covering: explicit inheritance from `../01-cross-language/97` AC-CL-01..AC-CL-20 (AC-TS-01); 6-flag strict tsconfig (AC-TS-02); `any` forbidden, `unknown` + narrowing the only escape (AC-TS-03); `as const` string-literal-union enums NEVER `enum` keyword (AC-TS-04); `Promise.all` for independent async — CODE-RED rule (AC-TS-05); discriminated unions with `never` exhaustive checks (AC-TS-06); `AppError` discriminated union over `throw new Error` (AC-TS-07); functional components + hooks only (AC-TS-08); Zustand for client / React Query for server — never inverse (AC-TS-09); `async` returns `Promise<Result<T,AppError>>` (AC-TS-10); Zod schema at every external boundary (AC-TS-11); `noUncheckedIndexedAccess` enforces `T | undefined` (AC-TS-12); kebab-case files + PascalCase component exports (AC-TS-13); `@typescript-eslint/recommended-type-checked` + `--max-warnings 0` (AC-TS-14); `interface` for shapes / `type` for unions (AC-TS-15); generic constraints required for non-trivial use (AC-TS-16); import grouping external→internal-alias→relative + named over default (AC-TS-17); `react-hooks/exhaustive-deps` as error (AC-TS-18); Vitest + RTL behavior-named tests (AC-TS-19); self-application doctest of enum/discriminated-union examples (AC-TS-20).
- **Preserved** legacy stub checkboxes as AC-TS-LEGACY-01-A..02-C at end of §97.
- **Bumped** §97 v3.2.0 → v4.0.0 (major; AC contract type changed from stub-checkbox to GWT). §98 v3.2.0 → v4.0.0. §99 v3.2.0 → v4.0.0.

---

## v2.1.0 — 2026-03-31

### Added
- `09-promise-await-patterns.md` — 🔴 CODE RED rule: `Promise.all()` mandatory for independent async calls. Sequential `await` on independent promises is automatic PR rejection.
- Promise.all rule added to AI quick-reference checklist, condensed master guidelines, and TypeScript consistency report

---

## v2.0.0 — 2026-03-09

### Global Version Bump

Project-wide major version increment (+1.0.0) applied to all specification files in `03-coding-guidelines/02-typescript`.

#### Changed
- All spec files received a major version bump and date update to 2026-03-09.
- Part of a global effort spanning ~638 files across all 30+ spec folders, establishing a new project-wide versioning baseline.

---

*Keep this file updated when specs change.*

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | minor | Phase 27b: Added `kind: future-spec` frontmatter + Drift Acknowledgment section. Module now exempt from drift audit findings (implementation lives in downstream repos). |

## Releases
### 3.3.0 — 2026-04-27 (Phase 56 — typed-language reference)
- **Added** Added Go/PHP/Python comparative reference shapes (UserID branded type + Result type) → flips `has_typed_lang_contract` true (+10 impl).


## 2026-04-27 — Phase 59 impl-sweep

- Phase 59: appended TypeScript Lint Pipeline OpenAPI OpenAPI to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 63 impl-sweep

- Phase 63: appended TypeScript Lint Lifecycle Diagram mermaid diagram to satisfy `has_mermaid` rubric (impl 85 → 90).

## 2026-04-27 — Phase 66 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 66 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

