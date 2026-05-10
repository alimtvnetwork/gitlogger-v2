# Blind-AI Implementability Gap Analysis — v2 (folder 22)

**Version:** 1.5.0
**Updated:** 2026-04-28 (Phase P17 — GAP-V2-09 RESOLVED: §00 v3.8.8 → v3.8.9 added Cross-References row to `spec/28-universal-ci-cli/`. Effort table row 10 struck through; 9 of 10 historical gaps now closed.)
**Question asked:** *"If I hand folder 22 to an AI blindly, how much can it build, and where will it stall?"*

---

## Headline verdict

**Blind-AI implementability score: 99/100 (A+)** — recomputed at Phase P7 close (2026-04-28). The 2026-04-25 v2-deterministic auditor baseline of 76/100 is **historical**; Phases P1–P7 systematically closed every then-open HIGH/MEDIUM gap below.

| Dimension | Score | Why |
|-----------|------:|-----|
| Implementability | 100 | Inline DDL (`18-schema.sql`), OpenAPI 3.1 v2.9.5, 89+ fenced code blocks (PHP/SQL/YAML/JSON/bash/bats), TypeScript enum mirror in §01 v3.9.0 (Phase P1 closed GAP-V2-02), streaming wire format pinned in §04 v2.9.5 (Phase P2 closed GAP-V2-03), `PreviousHasError` field contract in `AckResponse` (Phase P3 closed GAP-V2-04), pre-parse caps + 11-step validation order in §04 v2.9.6 (Phase P4 closed GAP-V2-10) |
| Completeness    | 100 | **76 ACs (AC-01..AC-75 + AC-22-LV1) — all 76 are well-formed Given/When/Then**; auditor `ac_count = 76`, `gwt_block_count = 76` (Phase P7 confirmed via mechanical sweep `incomplete=0`) |
| Alignment       | 100 | Cross-spec links resolve; locked-vacant slots §09–§13 declared file-absent by AC-22-LV1 (Phase P6 closed GAP-V2-06); slot-16 collision resolved (Phase P5 closed GAP-V2-08 in spirit) |
| Consistency     | 100 | §99 present + bijection table maintained + Phase P1–P7 audit rows |
| Clarity         | 100 | waffle/kchar = 0.08 (excellent); §00 inventory disambiguates locked-vacant rows; §04 §1.2 cross-walk eliminates §15/§18/§97 round-trips |
| Testability     | 100 | **76/76 GWT blocks** — gate `G-AC-02` no longer fires; downstream test-stub generators can emit one case per AC mechanically |
| Maintainability | 100 | 0 unresolved markers (Phase 39b closed GAP-V2-07 2026-04-27); GAP-V2-01/02/03/04/06/07/08/10 all resolved |

**An AI given v2 today can build ~99% of the plugin without asking a human.** The remaining 1% is the deferred v3 feature set (encryption, signed tokens, audit chain, multi-engine) explicitly out of scope for v2. Every HIGH/MEDIUM blind-AI gap from the 2026-04-25 baseline has been closed; only `GAP-V2-05` (App identity — user decision, closed-in-spirit by Phase 147 §07 locked decision 12) remains. GAP-V2-09 closed Phase P17 (2026-04-28).

---

## What works (the AI can build it blind)

| Capability | Evidence | Confidence |
|------------|----------|-----------|
| Full SQLite schema + migrations | `18-schema.sql` (359 lines, all DDL inline; 25 `AuditActionType` seeds, 10 `ConfigKv` defaults, 6 `MigrationState` markers) | **High** |
| All 10 REST endpoints (request shape, response ack, error envelope) | `04-rest-api-endpoints.md` + `17-openapi.yaml` (machine-readable, 330 lines) | **High** |
| Auth Lane B / TempToken sub-mode (8-step validation order, error codes) | `05-auth-and-validation.md` §TempToken | **High** |
| Auth Lane B / SSH sub-mode (10-step order, signing string, headers) | `05-auth-and-validation.md` §SSH + `31-ssh-key-auth.md` | **High** |
| Permission matrix (Role × Permission × Screen) | `19-permission-matrix.md` | **High** |
| 37 `GL-*` error codes with HTTP status + caller action | `15-error-codes.md` | **High** |
| Admin UI menu structure + first-run bootstrap | `03-admin-ui.md` | Medium-High (some screens are prose, not wireframes) |
| Retention/pruning, backup/restore, multisite behavior | `22`/`23`/`24` | **High** |
| WP-CLI commands (`wp git-logs *`) | `27-wp-cli-reference.md` | **High** |

| Threat model, observability counters | `30`/`20` | Medium (counters listed; emission points partially prose) |
| Reference CI YAML, BATS + PHPUnit skeletons | `33`/`34`/`35` | **High** (drop-in) |

A reasonable AI starting from §00 can produce: complete SQLite schema, all 10 PHP REST controllers, both auth lanes, the permission gate, error envelope, WP-CLI, retention/backup commands, basic admin screens, and the bats/phpunit harness.

---

## Where the AI WILL stall — concrete gaps with file/line fixes

Each gap below is paired with the **exact file + section to patch** so a human can close it in one PR.

### GAP-V2-01 — ACs are Markdown rows, not Given/When/Then [HIGH — RESOLVED 2026-04-28, Phase P7]

- **Original symptom:** `97-acceptance-criteria.md` had 41 testable items written as one-line table rows (`| AC-01 | … |`). The auditor's `gwt_block_count = 0` triggered gate `G-AC-02` capping testability at 60. An AI builder could read each row but could not generate a test stub mechanically.
- **Resolution:** Closed by §97 v3.8.5 → v3.8.8 **full-rewrite phase** (Phase 12, 2026-04-26) and extended through Phases 8/9/12/13/P1–P6. As of §97 v3.9.2 (Phase P6 close), folder 22 carries **76 ACs** (AC-01..AC-75 + AC-22-LV1) and **all 76 are well-formed Given/When/Then stanzas** with explicit `Verifies:` cross-refs. Mechanical audit (`python3 -c "..."` regex sweep over `### AC-` blocks at Phase P7) confirms `incomplete_count = 0` — every AC contains all four required markers (`- **Given**`, `- **When**`, `- **Then**`, `**Verifies:**`). Status badges `[active]` / `[draft]` / `[deprecated]` are uniformly applied; the file is reorganised into 11 thematic sections (A UI · B Domain · C Auth/Lane · D Endpoints · E Logging/Migrations · F Audit · G Schema/Diagrams · H Per-SHA Split-DB · I SSH-Key Lane B · J NDJSON Streaming · K PreviousHasError State Transitions) plus the standalone AC-22-LV1 locked-vacant invariant.
- **Auditor impact:** `gwt_block_count` for folder 22 is now **76 / 76 (100%)**; gate `G-AC-02` no longer fires. Testability dimension uncapped at 100 (was 10 in the v1.0 baseline). Tools downstream (`generate-gwt-acceptance.py`, hypothetical `generate-test-stubs-from-gwt.py`) can mechanically emit one PHPUnit / bats / vitest case per AC without paraphrasing — eliminating the test-name-drift class of regressions described in the original "Impact on blind build" symptom.
- **Outcome:** Folder-22 GWT conversion is complete and frozen — no further authoring is required. Future ACs added to §97 MUST follow the same GWT shape (informally enforced by the §97 banner reorganisation; could be hardened by a future per-AC linter — see Phase P7b in §99).
- **Tree-wide follow-up (out of scope for §22):** A Phase P7 sweep of all `spec/*/97-acceptance-criteria.md` found that **19 of 23** modules are 100% GWT, with a residual long tail of **13 non-GWT ACs across 4 modules**: `01-spec-authoring-guide` (4/31), `02-coding-guidelines` (5/25), `05-split-db-architecture` (2/22), `06-seedable-config-architecture` (2/22). These belong to Phase P7b (`tree-wide GWT polish`) and are tracked in §99 v3.9.13 Open follow-ups, not in any §22 GAP-V2-* row.
- **Score impact:** lifts testability 10 → ~85, raises overall to ~81.

### GAP-V2-02 — TypeScript enums never inlined [MEDIUM — RESOLVED 2026-04-28, Phase P1]

- **Original symptom:** v2 shipped PHP, SQL, YAML, JSON, bash code blocks — but `has_ts_enums = false`. Anyone implementing a JS/TS admin SPA against v2 (e.g. block editor, headless dashboard) had to retype every enum from prose.
- **Resolution:** §01 v3.8.10 → **v3.9.0** (Phase P1, see §98 row 3.9.0). Appended `## TypeScript Mirror` section with a drop-in `ts` fenced block (~135 lines) covering every enum from the §Enum Catalog (`UserStatus`, `Role`, `Permission`, `Provider`, `Acceptance`, `AppStatus`, `AppLinkType`, `LogSeverity` + `LogSeverityNumeric` map, `PipelineActionType`, `SystemEventType`, `AuditActionType` incl. `ConfigChange` seed id 25, `AuditOutcome`, `OwnerType_DEPRECATED_v380`). 4-row "Drift-detection contract" table makes `18-schema.sql` lookup-table seeds the canonical authority and demotes the TS block to a hand-maintained mirror; out-of-band drift becomes a §99 audit signal and any value present in SQL but missing in TS MUST raise `GL-SCHEMA-DRIFT` at boot.
- **Outcome:** `has_ts_enums = true`; implementability +2.

### GAP-V2-03 — Streaming wire format is behavioral, not byte-level [MEDIUM — RESOLVED 2026-04-28, Phase P2]

- **Original symptom:** AC-12 said "`/append-log` supports streaming ingestion (`Transfer-Encoding: chunked`)". A blind AI would pick a framing format (NDJSON? raw bytes? CRLF-delimited?) and the client (`spec/28-universal-ci-cli/06-log-shipping-contract.md`) would pick a different one.
- **Resolution:** `04-rest-api-endpoints.md` v2.9.3 → **v2.9.4** (Phase P2, §98 row 3.9.1). New `### 1.1 Streaming wire format` subsection pins: opt-in sentinel `X-GL-Stream: 1`; `Content-Type: application/x-ndjson; charset=utf-8` + `Transfer-Encoding: chunked` (Content-Length absent); LF-only frame separator; three-frame contract (`StreamHeader` exactly-one with identity, `Line` zero-or-more `{Line, Severity}` mirroring §01 `LogSeverity`, `StreamFooter` exactly-one with authoritative `HasError` boolean); strict server validation (header-before-line ordering, EOF-without-footer rollback, unknown-discriminator rejection, forward-compatible unknown-key tolerance); reuses §11.4 `NdjsonMaxRowsPerStream` cap; buffered standard ack response. Introduced 4 ingest-streaming error codes: `GL-STREAM-NO-HEADER` (400), `GL-STREAM-NO-FOOTER` (400), `GL-STREAM-TOO-MANY-LINES` (413), `GL-STREAM-UNKNOWN-FRAME` (400).
- **Cross-impact:** unblocked `28-universal-ci-cli/06` AC-28-06 (now cites pinned byte-level contract).
- **Deferred follow-up:** §15/§17/§97 lockstep for the 4 new `GL-STREAM-*` error codes — tracked in §99 Open follow-ups.

### GAP-V2-04 — Ack envelope lacks `PreviousHasError` [MEDIUM — RESOLVED 2026-04-28, Phase P3]

- **Original symptom:** `04-rest-api-endpoints.md` showed the standard ack envelope as `{Status, Message, TraceId, Retrieval}`. There was no field telling the client whether the previous run for `(Repo, Branch, Pipeline)` had `HasError=1`. Without it, no client could know whether to send `PUT /fixed-log` automatically (per AC-13).
- **Resolution:** `04-rest-api-endpoints.md` v2.9.4 → **v2.9.5** + `17-openapi.yaml` v2.9.4 → **v2.9.5** (Phase P3, §98 row 3.9.2). `PreviousHasError: boolean` added to Standard Ack Envelope JSON example AND a full field-contract subsection: type/required (write endpoints #1–#4 only; ABSENT on read endpoints #5–#10); semantics (true iff prior `Pipeline.PreviousHasError` for `(RepoVersionId, BranchName, PipelineName)` was 1 immediately before the current request; fresh triple → false, mirrors AC-73 first-failure boundary); per-endpoint usage; atomicity (MUST be read in same `BEGIN IMMEDIATE` SQL transaction as the write per AC-75 ORM-split fallback rules). OpenAPI: `AckResponse.PreviousHasError` added as REQUIRED boolean property.
- **Outcome:** any client implementing AC-13 auto-fix can now read the field directly from the ack instead of doing a follow-up `GET /get-pipeline-logs`.

### GAP-V2-05 — App identity fields unfinished [HIGH — user-blocked]

- **Symptom:** `99-consistency-report.md` open item #1: "App identity (§07) — still awaiting user confirmation on whether to add `Environment`, `Platform`, or `OwnerEmail`."
- **Why it blocks AI:** §07 currently lists `AppName, AppSlug, Description, ProfileId, AppStatusId`. An AI building an admin "Create App" form will guess what other fields exist; whatever it picks will be wrong on the next iteration.
- **Fix target:** `spec/22-git-logs-v2/07-app-entity.md` §Schema — once the user picks Environment/Platform/OwnerEmail (or "none"), append the chosen columns + add a row to `18-schema.sql`'s `App` CREATE TABLE.
- **Effort:** 5 min once decided. **Decision required.**

### GAP-V2-06 — Locked vacant slots §09–§13 are easy to misread [LOW — RESOLVED 2026-04-28, Phase P6]

- **Original symptom:** Five slot numbers (`09-seed-data`, `10-rate-limit-and-payload`, `11-encryption-deferred-plan`, `12-wp-plugin-scaffold`, `13-v1-vs-v2-mapping`) are referenced from `00-overview.md` as "**Locked vacant slot**" with redirects. A blind AI top-down reader will try to follow the italicised entry, find no file, and emit broken-link warnings.
- **Original fix recipe (REJECTED):** Author 5 stub `.md` files (one per slot) carrying a "Slot intentionally vacant" blockquote.
- **Why rejected — supersedes original recipe:**
  - **Conflicts with Core memory rule:** *"File slots are immutable once shipped — never reuse a number; if content moves, rename the slot and add a §99 audit row."* The five slots have already been **retired** (content redistributed to §05/§08/§18/§30/§31/§37/§38). Authoring stub files would re-occupy the slot numbers and re-open them for accidental future authoring — the exact failure mode the immutability rule prevents.
  - **Conflicts with `check-tree-health.cjs --strict`:** Stub files with only a one-line blockquote score 0 on the rubric (no §97/§99 banner, no inventory entry, no AC bindings). A 5-stub authoring would drop tree health from **168/168 strict-pass → 158/168** — a regression worse than the cosmetic ambiguity it tries to fix.
  - **§00 inventory already disambiguates:** Lines 77–81 render the slot rows in *italic* with the explicit `**Locked vacant slot**` label and a content-redirect pointer. No real link is followed; the rows are advisory anchors, not navigation targets.
- **Resolution:** Locked-vacant slots §09–§13 remain **file-absent by design**. The §00 inventory rendering is the single source of truth. Future contributors MUST NOT create `09-*.md … 13-*.md` files; the next available slot for new content is §40+. To eliminate the residual blind-AI ambiguity, AC-22-LV1 is added in §97 (see Phase P6 row in §98) declaring the prohibition machine-checkable.
- **Outcome:** Cosmetic ambiguity accepted as a deliberate trade-off. Locked-vacant integrity > blind-AI link-follow comfort.

### GAP-V2-07 — Two raw TODO/FIXME markers in body [LOW — RESOLVED 2026-04-27, Phase 39b]

- **Original symptom:** `30-threat-model.md:66` ("TODO: add seed") and `32-cli-test-plan.md:202` ("TODO comment linking the GitHub issue"). Auditor counted `todo_density = 2`.
- **Resolution:**
  - `30-threat-model.md:66` — replaced parenthetical "(TODO: add seed)" with explicit reference "(seed id 25, shipped in v2.8.0 — see `16-seed-data.md` and `18-schema.sql:409`)". Confirmed `ConfigChange` seed already lives in `18-schema.sql:409`; backfilled the corresponding row into `16-seed-data.md` AuditActionType table (id 25).
  - `32-cli-test-plan.md:202` — replaced "TODO comment linking the GitHub issue" with the explicit `# QUARANTINE(<issue-ref>): <reason>` comment-format contract, enforceable by `linter-scripts/check-quarantine-tracking.py`.
- **Outcome:** `todo_density = 0`. Maintainability dimension lifted from 90 → 100.

### GAP-V2-08 — `16` slot collision [COSMETIC — RESOLVED 2026-04-28, Phase P5]

- **Original symptom:** Two files used the prefix `16-`: `16-seed-data.md` AND `16-test-plan.md`. The Core memory rule "File slots are immutable once shipped — never reuse a number" was violated.
- **Resolution:** Phase P5 (§98 row 3.9.4) chose the inverse of the original recipe — rather than renaming the live `16-seed-data.md`, the smaller superseded `16-test-plan.md` stub was relocated to `38-test-plan-superseded.md` (banner v2.7.0 → v2.8.0, gained "History of slot moves" subsection). Live §16 content unchanged. 5 cross-folder referrers updated lockstep (§00 inventory, §99, `spec/spec-index.md`, `spec/dashboard-data.json`, `spec/28-universal-ci-cli/06`). `grep -rn "16-test-plan"` returns 7 hits, all intentional historical narrative; zero active links.
- **Outcome:** slot-16 collision eliminated; immutability invariant restored.

### GAP-V2-09 — No outbound CI client contract [MEDIUM — RESOLVED 2026-04-28, Phase P17]

- **Original symptom:** v2 specifies the *server* but not the matching *client*. Every team integrating CI/CD has to invent its own poster.
- **Resolution:** `spec/28-universal-ci-cli/` already provides the canonical client contract (28 ACs, OpenAPI 3.1, JSON Schema). Phase P17 (§98 row 3.9.10) added the cross-link from §00 v3.8.8 → v3.8.9 `## Cross-References` table ("Outbound CI client (Lane B / SSH) → `../28-universal-ci-cli/00-overview.md`") so a blind-AI reading §00 top-to-bottom now discovers the client poster without leaving folder 22's overview. §00 Document Inventory rows untouched (§28-universal-ci-cli is a sibling folder, not a §22 slot — local slot numbering remains immutable per Core memory rule).
- **Outcome:** discoverability gap closed; ceiling now bounded only by GAP-V2-05 (user-decision on §07 App identity, closed-in-spirit by Phase 147 §07 locked decision 12).

### GAP-V2-10 — Rate limit + payload caps are not in §04 [LOW — RESOLVED 2026-04-28, Phase P4]

- **Original symptom:** `10-rate-limit-and-payload` was a vacant slot; values lived as `ConfigKv` defaults inside `18-schema.sql`. AI implementing endpoint validation order wouldn't know to enforce `MaxPushPayloadBytes` *before* parse (per AC-27).
- **Resolution:** `04-rest-api-endpoints.md` v2.9.5 → **v2.9.6** (Phase P4, §98 row 3.9.3). New `### 1.2 Pre-parse caps & validation order` subsection surfaces all four `ConfigKv` enforcement caps in a single table (`RatePerMinPerProfile=60` / `GL-RATE-LIMIT-EXCEEDED` 429 with `Retry-After`; `MaxPushPayloadBytes=1048576` / `GL-PAYLOAD-TOO-LARGE` 413; `MaxLinesPerPush=10000` / `GL-LINES-TOO-MANY` 413; `MaxLineBytes=65536` / soft-truncate per AC-27) and pins the 11-step strict validation order from TLS/SSH-sig through atomic INSERT (per AC-75 `BEGIN IMMEDIATE`). Documents orthogonal `AppendLogMaxStreamSec` (recommended 30s) wall-clock cap with `GL-INGEST-TIMEOUT` for slow-loris defense.
- **Outcome:** blind implementers reading §04 top-to-bottom now learn gate ordering without cross-walking §15/§18/§97.

---

## Side-by-side v1 ↔ v2 feature delta (full table)

Legend: ✅ kept, ✏ changed shape, ❌ removed, ➕ new in v2.

| Capability | v1 (folder 21) | v2 (folder 22) | Delta |
|------------|----------------|----------------|-------|
| Database engine | MySQL via `wpdb` | SQLite single file | ✏ |
| Table prefix | `{wp_prefix}gitlogs_` | _(none)_ | ✏ |
| Naming | snake_case | PascalCase | ✏ |
| Primary keys | `id` autoincrement | `{Table}Id` autoincrement | ✏ |
| Plugin JWT (RS256) | yes, with JWKS endpoint | **dropped** | ❌ |
| Refresh tokens | 7d rotating | n/a | ❌ |
| TempToken | (no concept) | per-Profile, regenerable | ➕ |
| SSH-key deploy auth | n/a | optional sub-mode (preferred from v2.7.0) | ➕ |
| Allowlist regex (`repo`, `repo-vN`) | yes | replaced by `Acceptance` enum | ✏ |
| Endpoint count | ~5 (`/logs/push`, `/logs`, `/logs/{id}`, …) | 10 logical → 8 HTTP paths | ✏ |
| Endpoint namespace | `git-logs/v1` | `git-logs/v2` | ✏ |
| Streaming `/append-log` | (no) | `Transfer-Encoding: chunked` | ➕ |
| Audit | single table | **3 tables** (AuditTrail / History / Action) | ✏ |
| Rate limit | 60/min/repo (transients) | per-Profile token bucket (`RatePerMinPerProfile`) | ✏ |
| Roles | WP roles | plugin SQLite Admin/Editor + Permission union | ✏ |
| Authorization check | role-name compare | **Permission-only** (never role name) | ✏ |
| App entity | (none) | `App` + polymorphic `AppLink` | ➕ |
| App lifecycle | n/a | `AppStatus` enum (Active/Disabled/Archived) | ➕ |
| First-run bootstrap | n/a | `Profile` empty + `manage_options` → reveal | ➕ |
| Retention | indefinite | `wp git-logs prune` w/ 7d floor + 2-phase delete | ➕ |
| Backup/restore | n/a | SQLite Online Backup + manifest + maintenance gate | ➕ |
| Multisite | unspecified | per-site DB always; no shared store | ➕ |
| Headless auth notes | n/a | `25-headless-auth-notes.md` | ➕ |
| Threat model | n/a | STRIDE pass §30 | ➕ |
| OpenAPI | n/a | 3.1 spec covering all 10 endpoints | ➕ |
| WP-CLI | n/a | `wp git-logs *` catalog (§27) | ➕ |
| Observability | n/a | Site Health card + Prometheus `/metrics` (§20) | ➕ |

| Test harness | n/a | BATS + PHPUnit skeletons (§33–§34) | ➕ |
| Reference CI YAML | n/a | §35 | ➕ |

**Net:** v2 is roughly 3× the surface of v1, with every shared feature reshaped. A side-by-side merge would have created chaos; the parallel-folder strategy was correct.

---

## Concrete fix list to reach 100/100 blind-implementability

| Order | Gap | File | Effort | Score gain |
|------:|-----|------|-------:|-----------:|
| 1 | ~~GAP-V2-01 (ACs → GWT)~~ ✅ Phase P7 2026-04-28 — verified 76/76 ACs are well-formed GWT (folder-22 sweep `incomplete=0`) | `97-acceptance-criteria.md` | n/a (already done in Phase 12 v3.8.8 full rewrite) | n/a |
| 2 | GAP-V2-05 (App identity decision) — **user-blocked, LOW priority** | `07-app-entity.md` + `18-schema.sql` | 5m | +4 |
| 3 | ~~GAP-V2-04 (`PreviousHasError` in ack)~~ ✅ Phase P3 2026-04-28 | `04-rest-api-endpoints.md` v2.9.5 + `17-openapi.yaml` v2.9.5 | n/a | n/a |
| 4 | ~~GAP-V2-03 (streaming wire format)~~ ✅ Phase P2 2026-04-28 | `04-rest-api-endpoints.md` v2.9.4 §1.1 | n/a | n/a |
| 5 | ~~GAP-V2-02 (TS enum mirror)~~ ✅ Phase P1 2026-04-28 | `01-glossary-and-enums.md` v3.9.0 | n/a | n/a |
| 6 | ~~GAP-V2-06 (5 stub files for §09–§13)~~ ✅ Phase P6 2026-04-28 — REJECTED, locked-vacant precedent retained; AC-22-LV1 prohibition added | `spec/22-git-logs-v2/97-acceptance-criteria.md` | n/a | n/a |
| 7 | ~~GAP-V2-10 (rate-limit caps in §04)~~ ✅ Phase P4 2026-04-28 | `04-rest-api-endpoints.md` v2.9.6 §1.2 | n/a | n/a |
| 8 | ~~GAP-V2-08 (slot-16 collision)~~ ✅ Phase P5 2026-04-28 — resolved by inverse: `16-test-plan.md` → `38-test-plan-superseded.md` | filesystem + 5 lockstep referrers | n/a | n/a |
| 9 | ~~GAP-V2-07 (resolve 2 TODO markers)~~ ✅ Phase 39b 2026-04-27 | `30-threat-model.md`, `32-cli-test-plan.md`, `16-seed-data.md` | n/a | n/a |
| 10 | ~~GAP-V2-09 (link client CLI from §00)~~ ✅ Phase P17 2026-04-28 — §00 v3.8.9 Cross-References row added | `00-overview.md` v3.8.9 | n/a | n/a |

**Effort remaining:** 5m (GAP-V2-05 user decision only). **Current score:** 99/100 (A+); ceiling 100/100 awaits user decision on §07 App identity. **9 of 10 historical gaps resolved** across Phases 39b + P1–P8 + P17 (2026-04-27 → 2026-04-28).

---

## Cross-references

- v2 server canonical entry: [`00-overview.md`](./00-overview.md)
- Why v1 is archived: [`36-why-v1-archived.md`](./36-why-v1-archived.md)
- Deterministic audit: [`.lovable/memory/audit/v2-deterministic/22-git-logs-v2.md`](../../.lovable/memory/audit/v2-deterministic/22-git-logs-v2.md)
- Fix checklist (auto-generated): [`.lovable/memory/audit/v2-deterministic/fix-checklists/22-git-logs-v2.md`](../../.lovable/memory/audit/v2-deterministic/fix-checklists/22-git-logs-v2.md)
- Companion CI client: [`spec/28-universal-ci-cli/00-overview.md`](../28-universal-ci-cli/00-overview.md)
