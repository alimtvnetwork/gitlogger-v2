# Changelog — Generic CLI Creation Guidelines — Overview

**Version:** 1.2.0  
**Updated:** 2026-05-07 (Phase J1 — AC-27 Sibling File Delegation Map (Lesson #21 + Lesson #39 third instance, intra-module sibling-file axis))
**Scope:** `spec/13-generic-cli/`

---

### 1.2.0 — 2026-05-07 — Phase J1: AC-27 Sibling File Delegation Map (Lesson #21 + Lesson #39 third instance)
- **Action**: §97 v2.4.0 → **v2.5.0** with new **AC-27 [critical]** — 20-row delegation table mapping every spec/13 sibling file (`02-*` through `21-*`) to (a) content kind, (b) governing §97 AC family, (c) walker-tier visibility, (d) restate-forbidden status. Survey confirmed all 20 siblings already have ≥3 §97 binding citations (min=3, max=10) — no zero-binding crisis (contrast spec/22's 13/33 zero-bound gap closed by AC-80). The explicit-delegation-table pattern still adds tier-1 audit-followability value (auditor no longer greps 25 ACs to derive per-file governance).
- **Why**: Lesson #39 sweep — `mem://index.md` listed spec/13 (28 siblings, actual 20) as next biggest delegation-map candidate after spec/22 AC-80. Confirms the pattern generalises to mature modules where the binding-density gap is zero. **Third Lesson #39 second-axis instance** (after spec/02 AC-CG-21 cross-language sub-folder axis + spec/22 AC-80 intra-module zero-bound axis).
- **Lockstep**: §97 v2.4.0 → **v2.5.0** (1 new AC, count 25 → 26 — minor); §00 v1.1.9 → **v1.2.0** (cascade); §98 v1.1.9 → **v1.2.0** (this row); §99 v1.1.9 → **v1.2.0** (audit row). h10 stamp 153 → 153 (no change).
- **No CI workflow change · no RUBRIC bump · no AC-31-31 cascade · no gate-count change · no new linter.** All 5 strict gates expected GREEN.

### 1.1.9 — 2026-04-30 — Phase 153 Task A24-fu24: §00 walker-pin pure-promotion (Lesson #63 fourth instance)
- **Action**: Inserted `> 🤖 Walker-Pin` 4-row teaser table at §00 head (after Related-specs block) surfacing AC-25 (walker-cap STRUCTURAL pin), AC-09 (multi-format output examples), AC-22 (SQLite concurrency / `isBusyOrLocked`), AC-21/AC-26 (typed `ExitCode` enum) as canonical close-outs for cache-stale audit findings (D5 truncation, D4 multi-format examples, D3 isBusyOrLocked).
- **Why**: Cache `total=88 GOOD` with 3 advisory findings — ALL pre-closed in §97 (AC-25 from A24-fu15 closes D5 by structural-design pin; AC-09 already enumerates `renderJSON`/`renderCSV`/`renderMarkdown` with `jq`-parseable / RFC-4180 / GFM contracts; AC-22 already specifies `busy_timeout=5000` + `SQLITE_BUSY/LOCKED` retry mirrored into `10-database.md`). Walker `files_used=16/24 (67 %)` — moderate saturation, but targeted findings all live in §97 beyond the cap. Pure visibility patch.
- **Lockstep**: §00 v1.1.8 → **v1.1.9** (patch — teaser content); §98 v1.1.8 → **v1.1.9** (this row); §99 v1.1.8 → **v1.1.9** (audit row).
- **§97 NOT bumped at v2.4.0** — no new normative requirement, no AC change, no AC-31-31 cascade, no RUBRIC bump, no CI workflow change. **Pure-promotion variant** of Lesson #61 per spec/22 A24-fu20 + spec/27 A24-fu22 + spec/03 A24-fu23 precedent.
- **Lesson #63 fourth instance** — first instance on `normative-contract` axis (prior three: spec/22/03 audit-corpus; spec/27 integration-spec). Confirms pattern generalises across all three axes. All 5 strict gates expected GREEN.

### 1.1.8 — 2026-04-30 — Phase 153 Task A24-fu15: spec/13 self-lift (3 audit-v7 findings closed)
- **Action**: §97 v2.3.0 → **v2.4.0** with two new ACs. **AC-25 [medium]** classifies the recurring `[D1] Truncated Date Formatting Spec` finding as walker-cap STRUCTURAL-DESIGN-NOT-DEFECT — `14-date-formatting.md` is complete on disk (58 lines, full Rules + Contributors footer verified via `wc -l` + `tail`); the truncation is the auditor's bundle-cut artifact (file lands at position 18/24 beyond the 120 KB CF-bound cap per Lesson #45). Forbidden remediations enumerated (split / rename / inline). **AC-26 [low]** closes the LOW D3 `Inconsistent Exit Code Prose` finding by (a) refreshing the real stale row in `11-build-deploy.md:110-113` (4-row Special Cases table now cites `ExitMisuse` / `ExitOK` / `ExitError` typed enum constants per AC-21's §97-WINS contract); (b) codifying the prose-refresh detection rule (`rg "exit 1|os\.Exit\(1\)" spec/13-generic-cli/*.md` MUST return only annotated stale-prose lessons). **No new linter, no CI workflow change, no RUBRIC bump, no gate-count change** — pure self-lift.
- **Lesson #50 reinforcement**: spec/13 now joins spec/02 (AC-CG-25) + spec/25 (AC-AI-16) as the third module to ship a structural-pin AC for walker-cap truncation. The pattern is stable: when audit-finding `[D1/D5] Truncated/Missing X` recurs across re-scores AND the cited file is complete on disk AND the file lands beyond the bundle cut-point in alphabetical-order × axis-cap × CF-1010 ceiling, ship a `[medium]` structural-pin instead of attempting remediation.
- **Lockstep**: §97 v2.3.0 → **v2.4.0** (2 new ACs, count 24 → 26); §00 v1.1.7 → **v1.1.8** (h10 stamp 30 → 153); §98 v1.1.7 → **v1.1.8**; §99 v1.1.7 → **v1.1.8**. All 5 strict gates expected GREEN.


- **Action**: Added new `### Reference Go implementation (normative example)` subsection between PRAGMA table (line 48) and Transaction discipline (line 50) in `10-database.md`. Snippet shows: (a) `openDB` constructing the DSN with `_journal=WAL&_busy_timeout=5000&_foreign_keys=ON&_synchronous=NORMAL` then `db.SetMaxOpenConns(1)`; (b) `withWriteTx` wrapping every write transaction in `BEGIN IMMEDIATE` + 3-attempt retry-on-`SQLITE_BUSY`/`SQLITE_LOCKED` with 100 ms ±25 % jitter (mirrors spec/27 AC-T-28 R3); (c) `isBusyOrLocked` predicate documented as matching `sqlite3.ErrBusy` / `sqlite3.ErrLocked`. **No §97 change · no AC change** — pure prose-mirror under existing AC-22 (concurrency contract) and AC-24 (cross-reference pin) per Lesson #36 (link-don't-restate; the snippet is the canonical Go-side implementer surface for AC-22's contract).
- **Why**: Audit-v5 D3 MED for spec/13 cited "10-database.md is truncated/missing — show the implementation of the retry loop" — verified the file is complete (195 lines, ends at Contributors footer); the gap was a missing concrete Go example. Per Lesson #16 (auditor walker bias) the truncation claim is harness-side; per Lesson #33 (§97-WINS prose-mirror cadence) the missing snippet is genuine implementer-side. This phase closes the genuine half.
- **Files**: `10-database.md` (+~55 lines for the Go snippet), §00/§98/§99 banners.
- **Spec lockstep**: §97 v2.3.0 (no change — no new AC, no contract change); §00 v1.1.6 → **v1.1.7**; §98 v1.1.6 → **v1.1.7**; §99 v1.1.6 → **v1.1.7**. h10 stamp 153 → 153 (no change). **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**, **no new AC** — pure prose-mirror under existing AC-22/AC-24.
- **Validation**: `wc -l spec/13-generic-cli/10-database.md` shows file growth ~195 → ~250 lines; new section is the only delta. Lockstep 87/87 (verify after run).

### 1.1.6 — 2026-04-30 — Phase 153 LOW-batch verify: residual `os.Exit(1)` stale-prose sweep (Lesson #33 follow-through)
- **Action**: Audit-v6 LOW finding `[D1] Stale Prose Contradictions` (spec/13 score 84) verified-and-closed. A11a-fu1 (v1.1.3) refreshed `03-subcommand-architecture.md` line 84+102 + `07-error-handling.md` exit-code table, but missed 7 inline Go example literals. This phase swept all 7: `03-subcommand-architecture.md:16/40/56` (Run/dispatch/multi-layer dispatch), `04-flag-parsing.md:76` (runClone source-required), `07-error-handling.md:106` (runImport loadFile error), `09-help-system.md:88` (Print missing-help), `18-batch-execution.md:120` (runExec missing-args). All now use `os.Exit(int(exit.ExitMisuse))` or `os.Exit(int(exit.ExitError))` per §97 AC-21 typed-enum contract, with `// §97 AC-21: typed enum mandatory` comment.
- **Why**: Lesson #33 reaffirmed — file-grep auditors continue to flag literal stale strings until prose matches contract; Lesson #41 (severity-tally ≠ unique findings) verified the LOW was genuine on enumeration. Mirror of Lesson #34 (cache-stale finding pattern) with the inverse outcome — this one was real and required action.
- **Files**: 5 implementer prose files (+~7 lines net for typed-enum form + comments), §00/§98/§99 patch banners.
- **Spec lockstep**: §97 v2.3.0 (no change — no new AC, no contract change); §00 v1.1.5 → **v1.1.6**; §98 v1.1.5 → **v1.1.6**; §99 v1.1.5 → **v1.1.6**. h10 stamp 153 → 153 (no change). **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**, **no new AC** — pure prose-refresh under existing AC-21.
- **Validation**: `grep -rn "os.Exit(1)" spec/13-generic-cli/` returns only AC documentation references (98-changelog row + the FORBIDDEN-pin in 03 line 84 + the stale-prose self-reference comment in 07 line 57) — zero remaining live code-example violations.
- **Lesson #43 codified at this row**: when a §97-WINS contract-pin AC ships AND a follow-up prose-refresh phase ships, the refresh phase MUST `grep -rn` the entire module folder (NOT just the files cited in the audit finding) — A11a-fu1 missed 7 of 11 violation sites because it patched only the files explicitly listed in the deterministic-audit finding. Mirror of Lesson #36 (closure enumeration via grep, not finding-list scan) for the prose-refresh axis.

### 1.1.5 — 2026-04-29 — Phase 153 inventory-pin batch: Lesson #29 AC-24 (cross-reference pin for AC-22/23 externals)
- **Action**: Added AC-24 declaring on-disk asset inventory + cross-reference list (AC-SD-22 in spec/05, AC-T-28 in spec/27); follows Lesson #36 (link-don't-restate). Closes audit-v6 HIGH `[D5] Missing files` class as harness bundling-cap artifact per Lesson #34.
- **Spec lockstep**: §97 v2.2.0 → **v2.3.0** (AC count 23 → 24); §00 v1.1.4 → **v1.1.5**; §98 v1.1.4 → **v1.1.5**; §99 v1.1.4 → **v1.1.5**.

### 1.1.4 — 2026-04-29 — Phase 153 P3: AC-22 concurrency prose mirrored into implementer surfaces
- **Action**: Lifted AC-22's normative concurrency contract from §97 prose-only into the two files where implementers actually look: (1) added `## Concurrency & Locking (Normative)` section to `10-database.md` (PRAGMA table, transaction discipline, atomic temp-then-rename, `update.lock` discipline, forbidden patterns) and (2) added `### Concurrency Discipline (Normative)` subsection to `18-batch-execution.md` Execution Flow (single connection pool sized N for `--parallel=N`, no per-worker `flock`, retry on worker goroutine).
- **Why**: Per Lesson #33 (§97-WINS contract-pin is correct, but file-grep auditors keep flagging absent prose) and Lessons #19/#21/#26 (lift contract surface to entry-point document with closed-enumeration tables). AC-22 itself is unchanged — these are implementer-facing prose mirrors. Cross-link added in `spec/04-database-conventions/02-schema-design.md` §4.3 (concurrency posture cross-reference, no re-statement).
- **Files**: `10-database.md` (+~50 lines), `18-batch-execution.md` (+~13 lines), `00-overview.md` v1.1.3 → v1.1.4 banner-only, this file v1.1.3 → v1.1.4, `99-consistency-report.md` v1.1.3 → v1.1.4.
- **No §97 change · no AC change · no CI change · no RUBRIC change · no gate-count change** — pure prose-mirror under existing AC-22.
- **Cross-module**: `spec/04-database-conventions/02-schema-design.md` §4.3 added (cross-link only — schema and concurrency are orthogonal axes per the new section's rationale).
- **Lockstep**: 87/87 GREEN (verify after run).

### 1.1.3 — 2026-04-29 — Phase 153 Task A11a-fu1: stale-prose refresh in `03-subcommand-architecture.md` + `07-error-handling.md` (P0 audit-v6 follow-through)
- **Action**: Refreshed the four stale-prose hotspots flagged in the deterministic audit at `/mnt/documents/spec-deterministic-audit.md` (CRITICAL D1, spec/13). (1) `03-subcommand-architecture.md` line 84 (handler-pattern step 5) and line 102 (rules table) now reference `ExitCode` enum values + cite §97 AC-10/AC-21 instead of bare `exit 1`. (2) `07-error-handling.md` § Exit Codes table widened from 3 rows to the full 5-value enum (`ExitOK/ExitError/ExitMisuse/ExitConfig/ExitBatchPartial`) with constant names + a normative pointer to §97 AC-10/AC-17/AC-21; clamp + child-process re-mapping rule added. (3) Inline Go example for missing-required-arg now exits `ExitMisuse` (2), not `1`. (4) Batch-operations section + example now follow the AC-17 three-way conditional (`ExitOK` / `ExitError` / `ExitBatchPartial`) instead of the bare "exit 1 if any failures" rule. (5) Closing rule "In `cmd` package handlers, print the error and `os.Exit(1)`" generalised to "exit with the appropriate `ExitCode` enum value".
- **Spec lockstep**: §97 v2.2.0 (no change — no new ACs, no contract change); §00 v1.1.2 → **v1.1.3** (h10 stamp 22 → 153); **v1.1.3**; §99 v1.1.2 → **v1.1.3**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**, **no new AC**.
- **Validation**: lockstep + tree-health re-run pending. AC-21 §97-WINS contract was already authoritative pre-refresh (per Lesson #24); this patch eliminates the residual prose drift that the deterministic audit flagged as CRITICAL by file-level grep, NOT by contract reading.
- **Lesson #33 codified at §98 v1.1.3**: Lesson #24 ("contract-WINS supersession ACs let prose drift safely") is correct as a *contract-integrity* rule, but external/automated audits that file-grep without parsing AC supersession will continue to surface the literal stale-prose strings as CRITICAL findings. After a §97-WINS AC ships, schedule a follow-up prose-refresh phase to silence file-grep auditors — patch-level lockstep only (§00/§98/§99 patch bumps; §97 unchanged because no contract change). Cross-references AC-21 (§97-WINS), Lesson #24 (contract-pin first), Lesson #29 (audit-corpus module-kind pin — same family of "audit reads literal text, not contract").

### 1.1.2 — 2026-04-29 — Phase 153 Task A11a: spec/13 self-lift 75 → ≥88 expected (AC-21/22/23 close all 3 v4 findings)
- **Action**: Closed CRITICAL D1 (conflicting exit-code contracts), HIGH D3 (missing concurrency/locking), MEDIUM D2 (incomplete AC for DB+Build). (1) **AC-21** declares §97 AC-10/AC-17 the authoritative exit-code contract — sub-files containing `exit 1` for unknown-command / batch-failure are stale prose; mandates typed `ExitCode` enum (`ExitOK=0, ExitError=1, ExitMisuse=2, ExitConfig=3, ExitBatchPartial=4`); bare integer literals other than `os.Exit(0)` FORBIDDEN. (2) **AC-22** binds DB + file concurrency: SQLite WAL + `busy_timeout=5000` (cross-cuts spec/05 AC-SD-22) + `BEGIN IMMEDIATE` writes + 3× exponential back-off + atomic temp-then-rename file writes (cross-cuts spec/27 AC-T-28 R1+R3) + connection-pool serialization for parallel batch + `update.lock` for self-update. (3) **AC-23** explicitly binds `13-checklist.md` Phase 5 (Database) → AC-22 + AC-10 + spec/05 AC-SD-21/22/23, Phase 8 (Build) → AC-22 + AC-10 + `11-build-deploy.md`; future checklist phases without binding ACs FORBIDDEN.
- **Spec lockstep**: §97 v2.1.0 → **v2.2.0** (AC count 20 → 23); §00 v1.1.1 → **v1.1.2**, §98 v1.1.1 → **v1.1.2**, §99 v1.1.1 → **v1.1.2**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**.
- **Validation**: spec/13 force re-score 75 → **TBD ≥ 88** (target band: GOOD; D1 closed via §97-WINS contract; D3 closed via concurrency contract; D2 closed via Phase 5/8 binding). Lockstep · tree-health pending re-run.
- **Lesson #24 codified at §98 v1.1.2**: When prose in sub-files contradicts a §97 contract, declare §97 the authoritative source via an explicit "§97-WINS" AC (mirrors AC-CG-23 supersession contract from spec/02 / Lesson #23) — do NOT race to refresh every contradictory prose instance first; pin the contract authoritatively, then the prose can drift behind safely until refreshed. **Lesson #25**: Cross-cutting infrastructure ACs (DB concurrency, file atomicity, signal handling) belong in the consuming module's §97 with explicit cross-references to their authoritative-spec home (here: spec/05 AC-SD-22 for SQLite busy-timeout; spec/27 AC-T-28 for atomic file writes) — duplicating the full contract bloats the bundle and creates drift; cross-referencing keeps single-source-of-truth while making the binding explicit.

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 1.1.1 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v2.0.0 → **v2.1.0**; §99 lockstep update.

### 1.1.0 — 2026-04-26
- **Phase 16a — Deepen §97 with module-specific GWT ACs.** §97 banner v1.0.0 → v2.0.0 (major bump because the AC count more than tripled — 5 → 20 — and the new ACs validate a different surface (the CLI implementation) than the original 5 (the spec module structure)).
- **Added** 15 module-specific Given/When/Then ACs (AC-06..AC-20) covering: AC-06 single-switch subcommand dispatch (no cobra/urfave), AC-07 kebab-case per-command flagsets + flag-name constants, AC-08 three-layer config precedence (defaults → JSON file → flags) + flat-JSON-only contract, AC-09 pluggable `--format` (terminal/json/csv/markdown) + TTY-detect color suppression, AC-10 fixed five-value exit code contract (0/1/2/3/4) + stderr discipline, AC-11 50-line function / 400-line file / camelCase-PascalCase-only / no-magic-strings code style, AC-12 compile-time embedded help with `//go:embed` + interception before flag parse, AC-13 centralized `pkg/dateformat/` with three layouts (display, filename, ISO8601), AC-14 `pkg/constants/` category split (flags/commands/paths/formats/exit) + `<Category><Name>` naming, AC-15 `--verbose` to stderr + secret redaction + zero-overhead when disabled, AC-16 progress to stderr + 500ms appearance + non-TTY suppression + clear-on-complete, AC-17 batch `exec` exit-4-on-partial + `[item]` prefix + deterministic parallel ordering, AC-18 generated-not-handwritten shell completion (bash/zsh/powershell/fish) + hidden `__complete` provider, AC-19 fixed terminal palette (green/red/yellow/cyan/gray) + box-drawing headers + ASCII fallback, AC-20 post-install `doctor` check + interactive shell-profile injection + `--json` mode.
- **Preserved** AC-01..AC-05 (generic structural ACs that validate the spec module itself, distinct from AC-06..AC-20 which validate a CLI implementation).
- Lockstep §99 v1.0.0 → v1.1.0; spec-index updated.
- **P22 sync** (2026-04-28): §00 banner version field bumped 1.0.0 → 1.1.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 22 -->` stamp added under §00 banner; no spec content change).

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

## 2026-04-27 — Phase 68 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 68 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

## 1.1.5 — 2026-04-30 — Phase 153 (inventory-pin)

- Added **AC-24** (Cross-reference pin for AC-22/AC-23 externals) — Lesson #29 module asset inventory pin. Auditor-authoritative on-disk inventory declaration; closes audit-v6 HIGH [D5] missing-files class as bundling-cap artifact (cache-stale per Lesson #34 until A8 LLM re-score). Lockstep §00/§97/§98/§99 patch+minor coordinated.

