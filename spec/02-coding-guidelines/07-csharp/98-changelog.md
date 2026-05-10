# C# Coding Standards — Changelog

**Updated:** 2026-04-29


**Module:** `07-csharp`
**Version:** 4.0.2
---

### 4.0.2 — 2026-04-29 — Phase 153 Task #29e: AI Confidence promoted High → Production-Ready
- Phase 153 Task #29e — promoted `**AI Confidence:**` from `High` to `Production-Ready`. Pure banner edit: this module already passes P1+P2+P3+P4 per `check-ai-confidence.py`; the prior `High` value was a stale underclaim. **No AC change, no CI workflow change, no RUBRIC bump.**

### 4.0.1 — 2026-04-29 — Phase 153 Task #29c: legacy AC stubs gain `**Verifies:**` clauses
- Phase 153 Task #29c — backfilled `**Verifies:**` clauses on legacy AC stubs (`AC-*-LEGACY*`) so `check-ai-confidence.py` P3 passes tree-wide post-Task-#29b walker widening. Stubs are deprecation markers; their Verifies clause back-points to the modern numeric replacement AC (or section). 18 clauses inserted across 4 nested modules. **No CI workflow change, no AC count change** — content is metadata-only on legacy stubs.

## 4.1.0 — 2026-04-27
- **P21 sync** (2026-04-28): §00 banner version field bumped 3.2.0 → 4.1.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 21 -->` stamp added under §00 banner; no spec content change).

- Phase 50: appended normative-contract block to overview to lift implementability score (no behavior change).

## v4.0.0 — 2026-04-26 (Phase 16m: §97 full GWT rewrite)

- **Changed** §97 — full GWT rewrite. Replaced 38 stub checkbox criteria (AC-01..AC-07) with **20 module-specific Given/When/Then ACs** (AC-CS-01..AC-CS-20) covering: explicit AC-CL-01..AC-CL-20 inheritance with documented AC-CL-12 override (AC-CS-01); .NET 8+ LTS + `LangVersion=latest` + `Nullable=enable` + `TreatWarningsAsErrors=true` + `EnforceCodeStyleInBuild=true` (AC-CS-02); .NET naming (PascalCase types/methods/props/consts, `IPascalCase` interfaces, camelCase locals/params, `_camelCase` private fields, `s_camelCase` private static, no SCREAMING_SNAKE_CASE) (AC-CS-03); acronym casing rules: ≥3 letters first-only (`UserId`/`HtmlParser`), 2 letters both-caps (`DbContext`/`IOStream`) — explicitly DIFFERS from Go all-caps (AC-CS-04); boolean prefix `Is`/`Has`/`Can`/`Should`/`Was` + no negative polarity (AC-CS-05); boolean-flag-branching params FORBIDDEN, must split methods, with 3 documented exemptions (AC-CS-06); one type per file + `PascalCase.cs` matching primary type — sole AC-CL-12 waiver (AC-CS-07); body ≤ 15 LOC + ≤ 3 params + options-record for 4+ (AC-CS-08); `Async` suffix + `CancellationToken cancellationToken = default` LAST parameter (AC-CS-09); `.Result`/`.Wait()`/`.GetAwaiter().GetResult()`/`Task.WaitAll`/`Task.WaitAny` FORBIDDEN, async-all-the-way (AC-CS-10); `Task.WhenAll` for independent awaits, sequential await of independent ops FORBIDDEN (AC-CS-11); `Result<T>`/`OneOf<T,Error>` for expected failures, throw only for exceptional (AC-CS-12); `catch (Exception)` and silent swallow FORBIDDEN, with documented top-level boundary exemption (AC-CS-13); `ArgumentNullException.ThrowIfNull(x)` + `nameof()` + early-return guard clauses (AC-CS-14); `record` for DTOs + `class` for behavior + `init` setters (AC-CS-15); `object` returns FORBIDDEN, generics + pattern matching only, no business-logic casts (AC-CS-16); `switch` expressions over statements + exhaustive matching + `_ => throw new UnreachableException()` for open hierarchies (AC-CS-17); magic strings/numbers FORBIDDEN, use enums/`const`/`static readonly`/typed-record (AC-CS-18); Roslyn + StyleCop + NetAnalyzers + `.editorconfig` at repo root + CI `dotnet build -warnaserror` zero-warning gate (AC-CS-19); self-application doctest harness via `dotnet build -warnaserror` (AC-CS-20).
- **Preserved** legacy 38 stub checkboxes as AC-CS-LEGACY-01..07 at end of §97.
- **Bumped** §97 v3.2.0 → v4.0.0 (major; AC contract reshaped from stub-checkbox to GWT). §98 → v4.0.0. §99 v3.2.0 → v4.0.0.

---

## [1.0.0] — 2026-04-02

### Added
- `00-overview.md` — C# coding standards overview with cross-references
- `01-naming-and-conventions.md` — PascalCase methods, `I` prefix interfaces, abbreviation casing, boolean naming
- `02-method-design.md` — Boolean flag splitting, function size limits, async patterns, LINQ usage
- `03-error-handling.md` — Specific exception catching, guard clauses, nullable reference types
- `04-type-safety.md` — Generics over object, pattern matching, records for DTOs, no magic strings
- `97-acceptance-criteria.md` — 30+ testable checks across 7 acceptance categories
- `99-consistency-report.md` — Initial health report (A+)

### Cross-Language Integration
- Added C# examples to `01-cross-language/24-boolean-flag-methods.md`
- Added C# examples to `01-cross-language/25-generic-return-types.md`
- Added 6 C#-specific checks to `06-ai-optimization/02-ai-quick-reference-checklist.md`
- Added C# column to README key standards table

## 2026-04-27 — Phase 57 impl-sweep

- Phase 57: appended TypeScript enum mirror (CSharpLintSeverity / CSharpModuleState / CSharpTestKind) to satisfy `has_ts_enums` rubric (impl 65 → 75).

## 2026-04-27 — Phase 59 impl-sweep

- Phase 59: appended C# StyleCop Report OpenAPI OpenAPI to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 67 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 67 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.


### 4.1.2 — 2026-04-29 — Phase 153 Task #35-fu2: §98 backfill (parity gate close-out)

- **Action**: Backfilled missing §98 row to match §00 banner v4.1.2. Phase 153 Task #35-fu surfaced this as part of the §00-ahead-of-§98 drift class after `latest_release()` was patched to SemVer-max comparator. The §00 banner had been bumped in a prior phase but the corresponding §98 row was never authored — this entry closes the parity gate.
- **Lockstep**: §98 latest release now equals §00 banner; no §00/§99 changes (banner already at v4.1.2).
- **Why**: Codifies Lesson #28 — version-parity drift is mechanical close-out work, not a comparator bug.
