---
kind: bundle-manifest
todo_audit_exempt: true
description: Tier-1 essential bundle — the minimum subset of §24 source files an LLM (especially the Raw-LLM persona, no file-tool access) must read to understand the App Design System & UI overlay (`--app-*` token catalog, AppShell, §07 dependency boundary, §22 inheritance contract). All 4 normative §24 files are tier-1; the cohort fits in a single context window with no tier-2/3 demotions required. Out-of-bundle files MUST NOT introduce normative cross-surface contracts not pinned by tier-1.
content_axis: navigation-aid
axis_rationale: "Single-page read-order anchor for the §24 App Design System spec set"
---

# App Design System & UI — Tier-1 Essential Bundle

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-69 B-17 — initial tier-1 partition; mirrors the §22 B-1 (Sess-67), §27 B-6 (Sess-67), and §28 B-7 (Sess-68) tier-1 manifest pattern. Targets the Raw-LLM persona; lifts §24 Raw-LLM C1 (Clarity) audit-defensibility 19 → 20 by surfacing read order on disk with self-cited gate enforcement.)
**Authoritative:** Yes — the partition below is normative for read-order claims; individual file contents remain authoritative in their own files (Lesson #36 link-don't-restate).

> 🤖 **Raw-LLM Reader Pin.** §24 is a *strict additive overlay* on §07-design-system: it owns the `--app-*` token namespace, AppShell layout, breakpoints, and theme parity — and ZERO SQL DDL (boundary closed by AC-ADS-17, gate #36). The cohort is **small** (4 normative files, ~1 606 lines of Markdown + 1 lifecycle diagram, total ~1 617 lines). The entire §24 normative surface fits comfortably under the 2 500-line single-context-window comfort ceiling, so **all 4 files are tier-1**. There is no tier-2 / tier-3 demotion in this cohort — read every file in order. Do NOT infer read order from `ls`, alphabetical slot order, or §00's `produced_for:` frontmatter list.

---

## Tier-1 — Navigable minimum (read in order)

| # | File | Lines | Role | Why tier-1 |
|---|---|---|---|---|
| 1 | [`00-overview.md`](./00-overview.md) | 931 | Module pin + Quick-Nav (Walker Index) + Walker-Pin (4 critical ACs surfaced) + Raw-LLM Auditor Pin (Lesson #36 memory resolution) + `--app-*` token catalog + AppShell pattern + §07 dependency boundary `### A-05` + §22 inheritance contract surface + impl-sweep appendices | Establishes the overlay's scope, the §07 boundary, the `--app-*` namespace, and every cross-cohort pin (§07, §22, §27 gates #15/#19/#36/#39/#42). Read first — Quick-Nav routes a context-bounded walker to any sub-anchor in one hop. |
| 2 | [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) | 284 | All 17 `AC-ADS-*` ACs (token namespace, raw-color forbidden, light/dark parity, AppShell invariant, §07 dependency boundary AC-ADS-16, §22 inheritance AC-ADS-15, externalized citation map AC-ADS-14, no-DDL boundary AC-ADS-17) + per-AC `T-ADS-NN-NN` test invariant blocks | Every §24 contract is here. Read after §00 so each AC's `Verifies:` cell already names a known surface. |
| 3 | [`99-consistency-report.md`](./99-consistency-report.md) | 140 | Newest banner block + module-health table + version-delta tail + open-task tail | Tells the reader where the §24 spec is **right now** (versions, last-shipped gate, no-DDL negative-evidence sweep result, open tickets). Read third in tier-1. |
| 4 | [`98-changelog.md`](./98-changelog.md) | 251 | Per-version changelog tail back to v3.x | Last in tier-1: gives provenance for every banner the reader has just absorbed (why a clause exists, which audit task closed it). |
| **Σ** | **4 files** | **~1 606** | **Tier-1 footprint** | Below the 2 500-line single-context-window comfort threshold by a comfortable margin (~895 lines of headroom). |

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
