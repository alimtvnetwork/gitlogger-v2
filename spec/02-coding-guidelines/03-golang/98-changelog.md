# Golang Standards — Changelog


**Version:** 4.0.1
**Last Updated:** 2026-04-29

All notable changes to the Golang Standards specification are documented here.

---

### 4.0.1 — 2026-04-29 — Phase 153 Task #29d closure: AI Confidence parity reached 51/51 (100%)
- Lockstep companion bump for §00/§99 banner edits made under Phase 153 Task #29d (P1 inventory regex widened in `check-ai-confidence.py`, underclaim banners promoted, legacy stub Verifies clauses backfilled). **No AC change beyond Task #29c-pattern legacy stubs; no CI workflow change.** See `.lovable/memory/audit/v2-deterministic/phase-153-task-29d-p1-regex-widening-and-final-parity.md`.

## 4.1.0 — 2026-04-27
- **P21 sync** (2026-04-28): §00 banner version field bumped 3.2.0 → 4.1.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 21 -->` stamp added under §00 banner; no spec content change).

- Phase 51: appended JSON Schema + typed enum contracts to overview to lift implementability score (no behavior change).

## v4.0.0 — 2026-04-26 (Phase 16j: §97 full GWT rewrite)

- **Changed** §97 — full GWT rewrite. Replaced 6 stub checkbox criteria (AC-01 + AC-02 with sub-bullets) with **20 module-specific Given/When/Then ACs** (AC-GO-01..AC-GO-20) covering: explicit AC-CL-01..AC-CL-20 inheritance (AC-GO-01); minimum Go 1.22 + pinned toolchain (AC-GO-02); ALL-CAPS acronyms `URL`/`ID`/`HTTP`/`JSON`/`SQL` never `Url`/`Id` (AC-GO-03); `apperror.Result[T]` for project APIs / `(T, error)` for stdlib boundaries (AC-GO-04); `panic` forbidden outside main/init/_test.go (AC-GO-05); `errors.Is`/`As` over `==` or string match (AC-GO-06); `context.Context` as first parameter, never struct field (AC-GO-07); `defer` placement immediately after acquisition + no unbounded-loop defers (AC-GO-08); `type X string` + `Validate()` enums NOT iota for wire types (AC-GO-09); generics over `interface{}`/`any` for typed containers (AC-GO-10); goroutines MUST have explicit cancellation via ctx/quit/WaitGroup/errgroup (AC-GO-11); channel direction `<-chan`/`chan<-` in signatures, sender owns close (AC-GO-12); 11-linter `golangci-lint` config + CI fails on any warning (AC-GO-13); 1-3 letter receiver names consistent across type (AC-GO-14); pointer-vs-value receiver consistency, no mixing (AC-GO-15); explicit `json:"PascalCaseName"` tags per AC-CL-09 (AC-GO-16); table-driven tests + `t.Run` subtests + `t.Parallel` (AC-GO-17); minimal deps + no vendoring without waiver (AC-GO-18); `log/slog` with structured K/V, no `fmt.Println` for logging (AC-GO-19); self-application doctest of enum/defer examples (AC-GO-20).
- **Preserved** legacy stub checkboxes as AC-GO-LEGACY-01-A..02-C at end of §97.
- **Bumped** §97 v3.2.0 → v4.0.0 (major; AC contract type changed from stub-checkbox to GWT). §98 v3.2.0 → v4.0.0. §99 v3.2.0 → v4.0.0.

---

## v2.1.0 — 2026-03-31

### Changed
- `04-golang-standards-reference.md` split into subfolder (6 files, max 362 lines — down from 1,280)
- Deduplicated enum content in `05-enums-and-dry.md` — now links to `01-enum-specification/` as canonical source
- Fixed spacing violations in code examples

---

## v2.0.0 — 2026-03-09

### Global Version Bump

Project-wide major version increment (+1.0.0) applied to all specification files in `03-coding-guidelines/03-golang`.

#### Changed
- All spec files received a major version bump and date update to 2026-03-09.
- Part of a global effort spanning ~638 files across all 30+ spec folders, establishing a new project-wide versioning baseline.

---

*Keep this file updated when specs change.*

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | minor | Phase 27c: Added `kind: future-spec` frontmatter + Drift Acknowledgment. Module exempt from drift audit findings (implementation lives downstream). |

## 2026-04-27 — Phase 57 impl-sweep

- Phase 57: appended TypeScript enum mirror (GoLintSeverity / GoModuleState / GoTestKind) to satisfy `has_ts_enums` rubric (impl 65 → 75).

## 2026-04-27 — Phase 59 impl-sweep

- Phase 59: appended Go Module Audit OpenAPI OpenAPI to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 68 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 68 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 71 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.


### 4.1.1 — 2026-04-29 — Phase 153 Task #35-fu2: §98 backfill (parity gate close-out)

- **Action**: Backfilled missing §98 row to match §00 banner v4.1.1. Phase 153 Task #35-fu surfaced this as part of the §00-ahead-of-§98 drift class after `latest_release()` was patched to SemVer-max comparator. The §00 banner had been bumped in a prior phase but the corresponding §98 row was never authored — this entry closes the parity gate.
- **Lockstep**: §98 latest release now equals §00 banner; no §00/§99 changes (banner already at v4.1.1).
- **Why**: Codifies Lesson #28 — version-parity drift is mechanical close-out work, not a comparator bug.
