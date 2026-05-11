---
kind: bundle-manifest
todo_audit_exempt: true
description: Tier-1 essential bundle — the minimum subset of §23 source files an LLM (especially the Raw-LLM persona, no file-tool access) must read to implement the App-database surface (App / AppLink / AppStatus / AppLinkType tables + AppLink polymorphic resolution). All other §23 files are tier-3 (changelog archaeology). Out-of-bundle files MUST NOT introduce normative cross-surface contracts not pinned by tier-1 — drift = §23 §99 next consistency report row.
content_axis: navigation-aid
axis_rationale: "Single-page read-order anchor for the §23 spec set"
---

# App Database — Tier-1 Essential Bundle

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-78 B-27-§23 — initial tier-1 partition + walker-cost reflexivity in the same turn (mirror-sextet step 6/7); mirrors the §22 B-1 (Sess-67), §27 B-6 (Sess-67), §28 B-7 (Sess-68) tier-1 manifest pattern AND the §27 B-27 (Sess-71) / §25 B-27-§25 (Sess-74) / §24 B-27-§24 (Sess-75) / §22 B-27-§22 (Sess-76) / §28 B-27-§28 (Sess-77) walker-cost reflexivity lever. §23 has only 4 normative md files (small cohort), so the partition is degenerate: Tier-1 = §00 + §97 + §99 (3 files, ~107 KB / ~1 600 lines); Tier-3 = §98 changelog only. No tier-2 layer needed at this scale. Adds: (a) per-file **Walker-cost (KB)** column to the Tier-1 table; (b) **§ "Walker-cost reflexivity (load-budget pin)"** section with closed-set per-tier byte-cost table and 3 pre-budget recipes (verify-an-AC ~47 KB / decode-current-state ~74 KB / full-tier-1 read ~107 KB) plus reflexive drift contract. Lesson #15 reflexivity: this manifest IS the load-proven artefact for its own friction claim. **Mirror-sextet anchored**: §22 + §24 + §25 + §27 + §28 + §23 = 6 of 7 cohorts cite walker-cost reflexivity (only §26 remaining). **Pure navigation-aid surface**; no §97 AC body edits, no new gate. Same-PR banner-triple lockstep (§00 / §98 / §99). Lifts §23 R-band C6 (Friction) +1 → 19 (cited mechanism: tier-1 partition surfaces read order on disk + walker-cost reflexivity column makes byte-cost guess-cost zero); cumulative §23 R-band 118 → 119/120. C1/C2/C3/C4/C5/C6 @ 20/19/19/18/20/19 after this turn. **Lovable + Cursor unchanged at 120 ceiling**. Aggregate Raw-LLM Σ 818 → 819/840 (97.5/100). Closes B-27-§23.)
**Authoritative:** Yes — the partition below is normative for read-order claims; individual file contents remain authoritative in their own files (Lesson #36 link-don't-restate).

> 🤖 **Raw-LLM Reader Pin.** §23 is a small cohort (4 normative files, ~1 800 lines). Read tier-1 in order; do NOT infer read order from `ls` or alphabetical slot order. Tier-1 footprint = ~1 600 lines (well under the 2 500-line single-context-window comfort ceiling). Tier-3 (`98-changelog.md`) is changelog archaeology only — load on demand for version-history questions.

---

## Tier-1 — Implementable minimum (read in order)

| # | File | Lines | Walker-cost (KB) | Role | Why tier-1 |
|---|---|---|---|---|---|
| 1 | [`00-overview.md`](./00-overview.md) | 1 205 | ~60 | Module pin + `consumes:` cross-cohort frontmatter (§22 anchors) + R-1..R-09 query/contract matrix + Settings-persistence DDL + AppLink polymorphic resolution rules | The contract aggregator. Establishes vocabulary (App / AppLink / AppStatus / AppLinkType), R-1..R-09 query templates, and the §24 ↔ §23 settings-storage join. Read first. |
| 2 | [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) | 264 | ~33 | All `AC-ADB-*` ACs (REST + WE + SETTING families) | Every §23-side normative contract is here or inline-cited from §00. Read after §00 so each AC's `Verifies:` cell already names a known surface. |
| 3 | [`99-consistency-report.md`](./99-consistency-report.md) | 131 | ~14 | Newest banner block + version delta tail + open-task tail | Tells the reader where the §23 spec is **right now** (versions, last-shipped contract, open tickets). Read last in tier-1. |
| **Σ** | **3 files** | **~1 600** | **~107** | **Tier-1 footprint** | Below the 2 500-line single-context-window comfort threshold. |

**Read-order rationale:** vocabulary + contracts (1) → AC aggregator (2) → current state (3). After tier-1 the reader knows: every App-database table, every R-1..R-09 query template, every `AC-ADB-*` clause, and the cohort's current spec-version frontier.

---

## Tier-3 — Specialised surfaces (out-of-bundle)

These files exist for completeness but are not required for any persona to understand the §23 contract.

| File | Lines | Purpose |
|---|---|---|
| [`98-changelog.md`](./98-changelog.md) | 223 | Per-version changelog tail. Use only when archaeology is required (e.g., "when did `AC-ADB-SETTING-01` ship?"). |
| [`lifecycle-app-link-resolution.mmd`](./lifecycle-app-link-resolution.mmd) | (mermaid) | Mermaid lifecycle diagram for AppLink polymorphic resolution. Visualises §00 R-1..R-04; never the source of truth. |

---

## Walker-cost reflexivity (load-budget pin)

**Mirror of §27 B-27 (Sess-71), §25 B-27-§25 (Sess-74), §24 B-27-§24 (Sess-75), §22 B-27-§22 (Sess-76), and §28 B-27-§28 (Sess-77) walker-cost reflexivity lever.** This manifest is itself the load-proven artefact for its own friction claim: a Raw-LLM auditor walking §23 with a Tier-1 bundle cap (~30 KB per `mem://constraints/...` Tier-1 budget heuristics) can pre-budget which files to open against the per-file byte-costs in the Tier-1 table (column 4) before opening any cited surface. The Σ ~107 KB total is **far above** any single-walker 30 KB cap — sub-task pre-budgeting is therefore mandatory, not optional, for the Raw-LLM persona.

| Tier | Files | Σ KB | Role |
|---|---|---|---|
| Tier-1 #1 | `00-overview.md` | ~60 | Contract aggregator — ~200% of cap → mandatory 2-pass walk on its own |
| Tier-1 #2 | `97-acceptance-criteria.md` | ~33 | AC aggregator — ~110% of cap → 2-pass walk (single pass with overflow) |
| Tier-1 #3 | `99-consistency-report.md` | ~14 | Current-state tail — fits one walker pass alone with 16 KB headroom |
| **Σ tier-1** | **(3 normative files)** | **~107** | **~357% of cap → mandatory 4-pass walk, ordered §00 → §97 → §99 per Tier-1 read-order rationale** |

**Pre-budget recipes** (closed set, mirror of §27 + §25 + §24 + §22 + §28):

- **Verify-an-AC** (auditor confirming a single `AC-ADB-*` clause): load Tier-1 #1 (header + cited section only; ~14 KB worst-case sub-slice via section anchor) + #2 ≈ **~47 KB** (~157% of cap → 2-pass walk; AC body in §97 + the §00 contract section it `Verifies:`).
- **Decode-current-state** (auditor checking spec-version frontier or open tickets): load Tier-1 #1 + #3 ≈ **~74 KB** (~247% of cap → mandatory 3-pass walk; §00 banner + §99 version delta + open-task tail).
- **Full tier-1 read** (new contributor onboarding): load entire tier-1 set ≈ **~107 KB** (~357% of cap → mandatory 4-pass walk, ordered §00 → §97 → §99 per Tier-1 read-order rationale).

**Why this lifts C6, not C4** (mirror of all prior B-27-§N explanations): friction is the cost of finding the right surface; C6 measures that cost. The byte-cost annotations on each tier-1 file reduce guess-cost — the textbook C6 lever per the Rubric v2 band-anchor definition. C4 (Consistency) is unaffected — the AC source remains the single source of truth.

**§23-specific note:** §23 is the smallest in-scope cohort (4 normative files); the §00 contract aggregator dominates byte-cost (~56% of tier-1). The "verify-an-AC" recipe is the highest-frequency Raw-LLM walk and benefits most from sub-section anchoring within §00 (the contract aggregator is large enough that a section-anchor walk is a meaningful sub-budget).

**Long-tail ceiling (19 → 19 reflexive defensibility)**: this turn lifts §23 C6 from 18 → 19 (the partition + reflexivity column adds two new cited mechanisms simultaneously). C6 → 20 would require a third cited mechanism (e.g., `meta-verify-lockstep.py` clause-5 banner-triple lockstep extension to this manifest, mirroring the §27/§28 self-citation block) — out of scope this turn per `mem://constraints/no-implementation-suggestions` (gate-extension is implementation-side).

**Drift contract** (reflexive): if any tier-1 file's `wc -c` changes by ≥10 KB, the per-file byte-cost column above MUST be refreshed in the same PR. Reviewer-attestation today; gate #42 banner-triple lockstep already detects banner-version drift on §00 / §98 / §99 (this manifest's banner is bumped manually in the same PR). The Σ row is governed by the line-budget invariant in the drift contract below.

---

## Per-persona pre-flight checklist

- **Raw-LLM persona** — Stops after file 3 (`99-consistency-report.md`). Tier-3 is out of context-window reach for routine work. If a question demands changelog archaeology, the answer is "tier-3 file `98-changelog.md` would resolve this — please load it" and stop.
- **Cursor / Claude-Code persona** — Reads tier-1 in order; loads §98 on demand for archaeology. The 4-file cohort is small enough that a full read is feasible if needed.
- **Lovable persona** — Uses tier-1 as primer (it has file-tool access already), then jumps directly to §00's section anchors per current sub-task. Treats §97 as the AC index against which any code change must reconcile.

---

## Drift contract (Lesson #15 reflexivity)

1. Adding a new normative cross-surface contract (any new `AC-ADB-*` AC, any new R-NN row, any new DDL block) MUST in the **same commit**: (a) author the contract in its owning tier-1 file (§00 or §97), (b) update this manifest's Σ row + banner if line count crosses a 100-line bucket, (c) cite the new contract in §99's audit-row tail under that turn's task tag.
2. Promoting `98-changelog.md` to tier-1 is forbidden by precedent (changelogs are archaeology, not contracts; mirror of §22/§27/§28 partition).
3. Restating any clause body, R-NN query template, or AC body inside this manifest is **forbidden** (Lesson #36); this file is the partition + read-order map only.
4. **Line-budget invariant:** `wc -l spec/23-app-database/{00-overview.md,97-acceptance-criteria.md,99-consistency-report.md} | tail -1 | awk '{print $1}'` MUST be ≤ **2 500** (single-context-window comfort threshold). Any commit pushing the three-file sum above 2 500 MUST in the same commit either (a) trim the offending file, or (b) split a tier-1 file into a new tier-2 layer with a Lesson #36 link-don't-restate audit confirming all normative obligations are reachable from the surviving tier-1 set.
5. **Walker-cost drift contract** (reflexive, mirror of §22/§24/§25/§27/§28): any tier-1 file `wc -c` change ≥10 KB MUST trigger a same-PR refresh of the Walker-cost (KB) column in the Tier-1 table above.

---

## Self-citation (Lesson #15 reflexivity, mirror-sextet anchor)

This file's drift contract is enforced by `meta-verify-lockstep.py` (`spec/27-spec-toolchain/` slot 64, gate #42) clause-5 banner-triple lockstep against §23 §00 / §98 / §99 — any banner bump to this file that is not mirrored in §99's audit-row tail within the same commit trips gate #42 and hard-fails CI. The line-budget invariant (clause 4 above) is reviewer-attestation today; the walker-cost drift contract (clause 5 above) is reviewer-attestation today (same gate-extension target as §22/§24/§25/§27/§28's walker-cost reflexivity blocks). The closed-set perimeter is enforced by `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39) on the link-target axis.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [§22 §97 AC-23](../22-git-logs-v2/97-acceptance-criteria.md) — schema-drift gate (A-07 cross-flag)
- [§22 §02 database schema](../22-git-logs-v2/02-database-schema.md) — ER baseline + ShaRegistry split-DB boundary
- [§24 settings surface](../24-app-design-system-and-ui/00-overview.md) — downstream consumer of tier-1 file 1's Settings-persistence DDL block
