# 35 — Full Spec-Tree AI-Implementability Audit (v7.0)

> **Version:** 7.1.0
> **Updated:** 2026-04-30 (Phase 153 Task A20-rescore — A21 close-out confirmed)
> **Scope:** Entire `spec/` tree — 23 numbered top-level modules
> **Method:** LLM auditor (`linter-scripts/audit-ai-implementability.py` slot 34 v1.4.0) with **Rubric v7 axis-driven dimension weight cascades** + soft caps + fail-fast on missing `content_axis`
> **Supersedes:** [`34-full-tree-ai-audit-v6.md`](./34-full-tree-ai-audit-v6.md) (Phase 152, deterministic-only baseline 100/100; v6's LLM companion baseline was 82.3/100 across v3/v4/v5 LLM rebaselines in Tasks A3/A7/A8)
> **Headline (A20-rescore):** **Tree mean 83.7 → 84.4 (+0.7); zero NEEDS_WORK; zero BLOCKING.** Task A21 mechanical close-out lifted both 74-band modules past predicted floor: **spec/03 74 → 81 (+7)** via two D5 citation-cluster ACs (AC-EM-* in `03-error-manage/97`); **spec/04 74 → 82 (+8)** via D3 edge-case enumeration ACs in `04-database-conventions/97`. Tree band distribution: **5 EXCELLENT · 18 GOOD · 0 NEEDS_WORK · 0 BLOCKING.** v7's axis-driven scoring + A21's mechanical lifts together close the v6 75-floor era.

---

## Headline metrics (Phase 153 Task A20-rescore, 2026-04-30)

| Metric | v6 LLM baseline (Task A8) | v7 baseline (Task A20) | v7 + A21 (A20-rescore) | Δ vs v6 |
|---|---|---|---|---|
| Tree mean | 82.3 | 83.7 | **84.4** | **+2.1** |
| EXCELLENT (≥90) | 4 | 5 | **5** | +1 |
| GOOD (75-89) | 18 | 16 | **18** | held |
| NEEDS_WORK (60-74) | 1 | 2 | **0** | **−1** |
| BLOCKING (<60) | 0 | 0 | **0** | held |
| Strict CI floor | 60 | 60 | **60** | held (AC-34-11) |
| Modules with `content_axis` | 0 | 23/23 | **23/23** | full coverage |
| Auditor exits 2 on missing axis | n/a | yes | **yes** | AC-34-12 |

## Per-module v6 → v7 deltas (sorted by delta)

| Module | Axis | v6 | v7 | Δ | Band |
|---|---|---:|---:|---:|---|
| 10-research | audit-corpus | 75 | **87** | **+12** | GOOD |
| 01-spec-authoring-guide | process-guidance | 75 | **82** | **+7** | GOOD |
| 02-coding-guidelines | normative-contract | 80 | **86** | **+6** | GOOD |
| 11-powershell-integration | integration-spec | 75 | **81** | **+6** | GOOD |
| 26-gitlogs-diagrams | audit-corpus | 75 | **80** | **+5** | GOOD |
| 23-app-database | normative-contract | 93 | **97** | **+4** | EXCELLENT |
| 25-app-issues | audit-corpus | 75 | **79** | **+4** | GOOD |
| 17-consolidated-guidelines | process-guidance | 75 | **78** | **+3** | GOOD |
| 15-distribution-and-runner | normative-contract | 90 | **93** | **+3** | EXCELLENT |
| 24-app-design-system-and-ui | normative-contract | 93 | **95** | **+2** | EXCELLENT |
| 27-spec-toolchain | tooling-spec | 75 | **76** | **+1** | GOOD |
| 28-universal-ci-cli | normative-contract | 86 | **87** | **+1** | GOOD |
| 05-split-db-architecture | normative-contract | 89 | **89** | 0 | GOOD |
| 06-seedable-config-architecture | normative-contract | 89 | **89** | 0 | GOOD |
| 12-cicd-pipeline-workflows | integration-spec | 75 | **75** | 0 | GOOD |
| 16-generic-release | normative-contract | 90 | **90** | 0 | EXCELLENT |
| 18-wp-plugin-how-to | process-guidance | 80 | **80** | 0 | GOOD |
| 22-git-logs-v2 | normative-contract | 86 | **86** | 0 | GOOD |
| 03-error-manage | audit-corpus | 75 | **81** (was 74 pre-A21) | **+6** | GOOD |
| 04-database-conventions | normative-contract | 75 | **82** (was 74 pre-A21) | **+7** | GOOD |
| 13-generic-cli | normative-contract | 93 | **92** | **-1** | EXCELLENT |
| 07-design-system | process-guidance | 89 | **80** | **-9** | GOOD |
| 14-update | normative-contract | 86 | **76** | **-10** | GOOD |

## Rubric v7 mechanics summary

Per AC-34-10..12 in `spec/27-spec-toolchain/34-audit-ai-implementability.md` v1.3.0:

- **AC-34-10** Per-`content_axis` D1–D5 multipliers applied before summing; total weight renormalized to 5.0.
- **AC-34-11** Soft caps (95 for non-contract axes) applied to **bands only**; numeric scores preserved; **strict CI floor stays at 60** tree-wide.
- **AC-34-12** Auditor exits code 2 (fail-fast) if `content_axis` is missing or invalid.

Axis distribution (23 modules):
- `normative-contract`: 12 (52%)
- `audit-corpus`: 4 (17%)
- `process-guidance`: 4 (17%)
- `integration-spec`: 2 (9%)
- `tooling-spec`: 1 (4%)

## Honest-baseline corrections (down-movers)

Two modules dropped under v7 because they previously over-scored on D2/D3 (AC-coverage / Edge-case) for content that is fundamentally narrative or design-rationale:

- **spec/14-update (86→76, -10)** — `normative-contract` axis. v7 caught that update prose carries narrative D5 over-credit; D2/D3 now weighted higher for normative axis. **Action:** mechanical close — bind missing GWT ACs in `14-update/97-acceptance-criteria.md`.
- **spec/07-design-system (89→80, -9)** — `process-guidance` axis. v7 down-weights D2 (AC coverage) for design rationale where ACs are deliberately sparse. Score still GOOD; no action required (matches axis intent).

## NEEDS_WORK close-out (CLOSED — A21 + A20-rescore)

- **spec/03-error-manage:** 74 → **81 (+7)** via D5 citation-cluster ACs in §97 (audit-corpus axis lift exceeded +1 prediction by 6×).
- **spec/04-database-conventions:** 74 → **82 (+8)** via D3 edge-case enumeration ACs in §97.

**Result: 0 NEEDS_WORK modules tree-wide.** A21's predicted lifts (76-78 / 76-77) were exceeded — mechanical AC additions on `audit-corpus` and `normative-contract` axes carry stronger D5/D3 multipliers than estimated.

## What v7 unblocked

- **75-floor breakthrough:** 5 modules (`01`, `10`, `11`, `25`, `26`) escaped v6's 75 ceiling — proof axis-aware scoring works.
- **EXCELLENT-band integrity:** spec/23 lifted to 97 (highest-ever module score); contract-axis modules retain ceiling headroom.
- **Down-movers honest-correct** rather than artificially preserved (Lesson #18 reinforced).

## Open items

- **A21 (CLOSED 2026-04-30):** spec/03 81, spec/04 82 — both GOOD. ✅
- **R1 (blocked):** Trace-map deeper bindings — needs `enable cloud` (separate from `LOVABLE_API_KEY`).
- **A18 (conditional):** D5 honor-list pattern auto-detection — pursue only if a future re-score reveals miscalibration. v7+A21 baseline shows none.
- **P4 (cache hygiene):** All 23 caches refreshed under v7 + A21 lifts; no follow-up needed.

---

**Snapshot source:** `.lovable/memory/audit/v2-deterministic/audit-ai-implementability-latest.md` (Phase 153 Task A20 run, 2026-04-30).
