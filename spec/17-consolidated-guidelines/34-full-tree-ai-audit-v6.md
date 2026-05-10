# 34 — Full Spec-Tree AI-Implementability Audit (v6.0)

> **Version:** 6.0.0
> **Updated:** 2026-04-29 (Phase 152)
> **Scope:** **Entire `spec/` tree** — 23 numbered top-level modules, 56 leaf modules, 1373 ACs across §97 files, 87 §99 files
> **Method:** Empirical filesystem scan + automated gate replay (`check-tree-health --strict`, `check-lockstep`, `check-99-summary-freshness`, `check-ai-confidence`)
> **Supersedes:** [`33-full-tree-ai-audit-v5.md`](./33-full-tree-ai-audit-v5.md) (Phase 130 reconciliation, no numeric headline)
> **Superseded by:** [`35-full-tree-ai-audit-v7.md`](./35-full-tree-ai-audit-v7.md) (Phase 153 Task A20, Rubric v7 axis-driven baseline 83.7/100)
> **Headline:** **Tree-wide P3 (Verifies-coverage) driver CLOSED.** All 11 P3-drifter modules brought from partial/zero to full `**Verifies:**` coverage across Tasks #21a–#21d (Phases 148–151). 12 of 15 declared `Production-Ready` modules now match the deterministic AI-confidence derivation; the remaining 3 drift solely on P4 (workflow-ref), not on P3 (contract depth).

---

## Headline metrics (Phase 152, 2026-04-29)

| Metric | v5 baseline (Phase 130) | v6 baseline (Phase 152) | Delta |
|---|---|---|---|
| Tree health (strict) | 100/100 (162/162 credits) | **100/100 (168/168 credits)** | +6 credits (rubric v2.24 widening) |
| Lockstep findings | 0 (87/87) | **0 (87/87)** | held |
| §99 stamp coverage | 0 stamped (advisory) | **81 stamped + 6 exempt + 0 unstamped** | full opt-in adoption |
| §99 stamp staleness | n/a | **0 stale** (max-age 20 phases, h1_horizon=151) | clean |
| AI-confidence eligible modules | not measured | 15 of 23 declared | new gate |
| AI-confidence match rate | not measured | **12/15 (80%)** | new metric |
| P3 (Verifies-coverage) drifters | not measured | **0** ✅ CLOSED tree-wide | new metric |
| P4 (workflow-ref) drifters | not measured | 3 (`07`, `14`, `28`) | residual |
| §97 ACs (tree-wide) | ~1304 (H1 rebaseline) | **1373** | +69 (P3 sweep + ongoing) |
| Trace-map ac_traced | 74 | 74 (held — G-series CLOSED, R1 deferred) | held |
| Strict CI gates | 14 | **15** (added `check-99-summary-freshness.py` at H1; `check-spec-folder-refs` at F2) | +1 net |
| RUBRIC_VERSION | v2.22 | **v2.24** | +2 minors |

## What changed since v5 (Phase 130 → Phase 152)

### Closed (large-impact)
- **P3 Verifies-coverage sweep COMPLETE (Tasks #21a–#21d, Phases 148–151).** 11 slots: `spec/00`, `spec/01-spec-authoring-guide`, `spec/04-database-conventions`, `spec/07-design-system`, `spec/11-powershell-integration`, `spec/14-update`, `spec/17-consolidated-guidelines`, `spec/22-git-logs-v2`, `spec/23-app-database`, `spec/27-spec-toolchain`, `spec/28-universal-ci-cli`. Pattern: scripted Python dict → loop insertion (NOT hand-edit), §97 minor + §00/§98/§99 patch lockstep. Authoring rule codified at `mem://process/verifies-clause-authoring.md`.
- **§99 stamp-freshness gate (Phase H1).** Slot 26 validator `check-99-summary-freshness.py` shipped opt-in stamps; H8 closed coverage to 87/87 (81 stamped + 6 exempt); H9 added stamp-position structural enforcement; P20 added per-file opt-in for `check-version-parity` mirroring the H1 pattern.
- **AI-confidence rubric became normative (Phase P48-1).** `01-spec-authoring.md` § *AI Confidence Rubric (normative)* + AC-09 measurement-evidence requirement; P48-1-fu1 shipped `check-ai-confidence.py` (slot 33 of §27) mechanizing the four-gate derivation. Drift visible since: 13 → 3 over 5 sweep phases.
- **G-series trace-map binding (G1+G2+G3).** `ac_traced` 24 → 69 (+188%); 14 Phase 117–absorbed scripts bound. Remaining ~25 orphans are run.sh/deprecated-v1/helpers — R1 territory.
- **Phase 108 closure (Phase 108-full).** O1/O2/O3 migrated to §27 slots 18/19/25 with end-to-end trace-map bindings.
- **Folder-ref allowlist gate (F1/F2/F3).** `check-spec-folder-refs.py` wired strict; missing-folder discovery dropped from "26 claimed" to 11 actual to 0 after `[doc-only]` classification.
- **B1 Git Logs §07 App identity** — locked decision 12 PERMANENT (Phase 147).

### Open (small-impact, residual)
| Item | Owner | Driver | Notes |
|---|---|---|---|
| **R1** real-AI re-audit | blocked (Lovable Cloud) | Carries forward ~25 trace-map orphans (run.sh/deprecated-v1/helpers/audit-internals) that mechanical binding can't cover |
| **R2** session-persistence regression | monitor | Not re-observed in Phases 117–151 (35 phases clean) |
| **P4 drift** on `spec/07`, `spec/14`, `spec/28` | spec-health.yml workflow-ref editor | Each module's `derived='High'` because the slot isn't called out by name in `.github/workflows/spec-health.yml`. Cosmetic — gate is workflow-ref, not contract depth. Optional patch: add per-module workflow-step name reference |
| **Cosmetic stamp refresh** on 7 modules carrying stamps from Phases 147–148 | optional | Bump to 151 to formally signal "Production-Ready as of P3-sweep close". Gate doesn't require it (max-age budget = 20 phases) |

### Deliberately deferred (out of scope for v6 baseline)
- GAP-V2-05 (Tasks #1–#8): encryption story, advisory-rot lint, app-identity follow-ups, helper parity. Listed in session task ledger; each requires its own focused phase, not a sweep.

## Verification (this audit, 2026-04-29)

```
$ node linter-scripts/check-tree-health.cjs --strict
  ✓ PASS: tree health 100 ≥ threshold 100 (strict — all 56 modules at full marks)
  §99 quality credits: 168 / 168  (15% weight)

$ node linter-scripts/check-lockstep.cjs
  ✓ PASS: lockstep gate
  Findings: 0  (87/87 modules)

$ python3 linter-scripts/check-99-summary-freshness.py --report-only
  Current phase: 147; max stale delta: 20
  §99 files scanned: 87; stamped: 81; exempt: 6; unstamped: 0
  ✅ All stamped §99 Summary blocks are within freshness budget.

$ python3 linter-scripts/check-ai-confidence.py --report
  AI-Confidence rubric parity: scanned=23; eligible=15; matches=12; mismatches=3
  (3 drifts all P4 workflow-ref, not P3 contract-depth)
```

## Method note (why publish a numeric headline this time)

audit-v5 (Phase 130) deliberately published **no** numeric headline because re-using audit-v4's rubric without the AI scorer would have been a fake number. v6 publishes metrics because every claim above is derived from a deterministic gate (`check-tree-health.cjs --strict`, `check-lockstep.cjs`, `check-99-summary-freshness.py`, `check-ai-confidence.py`) — none are AI-generated estimates. The **80% AI-confidence match rate** (12/15) is the v6 headline because it's the first audit where mechanical derivation became possible (P48-1-fu1, Phase 152 baseline).

R1 (real-AI re-audit, blocked on Lovable Cloud) remains the right tool for semantic depth claims (e.g., "is this AC actually implementable by a fresh AI?"). v6 makes no semantic claims — only structural/contract ones backed by gates.

## Forward-looking

- **When R1 unblocks**: re-run trace-map binding on the ~25 remaining orphans; expect `ac_traced` 74 → ~95 (+28%).
- **When P4 drift closes** (3 modules referenced in workflow): AI-confidence match rate 12/15 → 15/15.
- **When 7 cosmetic stamp refreshes land**: visual signal "post-P3-sweep" on every graduated module.

At that point a v7 baseline will be warranted. Until then, v6 is the standing reference.
