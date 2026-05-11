---
kind: future-spec
todo_audit_exempt: true
description: Authoritative spec for the Git Logs WordPress plugin (SQLite-backed). The actual PHP plugin code lives in a downstream WordPress-plugin repo, not in this spec-only repo. Exempt from drift findings that flag missing PHP / SQL / REST endpoint files. TODO markers in body files are historical-resolution narrative inside `37-blind-ai-gap-analysis.md` (Phase 39b) — quoted, not actionable.
content_axis: normative-contract
axis_rationale: "Git Logs WordPress plugin enforceable spec"
---

# Git Logs v2 — Spec Overview

**Version:** 3.27.0  
**Updated:** 2026-05-11 (Sess-76 B-27-§22 — banner-triple lockstep with `00-tier1-bundle.md` v1.0.0 → **v1.1.0** (mirror of §27 B-27, §25 B-27-§25, §24 B-27-§24 walker-cost reflexivity lever applied to §22): added per-file **walker-cost (KB)** column to Tier-1 table (Σ ~119 KB across 9 normative tier-1 files) + new **§ "Walker-cost reflexivity (load-budget pin)"** section with closed-set per-tier byte-cost table + 4 pre-budget recipes (verify-an-endpoint ~57 KB / trace-a-reject-code ~40 KB / audit-permission-matrix ~40 KB / full-tier-1 read ~119 KB). Pure navigation-aid extension; no AC body edits, no new gate. **Scorecard impact**: §22 R-band C6 (Friction) **carried at 20** (defensibility refresh — fourth-leg cited mechanism added alongside mirror-quartet / auditor-pin / tier-1 read-order DAG); §22 Raw-LLM /120 **carried at 119**; aggregate Raw-LLM Σ **carried at 818/840**. Mirror-count: 4 of 7 cohorts now cite walker-cost reflexivity (§22 + §24 + §25 + §27); §23 + §26 + §28 remain mirror candidates. Closes B-27-§22. Prior banner — **Version:** 3.26.0; **Updated:** 2026-05-11 (Sess-69 B-15 — extracted Raw-LLM Auditor Pin + Walker-Pin §97-tail surfacing table + Walker-Cap Finding Disposition into new `00-auditor-notes.md` per Lesson #36 link-don't-restate (intra-module variant). §00 now points there in one row, slimming this overview from 275 → ~205 lines and freeing single-file walker tier-1 budget. Zero normative content removed — every clause remains in force on disk via §27 gates #20 / #39 / #42 cited from `00-auditor-notes.md`. Prior: Sess-68 B-11 — added `00-citation-density-audit.md`.)

> 🤖 **Auditor pre-read — open `00-auditor-notes.md` BEFORE filing any §22 finding.** That file is the canonical surface for: (1) `mem://constraints/spec-scope` + `mem://preferences/scorecard-ritual` resolution; (2) cross-cohort gate map (#20/#39/#40/#41/#42); (3) §97-tail surfacing table for AC-78 / AC-22-LV1 / AC-26 (walker-cap classification); (4) Walker-Cap Finding Disposition (D5/D4/D3 closed dispositions with on-disk evidence triple). Citation-density resolution lives in `00-citation-density-audit.md` §3 (closed-set back-fill rule, 5 covering surfaces S1–S5). Both files are self-cited on disk via `meta-verify-lockstep.py` (slot 64, gate #42) clause-5 and `check-spec22-inventory.py` (slot 37, gate #20).

---

## AI Quick-Nav Map (Lesson #88 — sprawl navigation aid)

> 60 files / ~1 MB. Grouped by theme so a context-bounded agent (Lovable / Cursor / Raw-LLM) can locate the right entry file in one glance without loading the full bundle. Pure index — no normative content; canonical contracts remain in §97 and the cited files.

| Theme | Entry files | Purpose |
|---|---|---|
| **Schema & data model** | `01-glossary-and-enums.md`, `02-database-schema.md`, `16-seed-data.md`, `18-schema.sql`, `51-ac-enum-catalog-detail.md` | Tables, enums, seed rows, canonical DDL |
| **REST surface** | `04-rest-api-endpoints.md`, `14-endpoint-examples.md`, `15-error-codes.md`, `17-openapi.yaml`, `57-ac-section-d-endpoints-detail.md` | HTTP endpoints, payloads, error codes |
| **Plugin runtime (PHP)** | `03-admin-ui.md`, `05-auth-and-validation.md`, `06-migrations-and-logger.md`, `07-app-entity.md`, `08-history-and-action.md`, `19-permission-matrix.md`, `20-observability.md`, `59-ac-section-e-logger-detail.md` | WordPress admin UI, auth, logger, permissions |
| **Operations** | `22-retention-and-pruning.md`, `23-backup-restore.md`, `24-multisite.md`, `29-uninstall-policy.md`, `58-ac-section-e-multisite-detail.md` | Lifecycle, multisite, retention |
| **Security** | `25-headless-auth-notes.md`, `30-threat-model.md`, `31-ssh-key-auth.md` | Threat model, SSH keys, headless auth |
| **CLI client** | `40-cli-overview.md`, `41-cli-pointer-file-schema.md`, `42-cli-classifier-rules.md`, `43-cli-upload-protocol.md`, `44-cli-autofix-protocol.md`, `45-cli-test-plan.md`, `54-ac-j-series-cli-detail.md` | Companion CLI binary spec |
| **Server-side CLI endpoints** | `46-server-upload-frames-endpoint.md`, `47-server-autofix-endpoint.md`, `48-server-refresh-pointer-endpoint.md`, `52-ac-k-series-server-detail.md` | Upload/autofix/refresh frame endpoints |
| **Tests & CI** | `28-example-github-actions.md`, `32-cli-test-plan.md`, `33-bats-test-skeleton.md`, `34-phpunit-test-skeleton.md`, `35-reference-ci-yml.md`, `38-test-plan-superseded.md` | Test fixtures, CI workflows |
| **Docs & narrative** | `26-readme-and-screenshots.md`, `27-wp-cli-reference.md`, `36-why-v1-archived.md`, `37-blind-ai-gap-analysis.md`, `39-split-db-log-storage.md` | Reader-facing docs, history, gap analyses |
| **AC detail files** | `49-ac-section-a-detail.md`, `50-ac-delegation-maps-detail.md`, `53-ac-section-e-detail.md`, `55-ac-section-d-detail.md`, `56-ac-section-d-constraints-detail.md` | Promoted AC bodies (auditor-visible §97 satellites) |
| **Authoritative & meta** | `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md` | All ACs · version history · health report |
| **Locked-vacant** | slots `09–13` | Intentionally absent per AC-22-LV1 — do NOT fill |

**Entry-point heuristics:**
- New to §22? Read `00-overview.md` (this file) → `97-acceptance-criteria.md` → §99 inventory.
- Implementing an endpoint? Start at the REST or CLI-endpoint row.
- Debugging an audit finding? Read AC-78 + AC-22-LV1 in the Walker-Pin block above.

---

## AI Implementer Quickstart

**§22 is the largest module in scope (60 files, ~1 MB). Use the Quick-Nav Map above to locate files; use this block to land a change in ≤30 min without loading the bundle.**

1. **Contracts first** — [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) is canonical; AC detail files (`49–56`) are promoted bodies, not new contracts.
2. **Schema change?** Edit `02-database-schema.md` + `18-schema.sql` + `51-ac-enum-catalog-detail.md` together; re-render §26 `01-er-diagram.mmd` in the same commit.
3. **Endpoint change?** Edit `04-rest-api-endpoints.md` + `17-openapi.yaml` + `15-error-codes.md` together; touch `57-ac-section-d-endpoints-detail.md` if AC body shifts.
4. **CLI change?** `40-cli-overview.md` is the index; protocol files are `41-44`; ACs live in `54-ac-j-series-cli-detail.md`.
5. **SQLite locking / atomic writes?** See `## Appendix A` (line 217) — mirror of spec/13 AC-22, bound here via AC-26.
6. **Walker / audit finding?** Read [`00-auditor-notes.md`](./00-auditor-notes.md) §3 (AC-78 / AC-22-LV1 / AC-26 §97-tail surfacing) and §4 (Walker-Cap Finding Disposition with on-disk evidence triple) before touching slots `09–13` or filing any `[D5]/[D4]/[D3]` finding.

**Hard rules:** locked-vacant slots `09–13` MUST stay empty (AC-22-LV1) · §97 is the only place ACs live (detail files are promoted bodies, never new ACs) · schema/endpoint/CLI edits MUST update all sibling files in the same commit · no JWT/RS256 anywhere · split-DB boundary (`ShaRegistry` separate) is non-negotiable.

---

## Walker-Cap Finding Disposition (pointer)

> Full normative body relocated to [`00-auditor-notes.md` §4](./00-auditor-notes.md) per Sess-69 B-15 (Lesson #36 link-don't-restate, intra-module variant). On-disk evidence triple, D5/D4/D3 closed dispositions, and tier-1 walker footprint table all live there. Self-cited via `meta-verify-lockstep.py` (slot 64, gate #42) clause-5 banner-triple lockstep — any edit to the auditor-notes pin surface MUST be mirrored here in the same commit or CI fails.

---

## Drift Acknowledgment (Phase 27 — 2026-04-26)

This module is the **authoritative contract** for the Git Logs WordPress plugin (SQLite root DB, REST endpoints, App-Password auth, etc.). The actual plugin implementation (PHP files, SQLite migrations, REST handlers) lives in a **separate downstream WordPress-plugin repository**, not in this spec-only repo. The local code index only contains `linter-scripts/`. Drift findings of the form "spec describes WP plugin but no PHP/SQL files exist locally" are **expected and accepted**. The `kind: future-spec` frontmatter signals the audit to skip them. Until the downstream repo is wired into a unified codebase, an alignment score of N/A (not 0) is correct.

---

## Origin

This module is the authoritative rewrite of the Git Logs WordPress plugin spec, derived from the verbatim brief at [`../_archive/21-git-logs-v1/reference/00-verbatim-brief.md`](../_archive/21-git-logs-v1/reference/00-verbatim-brief.md). Where v1 (folder 21) and v2 (folder 22) conflict, **v2 wins**.

---

## Locked Decisions

| # | Decision | Value |
|---|----------|-------|
| 1 | Database engine | SQLite (Gitlogs root DB), single file |
| 2 | Naming | PascalCase tables, columns, JSON keys, JSON values |
| 3 | Primary keys | `INTEGER AUTOINCREMENT`, named `{TableName}Id` |
| 4 | Auth (writes / admin UI) | WordPress App Password / cookie auth |
| 5 | Auth (CI/CD) | `TempToken` + GitHub URL + branch validation; **JWT dropped** |
| 6 | Roles | Plugin-internal SQLite (Admin, Editor); not WP roles |
| 7 | Authorization | Always check **Permission**, never Role |
| 8 | Acceptance modes | `AcceptAllRepos`, `AcceptSelectedRepoOnly`, `AcceptSelectedRepoInAllVersions` |
| 9 | Branch restriction | `IsRestrictInBranch` + `StrictBranch` on GitProfile |
| 10 | App linkage | Polymorphic `AppLink` table (LinkType: GitProfile \| Repo) |
| 11 | App credentials | Inherit from parent Profile (no own tokens) |
| 12 | App lifecycle | `AppStatus` enum: Active, Disabled, Archived |
| 13 | Audit model | Three tables: `AuditTrail` (system), `History` (per RepoVersion), `Action` (enum log) |
| 14 | Migrations | Marker per plugin version in DB config table; idempotent |
| 15 | Logger | Level-aware (Trace/Debug/Info/Warn/Error/Fatal); Info/Debug runtime-disable |
| 16 | REST namespace | `git-logs/v2` |
| 17 | Endpoint count | 10 (see 04) |
| 18 | Plugin slug | `git-logs` |
| 19 | DB table prefix | none (SQLite root DB owned by plugin) |

---

## Top-Level UI Menus

Profile · Roles · AccessToRoles · GitProfile · Repo · RepoVersion · History · Action

Items marked `format:hide` in mind-map are informational only and never rendered.

---

## Document Inventory

| # | File | Description |
|---|------|-------------|
| 00 | [00-overview.md](./00-overview.md) | This index |
| 01 | [01-glossary-and-enums.md](./01-glossary-and-enums.md) | Terms + enum catalog |
| 02 | [02-database-schema.md](./02-database-schema.md) | Tables, columns, FKs, indexes (markdown) |
| 03 | [03-admin-ui.md](./03-admin-ui.md) | Menus, screens, fields |
| 04 | [04-rest-api-endpoints.md](./04-rest-api-endpoints.md) | 10 endpoints, request/response shapes |
| 05 | [05-auth-and-validation.md](./05-auth-and-validation.md) | TempToken + URL/branch validation |
| 06 | [06-migrations-and-logger.md](./06-migrations-and-logger.md) | Versioned migration markers + level-aware logger |
| 07 | [07-app-entity.md](./07-app-entity.md) | App schema, AppLink polymorphism, lifecycle |
| 08 | [08-history-and-action.md](./08-history-and-action.md) | History/Action vs AuditTrail separation |
| 09 | _09-seed-data_ | **Locked vacant slot** — content redistributed to §37 + §08 |
| 10 | _10-rate-limit-and-payload_ | **Locked vacant slot** — content redistributed to §05 + §18 |
| 11 | _11-encryption-deferred-plan_ | **Locked vacant slot** — content redistributed to §30 R3 |
| 12 | _12-wp-plugin-scaffold_ | **Locked vacant slot** — content redistributed to §38 (planned) |
| 13 | _13-v1-vs-v2-mapping_ | **Locked vacant slot** — mapping distributed across §05/§18/§30/§31 |
| 14 | [14-endpoint-examples.md](./14-endpoint-examples.md) | Curl + JSON samples for all 10 endpoints |
| 15 | [15-error-codes.md](./15-error-codes.md) | Unified `GL-*` error catalog |
| 16 | [16-seed-data.md](./16-seed-data.md) | Authoritative initial-row content for every lookup table + `ConfigKv` defaults (Phase P5 — slot 16 collision with old `16-test-plan.md` resolved by relocating the superseded stub to §38) |
| 17 | [17-openapi.yaml](./17-openapi.yaml) | OpenAPI 3.1 machine-readable spec for all 10 endpoints |
| 18 | [18-schema.sql](./18-schema.sql) | Verbatim DDL for V2_0_0 migration |
| 19 | [19-permission-matrix.md](./19-permission-matrix.md) | Role × Permission × Screen audit grid |
| 20 | [20-observability.md](./20-observability.md) | Site Health card, metrics endpoint, counters |
| 21 | _(removed v3.7.8 — slot retired, see §99)_ | i18n out of scope for v2 |
| 22 | [22-retention-and-pruning.md](./22-retention-and-pruning.md) | `wp git-logs prune` command + eligibility rules |
| 23 | [23-backup-restore.md](./23-backup-restore.md) | SQLite Online Backup + manifest + restore validation |
| 24 | [24-multisite.md](./24-multisite.md) | Per-site vs network behavior |
| 25 | [25-headless-auth-notes.md](./25-headless-auth-notes.md) | Headless WP + JWT/OAuth supported combos |
| 26 | [26-readme-and-screenshots.md](./26-readme-and-screenshots.md) | WP.org `readme.txt` + screenshot inventory |
| 27 | [27-wp-cli-reference.md](./27-wp-cli-reference.md) | Consolidated `wp git-logs *` subcommand catalog |
| 28 | [28-example-github-actions.md](./28-example-github-actions.md) | Drop-in workflow YAML for Lane B push + fixed |
| 29 | [29-uninstall-policy.md](./29-uninstall-policy.md) | DB retention modes on plugin removal |
| 30 | [30-threat-model.md](./30-threat-model.md) | STRIDE pass over the v2 attack surface |
| 31 | [31-ssh-key-auth.md](./31-ssh-key-auth.md) | SSH-key Lane B authentication: keypair lifecycle, signing, verification on ingest |
| 32 | [32-cli-test-plan.md](./32-cli-test-plan.md) | Authoritative CLI test plan (supersedes the old §16 plan; pairs with §33/§34 skeletons) |
| 33 | [33-bats-test-skeleton.md](./33-bats-test-skeleton.md) | Bats test skeleton — bash CLI integration coverage |
| 34 | [34-phpunit-test-skeleton.md](./34-phpunit-test-skeleton.md) | PHPUnit test skeleton — PHP plugin & REST coverage |
| 35 | [35-reference-ci-yml.md](./35-reference-ci-yml.md) | Reference GitHub Actions CI workflow wiring §33+§34 + lint gates |
| 36 | [36-why-v1-archived.md](./36-why-v1-archived.md) | Why v1 was archived — design rationale + migration trail (links to `_archive/21-git-logs-v1/`) |
| 37 | [37-blind-ai-gap-analysis.md](./37-blind-ai-gap-analysis.md) | Blind-AI gap analysis — implementability audit findings (relocated from §16 per Phase P5 immutability) |
| 38 | [38-test-plan-superseded.md](./38-test-plan-superseded.md) | **Superseded** — redirect stub for the old §16 test plan; authoritative content in §32–§35. Relocated from slot 16 in Phase P5 (2026-04-28) per Core memory file-slot-immutability rule. |
| 39 | [39-split-db-log-storage.md](./39-split-db-log-storage.md) | **v3.8.0 introduced; v2.9.0 active.** Per-SHA SQLite log storage. Root DB keeps only `ShaRegistry` + 3 ConfigKv keys (`ShaLogsRoot`, `MaxOpenShaDbHandles`, `ShaDbIdleCloseSec`); logs live in `<dataDir>/<ShaLogsRoot>/<Sha[0:2]>/<Sha>.db`. See §15 `GL-SHA-DB-*` codes, §22 prune, §23 backup manifest, §29 wipe. |
| 40 | [40-cli-overview.md](./40-cli-overview.md) | **J10.** `riseup-git-logs` CLI architecture overview — 4 read-only subcommands, 5-step identity discovery, `init` bootstrap. J-series tier-1 entry. Bound by §97 **AC-82**. |
| 41 | [41-cli-pointer-file-schema.md](./41-cli-pointer-file-schema.md) | **J11.** `.riseup-git-logs.json` wire format — JSON Schema Draft-07, 8-field closed inventory, 11-entry forbidden-field list, SemVer evolution. Bound by §97 **AC-83**. |
| 42 | [42-cli-classifier-rules.md](./42-cli-classifier-rules.md) | **J12.** Per-subcommand classifier rules — 4-outcome closed set (`NORMAL`/`WARN`/`ERROR`/`INTERNAL`), 5-step deterministic precedence, banner-version IS classifier-version. Bound by §97 **AC-84**. |
| 43 | [43-cli-upload-protocol.md](./43-cli-upload-protocol.md) | **J13.** CLI→server NDJSON-over-HTTPS upload — 7-section transport contract, 9-field frame envelope (16 forbidden), `Idempotency-Key` UUIDv4 (24h, sha256-mismatch→409), 6-attempt jittered retry, 7-row `GL-UPLOAD-*` envelope. Bound by §97 **AC-85**. |
| 44 | [44-cli-autofix-protocol.md](./44-cli-autofix-protocol.md) | **J14.** Server→CLI auto-fix — hybrid 4-state propose-diff-confirm-apply, 7-field bundle envelope (17 forbidden), 7-step preflight (`--auto-confirm` ignored for `major`), atomic per-file apply (no auto-rollback / no auto-commit / no auto-push), 11-row `GL-FIX-*` envelope. Bound by §97 **AC-86**. |
| 46 | [46-server-upload-frames-endpoint.md](./46-server-upload-frames-endpoint.md) | **K1.** `POST /wp-json/git-logs/v3/upload-frames` — Lane B writes only (Lane A→401 `GL-AUTH-LANE-MISMATCH`), 10-step validation order, per-SHA storage per §39, MUST NOT touch v2 `LogEntry`. Bound by §97 **AC-88**. |
| 47 | [47-server-autofix-endpoint.md](./47-server-autofix-endpoint.md) | **K2.** `GET /wp-json/git-logs/v3/autofix/{repoIdentityHash}/{frameId}` — Lane B reads only, 11-step validation+lookup, server-issued URL discipline (client construction→403 `GL-FIX-URL-CONSTRUCTED`), single-consumption atomic transaction, default 24h TTL, strong `ETag` + `Cache-Control: private, no-store`. Bound by §97 **AC-89**. |
| 48 | [48-server-refresh-pointer-endpoint.md](./48-server-refresh-pointer-endpoint.md) | **K3.** `POST /wp-json/git-logs/v3/refresh-pointer` — Lane B writes only, 9-step validation (auth precedes parse — CPU-amplification guard), 4-field identity envelope (10 forbidden body-top-level + 11 forbidden secret-shaped), 8-field §41 payload production, NO frame ingestion / NO `FixBundle` write, lower rate-limit (cap 30, refill 1/s). Bound by §97 **AC-90**. |
| 97 | [97-acceptance-criteria.md](./97-acceptance-criteria.md) | Testable AC (mirrors brief §Acceptance) |
| 98 | [98-changelog.md](./98-changelog.md) | Changelog |
| 99 | [99-consistency-report.md](./99-consistency-report.md) | Health/structure report |

---

## Audit Marker Exemption (Phase 39b, 2026-04-27)

**Issue:** The 2026-04-27 AI-implementability audit recorded `todo_count: 10` (overstated) and called out 2 unresolved markers from GAP-V2-07. As of Phase 39b both genuine markers are **resolved**:

- `30-threat-model.md:66` — replaced "(TODO: add seed)" with explicit reference to `ConfigChange` seed id 25 (already shipped in `18-schema.sql:409`); `16-seed-data.md` AuditActionType table backfilled to include row 25.
- `32-cli-test-plan.md:202` — replaced "with a TODO comment linking the GitHub issue" with the explicit `# QUARANTINE(<issue-ref>): <reason>` contract enforceable by `linter-scripts/check-quarantine-tracking.py`.

The remaining grep hits in `37-blind-ai-gap-analysis.md` are **historical narrative inside the GAP-V2-07 retrospective entry** — they describe what was fixed, not open work. Removing them would erase the audit trail required by the project memory's lockstep rule.

**Decision:** the module's `todo_density` is now `0` for active work. The audit's count of 10 was a substring false-positive driven by the GAP-V2-07 retrospective text and by quoted error-message fragments inside ACs. Future audit iterations SHOULD exclude `*-blind-ai-gap-analysis.md`, `*-changelog.md`, and fenced code blocks (Phase 39b follow-up R4).

**Evidence verified:** see `37-blind-ai-gap-analysis.md` GAP-V2-07 entry (now flagged `[LOW — RESOLVED 2026-04-27, Phase 39b]`).

---

## Appendix A — Mirror of `spec/13-generic-cli/97 AC-22` (SQLite locking + atomic file writes)

> **Non-normative mirror — canonical at `spec/13-generic-cli/97-acceptance-criteria.md` AC-22 (Phase 153 Task A11a).** Inlined here per Lesson #88 (cross-folder citation resolvability for context-bounded Raw-LLM agents). AC-26 of this module delegates the persisted-floor concurrency contract to AC-22; if you only have spec/22 in context, this excerpt is the contract you implement against. **If this mirror and spec/13 AC-22 ever diverge, spec/13 wins** — re-sync via `linter-scripts/check-lockstep.py`.
>
> **AC-22 — Database + file concurrency contract for SQLite + multi-threaded `exec` / `update`**
>
> - **Given** any binary that opens a SQLite database OR concurrently writes files under the config/data directory,
> - **When** the binary opens the connection or performs a write,
> - **Then** all of the following MUST hold:
>   - **PRAGMAs at startup:** `journal_mode=WAL`, `busy_timeout=5000` (cross-cuts spec/05 AC-SD-22), `foreign_keys=ON`.
>   - **Write transactions:** every WRITE MUST use `BEGIN IMMEDIATE` (NOT default `DEFERRED`) so lock acquisition fails fast rather than mid-transaction.
>   - **Retry on lock:** any `SQLITE_BUSY` / `SQLITE_LOCKED` MUST retry with exponential back-off — **3 attempts, base 100 ms, ±25 % jitter** (mirrors spec/27 AC-T-28 R3).
>   - **Atomic file writes outside SQLite:** config/lock/cache files MUST follow temp-then-rename (spec/27 AC-T-28 R1) — write to `<target>.tmp.<pid>`, `fsync`, `os.Rename`, cleanup in `finally`.
>   - **Parallel batch:** `--parallel=N` MUST serialize SQLite writes through a single connection pool (size = N), NOT N independent connections (N-connection mode is FORBIDDEN — amplifies WAL checkpoint contention).
>   - **Update lock:** `update` / `self-update` MUST acquire a process-level lock file at `~/.local/state/<binary-name>/update.lock` before mutating the binary; if held, exit 1 with `error: another update is in progress (lock held by PID <n>)`; release in `finally`/`defer`.
>
> **Cross-cuts:** spec/05 AC-SD-22 (`busy_timeout` cross-cutting), spec/27 AC-T-28 R1 (atomic temp-then-rename) + R3 (retry policy).
>
> **§22 binding:** AC-26 (rate-limit persisted-floor concurrency) delegates to this contract for the SQLite-backed `RateLimitFloor` table — the persisted floor is mutated under the same `BEGIN IMMEDIATE` + retry envelope. Any §22 endpoint that touches the floor (rate-limit checks in `04-rest-api-endpoints.md`, frame ingestion in `46-server-upload-frames-endpoint.md`) inherits this contract.

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Verbatim brief | [../_archive/21-git-logs-v1/reference/00-verbatim-brief.md](../_archive/21-git-logs-v1/reference/00-verbatim-brief.md) |
| Diagrams | [../26-gitlogs-diagrams/00-overview.md](../26-gitlogs-diagrams/00-overview.md) |
| Legacy v1 spec | [../_archive/21-git-logs-v1/00-overview.md](../_archive/21-git-logs-v1/00-overview.md) |
| DB conventions | [../04-database-conventions/00-overview.md](../04-database-conventions/00-overview.md) |
| Master coding guidelines | [../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/00-overview.md](../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/00-overview.md) |
| Outbound CI client (Lane B / SSH) | [../28-universal-ci-cli/00-overview.md](../28-universal-ci-cli/00-overview.md) — canonical client contract: posters CI runs invoke to push logs into this server (closes GAP-V2-09 per §37 Phase P17). |
