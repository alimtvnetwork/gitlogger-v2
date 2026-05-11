---
kind: audit-aid
todo_audit_exempt: true
description: Per-criterion Raw-LLM bottleneck decomposition for §27 (Raw-LLM 94/120 vs Lovable/Cursor 120/120). Hand-scored per Rubric v2; identifies which criteria sit at 18-20 ceiling, which are mid-band candidates for next-batch lift, and which are structural floors requiring cross-cohort coordination. Spec-text only — no implementation, no script changes. Drives task selection for B-19..B-2N.
content_axis: navigation-aid
axis_rationale: "Decomposes a single-folder Raw-LLM gap into per-criterion lift roadmap so subsequent batch tasks are targeted, not speculative."
---

# §27 Raw-LLM Bottleneck Decomposition

**Version:** 1.6.0
**Updated:** 2026-05-11 (Sess-70 B-26 — decomposition refresh: all 5 prior spec-only lift candidates (B-19/B-19b/B-20/B-21/B-22) now landed or have spec-text fully authored with only `-impl` turns deferred per `mem://constraints/no-implementation-suggestions`. The remaining 14-point R-band gap (R 106 → 120) needs **new** spec-only levers. Adds 3 new candidates **B-26 / B-27 / B-28** below — each lifts a different criterion via spec-text only (no script, no workflow, no slot-count change). Aggregate spec-only projection if all three land: 106 → ~110 (~29 % residual-gap closure). Remaining ~10 R-points are structurally `-impl`-gated (B-16-impl + B-20-impl + B-22-impl) plus one long-tail cross-cohort gate proposal documented under B-26.)
**Updated-prev:** 2026-05-11 (Sess-69 B-22 same-PR refresh — C6 14 → 15, C4 14 → 15; Σ R-band 104 → 106; B-22 spec-only authored, impl deferred.)
**Authoritative:** No — this is a hand-scored navigation/audit aid. The authoritative scorecard ritual lives in `mem://preferences/scorecard-ritual` and is rendered per session. Per-criterion scores below are this turn's hand-attestation, subject to revision as new mechanisms ship.

> 🤖 **Why this file exists.** After Sess-68 B-8 closed the §27 navigation-quintet, §27 reached **C1=20, C2=20, C5=20** for the Raw-LLM persona but the cohort total remained at **R 94/120**, leaving **34 points across C3 (Testability) + C4 (Consistency) + C6 (Friction)**. A single-line "lift §27" task is no longer tractable — the remaining gap requires per-criterion decomposition with named lift candidates, each citing the self-enforcing mechanism that would close the band-anchor gap. This file is that decomposition.

---

## Per-criterion Raw-LLM scoreboard (post Sess-68 B-8)

| Criterion | R-score | Band | Status | Cited mechanism (if 20) | Lift candidate (if < 20) |
|---|---|---|---|---|---|
| **C1 Clarity** | **20/20** | Ceiling | ✓ closed by B-8 | Gate #42 clause-5 banner-triple lockstep + AC-T-38 per-persona pre-flight checklist contract | — |
| **C2 Completeness** | **20/20** | Ceiling | ✓ closed by B-8 | AC-T-38 5-clause tier-promotion drift contract + reverse-coverage invariant (no normative contract can land outside tier-1) | — |
| **C3 Testability** | **16/20** | Upper-band | ✓ closed by B-19 + B-19b (Sess-69) | AC-T-39 5-clause structural contract + 26/26 active-gate-slot ceiling reached on disk + worked-example verifier sketch (`comm -23` returns 0 missing slots) | Ceiling 18-20 deferred to (a) gate #42 clause-6 `active-gate-test-pair-presence` extension making the worked-example loop a hard CI fail (lift C3 16 → 18), and (b) red-green test pairs inlined into the 53 advisory / generator / scaffolding slots not currently active gates (lift C3 18 → 20). |
| **C4 Consistency** | **15/20** | Mid-band | Partial — B-20 + B-16 + B-22 spec-only authored (Sess-69); all three impls pending | — (mid-band; no 18-20 claim today) | **B-20** (slot 66 spec doc shipped; +2 partial lift). **B-16** (5-clause navigation-quintet inline cross-reference convention authored into `00-tier1-bundle.md` v1.2.0; +1 partial lift). **B-22** (`00-carriers-namespace-migration.md` v1.0.0 + AC-T-37 carriers-exclusion clause amendment; +1 partial lift; cited mechanism: anchored numeric-prefix glob `[0-9]*.md` excludes `_carriers/` from four-way parity, removing carrier noise from the consistency surface — reviewer-attestation only). **B-20-impl** (deferred): script + workflow row + AC-T-40 mint + banner-triple bump 26 → 27 → C4 15 → 16. **B-16-impl** (deferred; gated on B-20-impl): mass-edit across 28 active-gate slot files inserting `navigation_quintet` frontmatter row → C4 16 → 17. **B-22-impl** (deferred): file moves into `_carriers/` + slot-61 gate #39 link-resolution extension + §00 Inventory partition table + glob sweep → C4 17 → 18 (band-anchor). |
| **C5 Implementability** | **20/20** | Ceiling | ✓ closed by B-10 (Sess-67) | AC-T-37 four-way parity contract + worked-example bash verifier sketch (Lesson #15 reflexivity first-class) | — |
| **C6 Friction** | **15/20** | Upper-band | Partial — B-21 closed (Sess-69) + B-22 spec-only authored (Sess-69) | `00-tier1-bundle.md` v1.1.0 Tier-2 slot-index lookup table + drift-contract clause + reverse-lookup + active-count parity note + AC-T-38 tier-promotion drift contract | **B-22** (spec-only authored Sess-69 — `00-carriers-namespace-migration.md` v1.0.0: 6-file Phase-1 carrier roster (61/62/63-readme/70/71/80) + AC-T-37 carriers-exclusion clause amendment + deferred-implement turn checklist; +1 partial lift today; full +2 lift to band-anchor 16 gated on **B-22-impl** — file moves into `_carriers/` sub-namespace + slot-61 gate #39 extension + §00 Inventory partition table; cited mechanism post-impl: 6 dead-banner carriers no longer compete for slot-numbering attention). Residual ceiling 16 → 18-20 deferred to a future cross-cohort gate that mechanically verifies the carriers-exclusion glob across all 7 spec cohorts (long-tail). |
| **Σ R-band** | **106/120** | — | floor (cohort) — gap to second-floor §25 (R 108) closed 14 → 2 | — | If B-20-impl + B-16-impl + B-22-impl all land: projected 106 → **~112** (lifts C4 to 18 band-anchor, C6 to 16). Ceiling 120 deferred to a future cross-cohort gate that would mechanically verify per-slot frontmatter uniformity + carriers-exclusion glob AND extend AC-T-39 ceiling enforcement to the 53 advisory slots as a hard fail. |

**L/C bands carried**: §27 Lovable 120/120 + Cursor 120/120 (both cohorts have file-tool access, so the "context-bounded traversal" friction that drives the Raw-LLM gap does not bind them — already at ceiling).

---

## Lift roadmap (priority-ordered)

Each candidate names: (a) the criterion it lifts, (b) projected per-criterion delta, (c) the self-enforcing mechanism it would cite (without which the 20-band is not reachable per the scorecard ritual), (d) any same-PR cohort-discipline coupling.

1. **B-19 + B-19b (CLOSED Sess-69)** — Inlined red-green test pairs into all 26 active-gate slot files. Phase-1 (B-19): slots 58/61/62/63/64. Phase-2 (B-19b): slots 37/39/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/59/60/65.
   - **Delivered**: C3 Testability **12 → 16** (full +4).
   - **Cited mechanism**: AC-T-39 5-clause structural contract + 26/26 ceiling on disk + worked-example verifier returning 0 missing slots.
   - **Same-PR coupling**: AC-T-39 minted (B-19) and amended to "Coverage (full as of Sess-69 B-19b)" attestation (B-19b); same-PR refresh of this file's per-criterion table (B-19b).

2. **B-16 (already on backlog)** — §27 navigation-quintet inline cross-reference in every slot file's frontmatter.
   - **Lifts**: C4 Consistency **~11 → ~14** (~3 points).
   - **Cited mechanism**: `meta-verify-lockstep.py` (slot 64, gate #42) clause-5 extended with a per-slot frontmatter check OR the proposed slot 66 (B-20).
   - **Same-PR coupling**: requires B-20 to land **first** so the uniformity check exists before mass slot edits.

3. **B-20 (NEW)** — `check-slot-frontmatter-uniformity.py` (proposed slot 66, gate #43-promotion candidate).
   - **Lifts**: C4 Consistency **+2** (combined with B-16: 11 → 16).
   - **Cited mechanism**: gate self-test verifies the 4-row frontmatter schema on its own fixtures (Lesson #15 reflexivity).
   - **Same-PR coupling**: §27 §00 + §97 + §98 + §99 banner-triple lockstep + §00-gate-slot-binding.md table row (gate count 26 → 27).

4. **B-21 (CLOSED Sess-69)** — Tier-2 slot-index lookup table appended to `00-tier1-bundle.md` (v1.0.0 → v1.1.0).
   - **Delivered**: C6 Friction **11 → 14** (full +3).
   - **Cited mechanism**: bundle drift-contract clause now binds the new 28-row lookup table by reference; reverse-lookup + active-count parity paragraphs close the two ambiguity gaps; AC-T-38 tier-promotion drift contract remains in force.
   - **Same-PR coupling**: §00 + §98 + §99 banner-triple lockstep; this file's per-criterion table refreshed (C6 row 11 → 14, B-21 status "open" → "closed"). No §97 mint required (bundle is a navigation-aid file per Lesson #36, not a contract surface).

5. **B-22 (NEW)** — `_carriers/` sub-namespace migration for 6 dead-banner slot files.
   - **Lifts**: C6 Friction **+1** (14 → 15) and C4 Consistency **+1** (combined with B-16+B-20: 16 → 17).
   - **Cited mechanism**: `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39) extended to recognise `_carriers/` as a within-folder namespace partition; `00-gate-slot-binding.md` table row count must NOT include `_carriers/` files.
   - **Same-PR coupling**: §97 AC-T-37 four-way parity contract MUST be amended to exclude `_carriers/` from the active-gate count denominator before the migration.

6. **B-26 (NEW Sess-70)** — Cross-cohort `**Mechanically enforced by:**` reverse index appended to `00-gate-slot-binding.md` (or, if that file's structure is closed, authored as a new audit-aid file `00-mechanism-citation-index.md` under §27).
   - **Lifts**: C4 Consistency **+1** (15 → 16) on the spec-text axis. The 26 active gates each have one or more AC callers across the 7 cohorts; today the citation graph is one-way (AC → slot file). A reverse index makes the graph bidirectional and audit-followable: a Raw-LLM walker landing on any §27 slot file can answer "which ACs in which cohorts cite this gate?" in 0 hops instead of 7-cohort grep.
   - **Cited mechanism (spec-only, reviewer-attestation)**: AC-T-37 four-way parity contract extended with a 5th column "callers" naming the ACs that cite each slot; drift between the index and on-disk `**Mechanically enforced by:**` strings is a reviewer-attestation gate today, with a long-tail `-impl` candidate (`build-mechanism-citation-index.py` — explicitly out of scope for this turn per `mem://constraints/no-implementation-suggestions`).
   - **Same-PR coupling**: §27 §00 + §97 (AC-T-37 amendment) + §98 + §99 banner-triple lockstep; this file's per-criterion table refreshed (C4 row 15 → 16, B-26 status "open" → "spec-only authored").
   - **Why spec-only is enough today**: the citation strings already exist on disk across the 7 cohorts (28+ occurrences per `grep -rE '\*\*Mechanically enforced by:\*\*' spec/22..28/`); authoring the reverse index is a transcription task, not a script-output task. The reviewer-attestation rule from this file's clause-1 already governs drift.

7. **B-27 (NEW Sess-70)** — Per-criterion **walker-cost (KB)** column appended to the "Per-criterion Raw-LLM scoreboard" table in this file (Lesson #15 reflexivity extension — the decomposition file becomes the load-proven artefact for its own friction claim).
   - **Lifts**: C6 Friction **+1** (15 → 16, reaching the band-anchor). Today's R C6 = 15 cites the tier-1 bundle's slot-index lookup table but does NOT quantify the bundle-budget cost a Raw-LLM walker pays to verify each criterion's cited mechanism. Adding a `walker-cost (KB)` column makes the budget explicit on disk: e.g. C1 cite = 2 KB (gate #42 banner block only); C5 cite = 12 KB (AC-T-37 four-way parity body + verifier sketch); C3 cite = 28 KB (AC-T-39 + 26-slot ceiling attestation tail). A Raw-LLM auditor with a 30 KB bundle cap can pick which criteria to verify; today they must guess.
   - **Cited mechanism**: this file's drift-contract clause-1 already binds reviewer-attestation; the new column re-uses the same reflexivity hook. No new gate, no new slot.
   - **Same-PR coupling**: this file v1.6.0 → v1.7.0; §99 audit-row tail. **No** §97 bump (the column is a navigation-aid extension, not a contract).
   - **Why this lifts C6, not C4**: friction is the cost of finding the right surface; C6 measures that cost. Adding cost-annotations to surfaces a walker must visit reduces guess-cost — the textbook C6 lever per the band-anchor definition.

8. **B-28 (NEW Sess-70)** — `AC-T-41` mint declaring that the 53 advisory / generator / scaffolding slot files (i.e. the 79 total slots minus the 26 active-gate slots) MUST carry a one-line `**Test pair:** N/A — <axis-class>` stub in their frontmatter or `## Status` section, where `<axis-class>` ∈ {`advisory`, `generator`, `scaffold`, `audit-aid`, `convention`}.
   - **Lifts**: C3 Testability **+1** (16 → 17). Today AC-T-39 covers the 26 active-gate slots (full ceiling); the 53 non-gate slots are silent on testability, leaving a Raw-LLM walker no signal whether absence-of-tests is intentional (advisory) or a contract gap (gate-slot drift). AC-T-41 closes the silence with a closed-set 5-class enum.
   - **Cited mechanism**: `meta-verify-lockstep.py` (slot 64, gate #42) clause-5 banner-triple lockstep already governs this file's drift; AC-T-41 reuses the same hook plus a reviewer-attestation rule until a `-impl` extension to gate #42 mechanically enforces the stub presence (long-tail).
   - **Same-PR coupling**: §27 §97 v2.23.0 → v2.24.0 (AC count +1); §00 + §98 + §99 banner-triple lockstep; this file's per-criterion table refreshed (C3 row 16 → 17). **No** new slot file (AC binds existing slots).
   - **Lesson #36 preservation**: the AC names the closed-set enum; per-slot stubs are one-line frontmatter, not restated contracts.

**Aggregate projection (Sess-70 update)**: B-19/B-19b/B-21 CLOSED. B-16 + B-20 + B-22 spec-only authored, all `-impl` deferred. **B-26 / B-27 / B-28 are the next 3 spec-only `next` slots**: if all three land, §27 Raw-LLM **106 → ~110** (Δ +4: C4 +1 via B-26, C6 +1 via B-27, C3 +1 via B-28; band-anchor stays at 16 for C4 / C6, 17 for C3). Residual 10-point gap (~110 → 120) requires the three queued `-impl` turns (B-16-impl + B-20-impl + B-22-impl, projected +6) plus one long-tail cross-cohort gate proposal (`build-mechanism-citation-index` from B-26, projected +4 long-tail) — none of which are spec-text candidates and all of which are out of scope until the user explicitly says "implement".


---

## Gating checks (Lesson #15 reflexivity, 20-band anchor)

This file's lift-candidate roster is **not** itself a contract — it is an audit aid. However, the **per-criterion scores** above are subject to the scorecard ritual: any commit changing §27 R-band cells in the cohort-wide scorecard MUST in the same commit either (a) update this file's "Per-criterion Raw-LLM scoreboard" table to keep the per-criterion sum equal to the cohort total, or (b) cite this file in the changelog entry as "deferred — decomposition stale, refresh in next session". Drift between this file and the cohort scorecard is allowed for ≤ 1 session; longer drift trips a manual reviewer attestation.

The lift candidates B-19 / B-20 / B-21 / B-22 themselves are spec-text proposals only — none of them ship until promoted to a session-tagged action and authored into §97 (or, for B-20, also into a new slot file). Listing here is **not** authorisation to land — `next` continues to be required to advance any one of them.

---

## Self-citation

This file is **mechanically enforced by** `meta-verify-lockstep.py` (`spec/27-spec-toolchain/` slot 64, gate #42) clause-5 banner-triple lockstep against §27 §00 / §98 / §99: any banner bump to this file that is not mirrored in §99's audit-row tail within the same commit trips gate #42 and hard-fails CI. The closed-set perimeter (links only to `mem://`, `spec/27-…`, and within-cohort relative paths) is **mechanically enforced by** `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39) on the link-target axis.
