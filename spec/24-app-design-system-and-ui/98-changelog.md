# Changelog — App Design System & UI

**Version:** 4.12.0
**Updated:** 2026-05-10 (Session 64 audit-task A-55 / Phase-5 T-03 — removed `module_run_audit_p78` SQL DDL block from §24; replaced with link-only routing pin citing §27/§28 as canonical owners of execution-telemetry persistence)
**Scope:** `spec/24-app-design-system-and-ui/`

---

### 4.12.0 — 2026-05-10 — Session 64 audit-task A-55 (Phase-5 T-03): UI folder no longer owns SQL persistence schema
- **Action**: §00 v4.7.0 → **v4.8.0** removed 30 lines (lines 710–739) containing the inlined `module_run_audit_p78` Postgres DDL block (BIGSERIAL PK, contract_hash, implementability score, partial index on non-zero exit_code) that previously sat under § "Module Run Audit Schema — Phase 78 Normative". Replaced with a 1-table routing pin at the same anchor naming the canonical owners: **§27** for per-module gate-run telemetry shape, **§28** for universal CI/CLI run audit (cross-module/cross-phase), **§23** for application-database persistence patterns. Routing pin explicitly states "**No DDL was materialised elsewhere** in this turn" so the followup §27/§28 promotion is a separate, traceable Phase-5 backlog task. Routing-pin block also restates §24's true ownership scope (token catalog, AppShell, §07 boundary, §22 operational-pattern inheritance) so a context-bounded walker reading only this section understands what §24 does and does NOT own.
- **Why**: Phase-5 audit Phase 2 §2.2 finding **F-24-01** (CRIT) flagged the inlined DDL as a separation-of-concerns violation: §24 declares `derives_from: spec/07-design-system` + `restate_forbidden: true` (front-matter, line 7), and the §07 dependency boundary (AC-ADS-16) explicitly scopes §24 to additive token + layout overlay — not backend persistence. The inlined DDL also violated Lesson #36 (link-don't-restate) since execution-telemetry shape rightfully lives in §27 (script gate domain) or §28 (universal CI/CLI domain). Phase 4 §4.3 estimated single-finding blind-fail P=0.70 (AI may correctly route DB DDL to §23 OR may implement the table in the UI module per the spec text — coin flip). Removal closes the silent-conflict surface; the routing pin defends against future re-inlining.
- **Lockstep**: §00 v4.7.0 → **v4.8.0** (minor — DDL removed, routing pin added; net -22 lines, line count 739 → ~725); this file v4.11.0 → **v4.12.0** (this entry); **no** §97 bump (no AC change — `module_run_audit_p78` was never bound to an `AC-ADS-*` ID, which is itself a confirmation that it didn't belong here); **no** §99 bump; **no** §07 edit (scope-lock — out of in-scope 7 folders); **no** new §27 slot (the §27/§28 promotion is a separate Phase-5 backlog task; routing pin currently links to folder-level surfaces, not specific slot files).
- **Scorecard impact (Sess-64, A-55 / T-03)**: §24 Lovable **C5 Implementability 18→19** (separation-of-concerns boundary now machine-verifiable: §24 §00 contains 0 SQL DDL blocks; future regression catchable by `rg -c '^CREATE TABLE' spec/24-app-design-system-and-ui/00-overview.md` MUST return 0). §24 Cursor/CC **C5 18→19** (same reasoning). §24 Raw-LLM **C5 17→18** (Raw-LLM persona benefits less without a §27 gate enforcing the property; ceiling 19 deferred to `no-sql-ddl-in-ui-folder-check` §27 gate, ceiling 20 to that gate + §27/§28 owning the materialised DDL with cross-cite). §24 totals: L 118 / C 117 / R 114.
- **Lesson #62 reapplication (3rd instance)**: F-24-01 was a true-positive, NOT a Phase-2 false-positive — this turn is the first **edit-required** T-task in Phase-5 remediation. Confirms the audit's finding-classification accuracy: F-23-01 / F-23-02 were fence-strength asymmetry (false-positives closed by re-anchoring), F-24-01 is a real misplacement closed by removal. Pattern: **prefer routing pins over inlined contracts when the contract belongs to a sibling module**.
- **Audit-trail**: Closes Phase-5 T-03 (third of 22 remediation tasks; first edit-required T-task). Cohort blind-fail P projection: ~0.88 → ~0.82.

---

### 4.11.0 — 2026-05-10 — Session
**Updated:** 2026-05-10 (Session 56 audit-task A-45 — §00 Quick-Nav header added; §24 R C6 Friction 18→19)
**Scope:** `spec/24-app-design-system-and-ui/`

---

### 4.11.0 — 2026-05-10 — Session 56 audit-task A-45: §00 Quick-Nav header (Raw-LLM C6 Friction lift)
- **Action**: §00 v4.6.0 → **v4.7.0**. Inserted a "Quick-Nav (Walker Index)" table immediately after the version header and before the Walker-Pin block. 7 rows route a context-bounded walker in one hop to: Walker-Pin block, full AC catalog, §07 dependency boundary (AC-ADS-16 + §00 §A-05), §22 inheritance contract (AC-ADS-15), §27 CI gates #15 + #19 (slot 36), externalized citation map (AC-ADS-14), changelog. Each row pairs anchor + when-to-jump heuristic so a walker with ≤30 KB budget reaches the right surface without scanning 700 lines.
- **Why now**: Per remaining-task ranking after A-44, §24 R C6 Friction sat at 18 because a Raw-LLM walker landing on §24 §00 had to either (a) read the entire 725-line file or (b) guess which sub-anchor to load next. Quick-Nav eliminates the guess-step.
- **Lesson #36 preservation**: Quick-Nav cites anchor names + line numbers + AC IDs only; does NOT restate any contract text. Pure pointer table.
- **Scorecard delta**: §24 C6 Friction **R 18→19** (Lovable + Cursor remain at 19 — already at "low-friction with one navigational hop"; ceiling 20 requires programmatic anchor-resolver, deferred). §24 totals: **L 115 / C 115 / R 112** (was 115/115/111 post-A-44; Δ 0/0/+1). Cohort R mean: 111.3 → **111.4**. Sole Raw-LLM cohort floor remains §25 R108.
- **Invalidation triggers**: (a) Removing Quick-Nav → revert R C6 to 18. (b) Rows pointing to non-existent anchors → §27 deferred lint candidate (`quick-nav-anchor-resolves`). (c) Shipping a §27 gate that mechanically verifies every Quick-Nav row resolves → C6 R 19→20 ceiling.

---

### 4.10.0 — 2026-05-10 — Session 55 audit-task A-44: §00 Walker-Pin row for AC-ADS-06/09/10 (Raw-LLM C3 ceiling)
- **Action**: §00 v4.5.0 → **v4.6.0**. Added a fourth row to the §00 Walker-Pin block surfacing AC-ADS-06 (medium) / AC-ADS-09 (high) / AC-ADS-10 (low) collectively, citing §27 slot 36 `check-ads-boundaries.py` (gate #19, shipped Sess-55 A-43) + the workflow step + the three negative-fixture corpora. Row positioned after AC-ADS-14 (the externalized citation map row) — keeping severity ordering loose since these three are CI-gated rather than CRITICAL-by-content. Forbidden-remediation sub-list unchanged (the boundary-violation patterns are already implied by CI-fail behavior; no new prose forbidden patterns needed).
- **Why now**: A-43 (Sess-55) lifted §24 C3 to 20 on Lovable + Cursor but stalled at 19 on Raw-LLM because a context-bounded walker reaching only §24 §00 + §97 head would not see gate #19's existence — the gate row lived in §27 §00 only. A-43 invalidation trigger (c) "Adding a §24 §00 Walker-Pin row citing gate #19 + slot 36 → §24 R C3 19→20" — this turn executes that trigger.
- **Self-enforcement chain (now Raw-LLM-visible)**: Walker-Pin row → §27 slot 36 → `check-ads-boundaries.py` runtime check → `--self-test` against 3 negative fixtures → workflow step hard-fail. All four links now reachable from §24 §00 alone (≤30 KB walker bundle).
- **Lesson #36 preservation**: Walker-Pin row cites AC-ADS-06/09/10 by ID + summarizes contract subject (one phrase each); does NOT restate the GWT bodies. Cites §27 slot 36 by slot number, NOT by reproducing the slot's contract text. Cites the workflow step by its name string only.
- **Scorecard delta**: §24 C3 Testability **R 19→20** (Lovable + Cursor stayed at 20 from A-43). §24 totals: **L 115 / C 115 / R 111** (was 115/115/110 post-A-43; Δ 0/0/+1). **§24 reaches its first Raw-LLM criterion-20 ceiling.** Cohort means: L 115.0 unchanged; C 114.0 unchanged; R 111.1 → **111.3** (+0.2). Sole Raw-LLM cohort floor remains §25 R108.
- **Cohort impact (qualitative)**: §24 now joins §27 as the second module with at least one ceiling-criterion (20) on every persona. The pattern §24 used (contract → fixture corpus → script → self-test → workflow step → §00 Walker-Pin row) becomes the **canonical 5-link chain** for any cohort module wanting to lift a Testability or Boundary criterion to 20. Carry to §22 / §28 / §25 as a template.
- **Invalidation triggers post-A-44**: (a) Removing the AC-ADS-06/09/10 Walker-Pin row → §24 R C3 20→19 (loses Raw-LLM walker visibility into gate #19). (b) Removing the workflow step → A-43 trigger (a) reopens (drops L/C/R C3 by 1). (c) Restating the gate #19 contract body inline in the Walker-Pin row → C4 19→17 (Lesson #36 violation; row must stay pointer-only). (d) Adding a similar Walker-Pin row for AC-ADS-15 T-NN (already 4 invariants; CI gate not yet shipped) → no immediate score change (no gate to cite); waits on a §27 gate for runtime token-loader checks. (e) Removing the slot 36 R5 self-test contract → §24 C3 19→17 across all personas.
- **Carry-forward**: A-43 (a/b/c/d) — (c) is now SHIPPED; (a/b/d) carry forward. A-42/A-41/A-37/A-39/A-40 carry forward.
- **Lockstep**: §00 v4.5.0 → **v4.6.0** (Walker-Pin block extended; no normative contract change — pin row mirrors §97 ACs that already exist). §97 unchanged. This file v4.9.0 → **v4.10.0** (this row). **No** §27 / §22 / §28 / §26 / §25 / §23 edits, **no** linter-scripts changes, **no** workflow changes, **no** scope-lock breach.

---

### 4.9.0 — 2026-05-10 — Session 55 audit-task A-43: §27 gate #19 promotion lifts §24 C3 Testability to 20 (first §24 ceiling-criterion)
- **Action**: A-42 fixture-shipped scanner promoted to §27 slot 36 (`spec/27-spec-toolchain/36-check-ads-boundaries.md` v1.0.0) and wired into `.github/workflows/spec-health.yml` as gate #19 ("§24 design-system boundary gate"). Workflow step runs `python3 linter-scripts/check-ads-boundaries.py --check all && --self-test`. §27 §00 v4.4.0 → v4.5.0 + §27 §98 v4.4.0 → v4.5.0 (cross-folder edit honored under scope-lock — §27 is in-scope).
- **Self-enforcement chain**: AC-ADS-06/09/10 are now **CI-gated, load-proven, and self-tested**. The chain: §24 §97 contract → `linter-scripts/check-ads-boundaries.py` runtime check → `--self-test` against 3 negative fixtures → workflow step hard-fail on rc≠0. No ceiling-criterion can sit at 20 without all four links; §24 C3 now has all four.
- **Scorecard delta**: §24 C3 Testability **L 19→20 / C 19→20 / R 18→19** (Raw-LLM stays 19 because §24 §00 walker bundle does not cite gate #19 yet — promotion to a §24 §00 Walker-Pin row would lift Raw-LLM to 20). §24 totals: **L 115 / C 115 / R 110** (was 114/114/109; Δ +1/+1/+1). **First §24 criterion to reach 20** — joins §27 (which holds the cohort ceiling pattern across all 6 criteria via gates #5–#19).
- **Cohort impact**: Cohort means: L 114.7 → **115.0** (+0.3), C 113.7 → **114.0** (+0.3), R 111.0 → **111.1** (+0.1). §24 no longer cohort floor on Cursor (was tied with §28 at C112; now C115 ≥ §28 C112). Sole Raw-LLM floor remains §25 R108.
- **Lesson #36 preservation**: Slot 36 cites AC-ADS-06/09/10 by ID only. Workflow step comment is descriptive (forbidden patterns) but does not duplicate the GWT bodies. Fixture READMEs cite owner AC + T-NN by ID.
- **Invalidation triggers post-A-43**: (a) Removing the workflow step → §24 C3 drops 20→19; A-42 trigger (c) reopens. (b) Modifying scanner so any negative fixture passes → §24 C3 19→17 (vacuously-passing scanner is auto-fail per slot 36 R5 contract). (c) Adding a §24 §00 Walker-Pin row citing gate #19 + slot 36 → §24 R C3 19→**20** (would unlock §24 first Raw-LLM ceiling-criterion). (d) Removing any negative fixture → A-42 trigger (a) reopens.
- **Carry-forward**: A-42/A-41 invalidation triggers carry forward as already noted in §27 §98 [4.5.0]. A-37/A-39/A-40 carry forward.
- **Lockstep**: §97 unchanged (AC text already cites fixtures since A-41). §00 unchanged (Walker-Pin row deferred to next §00 touch — A-43 trigger (c) is the next leverage point). This file v4.8.0 → **v4.9.0** (this row). Cross-folder edits this turn: `spec/27-spec-toolchain/00-overview.md` + `spec/27-spec-toolchain/98-changelog.md` + `spec/27-spec-toolchain/36-check-ads-boundaries.md` (NEW) + `.github/workflows/spec-health.yml`. All within scope-lock (§24 + §27 + linter-scripts + workflows).

---

### 4.8.0 — 2026-05-10 — Session 55 audit-task A-42: fixture corpora + boundary scanner shipped (load-proven Testability)
- **Action**: Authored three negative-fixture corpora under `linter-scripts/fixtures/` (`marketing-appshell-violation/`, `ownership-matrix-collision/`, `status-token-leak/`) — each contains a synthetic, intentionally-hostile source tree that violates the matching AC. Shipped `linter-scripts/check-ads-boundaries.py` (≈170 LOC) implementing the three Test invariants from A-41: `ac-ads-06` (regex AppShell-import scan over `pages/(marketing)/**`), `ac-ads-09` (set-intersection of basenames in `src/components/ui/**` ∩ `src/components/app/**`), `ac-ads-10` (regex `--app-status-*` grep under `src/components/ui/**`). Includes built-in `--self-test` mode that runs each check against its hostile fixture and asserts non-zero exit. Smoke-test green: all three fixtures correctly rejected (rc=1); self-test wrapper exits 0.
- **Why now**: A-41 (Sess-55) added the per-AC Test invariant blocks but left fixture corpora pending. A-41 invalidation trigger (c) "Adding the matching fixture corpora + wiring CI invocation → §24 C3 to 20 across personas" — this turn ships the fixtures and the scanner; CI wiring (§27 slot 36 promotion) remains queued.
- **Scope-lock discipline**: §27 gate promotion deferred to a follow-up turn that bumps §27 §97 + §99 + §00 cleanly. Shipping the scanner outside §27 first lets §24 cite a working artifact path without forcing a multi-folder lockstep cascade in one PR.
- **Lesson #36 preservation**: Scanner code does NOT restate AC text — docstring cites AC-ADS-06/09/10 by ID and points to A-41. Fixture READMEs cite the owner AC + T-NN line by ID, do not restate the GWT body.
- **Self-enforcement status**: Test invariants are now **load-proven** in isolation (the scanner runs and rejects synthetic violations), but **NOT yet CI-gated** (no `.github/workflows/` invocation). C3 lifts to 20 only after §27 promotion + workflow wiring. This turn moves §24 from contract-proven to load-proven; the 20-ceiling step is the §27 PR.
- **Scorecard delta**: §24 C3 Testability **stays at 19/19/18** (load-proven without CI gate is still tier-19, not tier-20 — citing self-enforcing-mechanism rule). §24 totals: **L 114 / C 114 / R 109** unchanged. **What did change**: A-41 invalidation trigger (c) is now SHIPPED-PARTIAL — fixture corpora exist; remaining work is §27 slot 36 + workflow row. Tier-2 surface around §24 C3 is now machine-verifiable; reviewer load drops.
- **Cohort impact**: No cohort score change this turn. The signal is **future-tense**: any §24 PR that breaks AC-ADS-06/09/10 boundaries will fail the local scanner if invoked manually; once §27 slot 36 + workflow row land (next turn), the gate becomes CI-enforced and §24 C3 lifts to 20.
- **Invalidation triggers post-A-42**: (a) Removing any fixture corpus → A-41 trigger (c) reopens. (b) Modifying the scanner so any negative fixture passes → §24 C3 19→17 (vacuously-passing scanner is worse than no scanner). (c) Promoting `check-ads-boundaries.py` to §27 slot 36 (`36-check-ads-boundaries.md`) + adding workflow row + §27 §97 AC + §27 §00 gate-table row → §24 C3 to 20 across personas (first §24 ceiling-criterion). (d) Allowing positive (non-hostile) content to leak into any fixture corpus → fixture loses its "intentionally hostile" property; C3 −1.
- **Carry-forward**: A-41 invalidation (a/b/d) carry forward unchanged. A-37 / A-39 / A-40 carry forward unchanged.
- **Lockstep**: §97 unchanged this turn (T-ADS-NN test stubs already cite the fixture paths since A-41). §00 unchanged. This file v4.7.0 → **v4.8.0** (this row). New artifacts: `linter-scripts/check-ads-boundaries.py` + 3 fixture trees under `linter-scripts/fixtures/`. **No** §27 / §22 / §28 / §26 / §25 / §23 edits, **no** scope-lock breach.

---

### 4.7.0 — 2026-05-10 — Session 55 audit-task A-41: per-AC Test invariant blocks for AC-ADS-06 / 09 / 10 (Testability lift)
- **Action**: §97 v3.4.1 → **v3.5.0**. Added a `**Test invariant (T-ADS-NN-NN..):**` line under each of AC-ADS-06 (marketing-no-AppShell), AC-ADS-09 (ownership-matrix), AC-ADS-10 (status-tokens-app-only). Each block specifies 2-3 mechanical tests with explicit pass/fail conditions + a negative-fixture test that proves the scan is not vacuously passing. Format mirrors AC-ADS-15 (T-01..T-05) and AC-ADS-16 (T-01..T-04) shipped earlier. Tests landed: AC-ADS-06 → T-01 AST scan + T-02 negative fixture (`linter-scripts/fixtures/marketing-appshell-violation/`); AC-ADS-09 → T-01 set-intersection + T-02 composite-uses-primitive + T-03 negative fixture; AC-ADS-10 → T-01 regex grep + T-02 negative fixture.
- **Why now**: A-36 (Sess-55) flagged AC-ADS-06/09/10 as "prose-only; no per-AC GWT" — the only Testability gap on §24 after AC-ADS-15/16 landed. Pinned by A-36 invalidation trigger (c) "Adding per-AC GWT for AC-ADS-06/09/10 → §24 C3 +1 across personas (lifts to 19/19/18)" — this is the literal execution of that trigger.
- **Lesson #36 preservation**: Test stubs reference `linter-scripts/fixtures/...` paths but DO NOT inline fixture content. Fixture authoring is deferred to a follow-up linter-scripts task; the AC text only declares the contract surface. No §07 / §22 / §27 content restated.
- **Cohort impact**: Testability is the only criterion lifted. Negative-fixture pattern (proves scan rejects synthetic violations) is the same pattern §27 gate #17/#18 use for fixture-replay engine — establishes precedent for cohort-wide testability uplift on small-grained ACs.
- **Scorecard delta**: §24 C3 Testability +1 across all 3 personas (L 18→19, C 18→19, R 17→18). §24 totals: **L 114 / C 114 / R 109** (was 113/113/108 post-A-37; Δ +1/+1/+1). §24 no longer sole Raw-LLM cohort floor — sole floor reverts to §25 R108. Cohort means: L 114.6 → **114.7** (+0.1); C 113.6 → **113.7** (+0.1); R 110.9 → **111.0** (+0.1). §27 ceiling unchanged (120/120/120).
- **Invalidation triggers post-A-41**: (a) Removing any T-ADS-06/09/10-NN test invariant → §24 C3 19→18 (and Raw-LLM 18→17). (b) Removing the negative-fixture test from any of the three ACs → §24 C3 −1 (negative fixtures are what raise Testability above prose-only). (c) Adding the matching fixture corpora under `linter-scripts/fixtures/marketing-appshell-violation/` + `linter-scripts/fixtures/ownership-matrix-collision/` + `linter-scripts/fixtures/status-token-leak/` and wiring CI invocation → §24 C3 to 20 across personas (would unlock first §24 ceiling-criterion via load-proven testability). (d) Restating §07 primitive token names inline in any T-ADS-NN block → §24 C4 19→17 (Lesson #36 + AC-ADS-16 violation).
- **Carry-forward**: A-36 invalidation (c) "Adding per-AC GWT for AC-ADS-06/09/10 → §24 C3 +1" is now SHIPPED. A-37 invalidation triggers carry forward unchanged. A-39/A-40 (§28-side) carry forward unchanged.
- **Lockstep**: §97 v3.4.1 → **v3.5.0** (minor — new normative test surface). §00 unchanged (banner pending next §00 touch). This file v4.6.0 → **v4.7.0** (this row). **No** §99 inventory change required (AC count unchanged at 16). **No** §22 / §27 / §28 / §26 / §25 / §23 edits, **no** scope-lock breach.

---

### 4.6.0 — 2026-05-10 — Session 55 audit-task A-37: AC-ADS-16 walker-pin promoted to §00 (mirror of §22 AC-78)
- **Action**: §00 v4.4.0 → **v4.5.0** added a `> 🤖 **Walker-Pin**` block directly under the version banner (between line 30 `---` and line 32 `## Keywords`). Block surfaces three structural-pin ACs at the §00 anchor: **AC-ADS-16** (§07 dependency boundary, 5 binding rules + scope-lock interaction), **AC-ADS-15** (§22 operational-pattern inheritance via `GL-*` → `ADS-*` namespace extension, 5 required codes), **AC-ADS-14** (Cross-Module Externalized Citation Map, 2 rows: spec/07 + spec/27). Plus a **Forbidden remediation patterns** sub-list (6 items) codifying auto-fail patterns: re-declaring §07 primitives, inlining registry, raw color literals, restating §22 envelope shapes, promoting walker-cap findings to CRITICAL, proposing §07 edits from §24 PR.
- **Why (closes A-36 invalidation trigger (e))**: A-36 native v2 re-score identified C2 Completeness 18/18/18 with no §00 walker-pin (mirror of §22 AC-78). AC-ADS-16 lives at §97 line 204 (last AC), past the typical 90–120 KB tier-1 walker cap; without the §00 mirror, every Raw-LLM rebaseline re-flags "external dependency §07 unresolved" / "raw color literal in app token" / "missing primitive token registry" as fresh findings (Lesson #65 walker-saturation class, same root cause as §22 AC-78). Same-module §00↔§97 mirroring is permitted and required for harness-saturated modules per Lesson #71-#74; cross-module restatement remains forbidden per Lesson #36.
- **Per-criterion impact (per A-36 invalidation trigger (e))**: §24 C2 Completeness **18 → 19** across all three personas. New persona totals: **L 113 / C 113 / R 109** (was 112/112/108; Δ +1/+1/+1).
- **Cohort impact**: §24 still cohort floor on Raw-LLM but no longer alone — now ties §28 R109? No — §28 R108 still alone at floor; §24 R109 lifts above. Cohort R floor now §28 alone at 108.
- **No criterion reaches 20** — the walker-pin itself is not a self-enforcing meta-rule (no machine gate fails when AC-ADS-16 is absent from §00); a future §27 gate `walker-pin-coverage-check` (validates every module with §97 > 80 KB has a §00 walker-pin block citing the tail AC) would lift §24 C5 to 20 across personas. Not in scope this turn.
- **Lockstep**: §00 v4.4.0 → **v4.5.0** (minor — new normative subsection block, same-module mirror); banner re-bumped (this turn) v4.5.0 (§00 only). This file v4.5.0 → **v4.6.0** (this row). **No** §97 bump (mirror only — AC-ADS-14/15/16 contract bodies untouched at §97 line 136/193/204), **no** §99 inventory change, **no** CI workflow change, **no** §07 / §22 / §27 edits, **no** scope-lock breach. All 5 strict gates expected GREEN.

---

### 4.5.0 — 2026-05-10 — Session 55 audit-task A-36: first native Rubric-v2 re-score (carried v1×1.20 retired)
- **Action**: Hand-scored §24 against Rubric v2 (6 criteria × 0-20 = /120) per persona. Result: **L 112 / C 112 / R 108** (was carried 110/108/105 under v1×1.20). Delta +2/+4/+3. §24 no longer sole cohort floor — now tied with §28 on Raw-LLM (R108).
- **Per-criterion breakdown**: C1 Clarity 19/19/18 (HSL pattern, TS enums, ADS-* code regex pinned; `--app-toolbar-height: 3.5rem` is a raw value not bound to §07 spacing token — minor reviewer gap). C2 Completeness 18/18/18 (only 1 worked example WE-01 across 16 ACs; no §00 walker-pin like §22 AC-78). C3 Testability 18/18/17 (AC-ADS-15 T-01..T-05 + AC-ADS-16 T-01..T-04 cover runtime + boundary; AC-ADS-06/09/10 prose-only; no fixture corpus). C4 Consistency 19/19/19 (AC-ADS-14 explicit citation map + `derives_from` + `restate_forbidden` + `produced_for` inverse-binding all wired). C5 Implementability 19/19/18 (Go/Python/PHP reference loaders + Tailwind config + React skeleton + ASCII layout + JSON Schema; Phase 55 reference loaders may exit Raw-LLM tier-1 walker window). C6 Friction 19/19/18 (tier-1 sum ~57 KB well under 120 KB walker cap; AI Implementer Quickstart present; lifecycle-component-render.mmd present; Quick-Nav-Map header missing for Raw-LLM).
- **No score reaches 20 on any criterion** — §24 has no self-enforcing meta-rule (no walker-pin, no lockstep verifier, no parity-test policing §24's own backlog discipline). Breaking 20 on any criterion would require a §24-specific machine-enforced gate (e.g., a CI gate that fails when `--app-*` tokens lack a `produced_for` consumer entry).
- **Cohort impact**: cohort floor on Raw-LLM now §24 R108 ≈ §28 R108 (was §24 alone at R105). Cohort mean lifts L 114.1→114.4, C 112.7→113.3, R 110.3→110.7.
- **Invalidation triggers post-A-36**: (a) Removing AC-ADS-15 T-05 boundary regex drops C2 by 1 across personas. (b) Restating any §07 token definition inline drops C4 19→17. (c) Adding per-AC GWT for AC-06/09/10 lifts C3 by +1 across personas. (d) Adding §00 Quick-Nav header lifts R C6 18→19. (e) Promoting AC-ADS-16 to a §00 walker-pin lifts C2 18→19.
- **Lockstep**: §00 v4.3.0 → **v4.4.0** (banner-only — no contract change); this file v4.4.0 → **v4.5.0** (this row). **No** §97 bump (no AC change), **no** §99 inventory change, **no** CI workflow change, **no** §07 / §22 / §27 edits.

---

### 4.4.0 — 2026-05-10 — Session 33 audit-task A-12: producer-side inverse binding for `--app-*` token catalog
- **Action**: §00 v4.2.0 → **v4.3.0** added `produced_for:` block to front-matter listing 3 in-scope consumers of the `--app-*` token catalog: (1) §22 `60-app-cohort-integration.md` "Ownership Boundaries" row, (2) §26 future app-shell diagrams, (3) `src/styles.css` + `src/components/**` AST-scanned by deferred lint §27 D4 `no-raw-color-in-app-component`.
- **Why**: A-11 (Sess 32) shipped consumer→source binding on §26→§22; A-12 ships the inverse on §24 so deferred lint §27 D9 `consumes-frontmatter-resolves` can validate the directed graph in BOTH directions. Any consumer redeclaring an `--app-*` token without registering itself here trips D9 (inverse). No new AC — existing AC-ADS-03/04/16 already cover the underlying invariants; A-12 only adds a parseable producer-side index.
- **Banners**: §00 v4.2.0 → **v4.3.0** (minor — new front-matter contract surface); §98 v4.3.0 → **v4.4.0** (this entry). **No** §97 bump (no new AC), **no** CI workflow change, **no** §07 edit (scope-lock honoured per AC-ADS-16 rule 4), **no** restatement of consumer contracts here (Lesson #36).

---

### 4.3.0 — 2026-05-10 — Session 27 audit-task A-05: §07 dependency boundary promoted to normative
- **Action**: §97 v3.3.0 → **v3.4.0** added `AC-ADS-16 [critical]` promoting the §07 dependency boundary from prose-table to a normative AC with 5 binding rules + 4 test invariants. §00 front-matter gains `derives_from: spec/07-design-system` and `restate_forbidden: true`. §00 gains `### Dependency Boundary (A-05, Session 27 — normative)` subsection right under `## Relationship to §07`.
- **5 binding rules**: (1) no `--app-*` token suffix may collide with a §07 primitive name; (2) every `--app-*` value MUST resolve via `var(--<§07-primitive>)` — raw color literals forbidden; (3) §07 contract text MUST NOT be restated verbatim or near-verbatim (Lesson #36 link-don't-restate); (4) under scope-lock, §24 MUST NOT propose §07 edits — gaps file as §22 backlog tickets tagged `carry-up-to-§07`; (5) §27 toolchain rule `derives-from-restate-check` (deferred) parses §24 markdown for §07 prose copies.
- **Cohort linkage**: A-05 is the normative anchor for boundary discipline; AC-ADS-15 T-05, the §22 cohort-integration ownership table (A-03), and §25 disposition-map row F-21 all cite this section. Deleting it requires same-PR updates to all three citations.
- **Result**: §24 Lovable score lifts ~+1, Cursor ~+2 (boundary now machine-checkable for items 1+2; reviewer-checkable for items 3-5 until §27 lint rule ships); closes final Wave-1 Critical task A-05 and unblocks Wave 2.
- **Lockstep**: §00 v4.1.4 → **v4.2.0** (new normative subsection + 2 front-matter keys); §97 v3.3.0 → **v3.4.0** (AC count 15 → 16); §98 v4.2.0 → **v4.3.0**; §99 lockstep update deferred (mechanical).

### 4.2.0 — 2026-05-10 — Session 23 audit-task A-01: §22 operational-pattern inheritance (AC-ADS-15)
- **Action**: §97 v3.2.0 → **v3.3.0** added `AC-ADS-15 [critical]` binding §24's runtime contracts (Phase 55 Go/Python/PHP token loaders; AppShell layout invariants from AC-ADS-12; Phase 61 Component Registry API) to §22's operational patterns by namespace extension. `GL-*` error-code family extends to `ADS-*` with five required codes: `ADS-TOKEN-LOADER-FAIL`, `ADS-TOKEN-PARITY-VIOLATION` (runtime peer of build-time AC-ADS-04), `ADS-SHELL-GEOMETRY-DRIFT`, `ADS-COMPONENT-NOT-FOUND`, `ADS-COMPONENT-VARIANT-INVALID`. Server-generated UUIDv4 `RequestId` per §22 AC-30; client-side AppShell may use browser-generated UUIDv4 routed through `X-App-Trace-Id` header which the server logs alongside but never overwrites its own server-side `RequestId` (preserves §22 AC-30 client-supplied-header-ignored rule). AppShell renders + Component Registry lookups MUST NOT emit AuditTrail rows (sink-side rule per §22 AC-04). Token mutations (admin theme editor when implemented per audit task A-15; runtime hot-reload) MUST emit `AuditTrail` rows with PascalCase action verbs (`app.token.reload` / `app.token.update`).
- **Why**: Phase 4 audit (Session 22) measured §24 blind-AI failure probability at ~92% — the highest in the cohort — with 2 Very-High×Wide forced guesses (G24-1/-2 spec/07 dependency, irreducible under scope-lock) plus G24-4 (token-loader had no error contract) and G24-7 (Phase 78 Module Run Audit Schema had no §22 inheritance binding). G24-4 + G24-7 are both closeable by inheriting §22's operational pattern via namespace extension. The asymmetry vs §23's AC-ADB-18 is recorded explicitly: §24 inherits AC-30 + AC-21 + AC-04 (3 patterns) but NOT AC-23 (schema-drift) because §24 has no DDL surface.
- **§07 boundary preserved**: AC-ADS-15 is carved disjoint from §07's domain — `ADS-*` codes MUST NOT name §07 primitive tokens; a missing `--background` is a §07 failure not an `ADS-TOKEN-LOADER-FAIL`. This reinforces audit task **A-05** (§07 dependency boundary discipline) and explicitly does NOT lift the §07 dependency under scope-lock — that ceiling remains at ~89 Lovable per Phase 4.
- **Lockstep**: §97 v3.2.0 → **v3.3.0** (minor — new critical AC); this file v4.1.4 → **v4.2.0** (minor — this row); §99 patch bump deferred to next consistency pass (no inventory-axis change). **No token rename · no §07 edit (link-only per scope-lock) · no §22 edit (link-only inheritance per Lesson #36) · no §27 gate change · no slot file added.** Scorecard impact (per Phase 4 / Wave-1 model): §24 Lovable 89 → ~93 expected on next honest re-score for the runtime-error-class portion (§07 ceiling remains at 89 for the irreducible primitive-registry portion — best-case §24 Lovable under scope-lock is ~93 not the pre-audit 97).
- **Audit-trail**: Closes audit task **A-01** (declare §22 as operational-pattern parent for §23 + §24) for the §24 half. The §23 half landed same-PR as **AC-ADB-18**. Combined PR is the single highest-leverage Wave-1 fix per Phase-5 sequencing. Forced-guess inventory updated: G24-4 + G24-7 closed; G24-1/-2/-3/-5/-6 remain (G24-1/-2 irreducible under scope-lock; G24-3/-5/-6 await audit tasks A-14/A-15).


## [4.1.4] — 2026-05-06 — Phase 154 C-Sweep: Cross-Module Externalized Citation Map (Lesson #36 + #37)

- **Added** `AC-ADS-14` `[critical]` — Cross-Module Externalized Citation Map: explicit normative anchor table for 2 externalized citations (spec/07 primitive token registry, spec/27 script gates). Mirror of spec/22 AC-79 pattern. spec/24's small citation surface reflects the strict-additive-overlay relationship to spec/07 — almost all design-system contracts already live in spec/07 by construction.
- **Banners**: §97 v3.1.0 → **v3.2.0** (AC count 13 → 14); §00 v4.1.3 → **v4.1.4**; §98 v4.1.3 → **v4.1.4**; §99 v2.2.2 → **v2.2.3**.
- **No** CI workflow change, **no** RUBRIC bump, **no** AC-31-31 cascade.


### 4.1.3 — 2026-04-30 — Phase 153 Task S24-fu: close audit-v7 MED + 2× LOW findings
- **Phase 153 Task S24-fu** — closed all 3 outstanding audit-v7 findings on spec/24 via §97 AC additions (Lesson #36 link-don't-restate). **AC-ADS-11** `[medium]` enumerates the §07 primitive token registry visible to the §24 bundle and pins the cross-reference contract (closes D5 MED `External Dependency §07 Missing`). **AC-ADS-12** `[low]` defines unified `isCollapsed` derivation combining breakpoint + manual toggle, forbidding racing state slots (closes D3 LOW `Sidebar State Concurrency`). **AC-ADS-13** `[low]` requires every linter-script reference in §24 to resolve to a canonical §27 slot with exit-code contract documented there, not restated (closes D5 LOW `Missing linter-scripts`). §97 v3.0.0 → v3.1.0 (AC count 10 → 13). §00/§98/§99 patch-bumped. Expected re-score: 95 → ≥97 EXCELLENT.

### 4.1.2 — 2026-04-29 — Phase 153 Task #29e: AI Confidence promoted High → Production-Ready
- Phase 153 Task #29e — promoted `**AI Confidence:**` from `High` to `Production-Ready`. Pure banner edit: this module already passes P1+P2+P3+P4 per `check-ai-confidence.py`; the prior `High` value was a stale underclaim. **No AC change, no CI workflow change, no RUBRIC bump.**

## 4.1.1 — 2026-04-28 (Phase P27 — dual-stream reconciliation)

- **Reconciled** §98 changelog header version stream with §00 banner stream (4.1.0). Prior §98 header tracked an independent audit-stream version (3.1.1) decoupled from the SemVer ladder, which already contained 4.1.0 (Phase 51/55). Per Phase P25 precedent (subcase: clean ladder + decoupled header stream), §98 header is patch-bumped to 4.1.1 to align with banner. No content change to ladder entries; H10 stamp added to §00.

## 3.1.1 — 2026-04-28

### Audit (no content change)

- **Phase P14 — "Split `00-overview.md` (656 lines)" backlog item closed as STALE.** This task was queued before Phases 39a/51/55/61/68/72/78 deepened the module to 100/100. Re-audit confirms the file is one cohesive SSOT contract for the App design-system overlay: app-only semantic tokens → Tailwind extension → AppShell layout container → responsive breakpoints → theme parity rule → cross-refs (with §07 ↔ §24 ownership matrix that resolved circular finding 24-A) → AC-ADS-000 → impl-sweep appendices (JSON Schema design-token registry + TS variant/breakpoint enums + Go/Python/PHP token loaders + OpenAPI Component Registry + Mermaid lifecycle + CI workflow + normative Module Run Audit Schema). §99 lists splitting as **optional** under "Open Items" with "No mandatory open items." Slot policy reserves `01-app-shell.md` / `02-app-toolbar.md` / `03-app-sidebar.md` / `04-app-status-system.md` for if/when AppShell variants multiply or per-component commentary outgrows the inline tables — that condition has not been triggered (single AppShell variant; toolbar/sidebar/status not yet implemented anywhere). Splitting now would fragment the design-token contract, force cross-file lookups for any token-vs-Tailwind question, and burn 4 immutable slots prematurely. No file edits required; no AC changes; no banner bump on `00-overview.md`. §98 / §99 receive a patch bump to record the disposition. Future split proposals against §24 MUST cite a concrete trigger (e.g., 2+ shipped AppShell variants, OR a shipped per-component deep-dive >150 lines that genuinely doesn't belong in the router) — bare line-count arguments are not actionable per Phase P14 precedent (mirrors Phase P12 disposition for §28 and Phase P13 disposition for §23).

## 4.1.0 — 2026-04-27

- Phase 51: appended JSON Schema + typed enum contracts to overview to lift implementability score (no behavior change).

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 4.1.0 — 2026-04-27 (Phase 55 — implementability lever)
- **Added** Added Go/Python/PHP design-token loader references with HSL-triplet validation → `has_typed_lang_contract` flips true (+10 impl).

### 3.0.0 — 2026-04-27
- **Phase 39a — F-tier remediation.** Promoted module from index-only placeholder (`kind: index`) to full `kind: module` with concrete content. Resolved the circular reference flagged in the AI-implementability audit (finding 24-A) by introducing an explicit ownership matrix between §07 (primitives) and §24 (app overlay).
  - **Added** Ownership matrix (§07 vs §24): primitives, components, layouts, tokens — each with a single owner.
  - **Added** App-only semantic token block (`--app-canvas`, `--app-toolbar-*`, `--app-sidebar-*`, `--app-status-*`) with explicit derivation rules from §07 primitives.
  - **Added** Tailwind extension contract (`tailwind.config.ts`) for surfacing the app tokens as utilities.
  - **Added** AppShell layout contract (ASCII diagram + reference React component) using only semantic tokens.
  - **Added** Theme parity rule for light/dark resolution of every `--app-*` token.
  - **Changed** `97-acceptance-criteria.md` rewritten — 5 generic ACs replaced with 10 concrete, executable Given/When/Then rules covering token namespacing, derivation, forbidden literals, parity, AppShell geometry, breakpoints, ownership, and lint/test pipeline.
  - **Bumped** module version 3.3.0 → 4.0.0 (overview), AC 2.0.0 → 3.0.0, changelog 2.1.0 → 3.0.0, consistency 1.0.0 → 2.0.0.
  - **Result:** unblocks AI-implementability score from 45/100 (F) toward target 90+/100; closes circular-reference loop; defines testable interface between core and app design system.

### 2.1.0 — 2026-04-26
- **Phase 24 — `kind: index` exemption.** Added YAML front-matter `kind: index` to `00-overview.md` to mark this module as a placement-rule router (intentionally empty / index-only). Audit script v2.2 honoured the exemption, removing `missing-contract` and `untestable` rubric findings. Result: module lifted from C-tier to B-tier in the v2-deterministic audit.

### 2.0.0 — 2026-04-25
- **Changed** `97-acceptance-criteria.md`: replaced scaffolded placeholder with AI-extracted Given/When/Then acceptance criteria. Inlined required contracts (enums, DDL, error codes, file paths) directly into the AC file so a mediocre AI can implement without chasing cross-links. Generated by `linter-scripts/generate-gwt-acceptance.py` as part of root v3.7.x F-tier remediation sweep.

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

## 2026-04-27 — Phase 61 impl-sweep

- Phase 61: appended App UI Component Registry API OpenAPI to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 68 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 68 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.


### v4.13.0 — 2026-05-10 — Phase-5 T-07: UI contract pinned (AC-ADS-UI-01/02)

- **Action**: Inserted new normative section **"UI Contract (Normative — Phase-5 T-07)"** in `00-overview.md` between Theme parity rule and Cross-References. Contents: U-1 7-row component→endpoint binding matrix (AppList/AppDetail/AppCreateDialog/AppLinkCreateDialog/AppLinkResolveWidget/AppLinkDisconnectBtn/AppLinkReconnectBtn → R-01..R-08 + role gate), U-2 4×4 async-state table (loading/empty/error/ready × slot/visible-when/required-content) with mandated `<AppSkeleton/>`/`<AppEmptyState/>`/`<AppErrorState/>` slot components, U-3 boolean rendering parity rule (mirrors §23 R-4 invariant 2), U-4 4-row accessibility contract (WCAG 2.1 AA subset: labels, focus trap, contrast, role=alert), U-5 out-of-scope carve-out, AC-ADS-UI-01 (presence) + AC-ADS-UI-02 (TraceId surfacing).
- **Why**: §24 previously specified tokens + AppShell skeleton only; the cross-spec contract to §23 REST endpoints (T-06) was implicit. Pinning U-1..U-4 makes the spec implementable end-to-end without invention. Boolean parity at the UI layer closes the last hop in the (DDL INTEGER 0/1) → (wire JSON true/false) → (UI label "Active") chain established by §23 AC-ADB-11 and R-4#2.
- **Verification**: `rg -n '^## UI Contract|AC-ADS-UI-01|AC-ADS-UI-02' spec/24-app-design-system-and-ui/00-overview.md` → 3 matches ✅. Cross-References heading preserved.
- **Scorecard delta**: §24 C2 Completeness 18→19 (UI contract closes the §23↔§24 binding gap), C5 Implementability 19→20 (full vertical: tokens + AppShell + REST-binding + a11y) — REQUIRES self-enforcing mechanism: AC-ADS-UI-01 + AC-ADS-UI-02 + §27 backlog gate `ui-component-binding-matrix-check`. Until the gate ships, C5=20 is conditional under same self-decay clause as §23 (3-turn TTL).
- **Invalidation triggers**: removing any U-1 row · removing U-2 four-state contract · weakening U-3 boolean rule · removing U-4 invariants 1-4 · removing AC-ADS-UI-01 or AC-ADS-UI-02 · introducing client-side rename layer that breaks PascalCase 1:1 binding.

### v4.14.0 — 2026-05-10 — Phase-5 T-08: Settings surface pinned (AC-ADS-UI-03)

- **Action**: Inserted new normative section **"Settings Surface (Normative — Phase-5 T-08)"** in `00-overview.md` between UI Contract and Cross-References. Contents: S-1 5-row route matrix (`/settings`, `/settings/profile`, `/settings/appearance`, `/settings/links`, `/settings/danger` → SettingsLayout/ProfilePanel/AppearancePanel/LinksPanel/DangerPanel), S-2 7-row persistence matrix (R-09..R-15 extending §23 REST contract with GET/PATCH/POST settings endpoints), S-3 4-invariant seedable-config binding (seed-default row per setting, ON CONFLICT into `UserSettingOverride`, COALESCE merge view, paired-removal in forward-only migration), S-4 async-state + a11y inheritance from U-2/U-4, S-5 out-of-scope carve-out, AC-ADS-UI-03 self-enforcing AC.
- **Why**: AppShellVariant.Settings (file-line 445) was an enum literal with no surface contract; downstream implementers had to invent the route tree, persistence model, and seedable-config integration. T-08 closes that gap and binds the §24 settings shell to the foundational seedable-config concept (which previously had no §24 anchor). R-09..R-15 are scoped to §24 (not §23) because they are settings-surface-only — keeping them with §24 prevents §23 REST contract bloat.
- **Verification**: `rg -n '^## Settings Surface|AC-ADS-UI-03' spec/24-app-design-system-and-ui/00-overview.md` → 2 matches ✅. Cross-References heading preserved.
- **Scorecard delta**: §24 C2 Completeness 19→20 (settings vertical now complete) — REQUIRES self-enforcing mechanism: AC-ADS-UI-03 (in-spec) + §27 backlog gate `seedable-config-row-present-check` (NEW). AC alone supports 19; C2=20 is **conditional** on §27 gate shipping within 3 turns or reverts to 19 (self-decay clause). C5 stays at 20 (already at ceiling under T-07 mechanism).
- **Invalidation triggers**: removing any S-1 row · removing any S-2 row · weakening S-3 invariants 1 or 2 (which would silently allow seed-row mutation) · breaking S-4 inheritance · removing AC-ADS-UI-03 · materialising R-09..R-15 in §23 instead of as §24-scoped extensions.

### v4.15.0 — 2026-05-10 — Phase-5 T-09: AppShell route matrix pinned (AC-ADS-UI-04)

- **Action**: Inserted new normative subsection **"AppShell Route Matrix (Normative — Phase-5 T-09)"** in `00-overview.md` between the AppShell React skeleton and Responsive breakpoints (Inlined Contracts section). Contents: 8-row AS-NN matrix (`/`, `/login`, `/apps`, `/apps/$AppId`, `/resolve`, `/settings`, `/api/*`, `*` notFound) → AppShellVariant {Marketing, Console, Settings, Modal} + Auth-gated flag, 4-row variant→behaviour binding table (AppToolbar/AppSidebar/AppCanvas-padding/Used-by columns), 4 binding invariants (matrix is single source of truth, Marketing forbids transitive AppShell imports extending AC-ADS-06, Console+Settings share toolbar height token, 5th enum value requires 5th binding-table row), AC-ADS-UI-04 self-enforcing AC.
- **Why**: `AppShellVariant` enum (file-line 511) had 4 values with no binding to which routes use which variant; downstream implementers had to invent the route→variant mapping. T-09 closes that gap and gives `appshell-route-matrix-check` (§27 backlog) a normative target. Invariant 1 makes the matrix mechanically enforceable. Invariant 2 transitively extends the existing AC-ADS-06 marketing-import boundary to cover indirect imports.
- **Verification**: `rg -n '^### AppShell Route Matrix|AC-ADS-UI-04' spec/24-app-design-system-and-ui/00-overview.md` → 2 matches ✅. Responsive breakpoints heading preserved (auto-restored after accidental consume).
- **Scorecard delta**: §24 C4 Consistency 19→20 (route matrix locks the §24↔TanStack route binding) — REQUIRES self-enforcing mechanism: AC-ADS-UI-04 (in-spec) + §27 backlog gate `appshell-route-matrix-check` (NEW). AC alone supports 19; C4=20 conditional on §27 gate shipping within 3 turns or reverts to 19 (self-decay clause). C2 and C5 already at 20 (T-07/T-08).
- **Invalidation triggers**: removing any AS-NN row · removing the variant→behaviour binding table · weakening invariants 1, 2, or 4 · adding a 5th `AppShellVariant` enum value without a 5th binding-table row · removing AC-ADS-UI-04.
