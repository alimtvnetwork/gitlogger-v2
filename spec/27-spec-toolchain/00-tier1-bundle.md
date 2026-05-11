---
kind: bundle-manifest
todo_audit_exempt: true
description: Tier-1 essential bundle — the minimum subset of §27 source files an LLM must read to understand the spec-toolchain, navigate the active gate set, and know which slot doc to consult for any specific gate. Targets the Raw-LLM persona (single context window, no file-tool access). All other §27 files are tier-2 (per-gate slot docs, read on demand) or tier-3 (changelog archaeology, allowlists, runner stubs). Out-of-bundle files MUST NOT introduce cross-gate contracts not pinned by tier-1.
content_axis: navigation-aid
axis_rationale: "Single-page read-order anchor for the §27 spec set"
---

# Spec Toolchain — Tier-1 Essential Bundle

**Version:** 1.2.0
**Updated:** 2026-05-11 (Sess-69 B-16 — added "Navigation-quintet inline cross-reference convention" sub-section pinning 5-clause frontmatter contract requiring every active-gate slot file to inline AC-T-30/-31/-36/-37/-38 under a `navigation_quintet` frontmatter key in canonical order. Carve-out: 7 module-level surfaces exempt (would be circular self-citation). Worked-example YAML + worked-example bash verifier sketch included for the post-mass-edit verifier (candidate body for slot 66 / gate #44 clause-5 extension). Phased rollout: today = spec-only authorship + reviewer-attestation; B-16-impl mass-edit across 28 active-gate slots gated on B-20-impl per slot 66 schema floor. Lifts §27 R-band C4 (Consistency) **+1** today (reviewer-attestation only); +3 cumulative post-impl. v1.1.0 → v1.2.0 — additive only; no tier partition changes.)
**Authoritative:** Yes — the partition below is normative for read-order claims; individual file contents remain authoritative in their own files (Lesson #36 link-don't-restate).

> 🤖 **Raw-LLM Reader Pin.** §27 is a *meta-module*: it specifies the gates that audit the other six in-scope cohorts (§22-§26, §28). Most §27 files are per-gate slot docs (one file per active gate, ~50-200 lines each). To **navigate** §27 you only need the four tier-1 files below (~1,573 lines). To **work on a specific gate**, add the corresponding tier-2 slot doc on demand. The 1,080-line `98-changelog.md` is tier-3 — never required for current work.


**Test pair:** N/A — audit-aid  <!-- AC-T-41 closed-set axis-class stub -->
---

## Tier-1 — Navigable minimum (read in order)

| # | File | Lines | Walker-cost (KB) | Role | Why tier-1 |
|---|---|---|---|---|---|
| 1 | [`00-overview.md`](./00-overview.md) | 465 | ~83 | Module pin + active-gate count (26) + invariants triple (I-1 EXISTS, I-2 WIRED, I-3 NUMBERED) + slot-numbering scheme + retired-gate frozen list (INV-03 anchor) | Establishes the toolchain's vocabulary, the gate-counting rule, and the perimeter for slot numbers. Read first. |
| 2 | [`trace-map.md`](./trace-map.md) | 419 | ~50 | Gate dependency DAG: which gates are prerequisites for which others; per-gate `consumes` / `produced_for` rows | The single source for "which gate to consult / extend first". Without this, an implementer cannot order changes correctly. |
| 3 | [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) | 429 | ~101 | 36 ACs for the toolchain itself (AC-T-* family — gate hygiene, slot reflexivity, ledger lockstep) | Every gate-side contract is here. Read after the trace map so each AC's `Verifies:` cell already names a known gate slot. |
| 4 | [`99-consistency-report.md`](./99-consistency-report.md) | 260 | ~185 | Newest banner block + per-version scorecard delta + current Sess-NN tasks | Tells the reader where the toolchain is **right now** (versions, last-shipped gate, open tickets). Read last in tier-1. |
| **Σ** | **4 files** | **~1,573** | **~419** | **Tier-1 footprint** | Below the 8K-token "single context window" comfort threshold by line-count; **far above** any reasonable byte-budget by KB-count (see Walker-cost reflexivity section below). |

**Read-order rationale:** vocabulary + invariants (1) → gate dependency graph (2) → contracts (3) → current state (4). After tier-1 the reader knows: how many active gates exist, which slot file owns each gate, what each gate guarantees, and which gate(s) are currently open work.

---

## Tier-2 — Per-gate slot docs (read on demand, one file per gate)

§27 follows a **one-file-per-slot** convention: every active gate gets a numbered slot file (`NN-<short-name>.md`) describing its purpose, clauses, self-test fixture roster, and CI wiring. Read the slot doc only when working on that specific gate. The slot files are listed in `00-overview.md` Active Gate Inventory section in canonical numeric order — duplicate the read-order from there.

**Categories** (all tier-2; read by category as needed):

| Category | Slot range | Examples | When to read |
|---|---|---|---|
| Cross-link / structural hygiene | 01-09, 18, 19 | spec cross-links, forbidden strings, mermaid syntax | When editing inter-spec navigation or adding a new spec file. |
| Generators (produce ledgers/reports) | 10-17 | spec-index, dashboard-data, gwt-acceptance, trace-map regenerator | When the auto-generated artefact drifts from its source spec. |
| Scaffolders / fillers | 20-23 | fill-missing-acceptance-criteria, scaffold-spec-module | When introducing a new spec module from scratch. |
| Lockstep + version parity | 24, 27, 29 | check-lockstep, check-99-stamp-bump, check-version-parity | When bumping a banner triple (§00/§97/§98/§99) on any cohort. |
| §99 freshness + audit cadence | 25, 26, 38, 46 | deepen-consistency-reports, check-99-summary-freshness, audit-quoted-evidence-marker | When editing any §99 file. |
| Audit-AI implementability | 33, 34, 35 | check-ai-confidence, audit-ai-implementability, audit-bundle-budget | When tuning auditor scoring or bundle sizes. |
| Cohort-specific surface gates | 39, 42-45, 49, 53-60, 63 | applink-xor, error-envelope-uniformity, ui-component-binding-matrix, appshell-route-matrix, no-sql-ddl-in-ui-folder, diagram-parity | When the named cohort surface gains a new contract. |
| Boundary / scope perimeter | 36, 58, 59, 60, 61 | ads-boundaries, no-sql-ddl-in-ui-folder, no-ci-yaml-in-issues-folder, no-toolchain-enum-in-issues-folder, no-out-of-scope-spec-folder-link | When the locked-7 perimeter is touched. |
| §97 hygiene + AC structure | 47, 48 | ac-section-orphan-header, ac-prefix-contract | When adding/removing/renaming any AC. |
| Sub-cohort boundary checks | 50, 51, 52, 56, 57 | validate-guidelines, axios-version, rest-pascalcase-parity, rest-boolean-parity | When editing platform contracts (REST surface, dependency pins). |
| §28 / §26 self-test harness | 62, 63 | check-ci-cli-self-test-harness, check-diagram-parity | When extending §28 self-tests or §26 diagram contracts. |
| Meta gates (audit the toolchain itself) | 64, 65 | meta-verify-lockstep, check-gate-ledger-vs-workflow | When making any structural change to §27 itself. |

### Tier-2 slot index — lookup table (B-21, Sess-67)

> **Purpose.** A single-shot slot-number → gate-number → file lookup so a Raw-LLM reader (no file-tool access) can resolve "which slot doc owns gate #N?" or "which gate does slot NN ship?" without paging through `00-overview.md`'s category-grouped inventory. The mapping below is authoritative for the **active gate set** as of Sess-67; carrier files (allowlists, runner stubs, workflow YAML specs) are tier-3 and listed in their own table above. Source of truth: per-file `# title` line + first `gate #N` literal in the slot doc body.
>
> **Drift contract.** Add a new active gate → add a row here AND to the Active Gate Inventory in `00-overview.md` in the same commit. Retire a gate → strike the row here AND record the frozen-slot entry in `00-overview.md` retired-gates list. Failure to do so MUST be flagged by the next §99 entry per the existing tier-1 drift contract below.

| Slot | Gate # | File | Category |
|---|---|---|---|
| 27 | #16 | [27-check-99-stamp-bump.md](./27-check-99-stamp-bump.md) | §99 freshness |
| 28 | #17 | [28-check-archive-exclusion-runtime.md](./28-check-archive-exclusion-runtime.md) | Lockstep / runtime probe |
| 29 | #19 | [29-check-version-parity.md](./29-check-version-parity.md) | Lockstep + version parity |
| 36 | #19 | [36-check-ads-boundaries.md](./36-check-ads-boundaries.md) | Boundary / scope perimeter (§24) |
| 37 | #20 | [37-check-spec22-inventory.md](./37-check-spec22-inventory.md) | Cohort surface (§22) |
| 38 | #21 | [38-check-verification-ledger-cadence.md](./38-check-verification-ledger-cadence.md) | §99 freshness + audit cadence |
| 39 | #22 | [39-check-applink-xor-clause.md](./39-check-applink-xor-clause.md) | Cohort surface (§23) |
| 42 | #23 | [42-check-error-envelope-uniformity.md](./42-check-error-envelope-uniformity.md) | Cohort surface (§22+§23+§24) |
| 43 | #24 | [43-check-boolean-uniformity-primary-lane.md](./43-check-boolean-uniformity-primary-lane.md) | Cohort surface (§22+§23+§24) |
| 44 | #25 | [44-check-seedable-config-row-present.md](./44-check-seedable-config-row-present.md) | Cohort surface (§23) |
| 45 | #26 | [45-check-idempotency-observability.md](./45-check-idempotency-observability.md) | Cohort surface (§22+§23) |
| 46 | #27 | [46-check-audit-quoted-evidence-marker.md](./46-check-audit-quoted-evidence-marker.md) | §99 freshness + audit cadence |
| 47 | #28 | [47-check-ac-section-orphan-header.md](./47-check-ac-section-orphan-header.md) | §97 hygiene + AC structure |
| 48 | #29 | [48-check-ac-prefix-contract.md](./48-check-ac-prefix-contract.md) | §97 hygiene + AC structure |
| 49 | #30 | [49-check-ui-component-binding-matrix.md](./49-check-ui-component-binding-matrix.md) | Cohort surface (§24) |
| 53 | #31 | [53-check-appshell-route-matrix.md](./53-check-appshell-route-matrix.md) | Cohort surface (§24) |
| 54 | #32 | [54-check-seed-id-explicit-locked-form.md](./54-check-seed-id-explicit-locked-form.md) | Cohort surface (§23) |
| 55 | #33 | [55-check-dialect-precedence-banner-present.md](./55-check-dialect-precedence-banner-present.md) | Cohort surface (§22+§23) |
| 56 | #34 | [56-check-rest-pascalcase-parity.md](./56-check-rest-pascalcase-parity.md) | Sub-cohort REST surface |
| 57 | #35 | [57-check-rest-boolean-parity.md](./57-check-rest-boolean-parity.md) | Sub-cohort REST surface |
| 58 | #36 | [58-check-no-sql-ddl-in-ui-folder.md](./58-check-no-sql-ddl-in-ui-folder.md) | Boundary / scope perimeter (§24) |
| 59 | #37 | [59-check-no-ci-yaml-in-issues-folder.md](./59-check-no-ci-yaml-in-issues-folder.md) | Boundary / scope perimeter (§25) |
| 60 | #38 | [60-check-no-toolchain-enum-in-issues-folder.md](./60-check-no-toolchain-enum-in-issues-folder.md) | Boundary / scope perimeter (§25) |
| 61 | #39 | [61-check-no-out-of-scope-spec-folder-link.md](./61-check-no-out-of-scope-spec-folder-link.md) | Boundary / scope perimeter (locked-7) |
| 62 | #40 | [62-check-ci-cli-self-test-harness.md](./62-check-ci-cli-self-test-harness.md) | §28 self-test harness |
| 63 | #41 | [63-check-diagram-parity.md](./63-check-diagram-parity.md) | §26 diagram parity |
| 64 | #42 | [64-meta-verify-lockstep.md](./64-meta-verify-lockstep.md) | Meta gate (audits §27 itself) |
| 65 | #43 | [65-check-gate-ledger-vs-workflow.md](./65-check-gate-ledger-vs-workflow.md) | Meta gate (audits §27 itself) |
| 80 | (carrier for #17) | [80-lib-fixture-replay.md](./80-lib-fixture-replay.md) | Shared self-test harness library |

**Reverse lookup (gate # → slot).** Read the table top-to-bottom; the gate column is monotonic except for the §99-freshness pair (slot 27 = #16 then slot 28 = #17 then slot 29 = #19 — gate #18 is reserved/retired per `00-overview.md` retired-gate list). Slots 01-26 + 30-35 + 40-41 + 70-71 are tier-2 carriers or pre-numbered-gate validators (no gate # assignment) and continue to live under the categorical inventory above.

**Active count parity.** 28 active-gate rows above + the 26 active-gate count in `00-overview.md` differ because the overview counts **distinct gate numbers** (#16..#43 minus retired #18, #44 reserved) while the slot index counts **slot files that ship an active gate**. Slot 36 and slot 29 both bind to gate #19 historically (slot 29 = version-parity, slot 36 = ADS-boundaries) — overview consolidates this into one gate number; slot index keeps the file row distinct. This off-by-N is **expected and intentional**, not drift.

---

**Per-gate slot doc anatomy** (canonical sections, mirrored across all slot files):
1. Status banner (`Active gate #N (Phase / Sess-NN tag)`)
2. Purpose + 1-paragraph "what does this gate guarantee?"
3. Clauses (numbered, each with Given/When/Then)
4. R5 anchor (vacuous-pass condition)
5. Self-test fixture roster (F-1..F-N)
6. CI invocation block (workflow step name, `--self-test` + live disk)
7. Failure modes + invalidation triggers
8. Cross-references to consumed/produced files

---

### Navigation-quintet inline cross-reference convention (B-16, Sess-69)

> **Purpose.** Surface the §27 navigation quintet (**AC-T-30, AC-T-31, AC-T-36, AC-T-37, AC-T-38**) inside every active-gate slot file's frontmatter so a context-bounded reader (Raw-LLM persona, single context window, no file-tool access) sees the full navigation contract without traversing to `97-acceptance-criteria.md`. Today, a Raw-LLM walker landing on any one of the 28 active-gate slot files learns the slot's own contract but cannot see how it composes with the four other navigation ACs without a ≥ 1-hop traversal. This convention collapses that traversal to **0 hops** by inlining the quintet into the frontmatter axis_rationale row. Lifts §27 R-band C4 (Consistency) **+3** when applied across all 28 active-gate slot files (mass-edit gated on B-20-impl per slot 66 schema floor).

> **Why this convention lives in the bundle, not in §97.** Per Lesson #36 ("link, don't restate"), the AC-T-30/-31/-36/-37/-38 bodies remain authoritative in §97; this convention pins only the **placement contract** for their cross-references in slot frontmatter. The bundle is the correct surface because (a) the bundle already pins the per-gate slot doc anatomy above, and (b) the navigation quintet is itself a tier-1 contract surface (each AC is delegated_from one of the four tier-1 files). Per AC-T-38 reverse-coverage invariant, no normative cross-gate contract may land outside tier-1 — this convention sits inside the tier-1 bundle file precisely to satisfy that invariant.

#### The 5-AC navigation quintet (recap)

| AC | Subject | Tier-1 surface pinned |
|---|---|---|
| **AC-T-30** | Slot delegation map (every active-gate slot must have a `delegates_from_ac` row pointing to its owning AC) | `97-acceptance-criteria.md` Slot Delegation Map section |
| **AC-T-31** | Per-slot reflexivity (Lesson #15 — every active-gate slot doc must self-cite as its own enforcement mechanism) | per-slot `Mechanically enforced by:` row |
| **AC-T-36** | Gate-↔-slot binding map (4-way parity: disk grep ↔ binding table ↔ §00/§98/§99 banner literal) | `00-gate-slot-binding.md` table |
| **AC-T-37** | Banner-triple lockstep four-way parity (gate-#42 clause-5 cite chain) | §00 + §97 + §98 + §99 banner version triple |
| **AC-T-38** | Tier-1 bundle reverse-coverage invariant (no normative cross-gate contract outside tier-1) | this very `00-tier1-bundle.md` file |

#### Frontmatter inline cross-reference contract (5 clauses)

Every active-gate slot file (the 28 rows above in the Tier-2 slot index lookup table) MUST inline the navigation quintet under a dedicated `navigation_quintet` frontmatter key. The key value is a YAML inline-list of the 5 AC-IDs in canonical order. Worked example (the canonical shape any active-gate slot file SHOULD adopt):

```yaml
---
kind: gate-spec
axis: <slot's own axis>
axis_rationale: "<slot's own rationale, ≥ 20 chars>"
delegates_from_ac: <slot's owning AC, e.g. AC-T-39 for slot 64>
mechanically_enforced_by: linter-scripts/<slot's script>
navigation_quintet: [AC-T-30, AC-T-31, AC-T-36, AC-T-37, AC-T-38]
---
```

**5-clause contract:**

1. **Presence.** The `navigation_quintet` key MUST be present in every active-gate slot file's frontmatter. Carve-out: the 7 module-level surfaces exempt under slot 66 U-1 (overview, bundle, binding, decomposition, AC, changelog, consistency-report) DO NOT carry this key — they ARE the navigation surfaces being cited, so a self-citation would be circular.
2. **Canonical order.** The 5 AC-IDs MUST appear in the order: `AC-T-30, AC-T-31, AC-T-36, AC-T-37, AC-T-38`. Reordering fails the convention. The order encodes the navigation read-flow: slot delegation (T-30) → reflexivity (T-31) → binding map (T-36) → banner-triple (T-37) → tier-1 reverse-coverage (T-38).
3. **Closed set.** Exactly these 5 AC-IDs. Adding a 6th (even a related navigation AC) fails — the quintet is a frozen anchor; extension requires a `navigation-quintet` → `navigation-sextet` migration spec authored same PR as the new AC.
4. **No restate.** Slot files MUST NOT restate the AC bodies in their own prose (Lesson #36). The frontmatter inline-list is the **only** permitted surface; any `## Navigation` or similar section in slot body that duplicates AC-T-30..-38 text fails the convention.
5. **Reverse coverage.** Every AC in the quintet MUST appear in **at least 1** active-gate slot's `navigation_quintet` row (after mass-edit lands). Reverse-coverage failure (an AC silently dropped from all slots) MUST be flagged by the next §99 entry. Today, reverse coverage is 0/5 (mass-edit not landed); post-B-16-impl it MUST be 28/5 (every slot cites every AC).

#### Phased rollout (today's spec-only authorship → mass-edit gated)

- **Sess-69 B-16 (today)**: convention authored in this sub-section. Reviewer attestation only. **No slot file modified.** §27 R-band C4 lifts +1 (cited mechanism: this 5-clause contract + worked-example YAML in `00-tier1-bundle.md` v1.2.0 body).
- **B-16-impl** *(deferred-implement; do NOT propose without explicit user "implement" turn)*: mass-edit across the 28 active-gate slot files inserting the `navigation_quintet` frontmatter row. Gated on B-20-impl landing first (slot 66 / gate #44 must be active to validate the schema during the mass-edit, otherwise the mass-edit could itself introduce drift). Post-B-16-impl: §27 R-band C4 +3 cumulative (today's +1 → +3 once 28/28 coverage holds on disk and gate #44 enforces it as a hard CI fail). Combined with B-20-impl C4 +3, total C4 trajectory: 13 → 16 (B-20-impl) → 18 (B-16-impl, band-anchor reached).

#### Worked-example bash verifier sketch (post-B-16-impl + B-20-impl)

```bash
# Reverse-coverage invariant (clause 5): every AC in the quintet appears in ≥ 1 active-gate slot.
for ac in AC-T-30 AC-T-31 AC-T-36 AC-T-37 AC-T-38; do
  count=$(grep -lE "navigation_quintet:.*${ac}" spec/27-spec-toolchain/[0-9][0-9]-*.md 2>/dev/null | wc -l)
  test "$count" -ge 1 || echo "FAIL: $ac has 0/28 active-gate slot citations (clause 5 reverse-coverage)"
done

# Presence invariant (clause 1): every active-gate slot file carries the key.
active_slots=$(grep -lE '^\*\*Status:\*\*\s+Active\s+gate\s+#' spec/27-spec-toolchain/*.md | sort)
keyed_slots=$(grep -lE '^navigation_quintet:' spec/27-spec-toolchain/*.md | sort)
comm -23 <(echo "$active_slots") <(echo "$keyed_slots") | tee /dev/stderr | wc -l \
  | xargs -I{} test {} -eq 0 || echo "FAIL: clause 1 presence — N slots missing navigation_quintet key"
```

This sketch is the candidate body for slot 66 / gate #44 clause-5 extension at B-20-impl + B-16-impl landing, hard-failing CI on either presence or reverse-coverage drift.

---

## Tier-3 — Specialised / archival (read only for the named purpose)

| File | Lines | Purpose | When to read |
|---|---|---|---|
| [`98-changelog.md`](./98-changelog.md) | 1,080 | Full version history of the toolchain (every banner since v1.0) | Spec-history archaeology only. Never required for current work — current state lives in §99. |
| `60-forbidden-strings-toml.md` | 85 | Forbidden-string list source | Read when adding a new forbidden literal to the perimeter. |
| `61-spec-cross-links-allowlist.md` | 71 | Allowlist for clauses that intentionally cross the perimeter | Read when adding a new cross-link exemption. |
| `62-spec-folder-refs-allowlist.md` | 86 | Allowlist for spec-folder reference checker | Read when adding a new folder-ref exemption. |
| `63-readme-cross-links-md.md` | 44 | README cross-link spec | Read when editing the repo README. |
| `40-run-sh.md` | 66 | `run.sh` runner stub spec | Read when editing the runner. |
| `41-run-ps1.md` | 59 | `run.ps1` runner stub spec | Read when editing the PowerShell runner. |
| `70-spec-health-yml.md` | 86 | `spec-health.yml` workflow spec | Read when editing the health workflow contract. |
| `71-spec-monthly-audit-yml.md` | 89 | `spec-monthly-audit.yml` workflow spec | Read when editing the monthly audit workflow contract. |
| `80-lib-fixture-replay.md` | 85 | Shared fixture-replay helper spec | Read when factoring fixtures across slot self-tests. |

---

## Reader pre-flight checklist (per persona)

| Persona | Read order | Stop reading after | Navigation guarantee |
|---|---|---|---|
| **Raw-LLM** (single context window) | Tier-1 only | After file 4 (`99-consistency-report.md`) | High for "what is §27, what gates exist, what is open right now". To work on a specific gate, request a follow-up turn that loads only the relevant slot doc + the cohort it audits. |
| **Cursor / Claude-Code** (file access + shell) | Tier-1 in order, then load tier-2 slot doc(s) on demand | When the gate under work is covered | Very high; meta-gates (slots 64, 65) catch drift in real time. |
| **Lovable** (full agent + Cloud + UI preview) | Tier-1 as primer, jump to whichever tier-2 the current sub-task names | n/a — agent re-loads files on demand | Very high; same as Cursor. |

---

## Walker-cost reflexivity (load-budget pin)

**Mirror-septet anchor closure citation.** As of Sess-79 B-27-§26, all 7 in-scope cohorts (§22 + §23 + §24 + §25 + §26 + §27 + §28) cite walker-cost reflexivity in their tier-1 manifests. §27 was the originating cohort (Sess-71 B-27 introduced the lever on `00-raw-llm-bottleneck-decomposition.md` per-criterion table) but did NOT carry the column on this file's Tier-1 table until this turn — Sess-80 B-33 closes that asymmetry.

**Reflexive claim.** This manifest is itself the load-proven artefact for its own friction claim: a Raw-LLM auditor walking §27 with a Tier-1 bundle cap (~30 KB per `mem://constraints/...` Tier-1 budget heuristics) can pre-budget which files to open against the per-file byte-costs in the Tier-1 table (column 4) before opening any cited surface. The Σ ~419 KB total is **far above** any single-walker 30 KB cap (the largest in-scope cohort by tier-1 KB; §27 §99 alone is ~185 KB ≈ 617% of cap). Sub-task pre-budgeting is therefore mandatory, not optional, for the Raw-LLM persona.

| Tier | Files | Σ KB | Role |
|---|---|---|---|
| Tier-1 #1 | `00-overview.md` | ~83 | Module pin + invariants — ~277% of cap → mandatory 3-pass walk on its own |
| Tier-1 #2 | `trace-map.md` | ~50 | Gate dependency DAG — ~167% of cap → 2-pass walk |
| Tier-1 #3 | `97-acceptance-criteria.md` | ~101 | AC aggregator — ~337% of cap → mandatory 4-pass walk |
| Tier-1 #4 | `99-consistency-report.md` | ~185 | Per-session ledger tail (largest §99 in any cohort) — ~617% of cap → mandatory 7-pass walk on its own |
| **Σ tier-1** | **(4 normative files)** | **~419** | **~1397% of cap → mandatory 14-pass walk, ordered §00 → trace-map → §97 → §99 per Tier-1 read-order rationale** |

**Pre-budget recipes** (closed set, mirror of §22/§23/§24/§25/§26/§28):

- **Verify-an-AC** (auditor confirming a single `AC-T-*` clause): load Tier-1 #3 sub-slice via section anchor (~5-15 KB per AC body) + #1 invariants tail (~10 KB) ≈ **~15-25 KB** (1-pass walk; the section-anchor sub-slice is the dominant friction-reducer here since §97 alone is 337% of cap).
- **Trace-a-gate-dependency** (auditor tracking which gate runs before which): load Tier-1 #2 ≈ **~50 KB** (~167% of cap → 2-pass walk; the trace-map is self-contained).
- **Decode-current-state** (auditor checking spec-version frontier or open tickets): load Tier-1 #4 newest-banner block (~10 KB sub-slice via "Module version:" anchor) ≈ **~10 KB** (~33% of cap → 1-pass walk; the §99 tail is the only safe sub-slice — full §99 read is forbidden by walker-cap).
- **Full tier-1 read** (new contributor onboarding): load entire tier-1 set ≈ **~419 KB** (~1397% of cap → mandatory 14-pass walk, ordered §00 → trace-map → §97 → §99 per Tier-1 read-order rationale; **§27 is the largest in-scope cohort by tier-1 KB and the most acute pre-budgeting target**).

**Why this lifts C6, not C4** (mirror of all prior B-27-§N explanations): friction is the cost of finding the right surface; C6 measures that cost. The byte-cost annotations on each tier-1 file reduce guess-cost — the textbook C6 lever per the Rubric v2 band-anchor definition. C4 (Consistency) is unaffected — the AC source remains the single source of truth.

**§27-specific note:** §27 has the **most extreme byte-distribution** of any in-scope cohort: §99 alone (~185 KB) is larger than the entire tier-1 footprint of §22 (~119 KB) or §28 (~136 KB). This is structural — §27 is the meta-cohort and accumulates per-session ledger entries from every other cohort's banner-triple lockstep. The "decode-current-state" recipe is therefore the highest-frequency Raw-LLM walk and **mandatorily** uses the §99 newest-banner-block sub-slice anchor (~10 KB) rather than a full §99 load (forbidden by walker-cap).

**Long-tail ceiling (16 → 17 mirror-septet anchor citation lever)**: §27 C6 was at 16 from Sess-71 B-27 (Tier-2 slot-index lookup table + drift-contract clause + walker-cost column on the bottleneck-decomposition file). This turn adds a **fourth cited mechanism**: walker-cost reflexivity column on this file's Tier-1 table itself (was previously only on the bottleneck-decomposition per-criterion table) **plus** the mirror-septet anchor closure citation as a **fifth cited mechanism** (the cross-cohort lever is now fully anchored — every spec/22..28 cohort has the column, and §27 closes its asymmetry by carrying the column itself). C6 16 → **17** band-anchor advance. C6 → 18 ceiling deferred to a future cross-cohort gate that mechanically verifies the carriers-exclusion glob across all 7 spec cohorts (long-tail `-impl`, out of scope per `mem://constraints/no-implementation-suggestions`); C6 → 19/20 deferred to a per-criterion walker-cost drift gate extending gate #42 clause-5 to recompute KB-costs against on-disk file sizes (long-tail `-impl`, also out of scope).

**Drift contract** (reflexive): if any tier-1 file's `wc -c` changes by ≥10 KB, the per-file byte-cost column above MUST be refreshed in the same PR. Reviewer-attestation today; gate #42 banner-triple lockstep already detects banner-version drift on §00 / §98 / §99 (this manifest's banner is bumped manually in the same PR). Note: §27 §99 grows on every session (per-session ledger tail) — the byte-cost column above is a **moving target** more than for any other cohort. Refresh cadence: every 5th `-stamp-bump` on §99 OR any single bump that pushes §99 past a 10 KB bucket boundary, whichever first.

---

## Drift contract (Lesson #36 + Lesson #15 reflexivity)

- **Add or retire a gate** → update both the relevant tier-2 category row here AND the Active Gate Inventory in `00-overview.md` in the same commit. Failure to do so MUST be flagged by the next §99 entry.
- **Add a new tier-3 file class** (e.g. a new runner stub) → add a row to the tier-3 table here in the same commit.
- **Tier-1 footprint MUST stay ≤ 1,800 lines** (the soft Raw-LLM ceiling for a meta-module). Breach triggers a tier-1 candidate-removal review in the same commit. Note: this ceiling is intentionally tighter than §22's 2,500 because §27 is a meta-module — its tier-1 should be navigation-only, not contract-bearing.
- **Forbidden:** introducing a new normative cross-gate contract in any tier-2 / tier-3 file that is not also surfaced (by reference) in tier-1. The four tier-1 files pin the cross-gate contract surface; per-slot files pin only their own gate.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Gate dependency trace map](./trace-map.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [§22 tier-1 essential bundle](../22-git-logs-v2/00-tier1-bundle.md) — sibling navigation-aid for §22 (Sess-67 B-1)
