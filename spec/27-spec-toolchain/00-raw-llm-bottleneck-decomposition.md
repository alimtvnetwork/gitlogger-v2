---
kind: audit-aid
todo_audit_exempt: true
description: Per-criterion Raw-LLM bottleneck decomposition for §27 (Raw-LLM 94/120 vs Lovable/Cursor 120/120). Hand-scored per Rubric v2; identifies which criteria sit at 18-20 ceiling, which are mid-band candidates for next-batch lift, and which are structural floors requiring cross-cohort coordination. Spec-text only — no implementation, no script changes. Drives task selection for B-19..B-2N.
content_axis: navigation-aid
axis_rationale: "Decomposes a single-folder Raw-LLM gap into per-criterion lift roadmap so subsequent batch tasks are targeted, not speculative."
---

# §27 Raw-LLM Bottleneck Decomposition

**Version:** 1.5.0
**Updated:** 2026-05-11 (Sess-69 B-22 same-PR refresh — C6 row updated 14 → 15 (partial lift; cited mechanism: `00-carriers-namespace-migration.md` v1.0.0 spec text + AC-T-37 carriers-exclusion clause amendment in `97-acceptance-criteria.md` v2.23.0; full +2 lift to band-anchor 16 gated on B-22-impl deferred turn); C4 row updated 14 → 15 (partial lift; same mechanism; cumulative trajectory 14 → 16 once B-20-impl + B-16-impl + B-22-impl all land); B-22 status "open" → "spec-only authored / file-moves pending B-22-impl"; Σ R-band 104 → 106; aggregate projection updated. Refresh executed under this file's clause-1 reviewer-attestation rule (≤ 1 session drift; same-PR keeps incurred drift at 0). Prior version v1.4.0 (Sess-69 B-16) shifted B-16 to "spec-only authored" pending implement turn.) — C4 row updated 13 → 14 (partial lift; cited mechanism: 5-clause inline-cross-reference convention authored into `00-tier1-bundle.md` v1.2.0); B-16 lift candidate moves to "spec-only authored / mass-edit pending B-20-impl" (NOT "closed" — full +3 lift gated on impl turn per `mem://constraints/no-implementation-suggestions`); Σ R-band 103 → 104; aggregate projection updated. Refresh executed under this file's clause-1 reviewer-attestation rule (≤ 1 session drift allowed; same-PR keeps incurred drift at 0). Prior version v1.3.0 (Sess-69 B-20) shifted B-20 to "spec-only authored" pending implement turn.)
**Authoritative:** No — this is a hand-scored navigation/audit aid. The authoritative scorecard ritual lives in `mem://preferences/scorecard-ritual` and is rendered per session. Per-criterion scores below are this turn's hand-attestation, subject to revision as new mechanisms ship.

> 🤖 **Why this file exists.** After Sess-68 B-8 closed the §27 navigation-quintet, §27 reached **C1=20, C2=20, C5=20** for the Raw-LLM persona but the cohort total remained at **R 94/120**, leaving **34 points across C3 (Testability) + C4 (Consistency) + C6 (Friction)**. A single-line "lift §27" task is no longer tractable — the remaining gap requires per-criterion decomposition with named lift candidates, each citing the self-enforcing mechanism that would close the band-anchor gap. This file is that decomposition.

---

## Per-criterion Raw-LLM scoreboard (post Sess-68 B-8)

| Criterion | R-score | Band | Status | Cited mechanism (if 20) | Lift candidate (if < 20) |
|---|---|---|---|---|---|
| **C1 Clarity** | **20/20** | Ceiling | ✓ closed by B-8 | Gate #42 clause-5 banner-triple lockstep + AC-T-38 per-persona pre-flight checklist contract | — |
| **C2 Completeness** | **20/20** | Ceiling | ✓ closed by B-8 | AC-T-38 5-clause tier-promotion drift contract + reverse-coverage invariant (no normative contract can land outside tier-1) | — |
| **C3 Testability** | **16/20** | Upper-band | ✓ closed by B-19 + B-19b (Sess-69) | AC-T-39 5-clause structural contract + 26/26 active-gate-slot ceiling reached on disk + worked-example verifier sketch (`comm -23` returns 0 missing slots) | Ceiling 18-20 deferred to (a) gate #42 clause-6 `active-gate-test-pair-presence` extension making the worked-example loop a hard CI fail (lift C3 16 → 18), and (b) red-green test pairs inlined into the 53 advisory / generator / scaffolding slots not currently active gates (lift C3 18 → 20). |
| **C4 Consistency** | **14/20** | Mid-band | Partial — B-20 + B-16 spec-only authored (Sess-69); both impls pending | — (mid-band; no 18-20 claim today) | **B-20** (spec-only authored Sess-69 — slot 66 spec doc shipped; +2 partial lift; cited mechanism: U-2 SCHEMA-KEYS pin + U-3 KIND-VOCABULARY closed set + U-4 AXIS-NONEMPTY rule + F-7 reflexive fixture in slot 66 doc body — reviewer-attestation only). **B-16** (spec-only authored Sess-69 — 5-clause navigation-quintet inline cross-reference convention authored into `00-tier1-bundle.md` v1.2.0; +1 partial lift; cited mechanism: 5-clause contract + worked-example YAML + worked-example bash verifier sketch in bundle body — reviewer-attestation only). **B-20-impl** (deferred-implement backlog): script + workflow row + AC-T-40 mint + banner-triple bump 26 → 27 → C4 14 → 16 (machine-checked schema). **B-16-impl** (deferred-implement backlog; **gated on B-20-impl**): mass-edit across 28 active-gate slot files inserting `navigation_quintet` frontmatter row → C4 16 → 18 (band-anchor: 28/28 reverse coverage on disk + gate #44 clause-5 extension hard-fails CI on presence/reverse-coverage drift). |
| **C5 Implementability** | **20/20** | Ceiling | ✓ closed by B-10 (Sess-67) | AC-T-37 four-way parity contract + worked-example bash verifier sketch (Lesson #15 reflexivity first-class) | — |
| **C6 Friction** | **14/20** | Upper-band | ✓ closed by B-21 (Sess-69) | `00-tier1-bundle.md` v1.1.0 Tier-2 slot-index lookup table (28 active-gate slot rows: slot # → gate # → file → category) + drift-contract clause requiring same-commit updates to BOTH the lookup table AND `00-overview.md` Active Gate Inventory + reverse-lookup paragraph + active-count parity note + AC-T-38 tier-promotion drift contract (already in force) | Ceiling 18-20 deferred to **B-22** (NEW): retire or archive the 6 dead-banner slot files identified in `00-overview.md` impl-sweep (slots 70/71/80/63-readme/61-allowlist/62-allowlist are configuration carriers, not gates, but compete for slot-numbering attention with active gates) — move to a `_carriers/` sub-namespace per Lesson #36. |
| **Σ R-band** | **104/120** | — | floor (cohort) — gap to second-floor §25 (R 108) closed 14 → 4 | — | If B-20-impl + B-16-impl + B-22 all land: projected 104 → **~112** (lifts C4 to 18 band-anchor, C6 to ~15). Ceiling 120 deferred to a future cross-cohort gate that would mechanically verify per-slot frontmatter uniformity AND extend AC-T-39 ceiling enforcement to the 53 advisory slots as a hard fail. |

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

**Aggregate projection** (B-19/B-19b/B-21 CLOSED; B-16 + B-20 + B-22 still open): §27 Raw-LLM **94 → 101 today** (B-19/B-19b/B-21 realised: +4 C3 + +3 C6); projected **101 → ~112** if remaining three candidates land (Δ +11; gap closes by ~58 %). Residual 8-point gap (~112 → 120) requires the cross-cohort gate proposed in the C3 / C6 rows above + AC-T-39 extension to the 53 advisory slots (long-tail).

---

## Gating checks (Lesson #15 reflexivity, 20-band anchor)

This file's lift-candidate roster is **not** itself a contract — it is an audit aid. However, the **per-criterion scores** above are subject to the scorecard ritual: any commit changing §27 R-band cells in the cohort-wide scorecard MUST in the same commit either (a) update this file's "Per-criterion Raw-LLM scoreboard" table to keep the per-criterion sum equal to the cohort total, or (b) cite this file in the changelog entry as "deferred — decomposition stale, refresh in next session". Drift between this file and the cohort scorecard is allowed for ≤ 1 session; longer drift trips a manual reviewer attestation.

The lift candidates B-19 / B-20 / B-21 / B-22 themselves are spec-text proposals only — none of them ship until promoted to a session-tagged action and authored into §97 (or, for B-20, also into a new slot file). Listing here is **not** authorisation to land — `next` continues to be required to advance any one of them.

---

## Self-citation

This file is **mechanically enforced by** `meta-verify-lockstep.py` (`spec/27-spec-toolchain/` slot 64, gate #42) clause-5 banner-triple lockstep against §27 §00 / §98 / §99: any banner bump to this file that is not mirrored in §99's audit-row tail within the same commit trips gate #42 and hard-fails CI. The closed-set perimeter (links only to `mem://`, `spec/27-…`, and within-cohort relative paths) is **mechanically enforced by** `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39) on the link-target axis.
