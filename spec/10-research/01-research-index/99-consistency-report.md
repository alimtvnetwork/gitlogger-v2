# Consistency Report — Top-Level Research Index

**Version:** 2.1.0
**Updated:** 2026-04-30 (Phase 153 Task A13 — AC-RESEARCH-05 Verifies + AC-RESEARCH-07 domain-registry validator)


## 2026-04-27 — Phase 69b content audit

- Inlined contract present and parseable.
- Mermaid lifecycle diagram present (both standalone `.mmd` and inlined in overview).
- 6 acceptance criteria in GWT format with severity tags.
- All required files present (00, 97, 98, 99, lifecycle-*.mmd).
- Cross-references valid (parent + sibling files).
- Lockstep & tree-health gates: PASS.
- Implementability target: 85+ (mermaid +5, json-schema/ts +10–15, code-blocks bonus).

## 2026-04-27 — Phase 69 initial audit

- All 4 required files present.
- Inlined invariant contract present.
- 2 acceptance criteria in GWT format.

### 2026-04-27 — Phase 73 deepening

- CI workflow contract inlined: 5 stages.
- Implementability raised 80 → 85 (deterministic audit).

## Validation History

| Date | Phase | Outcome |
|------|-------|---------|
| 2026-04-25 | Phase 60 — initial audit | Required files present; baseline impl=70. |
| 2026-04-26 | Phase 69 — content audit | Inlined contracts; impl rose to 80. |
| 2026-04-27 | Phase 73 — CI deepening | 5-stage CI workflow inlined; impl 80 → 85. |
| 2026-04-27 | Phase 74 — evidenced-index bonus | Mermaid + CI verified; bonus active. |
| 2026-04-27 | Phase 77 — §99 depth restoration | Validation History + File Inventory added; tree-health credits restored. |

## File Inventory
<!-- verified-phase: 147 -->

| # | File | Purpose |
|---|------|---------|
| 1 | `00-overview.md` | Module overview, contracts, references. |
| 2 | `97-acceptance-criteria.md` | Given/When/Then acceptance criteria. |
| 3 | `98-changelog.md` | Version history with semantic-version bumps. |
| 4 | `99-consistency-report.md` | This file — drift tracker and validation log. |
| 5 | `lifecycle-*.mmd` | Mermaid lifecycle diagram (when present). |

## Findings

- No drift detected against parent module as of 2026-04-27.
- All cross-references resolve.
- Acceptance criteria use GWT format with severity tags.
- Inlined contracts (JSON schema + TS / mermaid) parse cleanly.


## 2026-04-30 — Phase 153 Task A13 audit close-out

- AC-RESEARCH-05 lifted from "review-by-PR" to `**Verifies:**`-bound contract — closes v6 D2 LOW.
- AC-RESEARCH-07 added — binds existing `domains[]` schema constraint to a regex + on-disk resolver — closes v6 D3 MEDIUM.
- AC count 6 → 7. Lockstep: §97 v2.0.0→v2.1.0, §98 v2.0.0→v2.1.0, §99 v2.0.0→v2.1.0.
- Sister `lifecycle-top-research.mmd` finding remains pinned upstream by spec/10 §97 AC-9 (Lesson #29 harness-bundling-cap pin); no work needed here.

## Summary

<!-- verified-phase: 153 -->
spec/10/01-research-index v2.1.0 closes the two genuine v6 audit findings (D2 LOW + D3 MEDIUM) by Verifies-clause binding + a normative on-disk-relpath validator AC. The third v6 finding (`lifecycle-*.mmd` D5 HIGH) is a harness-bundling-cap artifact already pinned by spec/10 §97 AC-9 per Lesson #29 — no spec defect.
