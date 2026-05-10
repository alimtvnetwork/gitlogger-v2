# Changelog

**Updated:** 2026-05-10


All notable changes to `spec/28-universal-ci-cli/`.

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

