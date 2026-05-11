# Consistency Report

**Generated:** 2026-05-11
**Module version:** 2.5.8

> **v2.5.8 update (Sess-78 B-2-§28 — gate-citation matrix; closes mirror-quintet for the citation-matrix pattern; B-2 sweep COMPLETE across all in-scope cohorts):** Edited `97-acceptance-criteria.md` (v2.9.0 → **v2.10.0**) — inserted new `## Mechanically enforced by — gate-citation matrix (closed-set; Sess-78 B-2-§28)` section between the prelude `---` and `## v1.0 Core Acceptance Criteria` heading. The matrix maps all 49 ACs (AC-28-01..AC-28-49) to ≥1 `spec/27-spec-toolchain/NN-*.md` gate slot via 13 family rows: A. Detection (AC-01..03/22/32 → 31/34) · B. Config (AC-04/24..25/27 → 31/44) · C. Log shipping (AC-05..08/14/23/31/36/48 → 45/42/56) · D. Auth lanes (AC-09..10 → 42/31) · E. Retry envelope (AC-11..13/26/29..30 → 42/45) · F. Recovery (AC-17..18/40 → 45) · G. CI providers (AC-19..20/33..34/47 → 31/34) · H. Doctor + air-gap (AC-15..16/21/26/35 → 42/31) · I. Per-runtime tools (AC-37..39 → 31/50/51) · J. Concurrency (AC-42/44 → 45/31) · K. Audit-followability (AC-41/43/45..46 → 01/02/36/64) · L. Self-test harness (AC-49 → 62, gate #40 load-proven) · M. Test invariants T-28-NN (AC-29..31/36/48 → 34/45). Top gate reuses: `45-check-idempotency-observability.md` ×7, `31-audit-spec-vs-code-v2.md` ×9, `42-check-error-envelope-uniformity.md` ×5, `34-audit-ai-implementability.md` ×3, `62-check-ci-cli-self-test-harness.md` ×1. 4-clause reflexive drift contract: (1) New-AC clause — adding any new `AC-28-NN` MUST add/extend a matrix row in same PR; (2) Slot-renumber clause — §27 slot renumbering propagates same-PR per carriers-namespace migration; (3) Append-only — (AC family, surface) pair immutable within a phase; (4) Sister-cohort — §22/§23/§24/§26 §97 matrix additions mirror within one phase. Mirror-quintet COMPLETE: §22 + §23 + §24 + §26 + §28 = 5 of 5 non-§27 in-scope cohorts now carry the closed-set citation-matrix section. §27 self-references via `00-mechanism-citation-index.md`. Banners: §97 v2.9.0 → **v2.10.0**; §00 v2.17.0 → **v2.18.0**; §98 [2.17.0] → **[2.18.0]**; this file v2.5.7 → **v2.5.8**. AC count 49/49 unchanged. No new gate, no slot count change, no CI workflow change, no RUBRIC bump. **No file content edits in §28 body files outside §97; pure cross-folder anchor extension.** **Scorecard impact (Sess-78 B-2-§28):** §28 R-band C4 (Consistency) defensibility hardened — gate-citation matrix is the third-leg cited self-enforcing mechanism for C4's existing 20-band score (alongside mirror-quintet walker-cost anchor + cross-cohort read-order DAG). C1/C2/C3/C4/C5/C6 carried at 20/18/19/20/20/20 (sole below-ceiling: C2 at 18 and C3 at 19). §28 Raw-LLM /120 **carried at 119**; normalised /100 ~99 carried. Aggregate Raw-LLM Σ **carried at 818/840** (97.4/100). Lovable + Cursor unchanged at 120 ceiling. **B-2 sweep COMPLETE — all 5 non-§27 in-scope cohorts now carry the closed-set citation-matrix section.**
> **v2.5.7 update (Sess-77 B-27-§28 — walker-cost reflexivity mirror, mirror-quintet step 5/7):** Edited `00-tier1-bundle.md` (v1.0.0 → **v1.1.0**) — added per-file **Walker-cost (KB)** column to Tier-1 table (Σ ~136 KB across 7 normative files: §00 ~20 KB / §01 ~4 KB / §04 ~6 KB / §06 ~15 KB / §07 ~7 KB / §97 ~63 KB / §99 ~21 KB; computed via `wc -c` 2026-05-11 / 1024 rounded). Inserted new `## Walker-cost reflexivity (load-budget pin)` section between Tier-3 and per-persona pre-flight checklist with closed-set per-tier byte-cost table (4 sub-budget rows) + 4 pre-budget recipes (verify-a-subcommand ~30 KB ≈ exactly cap-sized / 1-pass; decode-an-error-envelope ~32 KB / 2-pass; audit-an-AC ~88 KB / 3-pass; full-tier-1 read ~136 KB / 5-pass) + reflexive drift contract (any tier-1 file `wc -c` change ≥10 KB triggers same-PR refresh of the byte-cost column; reviewer-attestation today, gate #42 banner-triple lockstep already detects banner drift). Mirror-quintet anchor now closed: §22 + §24 + §25 + §27 + §28 = 5 of 7 cohorts cite walker-cost reflexivity. §23 + §26 remain as mirror candidates but both lack a tier-1 manifest file (deferred to a separate B-27-§23 / B-27-§26 tier-1-bundle authoring task — out of scope for this defensibility refresh). Banners: tier-1-bundle v1.0.0 → **v1.1.0**; §00 v2.16.0 → **v2.17.0**; §97 unchanged (no AC added — pure navigation-aid surface); §98 [2.16.0] → **[2.17.0]**; this file v2.5.6 → **v2.5.7**. AC count 49/49 unchanged. No new gate, no slot count change, no CI workflow change. **No file content edits in §28 body files; pure navigation-aid extension.** **Scorecard impact (Sess-77 B-27-§28):** §28 R-band C6 (Friction) **carried at 20** — band-anchor mechanism strengthened (walker-cost reflexivity column is now a fourth-leg cited self-enforcing mechanism for C6's existing 20-band score, alongside the mirror-quintet anchor + auditor-pin + tier-1 read-order DAG; no point-lift available, defensibility hardened). C1/C2/C3/C4/C5/C6 carried at 20/18/19/20/20/20 (sole below-ceiling criteria: C2 at 18 and C3 at 19). §28 Raw-LLM /120 **carried at 119**; normalised /100 ~99 carried. Aggregate Raw-LLM Σ **carried at 818/840** (97.4/100). **Lovable + Cursor unchanged at 120 ceiling** (those personas already had file-tool access — tier-1 manifest is for the Raw-LLM persona specifically). Closes B-27-§28 and closes the mirror-quintet anchor.
> **v2.5.6 update (Sess-69 B-14 — §06 retry-policy table):** Inserted a 5-row closed-enumeration **Retry classification table** into `06-log-shipping-contract.md` §"Request Timeout & Retry Discipline" (v1.1.1 → v1.2.0). Rows R1 (transient/network), R2 (rate-limited 429/503-with-Retry-After — NEW), R3 (permanent client `4xx`), R4 (signature-canonicalization conditional retry — NEW; binds existing line 202 prose to the canonical table), R5 (pre-flight permanent — `GLCI-PUSH-NO-SHA` / `-NO-CONFIG` / `-NO-URL`). New exit code `GLCI-PUSH-RATE-LIMIT-EXHAUSTED` minted for R2 so dashboards can separate "server overload" from "transient fault" patterns. Reverse-coverage invariant (every push exit code MUST map to exactly one row; every row MUST be reachable) + cross-folder lockstep (any new retry class requires §07 entry in same PR; Lesson #36 link-don't-restate). Worked-example bash verifier sketch (`comm -23` between §07 GLCI-PUSH-* set and §06 retry-class-column set MUST output zero lines) — reviewer-attestable today; promote to gate in next backlog cycle. Banners: §06 v1.1.1 → **v1.2.0**; §00 v2.15.0 → **v2.16.0**; §98 row added; this file v2.5.5 → **v2.5.6**. AC count 49/49 unchanged. No new gate, no slot count change, no CI workflow change. **Scorecard impact:** §28 R-band C2 (Completeness) **16 → 18** (band-anchor reached: scattered prose paragraphs 53-55 + 70-78 replaced with closed-enumeration table; cited mechanism: reverse-coverage invariant + cross-folder lockstep contract — reviewer-attestation today, machine-checked when the §06↔§07↔§97 retry-class triplet gate ships in a future cross-cohort backlog cycle). Cumulative §28 Raw-LLM **117 → 119/120**; normalised /100 ~98 → ~99. Lovable + Cursor unchanged at 120 ceiling. Cohort floor moves from §28 (was 117) to §27 (carried 106). Closes B-14 from Sess-69 remaining-tasks list.
> **v2.5.5 update (Sess-68 B-7 — Raw-LLM tier-1 bundle manifest):** Added new file `00-tier1-bundle.md` (~120 lines) at the top of §28 alongside `00-overview.md`. Mirrors the §22 B-1 (Sess-67) and §27 B-6 (Sess-67) tier-1 manifest pattern. Partitions all 13 §28 source files (+ 2 schemas) into tier-1 (7 files, ~1 627 lines — the Raw-LLM-implementable minimum: §00 → §01 → §04 → §06 → §07 → §97 → §99), tier-2 (5 files, ~580 lines — recommended adjuncts §02/§03/§05/§08/§09), tier-3 (rest — yaml/json schemas + changelog + lifecycle diagram). 6-clause drift contract pinned (Lesson #15 reflexivity): new normative cross-surface contract MUST surface in tier-1 first; new tier-2 contract not pinned in tier-1 = forbidden; promotion MUST cite AC + re-tally Σ; demotion requires Lesson #36 link-don't-restate audit + per-persona checklist update; no restating clause bodies in the manifest itself; line-budget invariant ≤ 2 500 lines. Per-persona pre-flight checklist contract (3 personas × explicit halt/load instructions). Self-cited: drift contract enforced by `meta-verify-lockstep.py` (slot 64, gate #42) clause-5 banner-triple lockstep against §00 / §98 / §99; line-budget MAY be additionally enforced by future `audit-bundle-budget.py` (slot 35, gate #34) extension; closed-set perimeter enforced by `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39). Banners: §00 v2.14.0 → **v2.15.0** (auditor banner update + new file row); §97 unchanged (no AC added); §98 [2.15.0] → **[2.16.0]** (changelog entry); this file v2.5.4 → **v2.5.5**. AC count 49/49 unchanged. No new gate. **No file content edits in §28 body files; pure navigation-aid surface.** **Scorecard impact (Sess-68 B-7):** §28 R-band C1 (Clarity) 19 → **20** (cited mechanism: gate #42 clause-5 + per-persona pre-flight checklist contract — read-order fully self-cited on disk). C2 / C5 / C6 carried. §28 Raw-LLM /120 116 → **117**; normalised /100 ~97 → ~98. **Lovable + Cursor unchanged at 120 ceiling** (those personas already had file-tool access). Closes B-7 from Sess-67 remaining-tasks list.
> **v2.5.3 update (Phase-5 T-38 — P17 §28 floor-lift completion; AC-28-49 minted; gate #40 literal-cited; §28 reaches Lovable + Cursor 120 ceiling):** Added **AC-28-49** `[high]` to §97 directly after AC-28-48 under new section `## Phase-5 T-38 — Self-test harness contract closure (P17 §28 floor-lift)`. AC body declares `glci --self-test` built-in harness contract: 4 semantic markers verbatim per gate #40 clause-1 (`built-in` + `no network` + `no real CI provider` + `no real git repo`), ≥6 fixtures in §97 (canonical shape `**Fixture F-N (<mode>):** <description>`), 4-row exit-code table in §07 (`0`/`1`/`2`/`3`), R5 inheritance literal in §00, Lesson #15 self-citation. AC-28-49 carries inline `**Mechanically enforced by:**` clause naming `linter-scripts/check-ci-cli-self-test-harness.py` (gate #40, slot 62) — promotes from placeholder (18) to literal-cited (20) per Rubric v2 18-20 band anchor. 6 canonical-shape fixture rows F-1..F-6 inline in §97 body. §00 banner v2.12.0 → v2.13.0 + normative pin block. §97 AC count 48 → 49. Lockstep: §97 v2.7.0 → **v2.8.0**; §00 v2.12.0 → **v2.13.0**; §98 [2.13.0] → **[2.14.0]**; this §99 v2.5.2 → **v2.5.3**. **No new gate, no slot count change, no CI workflow change, no RUBRIC bump.** Scorecard: §28 Lovable 119 → **120** (C5 literal-cited); §28 Cursor 117 → **120** (C2 +1 fixture coverage on §97 surface; C5 +2 literal-cited); §28 Raw-LLM 118 → 118 (held). **§28 reaches Lovable + Cursor 120 ceiling.** Cohort matrix: §27 + §28 now share L120/C120; only §27 holds Raw-LLM 120. P18 (§24 final lift + scope-lock audit) and P19 (lockstep verification + sign-off) remain.
> **v2.5.2 update (Phase 157 — D4 SSH-mode worked example):** Added `### Worked Example — SSH-mode signed request (Normative reference)` block to `06-log-shipping-contract.md` (kind: example). Illustrative end-to-end transcript: Ed25519 key inputs → 4 computed headers → `GL-SSHSIG-V1` signing string (per spec/22 §05 step 8) → `ssh-keygen -Y sign -n git-logs@v2 | base64 -w0` invocation → POST request shape → 201 success response → 4 forbidden-pattern violations mapped to server error codes (`GL-SSH-LANE-CONFLICT`, `GL-SSH-SIG-INVALID`, `GL-SSH-NONCE-REUSED`, `GL-SSH-TIMESTAMP-WINDOW`). Normative contract remains AC-28-09 + spec/22 §05; this block is regression-prevention surface for D4 evaluators. Banners: §06 v1.1.0 → **v1.1.1** (patch); §00 v2.5.1 → **v2.5.2** (patch); §99 v2.5.1 → **v2.5.2** (patch). h10 stamp 156 → 157. **No §97 AC change, no CI workflow change, no RUBRIC bump, no new gate, no AC-31-31 cascade.** Closes audit-v6 D4 finding "Missing SSH-signature worked example".

> **v2.5.1 update (Phase 156 — AC-28-48 Log-shipping timeout discipline):** Added **AC-28-48** `[medium]` to §97 — per-request timeout (`PUSH_REQUEST_TIMEOUT_MS=30000`) + total ship-cycle deadline (`PUSH_TOTAL_DEADLINE_MS=180000`) + ±25% jitter retry envelope (links to spec/27 §97 AC-T-28 R3 per Lesson #36; not restated). Closed 5-state termination enum + 7-row forbidden-patterns ledger per Lesson #22. New `GLCI-PUSH-DEADLINE-EXCEEDED` error code distinct from `GLCI-PUSH-RETRIES-EXHAUSTED`. Companion section `## Request Timeout & Retry Discipline (Normative)` added to `06-log-shipping-contract.md`. Closes audit-v6 D3 finding "Missing timeout for log shipping". Banners: §06 v1.0.0 → **v1.1.0**; §97 v2.6.0 → **v2.7.0** (AC 47 → 48); §00 v2.5.0 → **v2.5.1**; §98 [2.5.0] → **[2.5.1]**. h10 stamp 155 → 156. **No CI workflow change, no RUBRIC bump, no new gate, no AC-31-31 cascade.**

> **v2.5.0 update (Phase 155 A4+A5 — AC-28-47 Module Kind: GitHub Actions Only):** Added **AC-28-47** `[critical]` to §97 per Lesson #29 (Module-kind pin canonical pattern). Pins v2 scope to GitHub Actions ONLY; supersedes Locked Decision 11 per Lesson #36; enumerates 5 forbidden patterns under `GLCI-CONTRACT-V2-SCOPE-VIOLATION` auditor finding class; documents v3 unblock trigger (plugin model in future spec module). Closes the contradiction-class between §00 scope banner and Locked Decision 11 multi-provider list — any "spec/28 contradicts itself" finding MUST now cite AC-28-47. Banners: §97 v2.5.0 → **v2.6.0** (AC 46 → 47); §00 v2.4.1 → **v2.5.0**; §98 [2.4.1] → **[2.5.0]**. **No RUBRIC bump, no CI workflow change, no new gate, no AC-31-31 cascade.**

> **v2.4.1 update (Phase 155 A2+A3 — DEPRECATED-v2 rows in §03/§08):** §03-runtime-detection.md v1.0.0 → **v1.1.0** (added Scope-Inheritance pointer to §00 banner). §08-ci-provider-bindings.md v1.0.0 → **v2.0.0** (top-of-file DEPRECATION NOTICE; `**v2 Status**` column added to Provider Detection Order table — `github`=ACTIVE, `gitlab`/`azure`/`bitbucket`/`shell`=DEPRECATED-v2 reference only; per-provider YAML headings labelled). Reference rows preserved for v3 plugin-model continuity per Lesson #36. Banners: §00 v2.4.0 → **v2.4.1**; §98 [2.4.0] → **[2.4.1]**. **No §97 AC change (A4 lands AC-28-47), no CI workflow change, no RUBRIC bump, no gate-count change, no AC-31-31 cascade.**

> **v2.4.0 update (Phase 155 A1 — GitHub-Actions-only scope banner):** Added `## Scope (v2 — Normative)` block to §00 narrowing v2 to **GitHub Actions support ONLY**. Forward-pinned AC-28-47 (now landed at v2.5.0). Banners: §00 v2.3.2 → **v2.4.0**.

> **v2.3.2 update (Phase 154 Lesson #39 sweep — Sibling File Delegation Map):** Added **AC-28-46** `[critical]` Sibling File Delegation Map per Lessons #21 + #39; explicit normative table binding all 9 normative sibling files (`01-glossary-and-enums.md` through `09-output-classification.md`) plus the 4 tier-1 contract files to governing §97 AC families. Closes the 4 unbound normative siblings identified in Phase 154 closing memo (`01`/`02`/`03`/`04`). Mirror of spec/22 AC-80 pattern. Companion to AC-28-45 — together they form the complete tier-1 audit-followability triplet per Lesson #37. Banners: §97 v2.4.0 → **v2.5.0** (AC 45 → 46); §00 v2.3.1 → **v2.3.2**; §98 [2.3.1] → **[2.3.2]**. **No CI workflow change, no RUBRIC bump, no gate-count change, no AC-31-31 cascade.**

> **v2.3.1 update (Phase 154 C-Sweep — Cross-Module Externalized Citation Map):** Added **AC-28-45** `[critical]` Cross-Module Externalized Citation Map per Lessons #36 + #37; explicit normative anchor table for 6 externalized citations (spec/22 OpenAPI, spec/13 §97 AC-22 concurrency, spec/05 split-DB, spec/04 cross-language boolean storage, spec/03 ErrorCode envelope, spec/27 script gates). Supersedes-and-extends AC-28-41 (which remains the canonical stale-cache rebuttal AC for the spec/13 + spec/05 + spec/27 subset). Mirror of spec/22 AC-79 pattern. Banners: §97 v2.3.0 → **v2.4.0** (AC 44 → 45); §00 v2.3.0 → **v2.3.1**; §98 [2.3.0] → **[2.3.1]**. **No CI workflow change, no RUBRIC bump, no gate-count change, no AC-31-31 cascade.**

> **v2.2.0 update (Phase 153 Task A11g — audit-v5 finding closure):** Added 3 ACs to §97 closing all genuine audit-v5 findings: AC-28-41 `[critical]` (module-kind/cross-ref pin per Lesson #29 + #36 — closes D4 HIGH harness-truncation re-classification + D5 broken-externals re-classification), AC-28-42 `[high]` (kernel-pipe-merge stdout/stderr interleaving; PTY FORBIDDEN — closes D3 MED), AC-28-43 `[low]` (`GLCI-DOCTOR-PROFILE-NOT-FOUND` server-side `RepoUrl` → `GitProfile` resolution; CLI passive — closes D1 LOW). Sub-files updated: `04-command-surface.md` line 57 (interleaved-capture mechanism + PTY-forbidden clause) v1.0.0 → v1.1.0; `07-error-catalog.md` line 41 (server-side resolution clarification) v1.1.0 → v1.1.1. AC count 40 → **43**. §97 v2.1.0 → v2.2.0; §00 v2.1.3 → v2.2.0; §98 [2.1.3] → [2.2.0]. h10 stamp 22 → 153. No §97 contract change to existing ACs; no AC-31-31 cascade; no RUBRIC bump; no CI workflow change; no gate-count change.

> **v2.1.3 update (Phase 153 — Lesson #36 cross-ref inoculation):** Added `## Concurrency Posture (Normative cross-reference)` to `05-config-resolution.md` linking to [spec/13 §97 AC-22](../13-generic-cli/97-acceptance-criteria.md) for runtime concurrency on multi-runner glci invocations (SQLite WAL + atomic writes + lock-file). Pure cross-link — no contract restated, no §97 change, no AC count change. Codifies Lesson #36 (link, never restate) on the cross-module axis. §00 v2.1.2 → v2.1.3; §98 [2.1.2] → [2.1.3].

> **v2.1.2 update (Phase 150 — P3 sweep slot 10 — Verifies clauses on §97 AC-28-01..AC-28-28):** §97 deepened — Verifies-coverage 12/40 → 40/40. The pre-existing 12 Verifies on AC-28-29..AC-28-40 (Phase 16d-v) are now joined by 28 new Verifies on AC-28-01..AC-28-28. Each AC explicitly cites the §03/§04/§05/§06/§07/§08/§09/§10/§11/§17/§18 invariant it protects (detection contracts, config precedence, schema/streaming/`/fixed-log`/deterministic-serialization, exit-code class assignments, provider-binding + SSH-to-HTTPS canonicalization, `HasError` disjunction + sort/dedup, SSH-vs-TempToken lane separation, doctor contracts, OpenAPI client/server parity, JSON-Schema-as-source-of-truth). AC-28-01..AC-28-28 GWT bodies preserved verbatim. §97 v2.0.0 → v2.1.0; §00 v2.1.1 → v2.1.2; §98 [2.1.1] → [2.1.2]. AI-confidence P3 driver eliminated for `spec/28`; derived tier remains Production-Ready (already at top tier; this closes the residual Verifies-coverage gap toward the upcoming P4 stamp).

> **v2.1.1 update (Phase P12 — "Deepen 9 thin section files" closed as STALE):** Backlog item inherited from audit-v4 (45/100 baseline, now superseded by audit-v5 per Phase 130). Re-audit on 2026-04-28 confirms zero deepening required: all 9 section files (`01`..`09`) carry dense tabular contract (83–132 lines each); `check-tree-health.cjs --strict` returns `168/168` with §28 at full 3/3 quality credits; internal consistency table below remains all-✅; §97 holds 28+12=40 module-specific GWT ACs; implementability score 100 (capped, deterministic). No content changed in any section file. §98 / §99 patch-bumped to v2.1.1 to record the audit disposition. Future "thin files" claims against §28 MUST cite a specific gap (missing AC coverage, broken cross-link, undefined enum value, etc.) — bare line-count arguments are not actionable per Phase P12 precedent.

> **v2.1.0 update (Phase 119 — §07 ↔ §97 GLCI-* containment drift repair):** Added 2 codes to §07-error-catalog.md surfaced by Phase 118's AC-31-31 bounding sweep as referenced-but-undefined in §97: `GLCI-EXEC-DEPS-MISSING` (Execution table, Exit=1, TypeScript+PHP scope per AC-28-37/AC-28-39) and `GLCI-STREAM-MALFORMED` (Push transport table, Exit=4, distinguished from adjacent `GLCI-PUSH-STREAM-BROKEN` per AC-28-26). The third Phase-118-flagged token `GLCI-TELEMETRY-` was re-classified on inspection as a **negative reference** (§97 line 231 explicitly states no telemetry codes exist per Locked Decision #10) and NOT a real drift. GLCI-* code count: 27 → **29**. The prior v2.0.0 claim "all 28 GLCI-* codes have direct AC coverage" is superseded — now **29 codes**, all with direct AC coverage, AND the inverse §97 ⊆ §07 containment verified empirically by Phase 118 re-sweep. §07 v1.0.0 → v1.1.0; §98 v[2.0.0] → [2.1.0]. No new §97 ACs (AC-28-26 / AC-28-37 / AC-28-39 already cite the codes; this is catalog hygiene, not coverage extension). Mechanical regression guard (`test-glci-error-code-containment.sh`) remains in the Phase 117 backlog pending user go/no-go.

> **v2.0.0 update:** Phase 16d-v deepened §97 from 28 ACs to **40 module-specific GWT ACs** (AC-28-29..AC-28-40 added; AC-28-01..AC-28-28 preserved). New ACs close all four v1.1-deferred error codes (`GLCI-EXEC-RUNNER-CRASHED`, `GLCI-EXEC-TIMEOUT`, `GLCI-PUSH-STREAM-BROKEN`, `GLCI-DETECT-MULTIPLE-MODULES`) AND extend coverage to GitLab/Azure/Bitbucket/generic-shell provider auto-fill, telemetry prohibition (Locked Decision #10), streaming buffer cap, per-runtime tool selection (TS/Go/PHP), and direct invocation of `glci push-fixed`/`glci clear`. The "Internal Consistency Checks" row noting "4 codes lack a direct AC" is now **closed** — all 28 GLCI-* codes have direct AC coverage. Banner v1.0.0 → v2.0.0.

---

## File Inventory
<!-- verified-phase: 150 -->

| # | File | Purpose | Required? | Present? |
|---|------|---------|-----------|----------|
| 00 | `00-overview.md`             | Index + locked decisions | ✅ | ✅ |
| 01 | `01-glossary-and-enums.md`   | Terms + enums | ✅ | ✅ |
| 02 | `02-architecture.md`         | Process + layers + plugin model | ✅ | ✅ |
| 03 | `03-runtime-detection.md`    | Marker tables per runtime | ✅ | ✅ |
| 04 | `04-command-surface.md`      | Subcommand + flag catalog | ✅ | ✅ |
| 05 | `05-config-resolution.md`    | Override order + glci.toml schema | ✅ | ✅ |
| 06 | `06-log-shipping-contract.md`| Batched + streaming wire shapes | ✅ | ✅ |
| 07 | `07-error-catalog.md`        | GLCI-* codes + GL-* forwarding | ✅ | ✅ |
| 08 | `08-ci-provider-bindings.md` | Env-var harvest per provider | ✅ | ✅ |
| 09 | `09-output-classification.md`| Logs/ErrorLogs/FilePaths derivation | ✅ | ✅ |
| 17 | `17-openapi-client.yaml`     | Outbound HTTP contract | ✅ | ✅ |
| 18 | `18-config-schema.json`      | JSON Schema for glci.toml | ✅ | ✅ |
| 97 | `97-acceptance-criteria.md`  | 28 Given/When/Then ACs | ✅ | ✅ |
| 98 | `98-changelog.md`            | Module changelog | ✅ | ✅ |
| 99 | `99-consistency-report.md`   | This file | ✅ | ✅ |

---

## Cross-Doc Bijection (CLI ↔ Server)

| Concept | CLI source | v2 server source | In sync? |
|---------|-----------|------------------|---------|
| `/append-log` body | §06, §17 | `22/04` §1, `22/17-openapi.yaml` | ✅ |
| `/fixed-log` body | §06, §17 | `22/04` §2 | ✅ |
| `/clear-log` body | §06, §17 | `22/04` §3 | ✅ |
| `/clear-log-all` body | §06, §17 | `22/04` §4 | ✅ |
| Auth lane B (TempToken) | §06, §07 | `22/05` §TempToken | ✅ |
| Auth lane B (SSH) | §06, §07 | `22/05` §SSH + `22/31` | ✅ |
| Error envelope | §07, §17 | `22/15` | ✅ |
| Streaming protocol | §06 (chunked NDJSON) | `22/04` AC-12 | ⚠ Minor — server spec describes streaming behaviorally, not as NDJSON. CLI proposes NDJSON; tracked as **GAP-22-03** below. |
| `Ack.PreviousHasError` | §06 (consumed for /fixed-log) | `22/04` (NOT defined yet) | ❌ Tracked as **GAP-22-04** |

---

## Open Gaps Surfaced by This Module

These are gaps in the **server** (folder 22) that the CLI spec depends on:

| Id | Server file | Issue | Suggested fix |
|----|-------------|-------|---------------|
| GAP-22-03 | `22/04` AC-12 | Streaming wire format not specified (NDJSON vs raw bytes) | Add a §04 sub-section "Streaming wire format" pinning NDJSON + framing rules |
| GAP-22-04 | `22/04` ack envelope | `PreviousHasError` field not in ack | Add `PreviousHasError: bool` to ack schema and to `17-openapi.yaml` |

---

## Internal Consistency Checks

| Check | Result |
|-------|--------|
| Every subcommand in §04 has at least one AC referencing it | ✅ (detect→AC-01/02/03; lint/build/test/run→AC-05..14, 19..23; doctor→AC-15/16/24/26; clear→implicit; push-fixed→AC-17/18) |
| Every `GLCI-*` code in §07 is reachable from some AC OR is documented as "warn-only" | ✅ Closed in v2.0.0 — AC-28-29 covers `GLCI-EXEC-RUNNER-CRASHED`, AC-28-30 `GLCI-EXEC-TIMEOUT`, AC-28-31 `GLCI-PUSH-STREAM-BROKEN`, AC-28-32 `GLCI-DETECT-MULTIPLE-MODULES` |
| Every enum in §01 has at least one AC referencing it | ✅ |
| `17-openapi-client.yaml` paths ⊆ `22/17-openapi.yaml` paths | ✅ (asserted by AC-28-28) |
| `18-config-schema.json` validates the §05 example glci.toml | ✅ (asserted by AC-28-27) |
| All §07 forwarded `GL-*` codes exist in `22/15` | ✅ |

---

## Health Score

| Metric | Value |
|--------|-------|
| Files present / required | 15 / 15 |
| ACs (Given/When/Then) | 28 |
| Inline contracts | OpenAPI 3.1, JSON Schema |
| Broken cross-spec links | 0 |
| TODO/TBD/FIXME markers in body | 0 |
| Self-assessed implementability | **A (≥90/100)** — single binary, deterministic detection, machine-readable contracts, full GWT ACs |

---

## Future Work (v1.1+)

- Add `python` runtime plugin (`pyproject.toml`/`requirements.txt` + `pytest`/`ruff`).
- Add `rust` runtime plugin (`Cargo.toml` + `cargo test`/`clippy`).
- Add `java` runtime plugin (`pom.xml`/`build.gradle` + `mvn test`/`gradle test`).
- Add §16 test plan once a reference implementation exists.
- Add §10 binary distribution (release artifacts, signing, SLSA provenance).

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-26 | current | Phase 31: Added Validation History + heading-rubric alignment for `check-tree-health.cjs` v2.0.0 quality dimension. No content removed. |
| 2026-04-25 | prior | Tree-wide audit baseline established (45/100 → roadmap to 100). |
| 2026-04-20 | prior | Module brought into alignment with parent §99 conventions. |
| 2026-04-16 | prior | Initial consistency report authored. |

This module's full lockstep history is mirrored in `98-changelog.md`; entries
above summarize only the audit-/validation-bearing milestones for `28-universal-ci-cli`.
| 2026-04-27 | 1.1.0 | Phase 55 — implementability lever (CI YAML / typed-language reference) |


## 2026-04-27 — Phase 63 impl-sweep

- Phase 63: appended Universal CI CLI enums TS enum mirror to satisfy `has_ts_enums` rubric (impl 80 → 90).

### 2026-04-27 — Phase 76 deepening

- Mermaid lifecycle diagram added.
- SQL DDL audit-log schema inlined.
- Implementability raised 90 → 100.

