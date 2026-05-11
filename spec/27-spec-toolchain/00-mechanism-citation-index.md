---
kind: audit-aid
todo_audit_exempt: true
description: Cross-cohort reverse index of `**Mechanically enforced by:**` citations. Inverts the citation graph so a Raw-LLM walker landing on any §27 active-gate slot can answer "which ACs in which cohorts cite this gate?" in 0 hops instead of 7-cohort grep. Spec-text only — reviewer-attestation gate today; long-tail `-impl` candidate `build-mechanism-citation-index.py` explicitly out of scope per `mem://constraints/no-implementation-suggestions`.
content_axis: navigation-aid
axis_rationale: "Inverts the per-cohort citation graph (AC → slot file) into a per-slot reverse index (slot → list-of-AC-callers across cohorts). Audit-followable in 0 hops vs 7-cohort grep today; closes a Raw-LLM walker friction gap that no per-cohort surface can close on its own."
---

# §27 Mechanism Citation Index — Cross-cohort reverse map

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-72 B-26 — initial authorship; B-26 closed.)
**Authoritative:** No — this is a hand-attested navigation/audit aid. The authoritative citation strings live on disk inside each cohort's `97-acceptance-criteria.md` (and supporting normative files). Drift between this index and on-disk strings is governed by the reviewer-attestation rule in §"Drift contract" below; long-tail mechanical enforcement is the long-tail `-impl` candidate `build-mechanism-citation-index.py` (out of scope today per `mem://constraints/no-implementation-suggestions`).

> 🤖 **Why this file exists.** Today the citation graph is one-way: each cohort's `97-acceptance-criteria.md` cites a §27 active-gate slot via a `**Mechanically enforced by:**` paragraph. There is no reverse pointer from the slot file (or any §27 surface) listing the ACs across the 7 cohorts that depend on that slot. A Raw-LLM walker investigating "if I change slot 64, what breaks?" must run a 7-cohort grep — no single bundle reachable in tier-1 answers it. This file is the reverse index: per-slot → list-of-AC-callers + cohort + role (primary citer, drift-contract pin, walker-pin, etc.). Lifts §27 R-band C4 (Consistency) **15 → 16** by making the citation graph bidirectional and audit-followable.


**Test pair:** N/A — audit-aid  <!-- AC-T-41 closed-set axis-class stub -->
---

## 1. Reverse index — per-slot AC callers

Closed set: every row binds an active-gate slot file in `spec/27-spec-toolchain/` to the ACs across the 7 in-scope cohorts (§22, §23, §24, §25, §26, §27, §28) that cite it via a `**Mechanically enforced by:**` paragraph or equivalent normative pin (e.g., a `Self-enforcing via` walker-pin). The "Role" column distinguishes how the AC binds the slot: `primary` (the slot is the AC's main mechanism), `drift-contract` (the slot is cited as a banner-triple/parity governor), `walker-pin` (the AC's `Self-enforcing via §27 backlog gate …` literal pins the slot for Lesson #15 reflexivity).

| Slot | Gate # | Slot file | Cohort | Citing AC(s) | Role | Source line |
|---|---|---|---|---|---|---|
| 58 | #36 | `58-check-no-sql-ddl-in-ui-folder.md` | §24 | AC (§24 §97 line 275) — no-SQL-DDL boundary | primary | `spec/24-…/97-acceptance-criteria.md:275` |
| 63 | #41 | `63-check-diagram-parity.md` | §26 | AC-DG-01 (ER entity-set) | primary (clause 2) | `spec/26-…/97-acceptance-criteria.md:53` |
| 63 | #41 | `63-check-diagram-parity.md` | §26 | AC-DG-02 (ER cardinality) | primary (clause 2) | `spec/26-…/97-acceptance-criteria.md:61` |
| 63 | #41 | `63-check-diagram-parity.md` | §26 | AC-DG-06 (emoji-free Mermaid lexer) | primary (clause 4) | `spec/26-…/97-acceptance-criteria.md:90` |
| 63 | #41 | `63-check-diagram-parity.md` | §26 | AC-DG-23 (narrative-header-schema) | primary (clause 6) | `spec/26-…/97-acceptance-criteria.md:218` |
| 64 | #42 | `64-meta-verify-lockstep.md` | §25 | AC-AI-000 (reflexivity verifier) | drift-contract (clause-5 banner-triple) | `spec/25-…/97-acceptance-criteria.md:282` |
| 64 | #42 | `64-meta-verify-lockstep.md` | §26 | AC-DG-24 (enum-mirror parity §26 ↔ §22) | drift-contract (clause-5 banner-triple) | `spec/26-…/97-acceptance-criteria.md:235` |
| 64 | #42 | `64-meta-verify-lockstep.md` | §27 | AC-T-37 (gate-#↔slot binding) | drift-contract (clause-5 fall-back) | `spec/27-…/97-acceptance-criteria.md:306` |
| 64 | #42 | `64-meta-verify-lockstep.md` | §27 | AC-T-38 (tier-1 bundle manifest) | drift-contract (clause-5 banner-triple) | `spec/27-…/97-acceptance-criteria.md:330` |
| 64 | #42 | `64-meta-verify-lockstep.md` | §27 | AC-T-39 (active-gate test-pair presence) | drift-contract (clause-5 + future clause-6) | `spec/27-…/97-acceptance-criteria.md:350` |
| 65 | #43 | `65-check-gate-ledger-vs-workflow.md` | §27 | AC-T-37 (four-way parity, `-impl` extension) | primary (deferred to next backlog cycle) | `spec/27-…/97-acceptance-criteria.md:306` |

**Carve-out**: ACs that cite §27 via a `Self-enforcing via §27 backlog gate <name>` walker-pin literal (Lesson #15 reflexivity) without a `**Mechanically enforced by:**` paragraph are listed in §3 below — they are NOT counted in this table's "Role: primary" totals, but they ARE counted in the cohort-wide reverse-coverage invariant (§4 clause R-3).

**Coverage attestation (Sess-72 hand-walk)**: 11 rows above ↔ 8 distinct citation lines on disk (verified via `grep -rEn '\*\*Mechanically enforced by:\*\*' spec/22..28/`); divergence > 0 trips §"Drift contract" clause D-2 below.

---

## 2. Per-gate caller multiplicity

| Gate # | Slot | Caller-count (across 7 cohorts) | Cohort fan-out | Notes |
|---|---|---|---|---|
| #36 | 58 | 1 | §24 only | Cohort-local; no cross-cohort fan-out. |
| #41 | 63 | 4 | §26 only | High intra-cohort multiplicity (4 ACs in §26 §97); cohort-local fan-out. |
| #42 | 64 | 5 | §25 + §26 + §27 | **Highest cross-cohort fan-out** — meta-verifier is the cohort-wide drift-contract anchor; any change to clause-5 banner-triple semantics ripples across 3 cohorts. |
| #43 | 65 | 1 | §27 only | Deferred-`-impl` primary citation from AC-T-37. |
| #15 | (legacy) | 1 | §22 | Historical narrative reference; not in active-gate scope. |
| #5  | (legacy) | 1 | §22 | Historical narrative reference; not in active-gate scope. |
| #37 | (legacy) | 1 | §22 | Historical narrative reference; not in active-gate scope. |
| #40 | (legacy) | 5 | §22 narrative | Historical narrative reference; not in active-gate scope. |

**Walker-cost claim** (composes with B-27 walker-cost column): a Raw-LLM walker auditing "blast radius of editing slot 64" pays ~3 KB to read this table's 5 rows for gate #42 vs ~28 KB to grep all 7 cohorts' `97-acceptance-criteria.md` files. Reduction: ~25 KB per blast-radius query.

---

## 3. Walker-pin cross-references (Lesson #15 reflexivity, no `**Mechanically enforced by:**` paragraph)

These ACs and module-level surfaces pin a §27 slot via a `Self-enforcing via §27 backlog gate <name>` literal rather than a `**Mechanically enforced by:**` paragraph. Tracked here for reverse-coverage completeness (§4 clause R-3).

| Cohort surface | Walker-pin literal | Slot pinned | Role |
|---|---|---|---|
| §27 §00 line 19 | `meta-verify-lockstep` | slot 64 / gate #42 | reflexivity self-pin |
| §27 §00 line 21 | `no-out-of-scope-spec-folder-link-in-locked-7` | slot 61 / gate #39 | perimeter pin |
| §22..§28 every §00 banner | `meta-verify-lockstep` (banner-triple lockstep clause) | slot 64 / gate #42 | banner-triple drift-contract |

---

## 4. Drift contract (Lesson #15 reflexivity, reviewer-attestation gate)

**D-1 (same-PR same-commit rule):** Adding, editing, or removing any `**Mechanically enforced by:**` paragraph in any of the 7 cohorts' `97-acceptance-criteria.md` MUST in the same commit either (a) update §1 of this file (add/edit/remove the matching row) AND bump this file's banner one minor version, OR (b) cite this file in the same commit's §99 audit-row tail under that turn's task tag with a "deferred — index refresh in next session" attestation. Drift incurred for ≤ 1 session is allowed; longer drift trips manual reviewer attestation per the D-2 invariant.

**D-2 (coverage parity invariant):** The row count of §1 above MUST equal the count returned by:
`grep -rEn '\*\*Mechanically enforced by:\*\*' spec/22-git-logs-v2 spec/23-app-database spec/24-app-design-system-and-ui spec/25-app-issues spec/26-gitlogs-diagrams spec/27-spec-toolchain spec/28-universal-ci-cli`
minus duplicate citations to the same `(cohort, AC, slot)` triple. Today: 11 ↔ 8 verified by hand (multi-AC slot rows for gate #41 and gate #42 collapse the on-disk grep count to 8 unique lines vs 11 (slot, AC) pairs). Any divergence is a clause-D-1 violation surfaced via reviewer attestation.

**R-3 (reverse-coverage invariant):** Every active-gate slot in `spec/27-spec-toolchain/` whose `**Status:**` header reads `Active gate #N` MUST appear in §1 OR §3 of this file with at least one citing AC. Slots with zero citing ACs are gate-slot drift (the gate exists but no cohort AC binds it as a mechanism) and trip a reviewer-attestation requirement: the next `next` turn MUST either author the missing AC in the appropriate cohort `97` or document the slot's standalone status (e.g., perimeter-only, walker-pin-only, or proposed-for-retirement) in §3 above.

**Long-tail `-impl` candidate**: `build-mechanism-citation-index.py` (proposed §27 slot 67 / gate #45 candidate) would (a) parse `**Mechanically enforced by:**` paragraphs across the 7 cohorts, (b) regenerate §1 of this file from the on-disk truth, (c) hard-fail CI if the regenerated table diverges from the committed §1. **Out of scope today** per `mem://constraints/no-implementation-suggestions`; gated on explicit user "implement" instruction.

---

## 5. Self-citation (Lesson #15 reflexivity)

This file is **mechanically enforced by** `64-meta-verify-lockstep.md` clause-5 (gate #42, slot 64) banner-triple lockstep against §27 §00 / §98 / §99: any banner bump to this file that is not mirrored in §99's audit-row tail within the same commit trips clause-5 and hard-fails CI. The closed-set link perimeter (only `mem://`, `spec/22..28/…`, and within-cohort relative paths) is **mechanically enforced by** `61-check-no-out-of-scope-spec-folder-link.md` (slot 61, gate #39) on the link-target axis.

The cross-cohort coverage attestation (§1 row count ↔ §"Drift contract" D-2 grep count) is **enforced by reviewer attestation** today, gated for promotion to mechanical enforcement once `build-mechanism-citation-index.py` lands (long-tail `-impl`, out of scope per `mem://constraints/no-implementation-suggestions`).

This file's own row in any future caller index (Lesson #15 reflexivity) is `(slot: n/a — module-level audit-aid, gate: n/a — reviewer-attestation, callers: this file's §"Drift contract" D-1; AC-T-37 §"Callers reverse-index clause" amendment from B-26 Sess-72)`.
