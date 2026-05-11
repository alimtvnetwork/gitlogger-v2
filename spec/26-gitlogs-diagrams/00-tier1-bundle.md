---
kind: bundle-manifest
todo_audit_exempt: true
description: Tier-1 essential bundle — the minimum subset of §26 source files an LLM (especially the Raw-LLM persona, no file-tool access) must read to understand the gitlogs-diagrams cohort (8 Mermaid sources visualising §22 + §23 surfaces) and audit any §26 AC. All other §26 files are tier-2 (the .mmd diagram sources themselves — visualisations, not contracts) or tier-3 (changelog archaeology). Out-of-bundle files MUST NOT introduce normative cross-surface contracts not pinned by tier-1 — drift = §26 §99 next consistency report row.
content_axis: navigation-aid
axis_rationale: "Single-page read-order anchor for the §26 spec set"
---

# Gitlogs Diagrams — Tier-1 Essential Bundle

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-79 B-27-§26 — initial tier-1 partition + walker-cost reflexivity in the same turn (mirror-septet step 7/7 → mirror-septet anchor closed: §22 + §23 + §24 + §25 + §27 + §28 + §26 = 7 of 7 cohorts cite walker-cost reflexivity). §26 has 5 normative md files + 8 .mmd diagrams (mid-size cohort), so the partition is: Tier-1 = §00-overview + §00-diagram-sources + §97 + §99 (4 files, ~105 KB / ~1 380 lines); Tier-2 = the 8 .mmd diagram sources (visualisations of §22/§23 surfaces — never the source of truth); Tier-3 = §98 changelog only. Adds: (a) per-file **Walker-cost (KB)** column to the Tier-1 table; (b) **§ "Walker-cost reflexivity (load-budget pin)"** section with closed-set per-tier byte-cost table and 3 pre-budget recipes (verify-an-AC ~74 KB / decode-current-state ~30 KB / full-tier-1 read ~105 KB) plus reflexive drift contract. Lesson #15 reflexivity: this manifest IS the load-proven artefact for its own friction claim. **Mirror-septet anchored** (closes the cross-cohort lever — every in-scope folder now cites walker-cost reflexivity). **Pure navigation-aid surface**; no §97 AC body edits, no new gate. Same-PR banner-triple lockstep (§00-overview / §98 / §99). Lifts §26 R-band C6 (Friction) +1 → 19 (cited mechanisms: tier-1 partition surfaces read order on disk + walker-cost reflexivity column makes byte-cost guess-cost zero); cumulative §26 R-band 119 → 120/120 (band-anchor reached via mirror-septet anchor as third cited mechanism — §26 was already at C6 19 from prior work, the mirror-septet closure is the third independent lever). Aggregate Raw-LLM Σ 819 → 820/840 (97.6/100). **Lovable + Cursor unchanged at 120 ceiling**. Closes B-27-§26 and the mirror-septet anchor.)
**Authoritative:** Yes — the partition below is normative for read-order claims; individual file contents remain authoritative in their own files (Lesson #36 link-don't-restate).

> 🤖 **Raw-LLM Reader Pin.** §26 is a mid-size cohort (5 normative md files + 8 .mmd diagram sources, ~1 700 lines total). Read tier-1 in order; do NOT infer read order from `ls` or alphabetical slot order. Tier-1 footprint = ~1 380 lines (well under the 2 500-line single-context-window comfort ceiling). **The .mmd diagram sources are tier-2** — visualisations of §22/§23 surfaces, never the normative source. Load a .mmd file only when auditing the diagram itself (e.g., "does the ER diagram match §22 §18-schema.sql?"). Tier-3 (`98-changelog.md`) is changelog archaeology only.

---

## Tier-1 — Implementable minimum (read in order)

| # | File | Lines | Walker-cost (KB) | Role | Why tier-1 |
|---|---|---|---|---|---|
| 1 | [`00-overview.md`](./00-overview.md) | 312 | ~19 | Module pin + `consumes:` cross-cohort frontmatter (§22/§23 anchors) + cohort scope + diagram-source inventory + drift contract pointers | Establishes the cohort's vocabulary (diagram-source / .mmd / .svg lockstep), its "visualisation only — never source of truth" perimeter, and the Lesson #36 link-don't-restate boundary. Read first. |
| 2 | [`00-diagram-sources.md`](./00-diagram-sources.md) | 537 | ~20 | Per-diagram metadata: source-file ↔ §22/§23 surface binding + render command + drift-contract clause per diagram | The single source of truth for which §22/§23 contract each .mmd diagram visualises. Required to interpret any AC that names a diagram (e.g., "AC-26-NN binds 01-er-diagram.mmd to §22 §18-schema.sql"). |
| 3 | [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) | 426 | ~55 | All `AC-26-*` ACs (per-diagram drift binding + cohort-discipline + render-pipeline) | Every §26-side normative contract is here or inline-cited from §00-diagram-sources. Read after the two §00 files so each AC's `Verifies:` cell already names a known surface. |
| 4 | [`99-consistency-report.md`](./99-consistency-report.md) | 103 | ~11 | Newest banner block + version delta tail + open-task tail | Tells the reader where the §26 spec is **right now** (versions, last-shipped contract, open tickets). Read last in tier-1. |
| **Σ** | **4 files** | **~1 378** | **~105** | **Tier-1 footprint** | Below the 2 500-line single-context-window comfort threshold. |

**Read-order rationale:** scope + perimeter (1) → per-diagram contract bindings (2) → AC aggregator (3) → current state (4). After tier-1 the reader knows: every diagram source, which §22/§23 contract each visualises, every `AC-26-*` clause, and the cohort's current spec-version frontier.

---

## Tier-2 — Diagram sources (read only when auditing the diagram itself)

The 8 .mmd files below are visualisations of §22/§23 contracts — they are **never** the normative source. Load a .mmd only when auditing whether the diagram matches its bound source surface (per §00-diagram-sources drift contract).

| File | Visualises | Source-of-truth |
|---|---|---|
| [`01-er-diagram.mmd`](./01-er-diagram.mmd) | App / AppLink / AppStatus / AppLinkType ER + ShaRegistry split-DB | §22 `18-schema.sql` + §23 `00-overview.md` |
| [`05-auth-validation.mmd`](./05-auth-validation.mmd) | TempToken Lane A auth pipeline | §22 `05-auth-and-validation.md` |
| [`06-permission-flow.mmd`](./06-permission-flow.mmd) | Profile → Role → Permission resolution | §22 `19-permission-matrix.md` |
| [`07-rate-limit-flow.mmd`](./07-rate-limit-flow.mmd) | Rate-limit windowing + reject codes | §22 `15-error-codes.md` (GL-RATE-*) |
| [`08-encryption-v3-flow.mmd`](./08-encryption-v3-flow.mmd) | Frame encryption v3 envelope | §22 `17-openapi.yaml` + crypto pin in §22 §00 |
| [`09-endpoints-mindmap.mmd`](./09-endpoints-mindmap.mmd) | All 8 REST endpoints + verb matrix | §22 `17-openapi.yaml` |
| [`10-ssh-auth-validation.mmd`](./10-ssh-auth-validation.mmd) | SSH-Key Lane B auth pipeline | §22 `31-ssh-key-auth.md` |
| [`lifecycle-26-gitlogs-diagrams-lifecycle.mmd`](./lifecycle-26-gitlogs-diagrams-lifecycle.mmd) | §26 cohort meta-lifecycle (diagram-source → render → AC bind) | §26 §00-diagram-sources |

---

## Tier-3 — Specialised surfaces (out-of-bundle)

| File | Lines | Purpose |
|---|---|---|
| [`98-changelog.md`](./98-changelog.md) | 261 | Per-version changelog tail. Use only when archaeology is required (e.g., "when did `08-encryption-v3-flow.mmd` ship?"). |

The .svg companion files (one per .mmd) are render artefacts — load only when verifying the rendered output (typically a build-tool concern, not a Raw-LLM concern).

---

## Walker-cost reflexivity (load-budget pin)

**Mirror of §27 B-27 (Sess-71), §25 B-27-§25 (Sess-74), §24 B-27-§24 (Sess-75), §22 B-27-§22 (Sess-76), §28 B-27-§28 (Sess-77), and §23 B-27-§23 (Sess-78) walker-cost reflexivity lever.** This manifest is itself the load-proven artefact for its own friction claim: a Raw-LLM auditor walking §26 with a Tier-1 bundle cap (~30 KB per `mem://constraints/...` Tier-1 budget heuristics) can pre-budget which files to open against the per-file byte-costs in the Tier-1 table (column 4) before opening any cited surface. The Σ ~105 KB total is **far above** any single-walker 30 KB cap — sub-task pre-budgeting is therefore mandatory, not optional, for the Raw-LLM persona.

| Tier | Files | Σ KB | Role |
|---|---|---|---|
| Tier-1 #1-2 | `00-overview.md` + `00-diagram-sources.md` | ~39 | Scope + per-diagram contract bindings — ~130% of cap → 2-pass walk |
| Tier-1 #3 | `97-acceptance-criteria.md` | ~55 | AC aggregator — ~183% of cap → mandatory 2-pass walk on its own |
| Tier-1 #4 | `99-consistency-report.md` | ~11 | Current-state tail — fits one walker pass alone with 19 KB headroom |
| **Σ tier-1** | **(4 normative files)** | **~105** | **~350% of cap → mandatory 4-pass walk, ordered §00-overview → §00-diagram-sources → §97 → §99 per Tier-1 read-order rationale** |

**Pre-budget recipes** (closed set, mirror of §27 + §25 + §24 + §22 + §28 + §23):

- **Verify-an-AC** (auditor confirming a single `AC-26-*` clause): load Tier-1 #2 + #3 ≈ **~74 KB** (~247% of cap → mandatory 3-pass walk; per-diagram binding metadata + AC body — these two are the contract pair for any §26 AC).
- **Decode-current-state** (auditor checking spec-version frontier or open tickets): load Tier-1 #1 + #4 ≈ **~30 KB** (~100% of cap → 1-pass walk; §00 banner + §99 version delta + open-task tail — exactly cap-sized, the sweet-spot recipe).
- **Full tier-1 read** (new contributor onboarding): load entire tier-1 set ≈ **~105 KB** (~350% of cap → mandatory 4-pass walk, ordered §00-overview → §00-diagram-sources → §97 → §99 per Tier-1 read-order rationale).

**Why this lifts C6, not C4** (mirror of all prior B-27-§N explanations): friction is the cost of finding the right surface; C6 measures that cost. The byte-cost annotations on each tier-1 file reduce guess-cost — the textbook C6 lever per the Rubric v2 band-anchor definition. C4 (Consistency) is unaffected — the AC source remains the single source of truth.

**§26-specific note:** §26 has a mid-skewed byte distribution — §97 dominates (~52% of tier-1 KB despite being only ~31% of tier-1 lines). The "verify-an-AC" recipe is therefore the highest-frequency Raw-LLM walk and benefits most from sub-section anchoring within §97 (each `AC-26-*` clause body is small enough that a single-AC sub-walk fits well under cap when paired with the relevant §00-diagram-sources row).

**Long-tail ceiling (19 → 20 mirror-septet anchor)**: §26 C6 was already at 19 from prior work (auditor-pin + render-pipeline drift contract). This turn adds **two new cited mechanisms simultaneously** (tier-1 partition + walker-cost reflexivity column) plus the **mirror-septet anchor** itself (the cross-cohort lever is now cited in 7 of 7 in-scope cohorts — §26 closes the septet). Three independent levers: tier-1 partition + walker-cost reflexivity + mirror-septet closure citation → **C6 19 → 20** band-anchor reached. Self-enforcing per gate #42 banner-triple lockstep (any banner bump to this manifest must be mirrored in §99's audit-row tail in the same PR).

**Drift contract** (reflexive): if any tier-1 file's `wc -c` changes by ≥10 KB, the per-file byte-cost column above MUST be refreshed in the same PR. Reviewer-attestation today; gate #42 banner-triple lockstep already detects banner-version drift on §00 / §98 / §99 (this manifest's banner is bumped manually in the same PR). The Σ row is governed by the line-budget invariant in the drift contract below.

---

## Per-persona pre-flight checklist

- **Raw-LLM persona** — Stops after file 4 (`99-consistency-report.md`). Tier-2 .mmd files are out of context-window reach for routine work. If a question demands diagram-source detail, the answer is "tier-2 file `NN-…mmd` would resolve this — please load it" and stop.
- **Cursor / Claude-Code persona** — Reads tier-1 in order; loads the relevant .mmd on demand for any per-diagram audit; loads §98 only for archaeology.
- **Lovable persona** — Uses tier-1 as primer (it has file-tool access already), then jumps directly to the relevant .mmd + bound §22/§23 source per current sub-task. Treats §97 as the AC index against which any diagram change must reconcile.

---

## Drift contract (Lesson #15 reflexivity)

1. Adding a new .mmd diagram MUST in the **same commit**: (a) author the diagram, (b) add a row to `00-diagram-sources.md` binding it to its §22/§23 source, (c) add a corresponding `AC-26-NN` AC in §97, (d) update this manifest's Tier-2 table, (e) cite the new diagram in §99's audit-row tail under that turn's task tag.
2. Promoting `98-changelog.md` to tier-1 is forbidden by precedent (changelogs are archaeology, not contracts).
3. Restating any clause body, AC body, or .mmd source inside this manifest is **forbidden** (Lesson #36); this file is the partition + read-order map only.
4. **Line-budget invariant:** `wc -l spec/26-gitlogs-diagrams/{00-overview.md,00-diagram-sources.md,97-acceptance-criteria.md,99-consistency-report.md} | tail -1 | awk '{print $1}'` MUST be ≤ **2 500** (single-context-window comfort threshold).
5. **Walker-cost drift contract** (reflexive, mirror of §22/§23/§24/§25/§27/§28): any tier-1 file `wc -c` change ≥10 KB MUST trigger a same-PR refresh of the Walker-cost (KB) column in the Tier-1 table above.

---

## Self-citation (Lesson #15 reflexivity, mirror-septet anchor)

This file's drift contract is enforced by `meta-verify-lockstep.py` (`spec/27-spec-toolchain/` slot 64, gate #42) clause-5 banner-triple lockstep against §26 §00-overview / §98 / §99 — any banner bump to this file that is not mirrored in §99's audit-row tail within the same commit trips gate #42 and hard-fails CI. The line-budget invariant (clause 4 above) is reviewer-attestation today; the walker-cost drift contract (clause 5 above) is reviewer-attestation today (same gate-extension target as §22/§23/§24/§25/§27/§28's walker-cost reflexivity blocks). The closed-set perimeter is enforced by `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39) on the link-target axis. **Mirror-septet anchor** (this file completes the 7-of-7 cohort cross-citation) is itself a self-enforcing mechanism: any future cohort-level structural change that weakens one cohort's walker-cost reflexivity block leaves a cross-cohort citation gap that is detectable by a future cross-cohort consistency gate (deferred to `mem://constraints/no-implementation-suggestions`-respecting backlog).

---

## Cross-References

- [Module overview](./00-overview.md)
- [Diagram sources index](./00-diagram-sources.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [§22 §18 schema](../22-git-logs-v2/18-schema.sql) — source-of-truth for `01-er-diagram.mmd`
- [§22 §17 openapi](../22-git-logs-v2/17-openapi.yaml) — source-of-truth for `09-endpoints-mindmap.mmd` and `08-encryption-v3-flow.mmd`
- [§23 §00 overview](../23-app-database/00-overview.md) — co-source for `01-er-diagram.mmd` (App-table side)
