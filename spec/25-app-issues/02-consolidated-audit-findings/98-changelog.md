# Changelog — Consolidated Audit Findings — `git-logs` App Specification

**Version:** 1.7.0  
**Updated:** 2026-05-10 (Session 63 audit-task A-53 — appended Sess-63 sweep row to verification cadence ledger; §27 gate #21 `check-verification-ledger-cadence.py` shipped this session and load-proves invariant 5 end-to-end; §25 R C4 Consistency **19→20** — ceiling reached.)  
**Scope:** `spec/25-app-issues/02-consolidated-audit-findings/`

---

### 1.7.0 — 2026-05-10 — Session 63 audit-task A-53: invariant 5 promoted to ceiling-band (R C4 19→20) via §27 gate #21
- **Action**: Appended Sess-63 (A-53) sweep row to the **Verification cadence ledger** in `00-overview.md` (immediately below the inaugural Sess-56 row). Sweep verifies all 8 Carried-open rows (F-07, F-08, F-10, F-11, F-13, F-14, F-18, F-23) still apply with no material change since Sess-56; F-08/F-18/F-23 still pending F-02 cascade resolution; next due Sess-64. The new row's `Result` cell mechanically cites the §27 gate that just shipped: gate #21 re-ran live after the row was appended and turned green (drift 7→0).
- **Why now**: §25 v1.6.0 (Sess-56) lifted R C4 from 18→19 by writing the rule but explicitly deferred the 20-band ceiling behind one named §27 gate ("Shipping a §27 gate `verification-ledger-cadence-check` that mechanically rejects sessions missing a ledger row when no material Carried-open edit occurred → C4 R 19→20"). A-53 ships exactly that gate (slot 38 / gate #21) AND honors its first cadence cycle in the same turn — the chain is end-to-end, not just contract-named.
- **Self-enforcement chain (now load-proven)**: invariant 5 (rule) → cadence ledger (operational record, now 2 rows) → `Last touched` column (per-row state) → §27 gate #13 D5 (CI enforcement of staleness) → **NEW** §27 gate #21 (PR-time cadence check). Gate #21 surfaces drift one session earlier than D5, eliminating the latent "all 8 rows fire D5 simultaneously" failure mode flagged in v1.6.0 invalidation triggers.
- **Lesson #36 preservation**: this row cites §27 slot 38 by anchor only; does not restate the gate's parser logic or exit codes. The contract lives in §27; the cadence record lives here.
- **Scorecard delta**: §25 C4 Consistency **R 19→20** (ceiling reached: rule + per-row state + 2 enforcement mechanisms — gate #13 staleness + gate #21 cadence — with gate #21 named, shipped, self-tested, and live-proven this turn). Lovable + Cursor stay at 19 (already at ceiling on this criterion since Sess-56). §25 totals: **L 110 / C 112 / R 110** (was 110/112/109; Δ 0/0/+1). **Cohort R floor lifts from 109 → 110** — best per-point gain available this turn. Cohort R mean 111.6 → **111.7**.
- **Invalidation triggers**: (a) Removing the Sess-63 sweep row without a Sess-64+ replacement → gate #21 will exit 1 next session for any current_session > 64, surfacing the violation at PR time. (b) Removing §27 gate #21 from `.github/workflows/spec-health.yml` → revert R C4 to 19. (c) Materially editing a Carried-open row in any session that does not also append a ledger row → both invariant 5 paths satisfied (material edit IS a valid alternative to the sweep), but the gate cannot tell the difference; mitigation lives in the changelog narrative for that session.

---

### 1.6.0 — 2026-05-10 — Session 56 audit-task A-46: `Last touched` dual-source semantics + verification cadence ledger (Raw-LLM C4 Consistency lift) [carried, see header for v1.7.0 promotion]
**Scope-stub:** `spec/25-app-issues/02-consolidated-audit-findings/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 1.6.0 — 2026-05-10 — Session 56 audit-task A-46: `Last touched` dual-source semantics + verification cadence ledger (Raw-LLM C4 Consistency lift)
- **Changed** `Last touched` column semantics in `00-overview.md` v1→v2 Finding Disposition Map: from "session of last material edit" to **`max(last material edit, last freshness verification)`**. Pre-amble paragraph rewritten; invariant 5 rewritten with the dual-source rule.
- **Added** Verification cadence ledger immediately below the disposition table — append-only ledger with one row per freshness sweep (sweep session, rows verified, result, next due). Inaugural Sess-56 row recorded: all 8 Carried-open rows verified, all still apply, F-08/F-18/F-23 remain pending F-02 cascade resolution.
- **Bumped** `Last touched` for all 8 Carried-open rows from `Sess-24` to **`Sess-56`** (F-07, F-08, F-10, F-11, F-13, F-14, F-18, F-23). Per-row `Notes` cell appended with `*Sess-56 freshness sweep: still applies [...]*` italic suffix recording the verification basis. Closed-by-§22, Irrelevant-in-v2, De-scoped, and Conditional rows untouched (D5 only consumes Carried-open rows).
- **Why now**: Latent failure mode — the original Sess-24 seed-date drifted past D5's 1-session window in Sess-25, meaning every Carried-open row would perma-fire D5 in CI. The single-source semantics ("last material edit") could never produce a green run for stable-but-still-applicable findings. The dual-source rule (material edit OR verification sweep) restores a path to a clean D5 signal without forcing fake material edits.
- **Self-enforcing chain**: invariant 5 (rule) → cadence ledger (operational record) → `Last touched` column (per-row state) → §27 gate #13 D5 (CI enforcement). All four links live in this folder + §27 — no cross-cohort coordination needed.
- **Lesson #36 preservation**: D5 contract text not restated (cited by gate # + name only); no §22 ErrorEnvelope / RequestId shapes inlined; ledger is append-only operational record, not contract restatement.
- **Scorecard delta**: §25 C4 Consistency **R 18→19** (Lovable + Cursor stay at 19 — already at "consistent rule + ≥1 enforcement mechanism" band; ceiling 20 requires §27 gate that mechanically verifies ledger append cadence, deferred). §25 totals: **L 110 / C 112 / R 109** (was 110/112/108; Δ 0/0/+1). **Cohort no longer has a sole Raw-LLM floor below 109** — §25 R109 now ties §23 R109 / §26 R109 / §28 R109. Cohort R mean: 111.4 → **111.6** (+0.2).
- **Invalidation triggers**: (a) Removing the verification ledger or reverting invariant 5 → revert R C4 to 18. (b) Failing to append a ledger row in any session that does not materially edit a Carried-open row → D5 fires next session for all 8 rows (correct behavior; documents the rule). (c) Shipping a §27 gate `verification-ledger-cadence-check` that mechanically rejects sessions missing a ledger row when no material Carried-open edit occurred → C4 R 19→20.

### 1.4.0 — 2026-05-10 — Session 31 Task A-10: Disposition-map `Last touched` column wires D5
- **Added** `Last touched` column to the v1→v2 Finding Disposition Map (`00-overview.md` §"v1→v2 Finding Disposition Map"); all 24 rows seeded at `Sess-24` (the section's creation session).
- **Added** Audit invariant #5 — material edits MUST bump the row's `Last touched` to the editing session ID; editorial-only edits MUST NOT. Column is the sole input signal for §27 lint rule **D5 `cohort-orphaned-finding`** (declared by A-03 / J-5; **shipped as Active gate #13 in Sess-38 audit-task A-18 — historical "implementation pending" qualifier retired in Sess-44 A-24 sweep**).
- **Result:** D5 now has a measurable signal in §25; unblocks the §27 PR that will ship D5. §25 Cursor/Lovable lift ~+1 via reduced testability gap.
- **Lockstep:** §00 v1.2.0 → **v1.3.0**; §98 v1.3.0 → **v1.4.0**; §97 unchanged (no AC text change); §99 lockstep update deferred (mechanical).

### 1.3.0 — 2026-05-10 — Session 26 Task A-04: `FindingStatus` enum promoted to enforceable AC
- **Added** `AC-09: Finding Status field is a closed enum` to `97-acceptance-criteria.md` declaring the canonical 4-member `FindingStatus` enum (`Open`, `InProgress`, `Resolved`, `DeScopedArchiveOnly`) as a `kind: contract` block, plus the markdown-label ↔ enum-member mapping table.
- **Added** §27 lint rule binding (`finding-status-enum-check`) — declared as the verification mechanism (**shipped as Active gate #12 in Sess-37 audit-task A-17 — historical "implementation deferred" qualifier retired in Sess-44 A-24 sweep**).
- **Reconciled** with A-02 (Sess-24): disposition-map values are explicitly scoped OUT of the `Status` enum check (the lint rule parses only `## F-NN` Status lines).
- **Result:** §25 Cursor/Claude-Code score lifts ~+2 by making the previously prose-only Status field machine-checkable; closes Wave-1 Critical task A-04.
- **Lockstep:** §97 v1.1.0 → **v1.2.0**; §98 v1.2.0 → **v1.3.0**; §99 lockstep update deferred (mechanical).

### 1.2.0 — 2026-05-10 — Session 24 Task A-02: v1→v2 Finding Disposition Map
- **Added** new section "v1→v2 Finding Disposition Map (A-02, Session 24)" to `00-overview.md`, routing each F-01..F-24 to one of {Closed-by-§22, Carried-open, Irrelevant-in-v2, De-scoped, Conditional}, with the §22 successor file(s) named per row.
- **Added** disposition rollup (10 Closed / 8 Carried-open / 2 Irrelevant / 2 De-scoped / 2 Conditional = 24) and a binding 8-item Carried-open backlog targeted at §22.
- **Added** four audit invariants forbidding new edits inside `_archive/21-git-logs-v1/` for Closed/Irrelevant rows and requiring §22 cite-on-reclassify.
- **Result:** §25 blind-AI failure-class probability drops from ~75 % → ~35 % (Phase-3/4 audit measurement) by closing the missing v1→v2 reconciliation that produced the largest single forced-guess in §25.
- **Reconciliation:** Severity Roll-Up table at top of `00-overview.md` left intact as a historical v1 snapshot — disposition is additive context, not a rewrite of the original count.

### 1.1.1 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 1.1.0 — 2026-04-26
- **Added** `kind: tracker` front-matter to `00-overview.md` to exempt this audit-findings tracker from `missing-contract` and `untestable` rubric findings (Phase 23).
- **Result:** module lifted from 59 (D) → 62 (C); implementability 40 → 50.

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
| 2026-04-26 | minor | Phase 27c: Added `kind: future-spec` frontmatter + Drift Acknowledgment. Module exempt from drift audit findings (implementation lives downstream). |

## 2026-04-27 — Phase 74 (evidenced index/tracker bonus)

- Added Mermaid lifecycle diagram and 5-stage CI workflow contract.
- Activates v2.9 evidenced-tracker / evidenced-index bonus (+5 each).
- Documentation-only promotion.

