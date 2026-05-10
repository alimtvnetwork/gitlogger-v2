# Spec Authoring Guide — Changelog Archive: pre-v4.4.0 entries

**Frozen:** 2026-04-30 (Phase 153 Task A24-fu30 — §98 archive split per fu28/fu29 pattern)

> This file holds historical changelog entries extracted from `98-changelog.md` to keep
> the live file under the AI-implementability walker bundle cap. Entries here are **frozen**
> — never edited. See live `98-changelog.md` for v4.4.0 and newer.

---

## [4.3.0] — 2026-04-27 (Phase 48 — §01 implementability lift)

- **Added** §00 — new "Inlined Contract — Spec Module Structure" section at end-of-file with a JSON-Schema 2020-12 `SpecModule` block (~70 lines, `json` fence). Contract codifies `folder_name` regex, required-files set, naming/case/depth rules, overview frontmatter `kind` enum, lockstep version triple, AC ID pattern + GWT format, and cross-reference resolution rules. Plus 3 invariants (INV-AUTH-01..03) and 1 failure mode (FAIL-AUTH-01).
- **Fixed** §09 line 193 — wrapped bare `C-XXX` in inline backticks so the `XXX` token is treated as code by the deterministic auditor's `INLINE_CODE_RX` strip pass (previously contributed `todo_density=1`, the sole drift-LOW finding for §01).
- **Rationale:** Pre-Phase-48 audit showed §01 at impl=40, the *lowest implementability score in the entire tree*, with two findings: (1) HIGH `missing-contract` (impact 8/10) — replaces the v4.1.0 `text` block (auditor counts `text` as 0/3 contracts; a `json` block counts as a real contract); (2) LOW `drift` from a single `XXX` substring inside a table cell (`Legacy C-XXX suggestion names`).
- **Bumped** §00 v3.4.0 → v3.5.0; §99 v4.1.0 → v4.2.0.

---

## [4.2.0] — 2026-04-26 (Phase 38 — queued-decisions trail format formalised)

- **Added** [`12-queued-decisions-trail.md`](./12-queued-decisions-trail.md) v1.0.0 — codifies the queued-decisions trail format that has been used informally in `mem://specs/git-logs.md` since v3.7.x. Defines: file location (`mem://specs/<slug>.md`), Q-identifier monotonicity rule, 4 status markers (`🔄`/`✅`/`❌`/`⏸`), landing-time replacement (not append) rule, lockstep edit set (banner + §98 + §99 + memory), audit-recovery procedure for broken chains, when-applicable matrix (≥3 multi-session decisions OR ≥2 SemVer/week OR user-blocked decision present), worked example from git-logs Q1 + Q3, 5 ACs (AC-12-01..05).
- **Changed** §00 inventory — added slot 12 row; bumped overview banner v3.3.0 → v3.4.0.
- **Rationale:** project memory Core rule says "Spec edits keep these in lockstep: target file banner + §98 changelog row + §99 health/inventory + `mem://specs/git-logs.md` queued-decisions trail" — but until now the trail format itself was undocumented, only demonstrated. Phase 38 closes the gap so any future AI can apply the rule from the spec alone, without having to reverse-engineer it from `mem://specs/git-logs.md`.

---

## [4.1.0] — 2026-04-26 (Phase 26: missing-contract remediation)

- **Added** §00 — inlined normative `SpecModule` JSON schema (≥10 lines, `text` fence) clearing the `missing-contract` G-CON-01 blocker. Module rises out of C-tier.
- **Bumped** §00 v3.2.0 → v3.3.0 (minor; new contract added, no breaking change).

---

## [4.0.0] — 2026-04-26 (Phase 16f: §97 full GWT rewrite)

- **Changed** §97 — full GWT rewrite. Replaced 18 table-row criteria (AC-001..AC-018) with **20 module-specific Given/When/Then ACs** (AC-SAG-01..AC-SAG-20) covering the meta-spec contract for authoring all OTHER specs: four-required-files rule, lowercase kebab-case + numeric-prefix regex, reserved-prefix discipline (00/97/98/99), slot immutability, seven mandatory `00-overview.md` sections, ≥ 5 GWT ACs per `97`, reverse-chronological SemVer-bumped `98`, ≤ 7-day stale rule on `99`, relative + `.md` cross-link rule, four-file lockstep on every spec edit, three template patterns (CLI / app+features / flat), 3+ files → subfolder `00-overview.md`, `.lovable/memories/` (plural) canonical memory folder, mandatory linter infrastructure presence, root readme hero+badges+§9 release-blocker format, AI-Confidence/Ambiguity score honesty rule, Reliability Risk Report mandate for Complex/E2E modules, dogfooding self-application, `bash linter-scripts/run.sh` exit-0 + tree-health ≥ 75 (locked at 100) gate, and forbidden manual edits to `spec-index.md`.
- **Preserved** legacy table-row criteria as AC-SAG-LEGACY-001..018 at end of §97 for traceability.
- **Bumped** §97 v3.2.0 → v4.0.0 (major; AC contract type changed from table-row to GWT). §98 v3.2.0 → v4.0.0. §99 v3.2.0 → v4.0.0.

---

## [2026-03-30] v2.0.0 Compliance Rollout

**Scope:** Project-wide sub-folder `00-overview.md` upgrade  
**Total files upgraded:** 139 sub-folder overviews + 2 new files created  
**Health impact:** 100% compliance with Spec Authoring Guide v2.0.0

### Summary

Upgraded all `00-overview.md` files across the entire spec tree to include the four mandatory sections introduced by the Spec Authoring Guide v2.0.0:

1. **AI Confidence** — metadata field (High for all modules)
2. **Ambiguity** — metadata field (None for all modules)
3. **Keywords** — searchable tags derived from module context
4. **Scoring** — standardized compliance table

### Phases

| Phase | Scope | Files |
|-------|-------|-------|
| 2026-04-26 | minor | Phase 30: Documented rubric v2.0.0 (Required 60% / Recommended 25% / §99 Quality 15%). Replaced Phase-27c drift note with concrete rubric versioning. |
| 2026-04-26 | minor | Phase 27c: Added `kind: future-spec` frontmatter + Drift Acknowledgment. Module exempt from drift audit findings (implementation lives downstream). |
| 1 | Module-level overviews (01–36, 99) | 31 |
| 2 | Module 01 sub-folders | 12 |
| 3 | Module 02 sub-folders | 60 |
| 4 | Module 03 sub-folders | 5 |
| 5 | Modules 04–36, 99, validation-reports | 62 |

### New Files Created

| File | Module |
|------|--------|
| `spec/02-coding-guidelines/05-rust/97-acceptance-criteria.md` | Rust Coding Standards |
| `spec/02-coding-guidelines/05-rust/99-consistency-report.md` | Rust Coding Standards |

### Method

- Phases 1–2: Manual per-file upgrades
- Phases 3–5: Automated Python script with keyword derivation and version bumping
- Post-processing: Keyword cleanup pass to remove path artifacts

### Verification

- Final scan confirmed 0 non-compliant `00-overview.md` files (excluding root dashboard)
- Parent consistency reports updated where applicable

---

## Cross-References

- [Spec Authoring Guide Overview](./00-overview.md)
- [Acceptance Criteria](./97-acceptance-criteria.md)
- [Consistency Report](./99-consistency-report.md)

## 2026-04-27 — Phase 57 impl-sweep

- Phase 57: appended Go/PHP/Python SpecModule validator references to satisfy `has_typed_lang_contract` rubric (impl 65 → 75).

## 2026-04-27 — Phase 60 impl-sweep

- Phase 60: appended Spec Authoring Audit API OpenAPI to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 66 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 66 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

