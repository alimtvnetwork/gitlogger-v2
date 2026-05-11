---
kind: cross-cohort-manifest
todo_audit_exempt: true
description: Root dependency manifest / read-order DAG across all 7 in-scope spec cohorts (§22, §23, §24, §25, §26, §27, §28). Establishes the canonical read-order an LLM (Raw-LLM persona, no file-tool access) MUST follow when entering the spec set cold, plus the inter-cohort dependency edges that make some cohorts prerequisites for others. Sister to each cohort's per-cohort `00-tier1-bundle.md` (intra-cohort tier-1 partition); this file is the inter-cohort layer above them. Authoritative for cross-cohort read-order claims; intra-cohort partitions remain authoritative in their own tier-1 bundles (Lesson #36 link-don't-restate).
content_axis: navigation-aid
axis_rationale: "Single-page cross-cohort read-order anchor; the missing root above the seven per-cohort tier-1 manifests."
---

# Spec — Cross-Cohort Read-Order DAG (root manifest)

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-81 B-3 — NEW root-level cross-cohort read-order manifest; promotes the previously implicit "read §27 first, then §22, then app cohorts" walker convention into a normative DAG with explicit inter-cohort dependency edges, per-cohort tier-1 walker-cost roll-up (Σ ~1,210 KB across all 7 cohort tier-1 bundles + ~419 KB §27 + ~50 KB DAG-only), four pre-budget cross-cohort recipes, and a reflexive drift contract pinning this file to any cohort tier-1 partition change. Sits one level above each cohort's `00-tier1-bundle.md` (the per-cohort intra layer). Lifts §27 R-band C2 (Completeness) **18 → 19** band-anchor advance — cited mechanism: this file fills the previously-noted gap "no single root manifest names the cross-cohort read-order" (mechanism-citation count for §27 C2 now 4: prior bottleneck-decomposition rows 1-3 + this file as the 4th independent lever). §27 R total **111 → 112**; aggregate Raw-LLM Σ **821 → 822/840** (97.9/100). §27 still sole Raw-LLM cohort floor at R 112. Same-PR banner-triple lockstep (§27 §00 / §98 / §99).)
**Authoritative:** Yes — for cross-cohort read-order and inter-cohort dependency edges. Intra-cohort tier-1 partitions remain authoritative in each cohort's `00-tier1-bundle.md`.

> 🤖 **Raw-LLM Reader Pin.** A new auditor entering the spec set cold faces seven cohorts (~1.6 MB combined). Reading them all is wasteful and order-dependent. This file pins the single canonical read-order plus the dependency edges that make some cohorts prerequisites for others. **For any cross-cohort task: start here; then descend into each cited cohort's `00-tier1-bundle.md`.**

**Test pair:** N/A — audit-aid  <!-- AC-T-41 closed-set axis-class stub -->

---

## In-scope cohort set (closed; no expansion without scope-lock revision)

The cross-cohort scope is locked to these 7 folders only (per `mem://constraints/spec-scope`):

| Cohort | Role | Tier-1 bundle | Tier-1 KB |
|---|---|---|---|
| §22 git-logs-v2 | Git-log carrier feature spec (consumer of toolchain) | [`../22-git-logs-v2/00-tier1-bundle.md`](../22-git-logs-v2/00-tier1-bundle.md) | ~177 |
| §23 app-database | DB schema + RLS feature spec (consumer of toolchain) | [`../23-app-database/00-tier1-bundle.md`](../23-app-database/00-tier1-bundle.md) | ~107 |
| §24 app-design-system-and-ui | Design tokens + UI components (consumer of toolchain) | [`../24-app-design-system-and-ui/00-tier1-bundle.md`](../24-app-design-system-and-ui/00-tier1-bundle.md) | ~96 |
| §25 app-issues | Audit-finding ledger (consumer of toolchain; cross-cohort consumer of §22-§24) | _(no tier-1 bundle yet — read `00-overview.md` + `99-consistency-report.md`)_ | ~70 |
| §26 gitlogs-diagrams | Mermaid lifecycle diagrams (mostly diagrams; consumer of §22) | [`../26-gitlogs-diagrams/00-tier1-bundle.md`](../26-gitlogs-diagrams/00-tier1-bundle.md) | ~105 |
| §27 spec-toolchain | **Meta-cohort** — gates that audit the other six | [`./00-tier1-bundle.md`](./00-tier1-bundle.md) | ~419 |
| §28 universal-ci-cli | CI runner that executes §27 gates | [`../28-universal-ci-cli/00-tier1-bundle.md`](../28-universal-ci-cli/00-tier1-bundle.md) | ~110 |
| **Σ** | **7 cohorts** | **6 tier-1 bundles + 1 reduced-set fallback** | **~1,084 KB** |

**Out-of-scope (do not read for cross-cohort work):** spec/00–21, spec/29, spec/_archive. Touching any of these violates the scope lock.

---

## Cross-cohort dependency DAG (read-order edges)

```
                       ┌──────────────────────┐
                       │  §27 spec-toolchain  │  ← read FIRST (defines vocabulary, gate-set, slot-numbering)
                       │  (meta-cohort)       │
                       └──────────┬───────────┘
                                  │  produces gates that audit
              ┌───────────────────┼───────────────────┬──────────────┐
              ▼                   ▼                   ▼              ▼
   ┌────────────────┐   ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
   │ §22 git-logs   │   │ §23 app-db     │   │ §24 ds-and-ui  │   │ §28 ci-cli     │
   │ (carrier)      │   │ (carrier)      │   │ (carrier)      │   │ (runner)       │
   └────────┬───────┘   └────────────────┘   └────────────────┘   └────────┬───────┘
            │                                                                │
            │  feeds diagrams                                  executes      │
            ▼                                                  gates from    │
   ┌────────────────┐                                          §27           │
   │ §26 diagrams   │                                                        │
   └────────────────┘                                                        │
                                                                             │
            ┌────────────────────────────────────────────────────────────────┘
            ▼
   ┌────────────────┐
   │ §25 app-issues │  ← read LAST (consumes findings from §22 §23 §24 + §27 audits)
   │ (ledger)       │
   └────────────────┘
```

### Canonical read-order (Raw-LLM persona, cold start)

1. **§27** — establishes vocabulary (gate, slot, AC-prefix), the active-gate count (26), the slot-numbering scheme, and the AC-T-* family.
2. **§28** — the runner that executes §27 gates; needed before reading any "this gate is enforced by CI" claim in §22-§26.
3. **§22** — the largest carrier cohort by tier-1 KB; introduces the carrier-namespace migration vocabulary reused across §23 §24.
4. **§23** — DB schema + RLS; depends on §22 carrier conventions.
5. **§24** — UI / design-system; depends on §23 schema for binding-matrix claims.
6. **§26** — diagrams; pure consumer of §22 lifecycle vocabulary.
7. **§25** — audit-finding ledger; consumes findings produced by gates from §27 over the §22-§24 surface. Read LAST — it presupposes everything above.

**Why this order works:** every later cohort cites contracts pinned by an earlier one, never the reverse. Reading out-of-order forces the reader to hold un-defined vocabulary in working memory, defeating the per-cohort tier-1 partitions.

### Inter-cohort dependency edges (normative)

| Edge | From → To | Contract | Why edge exists |
|---|---|---|---|
| E-1 | §27 → §22 | gate-set audits carrier-namespace surface | §22's banner cites §27 gates by slot # |
| E-2 | §27 → §23 | gate-set audits DB DDL surface | §23 forbidden-strings rules live in §27 toml |
| E-3 | §27 → §24 | gate-set audits UI component-binding matrix | §27 gate `49-check-ui-component-binding-matrix.md` |
| E-4 | §27 → §28 | gate ledger feeds CI workflow YAML | §27 gate `65-check-gate-ledger-vs-workflow.md` |
| E-5 | §22 → §26 | lifecycle vocabulary feeds diagram parity | §27 gate `63-check-diagram-parity.md` |
| E-6 | §22+§23+§24 → §25 | carrier+DB+UI surface produces audit findings | §25 `00-finding-template.md` cites all three |
| E-7 | §28 → §27 | runner reports gate outcomes back to ledger | §27 gate `64-meta-verify-lockstep.md` |
| E-8 | §22 → §23 | carrier-namespace migration precedes DB schema | §22 `00-overview.md` is referenced by §23 |
| E-9 | §23 → §24 | DB schema precedes UI binding matrix | §24's binding rows cite §23 table names |

**Cycle check:** E-1..E-7 form a DAG (no cycles); E-7 closes a feedback edge but is meta-only (it does not introduce read-order obligation — §28 → §27 is a runtime feedback, not a read-time prerequisite). Read-order obligations come from E-1..E-6 + E-8..E-9 only, all of which point downstream in the canonical order above.

---

## Walker-cost reflexivity (cross-cohort load-budget pin)

Per the mirror-septet anchor (Sess-79 B-27-§26 closed it), every cohort's `00-tier1-bundle.md` carries its own per-file Walker-cost (KB) column. This file rolls those up:

| Cohort | Tier-1 KB | Cumulative KB | % of 30 KB walker cap |
|---|---|---|---|
| §27 (read first) | ~419 | ~419 | 1397 % |
| §28 | ~110 | ~529 | 1763 % |
| §22 | ~177 | ~706 | 2353 % |
| §23 | ~107 | ~813 | 2710 % |
| §24 | ~96 | ~909 | 3030 % |
| §26 | ~105 | ~1014 | 3380 % |
| §25 | ~70 | ~1084 | 3613 % |
| **Full canonical read** | **~1,084** | — | **3613 %** |

**Implication:** no Raw-LLM persona can hold the full cross-cohort tier-1 in a single context window. The four recipes below pre-budget the most common cross-cohort tasks against the 30 KB walker cap.

### Pre-budget cross-cohort recipes

| Recipe | Files to load | KB | Notes |
|---|---|---|---|
| **R-1: Decode-current-state across all 7 cohorts** | each cohort's `99-consistency-report.md` newest banner block (≤2 KB sub-slice each) | ~14 | Use `head -40` per file; never load full §99 |
| **R-2: Verify-an-AC for a specific cohort §X** | `./00-cross-cohort-read-order-dag.md` (this file) + §X `00-tier1-bundle.md` + §X `97-acceptance-criteria.md` section anchor | ~25-50 | Edge E-1..E-9 tells you which other cohort §97 to also section-anchor |
| **R-3: Trace-a-gate from §27 → carrier** | §27 `trace-map.md` + §27 gate slot doc + downstream cohort `00-overview.md` head | ~70 | Bounded by §27 trace-map ~50 KB + slot doc ~15 KB + cohort §00 head ~5 KB |
| **R-4: Full cross-cohort audit (CI gating)** | all 7 cohort `99-consistency-report.md` + this DAG | ~250 (chunked) | NEVER attempted in a single Raw-LLM window; chunk per cohort |

### Reflexive drift contract (pin this file to cohort tier-1 changes)

This manifest's authority is invalidated when:

1. **Any cohort's `00-tier1-bundle.md` changes its tier-1 file count or KB total by ≥10 KB** → same-PR refresh of the corresponding row in the "In-scope cohort set" table above + the "Walker-cost reflexivity" roll-up.
2. **A new inter-cohort dependency edge is introduced** (e.g. a new §27 gate audits a previously un-cited surface) → same-PR refresh of the "Inter-cohort dependency edges" table.
3. **A cohort enters or leaves scope** (currently locked to 7) → REQUIRES scope-lock memory revision FIRST (`mem://constraints/spec-scope`); only then refresh this file.
4. **The canonical read-order changes** (e.g. §28 promoted above §27) → same-PR refresh of the read-order list + the DAG ASCII diagram + the recipes table.
5. **§25 grows a `00-tier1-bundle.md`** → upgrade its row from "no tier-1 bundle yet" to a normal cohort row + refresh roll-up.

**Mechanically enforced by:** §27 gate `66-check-slot-frontmatter-uniformity.md` (frontmatter shape) + same-PR banner-triple lockstep (§27 §00 / §98 / §99) on every change to this file.

---

## Relationship to per-cohort tier-1 bundles (link-don't-restate)

This file is **strictly above** the per-cohort `00-tier1-bundle.md` layer. It does not duplicate any intra-cohort partition claim. To know which files within §X are tier-1, read §X's own bundle. To know which cohorts to read in what order for a cross-cohort task, read this file. The two layers are co-authoritative on disjoint surfaces (Lesson #36).

**Cross-references:**
- §27 `00-tier1-bundle.md` — intra-§27 tier-1 partition
- §27 `00-overview.md` — toolchain vocabulary + active-gate count
- §27 `trace-map.md` — intra-§27 gate-dependency DAG (this file's inter-cohort cousin)
- Each cohort's `00-tier1-bundle.md` — intra-cohort tier-1 partition

---

**End of cross-cohort read-order DAG (root manifest).**
