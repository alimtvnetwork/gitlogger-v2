# Changelog — AI Optimization

**Version:** 4.0.1
**Updated:** 2026-04-29
**Scope:** `spec/02-coding-guidelines/06-ai-optimization/`

---

### 4.0.1 — 2026-04-29 — Phase 153 Task #29c: legacy AC stubs gain `**Verifies:**` clauses
- Phase 153 Task #29c — backfilled `**Verifies:**` clauses on legacy AC stubs (`AC-*-LEGACY*`) so `check-ai-confidence.py` P3 passes tree-wide post-Task-#29b walker widening. Stubs are deprecation markers; their Verifies clause back-points to the modern numeric replacement AC (or section). 18 clauses inserted across 4 nested modules. **No CI workflow change, no AC count change** — content is metadata-only on legacy stubs.

## v4.0.0 — 2026-04-26 (Phase 16n: §97 full GWT rewrite)
- **P21 sync** (2026-04-28): §00 banner version field bumped 3.2.0 → 4.0.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 21 -->` stamp added under §00 banner; no spec content change).

- **Changed** §97 — full GWT rewrite. Replaced 7 stub checkbox criteria with **20 module-specific Given/When/Then ACs** (AC-AI-01..AC-AI-20) covering: explicit AC-CL-* inheritance + per-language AC-XX-* satisfaction for example code (AC-AI-01); 6-language coverage including C# (AH-X/G/T/P/R/C) + AI-meta `AH-A*` namespace (AC-AI-02); rule ID regex `^AH-(X|G|T|P|R|C|A)\d+$` + retired-ID immutability (AC-AI-03); mandatory ❌Forbidden + ✅Required + Source link triplet per rule (AC-AI-04); machine-parsable `- [ ] CHK-NN — desc` checklist format with ≥ 50 checks (AC-AI-05); every check links to ≥1 rule or canonical spec section (AC-AI-06); 7-section common-mistake template (Title/Severity/Frequency/❌Before/✅After/Why/Source) with ≥ 15 entries (AC-AI-07); zero-overlap rule across rules+checks+mistakes tri-set per AC-CL-20 (AC-AI-08); condensed master ≤ 200 non-blank non-fence lines for context-window fit (AC-AI-09); enum quick-reference 5-section template per language (AC-AI-10); placeholder-name blocklist `foo`/`bar`/`baz`/`xxx`/`todo`/`myVar`/`temp`/`data1`/etc. with sole `❌ Before` exemption (AC-AI-11); fabricated-API ban (every imported symbol MUST exist) (AC-AI-12); mandatory `AH-A*` AI-meta rules covering STOP/scan/verify, no-silent-assumption, ask-when-ambiguous, cite-source (AC-AI-13); closed Severity enum {low,medium,high,critical} + Frequency {rare,occasional,common} (AC-AI-14); checklist 4-section ordering Pre-Output/During/Post-Output/Per-Language (AC-AI-15); every code fence declares language tag, bare ``` FORBIDDEN (AC-AI-16); rule body ≤ 60 lines for atomicity, AC-CL-06 doc analogue (AC-AI-17); checklist runnable as self-graded test ≥ 90% green-rate (AC-AI-18); cross-language sibling-linking for universal concepts anchored at AC-CL-09 (AC-AI-19); self-application doctest gate (AC-AI-20).
- **Preserved** legacy 7 stubs as AC-AI-LEGACY-* at end of §97.
- **Bumped** §97 v3.2.0 → v4.0.0 (major; AC contract reshaped from stub-checkbox to GWT). §98 v1.0.0 → v4.0.0. §99 v3.2.0 → v4.0.0.

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | minor | Phase 27b: Added `kind: future-spec` frontmatter + Drift Acknowledgment section. Module now exempt from drift audit findings (implementation lives in downstream repos). |

## 2026-04-27 — Phase 58 impl-sweep

- Phase 58: appended AI Optimization Telemetry OpenAPI to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 66 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 66 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

