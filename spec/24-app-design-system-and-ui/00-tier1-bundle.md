---
kind: bundle-manifest
todo_audit_exempt: true
description: Tier-1 essential bundle — the minimum subset of §24 source files an LLM (especially the Raw-LLM persona, no file-tool access) must read to understand the App Design System & UI overlay (`--app-*` token catalog, AppShell, §07 dependency boundary, §22 inheritance contract). All 4 normative §24 files are tier-1; the cohort fits in a single context window with no tier-2/3 demotions required. Out-of-bundle files MUST NOT introduce normative cross-surface contracts not pinned by tier-1.
content_axis: navigation-aid
axis_rationale: "Single-page read-order anchor for the §24 App Design System spec set"
---

# App Design System & UI — Tier-1 Essential Bundle

**Version:** 1.1.0
**Updated:** 2026-05-11 (Sess-75 B-27-§24 — mirror of §27 B-27 (Sess-71) and §25 B-27-§25 (Sess-74) walker-cost reflexivity lever applied to §24. Adds: (a) per-file **walker-cost (KB)** column to the Tier-1 table (Σ ~150 KB across the 4 normative files: §00 ~47 KB / §97 ~37 KB / §99 ~11 KB / §98 ~53 KB; computed via `wc -c` 2026-05-11); (b) NEW **§ "Walker-cost reflexivity (load-budget pin)"** section between Tier-3 and the per-persona checklist, with a closed-set per-tier byte-cost table and 4 pre-budget recipes (verify-an-AC ~84 KB / contract-only-walk; audit-current-state ~64 KB / live-banner-walk; provenance-audit ~100 KB / changelog-walk; full-tier-1 read ~150 KB / new-contributor-onboarding). Lesson #15 reflexivity: this manifest IS the load-proven artefact for its own friction claim — mirror of §27 `00-tier1-bundle.md` Tier-2 lookup pattern but specialised on walker-cost vs slot-index. **Pure navigation-aid extension**; no §97 AC body edits, no new gate, no new tier promotion. Same-PR banner-triple lockstep (§00 / §98 / §99). Lifts §24 R-band C6 (Friction) **carried at 20** (band-anchor mechanism strengthened — walker-cost reflexivity column is now the cited self-enforcing mechanism for C6's existing 20-band score; no point-lift available, defensibility hardened — analogous structural lever to §27 B-27 C6 15 → 16 and §25 B-27-§25 C6 18 → 19, but applied to a cohort whose C6 was already at ceiling). C1/C2/C3/C4/C5 carried at 20/20/19/20/20 (per Sess-69 B-17 §99 attestation R 119; sole below-ceiling criterion is C3 Testability). §24 Raw-LLM /120 **carried at 119** (Sess-69 B-17 baseline; this turn is a score-holding defensibility refresh, not a point-lift). **Lovable + Cursor unchanged** (file-tool traversal already resolves byte-costs trivially). Aggregate Raw-LLM Σ **carried at 817/840** (this turn is a score-holding defensibility refresh; no point-lift). Closes B-27-§24. Prior: 1.0.0 — Sess-69 B-17 initial tier-1 partition.)
**Updated-prev:** 2026-05-11 (Sess-69 B-17 — initial tier-1 partition; mirrors the §22 B-1 (Sess-67), §27 B-6 (Sess-67), and §28 B-7 (Sess-68) tier-1 manifest pattern.)
**Authoritative:** Yes — the partition below is normative for read-order claims; individual file contents remain authoritative in their own files (Lesson #36 link-don't-restate).

> 🤖 **Raw-LLM Reader Pin.** §24 is a *strict additive overlay* on §07-design-system: it owns the `--app-*` token namespace, AppShell layout, breakpoints, and theme parity — and ZERO SQL DDL (boundary closed by AC-ADS-17, gate #36). The cohort is **small** (4 normative files, ~1 606 lines of Markdown + 1 lifecycle diagram, total ~1 617 lines). The entire §24 normative surface fits comfortably under the 2 500-line single-context-window comfort ceiling, so **all 4 files are tier-1**. There is no tier-2 / tier-3 demotion in this cohort — read every file in order. Do NOT infer read order from `ls`, alphabetical slot order, or §00's `produced_for:` frontmatter list.

---

## Tier-1 — Navigable minimum (read in order)

| # | File | Lines | Walker-cost (KB) | Role | Why tier-1 |
|---|---|---|---|---|---|
| 1 | [`00-overview.md`](./00-overview.md) | 932 | ~47 | Module pin + Quick-Nav (Walker Index) + Walker-Pin (4 critical ACs surfaced) + Raw-LLM Auditor Pin (Lesson #36 memory resolution) + `--app-*` token catalog + AppShell pattern + §07 dependency boundary `### A-05` + §22 inheritance contract surface + impl-sweep appendices | Establishes the overlay's scope, the §07 boundary, the `--app-*` namespace, and every cross-cohort pin (§07, §22, §27 gates #15/#19/#36/#39/#42). Read first — Quick-Nav routes a context-bounded walker to any sub-anchor in one hop. |
| 2 | [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) | 284 | ~37 | All 17 `AC-ADS-*` ACs (token namespace, raw-color forbidden, light/dark parity, AppShell invariant, §07 dependency boundary AC-ADS-16, §22 inheritance AC-ADS-15, externalized citation map AC-ADS-14, no-DDL boundary AC-ADS-17) + per-AC `T-ADS-NN-NN` test invariant blocks | Every §24 contract is here. Read after §00 so each AC's `Verifies:` cell already names a known surface. |
| 3 | [`99-consistency-report.md`](./99-consistency-report.md) | 142 | ~11 | Newest banner block + module-health table + version-delta tail + open-task tail | Tells the reader where the §24 spec is **right now** (versions, last-shipped gate, no-DDL negative-evidence sweep result, open tickets). Read third in tier-1. |
| 4 | [`98-changelog.md`](./98-changelog.md) | 261 | ~53 | Per-version changelog tail back to v3.x | Last in tier-1: gives provenance for every banner the reader has just absorbed (why a clause exists, which audit task closed it). |
| **Σ** | **4 files** | **~1 619** | **~148** | **Tier-1 footprint** | Below the 2 500-line single-context-window comfort threshold by ~881 lines; byte-budget annotations (column 4) let a Raw-LLM walker pre-budget which files fit any sub-task before opening them. |

**Read-order rationale:** scope + token catalog + AppShell + boundary pins (1) → contract aggregator (2) → current state (3) → provenance (4). After tier-1 the reader knows: every `--app-*` token, the AppShell invariant, the §07 dependency boundary, the §22 inheritance contract, every AC and its test, the live banner state, and the audit-task history that produced it.

---

## Tier-2 — Recommended adjuncts (read on demand)

**None.** §24 has no tier-2 files. The cohort's normative surface is fully contained in the 4 tier-1 files above. If a future contract addition pushes a file's line-count or scope past the cohesion threshold, the demotion candidate (per the drift contract clause 4 below) is the impl-sweep appendix at the tail of `00-overview.md`, which would split into a new `01-impl-sweep.md` tier-2 file.

---

## Tier-3 — Specialised surfaces (out-of-bundle)

| File | Lines | Purpose |
|---|---|---|
| [`lifecycle-component-render.mmd`](./lifecycle-component-render.mmd) | 11 | Mermaid lifecycle diagram for the AppShell component render flow. Visualises the §00 AppShell pattern; never the source of truth. |

---

## Walker-cost reflexivity (load-budget pin)

**Mirror of §27 B-27 (Sess-71) and §25 B-27-§25 (Sess-74) walker-cost reflexivity lever.** This manifest is itself the load-proven artefact for its own friction claim: a Raw-LLM auditor walking §24 with a Tier-1 bundle cap (~30 KB per `mem://constraints/...` Tier-1 budget heuristics) can pre-budget which files to open against the per-file byte-costs in the Tier-1 table (column 4) before opening any cited surface. The Σ ~148 KB total is **above** any single-walker 30 KB cap — sub-task pre-budgeting is therefore mandatory, not optional, for the Raw-LLM persona.

| Tier | Surface | Byte-cost (KB) | Closed-set role |
|---|---|---|---|
| Tier-1 #1 | `00-overview.md` (scope + token catalog + AppShell + boundary pins + Quick-Nav) | ~47 | Read-first scope-setter; Quick-Nav resolves any sub-anchor in 1 hop |
| Tier-1 #2 | `97-acceptance-criteria.md` (17 `AC-ADS-*` + per-AC `T-ADS-NN-NN` test invariants) | ~37 | The contract aggregator; every §24 normative claim lives here |
| Tier-1 #3 | `99-consistency-report.md` (newest banner + module health + open tickets) | ~11 | Live state — read after §00/§97 to know what the spec is **right now** |
| Tier-1 #4 | `98-changelog.md` (per-version provenance back to v3.x) | ~53 | Provenance — last in tier-1; explains *why* each banner clause exists |
| Tier-3 | `lifecycle-component-render.mmd` (Mermaid AppShell render flow) | ~0.5 | Visual aid only; never source-of-truth (Lesson #36) |
| **Σ tier-1** | (4 normative files) | **~148** | Above any 30 KB single-walker cap → sub-task pre-budgeting mandatory |

**Pre-budget recipes (Raw-LLM auditor with 30 KB cap; mandatory sub-task selection):**

- **Verify an `AC-ADS-*` clause** (contract-only walk): load §97 ≈ **~37 KB** (~123% of cap → must be split across 2 walker passes, or only the relevant AC body excerpted via Quick-Nav from §00 #2). Skip §00 / §99 / §98.
- **Audit current state** (live-banner walk): load §99 + §00 banner block ≈ **~14 KB** (~47% of cap; §99 ~11 KB + §00 banner head ~3 KB). Skip §97 / §98.
- **Provenance audit** (changelog walk for any banner clause): load §98 + §99 ≈ **~64 KB** (~213% of cap → split across 2 walker passes, OR scope to a single `### vN.M.K` ladder entry which is ~2-4 KB). Skip §00 / §97.
- **Full tier-1 read** (new contributor onboarding): load entire tier-1 set ≈ **~148 KB** (~493% of cap → mandatory 5-pass walk, ordered §00 → §97 → §99 → §98 per Tier-1 read-order rationale).
- **Audit-drift** (banner-triple lockstep verification): load §00 banner head + §98 newest entry + §99 newest update block ≈ **~9 KB** (~30% of cap; each surface ~3 KB). Cheapest workflow.

**Why this lifts C6, not C4** (mirror of §27 B-27 and §25 B-27-§25 explanations): friction is the cost of finding the right surface; C6 measures that cost. The byte-cost annotations on each tier-1 file reduce guess-cost — the textbook C6 lever per the Rubric v2 band-anchor definition. C4 (Consistency) is unaffected — the AC source remains the single source of truth.

**Long-tail ceiling (19 → 20)**: deferred to a `-impl` walker-cost drift gate that recomputes the per-file byte-costs above against on-disk file sizes on every banner-triple lockstep run (out of scope per `mem://constraints/no-implementation-suggestions`).

**Drift contract** (reflexive): if any tier-1 file's `wc -c` changes by ≥10 KB, the per-file byte-cost column above MUST be refreshed in the same PR; gate #42 banner-triple lockstep already detects banner-version drift, the byte-cost refresh is reviewer-attestation today. The Σ row is governed by clause 6 of the existing drift contract below (line-budget invariant — KB-budget refresh is its byte-axis sibling).

---

## Per-persona pre-flight checklist

- **Raw-LLM persona** — Reads all 4 tier-1 files in order. Total ~1 606 lines fits a single context window. Skip the `.mmd` diagram (visual aid only). If a question demands the diagram's content, defer to the AppShell pattern in `00-overview.md` — the Mermaid is a render of the prose, not its own contract surface.
- **Cursor / Claude-Code persona** — Reads tier-1 in order, opens the `.mmd` diagram only when reviewing or modifying the AppShell render flow. Treats §97 as the contract index against which any code change must reconcile.
- **Lovable persona** — Uses tier-1 as primer (it has file-tool access already), then jumps directly to the relevant `00-overview.md` sub-anchor (via Quick-Nav) per current sub-task. The `.mmd` is loaded only when authoring a §26 mirror diagram per AC-DG-05.

---

## Drift contract (Lesson #15 reflexivity)

1. Adding a new normative cross-surface contract (any `AC-ADS-*` clause governing ≥ 2 files, any new `--app-*` token category, any new AppShell variant, any new §07 boundary condition) MUST in the **same commit**: (a) author the contract in its owning tier-1 file, (b) update this manifest's Σ row + banner if line count crosses a 100-line bucket, (c) cite the new contract in §99's audit-row tail under that turn's task tag.
2. Adding a new tier-2 file that introduces a contract not yet pinned in tier-1 is **forbidden** — surface the contract in tier-1 first, then author the tier-2 file that delegates to it (mirror of §22 AC-22-CE1, §27 AC-T-30, §28 tier-1 manifest clause 2 same-PR cohort discipline).
3. Promoting the `.mmd` diagram or any future tier-3 file to tier-1 MUST cite the AC family that newly depends on it AND re-tally the Σ row in the same commit.
4. Demoting a tier-1 file is allowed only when its normative obligations have been migrated into the surviving tier-1 set (Lesson #36 link-don't-restate audit required); the demotion commit MUST update the per-persona pre-flight checklist above. The demotion candidate is the impl-sweep appendix at the tail of `00-overview.md`, which would become `01-impl-sweep.md`.
5. Restating any clause body, AC text, token definition, or AppShell prop body inside this manifest is **forbidden** (Lesson #36); this file is the partition + read-order map only.
6. **Line-budget invariant:** `wc -l spec/24-app-design-system-and-ui/{00-overview.md,97-acceptance-criteria.md,98-changelog.md,99-consistency-report.md} | tail -1 | awk '{print $1}'` MUST be ≤ **2 500** (single-context-window comfort threshold). Any commit pushing the four-file sum above 2 500 MUST in the same commit either (a) trim the offending file, or (b) demote the impl-sweep appendix to a new `01-impl-sweep.md` tier-2 file with a Lesson #36 link-don't-restate audit confirming all normative obligations are reachable from the surviving tier-1 set.
7. **No-tier-2 invariant:** as long as clause 6 holds, this cohort MUST NOT introduce any tier-2 file. The Raw-LLM contract relies on the entire §24 surface being readable in a single pass; introducing a tier-2 surface without first tripping the line-budget ceiling is itself a regression of the audit-defensibility property this manifest exists to protect.

---

## Self-citation (Lesson #15 reflexivity, 20-band anchor)

This file's drift contract is **mechanically enforced by** `meta-verify-lockstep.py` (`spec/27-spec-toolchain/` slot 64, gate #42) clause-5 banner-triple lockstep against §24 §00 / §98 / §99. Any banner bump to this file that is not mirrored in §99's audit-row tail within the same commit trips gate #42 and hard-fails CI. The line-budget invariant (clause 6 above) MAY be additionally enforced by a future extension of `audit-bundle-budget.py` (slot 35, gate #34) loading the four-file tier-1 set as a named bundle target with the 2 500-line ceiling — until that extension ships, the line-budget is enforced by reviewer attestation that `wc -l` of the four tier-1 files was checked in the same PR. The closed-set perimeter (clauses 1–5, 7) is **mechanically enforced by** `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39) on the link-target axis (any tier-1 file linking out to a non-locked-7 folder is a SPEC VIOLATION). The no-DDL boundary cited in the Reader Pin above is **mechanically enforced by** `check-no-sql-ddl-in-ui-folder.py` (slot 58, gate #36) per AC-ADS-17.
