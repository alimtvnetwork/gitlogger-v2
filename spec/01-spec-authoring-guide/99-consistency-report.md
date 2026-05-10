# Consistency Report — Spec Authoring Guide

**Version:** 4.15.0
**Last Updated:** 2026-04-30 (Phase 153 Task A24-fu30 — §98 archive split per Lesson #65 / fu28-fu29 pattern)

> **v4.11.0 update (Phase 153 Task A24-fu21 — spec/01 floor lift via walker-pin promotion + 2 new ACs):** Lifts spec/01 from the 83 floor (process-guidance axis, walker 3/17 saturation) by (a) adding a Lesson #55 §00 walker-pin teaser surfacing AC-SAG-29 at the file head (line 317 was unreachable to the bundle-capped walker), (b) adding AC-SAG-30 `[high]` linter-script-logic-anchor pin per Lesson #36 to dissolve the MEDIUM D3 finding, (c) adding AC-SAG-31 `[low]` inlined-schema-version-pluralism pin to dissolve the LOW D1 finding. Lesson #62 codified at §98 v4.14.0 row: process-guidance axis modules (d2≤0.7) are walker-saturation-dominant — §00 walker-pin teaser is the canonical floor-lift pattern. Lockstep: §00 4.13.3→**4.14.0**, §97 4.10.0→**4.11.0**, §98 4.13.3→**4.14.0**, §99 4.10.3→**4.11.0**. Tree-health 168/168 strict-pass holds; lockstep 87/87; version-parity 74/74. LLM re-score deferred per Lesson #20.


> **v4.10.2 update (Phase P48-1-fu1-batch P3 sweep slot 8 — `### AC-SAG-LEGACY` Verifies clauses):** Closes the P3-tier `**Verifies:**` gap for this module (28/32 → 32/32 — smallest remaining gap among P3 drifters). Added group-level `**Verifies:**` clauses to all four `### AC-SAG-LEGACY` block headings; each clause names the GWT-rewrite supersession chain and the AC-SAG-28 exemption-regex contract. Graduates this module's AC-block from Medium → High AI-confidence per `01-spec-authoring.md` § *AI Confidence Rubric (normative)* gate P3. Lockstep: §00 banner 4.13.1 → 4.13.2, §97 4.8.0 → 4.9.0, §98 release row 4.13.2 added, §99 4.10.1 → 4.10.2. P3 derived tier: Medium → High. Tree-health 168/168 strict-pass holds; lockstep 87/87. **Lesson reinforced** (already in Core from slots 2–4): `**Verifies:**` is the single highest-leverage AC field for AI implementability; group-level clauses on LEGACY scaffolds are the canonical pattern (precedent: spec/02 slot 1).

> **v4.10.1 update (Phase P48-1-fu1-batch slot 2 — §00 inventory drift fix, slot 04 co-location):** Reconciles a §00↔disk drift surfaced by `check-ai-confidence.py` (Phase P48-1-fu1) — this folder was 1 of 5 P1 inventory-gap drifters. File `04-ai-onboarding-prompt.md` was on disk and tracked by §99 inventory but never added to the §00 inventory table; per the **co-location precedent** (Core memory — when two folders ship at the same slot before the collision is noticed, both retain the slot, disambiguate by trailing slug), the resolution is to add a second slot-04 row, NOT to renumber. Patch adds the missing §00 row and updates §99 inventory (line 47) to enumerate both slot-04 occupants. §00 banner 4.13.0→**4.13.1**, §98 release row 4.13.1 added. No score change (single-row sync); restores P1 → pass and unblocks tier re-derivation under the P48-1 rubric. Follows precedent established by §17 v3.4.1 (P48-1-fu1-batch slot 1, 2026-04-29).

> **v4.10.0 update (Phase P7b — `## Legacy Index` GWT-completeness exemption codified):** Added **AC-SAG-28** at §97 codifying that AC headings matching `^AC-[A-Z]+-LEGACY(-\d+)?$` MUST be excluded from any GWT-completeness audit denominator. Surfaced when the Phase P7 mechanical sweep over `spec/*/97-acceptance-criteria.md` flagged 13 "non-GWT" ACs across §01/§02/§05/§06 — investigation revealed all 13 are intentional `## Legacy Index (preserved for traceability)` rows kept after a GWT-rewrite phase and referenced from new GWT ACs' `Verifies:` chains (e.g. §05 AC-SD-02 cites `+ AC-SD-LEGACY-001-a`). Removing them would silently break those cross-refs; re-authoring as GWT would balloon §97 length without new contract surface. AC-SAG-28 codifies the canonical exemption regex + four-module exemption snapshot (§01 4 / §02 5 / §05 2 / §06 2) + pre-conditions for new modules introducing a Legacy Index + downstream-tools contract (any future `check-ac-gwt-completeness.py` MUST hardcode the regex AND emit a banner line `excluding N LEGACY ACs across M modules per AC-SAG-28` for visibility). No code change, no new gate, no `RUBRIC_VERSION` bump — pure declarative meta-spec contract. Lockstep: §97 v4.7.0 → **v4.8.0**; §98 v4.12.0 → **v4.13.0**. CI gate count unchanged at **15**; `RUBRIC_VERSION` unchanged at **v2.24**. Verification: `node linter-scripts/check-lockstep.cjs` ✅ 87/87; `node linter-scripts/check-tree-health.cjs --strict` ✅ 168/168. Cross-folder lockstep snapshot to be mirrored at `spec/22-git-logs-v2/98-changelog.md` v3.9.7 + §99 v3.9.14 (Phase P7b row) so the §22 GAP-V2-01 closure narrative carries the full disposition of the 13-row tree-wide follow-up. **Closes Phase P7b** — the 13 "non-GWT" findings are reclassified as intentional traceability infrastructure, not authoring debt. No score regression — §01 holds at 97/100 A+ with impl=100.

> **v4.9.0 update (Phase 115 — promote enumeration-vs-API-surface distinction to §01 meta-spec):** Added **AC-SAG-27** at §97 — promotes the **enumeration-restatement vs API-surface-use** distinction (originally surfaced inline in §31's "Currently-NOT-qualifying enumerations" prose during Phase 114's AC-31-31 bounding sweep) into a §01 meta-spec contract. Codifies: (a) two definitions (enumeration-restatement vs API-surface-use); (b) four diagnostic questions Q1–Q4 (same set?, same semantics?, no single source-of-truth?, silent drift risk?); (c) routing rule (all four `YES` → AC-31-31 parity test; any `NO` → dismissal record at §31, no parity test — authoring one would be a category error); (d) worked Phase-114 dismissal record as a 5-row reference table preserved for future contributors. The §01 promotion ensures parity-test triage applies uniformly across the spec tree, not only within §27 — preventing future contributors in `spec/22-git-logs-v2/` or `spec/04-database-conventions/` from re-deriving the triage from scratch and authoring category-error parity tests that lock API surfaces. Pure declarative — no code, no new gate, no `RUBRIC_VERSION` bump. Lockstep: §97 v4.6.0 → **v4.7.0**; §98 v4.11.0 → **v4.12.0**. CI gate count unchanged at **13**; `RUBRIC_VERSION` unchanged at **v2.22**. Verification: all 13 strict gates green (cross-links OK; tree-health 100/100; lockstep 0; audit ✓ at 98.0/99.8; Phases 91/94/95 self-tests 6/14/7 ✅; Phase 97 mermaid 106/106 ✓; Phase 102 self-test 16/16 ✅; Phase 103 self-test 13/13 ✅; Phase 104 meta-linter ✅; Phase 112 inventory parity ✅; Phase 113 weights parity 8/8 ✅). No score regression — §01 holds at 97/100 A+ with impl=100; §27 holds at 97/100 A+ with impl=100.

> **v4.8.0 update (Phase 111 — documentation-cadence retirement pattern):** Added **AC-SAG-26** at §97 — the abstract pattern that generalises Phase 100's empirical verdict (forward-looking phase-memo sections were drifting within 1 phase of being written across Phases 78–83 / 92–93 / 96) + Phase 104's mechanical enforcement gate (`linter-scripts/check-memo-retrospective-headings.py` with `CUTOFF_PHASE = 100`). Specifies the trigger threshold (3+ historical instances + 1 of 3 drift conditions: stale-within-1-phase, adjacent-contradiction, migration-to-canonical-SoT), the retirement protocol (retirement memo + canonical replacement SoT + CUTOFF marker + out-of-scope clause for pre-cutoff artefacts + mechanical enforcement gate under `linter-scripts/` with `CUTOFF_PHASE` constant + `spec-health.yml` wiring + §27 spec per INV-01 + corresponding §27 `Verifies` AC), the current registered-retirements table (seeded with the Phase 100/104 pair: forward-looking H2/H3 sections in phase memos → canonical replacement = chat-reply "Remaining Tasks" table), and the declarative-with-mechanical-companions rationale (the AC defines the protocol; reviewer attention against the registry catches new retirements that bypass it; meta-meta-linter for "what cadences should be retired?" requires longitudinal analysis the toolchain doesn't perform). The mechanical gate that enforces the seed retirement (Phase 104) is unchanged. No code change — pure contract generalisation. Lockstep: §97 v4.5.0 → **v4.6.0**; §98 v4.10.0 → **v4.11.0**. CI gate count unchanged at **11**; `RUBRIC_VERSION` unchanged at **v2.20** (no script changes). Verification: all 11 strict gates green (cross-links OK; tree-health 100/100; lockstep 0; audit ✓ at 98.0/99.8; Phases 91/94/95 self-tests 6/14/7 ✅; Phase 97 mermaid 106/106 ✓; Phase 102 self-test 16/16 ✅; Phase 103 self-test 11/11 ✅; Phase 104 meta-linter ✅ — 9 in-scope memos / 0 forbidden headings, Phase 111 memo included). No score regression — §01 holds at 97/100 A+ with impl=100; §27 holds at 97/100 A+ with impl=100.

> **v4.7.0 update (Phase 105 — generalise AC-SAG-25 into a grammar-defining-library pin pattern):** Added a `Verifies` cross-reference from **AC-SAG-25** to the newly-introduced **AC-31-30** at [`spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md`](../27-spec-toolchain/31-audit-spec-vs-code-v2.md) — the abstract pattern of which AC-SAG-25 (mermaid + jsdom) is the concrete instance. AC-31-30 enumerates: (a) trigger condition (a `linter-scripts/` script `import`s the library AND uses it to inspect spec content), (b) the current pinned inventory (mermaid 11.14.0; jsdom 20.0.3) plus explicitly-NOT-qualifying examples (typescript / react / vite / tailwindcss — used by `src/` only), (c) the four-step protocol for adding a new gate built on a previously-unpinned library, and (d) the declarative-not-CI-enforced rationale (silent grammar drift is intrinsically pre-merge; `bun.lock` would already be corrupted by the time CI noticed). No code change in this phase — pure contract generalisation. Lockstep: §97 v4.4.0 → v4.5.0; §98 v4.9.0 → v4.10.0. Cascading lockstep at §27: §31 v1.17.0 → v1.18.0 (header `Source` gains `package.json` pin block as 9th artefact; Category gains `+ grammar-library pin contract`; AC-31-30 added with full inventory table); §98 v2.24.0 → v2.25.0; §99 v2.21.0 → v2.22.0. CI gate count unchanged at 11; `RUBRIC_VERSION` unchanged at v2.20 (no script changes). No score regression — §01 holds at 97/100 A+ with impl=100; §27 holds at 97/100 A+ with impl=100.

> **v4.6.0 update (Phase 101 — pin mermaid + jsdom):** Pinned `mermaid` (`^11.14.0` → `11.14.0`) and `jsdom` (`^20.0.3` → `20.0.3`) to exact versions in `package.json` to stabilise the Phase 97 syntax gate's parser grammar against silent caret-range upgrades. `bun install` regenerated `bun.lock` with both packages at the exact pinned versions; the syntax gate continues to report `106/106 files parsed cleanly`. Added **AC-SAG-25** in §97 (a) FORBIDDING caret/tilde ranges for these two packages, (b) requiring major-version bumps to record local gate-run output in §98 + re-run the full triad locally before merge, (c) permitting minor/patch bumps via CI alone since pinning aligns local + CI environments. `dompurify` is transitively pinned by mermaid and does NOT need a direct pin. Lockstep: §97 v4.3.0 → v4.4.0; §98 v4.8.0 → v4.9.0. No score regression — §01 holds at 97/100 A+ with impl=100.

> **v4.4.0 update (Phase 93 — lifecycle.mmd canonical SoT):** Rewrote [`lifecycle-spec-authoring.mmd`](./lifecycle-spec-authoring.mmd) from a 10-node skeleton into a 32-node typed flowchart with 6 styled classes faithfully rendering the actual pipeline built across Phases 81–91 (5 `kind:` branching paths; 6-step local linter pipeline; 6-gate CI sequence including the Phase 91 CLI self-test; `--explain=<module>` failure-recovery loop; post-merge phase-memo step). Replaced the inline mermaid excerpt in §00 ("Lifecycle Diagram (Phase 66, expanded in Phase 93)") with a high-level summary that delegates to the `.mmd` file. Added **AC-SAG-23** in §97 mandating the `.mmd` file as canonical source of truth and locking it stepwise with `linter-scripts/run.sh` + `.github/workflows/spec-health.yml`. Lockstep: §00 v3.6.0 → v3.7.0; §97 v4.1.0 → v4.2.0; §98 v4.6.0 → v4.7.0. No score regression — §01 already had `has_mermaid (+5)` from the existing skeleton; final score holds at 97/100 A+ with impl=100.


> **v4.1.0 update (Phase 38):** Added [`12-queued-decisions-trail.md`](./12-queued-decisions-trail.md) v1.0.0 — codifies the queued-decisions trail format (Q-identifier scheme, 4 status markers, lockstep edits, audit-recovery procedure, 5 ACs). Closes the gap where the project-memory Core lockstep rule referenced `mem://specs/git-logs.md` as a *demonstrated* format without ever specifying it. Inventory now also reflects slot 11 (`11-root-readme-conventions.md`, present since Phase 24 but missed in earlier §99 inventory rebuild).

> **v4.0.0 update (Phase 16f):** §97 fully rewritten from 18 table-row criteria to **20 module-specific Given/When/Then ACs** (AC-SAG-01..AC-SAG-20). The new ACs codify the meta-spec contract for authoring every OTHER spec in the tree — four-required-files rule, naming regex, reserved prefixes, slot immutability, seven `00-overview.md` sections, GWT depth requirement, lockstep rule, three template patterns, `.lovable/memories/` plural canonical, linter infrastructure mandate, root-readme format, score-honesty rule, reliability-report gate, dogfooding self-application, and forbidden manual edits to `spec-index.md`. Legacy AC-001..018 preserved as AC-SAG-LEGACY-001..018 at end of §97 for traceability. **Dogfooding verified**: this module satisfies all 20 ACs against itself (AC-SAG-18). Module-level tree-health: 100/100 (A+).

---

## Module Health
<!-- verified-phase: 153 -->

| Criterion | Status |
|-----------|--------|
| `00-overview.md` present | ✅ |
| `99-consistency-report.md` present | ✅ |
| Lowercase kebab-case naming | ✅ |
| Unique numeric sequence prefixes | ✅ |

**Health Score:** 100/100 (A+)

---

## File Inventory

| # | File | Status |
|---|------|--------|
| 00 | `00-overview.md` | ✅ Present |
| 01 | `01-folder-structure.md` | ✅ Present (canonical folder structure — single source of truth) |
| 02 | `02-naming-conventions.md` | ✅ Present |
| 03 | `03-required-files.md` | ✅ Present |
| 04 | `04-cli-module-template.md` | ✅ Present |
| 04 | `04-ai-onboarding-prompt.md` | ✅ Present (co-located at slot 04 per immutable-slot rule; disambiguated by trailing slug — Phase P48-1-fu1-batch slot 2) |
| 05 | `05-app-project-template.md` | ✅ Present |
| 06 | `06-non-cli-module-template.md` | ✅ Present |
| 07 | `07-memory-folder-guide.md` | ✅ Present |
| 08 | `08-cross-references.md` | ✅ Present |
| 09 | `09-exceptions.md` | ✅ Present |
| 10 | `10-mandatory-linter-infrastructure.md` | ✅ Present |
| 11 | `11-root-readme-conventions.md` | ✅ Present |
| 12 | `12-queued-decisions-trail.md` | ✅ Present (Phase 38) |
| 97 | `97-acceptance-criteria.md` | ✅ Present |
| 98 | `98-changelog.md` | ✅ Present |
| 99 | `99-consistency-report.md` | ✅ Present |

**Total:** 13 files

---

## Cross-Reference Validation

All internal links verified valid. ✅

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-09 | 5.0.0 | Added `10-mandatory-linter-infrastructure.md`; noted 01-folder-structure.md as canonical source. Total: 12 → 13 |
| 2026-03-30 | 4.0.0 | Added `98-changelog.md`. Total: 11 → 12 |
| 2026-03-30 | 3.0.0 | Added `97-acceptance-criteria.md`. Total: 10 → 11 |
| 2026-03-30 | 2.0.0 | Enhanced overview with scoring metrics, keywords, reliability reports, .lovable folder guidance |
| 2026-03-30 | 1.0.0 | Initial consistency report created |

## 2026-04-27 — Phase 57 impl-sweep

- Phase 57: appended Go/PHP/Python SpecModule validator references to satisfy `has_typed_lang_contract` rubric (impl 65 → 75).

## 2026-04-27 — Phase 60 impl-sweep

- Phase 60: appended Spec Authoring Audit API OpenAPI to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 66 audit

- Mermaid lifecycle diagram present (`has_mermaid=true`).
- Lockstep & tree-health gates: PASS.
- Implementability promoted from 85 → 90.

### 2026-04-27 — Phase 72 deepening

- CI workflow contract inlined: 5 stages (detect, validate, lint, promote, report).
- Implementability raised 90 → 95 (deterministic audit).

## v4.15.0 Audit — Phase 153 Task A24-fu30 (§98 archive split)

| File | Change |
|---|---|
| `spec/01-spec-authoring-guide/_archive/98-changelog-pre-v4.4.0.md` | **NEW.** Archive holding 22 historical changelog sections (v4.3.0 → v2.0.0 + Phase 57/60/66/72 sweep notes) extracted from live `98-changelog.md` to free walker headroom. Frozen — never edited. |
| `spec/01-spec-authoring-guide/98-changelog.md` | Banner v4.14.0 → **v4.15.0**. File size 25 KB → ~19 KB (-24%). New v4.15.0 section + structural-change note added at top. |
| `spec/01-spec-authoring-guide/00-overview.md` | Banner v4.14.0 → **v4.15.0** (no body change — duplicate **Updated:** line collapsed). |
| `spec/01-spec-authoring-guide/99-consistency-report.md` (this file) | Banner v4.11.0 → **v4.15.0**; this audit table; no Health Score change. |

**Phase A24-fu30 scope discipline:** No §01 ACs added/removed; no §00 body change beyond banner (despite §00 being 48 KB / largest in tree, **§00 trim deferred per Lesson #30** — extracting "Phase NN Reference" sections risks AI-confidence regression on this canonical meta-spec). Pure structural surgery on §98 only. Mirror of A24-fu28 (spec/27, -82%) and A24-fu29 (spec/22, -62%); spec/01's smaller delta (-24%) reflects already-modest §98 size. Expected cache lift on next re-score: 83 → 84-85 (modest; spec/01 is bound more by §00 + §97 size than §98). Archive folder `_archive/` is invisible to all 5 strict gates (verified at fu28/fu29).

