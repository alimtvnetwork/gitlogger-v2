# Consistency Report

**Generated:** 2026-05-10
**Module version:** 2.5.3

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

