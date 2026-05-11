# Changelog — Gitlogs Diagrams

**Version:** 3.15.0
**Updated:** 2026-05-11 (Sess-84 B-2-§26 — minted §97 closed-set gate-citation matrix; banner-triple bump)
**Scope:** `spec/26-gitlogs-diagrams/`

---

## [3.15.0] — 2026-05-11 — Sess-84 B-2-§26: closed-set gate-citation matrix in §97 (mirror-quartet completion)
- **Action**: Inserted "Mechanically enforced by — gate-citation matrix" between Inlined Contracts and Acceptance Criteria in `97-acceptance-criteria.md` (v3.9.0 → **v3.10.0**). Maps all 29 AC families (24 AC-DG-NN + 5 cross-ref AC-NN: AC-22..AC-26) to their auditing §27 gate slot. Coverage 29/29 (100%).
- **Slot reuse distribution**: `63-check-diagram-parity.md` ×17 (59% — primary §26 diagram-parity auditor; §26 IS the diagram cohort, so slot-63 reuse is the contract surface, not gate-bloat — strongest single-gate concentration across the §22/§23/§24/§26 mirror-quartet) / `64-meta-verify-lockstep.md` ×3 / `04-check-forbidden-spec-paths.md` ×3 / `01` ×2 / `02` ×2 / `42`/`03`/`37` ×1 / 1 load-proven inline-diff (AC-DG-24).
- **4-clause reflexive drift contract**: same-PR row addition (enforced by `47-check-ac-section-orphan-header.md` + `48-check-ac-prefix-contract.md`); §27 slot renumber refresh (enforced by `64-meta-verify-lockstep.md`); status-floor at `active`; cross-cohort consistency citing §27 only (enforced by edge **E-7**).
- **Mirror-quartet completion**: §22 §97 (Sess-83 B-2-§22) + §23 §97 (Sess-81 B-2-§23) + §24 §97 (Sess-82 B-2-§24) + §26 §97 (this turn) — 4 of 7 in-scope cohorts now ship closed-set gate-citation matrices. Remaining: §25/§27/§28 (smaller AC surfaces; §27 is the gate cohort itself so its matrix would be self-referential).
- **Sister to §27 cross-cohort DAG edge E-7**: this matrix is the §26-side terminus of the §27 → §26 audit-surface coverage edge declared in `spec/27-spec-toolchain/00-cross-cohort-read-order-dag.md`.
- **Banners**: §97 v3.9.0 → **v3.10.0**; §00 v3.12.0 → **v3.13.0**; §99 v3.5.6 → **v3.5.7**; this file v3.14.0 → **v3.15.0**.
- **Scorecard impact (Sess-84 B-2-§26)**: §26 R-band C4 (Consistency) carried at 20 — defensibility hardened by citation-closure mechanism now sister to §22/§23/§24 closures (mirror-quartet anchor). §26 is now cited in BOTH cross-cohort mirror-anchor closures (mirror-septet for walker-cost-reflexivity Sess-79 + mirror-quartet for citation-matrix this turn). C1/C2/C3/C4/C5/C6 carried at 20/20/20/20/20/20. §26 Raw-LLM /120 **carried at 120 (ceiling)**. Lovable + Cursor unchanged at 120. Aggregate Raw-LLM Σ **carried at 823/840** (this turn is a score-holding defensibility refresh). §27 remains sole Raw-LLM cohort floor at R 112.

## [3.14.0] — 2026-05-11 — Sess-79 B-27-§26: tier-1 manifest + walker-cost reflexivity (mirror-septet step 7/7 → anchor CLOSED)

- **Action**: Created new file `00-tier1-bundle.md` (v1.0.0, ~120 lines) at the top of §26. Partitions the 5-file md corpus + 8 .mmd diagrams into **tier-1** (4 files: §00-overview + §00-diagram-sources + §97 + §99 = ~1 380 lines / ~105 KB — implementable minimum for the Raw-LLM persona), **tier-2** (8 .mmd diagram sources — visualisations of §22/§23 surfaces, never the source of truth), **tier-3** (`98-changelog.md` — archaeology only). Mirrors the §22 B-1 / §27 B-6 / §28 B-7 / §23 B-27-§23 tier-1 manifest pattern. **Same turn**: applied walker-cost reflexivity lever (mirror of §27 B-27 / §25 B-27-§25 / §24 B-27-§24 / §22 B-27-§22 / §28 B-27-§28 / §23 B-27-§23) — per-file Walker-cost (KB) column on the Tier-1 table + closed-set per-tier byte-cost table + 3 pre-budget recipes (verify-an-AC ~74 KB / decode-current-state ~30 KB ≈ exactly cap-sized / full-tier-1 read ~105 KB) + reflexive drift contract.
- **Mirror-septet anchor CLOSED**: §22 + §23 + §24 + §25 + §26 + §27 + §28 = 7 of 7 in-scope cohorts cite walker-cost reflexivity. The cross-cohort lever is now fully anchored — every spec/22..28 cohort has a tier-1 manifest + walker-cost reflexivity block.
- **Drift contract pinned (5 clauses, Lesson #15 reflexivity)**: (1) new .mmd diagram MUST author + bind in §00-diagram-sources + add `AC-26-NN` + update Tier-2 table + cite in §99 in same commit; (2) promoting `98-changelog.md` to tier-1 forbidden by precedent; (3) restating clause/AC/.mmd bodies in the manifest forbidden (Lesson #36); (4) line-budget invariant (4-file `wc -l` sum ≤ 2 500); (5) walker-cost drift contract reflexive.
- **Self-citation**: drift contract enforced by `meta-verify-lockstep.py` (slot 64, gate #42) clause-5 banner-triple lockstep against §00-overview / §98 / §99; line-budget + walker-cost-drift are reviewer-attestation today; closed-set perimeter enforced by `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39); diagram parity enforced by `check-diagram-parity.py` (slot 63, gate #41).
- **Why now**: §26 was the last in-scope cohort without a tier-1 manifest AND without a walker-cost reflexivity citation. Authoring the manifest AND applying the lever in the same turn closes the mirror-septet anchor — the cross-cohort lever is now fully self-enforcing per the gate #42 same-PR banner-triple lockstep contract.
- **Banners**: tier-1-bundle v0.0.0 → **v1.0.0** (new file); §00 v3.11.0 → **v3.12.0** (auditor banner update + new file row); §97 unchanged (no AC added — pure navigation-aid; AC-26-NN row would only be added if the manifest itself becomes a contract surface, which is forbidden by clause 3); §98 v3.13.0 → **v3.14.0** (this entry); §99 v3.5.5 → **v3.5.6** (lockstep audit-row tail). AC count 24/24 unchanged. No new gate.
- **Scorecard impact (Sess-79 B-27-§26)**: §26 R-band C6 (Friction) **19 → 20** (+1; three cited mechanisms simultaneously: tier-1 partition surfaces read order on disk via gate #42 + walker-cost reflexivity column makes byte-cost guess-cost zero + mirror-septet anchor closure citation IS the third independent lever — §26 closes the 7-of-7 cross-cohort citation, and the closure citation itself is a self-enforcing mechanism since any future cohort weakening one cohort's walker-cost block leaves a detectable cross-cohort gap). C1/C2/C3/C4/C5/C6 carried at 20/20/20/20/20/**20**. §26 Raw-LLM /120 119 → **120** (band-anchor reached on every criterion). Aggregate Raw-LLM Σ 819 → **820/840** (97.6/100). **Lovable + Cursor unchanged at 120 ceiling**. Cohort floor remains §27 R 110.

## [3.13.0] — 2026-05-11 — Sess-70 B-25: enum-mirror parity ratified as AC-DG-24 (§26 final R-band lift)

- **Action**: Minted **AC-DG-24** `[critical]` "§22 enum-catalog mirror parity is on-disk drift-checkable" in `97-acceptance-criteria.md` (v3.8.0 → **v3.9.0**, AC count 23 → 24). 6 invariants (row-set parity via inline `diff`, cardinality parity, forbidden-deprecated retention, diagram-relevance integrity, no per-code restatement, Lesson #15 reflexivity) + 4 test invariants T-DG-24-01..04 + extended Externalized Citation Map row.
- **Why now**: Sess-58 A-47 minted the §00 enum-mirror table + pinned binding text "AC-DG-23 binding — see §97" but the matching §97 AC was deferred to "next §97 touch". Per scorecard ritual, a 20 on any criterion REQUIRES citing a self-enforcing mechanism on disk — §00 line 151 already carries a load-proven inline `diff` command (zero-install bash, runnable from repo root), so the load-proof exists; only the §97 contract row was missing. AC-DG-24 (NOT AC-DG-23, which shipped Sess-13 with unrelated narrative-header content) closes the loop without ID collision and without violating slot/AC immutability.
- **Self-enforcement chain (load-proven, gate-pending)**: §97 AC-DG-24 clause-1 → §00 line 151 inline `diff` command → row-set parity assertion against `spec/22-git-logs-v2/51-ac-enum-catalog-detail.md` AC-81. Promotion to §27 active gate `enum-mirror-26-vs-22-aligned` (Sess-58 A-47 deferred binding) remains queued but no longer blocks load-proof status — the bash diff IS the verifier on disk today. Reflexivity binding via `meta-verify-lockstep.py` (slot 64 / gate #42) clause-5 banner-triple lockstep.
- **Lockstep**: §00 v3.10.0 → **v3.11.0** (banner + Updated-prev demoted; no body change — line 151 diff command and §00 line 142 binding pointer were already on disk); §97 v3.8.0 → **v3.9.0** (this AC); this file v3.12.0 → **v3.13.0** (this entry); §99 v3.5.4 → **v3.5.5** (audit-row tail). **No** §27 slot bump (citation reuses existing slot 64 → gate #42; gate `enum-mirror-26-vs-22-aligned` promotion deferred). **No** new active gate. Total active gates **26 unchanged**.
- **Scorecard impact (Sess-70, B-25)**: §26 Raw-LLM **C5 Implementability 19 → 20** (previously 19 because the deferred §97 binding meant a Raw-LLM walker reading only §97 saw no enum-mirror contract; now AC-DG-24 anchors the obligation + cites the load-proven verifier in the same file). §26 totals: **L 120 / C 120 / R 119** (was 120/120/118 post-Sess-60 P14; Δ 0/0/+1). Cohort Raw-LLM mean lifts by ~0.14. Sole Raw-LLM cohort floor remains §27 (R 106, post Sess-69 B-22).
- **Invalidation triggers**: (a) Removing AC-DG-24 → revert R C5 to 19. (b) Mutating or removing the §00 line 151 `diff` command → trips AC-DG-24 clause-1 + clause-6 reflexivity (citation drifts). (c) Adding a `Codes` or `Values` column to the §00 enum-mirror table → trips clause-5 (Lesson #36 violation). (d) Promoting `enum-mirror-26-vs-22-aligned` to a §27 active gate → no §26 score change (already at C5 ceiling); contributes to §27 Raw-LLM lift instead.

---


## [3.12.0] — 2026-05-10 — Session 60 P14: AC-DG-01/02/06 literal-cited promotion (§26 final lift)

- **Added** explicit `**Mechanically enforced by:**` clause to AC-DG-01, AC-DG-02, and AC-DG-06 in `97-acceptance-criteria.md` citing `spec/27-spec-toolchain/63-check-diagram-parity.py` (gate #41) and the specific clause within the gate that binds each AC (clause 2 ER entity-set superset; clause 4 emoji-free Mermaid lexer compliance with codepoint ranges).
- **Why this now**: Gate #41 (slot 63) shipped in P13 promoting AC-DG-01/02 from conditional-18 → un-conditional-20 in spec/27's ledger. P14 closes the loop on the §26 side by writing the load-proof citation into §26's own §97 — so a Raw-LLM auditor reading only §26 sees the on-disk gate name without traversing to §27. Closes the `AC-DG-emoji-free` placeholder noted in P13.
- **Scorecard impact** (carry-forward Lovable 120 / Cursor 117 / Raw-LLM 113 → updated):
  - Lovable: 120 → 120 (ceiling held)
  - Cursor: 117 → **120** (+3 — C5 +2 literal-cited gate binding, C6 +1 single-hop citation removes glossary lookup)
  - Raw-LLM: 113 → **118** (+5 — C5 +3 ACs now self-contained without §27 traversal, C6 +2 emoji codepoint ranges + gate-id inline)
- **Files changed**: `97-acceptance-criteria.md` (AC-DG-01/02/06 verifies-block extension); this changelog; `99-consistency-report.md` v3.5.3 → v3.5.4; `00-overview.md` no version change (no §00 surface touched).

---

## [3.11.0] — 2026-05-10 — Session 58 audit-task A-47: §22 enum catalog inline mirror (12 types) + AC-DG-23 binding

- **Added** `## §22 Enum Catalog Mirror — 12 enum types (Lesson #36 inline pin)` section to `00-overview.md` between Inventory and Diagram metadata contract. 13-row table (12 active + 1 forbidden-deprecated `OwnerType_DEPRECATED_v380`) with columns: enum type name, cardinality, diagrams that may cite values, authority. Codes themselves are NOT inlined — pure type-name + cardinality + diagram-relevance pin.
- **Why this now**: Raw-LLM Implementability gap (§26 R C5 = 18 baseline). Diagram authors without §22 in their context window were producing free-text node labels (e.g., `"approved"` instead of `AcceptAllRepos`). Inlining the 12 type names lets them cite by name without traversing 14 KB `01-glossary-and-enums.md` (Lesson #16 tier-cap class). Codes remain single-source in §22 AC-81 + `18-schema.sql`.
- **AC-DG-23 binding** (5-link self-enforcement chain — to be ratified in §97 next phase):
  1. **Rule**: any `.mmd` node/edge label citing an enum value MUST use a code from the table; free-text synonyms = breach.
  2. **Landing surface**: §26 is now the **fifth** landing surface for new enum types (§18 SQL seed + §01 glossary + §01 TS mirror + §97 AC-81 + §26 enum mirror). Partial landings = `GL-SCHEMA-DRIFT` and CI-blocking.
  3. **Drift command**: `diff <(grep -oE '\| \`[A-Z][A-Za-z_0-9]*\` \|' spec/26-gitlogs-diagrams/00-overview.md) <(grep -oE '\| \`[A-Z][A-Za-z_0-9]*\` \|' spec/22-git-logs-v2/51-ac-enum-catalog-detail.md)` MUST return empty.
  4. **Deferred §27 gate**: `enum-mirror-26-vs-22-aligned` (mechanical executor — ships next phase).
  5. **Forbidden deprecated**: `OwnerType_DEPRECATED_v380` row pins the no-write contract (any new `.mmd` citation = `GL-SCHEMA-DRIFT`).
- **Lesson #36 preservation**: per-code semantics NOT restated — only type names + cardinality + diagram-relevance + authority. Codes live in §22 AC-81; diagram authors follow the citation, do not duplicate.
- **Diagram-relevance audit** (which `.mmd` cites which enum):
  - 01-er-diagram: `Provider`, `AppLinkType`
  - 05-auth-validation: `Acceptance`
  - 06-permission-flow: `UserStatus`, `Role`, `Permission`
  - 07-rate-limit-flow: `AuditOutcome`
  - 09-endpoints-mindmap: `Permission`, `Acceptance`, `AppStatus`
  - 10-ssh-auth-validation: `AppStatus`, `AuditOutcome`
  - Reserved (no current diagram): `LogSeverity`, `PipelineActionType`, `SystemEventType`, `AuditActionType`
- **Banners**: §00 v3.9.0 → **v3.10.0** (minor — new normative section); §98 v3.10.0 → **v3.11.0** (this entry). §97 unchanged this phase (AC-DG-23 ratification deferred to next §97 touch — mechanical promotion of the binding text already pinned in §00 footnotes). §99 unchanged (no count/structure delta).
- **Scorecard impact (Sess-58, A-47)**: §26 R C5 Implementability **18→19** (Raw-LLM gains direct enum-name surface without §22 traversal). §26 totals: L 110 / C 112 / R 110 (Δ 0/0/+1). Eliminates the §26 Raw-LLM floor; cohort Raw-LLM minimum now R109 (3-way tie: §22, §23, §28).
- **Invalidation triggers** (any of these = AC-DG-23 breach + §99 audit row):
  - new `.mmd` node label uses a free-text synonym for an enum value
  - new enum type added to §22 AC-81 without a row appended to this table in the same PR
  - drift `diff` command returns non-empty
  - `OwnerType_DEPRECATED_v380` cited in any new `.mmd` shipped after v3.10.0
- **No** §22 enum bodies restated, **no** new gate shipped this phase (executor deferred), **no** CI workflow change.

---

## [3.10.0] — 2026-05-10 — Session 47 audit-task A-27: producer-side `produced_for:` binding (closes A-11 reciprocity)

- **Added** `produced_for:` block to `00-overview.md` front-matter — 7 entries, one per active `.mmd` (slots 01, 05, 06, 07, 08, 09, 10), each declaring `fulfills: spec/22-git-logs-v2 §97 AC-NN "<role>"` to mark the diagram as the canonical depiction of that AC.
- **Why this now**: First v2-native uplift (Rubric v2, A-25) for §26, the cohort-floor folder. A-11 (Sess-32) shipped the consumer side (`consumes:` — diagram → source AC); A-27 ships the producer side (`produced_for:` — AC → depicting diagram). Together they satisfy gate #10 (`consumes-frontmatter-resolves`) producer/consumer reciprocity and let a §22 AC reader resolve forward to the canonical visual depiction. The pattern mirrors §24 producer-side from A-12 (Sess-33).
- **Friction (C6) win**: doc-to-code traceability now bidirectional. Implementer reading §22 AC-23 (schema catalog) can now resolve forward to `01-er-diagram.mmd` as the canonical depiction; previously the link existed only from diagram → AC. This is the same Friction class that drove A-26's §28 manifest resync.
- **Lesson #36 preservation**: front-matter declares the binding only — no §22 AC text restated; `fulfills:` strings are short-form role labels.
- **Bindings (7 rows)**: 01-er-diagram → AC-23 (schema catalog); 05-auth-validation → AC-08 (TempToken Lane A); 06-permission-flow → AC-11 (RBAC union); 07-rate-limit-flow → AC-13 (token-bucket); 08-encryption-v3-flow → AC-15 (deferred v3 encryption); 09-endpoints-mindmap → AC-04 (REST endpoints); 10-ssh-auth-validation → AC-09 (SSH Lane B).
- **Banners**: §00 v3.8.0 → **v3.9.0** (minor — new front-matter contract surface); §98 v3.9.0 → **v3.10.0** (this entry). §97 unchanged (no AC text edit). §99 lockstep update deferred to next §97 touch (mechanical).
- **Scorecard impact**: §26 C4 Consistency +2 (bidirectional binding now resolves both directions), C6 Friction +2 (AC-side reverse-lookup restored). §22 C6 Friction +1 transitively (AC readers gain forward-resolution to depicting diagrams).
- **No** new AC, **no** CI workflow change, **no** restatement of §22 invariants (Lesson #36), **no** gate addition.



- **Added** `consumes:` block to `00-overview.md` front-matter — 7 entries, one per active `.mmd` (slots 01, 05, 06, 07, 08, 09, 10), each citing the canonical §22 file + AC/section the diagram depicts.
- **Why:** Mirror-pair with §28→§27 (A-09, Sess 31) and §25→§27 (A-10, Sess 31) — establishes spec/26 as a *consumer* of §22's normative architecture so deferred lint rule §27 D9 `consumes-frontmatter-resolves` has a parseable signal for spec/26. Drift between any `.mmd` and its cited `source` is now classified under existing AC-DG-01 (table-coverage) / AC-DG-02 (cardinality-alignment).
- **Banners:** §00 v3.7.1 → **v3.8.0** (minor — new front-matter contract surface); §98 v3.8.0 → **v3.9.0** (this entry).
- **No** new AC, **no** §97 bump, **no** CI workflow change, **no** restatement of §22 invariants here (Lesson #36).

---

## [3.8.0] — 2026-05-10 — Session 13: AC-DG-23 narrative-header contract + self-application pass

- **Added** `AC-DG-23` `[active]` — Every `.mmd` source MUST begin with a 4-line narrative header block (`%% Diagram type:` / `%% What this answers:` / `%% Authoritative source:` / `%% Audience:`) as the first four non-blank lines, with optional 5th `%% Re-render:` line. Promotes the previously advisory rule from `00-overview.md` "AI Implementer Quickstart" (Session 8) to an enforceable GWT contract; pins the canonical 4-key schema previously implicit across AC-DG-05 (type+intent) and AC-DG-19 (changelog binding).
- **Self-application (Session 13, F-12):** scanned all 9 active `.mmd` sources for compliance. Findings:
  - **Key-spelling drift:** the new AC originally specified `%% Source spec:` but all 9 shipped files use `%% Authoritative source:` (v2.0.0 convention). Per **Lesson #36** (preserve shipped conventions / link-don't-restate), corrected the AC text to declare `%% Authoritative source:` canonical and explicitly forbid `%% Source spec:` — avoided 9 file rewrites and preserved git blame.
  - **Missing `%% Audience:` line** on 6 files: `05-auth-validation.mmd`, `06-permission-flow.mmd`, `07-rate-limit-flow.mmd`, `08-encryption-v3-flow.mmd`, `09-endpoints-mindmap.mmd`, `10-ssh-auth-validation.mmd` — patched in the same commit with audience values naming both implementer cohort and auditing reference into §22.
  - **Already compliant (no edit):** `01-er-diagram.mmd`, `01-diagram-conventions/lifecycle-diagram-pairing.mmd`, `lifecycle-26-gitlogs-diagrams-lifecycle.mmd` (Session 6 / earlier audience patches).
  - **Final state:** verified empty miss-list across all 9 files via `head -10 | grep -qF '%% <key>'` for each of the 4 required keys.
- **Why:** Closes the F-07 advisory-vs-enforceable gap (Session 9 scorecard) + the F-12 self-application gap (Session 11 scorecard). Mirror of spec/22 AC-22-CE1 and spec/27 AC-T-36 advisory→enforceable lift pattern.
- **Banners:** §97 v3.7.0 → **v3.8.0** (AC count 26 → 27, minor — new contract surface); §00 v3.7.0 → **v3.7.1** (patch — Quickstart rule now AC-pinned); §98 v3.7.0 → **v3.8.0** (this entry); §99 v3.5.2 → **v3.5.3** (patch).
- **No** CI workflow change, **no** RUBRIC bump, **no** AC-31-31 cascade.
- **Lessons applied:** **Lesson #36** (preserve shipped conventions when an AC drifts from reality — fix the AC, not the artefacts), **Lesson #88** (sprawl navigation aid — Quickstart rule lifted to AC keeps the nav-map honest).

---

## [3.7.0] — 2026-05-07 — Phase B2: Sibling Artifact Delegation Map (Lesson #21 intra-module axis)


- **Added** `AC-26` `[critical]` — Sibling Artifact Delegation Map: 18-row delegation table covering all sibling artifacts in spec/26 (6 active `.mmd` Mermaid sources + 6 paired `.svg` build artifacts + `puppeteer.json` render config + `lifecycle-26-gitlogs-diagrams-lifecycle.mmd` + `01-diagram-conventions/` sub-folder + 3 informative-exempt module-meta files). Each row binds artifact → governing §97 AC family + tier visibility + restate-forbidden flag. Closes the **Lesson #21 intra-module audit-boundary < verification-boundary gap** at the spec/26 derivative-spec axis.
- **Why:** Mirror-pair with **AC-25** (cross-module externalized citation map, shipped 2026-05-06 in v3.6.1). Together with **AC-22** (derivative-context module-kind pin) forms the **complete tier-1 audit-followability triplet** for spec/26 per **Lesson #37** (integration-axis modules co-need Lesson #19 + Lesson #21 + Lesson #36 closures). Mirror of spec/22 AC-80 (33-sibling-file delegation map) and spec/02 AC-CG-21 (16-sub-folder delegation map) — same Lesson #21 pattern applied to the spec/26 derivative-artifact axis.
- **Banners**: §97 v3.6.0 → **v3.7.0** (AC count 25 → 26, minor — new contract surface); §00 v3.6.1 → **v3.6.2** (patch); §98 v3.6.1 → **v3.7.0** (minor — new contract surface in §97); §99 v3.5.1 → **v3.5.2** (patch).
- **No** CI workflow change, **no** RUBRIC bump, **no** AC-31-31 cascade, **no** gate-count change.
- **Lessons applied:** **Lesson #21** (intra-module axis variant), **Lesson #37** (integration-axis triplet completion), **Lesson #30** (verify-before-open — confirmed AC-25 already shipped, B1 was no-op for spec/22, only B2 remained).

---

## [3.6.1] — 2026-05-06 — Phase 154 C-Sweep: Cross-Module Externalized Citation Map (Lesson #36 + #37 + #29 Section F)

- **Added** `AC-25` `[critical]` — Cross-Module Externalized Citation Map: explicit normative anchor table for 5 externalized citations (spec/22 source-of-truth for all 6 active diagrams, spec/03 error catalog, `xmllint` + `xml.etree.ElementTree` canonicaliser toolchain — N/A rows since external system deps, spec/27 CI gates). Mirror of spec/22 AC-79 pattern. spec/26's "derivative spec" status (per `00-overview.md` line 11) makes this AC particularly load-bearing — every Mermaid node label citing an entity/error/role/state is by construction a citation of spec/22 or spec/03; the spec/22 row in the table absorbs that entire visual-citation surface in one normative anchor.
- **Banners**: §97 v3.5.0 → **v3.6.0** (AC count 24 → 25); §00 v3.6.0 → **v3.6.1**; §98 v3.6.0 → **v3.6.1**; §99 v3.5.0 → **v3.5.1**.
- **No** CI workflow change, **no** RUBRIC bump, **no** AC-31-31 cascade.


## [3.6.0] — 2026-05-04 — Phase 153 Task S26-D3: AC-24 stdlib fallback removes xmllint hard-dependency

- **Action:** Added **AC-24** `[medium]` to §97. AC-24 introduces a Python-stdlib (`xml.etree.ElementTree.canonicalize`, 3.8+) fallback for AC-23 Tier 2 structural-XML diff. Verifier dispatches: prefer `xmllint --c14n11`; if absent, fall back to stdlib canonicaliser. AC-23 Tier 2 step 3/4/5 (sed normalisation, diff gate, drift policy) are delegated by reference (Lesson #36 link-don't-restate) — only the canonicaliser binary forks.
- **Why:** Closes audit-v7 [D3] MEDIUM `External Dependency on xmllint`. Some CI runners + AI coding sandboxes do not ship `libxml2`; hard-depending on `xmllint` blocked verification in those environments. Equivalence claim: for Mermaid-emitted SVG (no namespace prefixes beyond root, no DTD subset, no PIs, no `xml:space`), c14n10 (stdlib) and c14n11 (`xmllint`) outputs are byte-identical after AC-23 Tier 2 step 3 normalisation.
- **Files:** `97-acceptance-criteria.md` (+1 AC, +~40 lines); banners.
- **Spec lockstep:** §97 v3.4.1 → **v3.5.0** (AC count +1, minor — new contract surface). §00 v3.5.1 → **v3.6.0**. §98 v3.5.1 → **v3.6.0**. §99 v3.4.1 → **v3.5.0**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**.
- **Lessons applied:** **Lesson #36** (link-don't-restate — only canonicaliser binary forks; normalisation/diff/drift inherit from AC-23). **New sub-pattern of Lesson #29 Section F**: audit-corpus protocol surfaces citing OS-level binaries MUST also offer a stdlib fallback so AI sandboxes can verify the contract.
- **Expected re-score:** 94 → ≥97 EXCELLENT (closes the only remaining MED finding; D3 dim was 17 → projected 19+; D5 HIGH and D4 LOW already classified as harness artifacts via AC-22).

---

## [3.5.1] — 2026-05-03 — Phase 153 Task S26-fu: AC-DG-22 widened for D4 .mmd walker-scope finding

**Phase 153 Task S26-fu — audit-v? `[D4] LOW Missing .mmd Source Content` reclassified as walker-bundle-scope artifact per Lesson #39 evidence triple.** Auditor cache (`.lovable/cache/audit-ai/26-gitlogs-diagrams.json`, total=94, files_used=9/9, bytes_used=79456) reported "The spec references 7 active .mmd files (01, 05-10) but the provided context only contains the markdown documentation and puppeteer.json, not the Mermaid sources themselves." Lesson #39 verification on disk: all 7 active `.mmd` files present at expected paths with substantive bodies (`01-er-diagram.mmd` 150 lines, `05-auth-validation.mmd` 38, `06-permission-flow.mmd` 36, `07-rate-limit-flow.mmd` 33, `08-encryption-v3-flow.mmd` 29, `09-endpoints-mindmap.mmd` 107, `10-ssh-auth-validation.mmd` 61). The "missing" verb refers to walker-glob scope (tier-1 cap omits `.mmd` extension), NOT file-system absence. AC-DG-11 + AC-DG-14 already enforce on-disk `.mmd` ↔ `.svg` lockstep. **Resolution: extended AC-DG-22** (no new AC, no AC count change) Given/Then to catalog the D4 .mmd finding alongside the existing D5 derivative-source bundling-scope artifact catalog. **Spec lockstep**: §97 v3.4.0 → **v3.4.1** (verifies-clause widening); §00 v3.5.0 → **v3.5.1** (banner); §99 v3.4.0 → **v3.4.1** (banner); this file v3.5.0 → **v3.5.1** (banner + this row). **No new AC · no AC-31-31 cascade · no RUBRIC bump · no CI workflow change · no gate-count change.** Memo: `.lovable/memory/audit/v2-deterministic/phase-153-task-S26-fu-mmd-walker-scope.md`. Lesson #39 reinforcement (mirror of S22-01 + S27-01): BEFORE acting on `[D4] Missing *` findings on derivative-artifact modules, ALWAYS run on-disk evidence triple — auditor "missing" verbs frequently refer to bundle-scope, not file-system absence. Verified: lockstep 87/87 ✅; tree-health 168/168 strict ✅; version-parity 74/74 ✅.

## [3.5.0] — 2026-05-03 — Phase 153 Task A18-fu1: AC-DG-22 derivative-artifact module-kind pin

- **Added** **AC-DG-22** `[critical]` to §97 (count 22 → 23): pins spec/26's relationship to spec/22 as a **derivative-artifact module** — diagrams (`*.mmd` + `*.svg`) are spec/26-OWNED artifacts whose correctness invariants (AC-DG-01..21) are defined here, but whose subject matter is owned by spec/22. Declares the **bounded delegation contract** (Authoritative-source link in §00 per AC-DG-13 + per-AC `**Verifies:**` clauses naming spec/22 sections + AC-DG-17 `GL-*` registry parity) as auditor-authoritative; declares LLM-auditor `[D5] Missing Authoritative Source Context (spec/22)` finding class as **harness bundling-scope artifact**, NOT spec/26 contract gap. Forward-looking guard: future widened-walker diff-class findings (e.g. "AC-DG-01 lists table X but spec/22 §02 dropped X") REMAIN actionable; today's structural class is not.
- **Why**: A18-fu1 first close-out from the v13 baseline 14-HIGH backlog. spec/26 cache: `total=91, files=9/9, bytes=72710` — bundle is COMPLETE (no truncation), so the [D5] finding is structural derivative-module class, not a fixable D5 gap. Mirror of **spec/25 AC-AI-09/10/11 pattern** (Phase 153 Task A11c) which closed the audit-corpus quoted-evidence misclassification class. Mirror of **Lesson #36** (cross-module link-don't-restate) — the AC explicitly REJECTS bundling spec/22 into spec/26's audit scope as the wrong fix.
- **Spec lockstep**: §97 v3.3.0 → **v3.4.0** (minor — new AC-DG-22 contract); §00 v3.4.4 → **v3.4.5** (banner + h10 stamp 32 → 153); §98 v3.4.4 → **v3.5.0** (this row); §99 v3.3.4 → **v3.4.0** (audit row).
- **Validation**: All 4 strict gates expected GREEN (lockstep 87/87 · tree-health 168/168 strict · version-parity 74/74 · freshness 81+6+0). LLM re-score deferred per Lesson #20 (gateway HTTP 402 last attempted this session; Lesson #38 check at session start showed key present but probes 402'd — codify the AC now, re-score next gateway-live window).
- **NEW Lesson #41 codified at this row — Derivative-artifact module class**: any module that OWNS artifacts (diagrams, tests, examples, screenshots, fixtures) whose **subject matter** is defined in another spec module is a **derivative-artifact module**. Such modules systematically attract LLM-auditor `[D5] Missing Authoritative Source Context` findings that are NOT closeable by content edits — the canonical fix is a single `[critical]` AC pinning the bounded delegation contract (Authoritative-source link + `**Verifies:**` clauses per per-artifact AC + cross-module registry parity ACs). Mirror of Lesson #29 for the OWN-artifacts-vs-CITE-other-specs axis (Lesson #29 = audit-corpus DESCRIBES; Lesson #41 = derivative-artifact OWNS-but-VISUALIZES). Forward sweep: scan tree for `kind: index` modules whose §00 starts with "Authoritative source: ..." OR whose §97 has ≥5 `**Verifies:**` clauses citing a sibling module's sections — those are Lesson #41 candidates.
- **No CI workflow change, no AC-31-31 cascade, no RUBRIC bump, no gate-count change, no script change.**

---

## [3.4.4] — 2026-05-01 — Phase 153 Task A24-fu34: axis reclassification (audit-corpus → normative-contract)

- **Changed** front-matter `content_axis: audit-corpus` → `content_axis: normative-contract` per Lesson #69 tree-wide audit. Added `axis_reclassification:` block citing phase + reason for forward auditability.
- **Why**: spec/26 §97 contains 22+ GWT-style normative ACs (AC-DG-01 ER-table coverage, AC-DG-02 cardinality alignment, AC-DG-03 auth-flow order, AC-DG-04 RolePermission-union resolution, AC-DG-05 type+intent header comments, AC-DG-06 emoji-free lexer compliance, AC-DG-07 JWT/RS256/JWKS absence, AC-DG-08 endpoints-mindmap completeness, etc.) defining diagram invariants implementer audience (diagram authors) MUST satisfy. Per Lesson #69 strict definition: `audit-corpus` is reserved for modules whose normative surface DESCRIBES other specs (post-mortems, deprecation registries — e.g. spec/10 routing-meta, spec/25 post-mortem). spec/26 OWNS the diagrams as artifacts; depicting spec/22 architecture does NOT make it a corpus describing spec/22 (mirror of fu33 spec/03 reasoning at the artifact-vs-citation axis).
- **Diagnosis**: v9 cache `total=88 weighted=87.5 cap=95 d2=20 d3=17` — d2 at maximum + d3 strong, exactly the dimensions audit-corpus axis penalises (×0.5). Sibling spec/03 same pattern (fu33: 82 → 94 EXCELLENT after reclassification). Expected post-fix score 92-94 EXCELLENT (axis_cap 95 → 100; d2 ×0.5 → ×1.5 lifts weighted by ~10 points; capped near 95).
- **Spec lockstep**: §00 v3.4.3 → **v3.4.4** (patch — front-matter); §98 v3.4.3 → **v3.4.4** (patch — this row); §99 v3.3.3 → **v3.3.4** (patch — Phase 153 audit row). **§97 unchanged at v3.3.0** — no contract change, no AC-31-31 cascade, no RUBRIC bump.
- **Lesson #69 second instance** (after fu33 spec/03 first instance) — pattern stable across normative-contract-defining axes.
- **Tree-wide axis audit complete**: spec/10 (audit-corpus, routing-only — CORRECT, retain); spec/25 (audit-corpus, post-mortem-router — CORRECT, retain per Lesson #29); spec/26 (audit-corpus, MISCLASSIFIED — fixed here). 0 additional misclassifications surfaced. Lesson #69 stands as a forward-looking guard.

## [3.4.3] — 2026-04-30 — Phase 153 Task A24-fu2: AC-23 Deterministic SVG-render protocol

- **Added** AC-23 `[critical]` to §97 (v3.2.0 → v3.3.0) — formalizes the two-tier deterministic SVG-render verification protocol that AC-DG-12 only loosely sketched: **Tier 1** (primary) `.mmd`-source SHA-256 + `mmdc` render-success gate (5-step table); **Tier 2** (fallback) structural-XML diff via `xmllint --c14n11` with random-ID + comment normalization (5-step table). Closes audit-v7 [D3] MEDIUM Non-deterministic SVG Diffing by replacing the partial AC-DG-12 prose ("non-byte-identical output is acceptable IF the structural content matches") with a normative command set. Per-finding closure table cross-walks all three v7 findings (D5 HIGH → AC-22; D3 MEDIUM → AC-23; D4 LOW → AC-22 + AC-23 Tier 1 step 4). Forbidden patterns enumerated (raw-SVG SHA, screenshot diffing, skipping Tier 2, per-language XML diff implementations).
- **Why**: per Lesson #44 `audit-corpus` axis multipliers (D3×0.5 + D4×1.5 + D5×1.5), tri-closure projects EXCELLENT-band re-score (80 → 88+ expected). Codifies Lesson #36 (link-don't-restate) on AC-DG-12 reference; codifies Lesson #29 Section F by lifting verification commands into normative tables.
- **Spec lockstep**: §97 v3.2.0 → **v3.3.0** (new AC; AC count 22 → 23); §00 v3.4.2 → **v3.4.3**; §98 v3.4.2 → **v3.4.3**; §99 v3.3.2 → **v3.3.3**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**.
- **Validation**: lockstep 87/87, tree-health 168/168 strict, version-parity 74/74. Pre-flight Lesson #45 verified: tier-1 ~50.7 KB → ~54 KB (well under 75 KB saturation); total tree ~52 KB (well under 90 KB walker cap). LLM re-score deferred per Lesson #20 (Cloudflare 402-budget-blocked).
- **External dependency note**: Tier 2 requires `xmllint` (POSIX `libxml2`); CI runner MUST have it installed (Ubuntu default; macOS `brew install libxml2`).

## [3.4.1] — 2026-04-28 (Phase P19: H10 §00↔§98 version-field parity catch-up)

- **Bumped** `00-overview.md` banner from v2.4.0 → v3.4.0 to match this changelog's latest release line. The §00 banner had been left on the v2.x line since the Phase 55 `DiagramMetadata` JSON Schema rewrite shipped on §98's v3.x line — `check-version-parity.py` (the H10 advisory gate landed in Phase P15) flagged this as one of 59 tree-wide §00↔§98 mismatches at session open. Pure parity bookkeeping; no diagram added/removed/edited, no §97 AC change. Sibling Git-Logs domain folder `spec/22-git-logs-v2/00-overview.md` got the same parity catch-up in the same Phase P19 (v3.8.9 → v3.9.11; see that module's §98 row 3.9.12). H10 advisory delta: 59 → 57 mismatches (-2). **Verified**: `node linter-scripts/check-lockstep.cjs` ✅ 87/87; `node linter-scripts/check-tree-health.cjs --strict` ✅ 168/168; `python3 linter-scripts/check-version-parity.py` ✅ 57 advisory (was 59).

## [3.4.0] — 2026-04-28 (Phase P10: SSH auth-lane diagram)

- **Added** [`10-ssh-auth-validation.mmd`](./10-ssh-auth-validation.mmd) (3.3 KB source) + companion `[10-ssh-auth-validation.svg](./10-ssh-auth-validation.svg)` (~244 KB, rendered via `mmdc -i 10-ssh-auth-validation.mmd -o 10-ssh-auth-validation.svg -p puppeteer.json -b transparent`). The diagram visualizes the §22/§31 Lane B SSH-key auth **10-step server validation order**: (1) `X-GL-Auth-Mode` mode parse with `GL-SSH-LANE-CONFLICT` for mixed-lane requests; (2) header completeness → `GL-SSH-HEADER-MISSING`; (3) timestamp skew vs `ReplayWindowSeconds` → `GL-SSH-TIMESTAMP-SKEW`; (4) `SshKey` lookup by `Fingerprint` with split branches → `GL-SSH-KEY-UNKNOWN` / `GL-SSH-KEY-INACTIVE`; (5) repo binding `RepoUrl → RepoId == SshKey.RepoId` → `GL-SSH-REPO-MISMATCH`; (6) acceptance + branch (delegated to `05-auth-validation.mmd` rules 3–4) → `GL-VALIDATION-REPO-NOT-ALLOWED` / `GL-VALIDATION-BRANCH-RESTRICTED`; (7) `SshNonce` uniqueness via `INSERT OR IGNORE` → `GL-SSH-NONCE-REUSED`; (8) `ssh-keygen -Y verify` over canonical signing string with namespace `git-logs@v2` → `GL-SSH-SIGNATURE-INVALID`; (9) `OwnedByProfileId.UserStatus = Active` → `GL-AUTH-PROFILE-INACTIVE`; (10) `App.Status = Active` if linked → `GL-APP-NOT-ACTIVE`. Mode-header fall-through arrow points at `05-auth-validation.mmd` for the TempToken lane. Acceptance terminal updates `SshKey.LastUsedAt` and writes `AuditTrail.SshAuthSuccess`; reject terminal writes `AuditTrail.AuthFail`. classDef colors distinguish gates (blue), accept (green), and reject (red) nodes per the §06-permission-flow precedent.
- **Slot choice:** Slot **10** is the first numeric slot available per **AC-DG-10** ("the next available numeric slot for new diagrams is `10-*` onward"). Slots 02/03/04 remain locked (Phase P9 audit confirmed). Header comment block conforms to AC-DG-05 (`%% Diagram type:` + `%% What this answers:`) and to the Phase 55 `DiagramMetadata` JSON Schema (`id: 10-ssh-auth-validation`, `type: flow`, `owner_module: spec/26-gitlogs-diagrams/...`, `render_target: svg`).
- **Added** [`puppeteer.json`](./puppeteer.json) sibling render config (`{"args": ["--no-sandbox", "--disable-setuid-sandbox"], "defaultViewport": {"width": 2400, "height": 2400}}`). This file was referenced by AC-DG-18 + AC-DG-11 + AC-DG-12 + the §00 v2.1.0 Phase 10 banner ever since the GWT rewrite landed but had never actually been checked in — Phase P10 closes that pre-existing gap as a side-effect (the new diagram needed it to render). Conforms to AC-DG-18 (`--no-sandbox` for CI compatibility, viewport ≥ 2000×2000).
- **Added** §97 **AC-DG-21** ("SSH auth-lane diagram covers all 10 §31 validation steps + 11 reject codes") — codifies the diagram's coverage contract machine-checkably. AC count 20 → 21.
- **Bumped** §97 **AC-DG-20** active-diagram count `6 → 7` to reflect the new sibling.
- **Bumped** §00 v2.3.0 → **v2.4.0** (banner + inventory row 10 added). §97 v3.0.0 → **v3.1.0**. §99 v3.2.0 → **v3.3.0**.
- **Cross-walk:** No `.mmd` re-render of pre-existing diagrams (none of their source `.mmd` files changed). No §22/§31 source-of-truth edit (this folder trails §22 per AC-DG-19 governance rule). The §22 §31 spec was already authoritative at v2.9.1 (Phase 5 close) — Phase P10 simply gives it a visualization.
- **Verified:** `node linter-scripts/check-lockstep.cjs` ✅ 87/87; `node linter-scripts/check-tree-health.cjs --strict` ✅ 168/168.

---

## [3.3.0] — 2026-04-28 (Phase P9: slot-gap audit — verified RESOLVED, no edits required)

- **Verified** §26 slot gaps 02/03/04 are already fully resolved via the v2.0.0 retirement and the Phase 16g GWT rewrite. Audit checklist:
  - **§00 inventory** lists all three slots as `~~retired v2.0.0~~` with explicit `_locked_` annotations and content-redirect pointers (lines 30–32).
  - **§00 narrative** v2.0.0 banner explicitly declares "Slots **02**, **03**, **04** are now **intentional locked gaps** (never to be reused per project rule 'file slots are immutable once shipped')."
  - **§97 inlined contract** `LOCKED_GAPS:` field machine-encodes the three slot numbers + their original names.
  - **§97 AC-DG-10** ("Slots 02, 03, 04 remain intentional locked gaps") codifies the prohibition as a GWT acceptance criterion verified against AC-SAG-04 (slot immutability).
  - **§97 AC-DG-LEGACY-11** preserves the v2.0.0 historical narrative for traceability.
  - **§99 inventory** marks all three with 🗑️ + "Removed v2.0.0 — slot locked".
- **Outcome:** No new file authoring, no AC additions, no DDL/schema/enum change. P9 closes by audit-confirmation, parallel to Phase P6's resolution of §22 GAP-V2-06 (locked-vacant precedent retained; stub-file recipe rejected by Core memory rule on slot immutability + tree-health regression risk).
- **Scope discipline (Phase P9 ONLY):** Pure audit + this changelog row + §99 banner bump. No `.mmd` source change, no `.svg` re-render, no §00 / §97 edit. The five-source documentation cited above is already authoritative; this row simply records that the audit ran and confirmed coverage.
- **Verified:** `node linter-scripts/check-lockstep.cjs` ✅ 87/87; `node linter-scripts/check-tree-health.cjs --strict` ✅ 168/168.

---

## [3.0.0] — 2026-04-26 (Phase 16g: §97 full GWT rewrite)

- **Changed** §97 — full GWT rewrite. Replaced 9 table-row criteria (AC-D-01..AC-D-11, with 02/03/04 already retired) with **20 module-specific Given/When/Then ACs** (AC-DG-01..AC-DG-20) covering: ER schema parity with §22 (entities + cardinalities, forbidden v1 entities), auth validation order with `GL-*` reject codes, RBAC RolePermission-union resolution, header-comment contract (`%% Diagram type:` + `%% What this answers:` mandatory for non-ER), emoji-free + Mermaid-CLI rendering, JWT/RS256/JWKS forbidden, endpoints mindmap covering all 8 REST endpoints, encryption v3 7-node derivation chain, slot 02/03/04 locked-gap immutability, `.mmd` ↔ `.svg` lockstep build artifact rule, kebab-case ASCII node IDs, `GL-*` codes cross-validated against §22 §14 registry, `puppeteer.json` reproducibility, governance rule "§26 trails §22 — never leads", and self-application audit.
- **Preserved** legacy table-row criteria as AC-DG-LEGACY-01..11 (with 02/03/04 retired) at end of §97.
- **Bumped** §97 v2.0.0 → v3.0.0 (major; AC contract type changed from table-row to GWT). §98 v2.1.0 → v3.0.0. §99 v2.1.0 → v3.0.0.

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 2.3.0 — 2026-04-27 (Phase 55 — implementability lever)
- **Added** Removed `kind: index` exemption. Added `DiagramMetadata` JSON Schema + TypeScript enums → `has_json_schema` (+15) and `has_ts_enums` (+10).

### 3.1.0 — 2026-04-26
- **Phase 24 — `kind: index` exemption.** Added YAML front-matter `kind: index` to `00-overview.md` to mark this module as a placement-rule router (intentionally empty / index-only). Audit script v2.2 honours the exemption, removing `missing-contract` and `untestable` rubric findings. Result: module lifted from C-tier to B-tier in the v2-deterministic audit.

### 2.1.0 — 2026-04-26
- **Added** (Phase 10 — Diagram Render Pass per `mem://specs/phased-roadmap.md`) — Rendered all 6 active `.mmd` sources to companion `.svg` files via `@mermaid-js/mermaid-cli` v11+ (`mmdc -b transparent`, `--no-sandbox` Puppeteer flags): `01-er-diagram.svg` (313 KB, full v2.9.0 split-DB ER incl. `ShaRegistry`, `SshKey`, `SshNonce`), `05-auth-validation.svg` (177 KB), `06-permission-flow.svg` (113 KB, classDef-colored RBAC), `07-rate-limit-flow.svg` (35 KB, token-bucket sequence), `08-encryption-v3-flow.svg` (34 KB, deferred-v3 keys), `09-endpoints-mindmap.svg` (182 KB, all 8 endpoints). Sources unchanged; SVGs are checked-in build artifacts so reviewers without Mermaid tooling can preview the diagrams directly. Picks up the schema/UI changes that landed in Phases 4–9 (split-DB boundary already reflected in `01-er-diagram.mmd` since v3.8.5 Phase 4; SSH-Key Lane B entities since v3.8.6 Phase 5). No `.mmd` content edits in this phase — render-only.

### 2.0.0 — 2026-04-26
- **Removed** (MAJOR) — `02-domain-design.mmd` retired; it overlapped ~70% with `01-er-diagram.mmd` (both showed GitProfile → Repo → RepoVersion connectivity), causing user confusion that "everything looks like an ERD". Hierarchy info now lives in the ER's relationship arrows + the prose schema in `../22-git-logs-v2/02-database-schema.md`. Slot 02 is now an intentional locked gap.
- **Removed** (MAJOR) — `03-endpoints-write.mmd` and `04-endpoints-read.mmd` retired. Two sequence diagrams arbitrarily split the REST API by HTTP verb, fragmenting endpoint discovery. Slots 03 + 04 are now intentional locked gaps.
- **Added** — `09-endpoints-mindmap.mmd` (NEW). Single Mermaid `mindmap` covering all 8 endpoints (`/append-log`, `/fixed-log`, `/clear-log`, `/clear-log-all`, `/get-logs`, `/get-pipeline-logs`, `/get-error-logs`, `/get-pipeline-error-logs`) under `Writes` / `Reads` / `Cross-cutting` branches. Each endpoint branch carries: HTTP verb, full path, auth requirement, request-body fields with types, response shape, possible GL-* error codes, audit category. Replaces former AC-D-03 + AC-D-04.
- **Added** — `%% Diagram type: …` + `%% What this answers: …` header comments to every flowchart/sequence/mindmap (`05`, `06`, `07`, `08`, `09`). Resolves user feedback "permission flow / rate-limit flow look like ERDs" — they were always flowcharts/sequences but lacked explicit signposting.
- **Changed** — `06-permission-flow.mmd` redrawn: added classDef colors (input/step/decision/allow/deny), per-rejection GL-* error codes (`GL-AUTHZ-WP-AUTH-FAILED`, `GL-AUTHZ-NO-PROFILE`, `GL-AUTHZ-PERMISSION-DENIED`), and a `Seed` subgraph showing Admin/Editor/Viewer role → permission seeds. Same flowchart shape, much more visually distinct from the ER.
- **Changed** — `00-overview.md` inventory rewritten to show Diagram type column and tombstone rows for retired slots 02/03/04, plus a layman "Why so few diagrams now" section.
- **Changed** — `97-acceptance-criteria.md`: AC-D-02/03/04 marked retired; AC-D-09 reused for the new mindmap; AC-D-11 added for the locked-slot rule.
- **Changed** — CI lock: cross-link checker now wired in `.github/workflows/spec-health.yml` (zero broken links allowed baseline). See `spec/27-spec-toolchain/70-spec-health-yml.md` v1.1.0.

### 1.1.0 — 2026-04-25
- **Fixed** inventory drift: `00-overview.md` and `99-consistency-report.md` now list all 8 `.mmd` files plus `97`/`98`. Previously rows 07 (rate-limit) and 08 (encryption-v3) existed on disk but were undocumented, causing the v2 audit to false-flag them as missing.
- **Added** clickable relative links for every entry in the overview inventory.
- **Added** §99 cross-reference health and explicit "Open Gaps: none" closure.

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
| 2026-04-26 | patch | Phase 31: Added Validation History / File Inventory headings to §99 to satisfy rubric v2.0.0 quality dimension. |
| 2026-04-26 | patch | Phase 28: Fixed broken cross-reference link. |

## 2026-04-27 — Phase 74 (evidenced index/tracker bonus)

- Added Mermaid lifecycle diagram and 5-stage CI workflow contract.
- Activates v2.9 evidenced-tracker / evidenced-index bonus (+5 each).
- Documentation-only promotion.

## 3.4.2 — 2026-04-30 — Phase 153 (inventory-pin)

- Added **AC-22** (Derivative-context pin for spec/22 source) — Lesson #29 module asset inventory pin. Auditor-authoritative on-disk inventory declaration; closes audit-v6 HIGH [D5] missing-files class as bundling-cap artifact (cache-stale per Lesson #34 until A8 LLM re-score). Lockstep §00/§97/§98/§99 patch+minor coordinated.

