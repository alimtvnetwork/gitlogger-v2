# Consistency Report — Spec Toolchain

**Version:** 2.90.4
**Updated:** 2026-05-10 (Phase-5 T-16 — slot 42 `check-error-envelope-uniformity.py` shipped as gate #23, first cross-cutting App-framework gate; closes §27 backlog `error-envelope-uniformity-check`; promotes AC-CAF-02 from conditional 20 to un-conditional 20)

> **v2.90.4 update (Phase-5 T-16 — slot 42 + gate #23 close §27 backlog `error-envelope-uniformity-check` and lock AC-CAF-02 at un-conditional 20):** Slot 42 `check-error-envelope-uniformity.py` shipped (slot doc + workflow step "§22+§23+§24 ErrorEnvelope uniformity gate"). 5-clause uniformity scan: schema-pin (single top-level `ErrorEnvelope` in §22 `17-openapi.yaml` line 219 only); DB-mirror (every §23 R-3 WE-1..WE-N response embeds full envelope field set); UI-mirror (§24 AC-ADS-15 row + `<AppErrorState/>` cite `Error.Message` + `TraceId|RequestId`); code-prefix discipline (every `Error.Code` matches `^(GL\|ADB\|ADS\|CAF)-[A-Z0-9-]+$` AND is §97-AC-declared in at least one of §22/§23/§24); no-restate (no inlined YAML schema redefine per Lesson #36). 5-fixture in-memory `--self-test`: F-1 (complete-uniform) passes; F-2 (missing `RequestId`) fails clause-2; F-3 (missing `TraceId`) fails clause-3; F-4 (foreign `DB-FOREIGN-XYZ` code prefix) fails clause-4; F-5 (inlined schema redefine in §23) fails clause-5. R5 vacuously-passing clause enforced — zero-match scan exits `1` not `0`. **First §27 gate spanning three in-scope folders simultaneously (§22 + §23 + §24)** in a single PR-blocking assertion. Bindings: AC-CAF-02 (T-12) self-enforcing mechanism converts from paper-only with 3-turn decay clause to load-proven (gate #23 IS the cited mechanism). AC-ADS-15 namespace-extension gains its first machine-checked sibling. §22 AC-30 schema-pin mechanism upgrades from "implementation pending" to "load-proven". Complementary to gate #17 `error-envelope-shape-check` (runtime status-code → envelope-code mapping); gate #23 covers static contract surface gate #17 cannot reach. Lockstep: §00 v4.7.0 → **v4.8.0** (gate enumeration row #23 + slot delegation map row 42); §98 v4.9.0 → **v4.10.0** (release row); this §99 v2.90.3 → **v2.90.4**. **No CI / RUBRIC / AC-31-31 / §97 surface change** beyond gate-count delta (22 → 23). §27 backlog: 14 deferred entries remain (was 15): `dialect-precedence-banner-present`, `boolean-uniformity-primary-lane-check`, `no-sql-ddl-in-ui-folder-check`, `no-ci-yaml-in-issues-folder-check`, `no-toolchain-enum-in-issues-folder-check`, `no-out-of-scope-spec-folder-link-in-locked-7`, `rest-pascalcase-parity-check`, `rest-boolean-parity-check`, `ui-component-binding-matrix-check`, `seedable-config-row-present-check`, `appshell-route-matrix-check`, `seed-id-explicit-locked-form-check`, `audit-quoted-evidence-marker-check` (T-12), `ac-section-orphan-header-check` (T-13), `ac-prefix-contract-check` (T-14). Closed this turn: `error-envelope-uniformity-check` (T-12 → T-16).

> **v2.90.3 update (Phase-5 T-15 — slot 39 + gate #22 close §27 backlog `applink-xor-check-clause-present`):** Slot 39 `check-applink-xor-clause.py` shipped (slot doc + workflow step "§23 AppLink XOR clause gate"). 4-fixture in-memory `--self-test`: F-1 (complete-XOR + correct seed + both partial-indexes) passes; F-2 (XOR weakened to `AND`) fails clause-1; F-3 (seed `INSERT` omits explicit IDs) fails clause-3 (T-10/WE-2); F-4 (`IX_AppLink_TargetRepoId` `WHERE` stripped) fails clause-4. R5 vacuously-passing clause enforced — zero-match scan exits `1` not `0`. Bindings: §23 §00 WE-2/WE-3/WE-4 worked-examples block (T-11) becomes load-proven; AC-CAF-01 (T-12) gains partial §23-side `IsActive` coverage. Lockstep: §00 v4.6.0 → **v4.7.0** (gate enumeration row #22 + slot delegation map row 39); §98 v4.8.0 → **v4.9.0** (release row); this §99 v2.90.2 → **v2.90.3**. **No CI / RUBRIC / AC-31-31 / §97 surface change** beyond the gate-count delta (21 → 22). §27 backlog now: 15 deferred entries remain (was 16): `dialect-precedence-banner-present`, `boolean-uniformity-primary-lane-check`, `no-sql-ddl-in-ui-folder-check`, `no-ci-yaml-in-issues-folder-check`, `no-toolchain-enum-in-issues-folder-check`, `no-out-of-scope-spec-folder-link-in-locked-7`, `rest-pascalcase-parity-check`, `rest-boolean-parity-check`, `ui-component-binding-matrix-check`, `seedable-config-row-present-check`, `appshell-route-matrix-check`, `seed-id-explicit-locked-form-check`, `error-envelope-uniformity-check`, `audit-quoted-evidence-marker-check`, `ac-section-orphan-header-check` (T-13), `ac-prefix-contract-check` (T-14). Closed this turn: `applink-xor-check-clause-present` (T-15).

---

> **v2.90.0 update (Phase 158 — slot 34 AC-34-19 anchor-pair AC-boundary splitter, Lesson #87):** Replaced `pack_chunks()` inner last-resort branch (anchor pair > MAX_BYTES → `[:max_bytes]` truncation) with AC-boundary splitter: identifies LARGER anchor file, splits at `^### AC-` heading boundaries via `re.split(r"(?m)(?=^### AC-)", big_raw)`, greedy-packs slices under `slice_budget = max_bytes - small_size - CHUNK_OVERHEAD`, pairs each slice with smaller anchor as context (or fallback to solo slices when smaller anchor would consume >3/4 of cap). Live verification spec/22-git-logs-v2: chunk count 3 → 4; chunks 1+2 each carry §00+§97-slice (124 KB + 113 KB); full §97 (188 KB) now visible to auditor (was: 73 KB silently dropped including AC-80 sibling delegation map landed Phase 154). Slot 34 §97 grew **AC-34-19** `[high]`. Lockstep: slot 34 v1.10.1 → **v1.11.0**; §00 v2.94.1 → **v2.95.0**; §98 v2.94.1 → **v2.95.0**; this §99 v2.89.3 → **v2.90.0**; h10 stamp 155 → 158. All 16 AC-34-* + 21 AC-34-18 self-tests PASS unchanged. **No CI / RUBRIC / AC-31-31 / gate-count change.** Lesson #87 codified inside AC-34-19: when an LLM-walker last-resort branch is labelled "extreme" but a real spec module hits it, treat the label as a TODO marker not a permanent ceiling — Lesson #74 saturation triage refined per sub-class (anchor-pair-overflow now engineering-soluble; sub-module recursion for spec/02/03/14/25 OVERFLOW path remains deferred per AC-34-18(f) non-goal). Live LLM re-score deferred per Lesson #20 (gateway HTTP 402 at landing — Lesson #86 oscillation). Expected spec/22 lift: 76 → ≥85 once gateway unblocks.

> **v2.89.3 update (Phase J3-fu — slot 29 `check-version-parity.py` blockquote release shape, Lesson #28-fu):** Widened slot 29's release-shape regex set to recognise blockquote release prose `> **vX.Y.Z update (Phase … — …):** …` as a first-class shape alongside `RELEASE_HEADING_RE` and `RELEASE_ROW_RE`. `latest_release()` now unions all three candidate sets per line and returns SemVer-MAX. Closes a silent-skip class observed in spec/22 where archive prune (Phase fu29) moved all heading + table-row releases out of `98-changelog.md`, leaving only the most recent v3.22.0 visible as a blockquote update — prior comparator scanned the file as `skipped(no-release)` even though §00 banner correctly tracked the shipped release. Slot 29 §97 grew **AC-29-16** with the spec/22 worked example; AC count 15 → 16. Self-test `test-check-version-parity.sh` grew **T15** (synthetic blockquote-only release sandbox; asserts `matches=1, mismatches=0` AND not skipped); 14/14 → **15/15** ✅. Live tree gate unchanged: 77/77 matches, 0 mismatches, 74 stamped, 0 stamped_failed. Lesson #28-fu codified inside AC-29-16 — extends Lesson #28 (Phase 153 #35 comparator-semantics axis) to the regex-coverage axis: when the parity gate flags drift OR silently skips a known-shipped release, inspect both (a) COMPARATOR semantics AND (b) SCANNED-shape regex set BEFORE patching data. Lockstep: slot 29 inline `## Changelog` v1.3.0 → **v1.4.0** (minor — new AC + new self-test assertion); §00 v2.94.0 → **v2.94.1** (patch — banner + h10 stamp 154 → 155); §98 v2.94.0 → **v2.94.1** (this row mirrors slot-only patch); this §99 v2.89.2 → **v2.89.3** (audit row + freshness stamp). **No CI / RUBRIC / AC-31-31 / gate-count change.** Slot-content edit only; module-level §97 surface unchanged.

> **v2.89.2 update (Phase J9 — AC-T-35 slot-35 binding, Lesson #19 + #21 + #36 + #65):** Closed Phase J8's highest-leverage sibling-binding candidate. Added `[critical]` AC-T-35 to §97 binding `35-audit-bundle-budget.md` (kind: auditor) with full GWT covering: cap-source binding to slot 34 `MAX_BYTES` (Lesson #36 link-don't-restate — NOT a duplicated 140 KB literal); deterministic zero-network classification into `{UNDER, NEAR, OVER}` per AC-35-02; `--strict` graduating CI gate per AC-35-03; advisory default per AC-35-04; mechanical lock under `linter-scripts/test/test-audit-bundle-budget.sh` (10 assertions, snapshot-restore-safe per Lesson #31). Updated Slot Delegation Map row 35 (was `_(reserved)_` → bound to `linter-scripts/audit-bundle-budget.py` with `AC-35-*` family + AC-T-14/AC-T-30 governance) + AC Family Prefix Index (`AC-35-*` → `35-audit-bundle-budget.md`, ≥5 GWT). Appended 5 `[[trace]]` entries to `linter-scripts/trace-map.toml` covering AC-35-01..05. Slot file existed since Phase 153 Task A24-fu32 with on-disk ACs but had ZERO §97 binding, ZERO delegation-map row, ZERO family-prefix-index entry, ZERO trace-map presence — textbook three-surface Lesson #19 audit-boundary < verification-boundary gap. §97 v2.16.0 → **v2.17.0** (minor — new AC, count 32 → 33); §00 v2.93.1 → v2.93.2; §98 v2.93.1 → v2.94.0; this §99 v2.89.1 → v2.89.2; trace-map 96 → 101 `[[trace]]` blocks; h10 stamp 153 → 154; freshness stamp 147 → 154. **No CI / RUBRIC / gate-count change.** LLM re-score deferred per Lesson #20.

> **v2.87.1 update (Phase 153 Task R2-followup — AC-34-18 mechanical lock extended 3/8 → 8/8 affected modules):** Extended `linter-scripts/test/test-audit-ai-tier1b-promotion.sh` from 6 → **21 assertions** (T1-T8): added T4=spec/06 (FITS, 8 nested T1B), T5=spec/10 (FITS, 4), T6=spec/12 (FITS, 12 — natural 12-slot ceiling: 4 root T1 + 8 nested T1B = first 12 entries, remaining 4 fall to T2 by alpha), T7=spec/18 (FITS, 4), T8=spec/26 (FITS, 4). Reusable `fits_test()` helper added. Self-test 21/21 PASS. Per L21 parity-AC mechanical-lock rule (mirror of P49 AC-T-13 graduation): a contract-AC citing N affected modules MUST lock across ALL N — pre-R2-followup AC-34-18 only locked 3/8 sentinels. Slot 34 §00 v1.10.0 → **v1.10.1** (patch — test extension, no AC, no code); §00/§98 v2.91.0 → **v2.91.1**; this §99 v2.87.0 → **v2.87.1**. **No CI / RUBRIC / gate-count / new AC.** Discovery codified inside test header doc-block: spec/12's 12-slot ceiling (4 root T1 + 8 nested T1B fills priority-1, remaining 4 nested T1B fall to T2 alpha) is correct contract behavior, not regression. All 5 strict gates expected GREEN. Memo: `phase-153-task-R2-followup-tier1b-mechanical-lock.md`.


> **v2.87.0 update (Phase 153 Task A8-prep / R2 — AC-34-18 bounded tier-1B promotion):** Patched `linter-scripts/audit-ai-implementability.py` `load_module_bundle()` to lift nested `{00,97,98,99}-*.md` contract files to tier-1 priority alongside root contract files, BUT only when combined T1+T1B ≤ MAX_BYTES (140 KB). Tree-wide probe found 10 modules with nested contract files — 6 FITS path (spec/05/06/10/12/18/26 get full clean lift), 4 OVERFLOW-fallback (spec/02/03/14/25 retain current behavior — no regression). New self-test `test-audit-ai-tier1b-promotion.sh` (6/6 PASS) codifies bimodal contract. AC-34-18 `[high]` added to slot 34 §97 (count 17 → 18). Live LLM re-score deferred per Lesson #20 (gateway HTTP 402 on `--force` despite env var set — Lesson #86 oscillation reconfirmed). Sub-module recursion for OVERFLOW giants deferred indefinitely per Lesson #79 (saturation triage: spec/02 already 90/EXC, spec/03 already 87/GOOD via current flat walker). Lockstep: slot 34 §00 v1.9.0 → **v1.10.0** (minor — new AC); §00/§98 v2.90.3 → **v2.91.0**; this §99 v2.86.3 → **v2.87.0**. **No CI / RUBRIC / gate-count change.** All 5 strict gates expected GREEN. NEW Lesson #91 codified at §98 row: Lesson #17 dry-run probe BEFORE walker tier-1 promotion patches — bimodal FITS/OVERFLOW distribution is the design driver for "bounded promotion + graceful fallback" vs "blind mass promotion" (which would have bloated spec/02 from 98 KB to 783 KB).

> **v2.86.3 update (Phase 153 Task N6 — Lesson #82 mechanical lock):** `audit-ai-implementability.py` `main()` now emits `Lesson #82 advisory — pre-chunked-walker cache (chunked_path falsy)` for every sub-90 module whose on-disk cache lacks `chunked_path: True`. Gateway-402 immune. Pure stdout, no exit-code change. 6 modules trigger at landing. Slot 34 §00 v1.8.0 → v1.9.0; §00/§98 v2.90.2 → v2.90.3; this §99 v2.86.2 → v2.86.3.


> **v2.86.0 update (Phase 153 Task A18-impl-1 — AC-34-15 chunked re-scoring opt-in):** Implemented `pack_chunks()` + `merge_chunk_scores()` in `linter-scripts/audit-ai-implementability.py` (~170 LoC) behind `--chunked` (opt-in path) and `--chunk-stats` (no-network telemetry) flags. AC-34-15 `[high]` codifies: parity invariant on ≤MAX_BYTES modules (1 `FULL`-tier chunk byte-identical to `load_module_bundle()` output), T1 re-anchor invariant on multi-chunk slices (every chunk carries `{00,97,98,99}` prefix), tier-weighted merge `{T1: 1.00, T2: 0.85, T3: 0.60}` with `(severity, dimension, first_120_chars)` finding dedupe. Self-test 9 → **14 assertions** (all PASS); real-tree chunk-stats: 7 `FULL`-tier modules + 16 multi-chunk + 13 oversize-chunk slots reserved for A18-impl-2 single-file splitter. Default behaviour unchanged — gateway-independent ship per Lesson #20/#38; A18-impl-2 + A18-rebaseline gated on next gateway-on session. Lockstep: slot 34 §00 v1.5.0 → **v1.6.0**; §97 v2.12.0 → **v2.13.0**; §00 v2.89.0 → **v2.90.0**; §98 v2.89.0 → **v2.90.0**; this file v2.85.3 → **v2.86.0**. **No CI / RUBRIC / gate-count change.** All 5 strict gates expected GREEN.
> **v2.85.0 update (Phase 153 Task A18-fu2 — slot 34 AC-34-14 codifies 140 KB cap + dynamic truncation marker):** Added AC-34-14 `[critical]` to slot 34 §00 (v1.4.0 → v1.5.0) pinning (a) `MAX_BYTES = 140_000`, (b) dynamic `{MAX_BYTES//1024}KB` truncation-marker interpolation (no hard-coded literal byte counts — closes Lesson #77 LLM-fabrication class), (c) source-line comment cites both AC-34-13 + AC-34-14, (d) any future raise above 140 KB requires a fresh live-probe under canonical UA. AC-34-13 marked superseded (retained as historical contract). Slot Delegation Map row + AC Family Prefix Index updated to `AC-34-09..14` / count `≥14`. Closes spec-vs-code drift where `audit-ai-implementability.py:45` already cited the missing AC. **No script behaviour change** — pins existing line-45 + line-213 implementation. Lockstep: §00 v2.87.0 → **v2.88.0** (banner only); §97 v2.9.0 → **v2.10.0** (AC count 32 → 33 via slot internal addition + map/index updates); §98 v2.87.0 → **v2.88.0** (this row); this file v2.84.0 → **v2.85.0**. All 5 strict gates expected GREEN. LLM re-score for spec/27 deferred per Lesson #20 (gateway HTTP 402 active).
> **Validation-history archive (Phase 153 Task A24-fu35):** Historical update blocks v2.0.0 → v2.81.0 (89 entries, ~131 KB) moved to [`_archive/99-validation-history-pre-v2.83.0.md`](./_archive/99-validation-history-pre-v2.83.0.md) to restore AI-implementability walker tier-1 visibility (§99 was 141 KB → walker `files_used: 3/52`, spec/27 score regressed 93→86). Active §99 retains the 3 most-recent operational blocks below + all structural sections (File Inventory / Code-Artifact Bijection / Retired Slots / Open Gaps / Validation History table). Future Validation-History blocks append here; when this file again exceeds ~50 KB, open a new archive (e.g. `_archive/99-validation-history-v2.83-onwards.md`) per the spec/07 §98 archive precedent (Phase A24-fu31).

> **v2.82.0 update (Phase 153 Task A24-fu32 — slot 35 `audit-bundle-budget.py` productionised):** Productionised the ephemeral fu27 walker-bundle-budget script as permanent §27 slot 35. Spec doc v1.0.0 (5 ACs); self-test 10/10 PASS; inventory parity 41/41. Anti-drift contract: `MAX_BYTES` read from slot 34 source at runtime per Lesson #36. Current baseline: 4 OVER (post-fu31 deficits 5.5–148 KB, scoring 85-93 in v9), 6 AT_CEILING, 13 CLEAR. Default advisory; `--strict` exits 1 on OVER. CI wiring deferred to graduation phase when OVER count = 0. **NEW Lesson #68 codified at §98 v2.85.0 row**: ephemeral audit scripts driving multi-phase sweeps MUST be productionised under `linter-scripts/` immediately on sweep closure — temporary tools become institutional debt the moment their lesson ships. Lockstep: §00 v2.84.0 → **v2.85.0**; §98 v2.84.0 → **v2.85.0**; this file v2.81.0 → **v2.82.0**. Slot 34 untouched. All 5 strict gates GREEN.
> **v2.81.0 update (Phase 153 Task A20-fu4 — full-tree v9 rebaseline post OVER-class sweep):** Ran `audit-ai-implementability.py --force` tree-wide (gateway live per Lesson #38). **Tree mean 88.04 → 90.52 / 100 (+2.48) — first crossing into EXCELLENT band.** EXCELLENT count 9 → 15 (+6); GOOD 14 → 8; zero NEEDS_WORK; zero BLOCKING. Top movers: spec/17 +14, spec/04 +10, spec/27 +10, spec/07 +9, spec/22 +7, spec/13 +4, spec/14 +3. **OVER-class sweep validated empirically**: cumulative +28 score points across the 4 modules closed in fu28-fu31 (spec/27/22/01/07). Lesson #65 (structural surgery > pure-promotion) and Lesson #16 (walker tier-1 fix) both confirmed at LLM scoring level. **NEW Lesson #67 codified at §98 v2.84.0 row**: batch the full-tree rebaseline to the natural sweep boundary (cumulative cache snapshot, no HTTP 402 churn, surfaces band-threshold crossings). Lockstep: §00 v2.83.0 → **v2.84.0**; §98 v2.83.0 → **v2.84.0**; this file v2.80.0 → **v2.81.0**. §97 untouched. All 5 strict gates GREEN. Report: `/mnt/documents/spec-ai-implementability-audit-v9.md`.
> **v2.79.0 update (Phase 153 Task A24-fu22 — spec/27 §00 walker-pin promotion, Lesson #61 fourth instance / pure-promotion second instance):** Promoted pre-existing AC-T-27/28/29/30/31/32 (shipped A9 + A24-fu6) into §00 walker-pin teaser (Lesson #55) — 6-row table between Scope line and `## Purpose`. Walker (3/50 files = highest walker-saturation observed at 6%) now sees all 6 structural anchors in first ~2 KB. Audit-v9 cache findings (CRITICAL D5 + HIGH D2 + MEDIUM D3) were ALREADY closed in A24-fu6 by AC-T-30/31/32 — cache pre-A24-fu6 stale (Lesson #34). LLM re-score deferred per Lesson #20 (gateway HTTP 402; Lesson #38 check ran). **Lesson #63 codified at §98 v2.82.0 row**: cache-stale-finding + pre-existing closing AC + high walker-saturation → §00 walker-pin promotion is the canonical lightest-touch remediation. Lockstep: §00 v2.81.1 → **v2.82.0** (minor — new normative walker-pin block); §98 v2.81.1 → **v2.82.0**; §99 v2.78.1 → **v2.79.0**. §97 NOT bumped. All 5 strict gates GREEN expected.

## File Inventory
<!-- verified-phase: 154 -->

| File | Present | Notes |
|------|---------|-------|
| 00-overview.md | ✅ | Inventory + numbering convention (v1.0.0) |
| 01-check-spec-cross-links.md | ✅ | Validator |
| 02-check-spec-folder-refs.md | ✅ | Validator |
| 03-check-forbidden-strings.md | ✅ | Validator |
| 04-check-forbidden-spec-paths.md | ✅ | Validator |
| 05-check-tree-health.md | ✅ | Validator (gate) |
| 06-check-root-readme.md | ✅ | Validator |
| 07-check-readme-canonicals.md | ✅ | Validator |
| 08-check-readme-install-section.md | ✅ | Validator |
| 09-check-memory-mirror-drift.md | ✅ | Validator |
| 10-generate-spec-index.md | ✅ | Generator |
| 11-generate-dashboard-data.md | ✅ | Generator |
| 12-suggest-spec-cross-link-fixes.md | ✅ | Generator (advisory + `--apply`) |
| 13-generate-gwt-acceptance.md | ✅ | Generator (AI-driven) |
| 14-generate-trace-map.md | ✅ | Generator (Spec ↔ Code trace map) |
| 15-generate-fix-checklist.md | ✅ | Generator (per-module fix checklist) |
| 16-generate-gate-report.md | ✅ | Generator (hard-gate cause report) |
| 20-fill-missing-acceptance-criteria.md | ✅ | Filler |
| 21-fill-missing-changelogs.md | ✅ | Filler |
| 22-fill-missing-consistency-reports.md | ✅ | Filler |
| 23-scaffold-spec-module.md | ✅ | Scaffolder (Phase 37) |
| 24-check-lockstep.md | ✅ | Validator (Phase 40 lockstep gate) |
| 30-audit-spec-vs-code.md | ✅ | Auditor v1 |
| 31-audit-spec-vs-code-v2.md | ✅ | Auditor v2 |
| 32-check-truncated-prose.md | ✅ | Validator (slot-range note: in 30-39 band; see slot doc) |
| 40-run-sh.md | ✅ | Runner (bash) |
| 41-run-ps1.md | ✅ | Runner (powershell) |
| 50-validate-guidelines-py.md | ✅ | Source validator (Python) |
| 51-validate-guidelines-go.md | ✅ | Source validator (Go) |
| 52-check-axios-version.md | ✅ | Source validator |
| 60-forbidden-strings-toml.md | ✅ | Config |
| 61-spec-cross-links-allowlist.md | ✅ | Config |
| 62-spec-folder-refs-allowlist.md | ✅ | Config |
| 63-readme-cross-links-md.md | ✅ | Config |
| 70-spec-health-yml.md | ✅ | CI workflow (event-driven) |
| 71-spec-monthly-audit-yml.md | ✅ | CI workflow (cadence — Phase 35) |
| 97-acceptance-criteria.md | ✅ | AC-T-01..AC-T-10 |
| 98-changelog.md | ✅ | v1.0.0 |
| 99-consistency-report.md | ✅ | This file |

## Code-Artifact Bijection

| Code artifact | Spec section | Status |
|---------------|--------------|--------|
| `linter-scripts/check-spec-cross-links.py` | [01](./01-check-spec-cross-links.md) | ✅ |
| `linter-scripts/check-spec-folder-refs.py` | [02](./02-check-spec-folder-refs.md) | ✅ |
| `linter-scripts/check-forbidden-strings.py` | [03](./03-check-forbidden-strings.md) | ✅ |
| `linter-scripts/check-forbidden-spec-paths.sh` | [04](./04-check-forbidden-spec-paths.md) | ✅ |
| `linter-scripts/check-tree-health.cjs` | [05](./05-check-tree-health.md) | ✅ |
| `linter-scripts/check-root-readme.py` | [06](./06-check-root-readme.md) | ✅ |
| `linter-scripts/check-readme-canonicals.py` | [07](./07-check-readme-canonicals.md) | ✅ |
| `linter-scripts/check-readme-install-section.py` | [08](./08-check-readme-install-section.md) | ✅ |
| `linter-scripts/check-memory-mirror-drift.py` | [09](./09-check-memory-mirror-drift.md) | ✅ |
| `linter-scripts/generate-spec-index.cjs` | [10](./10-generate-spec-index.md) | ✅ |
| `linter-scripts/generate-dashboard-data.cjs` | [11](./11-generate-dashboard-data.md) | ✅ |
| `linter-scripts/suggest-spec-cross-link-fixes.py` | [12](./12-suggest-spec-cross-link-fixes.md) | ✅ |
| `linter-scripts/generate-gwt-acceptance.py` | [13](./13-generate-gwt-acceptance.md) | ✅ |
| `linter-scripts/generate-trace-map.py` | [14](./14-generate-trace-map.md) | ✅ |
| `linter-scripts/generate-fix-checklist.py` | [15](./15-generate-fix-checklist.md) | ✅ |
| `linter-scripts/generate-gate-report.py` | [16](./16-generate-gate-report.md) | ✅ |
| `linter-scripts/trace-map.toml` | [14](./14-generate-trace-map.md) | ✅ (data file consumed by §14) |
| `linter-scripts/fill-missing-acceptance-criteria.cjs` | [20](./20-fill-missing-acceptance-criteria.md) | ✅ |
| `linter-scripts/fill-missing-changelogs.cjs` | [21](./21-fill-missing-changelogs.md) | ✅ |
| `linter-scripts/fill-missing-consistency-reports.cjs` | [22](./22-fill-missing-consistency-reports.md) | ✅ |
| `linter-scripts/scaffold-spec-module.cjs` | [23](./23-scaffold-spec-module.md) | ✅ (Phase 37) |
| `linter-scripts/audit-spec-vs-code.py` | [30](./30-audit-spec-vs-code.md) | ✅ |
| `linter-scripts/audit-spec-vs-code-v2.py` | [31](./31-audit-spec-vs-code-v2.md) | ✅ |
| `linter-scripts/check-truncated-prose.py` | [32](./32-check-truncated-prose.md) | ✅ (Phase P47-followup-1) |
| `linter-scripts/run.sh` | [40](./40-run-sh.md) | ✅ |
| `linter-scripts/run.ps1` | [41](./41-run-ps1.md) | ✅ |
| `linter-scripts/validate-guidelines.py` | [50](./50-validate-guidelines-py.md) | ✅ |
| `linter-scripts/validate-guidelines.go` | [51](./51-validate-guidelines-go.md) | ✅ |
| `linter-scripts/check-axios-version.sh` | [52](./52-check-axios-version.md) | ✅ |
| `linter-scripts/forbidden-strings.toml` | [60](./60-forbidden-strings-toml.md) | ✅ |
| `linter-scripts/spec-cross-links.allowlist` | [61](./61-spec-cross-links-allowlist.md) | ✅ |
| `linter-scripts/spec-folder-refs.allowlist` | [62](./62-spec-folder-refs-allowlist.md) | ✅ |
| `linter-scripts/readme-cross-links.md` | [63](./63-readme-cross-links-md.md) | ✅ |
| `.github/workflows/spec-health.yml` | [70](./70-spec-health-yml.md) | ✅ |
| `.github/workflows/spec-monthly-audit.yml` | [71](./71-spec-monthly-audit-yml.md) | ✅ (Phase 35) |

**Bijection: 30/30 ✅** — every executable / configuration artifact has exactly one spec section.

**Subdirectory:** `linter-scripts/installer-templates/` is intentionally not specced here — it is a *content directory* not a *script*. If installer templates ever get their own conventions, add a sibling module (slot 28+) and reference from §00.

## Retired Slots

_None._

## Open Gaps

_None._

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-05-06 | 2.87.0 | Phase 153 Task A8-prep / R2: AC-34-18 — bounded tier-1B promotion. `load_module_bundle()` lifts nested `{00,97,98,99}-*.md` contract files to tier-1 priority when combined T1+T1B ≤ MAX_BYTES (140 KB); falls back to current behavior on overflow. 6 of 10 affected modules get full clean lift (spec/05/06/10/12/18/26 FITS); 4 fall back (spec/02/03/14/25 OVERFLOW). New self-test `test-audit-ai-tier1b-promotion.sh` (6/6 PASS). AC-34-18 `[high]` added (count 17 → 18). Slot 34 §00 v1.9.0 → v1.10.0; §00/§98 v2.90.3 → v2.91.0; this §99 v2.86.3 → v2.87.0. Live LLM re-score deferred per Lesson #20 (gateway HTTP 402). NEW Lesson #91 codified: Lesson #17 dry-run probe BEFORE walker tier-1 promotion patches (bimodal FITS/OVERFLOW distribution is the design driver). |
| 2026-05-05 | 2.86.3 | Phase 153 Task N6: Lesson #82 mechanical lock — `audit-ai-implementability.py` `main()` now emits `Lesson #82 advisory — pre-chunked-walker cache (chunked_path falsy)` for every sub-90 module whose on-disk cache lacks `chunked_path: True`. Gateway-402 immune (scans cache regardless of bundle_sha drift). Pure stdout advisory, no exit-code change, aligned with `--report-only` contract. Codifies `mem://process/phase-153-lessons` Section H. 6 modules trigger at landing (spec/01/04/05/17/18/22). Slot 34 §00 v1.8.0 → v1.9.0; §00/§98 v2.90.2 → v2.90.3; this §99 v2.86.2 → v2.86.3. No CI / RUBRIC / gate-count / AC change. |
| 2026-04-28 | 2.65.0 | Phase P46: retroactive parity-AC graduation survey. Scanned all §27 ACs whose `**Verifies:**` cite ≥2 source files (14 total: 9 already locked, 5 candidates). Triage: 3 graduation candidates surfaced (AC-31-29 memo-retro tri-source; AC-T-11 stderr/stdout convention; AC-T-13 generator determinism cross-script) → P46-followup-1/2/3. 2 false-positives explicitly classified (AC-T-10 trace-map self-citation; AC-T-25 prose-cited test missed by regex). No script/AC change. Banner 2.64.0→2.65.0; §98 v2.67.0→v2.68.0; §00 v2.67.0→v2.68.0. |
| 2026-04-28 | 2.64.0 | Phase P45: AC-11-05 mechanically locked via `linter-scripts/test/test-inline-code-blanking-parity.sh` (8 fixtures, 17 assertions, ~1 s). Folded into existing `Spec cross-link gate` step per H1 workflow-step parity rule (no standalone step, no AC-31-31 cascade, gate count stays 19/19/19). Slot 11 v1.2.0→v1.3.0 (`Verifies:` extended); README inventory 12→13 scripts; trace-map rebaselined +1 code file. Banner 2.63.0→2.64.0; §98 v2.66.0→v2.67.0; §00 v2.66.0→v2.67.0. |
| 2026-04-28 | 2.63.0 | Phase P44: AC-11-05 added to slot 11 (inline-code blanking parity with `check-spec-cross-links.py`); fixed JS dashboard generator's 22-phase `./test-foo.sh` false-positive. No spec score change. |
| 2026-04-27 | 2.5.0 | Phase 39b: Added §00 "Audit Marker Exemption" — `todo_count: 4` was substring false-positive (all hits inside script-spec content defining how the toolchain detects/processes TODOs). Banner v1.1.0→v1.2.0; §98 v2.7.0→v2.8.0. |
| 2026-04-26 | current | Phase 31: Added Validation History + heading-rubric alignment for `check-tree-health.cjs` v2.0.0 quality dimension. No content removed. |
| 2026-04-25 | prior | Tree-wide audit baseline established (45/100 → roadmap to 100). |
| 2026-04-20 | prior | Module brought into alignment with parent §99 conventions. |
| 2026-04-16 | prior | Initial consistency report authored. |

This module's full lockstep history is mirrored in `98-changelog.md`; entries
above summarize only the audit-/validation-bearing milestones for `27-spec-toolchain`.
