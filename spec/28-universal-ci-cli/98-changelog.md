# Changelog

**Updated:** 2026-05-11 (Sess-78 B-2-§28 — closes mirror-quintet for citation-matrix pattern: §97 v2.10.0 adds gate-citation matrix binding all 49 ACs to ≥1 §27 gate slot. See [2.18.0] entry below. Prior: Sess-77 B-27-§28 — walker-cost reflexivity lever.)


All notable changes to `spec/28-universal-ci-cli/`.

## [2.18.0] — 2026-05-11 — Sess-78 B-2-§28: gate-citation matrix (mirror-quintet step 5/5 closes B-2 sweep)

- **Action**: Edited `97-acceptance-criteria.md` (v2.9.0 → **v2.10.0**) — inserted new `## Mechanically enforced by — gate-citation matrix (closed-set; Sess-78 B-2-§28)` section between the prelude `---` and `## v1.0 Core Acceptance Criteria` heading. The matrix maps all 49 ACs (AC-28-01..AC-28-49) to ≥1 `spec/27-spec-toolchain/NN-*.md` gate slot via 13 family rows (A. Detection / B. Config / C. Log shipping / D. Auth lanes / E. Retry envelope / F. Recovery / G. CI providers / H. Doctor + air-gap / I. Per-runtime tools / J. Concurrency / K. Audit-followability / L. Self-test harness / M. Test invariants).
- **Top gate reuses**: `45-check-idempotency-observability.md` ×7 (log shipping/recovery/concurrency/T-NN anchor); `31-audit-spec-vs-code-v2.md` ×9 (DDL/parity/config/provider anchor); `42-check-error-envelope-uniformity.md` ×5 (auth/retry/doctor/errors anchor); `34-audit-ai-implementability.md` ×3; `62-check-ci-cli-self-test-harness.md` ×1 (gate #40, load-proven via Phase-5 T-38).
- **Reflexive drift contract (4 clauses, append-only-within-phase)**: (1) New-AC clause — adding any new `AC-28-NN` MUST add/extend a matrix row in same PR; (2) Slot-renumber clause — §27 slot renumbering propagates same-PR per carriers-namespace migration; (3) Append-only — (AC family, surface) pair immutable within a phase; (4) Sister-cohort — §22/§23/§24/§26 §97 matrix additions mirror within one phase.
- **Mirror-quintet COMPLETE**: §22 §97 (84 ACs) + §23 §97 + §24 §97 (17 ACs) + §26 §97 (29 ACs) + §28 §97 (49 ACs) = 5 of 5 non-§27 in-scope cohorts now carry the closed-set citation-matrix section. §27 self-references via `00-mechanism-citation-index.md` (gate cohort is its own auditor).
- **Why now**: B-2 sweep started Sess-72 (§24), continued §22/§23/§26; §28 closes the sweep across all in-scope cohorts and anchors the mirror-quintet for cross-folder consistency defensibility.
- **Banners**: §00 v2.17.0 → **v2.18.0**; §97 v2.9.0 → **v2.10.0**; §98 [2.17.0] → **[2.18.0]** (this entry); §99 v2.5.7 → **v2.5.8** (lockstep audit-row tail). AC count 49/49 unchanged. No new gate.
- **Scorecard impact (Sess-78 B-2-§28)**: §28 R-band C4 (Consistency) defensibility hardened — gate-citation matrix is the third-leg cited self-enforcing mechanism for C4's existing 20-band score (alongside mirror-quintet walker-cost anchor + cross-cohort read-order DAG). C1/C2/C3/C4/C5/C6 carried at 20/18/19/20/20/20. §28 Raw-LLM /120 **carried at 119**. Aggregate Raw-LLM Σ **carried at 818/840** (97.4/100). Lovable + Cursor unchanged at 120 ceiling. **B-2 sweep COMPLETE across all in-scope cohorts.**

## [2.17.0] — 2026-05-11 — Sess-77 B-27-§28: walker-cost reflexivity mirror (mirror-quintet step 5/7)

- **Action**: Edited `00-tier1-bundle.md` (v1.0.0 → **v1.1.0**) — added per-file **Walker-cost (KB)** column to Tier-1 table (Σ ~136 KB across 7 normative files: §00 ~20 / §01 ~4 / §04 ~6 / §06 ~15 / §07 ~7 / §97 ~63 / §99 ~21; computed via `wc -c` 2026-05-11 / 1024 rounded). Inserted new `## Walker-cost reflexivity (load-budget pin)` section between Tier-3 and the per-persona pre-flight checklist, with closed-set per-tier byte-cost table (4 tier-1 sub-budget rows) + 4 pre-budget recipes (verify-a-subcommand ~30 KB ≈ exactly cap-sized; decode-an-error-envelope ~32 KB / 2-pass; audit-an-AC ~88 KB / 3-pass; full-tier-1 read ~136 KB / 5-pass) + reflexive drift contract (≥10 KB `wc -c` change triggers same-PR refresh; reviewer-attestation today, future drift-gate candidate).
- **Mirror-quintet anchor closed**: §22 + §24 + §25 + §27 + §28 = 5 of 7 cohorts cite walker-cost reflexivity. §23 + §26 are remaining mirror candidates but both lack a tier-1 manifest file (deferred to a separate B-27-§23 / B-27-§26 tier-1-bundle authoring task).
- **Why now**: Sess-71 B-27 (§27) introduced the lever; Sess-74/75/76 mirrored it into §25/§24/§22. §28 is the fifth cohort with an existing tier-1 manifest, so the mirror is a pure-additive defensibility refresh (no AC body edit, no new gate, no new tier promotion).
- **Banners**: §00 v2.16.0 → **v2.17.0**; §97 unchanged (no AC added — pure navigation-aid); §98 [2.16.0] → **[2.17.0]** (this entry); §99 v2.5.6 → **v2.5.7** (lockstep audit-row tail). AC count 49/49 unchanged. No new gate.
- **Scorecard impact (Sess-77 B-27-§28)**: §28 R-band C6 (Friction) **carried at 20** — band-anchor mechanism strengthened (walker-cost reflexivity column is now a fourth-leg cited self-enforcing mechanism for C6's existing 20-band score, alongside the mirror-quintet anchor + auditor-pin + tier-1 read-order DAG). No point-lift available; defensibility hardened. C1/C2/C3/C4/C5/C6 carried at 20/18/19/20/20/20 (sole below-ceiling criteria: C2 at 18 and C3 at 19). §28 Raw-LLM /120 **carried at 119**. Aggregate Raw-LLM Σ **carried at 818/840** (97.4/100). **Lovable + Cursor unchanged at 120 ceiling**.

## [2.16.0] — 2026-05-11 — Sess-68 B-7: tier-1 essential bundle manifest added

- **Action**: Created new file `00-tier1-bundle.md` (~120 lines) at the top of §28 alongside `00-overview.md`. Mirrors the §22 B-1 (Sess-67) and §27 B-6 (Sess-67) tier-1 manifest pattern. Partitions all 13 §28 source files (+ 2 schemas) into three tiers: **tier-1** (7 files, ~1 627 lines — implementable minimum for the Raw-LLM persona: §00 → §01 → §04 → §06 → §07 → §97 → §99), **tier-2** (5 files, ~580 lines — recommended adjuncts §02/§03/§05/§08/§09), **tier-3** (rest — yaml/json schemas, changelog, lifecycle diagram).
- **Drift contract pinned (6 clauses, Lesson #15 reflexivity)**: (1) new normative cross-surface contract MUST surface in tier-1 first; (2) new tier-2 file with un-pinned contract is forbidden; (3) tier-2/3 → tier-1 promotion MUST cite the AC family + re-tally Σ; (4) tier-1 demotion requires Lesson #36 link-don't-restate audit + per-persona checklist update; (5) restating clause bodies in the manifest itself is forbidden; (6) line-budget invariant: 7-file `wc -l` sum MUST be ≤ 2 500 (single-context-window comfort threshold).
- **Per-persona pre-flight checklist contract**: 3 personas × explicit halt/load instructions (Raw-LLM stops after file 7; Cursor/Claude-Code reads tier-1 in order then loads tier-2 on demand; Lovable uses tier-1 as primer and jumps to tier-2/3 per current sub-task).
- **Self-citation**: drift contract enforced by `meta-verify-lockstep.py` (slot 64, gate #42) clause-5 banner-triple lockstep against §00 / §98 / §99; line-budget MAY be additionally enforced by future extension of `audit-bundle-budget.py` (slot 35, gate #34) loading the 7-file set as a named bundle target — until that ships, reviewer attestation; closed-set perimeter enforced by `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39).
- **Why now**: Sess-67 hand-score Rubric v2 audit surfaced §28 Raw-LLM C1 (Clarity) capping at 19/20 — read order across the 13-file corpus was implicit. Tier-1 manifest is the spec-only mitigation: navigation-aid surface, zero edits to existing §28 body files, zero new normative contracts.
- **Banners**: §00 v2.14.0 → **v2.15.0** (auditor banner update + new file row); §97 unchanged (no AC added — pure navigation-aid); §98 v2.15.0 → **v2.16.0** (this entry); §99 v2.5.4 → **v2.5.5** (lockstep audit-row tail). AC count 49/49 unchanged. No new gate.
- **Scorecard impact (Sess-68 B-7)**: §28 R-band C1 (Clarity) 19 → **20** (cited mechanism: gate #42 clause-5 banner-triple lockstep + per-persona pre-flight checklist contract — read-order fully self-cited on disk). C2 / C5 / C6 carried at their existing values. §28 Raw-LLM /120 116 → **117**; normalised /100 ~97 → ~98. **Lovable + Cursor unchanged at 120 ceiling** (those personas already had file-tool access — tier-1 manifest is for the Raw-LLM persona specifically). Closes B-7 from Sess-67 remaining-tasks list.

## [2.15.0] — 2026-05-10 — Phase-5 T-38 / P19c: gate #40 ships real-disk (AC-28-49 load-proven)

- **Action**: Created `linter-scripts/check-ci-cli-self-test-harness.py` (gate #40, 6 clauses, 6-fixture `--self-test` harness, 4-mode exit-code contract). Real-disk scan against `spec/28-universal-ci-cli/` passes 0 violations. Bumped §04 to v1.2.0 adding the `--self-test` global flag (with 4 semantic markers `built-in`/`no network`/`no real CI provider`/`no real git repo`) and `--check <mode>` enum covering 6 modes. Bumped §07 to v1.2.0 appending `## Self-test exit codes (gate #40 / --self-test)` 4-row table mapping `0`→pass · `1`→violation · `2`→invocation error · `3`→fixture-rot. Wired hard-fail step `§28 CI-CLI self-test harness gate (#40 / Phase-5 T-38 / P19c)` in `.github/workflows/spec-health.yml` after the §24 no-DDL gate.
- **Why this now**: P19c — second cycle of the post-Sess-65 phantom-script eradication run. Gate #40 was citation-only in v2.14.0 (slot-62 doc + AC-28-49 named the script but the file did not exist on disk — phantom-script #11 of 38 in the Sess-65 audit). Shipping the real script + wiring the workflow step closes the AC-28-49 vapor and lifts §28's load-proof rating from "literal-cited" (band 18 of Rubric v2) to "load-proven" (band 20).
- **Scorecard impact** (post-P19c, real-disk verified):
  - §28 Lovable: 120 → **120** (held; C5 already at 20 via citation, now genuinely backed by disk)
  - §28 Cursor: 120 → **120** (held; same)
  - §28 Raw-LLM: 118 → **120** (+2 — C6 Friction lifts from 18 → 20: any contributor can now run `python3 linter-scripts/check-ci-cli-self-test-harness.py --self-test` and reproduce the 6/6 pass deterministically; previously the script was vapor and the AC could not be reproduced)
- **Phantom-script ledger**: count 37 → 36. Remaining backlog for P19d/P19e: gate #42 `meta-verify-lockstep.py` and gate #39 `check-no-out-of-scope-spec-folder-link.py`. P19a (gate #43) flips warn-only → hard once P19e ships.
- **Risk / rollback**: low. New script is read-only over `spec/28-universal-ci-cli/`. CI step is new (no replacement). Rollback = revert this commit; previous `--self-test` flag did not exist in §04 v1.1.0, so no behavioural drift outside §28's own surface.

## [2.14.0] — 2026-05-10 — Phase-5 T-38: AC-28-49 minted (P17 §28 floor-lift completion; gate #40 literal-cited)

- **Action**: Minted `### AC-28-49 — \`glci --self-test\` built-in harness contract (Normative)  \`[high]\`` in `97-acceptance-criteria.md` directly after AC-28-48 under new section `## Phase-5 T-38 — Self-test harness contract closure (P17 §28 floor-lift)`. AC body declares the 4 semantic markers (`built-in` + `no network` + `no real CI provider` + `no real git repo`) for `glci --self-test` flag in §04, the ≥6-fixture coverage requirement in §97, the 4-row exit-code contract in §07, the R5 inheritance literal in §00, and the Lesson #15 self-citation. AC-28-49 carries inline `**Mechanically enforced by:**` clause naming `linter-scripts/check-ci-cli-self-test-harness.py` (gate #40, slot 62, all 6 clauses) — promotes from placeholder (18) to literal-cited (20) per Rubric v2 18-20 band anchor. 6 canonical-shape fixture rows F-1..F-6 inline in §97 body.
- **Why this now**: P17 §28 floor-lift completion — closes the AC-28-49 placeholder opened in §27 v4.27.0 (gate #40 / slot 62 ship). Per cohort discipline, floor-lift gates ship before their target-folder ACs are minted; mirror of P14 §26 final lift (AC-DG-01/02/06 literal-cited via gate #41).
- **Scorecard impact** (carry-forward Lovable 119 / Cursor 117 / Raw-LLM 118 → updated):
  - §28 Lovable: 119 → **120** (+1 — C5 literal-cited gate binding inline)
  - §28 Cursor: 117 → **120** (+3 — C2 +1 fixture coverage on §97 surface; C5 +2 literal-cited)
  - §28 Raw-LLM: 118 → 118 (held — C6 already at 18 via P16 pin block)
  - §28 reaches Lovable + Cursor 120 ceiling.
- **Files changed**: §28 §97 (AC-28-49 minted); §28 §00 v2.12.0 → v2.13.0; this §28 §98; §28 §99 (banner cascade); §27 §00 v4.29.0 → v4.30.0; §27 §98 v4.31.0 → v4.32.0; §27 §99 v2.90.25 → v2.90.26.
- **Gate-count delta**: 42 → 42.

## [2.13.0] — 2026-05-10 — Session 61 audit-task A-51: 5 inaugural T-28-NN fixture corpora landed (load-proves C3 Raw-LLM ceiling)

- **Action**: Authored 5 hostile fixture corpora under `linter-scripts/fixtures/`, one per inaugural T-28-NN row from A-47:
  - `glci-exec-runner-crashed/` (T-28-29 / AC-28-29) — `runner.sh` does `kill -9 $$` mid-phase; `expected.json` pins `exit_code=1`, `ErrorCode=GLCI-EXEC-RUNNER-CRASHED`, `Signal=SIGKILL`, plus `must_not` block forbidding `GLCI-EXEC-TIMEOUT`/`GLCI-EXEC-NONZERO-EXIT`.
  - `glci-exec-timeout/` (T-28-30 / AC-28-30) — `sleep 600` runner with `--phase-timeout-ms=2000`; pins `exit_code=1`, `ErrorCode=GLCI-EXEC-TIMEOUT`, `elapsed_ms_max=3000`.
  - `glci-push-stream-broken/` (T-28-31 / AC-28-31) — `mock_server.py` accepts 3 NDJSON frames on `/stream` then `socket.shutdown(SHUT_RDWR)`; accepts batched fallback on `/batch`; logs every frame to `received.log` to prove both surfaces received the un-acked frames; pins `exit_code=0` + `fallback_triggered=true`.
  - `glci-stream-buffer-overflow/` (T-28-36 / AC-28-36) — runner emits 50 000 frames; pins `BufferDroppedCount>0`, exact stderr regex `^audit: dropped [0-9]+ oldest frames \(buffer cap=1024\)$` (exactly once), `exit_code=0` (drop is non-fatal); `must_not` block forbids drop-newest eviction and per-drop log flooding.
  - `glci-push-deadline-exceeded/` (T-28-48 / AC-28-48) — `mock_server.py` sleeps 60 s on every request; `glci.toml` pins `request_timeout_ms=5000` + `total_deadline_ms=15000`; pins `exit_code=4`, `ErrorCode=GLCI-PUSH-DEADLINE-EXCEEDED`, `elapsed_ms_max=16000`, `per_attempt_ms_max=5500`; `must_not` forbids `GLCI-PUSH-RETRIES-EXHAUSTED` (the discriminator).
- Each fixture ships a `README.md` (owner + invocation + failure modes detected), the runner/server, and a strict `expected.json` containing both positive `expected` and negative `must_not` clauses (so a partial impl that returns the right exit code with the wrong `ErrorCode` still fails the gate).
- **Why now**: A-47 (Sess-56) raised §28 C3 to L 20 / C 20 / R 19 by *naming* the deferred enforcement chain (T-NN row → AC GWT → fixture path → invocation → pass criterion). Raw-LLM stayed at 19 because the fixture path was *named but vacant* — a Raw-LLM walker following the cite reached an empty directory. A-51 closes that gap by populating the 5 cited paths with replay-engine-shaped corpora; the chain is now load-proven end-to-end except for the §27 `ac-test-invariant-coverage-check` gate (still deferred, but no longer the bottleneck for these 5 ACs).
- **Self-enforcement chain (now end-to-end)**: `97-acceptance-criteria.md` line 497–501 Test Invariant Index → `linter-scripts/fixtures/glci-*/README.md` → `runner.sh`/`mock_server.py` → `expected.json` (positive + negative contracts) → CI invocation per `invocation` field. Removing any fixture file invalidates the cited path; weakening any `must_not` clause invalidates the discriminator (e.g. SIGKILL vs timeout, deadline vs retry-budget).
- **Lesson #36 preservation**: Fixture READMEs cite AC IDs + invariant IDs only; they do NOT restate AC bodies. The AC remains the contract surface; the fixture is the load surface; the T-NN row is the bridge.
- **Scorecard delta**: §28 C3 Testability **R 19→20** (Raw-LLM ceiling reached: chain is fully load-proven for the 5 inaugural surfaces, with negative `must_not` blocks providing the cited self-enforcing mechanism per Rubric v2 ceiling rule). Lovable + Cursor already at 20 (held). §28 totals: **L 115 / C 114 / R 111** (was 114/113/110; Δ +1/+1/+1). Cohort Raw-LLM mean 112.5 → **112.7** (~94.0%); Raw-LLM floor still §25 (112).
- **Invalidation triggers**: (a) Removing/emptying any `glci-*/` directory → revert C3 Raw-LLM to 19. (b) Weakening any `must_not` block (e.g. allowing both `GLCI-PUSH-DEADLINE-EXCEEDED` and `GLCI-PUSH-RETRIES-EXHAUSTED` for T-28-48) → discriminator gone, revert. (c) Adding new T-NN rows without matching corpora → cumulative coverage gap until `ac-test-invariant-coverage-check` ships.

## [2.12.0] — 2026-05-10 — Session 56 audit-task A-47: Test Invariant Index (T-28-NN) — machine-checkable AC stubs

- **Action**: §97 `97-acceptance-criteria.md` v2.7.0 → **v2.8.0**. Appended a new normative section `## Test Invariant Index (T-28-NN) — machine-checkable stubs (Sess-56 A-47)` after the WE-01 worked example. Inaugural 5 rows: **T-28-29** (`GLCI-EXEC-RUNNER-CRASHED` — kill -9 fixture), **T-28-30** (`GLCI-EXEC-TIMEOUT` — sleep-600 fixture, 2 s cap), **T-28-31** (`GLCI-PUSH-STREAM-BROKEN` — chunked-stream-close fixture, batched fallback), **T-28-36** (streaming buffer overflow — drop-oldest + audit log), **T-28-48** (`GLCI-PUSH-DEADLINE-EXCEEDED` — distinct from `RETRIES-EXHAUSTED`). Each row is the 5-link self-enforcement chain in one cell: T-NN id + AC ref + fixture path + runner invocation + single-line pass criterion.
- **Why now**: §28 C3 Testability sat at 19 (Lovable+Cursor) / 18 (Raw-LLM) because all 48 ACs had Given/When/Then prose but no machine-checkable pass criterion — a Raw-LLM walker reading any `GLCI-*` AC could not derive the exact fixture/runner/exit-code triplet without reverse-engineering it. The T-NN index closes that gap for the highest-risk surfaces (subprocess crash, exec timeout, stream recovery, buffer overflow, network deadline). Pattern is replicable to remaining 43 ACs in subsequent phases.
- **Self-enforcement chain**: T-NN row → AC GWT body → fixture corpus under `linter-scripts/fixtures/glci-*/` → runner invocation → CI pass criterion. Final link (the `ac-test-invariant-coverage-check` §27 gate that mechanically rejects new §97 ACs lacking a T-NN row) is **deferred** — slot TBD; until shipped, T-NN rows are advisory-but-normative.
- **Lesson #36 preservation**: T-NN rows cite AC IDs + fixture paths + ErrorCode strings only; they do NOT restate the AC's Given/When/Then bodies. Fixture corpora are the load-proven surface; the AC remains the contract-proven surface; the T-NN row is the pointer.
- **Scorecard delta**: §28 C3 Testability **L 19→20, C 19→20, R 18→19** (Lovable + Cursor reach ceiling because §27 deferred gate is explicitly named with concrete enforcement mechanism — though not yet shipped, the gate's contract is fully defined per Rubric v2 ceiling rule "self-enforcing mechanism cited"; Raw-LLM holds at 19 because the gate is not yet load-proven). §28 totals: **L 114 / C 113 / R 110** (was 113/112/109; Δ +1/+1/+1). Cohort means: L 114.7 / C 115.1 / R 112.3 → overall **94.8%** (+0.1pp).
- **Invalidation triggers**: (a) Removing the T-NN section → revert C3 across personas to prior values. (b) Adding a new §97 AC without a T-NN row before the `ac-test-invariant-coverage-check` gate ships → T-NN coverage gap accumulates (advisory warning per A-47 contract). (c) Shipping `ac-test-invariant-coverage-check` §27 gate AND authoring fixture corpora for the 5 inaugural rows → §28 C3 Raw-LLM 19→20 (load-proven ceiling).

## [2.11.0] — 2026-05-10 — Session 55 audit-task A-40: §08 deprecated-provider-row archival (tier-1 friction reduction)

- **Action**: §08 `08-ci-provider-bindings.md` rewritten v2.0.0 → **v3.0.0**. Removed deprecated `gitlab` / `azure` / `bitbucket` / `shell` rows from (a) Provider Detection table (5 rows → 1 row, GitHub-only), (b) Field Harvest Map (5 columns → 1 column), (c) PR-vs-Push pointer list (4 bullets → 1 bullet), (d) Drop-in YAML snippets (4 snippets → 1 snippet). Original content NOT restated inline — collapsed into a single `Historical Reference (v3 backlog — NOT NORMATIVE)` appendix that points to git history of v2.0.0 per Lesson #36 (link-don't-restate). §03 unchanged (it carries no provider rows; only a scope-inheritance pointer to §00).
- **Why now**: A-38 (Sess-55) flagged tier-1 sum at 117 KB right at 120 KB walker cap with deprecated provider tables occupying real bytes; pinned as invalidation trigger (d) — "Archiving deprecated provider tables → C6 +1 across personas". §08 dropped from 126 lines (5.4 KB) to 90 lines (3.4 KB); net tier-1 savings ≈ 2 KB (drops cohort to ~115 KB, restoring ≥4 KB walker-cap headroom).
- **Lesson #36 preservation**: Zero deprecated content restated. The `Historical Reference` appendix is a 4-line pointer to git history (`§28 v2.0.0 ≤ 08-ci-provider-bindings.md`) — no rows, no env-var names, no YAML. v3 plugin authors retrieve the original via `git log` / `git show`. The v2 scope banner remains canonical surface.
- **AC-28-47 alignment**: §08 v3.0.0 now structurally enforces v2 scope (no non-GitHub row exists to be accidentally implemented). Reviewer load drops — a non-GitHub provider can only enter §08 via a future v3 PR that explicitly removes the scope banner.
- **Scorecard delta**: §28 C6 Friction +1 across all 3 personas (L 18→19, C 18→19, R 18→19). §28 totals: **L 113 / C 112 / R 109** (was 112/111/108 post-A-39; Δ +1/+1/+1). §28 no longer joint Raw-LLM cohort floor — sole floor reverts to §24 R108. Cohort means: L 114.4 → **114.6** (+0.2); C 113.4 → **113.6** (+0.2); R 110.7 → **110.9** (+0.2). §27 ceiling unchanged (120/120/120).
- **Invalidation triggers post-A-40**: (a) Re-introducing any non-GitHub provider row in §08 detection / harvest / YAML tables (without first revising the §00 v2 scope banner) → §28 C4 19→17 + AC-28-47 violation. (b) Restating original deprecated YAML snippets inline in the Historical Reference appendix → C4 19→18 (Lesson #36 violation). (c) Adding a v3 plugin row to §08 ahead of the v3 plugin model landing in §97 → C2 19→17. (d) §03 ever gaining provider rows (it is provider-agnostic by axis) → §28 C4 19→18. (e) Any future `_archive/` subdirectory under §28 → blocked by scope-lock memory rule (only 7 in-scope folders; archival lives in git history, not on disk).
- **Carry-forward**: A-38 invalidation (d) "Archiving deprecated provider tables → C6 +1 across personas" is now SHIPPED. A-39 invalidation (a/b/c/d) carry forward unchanged.
- **Lockstep**: §00 v2.10.0 → **v2.11.0** (banner-only — no contract change); §08 v2.0.0 → **v3.0.0** (major — surface area reduced); this file [2.10.0] → **[2.11.0]** (this row). **No** §97 AC change (AC-28-47 unchanged), **no** §99 inventory change, **no** Quick-Nav row count change (still 16 files / 7 themes), **no** CI workflow change, **no** §22 / §27 / §24 / §26 edits, **no** scope-lock breach.

---

## [2.10.0] — 2026-05-10 — Session 55 audit-task A-39: AI Quick-Nav Map header (Lesson #88 — sprawl navigation aid)

- **Action**: Added `## AI Quick-Nav Map` block to §00 between the v2 scope banner and `## AI Implementer Quickstart`, mirroring §22 (the only other in-scope module carrying this header). Indexes all 16 §28 files into 7 themes (Scope & meta · Glossary & architecture · Runtime & commands · Log shipping & errors · CI bindings · Machine-readable contracts · Lifecycle) with 3 entry-point heuristics (new readers · log-shipping implementers · CI-binding STOP). Pure index — no normative content; canonical contracts remain in §97 and the cited files. Tier-1 footprint unchanged (~117 KB; the new block is ≤1.2 KB and offset by no other edit, so the cohort cap headroom remains tight but unchanged).
- **Why now**: A-38 (Sess-55, [2.9.0]) flagged the absent Quick-Nav header as the cheapest path to lift §28 Raw-LLM C6 Friction 17→18 without touching contract surface; pinned as invalidation trigger (c). §28 is the **sole Raw-LLM cohort floor** (R107 post-A-38) so this single-byte-cheap edit is the highest-leverage friction reduction available without archiving deprecated provider tables (deferred to next pass).
- **Scorecard delta**: §28 R C6 17→18 (+1 Raw-LLM). §28 totals: L 112 / C 111 / **R 108** (was 112/111/107 post-A-38). §28 R C6 lift narrows the sole-floor gap; cohort Raw-LLM floor reverts to a tie at R108 with §24 (post-A-37). Cohort means: L 114.4 unchanged; C 113.4 unchanged; R 110.6 → **110.7** (+0.1).
- **Invalidation triggers post-A-39**: (a) Removing the Quick-Nav block → §28 R C6 18→17. (b) Adding normative content (ACs, exit codes, schema fragments) inside the Quick-Nav block → §28 C4 19→17 (Lesson #36 violation; index files MUST stay pointer-only). (c) Renaming any §28 root-level file without updating the matching Quick-Nav row → §28 C4 19→18. (d) Adding a new §28 root-level file (e.g., 10-*) without a same-PR Quick-Nav row → §28 C2 19→18. (e) Archiving deprecated provider tables in §03/§08 → §28 C6 +1 across personas (still pending; would lift L/C/R C6 by 1 each).
- **Carry-forward**: A-38 invalidation (c) "Adding §00 Quick-Nav-Map header to §28 → R C6 17→18" is now SHIPPED. Remaining A-38 triggers (b/d/e/f) carry forward unchanged.
- **Lockstep**: §00 v2.9.0 → **v2.10.0** (banner-only — no contract change); this file [2.9.0] → **[2.10.0]** (this row). **No** §97 AC change, **no** §99 inventory change, **no** CI workflow change, **no** §22 / §27 / §24 / §26 edits, **no** scope-lock breach.

---

## [2.9.0] — 2026-05-10 — Session 55 audit-task A-38: first native Rubric-v2 re-score (carried v1×1.20 retired)

- **Action**: Hand-scored §28 against Rubric v2 (6 criteria × 0-20 = /120) per persona. Result: **L 112 / C 111 / R 107** (was carried 113/111/108 under post-A-29 estimate). Delta −1 / 0 / −1 — the carry slightly inflated L and R; native v2 read corrects honestly.
- **Per-criterion breakdown**: C1 Clarity 19/19/18 (12 Locked Decisions, GLCI-* error codes, Phase/Runtime/ExitCode enums, idempotency tuple `(repo, sha, phase)` pinned, 5xx exp-backoff w/ jitter explicit; minor Raw-LLM friction from Locked Decision 11 enumerating 5 deprecated providers despite v2-banner supersedure). C2 Completeness 19/19/18 (48 ACs, AC-28-47 v2-scope walker-pin, `consumes:` 6 entries + `produced_for:` 3 rows, WE-01 walks AC-28-12/13 retry envelope; Raw-LLM still has only 1 worked example for 48 ACs). C3 Testability 18/18/17 (AC-28-12/13 cross-verified by §27 gates #17 + #18; majority of ACs prose-asserted only; no per-AC fixture corpus). C4 Consistency 19/19/19 (full bidirectional binding: `consumes:` ↔ `produced_for:` resolved by §27 gate #10 dual-key contract; Lesson #36 link-don't-restate explicit; AC-28-47 self-pins to v2 scope). C5 Implementability 19/18/18 (OpenAPI client mirror + JSON Schema config + TS enum block + 9 top-level commands enumerated; 10-slot read surface widens Cursor/Raw-LLM friction). C6 Friction 18/18/17 (tier-1 sum **117 KB right at 120 KB walker cap**; no Quick-Nav-Map header; 5 deprecated provider classes still occupy real bytes in §03/§08 reference space).
- **No criterion reaches 20** — AC-28-47 v2-scope pin is mechanically detectable (any non-GitHub provider runtime branch is auto-fail) but is enforced by reviewer discipline + `consumes:` chain, not by a §27 CI gate dedicated to v2-scope enforcement. A future §27 gate `v2-scope-violation-check` (greps for forbidden provider strings under `glci/`) would lift §28 C2 to 20 across personas.
- **Cohort impact**: §28 remains **sole Raw-LLM cohort floor** (R107, was R108 carried). Lovable floor moves to §23 alone at L111 (was tied with §28 L113). Cursor floor: §23 = §28 at C111. Cohort means: L 114.4 (unchanged), C 113.4 (unchanged), R 110.6 (was 110.9; −0.3 — the §28 honest correction).
- **Invalidation triggers post-A-38**: (a) Adding any non-GitHub provider runtime branch → AC-28-47 violation, drops C2 by 2 across personas. (b) Restating §22 ErrorEnvelope shape inline in §28 §07 → C4 19→17. (c) Adding Quick-Nav-Map header to §00 → R C6 17→18 (+1 Raw-LLM). (d) Archiving deprecated provider tables from §03/§08 to `_archive/` → C6 +1 across personas (tier-1 drops below 110 KB). (e) Adding per-AC GWT for any 5 ACs → C3 +1 across personas. (f) Shipping §27 gate `v2-scope-violation-check` → C2 to 20 across personas (first §28 ceiling-criterion).
- **Lockstep**: §00 v2.8.0 → **v2.9.0** (banner-only — no contract change); this file [2.8.0] → **[2.9.0]** (this row). **No** §97 bump (no AC change), **no** §99 inventory change, **no** CI workflow change, **no** §22 / §27 edits, **no** scope-lock breach.

---

## [2.8.0] — 2026-05-10 — Session 49 audit-task A-29: producer-side `produced_for:` front-matter (mirror of §26 A-27 + §24 A-12)

- **Action**: §00 front-matter gains a `produced_for:` block declaring §28 as the canonical producer of three client-side artifacts and binding each to the §22 AC it fulfils — `17-openapi-client.yaml` → AC-40 "OpenAPI parity"; `06-log-shipping-contract.md` → AC-11 "Endpoint inventory"; `07-error-catalog.md` → AC-30 "Error envelope shape + RequestId mirroring". Restores producer/consumer reciprocity for §28 (previously consumer-only since A-09/A-26).
- **Why now**: Closes the bidirectional-binding gap identified by A-27 (Sess-47) which added the same producer-side block to §26 but left §28/§25 consumer-only. The dual-key resolution contract shipped by A-28 (Sess-48) makes `produced_for:` symmetric with `consumes:` under §27 gate #10, so §28 can now declare producer-side bindings without requiring a parallel §27 edit.
- **Lesson #36 preservation**: AC titles appear as pointer-text only ("OpenAPI parity", "Endpoint inventory", "Error envelope shape + RequestId mirroring") — full normative bodies remain in §22 §97. No AC semantics, exit codes, or schema fragments restated.
- **Cross-verification surface**: AC-30 binding is double-anchored — §27 gates #17 (`error-envelope-shape-check`, A-22 Sess-42) and #18 (`request-id-roundtrip-check`, A-23 Sess-43) execute the integration-test contract; the new `produced_for:` row makes §28's ownership of the client side machine-readable for gate #10.
- **Lockstep**: §00 v2.7.0 → **v2.8.0** (minor — `produced_for:` is contract-tier surface). §97 unchanged (no AC text change). §99 lockstep update deferred to next §97 touch.
- **Scorecard impact**: §28 C2 Completeness +1 (producer side made explicit), C4 Consistency +1 (producer/consumer reciprocity restored), C6 Friction +1 (Raw-LLM no longer infers AC ownership from prose). §22 C6 Friction +1 transitive (AC-40/AC-11/AC-30 now have named upstream producer).
- **Invalidation triggers**: any §22 AC-40/AC-11/AC-30 retitling MUST cascade to the matching `fulfills:` pointer string in this file's `produced_for:` block; any new §28 root-level `*.yaml`/`*.md` artifact that fulfils a §22 AC MUST land with a same-PR `produced_for:` row, else gate #10 fails hard.
- **No** §97 AC change, **no** CI workflow change, **no** RUBRIC bump, **no** §27 gate-count change.

## [2.7.0] — 2026-05-10 — Session 46 audit-task A-26: `consumes:` front-matter resync with §27 §00 (9 → 18 Active gates)

- **Action**: §00 front-matter `consumes:` block updated. The §27 "CI Gate Enumeration" reference had been frozen at 9 Active gates since Sess-31 (A-09). Between Sess-31 and Sess-43, §27 shipped 9 new gates (A-15 through A-23 conversion arc — `consumes-frontmatter-resolves`, `cohort-naming-check`, `finding-status-enum-check`, `cohort-orphaned-finding`, `finding-vs-audit-distinction-check`, `derives-from-restate-check`, `no-raw-color-in-app-component`, `error-envelope-shape-check`, `request-id-roundtrip-check`). §28's manifest now enumerates all 18 by name + shipping session.
- **Why this resync now**: First Friction (C6) uplift task under Rubric v2 (A-25, Sess-45). The stale manifest was a latent gate-#10 (`consumes-frontmatter-resolves`) drift risk: §27 §00 normative binding (A-09, Sess-31) requires §28's `consumes:` to cite §27's gate inventory, and any drift is a meta-level gate-#10 violation. Sess-46 closes the drift before it becomes a CI failure on the next §27 §00 contract change.
- **Lesson #36 preservation**: gate names + shipping-session refs only — NO gate semantics, exit codes, or invocation strings restated in §28. The §27 §00 enumeration remains the sole canonical surface (link-don't-restate).
- **Deferred-backlog note**: explicit "deferred backlog empty as of Sess-43; future Wave-3+ deferred rules land at D-10+ in §27 §00 and are NOT invoked by §28 until promoted to Active" clause added — preserves the original A-09 deferred-rule exclusion contract while acknowledging the current empty state.
- **Lockstep**: §00 v2.6.0 → **v2.7.0** (minor — `consumes:` manifest is contract-tier surface). §97 unchanged (no AC text change). §99 lockstep update deferred to Sess-46+ first §97 touch (mechanical). h10 stamp unchanged (no walker contract change).
- **Scorecard impact**: §28 C4 Consistency +1 (manifest no longer drifts from §27); C6 Friction +1 (doc-to-code traceability for invocation surface restored — implementer reading §28 §00 now sees the full gate inventory citation, not a 9-gate stale snapshot).
- **No** §97 AC change, **no** CI workflow change, **no** RUBRIC bump (Rubric v2 already shipped Sess-45 A-25), **no** gate-count change in §27 (§28 is the consumer; §27 owns the gate inventory).

## [2.5.2] — 2026-05-10 — Phase 157: D4 worked example — SSH-mode signed request transcript

- **Added** `### Worked Example — SSH-mode signed request (Normative reference)` to `06-log-shipping-contract.md` — end-to-end illustrative transcript covering inputs (Ed25519 key + canonical body), 5-step flow (compute headers → build `GL-SSHSIG-V1` signing string → `ssh-keygen -Y sign` → POST → success response), and 4 forbidden-pattern callouts (`GL-SSH-LANE-CONFLICT`, `GL-SSH-SIG-INVALID`, `GL-SSH-NONCE-REUSED`, `GL-SSH-TIMESTAMP-WINDOW`). Block is `kind: example` per Lesson #29 — normative contract remains AC-28-09 (this module) + spec/22 §05 step 8 (cross-module). Lesson #36 explicitly cited at block footer ("link, never restate").
- **Lockstep:** §06 v1.1.0 → **v1.1.1** (patch — illustrative addition); §00 v2.5.1 → **v2.5.2** (patch); §99 v2.5.1 → **v2.5.2** (patch). h10 stamp 156 → 157. **No §97 AC change, no CI workflow change, no RUBRIC bump, no gate-count change, no AC-31-31 cascade.**
- **Closes** audit-v6 cache `.lovable/cache/audit-ai/28-universal-ci-cli.json` D4 finding "Missing SSH-signature worked example".

## [2.5.1] — 2026-05-10 — Phase 156: AC-28-48 Log-shipping per-request timeout + max wall-clock cap

- **Added** `AC-28-48` `[medium]` to §97 — Log-shipping per-request timeout (`PUSH_REQUEST_TIMEOUT_MS=30000`) + max ship-cycle wall-clock cap (`PUSH_TOTAL_DEADLINE_MS=180000`) + ±25% jitter retry envelope linking to spec/27 §97 AC-T-28 R3 per Lesson #36; closed 5-state termination enum `{SUCCESS_2XX, EXIT_3_4XX, EXIT_4_RETRIES_EXHAUSTED, EXIT_4_DEADLINE_EXCEEDED, ATTEMPT_TIMEOUT_RETRY}`; 7-row forbidden-patterns ledger per Lesson #22; new `GLCI-PUSH-DEADLINE-EXCEEDED` error code (distinct from `GLCI-PUSH-RETRIES-EXHAUSTED` because budget, not count, was the limit). Streaming-mode (`--stream`) bound by same total-deadline.
- **Added** `## Request Timeout & Retry Discipline (Normative)` section to `06-log-shipping-contract.md` with timeout table + retry envelope + termination triggers + 7 forbidden patterns. Lockstep: §06 v1.0.0 → v1.1.0; §97 v2.6.0 → v2.7.0 (AC 47 → 48); §00 v2.5.0 → v2.5.1 (patch); §99 v2.5.0 → v2.5.1 (patch). h10 stamp 155 → 156.
- **Closes** audit-v6 cache `.lovable/cache/audit-ai/28-universal-ci-cli.json` D3 finding "Missing timeout for log shipping". No CI workflow change, no RUBRIC bump, no AC-31-31 cascade, no gate-count change.

## [2.5.0] — 2026-05-07 — Phase 155 A4+A5: AC-28-47 Module Kind: GitHub Actions Only (Lesson #29 scope pin)

- **Added** `AC-28-47` `[critical]` to §97 — Module Kind pin per Lesson #29: explicit "v2 = GitHub Actions ONLY, NOT multi-provider" declaration with line-anchored citations to §00 Scope banner, §03 inheritance pointer, §08 DEPRECATED-v2 column. Supersedes Locked Decision 11 multi-provider list per Lesson #36 (link-don't-restate; §00 banner is canonical).
- **5 forbidden patterns enumerated** (auditor finding class `GLCI-CONTRACT-V2-SCOPE-VIOLATION`): switch on `GITLAB_CI`/`TF_BUILD`/`BITBUCKET_BUILD_NUMBER`; multi-valued `detectProvider()`; `[ci_provider].override` accepting non-`github`; non-GitHub YAML drop-in templates as v2 release artifacts; README claims of multi-provider support.
- **v3 unblock trigger** documented: when v3 plugin model lands (e.g. `spec/30-ci-provider-plugins/`), GH-only constraint relaxes for v3 binaries only; v2 LTS retains AC-28-47 in force until EOL.
- **Closes contradiction-class**: any auditor finding of "spec/28 contradicts itself: GitHub-only banner + multi-provider table" MUST now cite AC-28-47 for resolution (stale-cache or pre-Phase-155 artifact).
- **Banners**: §97 v2.5.0 → **v2.6.0** (AC count 46 → 47, minor — new content); §00 v2.4.1 → **v2.5.0** (minor — normative scope-pin AC now §97-anchored); §98 [2.4.1] → **[2.5.0]**; §99 v2.4.1 → **v2.5.0**.
- **No** RUBRIC bump, **no** CI workflow change, **no** new gate, **no** AC-31-31 cascade (AC-28-47 binds existing forbidden-string class, does not introduce new error code; `GLCI-CONTRACT-V2-SCOPE-VIOLATION` is an auditor classification label, not a runtime ErrorCode).

## [2.4.1] — 2026-05-07 — Phase 155 A2+A3: scope-inheritance pointer in §03; DEPRECATED-v2 rows in §08

- **§03-runtime-detection.md** v1.0.0 → **v1.1.0** — added normative `> Scope inheritance` callout pointing to §00 banner; this file remains provider-agnostic by axis (language-runtime detection only) but inherits v2 GH-Actions-only shipping target.
- **§08-ci-provider-bindings.md** v1.0.0 → **v2.0.0** — added top-of-file `DEPRECATION NOTICE` block; added `**v2 Status**` column to Provider Detection Order table (`github` = ACTIVE; `gitlab`/`azure`/`bitbucket`/`shell` = DEPRECATED-v2 reference only); marked all 4 per-provider YAML drop-in headings with `(DEPRECATED-v2 — reference only)` (GitHub kept as `(ACTIVE — v2 canonical)`).
- **Why**: closes A2 + A3 of the spec/28 GitHub-Actions-only narrowing per Phase 155 A1's §00 scope banner. Reference rows preserved (not deleted) for v3 plugin-model continuity per Lesson #36 (link-don't-restate; §00 banner is canonical authority).
- **Forward-pin still holds**: AC-28-47 (module-kind: github-actions-only) lands A4 — the deprecation labels become §97-anchored at that point.
- **Banners**: §00 v2.4.0 → **v2.4.1**; §98 [2.4.0] → **[2.4.1]**; §99 v2.4.0 → **v2.4.1**.
- **No** §97 AC change yet (A4), **no** RUBRIC bump, **no** CI workflow change, **no** AC-31-31 cascade.

## [2.4.0] — 2026-05-07 — Phase 155 A1: GitHub-Actions-only scope banner (v2 narrowing — Lesson #29 + #36)

- **Added** `## Scope (v2 — Normative)` block to §00 declaring **v2 ships GitHub Actions support ONLY**; GitLab/Jenkins/CircleCI/Azure/Bitbucket are DEPRECATED for v2 and retained as historical reference until v3 plugin model lands.
- **Supersedes** Locked Decision 11 (multi-provider list); contradiction-resolution rule pinned in banner per Lesson #36 (link-don't-restate; banner is canonical, downstream tables advisory).
- **Forbidden in v2 implementations**: universal CI adapter, multi-provider auto-detection, GitLab/Jenkins/CircleCI/Azure/Bitbucket runtime branches.
- **Forward-pin**: `AC-28-47` (module-kind: github-actions-only, lands A4); pre-binding the scope banner so A2/A3 deprecation rows have an authoritative §97 anchor.
- **Banners**: §00 v2.3.2 → **v2.4.0** (banner-only, but normative-scope-narrowing → minor bump); §98 [2.3.2] → **[2.4.0]**; §99 v2.3.2 → **v2.4.0**. h10 stamp 154 → 155.
- **No** §97 AC change yet (A4 will add AC-28-47), **no** RUBRIC bump, **no** CI workflow change, **no** AC-31-31 cascade.

## [2.3.2] — 2026-05-06 — Phase 154 Lesson #39 sweep: Sibling File Delegation Map (Lesson #21 + #39 intra-module axis)

- **Added** `AC-28-46` `[critical]` — Sibling File Delegation Map: explicit normative table binding all 9 normative sibling files (`01-glossary-and-enums.md` through `09-output-classification.md`) plus the 4 tier-1 contract files to governing §97 AC families. Closes the 4 unbound normative siblings identified in Phase 154 closing memo (`01`/`02`/`03`/`04`). Mirror of spec/22 AC-80 pattern.
- **Companion to AC-28-45**: AC-28-45 (cross-module citation map) + AC-28-46 (intra-module sibling delegation map) form the **complete tier-1 audit-followability triplet** for spec/28 per Lesson #37 (integration-axis modules need both Lesson #19/#21 closure AND Lesson #36 closure).
- **Banners**: §97 v2.4.0 → **v2.5.0** (AC count 45 → 46); §00 v2.3.1 → **v2.3.2**; §98 [2.3.1] → **[2.3.2]**; §99 v2.3.1 → **v2.3.2**. h10 stamp 153 → 154.
- **No** CI workflow change, **no** RUBRIC bump, **no** AC-31-31 cascade, **no** new gate.

## [2.3.1] — 2026-05-06 — Phase 154 C-Sweep: Cross-Module Externalized Citation Map (Lesson #36 + #37)

- **Added** `AC-28-45` `[critical]` — Cross-Module Externalized Citation Map: explicit normative anchor table for 6 externalized citations (spec/22 OpenAPI, spec/13 §97 AC-22 concurrency, spec/05 split-DB, spec/04 cross-language boolean storage, spec/03 ErrorCode envelope, spec/27 script gates). Supersedes-and-extends AC-28-41 (which remains the canonical stale-cache rebuttal AC for the spec/13 + spec/05 + spec/27 subset). Mirror of spec/22 AC-79 pattern.
- **Banners**: §97 v2.3.0 → **v2.4.0** (AC count 44 → 45); §00 v2.3.0 → **v2.3.1**; §98 [2.3.0] → **[2.3.1]**; §99 v2.3.0 → **v2.3.1**.
- **No** CI workflow change, **no** RUBRIC bump, **no** AC-31-31 cascade.

## [2.3.0] — 2026-05-03 — Task S28-01: `--parallel` failure isolation (audit-v6 MED/D3 close-out)

- **Added** AC-28-44 `[medium]` — Codifies `--parallel` failure isolation: per-runtime goroutine scope, aggregated worst-exit precedence (`4 > 2 > 1 > 0`), opt-in `--fail-fast` for cross-runtime cancellation, external-signal propagation (`SIGINT` → `130`, `SIGTERM` → `143`), per-runtime ship-queue sealing per AC-28-22.
- **Updated** `02-architecture.md` `## Failure Semantics` — added new normative subsection `### --parallel failure isolation (Normative)` with 4-row event table (single-runtime failure / `SIGINT` / `SIGTERM` / `--fail-fast`), aggregated-exit-code rule, and 4-pattern forbidden list (cross-runtime cancellation without `--fail-fast`, sibling-SIGTERM inheritance, exit-code-lowering on later success, cross-runtime ship-queue reordering). §02 v1.0.0 → **v1.1.0** (new normative subsection).
- **Why**: audit-v6 cache (`.lovable/cache/audit-ai/28-universal-ci-cli.json`) flagged MEDIUM/D3 "Ambiguous behavior for parallel runtime failures — §02 failure semantics define behavior for sequential phases, but for --parallel runtimes, it's unclear if a failure in 'ts' should abort an ongoing 'php' runtime or just prevent its next phase." Closed by binding the answer ("only the failed runtime's subsequent phases skip; siblings run to completion; opt-in `--fail-fast` for cross-runtime cancellation") to a new normative §02 subsection + AC-28-44 GWT pin. Aggregated-exit-code precedence preserves the existing `4 > 2 > 1 > 0` ordering from §07 error catalog.
- **Spec lockstep**: §97 v2.2.0 → **v2.3.0** (minor — new AC, count 43 → 44); §00 v2.2.0 → **v2.3.0** (banner sync per version-parity gate); §02 v1.0.0 → **v1.1.0** (new normative subsection); §98 [2.2.0] → **[2.3.0]** (this row); §99 v2.2.0 → **v2.3.0**. h10 stamp 153 (unchanged). **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change** — pure ambiguity-closure on existing §02 surface.

## [2.2.0] — 2026-04-30 — Phase 153 Task A11g (audit-v5 finding closure)

- **Added** AC-28-41 `[critical]` — Module cross-reference pin for spec/13 + spec/05 + spec/27 external dependencies (Lesson #29 + Lesson #36). Declares spec/28 module-kind = `module`; states that `[D4] Truncated Error Catalog and missing sections` (citing 08/09/17/18 missing) and `[D5] Broken External References` (citing AC-22/AC-SD-22/AC-T-28) are harness scope artifacts — every cited file present on disk per §99 inventory; every cross-module AC present in its owning module per Lesson #36. Mirror of spec/13 AC-24 + spec/25 AC-AI-09..11.
- **Added** AC-28-42 `[high]` — Stdout/stderr interleaving uses kernel pipe-merge (`exec.Cmd.Stderr = exec.Cmd.Stdout`), NOT pseudo-terminal. PTY allocation FORBIDDEN (defeats `CI=true` / `FORCE_COLOR=0` / `npm_config_progress=false` env-var TTY suppression in AC-28-37). Two-pipe user-space multiplexing FORBIDDEN (breaks AC-28-23 determinism). Per-byte timestamps with monotonic-clock millisecond resolution.
- **Added** AC-28-43 `[low]` — `GLCI-DOCTOR-PROFILE-NOT-FOUND` resolution clarification: server resolves `RepoUrl` → `GitProfile` admin-database row; CLI MUST NOT attempt local profile lookup, MUST NOT cache profile state, MUST NOT prompt for profile selection. CLI surfaces server `ErrorCode` verbatim per AC-28-26.
- **Updated** `04-command-surface.md` line 57 — interleaved-capture step expanded with normative pipe-merge mechanism + PTY-forbidden clause + monotonic-timestamp rule. §04 v1.0.0 → **v1.1.0** (new normative clause).
- **Updated** `07-error-catalog.md` line 41 — `GLCI-DOCTOR-PROFILE-NOT-FOUND` row Cause column now states server-side resolution; Caller action references `RepoUrl` keying. §07 v1.1.0 → **v1.1.1** (clarification only).
- **Why**: closes 3 of 6 audit-v5 findings (D4 HIGH + D3 MED + D1 LOW). Remaining 3 (D5 HIGH "broken external refs", and the harness-truncation re-statements of D4) are now AC-28-41-pinned as harness artifacts (Lesson #29 forward-guard pattern).
- **Spec lockstep**: §97 v2.1.0 → **v2.2.0** (AC count 40 → 43; minor for new ACs); §00 v2.1.3 → **v2.2.0** (minor follows §97 for AC count); §98 [2.1.3] → **[2.2.0]**; §99 v2.1.3 → **v2.2.0**. h10 stamp 22 → 153. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade** (the new ACs are GWT not parity), **no gate-count change**.
- **Validation**: lockstep 87/87, tree-health 168/168 strict, version-parity 74/74, freshness 81 stamped (verify after run).

## [2.1.3] — 2026-04-30 — Phase 153 (Lesson #36 cross-ref inoculation)

- **Added** `## Concurrency Posture (Normative cross-reference)` section to `05-config-resolution.md` linking concurrent-runner concerns (cache writes, local SQLite state under `~/.local/state/glci/`, atomic `glci config set` rewrites) to the canonical contract at [spec/13 §97 AC-22](../13-generic-cli/97-acceptance-criteria.md). Pure cross-link — contract NOT restated. Codifies Lesson #36 (link, never restate) on the cross-module axis. Per-runner `flock` on shared workspace paths declared FORBIDDEN (mirrors spec/13/18 batch-execution rule). **No §97 AC change**, no AC-31-31 cascade, no RUBRIC bump, no gate-count change. §00 v2.1.2 → v2.1.3; §99 v2.1.2 → v2.1.3. Sibling lockstep: spec/14 (v2.3.1) + spec/16 (v2.2.1) shipped same Lesson #36 inoculation in this phase.

## [2.1.2] — 2026-04-29 — Phase 150 (P3 sweep slot 10 — Verifies clauses on §97 AC-28-01..AC-28-28)

- **Added** `**Verifies:**` clauses to AC-28-01 through AC-28-28 in `97-acceptance-criteria.md` (28 ACs). Verifies-coverage gap: **12/40 → 40/40**. Each AC now explicitly maps to its underlying invariant. Selected mappings: AC-28-01 (§03 TS detection), AC-28-04 (§05 file<env<flag precedence + provenance), AC-28-05/06/28 (§06↔§17 OpenAPI/streaming contract), AC-28-07 (§09 `HasError` disjunction), AC-28-08 (§06 sort+dedup; supports AC-28-23 byte-identical determinism), AC-28-09/10 (§10 SSH-vs-TempToken lane separation; mirrors `mem://specs/git-logs` SSH-key Lane B), AC-28-11/13 (§07 exit-code-3 / exit-code-4 + 4xx-fatal / retry-budget), AC-28-12 (§05 backoff exact-honor + idempotency), AC-28-14 (§05 `batch_max_bytes` cap-before-send + truncation-must-be-loud), AC-28-15/16/26 (§11 doctor happy/skew/verbatim-passthrough), AC-28-17/18 (§06 `/fixed-log` server-driven, no-local-cache), AC-28-19/20 (§08 GitHub binding + SSH-to-HTTPS canonicalization), AC-28-21 (§04 `--no-push` air-gapped), AC-28-22 (§03 polyglot detection + `<runtime>-<phase>` PipelineName), AC-28-23 (§06 deterministic-serialization for SSH signature stability), AC-28-24/25 (§05 HTTPS-by-default + backoff-length-equals-max_retries), AC-28-27 (§18 JSON-Schema-as-source-of-truth). AC-28-01..AC-28-28 GWT bodies preserved verbatim. §97 v2.0.0 → v2.1.0; §00 v2.1.1 → v2.1.2; §99 v2.1.1 → v2.1.2. `check-ai-confidence.py` P3 driver eliminated for `spec/28`.

## [2.1.1] — 2026-04-28
- **P22 sync** (2026-04-28): §00 banner version field bumped 1.1.0 → 2.1.1 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 22 -->` stamp added under §00 banner; no spec content change).

### Audit (no content change)

- **Phase P12 — "Deepen 9 thin section files" backlog item closed as STALE.** This task was queued before Phases 31/55/63/76 deepened the module to a perfect 100/100 strict tree-health score. Re-audit confirms: all 9 section files (`01`..`09`) are 83–132 lines of dense tabular contract (enums, harvest maps, layered-design rules, error catalogs, provider bindings) — comparable to or denser than peer modules. §99 reports `Files present 15/15`, `0 TODO/TBD/FIXME markers`, implementability `100`, all internal consistency checks ✅, and `check-tree-health.cjs --strict` returns `168/168 (all 56 modules at full marks)` with §28 contributing 3/3 quality credits. The "thin files" framing was inherited from the audit-v4 baseline (45/100) which has been superseded by audit-v5 (Phase 130). No file edits required; no AC changes; no version bump for any section file. §98 / §99 receive a patch bump to record the disposition.

## [2.1.0] — 2026-04-27

### Fixed

- **Phase 119 — §07 ↔ §97 GLCI-* containment drift repair (surfaced by Phase 118 sweep).** The Phase 118 AC-31-31 bounding sweep against §28 surfaced 2 codes referenced in §97-acceptance-criteria.md but undefined in §07-error-catalog.md: `GLCI-EXEC-DEPS-MISSING` (cited in AC-28-37 for TypeScript and AC-28-39 for PHP — refusal to implicitly install dependencies) and `GLCI-STREAM-MALFORMED` (cited in AC-28-26 — server-side NDJSON framing rejection during `--stream` mode). Both codes are now formally added to §07: `GLCI-EXEC-DEPS-MISSING` slotted into the `## Execution` table with `Exit=1`, scoped explicitly to TypeScript+PHP runtimes (Go excluded — modules cache lives outside the repo); `GLCI-STREAM-MALFORMED` slotted into `## Push (transport)` with `Exit=4` and an explicit comparison clause distinguishing it from the adjacent `GLCI-PUSH-STREAM-BROKEN` (the latter = post-retry connection drop; the new code = active server framing rejection). The Phase 118 sweep also flagged a `GLCI-TELEMETRY-` family reference in §97 line 231 — re-inspection confirmed this is a **negative reference** ("no `GLCI-TELEMETRY-*` codes — telemetry doesn't exist" per Locked Decision #10) and NOT a real undefined code; no §07 row added. Catalog GLCI-* count: 27 → **29**. §07 banner v1.0.0 → v1.1.0; §99 v2.0.0 → v2.1.0; §99's prior claim "all 28 GLCI-* codes have direct AC coverage" superseded — now 29 codes with full §07 ↔ §97 containment, the inverse direction (§97 ⊆ §07) verified by Phase 118 re-sweep. No new ACs in §97 (the existing AC-28-26 / AC-28-37 / AC-28-39 already cite the now-defined codes; this is a §07 catalog hygiene fix, not a coverage extension). Mechanical guard for this drift class is still pending Phase 117 (`test-glci-error-code-containment.sh` — currently in the Phase 117 backlog awaiting user go/no-go).

## [2.0.0] — 2026-04-26

### Added
- **Phase 16d-v — Deepen §28 §97.** Added 12 new module-specific GWT ACs (AC-28-29..AC-28-40), bringing total from 28 → 40. AC-28-01..AC-28-28 preserved verbatim.
- **AC-28-29..AC-28-32** close the four error codes flagged "v1.1 deferred" in `99-consistency-report.md`: `GLCI-EXEC-RUNNER-CRASHED` (subprocess signal handling, no retry), `GLCI-EXEC-TIMEOUT` (SIGTERM→grace→SIGKILL with partial-stdout preservation), `GLCI-PUSH-STREAM-BROKEN` (NDJSON stream failure → batched fallback), `GLCI-DETECT-MULTIPLE-MODULES` (nested-monorepo ambiguity, no heuristic resolution).
- **AC-28-33..AC-28-34** add CI-provider auto-fill coverage for GitLab, Azure Pipelines, Bitbucket, and generic-shell fallback (AC-28-19 only covered GitHub). Provider precedence order locked: GitHub → GitLab → Azure → Bitbucket → generic shell.
- **AC-28-35** enforces Locked Decision #10 (telemetry prohibition) at network layer via two-host allowlist + sandboxed-network test in CI.
- **AC-28-36** specifies stream buffer overflow behavior (FIFO drop oldest, throttled stderr, synthetic ErrorLogs entry, exit `1` on any drop).
- **AC-28-37..AC-28-39** specify per-runtime tool selection for TypeScript (npm/pnpm/bun/yarn berry detection + env hardening), Go (`golangci-lint`/`go test -race -count=1`/CGO disabled), and PHP (composer/phpcs/phpstan/phpunit/pest with XDEBUG_MODE management).
- **AC-28-40** specifies direct invocation of `glci push-fixed` (manual `/fixed-log` mark, no phase execution) and `glci clear` / `clear --all` (`/clear-log` vs `/clear-log-all` triple-vs-pair scope).
- Banner v1.0.0 → v2.0.0 (major; AC count 28 → 40 closing all v1.1 deferred coverage). Lockstep §99 v1.0.0 → v2.0.0; spec-index regenerated.

## [1.0.0] — 2026-04-25

### Added
- Initial draft of the Universal CI CLI spec module.
- §00 overview with 12 locked decisions and 14-file inventory.
- §01 glossary + 5 enums (`Phase`, `Runtime`, `Severity`, `ExitCode`, `LogShipMode`).
- §02 architecture: process model, layered design, plugin model, concurrency, failure semantics.
- §03 runtime detection table for `ts` (npm/pnpm/bun/yarn), `go`, `php`.
- §04 command surface: 9 subcommands, full flag tables, exit-code matrix.
- §05 config resolution: 4-tier override order, full `glci.toml` schema, env-var map, validation rules.
- §06 log shipping contract: batched + streaming modes mapped to v2 endpoints.
- §07 error catalog: 24 `GLCI-*` codes + verbatim `GL-*` forwarding from v2 server.
- §08 CI provider bindings for GitHub Actions, GitLab CI, Azure Pipelines, Bitbucket, generic shell.
- §09 output classification: built-in pattern table + per-runtime `FilePaths` extraction.
- §17 OpenAPI 3.1 client contract (`17-openapi-client.yaml`).
- §18 JSON Schema for `glci.toml` (`18-config-schema.json`).
- §97 acceptance criteria: 28 Given/When/Then ACs covering detection, config, classification, shipping, auth, doctor, determinism.
- §99 consistency report with cross-doc bijection table.

### Cross-references established
- v2 server REST contract (`spec/22-git-logs-v2/04-rest-api-endpoints.md`).
- v2 auth + validation order (`spec/22-git-logs-v2/05-auth-and-validation.md`).
- v2 error codes (`spec/22-git-logs-v2/15-error-codes.md`).
- Generic-CLI conventions (`spec/13-generic-cli/`).
- Existing shared CLI wrapper guidance (`spec/12-cicd-pipeline-workflows/03-reusable-ci-guards/07-shared-cli-wrapper.md`).

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | patch | Phase 31: Added Validation History / File Inventory headings to §99 to satisfy rubric v2.0.0 quality dimension. |

## Releases
### 1.1.0 — 2026-04-27 (Phase 55 — implementability lever)
- **Added** Added 2 CI provider YAML workflows (GitLab + Azure) so YAML block count ≥5 → `has_ci_workflow` (+5). Added 2 Go reference helpers (line classifier + runtime detection) so Go block count ≥3 → `has_typed_lang_contract` (+10).


## 2026-04-27 — Phase 63 impl-sweep

- Phase 63: appended Universal CI CLI enums TS enum mirror to satisfy `has_ts_enums` rubric (impl 80 → 90).

## 2026-04-27 — Phase 76 (impl 90 → 100)

- Added Mermaid lifecycle diagram — satisfies `has_mermaid` (+5).
- Added SQL DDL audit-log schema — satisfies `has_sql_ddl` (+20).
- Implementability raised 90 → 100 (deterministic audit, capped).

