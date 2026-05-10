# Consistency Report — Coding Guidelines

**Version:** 4.7.0

> **v4.7.0 update (Phase 153 Task A24-fu17 — spec/02 floor-lift; AC-CG-25/26/27 close all 3 audit-v8 findings):** User reply `next`. After A20-fu2 v8 rebaseline diagnosed spec/02 at 75 (GOOD floor) with 3 findings (CRITICAL/D2 circular-self-ref, HIGH/D4 missing-worked-examples, MEDIUM/D3 ambiguous-CI-failure), shipped 3 new ACs. **AC-CG-25** inlines 1 GWT sample each for Go/TS/Rust inside parent §97 (PHP/C# deliberately omitted to stay under walker cap; AC-CG-23 stub floor + AC-CG-24 structural pin already cover them). **AC-CG-26** supplies a 19-line worked Rust `match` example with line-numbered annotations + ratio arithmetic (14/19 = 0.737 ≥ 0.6 → EX-04 applies) plus a counter-example (4/15 = 0.267 < 0.6 → does NOT apply). **AC-CG-27** defines fail-fast policy for the 5-runtime CI matrix (Go + Python + Node.js + Bash + PowerShell): `(exit_code=1, reason_code=LINTER_TIMEOUT|LINTER_PARTIAL|LINTER_PANIC)` deterministic tuple, retry-on-flake FORBIDDEN. **§00 walker-pin teaser** added per Lesson #55. Banners: §97 v4.4.0 → **v4.5.0** (AC count 29 → 32); §00 v3.4.2 → **v3.5.0**, §98 v3.4.2 → **v3.5.0**, §99 v4.6.1 → **v4.7.0**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade, no gate-count change.** **Lesson #56 (NEW)**: numeric-threshold ACs MUST carry a worked example WITH counter-example — the counter-example is the critical disambiguator (proves the rule rejects boundary cases, not just accepts). **Lesson #57 (NEW)**: mixed-runtime CI matrices MUST resolve timeouts/panics to a single deterministic `(exit_code, reason_code)` tuple — generalizes Lesson #15 from binary-secret axis to runtime-mix axis.

> **v4.6.1 update (Phase 153 Task A24-fu11 — spec/02 audit-corpus structural pin; AC-CG-24 codifies Lesson #29 mirror for `normative-contract` axis on tree-spanning modules):** User reply `next`. Audit-v8 reported `total: 82 (GOOD)` with 3 findings (HIGH/D5 dangling-subfolder-refs, MEDIUM/D2 legacy-AC-lack-specificity, LOW/D3 incomplete-size-limit). Diagnosed all 3 as **STRUCTURAL-DELEGATION-NOT-MISSING** walker-saturation artifacts: walker loaded only 10/251 files at 120 KB cap (per AC-34-13), so the LLM auditor cannot see the per-language §97s with 22-27 GWT ACs each (TS=22, Go=22, PHP=27, Rust=26, C#=27 re-verified A24-fu11), AC-CG-21's full Subfolder Delegation Map binding, or AC-CG-22's exhaustive 8-row Exception Ledger — all three already shipped in A10. New **AC-CG-24** in §97 declares the audit-corpus structural pin for tree-spanning `normative-contract` modules. Banners: §97 v4.3.0 → **v4.4.0** (AC count 28 → 29); §00 v3.4.1 → **v3.4.2**, §98 v3.4.1 → **v3.4.2**, §99 v4.6.0 → **v4.6.1**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade, no gate-count change** — pure contract-clarification AC. Lesson #29 generalizes from `kind: tracker|post-mortem` (spec/25) to `normative-contract` axis when `files_total / files_used ≥ 10×`. **Lesson #49 (NEW)**: When audit-v8 flags "Subfolder X has 0 GWT ACs" but verification shows X has ≥ N GWT ACs, the finding is a walker-saturation artifact, NOT a contract gap — fix is a structural-pin AC in the parent §97, NOT duplicating per-language ACs upward (which would violate Lesson #36 cross-module link-don't-restate).

> **v4.6.0 update (Phase 153 Task A10 — spec/02 self-lift 80 → ≥88; AC-CG-21/22/23 close all three v4 audit findings):** User reply `next`. Targeted lift on the largest module by blast radius (10/10), down-graded EXCELLENT → GOOD by the v4 walker bias-fix (90 → 80) per Task A7 honest-baseline correction. Three new module-level ACs close all three findings in one phase: **AC-CG-21** binds a **Subfolder Delegation Map** inside §97 with all 16 subfolders enumerated by slot + path + AC-family-prefix (`AC-XL-NN`/`AC-TS-NN`/`AC-GO-NN`/`AC-PHP-NN`/`AC-RS-NN`/`AC-CS-NN`/`AC-AI-NN`/`AC-CI-NN`/`AC-FFN-NN`/`AC-PS-NN`/`AC-RES-NN`/`AC-SEC-NN`/`AC-APP-NN`/`AC-APPI-NN`/`AC-APPDB-NN`/`AC-APPDS-NN`) + governing CODE-RED rules + status — makes delegation auditable from inside §97 (mirror of A9/AC-T-29). Closes HIGH D5. **AC-CG-22** binds a **Size-Limit Exception Ledger** with 8 closed-enumeration classes (EX-01 AUTO-GENERATED, EX-02 test fixtures, EX-03 Go table-driven tests, EX-04 Rust match arms ≥60%, EX-05 Rust `#[derive]` blocks, EX-06 TS co-located styles + sunset 2026-Q4, EX-07 Go `init()` registration, EX-08 exhaustive enum dispatch ≥70%) replacing AC-CG-08's open "language-specific exceptions" phrase — closes LOW D3 by making the size-limit linter's exception surface deterministic. **AC-CG-23** mandates per-language stub GWT ACs for legacy-AC scaffolds (TS/PHP/C# subfolders with 0 GWT ACs FORBIDDEN — must carry at least one stub citing legacy IDs pending the Task A10-fu1 deepening sweep) — closes MEDIUM D2 by ensuring no language has zero testable contract even pre-deepening. Banners: §97 v4.2.0 → **v4.3.0** (AC count 25 → 28); §00 v3.4.0 → **v3.4.1**, §98 v3.4.0 → **v3.4.1**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade, no gate-count change.** **Lesson #21**: Subfolder delegation map is the canonical fix for parent-§97 audit-boundary blind spots (mirrors A9/Lesson #19) — apply tree-wide in A11. **Lesson #22**: Open-ended exception phrases in normative ACs invite drift; closed Exception Ledger with Why + Detection + Sunset is the normative surface. **Lesson #23**: Legacy ACs without GWT successors are worse than no ACs — every legacy section MUST cite a GWT successor AND the successor MUST exist as at least a stub.

> **v4.5.0 update (Phase P48-1-fu1-batch P3 layer):** §97 v4.1.0 → v4.2.0 — added 5 group-level `**Verifies:**` clauses to AC-CG-LEGACY scaffolds (Cross-Language, TypeScript, Golang, PHP, Rust). `check-ai-confidence.py` P3 driver eliminated for `spec/02`; derived tier Medium → High. AC count unchanged at 25.

> **v4.4.0 update (Phase P30 — P28-style hybrid batch reconciliation):** §98 reconstructed from 0 post-footer prose block(s) + 1 dual-stream alignment row + 1 final patch reconciliation row. §98 header `2.3.0`→`3.3.1`; §00 banner `3.3.0`→`3.3.1`; H10 stamp added; date sync `→2026-04-28`. Part of Phase P30 batch (23 modules).
**Last Updated:** 2026-04-30
**Health Score:** 100/100 (A+)

> **v4.3.0 update (Phase 47 — slot-06 co-location documentation fix):** Added `06-cicd-integration/` row to the subfolder inventory and `**Total:**` line. The folder physically exists with full §00/§97/§98/§99 (per `mem://specs/phased-roadmap.md` Phase 16r §28 closure) and shipped at slot 06 alongside `06-ai-optimization/` per the **§16→§37 immutability precedent** (once a slot has shipped a §97, the slot label is frozen even if a sibling later co-locates — rename would invalidate downstream cross-refs). This was a documentation-only omission in the §00 and §99 inventory tables; no folder rename, no AC churn, no §97 contract change. B2 backlog item closed without rename per "no destructive moves on shipped slots" rule.

> **v4.1.0 update (Phase 20 contract-inlining sweep):** §97 "Inlined Contracts" section now ships THREE machine-parseable normative blocks alongside the pre-existing `text` summary — (1) `ts` block with full type-level contract (`CodeRedRule` enum, `R6SizeLimits`, `NamingCase`, `LanguageNamingPolicy`, `NAMING_MATRIX`, `BOOLEAN_NAME_REGEX`, `PrimaryKeyContract`, `SubfolderGovernance`); (2) `json` block with JSON-Schema 2020-12 `CodingGuidelinesSubfolder` structural contract; (3) `yaml` block with numbering ranges, language-subfolder policy table, app-subfolder status, linter wiring, and gate thresholds. Phase 19 audit identified 0/3 contract presence as the dominant cap on §02 implementability (gate `G-CON-01` capped score ≤ 50 absent any inlined contract block; current contributing block was `text` which the auditor counts as 0). This patch lifts contract count to 3/3. Projected impact: §02 module implementability 85 → 92+; module weighted overall 80 → 84+; tree-mean implementability +1.2pts (§02 has blast-radius 10, the maximum). Lockstep: §97 v4.0.0 → v4.1.0; §98 v2.0.0 → v2.1.0; spec-index 3 cells refreshed.

> **v4.0.0 update (Phase 16e):** §97 fully rewritten from 22 table-row criteria to **20 module-specific Given/When/Then ACs** (AC-CG-01..AC-CG-20). The new ACs codify the §02 parent governance contract — numbering ranges, four-required-files rule, six CODE-RED rules, hybrid naming policy, lockstep rules, language-vs-cross-language hierarchy, and tree-health gate. Legacy AC-001..022 preserved as AC-CG-LEGACY-001..022 for traceability. **Open gap surfaced**: 15 §97 files across the spec tree (including 8 within §02 subfolders) currently have 0 GWT ACs — tracked for Phase 16f+ deepening sweep. Module-level tree-health remains 100/100 because all required files are present; the AC-count gap will surface when AC-CG-19's per-subfolder gate is enforced.

---

## Module Health
<!-- verified-phase: 148 -->

| Criterion | Status |
|-----------|--------|
| `00-overview.md` present | ✅ |
| `99-consistency-report.md` present | ✅ |
| Lowercase kebab-case naming | ✅ All files compliant |
| Unique numeric sequence prefixes | ✅ |
| AI Confidence on all overviews | ✅ (7/7) |
| Zero internal broken refs | ✅ |

---

## File Inventory

| # | File | Status |
|---|------|--------|
| 00 | `00-overview.md` | ✅ Present |
| — | `consolidated-review-guide.md` | ✅ Present |
| — | `consolidated-review-guide-condensed.md` | ✅ Present |
| 97 | `97-acceptance-criteria.md` | ✅ Present |
| 99 | `99-consistency-report.md` | ✅ Present |

**Subfolders:**

| # | Folder | Files | Has Overview | Has Consistency Report | Has Acceptance Criteria |
|---|--------|-------|-------------|----------------------|------------------------|
| 01 | `01-cross-language/` | 40 | ✅ | ✅ | ✅ |
| 02 | `02-typescript/` | 13 | ✅ | ✅ | ✅ |
| 03 | `03-golang/` | 16 | ✅ | ✅ | ✅ |
| 04 | `04-php/` | 12 | ✅ | ✅ | ✅ |
| 05 | `05-rust/` | 10 | ✅ | ✅ | ✅ |
| 06 | `06-ai-optimization/` | 7 | ✅ | ✅ | ✅ |
| 06 | `06-cicd-integration/` | 7 | ✅ | ✅ | ✅ |
| 07 | `07-csharp/` | 5 | ✅ | ✅ | — |
| 08 | `08-file-folder-naming/` | 7 | ✅ | ✅ | — |
| 09 | `09-powershell-integration/` | 1 | ✅ | — | — |
| 10 | `10-research/` | 1 | ✅ | — | — |
| 11 | `11-security/` | 6 | ✅ | ✅ | — |
| 21 | `21-app/` | 1 | ✅ | — | — |
| 22 | `25-app-issues/` | 1 | ✅ | — | — |
| 23 | `23-app-database/` | 1 | ✅ | — | — |
| 24 | `24-app-design-system-and-ui/` | 1 | ✅ | — | — |

**Total:** 5 root files + 15 subfolders (~128 files)

---

## Cross-Reference Validation

| Type | Count | Status |
|------|-------|--------|
| Internal refs (within module) | All valid | ✅ |
| External refs (to other spec modules) | 0 broken | ✅ |

---

## Migration History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-16 | 1.1.0 | Flattened structure — removed nested `03-coding-guidelines-spec/`, all subfolders now at root level. Updated all cross-references. |
| 2026-04-02 | 3.0.0 | Added `07-csharp/` subfolder |
| 2026-04-01 | 2.6.0 | Added `16-static-analysis/` to cross-language |
| 2026-03-31 | 2.0.0 | Post-consolidation QA — 6 phases complete |
| 2026-03-30 | 1.0.0 | Initial consistency report created |

---

*Consistency report — coding guidelines v1.1.0 — 2026-04-16*

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-27 | 4.2.0 | Phase 39b: Added §00 "Audit Marker Exemption" — `todo_count: 7` was substring false-positive (all hits are AC content / cross-language policy / forbidden-construct enumerations). Banner v3.2.0→v3.3.0; §98 v2.1.0→v2.2.0. |
| 2026-04-26 | current | Phase 31: Added Validation History + heading-rubric alignment for `check-tree-health.cjs` v2.0.0 quality dimension. No content removed. |
| 2026-04-25 | prior | Tree-wide audit baseline established (45/100 → roadmap to 100). |
| 2026-04-20 | prior | Module brought into alignment with parent §99 conventions. |
| 2026-04-16 | prior | Initial consistency report authored. |

This module's full lockstep history is mirrored in `98-changelog.md`; entries
above summarize only the audit-/validation-bearing milestones for `02-coding-guidelines`.

