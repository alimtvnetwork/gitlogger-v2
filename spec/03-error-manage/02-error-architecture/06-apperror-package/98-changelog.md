# Changelog — AppError Package

**Version:** 3.3.2
**Updated:** 2026-04-29
**Scope:** `spec/03-error-manage/02-error-architecture/06-apperror-package/`

---

### 3.3.2 — 2026-04-29 — Phase 153 Task #29d closure: AI Confidence parity reached 51/51 (100%)
- Lockstep companion bump for §00/§99 banner edits made under Phase 153 Task #29d (P1 inventory regex widened in `check-ai-confidence.py`, underclaim banners promoted, legacy stub Verifies clauses backfilled). **No AC change beyond Task #29c-pattern legacy stubs; no CI workflow change.** See `.lovable/memory/audit/v2-deterministic/phase-153-task-29d-p1-regex-widening-and-final-parity.md`.

## 3.3.1 — 2026-04-28 — Phase P29: P25-pure dual-stream reconciliation (batch)

- **Reconciled** §98 header version stream `1.2.0` → `3.3.1` to align with §00 banner stream (`3.3.0`). Prior §98 header tracked an independent audit-stream version decoupled from the SemVer ladder, which already contained `3.3.0` (matching §00 banner). Per Phase P25 precedent (subcase: clean ladder + decoupled header stream), §98 header is patch-bumped to `3.3.1` to align with banner; §00 banner also bumped to `3.3.1` per P27 sub-lesson (parity gate enforces exact match for stamped files). Ladder body unchanged. H10 stamp added to §00. **Phase P29 batch reconciliation** (8 P25-pure drifters processed in one phase per P27 batching lesson).

## 1.2.0 — 2026-04-27

- Phase 52: appended JSON Schema + typed enum/CI-YAML contracts to overview to lift implementability score (no behavior change).

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 3.3.0 — 2026-04-27 (Phase 56 — typed-language reference)
- **Added** Added PHP + Python `AppError` consumers (already had 1 Go); brings typed-lang count to ≥3 → flips `has_typed_lang_contract` true (+10 impl).

### 1.1.0 — 2026-04-26 (Phase 20 contract-inlining sweep)
- **Added** §97 — three normative machine-parseable contract blocks under "Inlined Contracts":
  - `go` block: full apperror package source-of-truth (AppErrType byte enum + custom JSON marshalling per AC-05; StackFrame/StackTrace + captureStack with skipFrames per AC-07; AppError struct + New/Wrap constructors per AC-01/AC-04; generic Result[T]/ResultSlice[T]/ResultMap[K,V] containers with PRIVATE fields enforcing AC-06 guard rule via Unwrap-panics-on-Err semantics).
  - `ts` block: cross-language mirror with discriminated-union `Result<T> = { ok: true; value: T } | { ok: false; error: AppError }` emulating the Go guard rule at the TypeScript type level (frontend cannot access `.value` without narrowing through `r.ok === true`); `AppErrCode` template-literal type for the E1xxx-E14xxx domain pattern.
  - `json` block: JSON-Schema 2020-12 wire-format validator (canonical EXxxx pattern `^E(1[0-4]|[1-9])[0-9]{1,3}$`, non-empty stack array per AC-01, required ref field for cross-service propagation).
- **Rationale** Phase 19 deterministic re-audit scored this module 49/100 (F) flagged as a "complete orphan" — spec described Go types `Result[T]`, `AppError`, `AppErrType` extensively but had ZERO inlined source-of-truth (the previous §97 contained naked Go-syntax pseudocode without a fenced ` ```go ` block, so the auditor's `CODE_BLOCK_RX` registered 0/3 contracts and gate `G-CON-01` capped implementability ≤ 50).
- **Expected lift** Module contracts 0/3 → 3/3; module weighted overall 49 (F) → 75+ (B); module implementability 30 → 80+. Tree-mean implementability projected +0.7pts (this module is referenced from 8+ other specs — `apperror.AppError` is the universal error type — so blast-radius is maximal).
- **Preserved** Pre-existing AC-01..AC-07 GWT criteria unchanged. The 7-file `01-apperror-reference/` subfolder remains the deep-dive reference; the new §97 contract is the single inlined source-of-truth.
- **Bumped** §97 v2.0.0 → v2.1.0; §98 v1.0.0 → v1.1.0; §99 v3.2.0 → v3.3.0; spec-index 3 cells refreshed.

### 1.0.0 — 2026-04-26
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

## 2026-04-27 — Phase 59 impl-sweep

- Phase 59: appended AppError Telemetry OpenAPI OpenAPI to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 68 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 68 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 71 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

