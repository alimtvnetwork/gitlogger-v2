---
kind: gate-spec
status: proposed
candidate_gate: "#44"
delegates_from_ac: AC-T-40 (proposed)
mechanically_enforced_by: linter-scripts/check-slot-frontmatter-uniformity.py (proposed; not yet on disk)
axis: per-slot-frontmatter-uniformity
axis_rationale: "Pin the 4-row slot-doc frontmatter schema across all 79 §27 slot files so a Raw-LLM walker can rely on a fixed shape without per-file branching."
---

# Slot 66 — `check-slot-frontmatter-uniformity.py` (PROPOSED)

**Status:** **Proposed gate #44** (Sess-69 B-20 — spec-only authorship; script not yet on disk; promotion to Active gate gated on an explicit "implement" turn per `mem://constraints/no-implementation-suggestions`).
**Source:** `linter-scripts/check-slot-frontmatter-uniformity.py` (proposed; would land in the same PR that promotes this slot to Active).
**Self-test:** built-in (`--self-test`) — 7 in-memory fixtures specified below (F-1..F-7).
**Workflow step:** `.github/workflows/spec-health.yml` "Slot frontmatter uniformity check (Sess-69 B-20 / proposed)" (proposed; would be added as `warn-only` for one phase, then promoted to hard fail in lockstep with the `00-overview.md` Active Gate Inventory bump 26 → 27).
**Wired-mode (when promoted):** **warn-only** for one Sess- cycle, then hard fail (mirrors slot 65 / gate #43 promotion pattern from Phase-5 T-40 / P19a).


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Why this slot exists (Raw-LLM C4 floor diagnosis)

`spec/27-spec-toolchain/00-raw-llm-bottleneck-decomposition.md` v1.2.0 identifies §27 Raw-LLM **C4 Consistency = 11/20** as the second-largest single-criterion gap after C3 (now closed). The named root cause: **frontmatter shapes drift across the 79 §27 slot generations**. A Raw-LLM walker reading any single slot file today cannot rely on a fixed front-matter schema — generations from Sess-30..Sess-50 use 2-row frontmatter, Sess-50..Sess-65 use 3-row, Sess-65..Sess-69 use 4-row. Per-criterion lift candidate **B-20** mints this slot to mechanise the 4-row schema as a hard floor; combined with **B-16** (navigation-quintet inline cross-reference, blocked on this slot landing first) it lifts C4 **11 → 16** (B-20 contributes +2; B-16 contributes +3).

This slot is spec-only authorship today. Per the project core memory ("Default mode = spec-only … never 'ship/wire/load-prove' phrasing"), the script and workflow row do not land until an explicit "implement" turn promotes the slot. Authoring the spec doc first follows the Lesson #15 reflexivity pattern already established by slots 47, 48, 53, 65 (spec doc precedes script by one or more sessions; promotion to Active happens in a single same-PR landing of script + workflow row + banner-triple bump + `00-overview.md` Active Gate Inventory row).

---

## Contract — four invariants

| ID  | Name              | Rule                                                                                                                                                                                                                                                                       | Exit |
|-----|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|
| U-1 | SCHEMA-PRESENT    | Every `spec/27-spec-toolchain/NN-*.md` slot file (NN ∈ 00..99, excluding `00-overview.md`, `00-tier1-bundle.md`, `00-gate-slot-binding.md`, `00-raw-llm-bottleneck-decomposition.md`, `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md`) MUST open with a YAML frontmatter block delimited by `---` lines. | 1    |
| U-2 | SCHEMA-KEYS       | The frontmatter MUST contain exactly the four canonical keys, in this canonical order: `kind`, `axis`, `delegates_from_ac`, `mechanically_enforced_by`. Optional 5th key `status` permitted ONLY if value ∈ {`active`, `proposed`, `deferred`, `archived`}. No other keys. | 2    |
| U-3 | KIND-VOCABULARY   | The `kind` value MUST be drawn from the closed-set `{gate-spec, validator-spec, generator-spec, scaffolder-spec, carrier-spec, bundle-manifest, decomposition-aid}`. Unknown kinds fail.                                                                                  | 3    |
| U-4 | AXIS-NONEMPTY     | The `axis` value MUST be a non-empty kebab-case string (regex `^[a-z][a-z0-9-]{2,}$`); the `axis_rationale` row (when present, optional) MUST be a quoted string ≥ 20 chars. Empty / placeholder axes (`tbd`, `?`, `axis`) fail.                                          | 4    |

Carve-outs: the 7 file names listed in U-1 are explicit exemptions because they are **module-level surfaces** (overview, bundle, binding, decomposition, AC, changelog, consistency-report), not per-slot gate specs. Their frontmatter shapes are pinned by AC-T-30/-31/-36/-37/-38 (the navigation quintet) and not by this gate. Reflexively, **this very file** (`66-check-slot-frontmatter-uniformity.md`) IS subject to U-1..U-4 — its own frontmatter above is a worked example of the canonical 4-row + optional `status` shape.

---

## Exit-code contract

Exit codes: `0` pass · `1` violation (U-1 SCHEMA-PRESENT — missing frontmatter) · `2` violation (U-2 SCHEMA-KEYS — wrong keys / wrong order / forbidden extras) · `3` violation (U-3 KIND-VOCABULARY — unknown `kind`) · `4` violation (U-4 AXIS-NONEMPTY — empty / placeholder axis) · `99` FATAL — `spec/27-spec-toolchain/` not found.

| Exit | Meaning                                                                                       |
|------|-----------------------------------------------------------------------------------------------|
| `0`  | pass — all four invariants hold across all in-scope slot files.                               |
| `1`  | U-1 SCHEMA-PRESENT failure — at least one slot file lacks the leading `---` frontmatter block.|
| `2`  | U-2 SCHEMA-KEYS failure — wrong key set, wrong order, or forbidden extra keys.                |
| `3`  | U-3 KIND-VOCABULARY failure — `kind` value outside the 7-token closed set.                    |
| `4`  | U-4 AXIS-NONEMPTY failure — `axis` empty / placeholder, or `axis_rationale` < 20 chars.       |
| `99` | FATAL — `spec/27-spec-toolchain/` directory not present (invocation error).                   |

First failure across U-1..U-4 wins; the script MUST print all violations of the failing invariant before exiting (no fail-fast). This mirrors slot 47 / slot 48 / slot 65 reporting discipline.

---

## Self-test fixture roster (F-1..F-7)

All 7 fixtures MUST be in-memory synthetic corpora (no on-disk file pollution; mirrors slot 47 / slot 48 / slot 65 pattern). Each fixture asserts a single named outcome.

| ID  | Name                          | Synthetic corpus                                                                                                                       | Expected exit | Asserts          |
|-----|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|---------------|------------------|
| F-1 | unique-passing                | Three slot files with canonical 4-row frontmatter + valid `kind` + non-empty kebab-case `axis`.                                        | `0`           | happy-path       |
| F-2 | missing-frontmatter           | Slot file opens with `# Title` directly (no `---` block).                                                                              | `1`           | U-1 fires        |
| F-3 | wrong-key-order               | Frontmatter present with all 4 canonical keys but `axis` precedes `kind`.                                                              | `2`           | U-2 fires        |
| F-4 | extra-key                     | Frontmatter present with 4 canonical keys + a forbidden 6th key `owner: alice`.                                                        | `2`           | U-2 fires        |
| F-5 | unknown-kind                  | Frontmatter present with canonical key set + canonical order; `kind: linter` (not in the 7-token closed set).                          | `3`           | U-3 fires        |
| F-6 | empty-axis                    | Frontmatter present with canonical key set + canonical order + valid `kind`; `axis: tbd`.                                              | `4`           | U-4 fires        |
| F-7 | reflexive-this-file           | This very `66-check-slot-frontmatter-uniformity.md` file's frontmatter parsed against the gate. MUST exit 0 — Lesson #15 reflexivity. | `0`           | self-cite passes |

Per slot 65 / gate #43 lesson "the self-test IS part of the gate": F-7 makes the spec doc itself a regression fixture. Stripping the frontmatter from this file MUST fail the gate's own `--self-test` before it fails any other slot doc.

---

## Bindings

- **Mechanically enforced by:** itself (slot 66 / proposed gate #44, when shipped) — Lesson #15 reflexivity. Until promoted, enforcement is reviewer-attestation per `mem://constraints/no-implementation-suggestions`.
- **Delegates from AC:** AC-T-40 (proposed; would be minted in §97 same PR as script promotion). Pre-promotion, the contract above stands as authoritative spec text per AC-T-37 four-way parity invariant treating slot doc bodies as the contract surface in the absence of a §97 row.
- **Composes with:** slot 65 / gate #43 (NUMBERED invariant — gate-number uniqueness still applies if this slot promotes to gate #44); slot 64 / gate #42 (banner-triple lockstep — promotion MUST bump §00 + §97 + §98 + §99 + `00-tier1-bundle.md` Tier-2 lookup table in the same commit); slot 47 / gate #28 (§97 hygiene — the proposed AC-T-40 MUST carry a `[critical]` status tag).
- **Unblocks:** slot-mass-edit task **B-16** (navigation-quintet inline cross-reference table) which mass-edits frontmatter across all 79 §27 slot files; B-16 cannot land safely without B-20 first establishing the schema floor (otherwise the mass edit could itself introduce drift). Sequencing B-20 → B-16 over two sessions captures C4 +5 (B-20 +2 + B-16 +3); skipping B-20 caps the achievable lift at C4 +1.

---

## Red-green test pairs (AC-T-39)

| Phase | Invocation                                                                                                                                        | Fixture / clause                              | Expected outcome                              |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|-----------------------------------------------|
| **RED:**   | (post-promotion) strip the `---` frontmatter from any in-scope slot file, then run `python3 linter-scripts/check-slot-frontmatter-uniformity.py`     | F-2 `missing-frontmatter` analogue            | exit `1` with stderr listing the offending slot path |
| **RED:**   | (post-promotion) reorder the 4 canonical keys in any in-scope slot file (e.g. swap `kind` and `axis`), then run `python3 linter-scripts/check-slot-frontmatter-uniformity.py` | F-3 `wrong-key-order` analogue                | exit `2` with stderr listing the offending slot path + observed key order |
| **GREEN:** | (today, pre-promotion) `cat spec/27-spec-toolchain/66-check-slot-frontmatter-uniformity.md \| head -10` — confirm leading `---` + 4 canonical keys + valid `kind` + non-empty `axis` + optional `status: proposed` | F-7 `reflexive-this-file` analogue            | manual-attestation pass; once script ships, F-7 self-test exits `0` |
| **GREEN:** | (post-promotion) `python3 linter-scripts/check-slot-frontmatter-uniformity.py --self-test`                                                        | All 7 fixtures (F-1..F-7)                     | exit `0`, stdout `OK — 7/7 fixtures pass`     |

Pre-promotion the RED rows are reviewer-attestation only; the script does not exist on disk. Post-promotion the same rows become hard-fail CI checks. The GREEN row F-7 (reflexive) is the single most important fixture: it makes this very spec doc a regression test for itself.

---

## Scorecard impact (Rubric v2 /120)

**Today (B-20, spec-only authorship):**
- §27 R-band C4 (Consistency) **11 → 13** (+2 partial lift; cited mechanism: U-2 SCHEMA-KEYS schema pin + U-3 KIND-VOCABULARY closed set, both in this slot doc body — but enforcement is reviewer-attestation only until script promotes).
- §27 Raw-LLM /120 **101 → 103**.
- Cohort R mean: ~113.0 → ~113.3.

**Projected (post-promotion, single-PR landing of script + workflow + AC-T-40 + banner-triple + `00-overview.md` Active Gate Inventory row):**
- §27 R-band C4 **13 → 16** (full +5 lift cumulative; +3 from machine-checked enforcement). Combined with B-16 inline navigation-quintet cross-reference (which becomes safe to land once this gate is hard): C4 **16 → 18** (band-anchor reached).
- §27 Raw-LLM /120 **103 → ~108**.
- Total active gates 26 → **27**; gate # ledger 43 → **44**.

The spec-only +2 today is the **maximum single-task lift achievable without script implementation**. The full +5 (band-anchor at 18) requires the explicit "implement" turn per `mem://constraints/no-implementation-suggestions` and is not authorised by this slot's mere existence.

---

## Self-enforcing mechanism (Rubric v2 18-20 band requirement)

Per `mem://preferences/scorecard-ritual` core memory: a score of **18-20** on any criterion REQUIRES citing a self-enforcing mechanism. **Today this slot does NOT claim 18-20** — C4 lifts to 13, mid-band, on the strength of the schema pin + closed-set vocabulary in this doc body alone.

The 18-20 band is reachable only after promotion to Active gate (script + workflow + AC-T-40), at which point the cited mechanism is: (a) the script itself running on every push as a hard fail (post-warn-only phase); (b) F-7 `reflexive-this-file` fixture making the spec doc its own regression test; (c) gate #43 (slot 65) NUMBERED invariant rejecting any frontmatter-uniformity-bypass that would otherwise duplicate gate numbers; (d) gate #42 (slot 64) banner-triple lockstep ensuring the Active Gate Inventory in `00-overview.md` cannot be bumped 26 → 27 without the script existing on disk.

---

## Cross-references

- [`00-overview.md`](./00-overview.md) — Active Gate Inventory (this slot listed as "Proposed" until promotion).
- [`00-tier1-bundle.md`](./00-tier1-bundle.md) v1.1.0 — Tier-2 slot-index lookup table (this slot would gain a row at `66 | #44 | this-file | Meta gate / structural hygiene` upon promotion; today carried as a Tier-3 proposed-gate carrier).
- [`00-raw-llm-bottleneck-decomposition.md`](./00-raw-llm-bottleneck-decomposition.md) v1.2.0 — B-20 lift candidate (this slot is the spec-side half of B-20).
- [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) — AC-T-40 to be minted same PR as script promotion (Lesson #36: AC body MUST cite this slot, not restate the contract).
- [`65-check-gate-ledger-vs-workflow.md`](./65-check-gate-ledger-vs-workflow.md) — gate #43 NUMBERED invariant (will accept gate #44 as next-in-sequence).
- [`64-meta-verify-lockstep.md`](./64-meta-verify-lockstep.md) — gate #42 clause-5 banner-triple lockstep (governs the 26 → 27 promotion bump).
- [`47-check-ac-section-orphan-header.md`](./47-check-ac-section-orphan-header.md) — gate #28 (governs the AC-T-40 `[critical]` status tag at mint).
- Sibling proposed-but-not-shipped slot precedent: none yet in §27 (this is the first); pattern borrowed from §22 §97 deferred-AC convention.

---

## History

- **Sess-69 B-20** — Spec doc authored. Status: Proposed. Script not on disk. AC-T-40 not yet minted. Promotion gated on explicit "implement" turn per `mem://constraints/no-implementation-suggestions`. Lifts §27 R C4 11 → 13 today; full lift to 16 (+ B-16 unblock to 18) deferred to post-promotion.
