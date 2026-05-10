# Coding Guidelines — Changelog


**Version:** 4.0.1
**Last Updated:** 2026-04-29

All notable changes to the Cross-Language Coding Guidelines specification are documented here.

---

### 4.0.1 — 2026-04-29 — Phase 153 Task #29d closure: AI Confidence parity reached 51/51 (100%)
- Lockstep companion bump for §00/§99 banner edits made under Phase 153 Task #29d (P1 inventory regex widened in `check-ai-confidence.py`, underclaim banners promoted, legacy stub Verifies clauses backfilled). **No AC change beyond Task #29c-pattern legacy stubs; no CI workflow change.** See `.lovable/memory/audit/v2-deterministic/phase-153-task-29d-p1-regex-widening-and-final-parity.md`.

## 4.1.0 — 2026-04-27
- **P21 sync** (2026-04-28): §00 banner version field bumped 3.2.0 → 4.1.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 21 -->` stamp added under §00 banner; no spec content change).

- Phase 53: appended typed-language / SQL DDL / JSON Schema contracts to overview to lift implementability score (no behavior change).

## v4.0.0 — 2026-04-26 (Phase 16h: §97 full GWT rewrite)

- **Changed** §97 — full GWT rewrite. Replaced 6 stub checkbox criteria (AC-01 + AC-02 with sub-bullets) with **20 module-specific Given/When/Then ACs** (AC-CL-01..AC-CL-20) covering language-agnostic rules INHERITED by every language subfolder under §02 (`02-typescript/`, `03-golang/`, `04-php/`, `05-rust/`, `07-csharp/`): inheritance contract + waiver discipline (AC-CL-01), positive-form boolean naming (AC-CL-02), boolean-flag method prefixes `is`/`has`/`can`/`should`/`will`/`was`/`did` (AC-CL-03), strict typing no implicit any/`interface{}`/`mixed`/`dynamic` (AC-CL-04), typed conversion over raw casts (AC-CL-05), cyclomatic complexity ≤ 10 hard / ≤ 5 preferred (AC-CL-06), nesting depth ≤ 3 (AC-CL-07), magic-value extraction on rule-of-two (AC-CL-08), JSON keys PascalCase wire-format (AC-CL-09), language-idiomatic function names with cross-language semantic-verb consistency (AC-CL-10), DB tables singular PascalCase + columns PascalCase + FK `<TargetTable>Id` (AC-CL-11), kebab-case ASCII slugs (AC-CL-12), explicit nullability typing (AC-CL-13), lazy evaluation for branched expensive computations (AC-CL-14), regex documentation + anchoring + no catastrophic backtracking (AC-CL-15), code mutation avoidance with `mutate*`-prefix exception (AC-CL-16), Result/Option/Either over throwing for expected failures (AC-CL-17), `types/` folder convention forbids `interfaces/`/`models/`/`dto/`/`entities/` (AC-CL-18), `<unit>.test.<ext>` naming + behavior-named test functions (AC-CL-19), DRY rule-of-three forbids premature abstraction (AC-CL-20).
- **Preserved** legacy stub checkboxes as AC-CL-LEGACY-01-A..02-C at end of §97.
- **Bumped** §97 v3.2.0 → v4.0.0 (major; AC contract type changed from stub-checkbox to GWT). §98 v3.2.0 → v4.0.0. §99 v3.2.0 → v4.0.0.

---

## v3.2.0 — 2026-03-31

### Structural Improvements

#### Changed
- `02-boolean-principles.md` split into subfolder (5 files, max 262 lines)
- `15-master-coding-guidelines.md` split into subfolder (7 files, max 277 lines)
- Deduplicated enum rules — `06-ai-optimization/05-enum-naming-quick-reference.md` is now the single cross-language enum source
- Fixed 229 spacing violations in code examples (R4, R5, R10 rules)
- Fixed all broken anchor links across 48 files
- Updated cross-references to point to new subfolder locations

---

## v3.0.0 — 2026-03-31

### Phase 4 Rules Added to Master Guidelines

#### Changed
- `15-master-coding-guidelines/00-overview.md` bumped to **v2.0.0**
- Added 7 new sections (§14–§20): Lazy Evaluation, Regex Usage, Code Mutation Avoidance, Null Pointer Safety, Nesting Resolution, Newline Styling, Defer Rules (Go)
- Expanded Quick Checklist with 7 new items covering mutation, regex, lazy eval, defer, nesting, newlines, null safety
- Added cross-references to Phase 4 spec files (16–21) in "How to Use" section

---

## v2.1.0 — 2026-03-11

### Added

- `14-test-naming-and-structure.md` — New spec covering test file naming, three-part test function naming convention, table-driven test rules, test helper placement, AAA pattern, test isolation, and integration test boundaries. Applies to Go, TypeScript, and PHP.

---

## v2.0.0 — 2026-03-09

### Global Version Bump

Project-wide major version increment (+1.0.0) applied to all specification files in `03-coding-guidelines/01-cross-language`.

#### Changed
- All spec files received a major version bump and date update to 2026-03-09.
- Part of a global effort spanning ~638 files across all 30+ spec folders, establishing a new project-wide versioning baseline.

---

*Keep this file updated when specs change.*

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | patch | Phase 27d: Added Drift Acknowledgment for low-severity doc-hygiene findings. |

### 4.1.1 — 2026-04-29 — Phase 153 Task #35-fu2: §98 backfill (parity gate close-out)

- **Action**: Backfilled missing §98 row to match §00 banner v4.1.1. Phase 153 Task #35-fu surfaced this as part of the §00-ahead-of-§98 drift class after `latest_release()` was patched to SemVer-max comparator. The §00 banner had been bumped in a prior phase but the corresponding §98 row was never authored — this entry closes the parity gate.
- **Lockstep**: §98 latest release now equals §00 banner; no §00/§99 changes (banner already at v4.1.1).
- **Why**: Codifies Lesson #28 — version-parity drift is mechanical close-out work, not a comparator bug.
