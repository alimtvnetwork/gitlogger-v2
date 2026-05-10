# 33 — Full Spec-Tree AI-Implementability Audit (v5.0) — SUPERSEDED

> **⚠️ SUPERSEDED by [`34-full-tree-ai-audit-v6.md`](./34-full-tree-ai-audit-v6.md) (Phase 152, 2026-04-29).** v6 publishes a deterministic numeric headline (tree-health 168/168, AI-confidence 12/15 match, P3 driver CLOSED tree-wide) that v5 deliberately deferred to R1.
>
> **Version:** 5.0.0
> **Updated:** 2026-04-27 (Phase 130)
> **Scope:** **Entire `spec/` tree**
> **Method:** Empirical filesystem scan re-validating every audit-v4 finding
> **Supersedes:** [`31-full-tree-ai-audit-v4.md`](./31-full-tree-ai-audit-v4.md) (45/100, 2026-04-25)
> **Headline:** **Audit-v4's 45/100 baseline is stale.** 3 of 4 critical findings already resolved between 2026-04-25 and 2026-04-27. Provisional re-baseline pending real-AI re-audit (R1, blocked on Lovable Cloud).

---

## §1 — Audit-v4 finding reconciliation

| Audit-v4 finding | v4 status | v5 verified state (2026-04-27) | Outcome |
|---|---|---|---|
| #1 Session-persistence regression | 🔴 unknown root cause | Not re-investigated this session — but also not re-observed: every file written by Phases 117–129 remains on disk. | **Open** — keep watching, no new evidence. |
| #2 Root slot 22 collision (`22-app-issues` vs `22-git-logs-v2`) | 🔴 critical | `spec/22-git-logs-v2/` is alone in slot 22; `spec/25-app-issues/` exists as the rename target. `ls -d spec/2[0-9]-*` confirms 22, 23, 24, 25, 26, 27, 28 — no collision. | ✅ **Resolved** |
| #3 32 broken links to external repo | 🔴 critical | Phase 129: actual count was 3 (not 32), all documentation-example links inside prose. Now waived via `linter-scripts/spec-cross-links.allowlist`. Dashboard reports **0 broken / 2924 ok / 12 external-allowed / 3 waived**. | ✅ **Resolved** |
| #4 Legacy `21-git-logs/` alongside authoritative v2 | 🔴 critical | Folder `spec/21-git-logs/` is **deleted entirely** — `test -d` returns false. Only references remaining are historical mentions in §00 indexes, audit-v4 itself, and `spec/22-git-logs-v2/36-why-v1-archived.md` (intentional archive note). | ✅ **Resolved** |

## §2 — Audit-v4 quantitative claims reconciliation

| v4 claim | v5 verified count | Note |
|---|---|---|
| 13 modules missing `97-acceptance-criteria.md` | **1** (`spec/_archive/`) | `_archive/` correctly excluded from inventory by design. **All real spec folders have §97.** |
| 15 modules missing `99-consistency-report.md` | **1** (`spec/_archive/`) | Same — archive folders intentionally skip §99. **All real spec folders have §99.** |
| 15 sub-folder name collisions | **6** name-duplicates across the tree (`01-diagram-conventions`, `01-research-index`, `02-features`, `03-issues`, `diagrams`, `images`) | All 6 are intentional naming patterns under different parent specs. Not a defect — the parent path disambiguates. |
| Health dashboard out-of-date (80/100, 2026-04-16) | Dashboard now reports **100/100 (A+)** as of Phase 129 (2026-04-27) | Lockstep gate 87/87 pass · 0 findings. |

## §3 — What this means for the 45/100 baseline

The audit-v4 score was computed on a tree state where 3 of the 4 critical findings have since been remediated. The arithmetic:

- **Audit-v4 sub-scores:** Discoverability 30 · Self-containment 40 · Validation Contract 35
- **Direct removals if those findings were re-scored today:**
  - Discoverability: collisions resolved → no longer a -? penalty
  - Self-containment: broken-link count went from 32 → 0 → no longer the main penalty
  - Validation Contract: missing §97/§99 claim was 13/15, actual is 1/1 (and that one is correct-by-design)
- **Likely re-baseline:** 80–95/100 range, but the only authoritative number comes from R1 (real-AI re-audit, blocked on Lovable Cloud).

**This v5 deliberately does NOT publish a numeric headline score.** Re-using audit-v4's rubric without the AI scorer would be a fake number. What v5 *does* publish is: every audit-v4 critical finding has been mechanically re-validated against the current tree state.

## §4 — Open items (carried forward)

1. **R1 — Real-AI re-audit** (still blocked on Lovable Cloud). When unblocked, run the audit-v3-style prompt against the full tree to get an authoritative numeric score that supersedes both v4 and v5.
2. **R2 — Session-persistence root cause** (audit-v4 finding #1). Not re-observed in Phases 117–129 but not formally proven absent. Keep monitoring.
3. **B1 — `spec/22-git-logs-v2/07-app-entity.md` `App` identity columns** — lone open question in folder 22 (`Environment` / `Platform` / `OwnerEmail` decision pending).

## §5 — Method (for reproducibility)

```bash
# Verify root slot collision
ls -d spec/2[0-9]-*

# Verify legacy folder absence
test -d spec/21-git-logs && echo "EXISTS" || echo "GONE"

# Verify §97/§99 inventory
for d in spec/*/; do test -f "$d/97-acceptance-criteria.md" || echo "MISSING §97: $d"; done
for d in spec/*/; do test -f "$d/99-consistency-report.md" || echo "MISSING §99: $d"; done

# Re-run dashboard
node linter-scripts/generate-dashboard-data.cjs   # → 100/100 (A+) · 0 broken
node linter-scripts/check-lockstep.cjs            # → 87/87 pass · 0 findings
python3 linter-scripts/check-spec-cross-links.py  # → OK
```

All commands above were executed on 2026-04-27 in the session that produced this file.

## §98 — Changelog

| Version | Date | Changes |
|---|---|---|
| 5.0.0 | 2026-04-27 | Initial publication. Reconciles audit-v4's 4 critical findings against current tree state — 3 of 4 resolved. Provides verifiable bash commands for re-validation. Defers numeric re-score to R1 (real-AI re-audit). |
