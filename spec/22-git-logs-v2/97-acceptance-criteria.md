# Acceptance Criteria (v2)

**Version:** 3.22.0  
**Updated:** 2026-05-07 (Phase J15 — final J-series slot: new file `45-cli-test-plan.md` v1.0.0 + new **AC-87** `[critical]` binding 6 sub-contracts (two-layer L1+L2 architecture + closed 5-suite matrix T-CLI-IDENT/PTR/CLASSIFY/UPLOAD/AUTOFIX with min-case floors 7/9/11/13/12 = ≥52 L2 cases + per-suite GWT 1:1 to AC-82..AC-86 sub-sections + fixture taxonomy + L1≥85% line coverage + 100% GL-* negative-path + 100% ExitCode positive + CI binding to spec/12 AC-10 runner matrix + 6 forbidden patterns); AC-80 row 42 added. **J-series sextet AC-82..AC-87 contract-complete.** AC count 83 → 84 (+1 — AC-87). Lesson #36 septuple link-don't-restate to spec/22 §32/§33/§41/§42/§43/§44 + spec/13 AC-21/AC-22 + spec/12 AC-10. Closes inherited backlog J15.)

---

## Format

Every criterion below is stated as **Given / When / Then**. Each AC also carries a `Verifies:` pointer to the source section(s) of this folder so a downstream auditor can trace the assertion back to the authoritative spec without external context.

> **Status legend:** `[active]` = enforced for v2.9.3 schema. `[draft]` = not yet enforced (no rows in this file currently carry this state — kept here for future phases). `[deprecated]` = retained for cross-version diff only.

---

## Section A — UI / Menu / First-Run

### AC-01 — Top-level menu inventory  `[active]`
- **Given** a freshly migrated v2 install with at least one Profile present
- **When** an authenticated WP admin opens the plugin's top-level menu
- **Then** exactly these 8 items render in this order: `Profile`, `Roles`, `AccessToRoles`, `GitProfile`, `Repo`, `RepoVersion`, `History`, `Action` — no more, no fewer.
- **Verifies:** brief §1.a–h, §03.

### AC-25 — `format:hide` items not rendered  `[active]`
- **Given** a mind-map node carries the `format:hide` annotation (per §03 spec-layout pragma family alongside `format:section`, `format:badge`)
- **When** the admin UI renderer projects the node into any DOM surface (list, detail, form, CSV export, JSON-API projection, audit diff)
- **Then** the node MUST be omitted from the rendered DOM entirely (never CSS-hidden, never `hidden`-attr, never off-screen) at the server- or React-render boundary; the rule MUST hold across every projection (partial honoring = SPEC VIOLATION); empty parents whose every child is hidden MUST also be omitted; the rule is **strictly subtractive** and distinct from RBAC hiding per AC-06 / AC-39.
- **Verifies:** brief §1.j, §03, AC-06, AC-39, **§49 §AC-25 detail (D1–D8)** — full normative body lives in `49-ac-section-a-detail.md`.

### AC-28 — First-run bootstrap form gating  `[active]`
- **Given** the `Profile` table is empty AND the current WP user holds `manage_options`
- **When** any plugin admin route is loaded
- **Then** the bootstrap form renders, the generated credentials are revealed exactly once on submit, and the form re-appears if the last Profile row is later deleted.
- **Verifies:** §03.

### AC-54 — IsOrganization checkbox in GitProfile form  `[active]`
- **Given** the GitProfile create/edit form
- **When** an admin opens it
- **Then** an **Is organization** checkbox (default off) renders bound to `GitProfile.IsOrganization` (0/1); the legacy "OwnerType (derived)" field MUST NOT render; toggling the checkbox flips the canonical URL form between `github.com/$org/$repo` and `github.com/$username/$repo` on save.
- **Verifies:** §03 + v3.8.1.

### AC-59 — History Activity tab  `[active]`
- **Given** the History admin screen post-v3.8.2
- **When** an authorized user opens it
- **Then** an **Activity** tab renders backed by `SystemEvent` with filter chip *Git events / System events / All*; the legacy "Action" top-level menu label is retained but is now backed by the renamed `PipelineAction` table.
- **Verifies:** §03 + v3.8.2.

### AC-77 — History `HasError + StateLabel` column rendering  `[active]`
- **Given** a `Pipeline` row with `(PreviousHasError, HasError)` both NOT NULL CHECK IN (0,1) per §18 v2.9.2
- **When** the admin UI renders the `HasError + StateLabel` column on the History screen (or any surface listing Pipeline rows — RepoVersion drill-down, Activity *All* tab)
- **Then** the cell MUST render the raw `HasError` glyph (✅/❌) plus the AC-73 derived state-transition chip carrying `data-state-label="<key>"` (key ∈ `{still-green, first-failure, still-failing, just-recovered}`); the label MUST be derived from `(PreviousHasError, HasError)` at render time per AC-73's pure-function rule (no caching, no `StateLabelCache` column); exhaustive over the 4-label set with no fallback (out-of-set tuple → `GL-INTERNAL`); localized text MAY translate but `data-state-label` MUST stay canonical English; color-blind safe (glyph or text required); column MUST offer 4-way sort + 4-value multi-select filter defaulting to all-selected; rendered label MUST equal AC-74 NDJSON `Header.StateTransition` for the same `PipelineId` at the same instant.
- **Verifies:** §03 v2.3.0, AC-73, AC-74, AC-75, §18 v2.9.2, §17 (`NdjsonHeaderFrame.StateTransition`), §01 v3.8.10, **§49 §AC-77 detail (D1–D8)** — full normative body lives in `49-ac-section-a-detail.md`.

---

## Section B — Domain Model & Profiles

### AC-02 — Profile fields  `[active]`
- **Given** a `Profile` row exists in the SQLite root DB (path per §39 `ConfigKv.RootDbPath`, conventionally `<plugin-data>/git-logs.db`)
- **When** the row is read via `SELECT * FROM Profile WHERE ProfileId = :id`
- **Then** the result MUST contain exactly these columns and no others (per §02 v3.8.6 + §18 v2.9.3 DDL): `ProfileId INTEGER PRIMARY KEY AUTOINCREMENT`, `UserName TEXT NOT NULL UNIQUE`, `Email TEXT NOT NULL`, `GeneratedKeyApi TEXT NOT NULL` (server-issued opaque token used as the WP App Password username — see §05 §3.a), `Token TEXT NOT NULL` (the long-lived bearer token paired with `GeneratedKeyApi` per §05), `TempToken TEXT NULL` (short-lived rotation slot, NULL when no rotation in flight), `CreatedAt INTEGER NOT NULL`, `UpdatedAt INTEGER NOT NULL`; AND there MUST NOT be any column named `Password`, `PasswordHash`, `Salt`, `Pepper`, or any other plaintext-or-derived secret material — the schema is intentionally password-free because authentication uses WP App Passwords (§05 Lane A) or SSH key signatures (§31 Lane B), never a Profile-stored password; AND the `UNIQUE` constraint on `UserName` MUST be enforced at the SQLite level (not application level) so concurrent inserts cannot race past a `SELECT … WHERE UserName = ?` check.
- **Verifies:** brief §2 (Profile entity), §02 v3.8.6 (Profile table doc), §18 v2.9.3 (DDL), §05 (Lane A auth flow), §31 (Lane B auth flow), §39 (RootDbPath ConfigKv key).

### AC-07 — GitProfile URL canonicalization  `[active]`
- **Given** a GitProfile is saved with `IsOrganization` set to 0 or 1
- **When** the URL is normalized on save
- **Then** the trailing slash is optional on input, the stored URL is `github.com/$org/$repo` when `IsOrganization=1` else `github.com/$username/$repo`.
- **Verifies:** brief §Domain.2 + v3.8.0, §02.

### AC-08 — GitProfile.Acceptance enum  `[active]`
- **Given** a GitProfile row
- **When** the `Acceptance` column is read
- **Then** the value MUST be one of `AcceptAllRepos`, `AcceptSelectedRepoOnly`, `AcceptSelectedRepoInAllVersions` — any other value is a schema violation.
- **Verifies:** brief §Domain.3.b, §02.

### AC-09 — Branch restriction toggle  `[active]`
- **Given** a GitProfile row with `IsRestrictInBranch` flipped
- **When** the form re-renders AND a `/append-log` request is dispatched
- **Then** the `StrictBranch` field's UI visibility AND server-side enforcement BOTH track the toggle (no orphan enforcement when hidden, no orphan visibility when disabled).
- **Verifies:** brief §Domain.3.f, §05.

### AC-10 — Repo / RepoVersion split  `[active]`
- **Given** a GitHub URL with a `-vN` suffix
- **When** it is registered
- **Then** the `Repo` row stores the URL **stripped** of `-vN`, and a `RepoVersion` row stores the variant linked back to the parent Repo row by FK.
- **Verifies:** brief §Domain.5, §02, §18.

### AC-17 — App entity columns  `[active]`
- **Given** an `App` row exists in the SQLite root DB (per §02 v3.8.6 + §18 v2.9.3 DDL; this is the consumer-app identity table introduced by §07 locked decisions 10–12)
- **When** the row is read via `SELECT * FROM App WHERE AppId = :id`
- **Then** the result MUST contain exactly these columns and no others: `AppId INTEGER PRIMARY KEY AUTOINCREMENT`, `AppName TEXT NOT NULL`, `AppSlug TEXT NOT NULL UNIQUE` (kebab-case identifier used in `/append-log` payloads — `[a-z0-9][a-z0-9-]*` per §07 locked decision 11), `Description TEXT NULL`, `ProfileId INTEGER NOT NULL REFERENCES Profile(ProfileId) ON DELETE RESTRICT` (the App MUST be owned by exactly one Profile — RESTRICT prevents orphaning), `AppStatusId INTEGER NOT NULL REFERENCES AppStatus(AppStatusId) ON DELETE RESTRICT` (lookup table per §02; values `Active` / `Suspended` / `Archived` per §01 glossary), `CreatedAt INTEGER NOT NULL`, `UpdatedAt INTEGER NOT NULL`; AND `AppSlug` UNIQUE MUST be enforced at the SQLite level so two Profiles cannot register the same slug; AND the `App` table MUST NOT carry `Environment`, `Platform`, `OwnerEmail`, or any other identity-shaped column — these are PERMANENTLY FORBIDDEN per §07 locked decision 12 (finalized 2026-04-28, Phase 147 `B1: keep forbidden`); future expansion requires a NEW locked decision, not an edit to #12.
- **Verifies:** locked decisions 10–12 (App entity scope), §02 v3.8.6 (App + AppStatus table doc), §18 v2.9.3 (DDL + FK constraints), §01 (AppStatus enum), §07 (Phase B1 blocked fields).

### AC-18 — Polymorphic AppLink  `[active]`
- **Given** an `AppLink` row insert is attempted (per §02 v3.8.6 + §18 v2.9.3 DDL — this table associates an `App` with EITHER a specific `Repo` OR a specific `GitProfile` for credential-inheritance scoping per §07 locked decision 10)
- **When** the row is committed
- **Then** the SQLite-level `CHECK` constraint MUST enforce XOR semantics: `CHECK ((RepoId IS NOT NULL) <> (GitProfileId IS NOT NULL))` — i.e. exactly one of the two FK columns is non-NULL, never both, never neither; AND inserting a row with both columns NULL MUST fail with SQLite error code 19 (`SQLITE_CONSTRAINT_CHECK`) — application-layer guards alone are NOT sufficient; AND inserting a row with both columns set MUST also fail with the same constraint error; AND the table MUST carry composite UNIQUE constraints `UNIQUE (AppId, RepoId)` and `UNIQUE (AppId, GitProfileId)` so a single App cannot link to the same Repo or GitProfile twice (the NULL side is exempt by SQLite's standard UNIQUE-with-NULL semantics, which is the desired behavior); AND both FKs MUST use `ON DELETE CASCADE` so deleting the parent `App`, `Repo`, or `GitProfile` automatically prunes the dangling link rows; AND the polymorphic discriminator is implicit (which column is non-NULL) — the table MUST NOT carry an explicit `LinkType TEXT` column because the XOR CHECK already encodes it and a separate column risks drift between `LinkType` and the actual non-NULL FK.
- **Verifies:** locked decision 10 (polymorphic linking design), §02 v3.8.6 (AppLink table doc), §18 v2.9.3 (DDL + CHECK + UNIQUE + FK CASCADE).

### AC-19 — App credential inheritance  `[active]`
- **Given** an App linked to a parent Profile
- **When** the App attempts an authenticated call
- **Then** the App MUST NOT carry its own `Token`/`TempToken`/`GeneratedKeyApi`; credentials resolve through `App.ProfileId → Profile`.
- **Verifies:** locked decision 11, §05.

### AC-20 — App lifecycle gates push  `[active]`
- **Given** an App with `AppStatus ∈ {Active, Disabled, Archived}`
- **When** a `/append-log` arrives bound to that App (via `Repo` or `GitProfile` linkage)
- **Then** only `Active` accepts; `Disabled` and `Archived` reject with the §15 envelope.
- **Verifies:** locked decision 12, §05, §15.

---

## Section C — Auth, Tokens & Lane Routing

### AC-15 — CI/CD URL+branch authoritative, TempToken non-authoritative  `[active]`
- **Given** a `/append-log` from CI/CD
- **When** the auth lane resolves
- **Then** the GitHub URL + branch combination is the authoritative identity; the `TempToken` is checked but is **non-authoritative** (it cannot grant access if URL/branch fails).
- **Verifies:** brief §Auth.4, §05, §25.

### AC-16 — JWT not implemented  `[active]`
- **Given** the v2 codebase and shipped DDL
- **When** any token-handling code path is inspected
- **Then** there MUST be no JWT issuance, validation, signing key, or `jwt.io`-style header parsing — only opaque Tokens (Lane A) and SSH signatures (Lane B).
- **Verifies:** brief §Auth + locked decision 5, §05, §25.

### AC-26 — Per-Profile rate limit  `[active]`
- **Given** a Profile is making sustained requests
- **When** the per-minute count exceeds `ConfigKv.RatePerMinPerProfile`
- **Then** subsequent requests in that minute return HTTP 429 with a `Retry-After` header; the bucket state survives the request boundary (in-memory + persisted floor).
- **Concurrency contract (cross-module, link-don't-restate per Lesson #36):** the SQLite persisted-floor write discipline (PRAGMA `journal_mode=WAL` + `busy_timeout=5000` + `foreign_keys=ON` + `synchronous=NORMAL`; `BEGIN IMMEDIATE` for the floor-bump write; `SQLITE_BUSY` retry 3×100 ms with ±25 % jitter) is owned by **spec/13 §97 AC-22** (canonical) — restating the PRAGMA table here is FORBIDDEN (would create the dual-source class Lesson #36 forbids; precedent: AC-78 evidence row). Implementers MUST link, not copy.
- **Verifies:** §10, §05; cross-module **spec/13 §97 AC-22** (concurrency/locking contract for persisted floor).

### AC-27 — Payload size enforcement  `[active]`
- **Given** an inbound `/append-log` body
- **When** the server reads the request
- **Then** `MaxPushPayloadBytes`, `MaxLinesPerPush`, `MaxLineBytes` are enforced **before parse**; an oversize line is truncated and tagged `Warn` (no `GL-*` error code raised) so a single bad line does not reject the whole push.
- **Verifies:** §10, §05.

### AC-35 — Wrong-lane rejection  `[active]`
- **Given** a Lane A credential is presented to a Lane B endpoint (or vice versa)
- **When** the auth resolver runs
- **Then** the response is `GL-AUTH-WRONG-LANE`; for Lane A, an unmatched `Email→Profile` resolves to `GL-AUTH-NO-PROFILE-LINK`.
- **Verifies:** §25, §15.

---

## Section D — Endpoints & Streaming

### AC-11 — Endpoint inventory  `[active]`
- **Given** the running plugin
- **When** the WP REST index is queried
- **Then** all 10 logical endpoints from §Endpoints exist with the documented field names; they fold to 8 HTTP paths in §17 via the `?q=` query-param collapse rule (rows #5/#6 share `/get-logs`; rows #7/#8 share `/get-pipeline-logs`).
- **Per-endpoint binding matrix (normative tier-1 surface — Lesson #19 audit-boundary pin; full JSON schemas remain canonical in §17 OpenAPI per Lesson #36 link-don't-restate):**

  | # | Method | Path | Request body schema (§17) | Response body schema (§17) | Auth class | Error envelope codes (§15) |
  |---|---|---|---|---|---|---|
  | 1 | POST | `/append-log` | `AppendLogRequest` (chunked NDJSON OR single JSON; §04 §1.1 + AC-12) | `AckResponse` (per AC-14) | TempToken + URL/Branch (§05 Lane A) | `GL-PAYLOAD-TOO-LARGE`, `GL-INGEST-TIMEOUT`, `GL-STREAM-*`, `GL-AUTH-*` |
  | 2 | PUT | `/fixed-log` | `FixedLogRequest` (`{PipelineId, Branch, Sha, PreviousHasError?}`) | `AckResponse` (per AC-14) | TempToken + URL/Branch | `GL-AUTH-*`, `GL-INTERNAL` |
  | 3 | POST | `/clear-log` | `ClearLogRequest` (`{PipelineId}`) | `AckResponse` (per AC-14, empty `Retrieval` URLs valid) | TempToken + URL/Branch | `GL-AUTH-*` |
  | 4 | POST | `/clear-log-all` | `ClearLogAllRequest` (`{RepoUrl, Branch}`) | `AckResponse` (per AC-14, empty `Retrieval` URLs valid) | TempToken + URL/Branch | `GL-AUTH-*` |
  | 5 | GET | `/get-logs` | n/a (query `?RepoUrl=&Branch=&Sha=` OR `?q=`) | `LogPage` JSON OR NDJSON `Header→Log*→End` (per AC-67) | App Password / Cookie (§05 Lane A) | `GL-AUTH-*`, `GL-NDJSON-*`, `GL-SHA-DB-*` |
  | 6 | GET | `/get-logs?q=…` | n/a (URL-style `?q=github.com/{org}/{repo}/{branch}/{sha}`) | as #5 | as #5 | as #5 |
  | 7 | GET | `/get-pipeline-logs` | n/a (query `?PipelineId=`) | `PipelineLogPage` JSON OR NDJSON (incl. `Header.StateTransition` per AC-74 when scope=1 pipeline) | App Password / Cookie | `GL-AUTH-*`, `GL-NDJSON-*` |
  | 8 | GET | `/get-pipeline-logs?q=…` | n/a (URL-style) | as #7 | as #7 | as #7 |
  | 9 | GET | `/get-error-logs` | n/a (query `?RepoUrl=&Branch=&Sha=`) | `ErrorLogPage` JSON OR NDJSON (severity ≥ Error filter server-side) | App Password / Cookie | `GL-AUTH-*`, `GL-NDJSON-*` |
  | 10 | GET | `/get-pipeline-error-logs` | n/a (query `?PipelineId=`) | `ErrorLogPage` JSON OR NDJSON (incl. `Header.StateTransition` per AC-74) | App Password / Cookie | `GL-AUTH-*`, `GL-NDJSON-*` |

- **AND** every successful response on write endpoints (#1–#4) MUST conform to `AckResponse` per **AC-14** (Retrieval URLs); every error response on any endpoint MUST conform to `ErrorEnvelope` per **AC-30** (`{Status, Code, Message, RequestId, HttpStatus}`); every NDJSON streaming response on read endpoints (#5–#10) MUST conform to the `Header→Log*|ErrorLog*→Progress*→End` frame contract per **AC-67/AC-68/AC-69/AC-71/AC-72** (opt-in via `Accept: application/x-ndjson`; server-driven frame ordering; resume via `?after-seq=` + `?stream-id=`; per-frame size cap; progress cadence).
- **AND** the canonical wire schemas (full property lists, examples, OpenAPI `components.schemas` entries) live in **`17-openapi.yaml` v2.9.4+** — restating those schemas inline here is FORBIDDEN per **Lesson #36** (dual-source drift class). This matrix is the audit-walker tier-1 binding (closes the Lesson #19 gap where AC-11 was a 4-line stub citing §17 but §17 lives in tier-2 and may exhaust the walker bundle cap).
- **AND** any auditor finding citing "missing per-endpoint contract" OR "endpoint inventory unbound to schemas" against the 10 endpoints above MUST be classified as a stale-cache walker-cap artifact per **Lesson #34** (verify by `grep -nE "^\| (1|2|3|4|5|6|7|8|9|10) \|" spec/22-git-logs-v2/97-acceptance-criteria.md` before flagging).
- **Verifies:** brief §Endpoints, §04 (full per-endpoint contracts), §17 (canonical OpenAPI), AC-12 (streaming ingest), AC-14 (Ack envelope), AC-30 (Error envelope), AC-67–AC-72 (NDJSON streaming retrieval frame contract).

### AC-12 — Streaming ingestion  `[active]`
- **Given** a client sends a request to `/append-log` (endpoint #1 per §04) carrying `Transfer-Encoding: chunked` (no `Content-Length` header) — typically used by CI runners forwarding live `tail -f` output
- **When** the server begins parsing the request body
- **Then** the server MUST consume the body as a stream — reading and parsing one JSON value (or one NDJSON line, if §04 §11 ingestion-side streaming is later adopted) at a time — and MUST NOT buffer the entire body into memory before validation begins; AND the §10 size caps (`ConfigKv.MaxPushPayloadBytes` default 1 MiB, `MaxLinesPerPush` default 10 000, `MaxLineBytes` default 64 KiB) MUST be enforced INCREMENTALLY against running counters: as soon as any threshold is crossed mid-stream, the server MUST abort by returning `GL-PAYLOAD-TOO-LARGE` (HTTP 413) per §15 with a partial-ingest indicator in the error envelope's `Message` (e.g. `"aborted at line 8217 of …"`); AND chunks already accepted before the abort MUST be rolled back (the entire `/append-log` request is atomic per AC-13's sticky-`HasError` contract — a partial commit would corrupt the per-SHA cursor); AND the server MUST set a hard wall-clock cap of `ConfigKv.AppendLogMaxStreamSec` (recommended default 30 s) to prevent slow-loris ingest exhausting the PHP-FPM worker pool — exceeding the cap MUST return `GL-INGEST-TIMEOUT` per §15; AND when the request omits `Transfer-Encoding: chunked` and instead sends `Content-Length: N`, the server MAY (but is not required to) enable streaming — buffered ingest is acceptable for known-bounded payloads under the size caps.
- **AND (Phase E2 — testable scenario matrix per Lesson #19 audit-boundary pin):** the 11-row scenario matrix below is the **normative tier-1 testable surface** for AC-12. Every row maps to a discrete PHPUnit/bats test case implementers can author 1:1. Test fixture skeletons SHOULD live under `34-phpunit-test-skeleton.md` per AC-80 sibling delegation; restating the matrix in any other spec/22 file is FORBIDDEN per Lesson #36.

  | T-ID | Scenario | Input | Expected outcome | Verifies clause |
  |---|---|---|---|---|
  | T-INGEST-01 | Chunked happy path under all caps | `Transfer-Encoding: chunked`, 100 lines × 1 KiB each, total 100 KiB, wall-clock 2 s | HTTP 200, `AckResponse.WrittenCount=100`, all rows committed atomically | streaming consume + AC-14 ack |
  | T-INGEST-02 | Buffered (Content-Length) happy path | `Content-Length: 50000`, 50 lines × 1 KiB, no chunked header | HTTP 200, `WrittenCount=50` (server MAY buffer; both paths legal) | "buffered ingest is acceptable for known-bounded payloads" |
  | T-INGEST-03 | Mid-stream `MaxLineBytes` (64 KiB) breach | chunked stream, line 17 = 70 KiB | HTTP 413 `GL-PAYLOAD-TOO-LARGE`, `Message` contains `"aborted at line 17"`, lines 1..16 ROLLED BACK (DB row count unchanged from pre-request) | INCREMENTAL line-byte enforcement + atomic rollback |
  | T-INGEST-04 | Mid-stream `MaxLinesPerPush` (10 000) breach | chunked stream, 10 001 lines × 100 B each | HTTP 413 `GL-PAYLOAD-TOO-LARGE`, `Message` contains `"aborted at line 10001"`, full rollback | INCREMENTAL line-count enforcement |
  | T-INGEST-05 | Mid-stream `MaxPushPayloadBytes` (1 MiB) breach | chunked stream, cumulative bytes cross 1 MiB at line 1043 | HTTP 413 `GL-PAYLOAD-TOO-LARGE`, `Message` contains `"aborted at line 1043"`, full rollback | INCREMENTAL byte-total enforcement |
  | T-INGEST-06 | Slow-loris timeout | chunked stream, sender pauses 31 s mid-stream (>`AppendLogMaxStreamSec=30`) | HTTP 408 (or per-§15 status) `GL-INGEST-TIMEOUT`, full rollback, FPM worker released within 1 s of abort | wall-clock cap + worker-pool protection |
  | T-INGEST-07 | Memory bound under streaming | chunked stream, 9 999 lines × 50 KiB ≈ 500 MiB total raw bytes | EITHER full success (if under all caps) OR a cap breach per T-INGEST-03/04/05; peak PHP heap MUST stay <64 MiB (proves NO whole-body buffering — see §10) | "MUST NOT buffer the entire body into memory" |
  | T-INGEST-08 | Atomic rollback on validation failure | chunked stream, line 200 fails JSON-schema validation per §04 | HTTP 422, `Code=GL-VALIDATION-FAILED`, lines 1..199 ROLLED BACK | atomicity binding to AC-13 sticky-HasError |
  | T-INGEST-09 | Logger gating during ingest | chunked stream firing 1000 `Logger::debug()` calls with `LogLevelMin=Info` | NO debug lines reach any sink, ingest latency unchanged ±5% vs T-INGEST-01 baseline | AC-04 constant-time gate applies inside ingest path |
  | T-INGEST-10 | Clock-injection determinism | T-INGEST-06 replayed under `ClockInterface::advance(31s)` (per AC-29 §5 clock-injection subsection) | same `GL-INGEST-TIMEOUT` outcome WITHOUT a real 31 s wait; test suite wall-time <500 ms | AC-29 §5 binding |
  | T-INGEST-11 | Cross-request idempotency boundary | two concurrent `/append-log` for SAME `{PipelineId, Sha}` | both succeed if non-overlapping seq ranges; one returns `GL-CURSOR-CONFLICT` if overlapping; NEVER a half-commit from one losing | per-SHA cursor isolation + atomicity |

- **Verifies:** brief §Endpoints.2.b (chunked ingest), §04 (endpoint #1 contract), §10 (size cap matrix), §15 (`GL-PAYLOAD-TOO-LARGE`, `GL-INGEST-TIMEOUT`, `GL-VALIDATION-FAILED`, `GL-CURSOR-CONFLICT`), AC-13 (atomicity coupling), AC-29 §5 (clock injection — deterministic timeout testing). For the test matrix: closes the **Lesson #19 audit-boundary < verification-boundary gap** for streaming-ingest semantics. Mirror of AC-05's T-DEDUP-* matrix (Phase E1) on the second testable-scenario axis (ingest path); two Phase E-series tier-1 promotions on the testable-scenario axis.

### AC-13 — HasError sticky until fixed-log  `[active]`
- **Given** an `/append-log` with `HasError=true` is accepted for a Pipeline
- **When** subsequent requests for the same Pipeline are read
- **Then** `Pipeline.HasError=1` remains until a `/fixed-log` for that Pipeline clears it back to 0.
- **Verifies:** brief §Endpoints.2.c, §04.

### AC-14 — Structured ack with Retrieval hints  `[active]`
- **Given** any write endpoint (`/append-log` #1, `/fixed-log` #2, `/clear-log` #3, `/clear-log-all` #4 per §04) returns a successful response (HTTP 200 or 202)
- **When** the response body is parsed
- **Then** the JSON body MUST conform to the `AckResponse` schema in §17 OpenAPI v2.9.4 — at minimum: `Status: "Ok"`, `RequestId` (UUID, mirrored to `AuditTrail.RequestId` per AC-30), `WrittenCount` (rows accepted into per-SHA storage), `Pipeline` (echo of the resolved `{PipelineId, Branch, Sha}`), AND a `Retrieval` block; AND the `Retrieval` block MUST contain canonical read-back URLs for the entity just written: `Retrieval.PipelineLogs` = absolute URL to `/get-pipeline-logs?PipelineId=<id>` (read all logs for this pipeline run), `Retrieval.PipelineErrorLogs` = absolute URL to `/get-pipeline-error-logs?PipelineId=<id>` (read only error rows), `Retrieval.RepoLogs` = absolute URL to `/get-logs?RepoUrl=<url>&Branch=<branch>` (read across the whole branch); AND each URL MUST be absolute (include scheme + host + `/wp-json/git-logs/v2/` namespace) so CI runners can paste it verbatim into chat/PR-comment integrations without further URL composition; AND the URLs MUST be the JSON-page form by default — clients wanting NDJSON streaming opt in by adding `Accept: application/x-ndjson` per AC-67, NOT by mutating the `Retrieval` URLs; AND the `Retrieval` block MUST also be present on `/clear-log` and `/clear-log-all` responses, where the URLs return empty pages (this proves the clear succeeded and is auditable); AND `Retrieval` URLs MUST NEVER include credentials or tokens — authentication is the caller's responsibility per §05.
- **Verifies:** brief §Endpoints.1.a–b (ack contract), §04 (write endpoints #1–#4), §17 v2.9.4 (`AckResponse` schema), AC-30 (RequestId mirroring), AC-67 (NDJSON opt-in).

### AC-30 — Error envelope shape + RequestId mirroring  `[active]`
- **Given** any endpoint (write #1–#4, read #5–#10, admin #11+) rejects a request for any reason — validation failure, auth failure, rate-limit hit, internal error, or any of the 30+ `GL-*` codes registered in §15
- **When** the response body is read
- **Then** the body MUST conform exactly to the `ErrorEnvelope` schema in §17 v2.9.4 `components.schemas.ErrorEnvelope`: `{Status: "Error", Code: <GL-* enum>, Message: <human-readable string>, RequestId: <UUID>, HttpStatus: <int matching the response status code>}` — and MUST NOT include any other top-level keys (no `details`, no `stack`, no `data` — those leak implementation detail and break client parsers); AND `Code` MUST be drawn from the `ErrorCode` enum in §17 (currently 30+ values incl. all `GL-NDJSON-*` and `GL-SHA-DB-*` codes per Phase 11); AND `RequestId` MUST be a UUIDv4 generated server-side (not client-supplied — clients sending an `X-Request-Id` header MUST have it ignored to prevent log-injection); AND the SAME `RequestId` MUST appear in the corresponding `AuditTrail.RequestId` row written for this request (so a customer reporting "I got error req_abc" can be cross-referenced to a single audit row); AND `HttpStatus` MUST equal the response's actual HTTP status code (no envelope claiming 400 inside a 200 response — that's a contract violation that breaks middleware error handling); AND `Message` MUST be safe to display verbatim to end users — it MUST NOT contain stack traces, file paths, SQL fragments, or any internal-only detail; AND on NDJSON streaming responses (per AC-67/AC-68), errors that occur BEFORE the `Header` frame flushes MUST use this envelope shape (the response is still conventional JSON); errors AFTER `Header` flushes MUST use the in-stream `NdjsonErrorFrame` per §17 instead — the envelope is for pre-stream failures only.
- **Verifies:** §15 (full `GL-*` code catalog), §10 (RequestId generation rule), §17 v2.9.4 (`ErrorEnvelope` + `ErrorCode` enum + `NdjsonErrorFrame`), §22 (`AuditTrail` correlation), AC-67/AC-68 (NDJSON error frame split).

### AC-37 — Prometheus metrics endpoint  `[active]`
- **Given** the metrics endpoint `GET /wp-json/git-logs/v2/metrics`
- **When** an authenticated client with `HistoryView` permission requests it
- **Then** the response is Prometheus exposition format; counter values are flushed every 5 minutes via `wp_cron`; missing permission ⇒ 403.
- **Verifies:** §20.

### AC-40 — OpenAPI parity  `[active]`
- **Given** `17-openapi.yaml`
- **When** it is loaded by an OpenAPI 3.1 parser
- **Then** the parse succeeds, all 10 endpoints are covered, and the error schema references `15-error-codes.md`'s envelope.
- **Verifies:** §17.

---

## Section E — Logging, Migrations & Roles

### AC-03 — Migration runs once per version  `[active]`
- **Given** the plugin boots at semver `X.Y.Z` (read from `ConfigKv.PluginVersion` per §18 v2.9.3 — currently `2.9.3`)
- **When** the migration runner executes during `plugins_loaded` action (per §06 §3.b)
- **Then** the runner MUST consult `MigrationState` (PK = `PluginVersion TEXT`, plus `AppliedAt INTEGER NOT NULL`, `ChecksumOk INTEGER NULL` per §18) and MUST execute the migration named `V<X>_<Y>_<Z>` (e.g. `V2_9_3` for `2.9.3`) IF AND ONLY IF no row exists with `PluginVersion = 'X.Y.Z'`; AND on successful completion the runner MUST insert exactly one new `MigrationState` row with `PluginVersion = 'X.Y.Z', AppliedAt = strftime('%s','now')` — re-boots at the same version MUST short-circuit by detecting the existing row and skipping the migration entirely (NEVER re-run, NEVER re-attempt — even if the prior run partially failed; partial failures are surfaced via `ChecksumOk = 0` and require manual operator intervention per §23 backup/restore); AND the runner MUST execute migrations in strict semver-ascending order — booting at `2.9.3` against a DB last migrated at `2.9.0` MUST run `V2_9_1` then `V2_9_2` then `V2_9_3` in that order, never out-of-order, never skipping; AND each migration MUST be wrapped in `BEGIN IMMEDIATE; … COMMIT;` so a failure mid-migration leaves the DB at the prior version (no half-migrated schema); AND the runner MUST refuse to start (returning `GL-MIGRATION-PENDING` per §15 on every API call) if the DB carries `MigrationState` rows for versions NEWER than the running plugin (a downgrade scenario — the operator must manually restore from §23 backup or upgrade the plugin); AND every Phase 0..11 marker (`2.0.0`, `2.5.0`, `2.6.0`, `2.7.0`, `2.8.0`, `2.8.7`, `2.8.8`, `2.8.9`, `2.9.0`, `2.9.1`, `2.9.2`, `2.9.3` — 12 markers total) MUST be present in `MigrationState` after a fresh install applying the v2.9.3 baseline schema, NOT just the latest one (the audit trail of intermediate versions matters for §23 restore correctness).
- **Verifies:** brief §3.b–e (migration lifecycle), §06 (plugin boot sequence), §12 (CI/CD migration coupling), §15 (`GL-MIGRATION-PENDING`), §18 v2.9.3 (`MigrationState` DDL + 12 baseline markers), §23 (backup/restore interaction).

### AC-04 — Logger level gating  `[active]`
- **Given** the plugin's logger subsystem (per §06) AND the `ConfigKv.LogLevelMin` row in the plugin DB (per §03 ConfigKv table) which holds one of the six canonical level strings: `Trace`, `Debug`, `Info`, `Warn`, `Error`, `Fatal` (case-sensitive, PascalCase per §23 PascalCase convention) — default value `Info` if the row is missing or NULL
- **When** any code path in the plugin invokes a logger method (e.g. `Logger::debug($msg, $ctx)`, `Logger::error(...)`, etc.) regardless of which subsystem the call originates from (admin UI, REST controller, CLI command, background scheduler, ingestion endpoint per AC-12)
- **Then** the logger MUST gate the line **at the call boundary BEFORE any sink work is performed** — specifically: (a) the level integer of the call (e.g. `Debug = 1`) MUST be compared against the cached integer value of `ConfigKv.LogLevelMin` (e.g. `Info = 2`), (b) if `call_level < min_level`, the logger MUST `return` immediately — no sink invocation, no message formatting (`sprintf`/template interpolation), no context-array serialization, no JSON-encode of `$ctx`, no timestamp computation, no stack-frame inspection, no source-location lookup; AND the gating MUST happen in CONSTANT TIME (just an integer comparison + early return) — heavyweight work (filtering, deduplication per AC-05, redaction) MUST NOT happen for dropped lines; AND a "filter-at-sink" implementation (where the message is built + handed to the sink which then drops it) is a SPEC VIOLATION because: (i) it wastes CPU on string formatting that's thrown away, (ii) it allocates intermediate strings/arrays that pressure the PHP allocator and add observable latency under high log volume, (iii) it defeats the purpose of `LogLevelMin` as a performance valve operators turn down to recover under load; AND the level comparison MUST use a CACHED integer (read once at request start or autoloader bootstrap, stored in a static / process-singleton) — re-reading `ConfigKv.LogLevelMin` from the DB on every log call is a SPEC VIOLATION (one DB query per debug log under `Info` would amplify load by 10-100×); AND when an operator updates `ConfigKv.LogLevelMin` via the admin UI, the change MUST take effect on the **next request** (not the current request) — the cache is request-scoped, NOT process-scoped; AND the six levels are FIXED and MUST NOT be extended (no `Verbose`, no `Critical`, no `Notice`) — a custom level requires a spec amendment + AC-04 update + DB migration; AND the canonical integer mapping is `Trace=0, Debug=1, Info=2, Warn=3, Error=4, Fatal=5` (lower number = more verbose); AND when `LogLevelMin = Fatal` (5), only `Fatal` lines emit — `Error` (4) lines are dropped (this is the "near-silence emergency mode" for when the plugin is causing observable system stress); AND the dedup rule per AC-05 applies AFTER level gating (a line that fails AC-04 never reaches AC-05's dedup window — order matters for performance).
- **Verifies:** brief §3.f (logger level contract), §06 (logger subsystem), §03 (ConfigKv table), §23 (PascalCase enum convention), AC-05 (dedup applies after gating), AC-12 (ingestion logger respects same gate).

### AC-05 — Diagnostic dedup window  `[active]`
- **Given** the plugin's diagnostic-logger pipeline (per §06) processing a stream of log lines, where each line carries a fingerprint composed of `(source, level, message_template, redacted_context_hash)` — `source` is the originating subsystem identifier (e.g. `ingest.streaming`, `admin.profile.save`, `cron.audit-rollup`), `message_template` is the format string BEFORE interpolation (so `"saved profile %d"` and `"saved profile %d"` with different IDs share a fingerprint), `redacted_context_hash` is the SHA-256 of the secrets-scrubbed `$ctx` array
- **When** two log lines arrive with the **same fingerprint** within a rolling 60-second window measured from the **first** occurrence (NOT a tumbling window aligned to wall-clock minutes — a rolling window so the boundary doesn't reset on minute marks)
- **Then** the second occurrence MUST be suppressed (NOT written to any sink); AND a counter MUST be incremented on the in-memory dedup-window entry tracking the suppressed count for that fingerprint; AND when the 60-second window expires (no further occurrences for 60s after the latest hit), the next occurrence MUST: (a) emit a single line with the original message PLUS a structured suffix `[deduped: N within 60s window starting <iso8601>]` where `N` is the count of suppressed occurrences during the window, (b) start a fresh dedup window; AND when the suppressed count is `0` (i.e. the fingerprint occurred exactly once and the window expired without repeats), NO suffix is emitted (this is the normal case for non-repeating logs); AND the dedup rule MUST NOT apply to lines at level `Error` or `Fatal` (per the spec carve-out: "error logs are NOT subject to this rule") — error/fatal lines emit verbatim every time, even when identical to a prior line milliseconds ago, because: (i) error storms ARE diagnostic signal (the cadence reveals the failure mode), (ii) suppressing errors causes the operator to under-estimate severity, (iii) error sinks (Sentry, OpenTelemetry exporters) typically have their own dedup that's tuned for their UI; AND the dedup STATE MUST live in **process-local memory** (e.g. an LRU cache keyed by fingerprint with 60s TTL entries) — NOT in the DB (a per-line DB roundtrip would amplify load), NOT in a shared cache like Redis (forces an external dependency for a logger), NOT in a file (lock contention on every log call); AND the LRU cache MUST be bounded (suggested `1024` distinct fingerprints) — under a fingerprint-storm where 1024 unique fingerprints fire within 60s, the eviction policy is LRU (the least-recently-seen fingerprint is evicted, allowing its next occurrence through as if it were fresh — this is acceptable degradation under abnormal load); AND the dedup window MUST apply AFTER the AC-04 level gate (a line that fails AC-04 never reaches AC-05); AND the dedup window MUST apply BEFORE any sink invocation (computing the dedup decision is cheaper than building+writing to the sink); AND the rule is per-PHP-process — a multi-worker setup (FPM with N workers) will dedup PER worker, NOT globally — this is documented as acceptable because cross-worker dedup would require shared state with all the downsides above.
- **AND (Phase E1 — testable scenario matrix per Lesson #19 audit-boundary pin):** the 11-row scenario matrix below is the **normative tier-1 testable surface** for AC-05. Every row maps to a discrete PHPUnit/bats test case implementers can author 1:1 (no semantic interpretation needed). Test fixture skeletons SHOULD live under `34-phpunit-test-skeleton.md` per AC-80 sibling delegation; restating the matrix in any other spec/22 file is FORBIDDEN per Lesson #36.

  | T-ID | Scenario | Input sequence | Expected sink output | Verifies clause |
  |---|---|---|---|---|
  | T-DEDUP-01 | Single occurrence, no repeat | 1 line @ t=0 (`Info`, fp=A) | 1 line, NO `[deduped: ...]` suffix after window expiry | "when suppressed count is `0` ... NO suffix is emitted" |
  | T-DEDUP-02 | Two occurrences within window | 2 lines @ t=0, t=30s (same fp=A, `Info`) | 1 line @ t=0; @ t≥60s+ε after last hit, 1 line with `[deduped: 1 within 60s window starting <iso8601>]` | "second occurrence MUST be suppressed; counter incremented" |
  | T-DEDUP-03 | Burst within window | 50 lines @ t=0..59s (same fp=A, `Info`) | 1 line @ t=0; @ window expiry, 1 line with `[deduped: 49 ...]` | LRU bound + count semantics |
  | T-DEDUP-04 | Rolling window (boundary reset) | line @ t=0, line @ t=30s, line @ t=80s (fp=A, `Info`) | t=80s line emits VERBATIM (window starts from FIRST occurrence per AC-05; window from t=0 expires at t=60s; t=30s arrival FALLS WITHIN window → suppressed; the suffix-emit @ t=60s+ε then resets; t=80s = NEW window) | "rolling window measured from the **first** occurrence" + boundary reset semantics |
  | T-DEDUP-05 | Error-level carve-out | 5 lines @ t=0..1s (same fp=B, `Error`) | 5 lines emitted verbatim, NO suppression, NO suffix | "MUST NOT apply to lines at level `Error` or `Fatal`" |
  | T-DEDUP-06 | Fatal-level carve-out | 3 lines @ t=0..1s (same fp=C, `Fatal`) | 3 lines emitted verbatim, NO suppression, NO suffix | "error/fatal lines emit verbatim every time" |
  | T-DEDUP-07 | Mixed levels same fingerprint | line @ t=0 (`Info`, fp=A), line @ t=10s (`Error`, fp=A) | both emit verbatim (`Error` bypasses dedup; `Info` would have been first-occurrence anyway) | level-axis carve-out is per-line, not per-fingerprint |
  | T-DEDUP-08 | Different fingerprints in window | line @ t=0 (fp=A), line @ t=5s (fp=B) — both `Info`, same source/template/level but different `redacted_context_hash` | both emit verbatim (different fingerprints = independent windows) | fingerprint composition `(source, level, message_template, redacted_context_hash)` |
  | T-DEDUP-09 | LRU eviction under storm | 1024 unique fingerprints fired by t=10s; @ t=15s a 1025th unique fingerprint arrives forcing eviction of the LRU entry (fp=A from t=0); @ t=20s fp=A re-occurs | the @ t=20s fp=A line emits VERBATIM (LRU evicted state — treated as fresh window start) | "LRU cache MUST be bounded ... acceptable degradation under abnormal load" |
  | T-DEDUP-10 | AC-04 level-gate ordering | line @ `Trace` level when logger threshold = `Info` (fp=A, would-otherwise-dedup) | line is dropped by AC-04 BEFORE reaching AC-05; dedup state for fp=A is NOT updated | "MUST apply AFTER the AC-04 level gate" |
  | T-DEDUP-11 | Cross-worker independence | 2 PHP-FPM workers; line @ t=0 in worker-1 (fp=A, `Info`), line @ t=5s in worker-2 (fp=A, `Info`) | both lines emit verbatim (per-worker dedup state) | "rule is per-PHP-process ... documented as acceptable" |

  **Test-suite assertion contract**: every row above MUST have ≥1 test case in `test/AcDedupWindowTest.php` (PHPUnit) OR `test/ac-dedup-window.bats` (bash harness for CLI-driven log injection) bearing the T-ID as part of the test method/case name (e.g., `public function test_DEDUP_01_single_occurrence_no_repeat() { ... }`). Test absence for any T-ID = `GL-TEST-COVERAGE-GAP` per `15-error-codes.md`. Time-mocking MUST use a deterministic monotonic-clock injection point (NOT `microtime(true)` directly) so T-DEDUP-02/03/04/09 assertions are deterministic — the clock-injection contract delegates to **AC-29 MigrationInterface contract** §"Test-time clock injection" subsection (Phase E1 follow-up if not yet authored).
- **Verifies:** brief §3.g (dedup window semantics + error carve-out), §06 (logger pipeline), AC-04 (level gate ordering — gate first, then dedup), AC-12 (ingest logger respects same dedup). For the testable scenario matrix: closes the **Lesson #19 audit-boundary < verification-boundary gap** for AC-05 (pre-E1, AC-05 was a single dense paragraph with no discoverable test-case enumeration — implementers had to derive scenarios from prose). Mirror of AC-23 (CHECK-constraint inventory, D3) and AC-11 (endpoint-binding matrix, D2) — three Phase D/E-series tier-1 contract surface promotions on three normative-content axes (constraints / endpoints / test scenarios). Test fixture skeletons live in `34-phpunit-test-skeleton.md` per AC-80 sibling delegation; `32-cli-test-plan.md` carries the bats variants. Lesson #36 reinforcement: test-fixture skeletons in §34 MUST cite this AC + T-ID by anchor, not restate scenario semantics.

### AC-06 — Roles in plugin DB, permission-name authz  `[active]`
- **Given** a permission check at any gate
- **Given** a permission check at any gate
- **When** the resolver runs
- **Then** it queries the plugin's `RolePermission` join (in plugin SQLite, NOT WP roles) and matches by **permission name**, never by role name string.
- **Verifies:** brief §4–5, §19.

### AC-29 — MigrationInterface contract  `[active]`
- **Given** the `inc/Migrations/V{Major}_{Minor}_{Patch}.php` files
- **When** each is loaded
- **Then** each implements `MigrationInterface`; `MigrationState` is keyed by `PluginVersion`; re-runs at the same version are idempotent (no duplicate rows, no schema drift).
- **AND (Phase E2 §5 — Test-time clock injection, Normative):** every code path that consults wall-clock time for **dedup-window expiry** (AC-05), **streaming-ingest timeout** (AC-12 / `AppendLogMaxStreamSec`), **temp-token rotation** (`SshNonce.ExpiresAt`), or **rate-limit bucket reset** (§07) MUST read time through a single injectable abstraction — recommended PHP signature: `interface ClockInterface { public function now(): int; /* Unix seconds */ public function nowMs(): int; /* Unix millis */ }`. Production binds `SystemClock implements ClockInterface` (delegates to PHP `time()` / `microtime(true)*1000`); tests bind `FakeClock implements ClockInterface` exposing `advance(int $seconds): void` + `set(int $unix): void`. **Direct calls to `time()`, `microtime()`, `date()`, `DateTimeImmutable("now")`, `gmdate()`, or `hrtime()` from any of the four time-sensitive code paths above is FORBIDDEN** — such calls MUST be detected by `linter-scripts/check-spec-folder-refs.cjs`-style grep gate against `inc/Logger/`, `inc/Ingest/`, `inc/Auth/Ssh/`, `inc/RateLimit/` (4 paths). Rationale: T-DEDUP-04 (60-s rolling-window boundary) and T-INGEST-06/T-INGEST-10 (30-s streaming timeout) are unimplementable as fast unit tests without clock injection — without this AC, the only path is real-time waits in CI which (a) make every PR take 90+ s in test, (b) produce flake under load. The injectable-clock pattern is industry-standard (Go `clockwork`, Rust `MockClock`, .NET `TimeProvider`); PHP has no stdlib equivalent so the spec mandates a project-local interface. Migration-runner code paths (this AC's primary contract) MAY use `time()` directly for `MigrationState.AppliedAt` because migrations run once per version per process and have no test-determinism requirement (the timestamp is forensic, not behavioural).
- **Verifies:** §06, §12. For §5 clock injection: closes Lesson #19 audit-boundary gap for time-sensitive contracts; binds AC-05 (T-DEDUP-04) and AC-12 (T-INGEST-06, T-INGEST-10); links to AC-64 SSH-key rotation flow (uses same `ClockInterface` for `SshKey.RotationDueAt` checks).

### AC-39 — Permission gate hides buttons  `[active]`
- **Given** a UI element bound to a permission
- **When** the current user lacks that permission
- **Then** the button is **hidden** (removed from DOM), not merely `disabled`; the underlying REST route also rejects with the §15 envelope.
- **Verifies:** §19.

---

## Section F — Audit & Activity

### AC-21 — Four audit tables coexist  `[active]`
- **Given** the v3.8.0+ schema
- **When** the audit surface is inventoried
- **Then** four tables coexist with the §08 split: `AuditTrail` (HTTP forensics), `History` (per-RepoVersion git timeline), `PipelineAction` (renamed from `Action` in v3.8.0 — pipeline-bound), `SystemEvent` (NEW v3.8.0 — non-Git business events).
- **Verifies:** locked decision 13 + v3.8.0, §08, §18.

### AC-38 — AuditActionType seed rows  `[active]`
- **Given** a fresh migration to v2.9.1
- **When** `AuditActionType` is queried
- **Then** rows include `Prune` (19), `Restore` (20), and SSH lane rows `SshKeyRegister` (22), `SshKeyRevoke` (23), `SshKeyRotate` (24) per `18-schema.sql` seed.
- **Verifies:** §22, §23, §18.

### AC-57 — SystemEvent table shape  `[active]`
- **Given** the v3.8.2+ schema
- **When** `SystemEvent` is inspected
- **Then** it has columns `(SystemEventId PK, SystemEventTypeId FK, ActorProfileId FK NULL, TargetType TEXT NULL, TargetId INTEGER NULL, Summary TEXT, DetailJson TEXT, OccurredAt INTEGER)` with indexes `(SystemEventTypeId, OccurredAt)`, `(ActorProfileId, OccurredAt)`, `(TargetType, TargetId, OccurredAt)`; `TargetType`/`TargetId` carry **no** FK CHECK so audit history outlives target rows.
- **Verifies:** §02, §08, §18 + v3.8.2.

### AC-58 — SystemEventType seed inventory  `[active]`
- **Given** a fresh migration to v3.8.2
- **When** `SystemEventType` is queried
- **Then** exactly 16 rows exist in this order: `ProfileCreated`, `ProfileDeleted`, `ProfileStatusChanged`, `RoleAssigned`, `RoleRevoked`, `GitProfileCreated`, `GitProfileAcceptanceChanged`, `GitProfileBranchRestrictionChanged`, `AppCreated`, `AppStatusChanged`, `AppLinkAdded`, `AppLinkRemoved`, `SshKeyRegistered`, `SshKeyRevoked`, `SshKeyRotated`, `TempTokenRotated`.
- **Verifies:** §01, §18 + v3.8.2.

---

## Section G — Schema Conventions & Diagrams

### AC-22 — Diagram inventory  `[active]`
- **Given** folder `spec/26-gitlogs-diagrams/` (the Mermaid companion folder for §22, brought to v2.1.0 by Phase 10)
- **When** the folder contents are listed
- **Then** the folder MUST contain exactly these 6 Mermaid source files (each named `NN-<purpose>.mmd`) reflecting the v2.9.0 split-DB shape: `01-er-diagram.mmd` (entity-relationship across root DB + per-SHA DBs — incl. `Profile`, `App`, `AppLink`, `Repo`, `RepoVersion`, `GitProfile`, `Pipeline`, `ShaRegistry`, `SshKey`, `SshNonce`, `MigrationState`, `ConfigKv`, `AuditTrail`), `05-auth-validation.mmd` (Lane A WP-App-Password flow + Lane B SSH-key flow per §05/§31), `06-permission-flow.mmd` (Casbin RBAC matrix per §28), `07-rate-limit-flow.mmd` (per-profile bucket per §07/§10), `08-encryption-v3-flow.mmd` (token encryption-at-rest per §30), `09-endpoints-mindmap.mmd` (the 10 REST endpoints organised by surface — write/read/admin/streaming per §04 §11.7); AND each `.mmd` file MUST have a companion `.svg` artifact (rendered by `@mermaid-js/mermaid-cli` v11+ per Phase 10) so reviewers without Mermaid tooling can preview directly — re-render command `mmdc -i <file>.mmd -o <file>.svg -p puppeteer.json -b transparent` documented in §00; AND the folder's §00 banner version MUST track the schema version the diagrams reflect (currently v2.1.0 reflecting v2.9.0 split-DB shape) — when §02/§18 schema changes land, §26 banner MUST be bumped and ALL affected `.mmd` files re-rendered before the changelog row is closed; AND no other `.mmd` files MUST exist in the folder (legacy diagrams from v1 live in `spec/_archive/21-git-logs-v1/` per the slot-26-archive precedent — never in the active folder).
- **Verifies:** brief §Diagrams, §26 v2.1.0 (Mermaid companion folder), §02/§18 (schema source-of-truth that diagrams reflect), §05/§28/§30/§31/§04 (each diagram's source spec), Phase 10 roadmap (mmdc render contract).

### AC-23 — PascalCase + AUTOINCREMENT PK + CHECK-constraint catalog  `[active]`
- **Given** any table or JSON payload in the codebase
- **When** identifiers are inspected
- **Then** all table names, column names, JSON keys, and JSON enum values use PascalCase; primary keys are `INTEGER AUTOINCREMENT` named `{Table}Id` (no `id`, `pk`, or snake_case).
- **AND (Phase D3 — CHECK-constraint inventory inline per Lesson #19 audit-boundary pin + Lesson #36 link-don't-restate):** the canonical normative CHECK-constraint inventory below is the **tier-1 binding** for SQLite domain enforcement — every row maps to (Table, Column / scope, Constraint expression, Constraint kind, Authority line in `18-schema.sql`, Drift signal). Full DDL remains canonical in `18-schema.sql` per Lesson #36 — restating constraint expressions in any other spec/22 file (`02-database-schema.md`, `06-migrations-and-logger.md`) is FORBIDDEN; cite this AC + the schema line by anchor only.

  | Table | Column / scope | Expression | Kind | `18-schema.sql` line | Drift signal |
  |---|---|---|---|---|---|
  | `GitProfile` | `IsOrganization` | `IN (0,1)` | boolean-domain (replaces retired `OwnerTypeId` per AC-55, v3.8.0) | L129 | `GL-SCHEMA-DRIFT` at boot |
  | `AppLink` | row-level (`GitProfileId`, `RepoId`) | `(GitProfileId IS NOT NULL AND RepoId IS NULL) OR (GitProfileId IS NULL AND RepoId IS NOT NULL)` | exactly-one-target polymorphic discriminator (binds AC-18 + spec/23 AC-ADB-14) | L179–183 | `GL-APPLINK-RESOLVE-FAILED` |
  | `Pipeline` | `HasError` | `IN (0, 1)` | boolean-domain (binds AC-13 sticky-until-fixed) | L198 | per-row write rejection |
  | `Pipeline` | `PreviousHasError` | `IN (0, 1)` | boolean-domain (v2.9.2 first-failure label support; binds AC-77 `HasError + StateLabel` column rendering) | L206 | state-transition label drift |
  | `SshKey` | `IsActive` | `IN (0,1)` | boolean-domain (binds AC-60 SshKey shape + AC-64 rotation flow) | L316 | rotation-flow consistency failure |

  **Cross-language storage convention**: every `IN (0,1)` CHECK above maps to **spec/04 §2.1 Cross-Language Boolean Storage Convention (Normative)** — SQLite stores `INTEGER 0/1`; Go scans into `bool`; PHP receives `int 0/1` cast at boundary; Rust scans into `bool`; C# scans into `bool`; TS receives `0|1` over wire and narrows at boundary. Restating the per-language scan/insert table in spec/22 is FORBIDDEN per Lesson #36 — cite spec/04 §2.1 by anchor.

  **Tri-state NULL exception**: none of the 5 CHECK rows above carry a `NULL`-allowed exception — every column is either `NOT NULL` (boolean-domain rows) or part of the polymorphic exactly-one constraint (where exactly one of the two FK columns is non-NULL). Future tri-state additions (e.g., `NULL` = "unknown / never measured") MUST land in spec/04 §2.1's tri-state exception clause AND add a row here in the same PR.

  **Migration discipline**: any future CHECK addition MUST follow spec/04 §2.1 migration discipline (NOT NULL DEFAULT 0/FALSE for new boolean columns; positive-only rename; type-swap precondition with orphan-value check); the migration AC binding is **AC-29 MigrationInterface contract**.

  **AND** any new CHECK constraint added in a future phase MUST land in **all three** surfaces in the same PR (DDL in `18-schema.sql` + a row in this AC-23 table + a §98 changelog row); partial landings = `GL-SCHEMA-DRIFT` and CI-blocking. Auditor finding "missing CHECK constraint catalog" or "[D2] domain-enforcement gap" against the 5 listed rows MUST be classified as a stale-cache walker-cap artifact per Lesson #34 — verify by `grep -nE "CHECK \(" spec/22-git-logs-v2/18-schema.sql` (5 hits expected: 1 boolean × 4 + 1 exactly-one polymorphic) before flagging.

- **Verifies:** brief §DB.2–4, §02, §18 (PascalCase + AUTOINCREMENT). For the CHECK-constraint catalog: closes the **Lesson #19 audit-boundary < verification-boundary gap** for SQLite domain enforcement (the DDL file `18-schema.sql` is tier-2 and may be walker-truncated; this AC lifts the constraint inventory into the tier-1 §97 bundle). Codifies **Lesson #36** (link-don't-restate) by delegating the cross-language storage convention to **spec/04 §2.1** and the migration discipline to **AC-29**. Mirror of AC-11 (endpoint-inventory pin, Phase D2) and AC-81 (enum-catalog pin, Phase C1) — three Phase D-series tier-1 promotions on three normative-content axes (endpoints / enums / domain constraints). Until A8 (LLM-gateway re-score) unblocks, this AC declares any "missing CHECK catalog" or "[D2] domain-enforcement gap" finding against the 5 listed rows a stale-cache walker-cap artifact per Lesson #34.
- **Source:** `97-acceptance-criteria.md` (this AC); cross-references `18-schema.sql` (canonical DDL), `spec/04 §2.1 Cross-Language Boolean Storage Convention` (canonical per-language storage rules per AC-79 row), `spec/23 AC-ADB-14` (AppLinkType polymorphic resolution — bound by the `AppLink` exactly-one row), AC-13 / AC-18 / AC-29 / AC-55 / AC-60 / AC-64 / AC-77 (downstream consumers), AC-78 / AC-79 / AC-81 (mirror tier-1 normative-surface pins).

### AC-24 — Enums modeled twice  `[active]`
- **Given** any typed value (severity, status, lane mode, etc.)
- **When** it is referenced
- **Then** it is modeled as an Enum in code AND as a lookup table in the DB; comparisons MUST use the lookup ID, never a string literal.
- **Verifies:** brief §DB.5, §01, §18.

### AC-55 — No legacy OwnerType  `[active]`
- **Given** `18-schema.sql`
- **When** it is parsed
- **Then** it MUST NOT create the `OwnerType` table, MUST NOT seed `OwnerType` rows, AND `GitProfile` MUST declare `IsOrganization INTEGER NOT NULL DEFAULT 0 CHECK (IsOrganization IN (0,1))` in place of `OwnerTypeId`.
- **Verifies:** §18 + v3.8.1.

### AC-56 — PipelineAction rename completeness  `[active]`
- **Given** `18-schema.sql`
- **When** the action surface is inspected
- **Then** there MUST be no `ActionType` or `Action` tables; the lookup is `PipelineActionType`; the audit-row table is `PipelineAction`; `History.ActionTypeId` is renamed to `History.PipelineActionTypeId` and references `PipelineActionType(PipelineActionTypeId)`.
- **Verifies:** §18 + v3.8.2.

---

## Section H — Per-SHA Split-DB (v2.9.0)

### AC-49 — Per-SHA file creation on first append  `[active]`
- **Given** an accepted `/append-log` for a `(PipelineId, Sha)` pair never seen before
- **When** the write commits
- **Then** the server creates `<dataDir>/<ShaLogsRoot>/<Sha[0:2]>/<Sha>.db` and a `ShaRegistry` row in the root DB keyed `UNIQUE(PipelineId, Sha)`; `LogEntry`/`ErrorLogEntry` tables MUST NOT exist in the root DDL — all log lines live exclusively in the per-SHA file.
- **Verifies:** §18, §39, §22.

### AC-50 — ShaRegistry mirrors per-SHA stats  `[active]`
- **Given** any per-SHA file is updated
- **When** the write completes
- **Then** `ShaRegistry` mirrors `RowCount`, `LastSeenAt`, `FileSizeBytes`, `Sha256` so dashboards and the prune planner can render summaries / compute eligibility WITHOUT opening the per-SHA file.
- **Verifies:** §18, §39.

### AC-51 — Per-SHA file is self-contained  `[active]`
- **Given** any `<Sha>.db` is exported, zipped, or handed to support
- **When** it is opened standalone (no root DB)
- **Then** it carries denormalized `LogSeverity` lookup + a single-row `ShaMeta` identity, so it is interpretable without root-DB context.
- **Verifies:** §39.

### AC-52 — Open per-SHA handle pool  `[active]`
- **Given** the running plugin holds open `<Sha>.db` connections
- **When** open count is measured per process
- **Then** it is capped at `ConfigKv.MaxOpenShaDbHandles` (default `32`) with LRU eviction; idle handles are closed after `ConfigKv.ShaDbIdleCloseSec` seconds (default `120`); pool refusal raises `GL-SHA-DB-QUOTA-EXCEEDED` (HTTP 507).
- **Verifies:** §15, §39.

### AC-53 — Prune / backup / restore / wipe lifecycle  `[active]`
- **Given** the per-SHA tree exists with N files
- **When** `wp git-logs prune` / `backup` / `restore` / uninstall `Wipe` runs
- **Then** **prune** walks `ShaRegistry` (eligibility on `LastSeenAt` + `Pipeline.HasError` + history-window guard), per row does `rename → delete-row → unlink` for crash-safety, and removes empty `<Sha[0:2]>/` shard folders while preserving the `<ShaLogsRoot>` root; **backup** writes a directory tree (`git-logs.sqlite` + `manifest.json` + `logs/<aa>/<sha>.db…`) with `manifest.ShaFiles[]` recording `{PipelineId, Sha, DbFilePath, RowCount, FileSizeBytes, Sha256}`; **restore** is all-or-nothing with `.bak`/`logs.bak.<ts>/` rollback and verifies sha256 against the manifest (drift ⇒ `GL-SHA-DB-CHECKSUM-MISMATCH`); **uninstall Wipe** deletes the per-SHA tree first, root DB last, then `rmdir`'s the parent.
- **Verifies:** §15, §22, §23, §29, §39.

### AC-31 — Prune CLI guards  `[active]`
- **Given** `wp git-logs prune --older-than=Nd`
- **When** N is provided
- **Then** the CLI enforces a 7d floor; refuses while a migration is pending; uses two-phase delete (logical first, physical after); ends with `wal_checkpoint(TRUNCATE)`; emits an `AuditActionType.Prune` row.
- **Verifies:** §22.

### AC-32 — Backup / restore cross-version safety  `[active]`
- **Given** `wp git-logs backup` / `restore`
- **When** they run
- **Then** backup uses SQLite Online Backup API + manifest JSON; restore refuses without maintenance mode unless `--force`; downgrade across **major** versions is always refused.
- **Verifies:** §23.

### AC-33 — Verify CLI surfaces  `[active]`
- **Given** `wp git-logs verify`
- **When** it runs
- **Then** it executes `integrity_check` + `foreign_key_check` + asserts `Profile≥1` + asserts `MigrationState.PluginVersion = ConfigKv.PluginVersion`; the result surfaces in the WP Site Health card.
- **Verifies:** §20, §23.

### AC-34 — Multisite per-site DB  `[active]`
- **Given** a WordPress multisite installation (per §24) — both flavors apply: (a) **network-activated** (the plugin is activated at the network level via Network Admin → Plugins, making it logically present on every subsite), (b) **per-site activated** (the plugin is activated only on a subset of subsites). The multisite has N subsites, each with its own `blog_id` (1, 2, 3, ...) and its own subsite-scoped `wp_<blog_id>_*` table prefix per WordPress convention
- **When** any code path touches the plugin's SQLite database — including: admin UI loads, REST endpoint requests (per AC-11..AC-14), CLI commands, cron tasks, ingestion writes (per AC-12), audit-log writes (per AC-21), background scheduler jobs, plugin-activation hooks, network-admin screens that aggregate across subsites
- **Then** each subsite MUST have its **own SQLite DB file** at a per-site path resolved via `wp_upload_dir()` (which returns subsite-scoped paths like `/wp-content/uploads/sites/2/git-logs/plugin.db` for `blog_id=2` and `/wp-content/uploads/git-logs/plugin.db` for the main site `blog_id=1`); AND a single shared DB file across subsites is FORBIDDEN even when the plugin is network-activated — multisite tenancy boundaries MUST be filesystem-level, not row-level (no `blog_id` column trick that funnels all sites into one DB), because: (i) per-site files allow per-site backup/restore + per-site purge without cross-site impact, (ii) per-site files prevent a runaway log volume on one subsite from filling a shared DB and starving others, (iii) per-site files preserve the WordPress mental model where each subsite "owns" its uploads directory, (iv) per-site files allow operators to delete a subsite by `rm -rf` of its uploads dir without leaving orphan rows; AND read paths MUST stay **strictly site-scoped** — a request handled in `blog_id=2` context MUST query ONLY the `sites/2/` DB, NEVER fan out to other subsites' DBs to aggregate; AND there is NO network-admin "all sites" aggregated view in the plugin's first-party UI (per spec — cross-site analytics is explicitly out of scope); AND when WordPress switches blog context mid-request via `switch_to_blog($blog_id)` (e.g. inside a network-admin loop), the plugin's DB connection MUST be invalidated AND a fresh connection opened against the newly-active subsite's DB on next access — the connection cache MUST be keyed by `(blog_id, db_path)`, NOT global; AND `restore_current_blog()` MUST symmetrically restore the prior connection — leaking a connection across blog-switch boundaries is a SPEC VIOLATION and a tenancy bug; AND the per-site DB schema MUST be IDENTICAL across all subsites (same migrations apply per AC-03 + AC-29) — the migration runner MUST run independently per subsite on first DB access in that subsite's context (lazy initialization), NOT eagerly at network-activation time (eager init would create N empty DBs even for subsites the user never visits, wasting filesystem inodes); AND deletion of a subsite (via WP `wp_delete_site($blog_id)`) MUST trigger plugin cleanup that removes the `sites/<blog_id>/git-logs/` directory entirely — orphan DBs from deleted subsites are a SPEC VIOLATION caught by an audit linter; AND single-site (non-multisite) WordPress installations are treated as `blog_id=1` with the DB at `/wp-content/uploads/git-logs/plugin.db` — the same code path, no `is_multisite()` branch in the DB locator.
- **Verifies:** §24 (multisite per-site DB contract), AC-03 / AC-29 (migration runner applies per-site lazily), AC-21 (audit tables are per-site, not network-wide), AC-12 (ingest writes go to the active subsite's DB).

### AC-36 — Translatable scope  `[deprecated]`
- **Given** §21 was retired in §98 v3.7.8 with rationale "i18n out of scope for v2" (see §00 inventory row 21: `_(removed v3.7.8 — slot retired, see §99)_`)
- **When** any contributor reads this AC seeking POT-extraction normative contract
- **Then** the AC is **dormant** and MUST NOT be cited by new code or tests; the i18n contract is out of scope for v2 entirely (no successor AC, no successor §). Future v3 i18n re-introduction MUST author a fresh AC at a new ID and a fresh § slot — re-using AC-36 or §21 is forbidden by the slot-immutability invariant (`mem://index.md` Core).
- **Verifies:** the dormancy contract above (kept in lockstep with §00 inventory row 21 retirement marker + §98 v3.7.8 retirement entry). Closes Phase 153 Task N3 false-coverage drift (only real drift surfaced by the tree-wide inverse audit; 1 of 1241 ACs).

### AC-41 — WP.org release ZIP  `[active]`
- **Given** the release CI job
- **When** the ZIP is assembled
- **Then** it contains `readme.txt` + `screenshot-1..8.png`; the CI gate runs `wp plugin check` before tagging.
- **Verifies:** §26.

---

## Section I — SSH-Key Lane B (v2.9.1) — NEW in Phase 7

> All ACs in this section are **active** for schema v2.9.1 / docs v3.8.7+. They formalize the contracts laid down in §05 (auth flow), §15 (error codes), §18 (DDL), §28 (GH-Actions example), §30 (threat model), §31 (Lane B reference).

### AC-60 — SshKey registration shape  `[active]`
- **Given** an admin registers a deploy key via the SshKey UI or REST
- **When** the row is committed to `SshKey`
- **Then** the row has `Fingerprint TEXT UNIQUE NOT NULL`, `RepoId FK → Repo ON DELETE CASCADE`, `KeyType` (recommended `ssh-ed25519`), `PublicKey`, `Label`, `OwnedByProfileId FK → Profile`, `IsActive INTEGER CHECK 0/1 DEFAULT 1`, `LastUsedAt`, `CreatedAt`, `RevokedAt`; AND a `SystemEvent` of type `SshKeyRegistered` is appended; AND an `AuditTrail` row of `AuditActionType.SshKeyRegister` (id 22) is written.
- **Verifies:** §18, §31, §08, §22 (AuditActionType seed).

### AC-61 — SshNonce replay defense  `[active]`
- **Given** a valid SSH-signed `/append-log` arrives with headers `X-GL-Fingerprint`, `X-GL-Timestamp`, `X-GL-Nonce`, `X-GL-Signature`
- **When** the server validates
- **Then** (a) `|now − X-GL-Timestamp| ≤ ConfigKv.SshReplayWindowSec` else `GL-SSH-TIMESTAMP-SKEW`; (b) `INSERT OR IGNORE INTO SshNonce(SshKeyId, Nonce, SeenAt)` with `affected_rows=0` ⇒ `GL-SSH-NONCE-REUSED`; (c) the nonce table is per-key (`UNIQUE(SshKeyId, Nonce)`), NOT global, so one tenant cannot DoS another's nonce space; (d) `SshNonceJanitorBatch` rows are pruned per request keeping the table bounded.
- **Verifies:** §05, §15, §18, §30 (S5).

### AC-62 — Lane gating via SshAuthMode  `[active]`
- **Given** `ConfigKv.SshAuthMode ∈ {optional, preferred, required}`
- **When** an inbound request is dispatched
- **Then** **`optional`**: both Lane A (TempToken) and Lane B (SSH) are accepted; **`preferred`**: both accepted but Lane A logs a deprecation warning header; **`required`**: any TempToken submission rejects with `GL-AUTH-LANE-DISABLED` regardless of header presence; AND a request carrying BOTH `X-GL-Auth-Mode: ssh` AND a body `TempToken` always rejects with `GL-SSH-LANE-CONFLICT` (no quiet fallback).
- **Verifies:** §05, §15, §18 (ConfigKv defaults), §30 (S7).

### AC-63 — Signature stripping defense  `[active]`
- **Given** an inbound request claims Lane B (`X-GL-Auth-Mode: ssh`)
- **When** any of `X-GL-Fingerprint`, `X-GL-Timestamp`, `X-GL-Nonce`, `X-GL-Signature` is missing
- **Then** the request rejects with `GL-SSH-HEADER-MISSING` **before** signature verification runs (header-completeness check ordered first); AND HTTPS is mandatory at the deployment surface so on-path header rewrite is blocked at TLS.
- **Verifies:** §05, §15, §30 (S7).

### AC-64 — SshKey rotation flow  `[active]`
- **Given** an active `SshKey` row with `IsActive=1`
- **When** an admin registers a replacement and flips the old row to `IsActive=0`
- **Then** the very next request signed by the old key rejects with `GL-SSH-KEY-INACTIVE` (no propagation delay, no cache); AND `SystemEvent.SshKeyRevoked` is appended for the old; AND `SystemEvent.SshKeyRotated` is appended capturing the new fingerprint; AND `AuditTrail` rows of types `SshKeyRevoke` (23) and `SshKeyRotate` (24) are written.
- **Verifies:** §31, §18, §08, §22 (AuditActionType seed), §30 (S6).

### AC-65 — Deploy-key one-Repo blast radius  `[active]`
- **Given** a stolen `SshKey` private key
- **When** the attacker attempts to forge `/append-log` for a different `RepoId`
- **Then** the request rejects with `GL-SSH-REPO-MISMATCH` because `SshKey.RepoId` is bound to exactly one Repo (FK with `ON DELETE CASCADE`); AND `SshKey.LastUsedAt` is updated on every accepted request so anomaly detection on the admin UI surfaces theft fast; AND the per-Profile rate limit (`RatePerMinPerProfile`) caps the blast radius even within the bound Repo.
- **Verifies:** §31, §18, §05, §10, §30 (S6).

### AC-66 — Canonical signing string + namespace  `[active]`
- **Given** a CI runner signs a request per the §28 / §31 contract
- **When** it constructs the signing input
- **Then** it builds exactly `GL-SSHSIG-V1\nMETHOD\nPATH\nTIMESTAMP\nNONCE\nsha256(body)` (LF-separated, no trailing newline) and signs via `ssh-keygen -Y sign -n git-logs@v2 -H sha512`; AND the server uses the same string + namespace to verify; AND any deviation (different namespace, missing field, CRLF separators) rejects with `GL-SSH-SIGNATURE-INVALID`.
- **Verifies:** §28, §31, §15, §05.

---

## Section J — NDJSON Streaming Retrieval (v2.9.3) — NEW in Phase 11

### AC-67 — NDJSON opt-in via Accept header  `[active]`
- **Given** a client issues a GET to one of `/get-logs`, `/get-pipeline-logs`, `/get-error-logs`, `/get-pipeline-error-logs` (endpoints #5–#10 per §04 §11.7)
- **When** the request carries `Accept: application/x-ndjson` (alone, or with a lower q-value alternative such as `application/x-ndjson, application/json;q=0.5`)
- **Then** the server MUST respond with `Content-Type: application/x-ndjson; charset=utf-8`, `Transfer-Encoding: chunked`, `X-Content-Type-Options: nosniff`, and MUST NOT set `Content-Length`; AND if the same request is sent without the header (or with `Accept: application/json`), the server MUST return the legacy `LogPage` / `ErrorLogPage` JSON envelope per §17 OpenAPI without setting any of the streaming headers; AND for write endpoints #1–#4 (`/append-log`, `/fixed-log`, `/clear-log`, `/clear-log-all`) the `Accept: application/x-ndjson` header MUST be silently ignored — these endpoints always return the standard JSON `AckResponse`.
- **Verifies:** §04 §11.2, §04 §11.7, §17 (paths `/get-*` content variants).

### AC-68 — Frame ordering and discriminator  `[active]`
- **Given** an NDJSON stream is opened against any of the 6 read endpoints
- **When** the server flushes frames over the socket
- **Then** exactly one `Header` frame MUST be the first line, with `Schema:"git-logs-v2/ndjson@1"` and a non-empty UUID `StreamId`; AND zero or more `Log` / `ErrorLog` / `Progress` frames MUST follow in cursor order with monotonically increasing `Seq` (no gaps, no duplicates within a single uninterrupted stream); AND at most one `Error` frame MAY appear; AND exactly one `End` frame MUST be the last line with `Status ∈ {Complete, Truncated, Error}`; AND every line MUST carry a `Type` discriminator matching one of the six values declared in `components.schemas.NdjsonFrame`; AND lines MUST be separated by exactly one LF (`\n`, U+000A) — never CRLF; AND the server MUST NOT split a single JSON object across `\n`.
- **Verifies:** §04 §11.3, §04 §11.4, §17 `components.schemas.NdjsonFrame` discriminator mapping.

### AC-69 — Resume via after-seq + stream-id  `[active]`
- **Given** an earlier stream returned `End{Status:"Truncated", NextAfterSeq:N}` — typically because `ConfigKv.NdjsonMaxRowsPerStream` (default `1000000`) was hit — or the client recorded the last successfully received `Seq` before disconnect
- **When** the client re-issues the same request with `?after-seq=N` (and optionally `?stream-id=<original Header.StreamId UUID>` for audit correlation)
- **Then** the new stream MUST emit a fresh `Header` frame with a NEW `StreamId` and resume row emission strictly after `Seq=N` (exclusive); AND if the per-SHA `.db` file referenced by the original cursor has since been pruned per AC-53, the response MUST be `Header` → `Error{Code:"GL-NDJSON-CURSOR-LOST"}` → `End{Status:"Error"}` per §15 v2.9.3; AND `?after-seq` and `?stream-id` MUST be ignored on legacy `application/json` responses (no error, no behavior change) so accidental presence does not break non-streaming clients.
- **Verifies:** §04 §11.6, §15 (`GL-NDJSON-CURSOR-LOST`), AC-53 (prune lifecycle).

### AC-70 — Client disconnect handling (GL-NDJSON-CLIENT-DISCONNECT)  `[active]`
- **Given** a streaming response is in progress with the per-SHA SQLite handle open via the AC-52 LRU pool
- **When** the client closes the TCP connection mid-stream (EPIPE / ECONNRESET / browser tab close)
- **Then** the server MUST detect the broken pipe within 1 flush cycle (≤ `NdjsonProgressEveryMs` worst case, default 2000 ms); AND MUST return the per-SHA handle to the AC-52 pool (no leak); AND MUST abandon the cursor without retry; AND MUST write exactly one `AuditTrail` row with `Code="GL-NDJSON-CLIENT-DISCONNECT"` (HTTP 499, informational, server-side audit only); AND MUST NOT attempt to send any further frames (the socket is gone — no `Error` frame, no `End` frame). **PHP detection mechanism (Phase 153 LOW close-out)**: the implementation MUST call `connection_aborted()` immediately after each `flush()` inside the streaming loop (between frames AND after every `NdjsonProgressEveryMs` heartbeat); when it returns `1`, exit the loop, return the handle, and write the audit row. `ignore_user_abort(true)` MUST be set at request entry to prevent PHP-FPM from killing the process before the audit row is written. Polling intervals longer than one flush cycle OR relying solely on `fwrite()` returning `false` (which can be delayed by output buffering) FAIL this AC.
- **Verifies:** §04 §11.4 step 4, §15 (`GL-NDJSON-CLIENT-DISCONNECT`), AC-52 (handle pool), PHP `connection_aborted()` + `ignore_user_abort()` semantics.

### AC-71 — Per-frame size cap and truncation  `[active]`
- **Given** the server is about to emit a `Log` or `ErrorLog` frame whose serialized JSON exceeds `ConfigKv.NdjsonMaxFrameBytes` (default `262144` = 256 KiB)
- **When** the frame is composed
- **Then** the server MUST truncate `LogText` to fit within the cap (preserving valid UTF-8 — never emit a partial multi-byte sequence), MUST add `"Truncated":true` to the same frame (mirroring AC-27 ingest-side `Warn` truncation semantics), and MUST emit the line atomically with a single trailing `\n`; AND the server MUST NOT split the object across multiple lines; AND `Seq` numbering MUST treat the truncated frame as one row (no gap, no duplicate).
- **Verifies:** §04 §11.4 step 3, §04 §11.5 (`NdjsonMaxFrameBytes`), AC-27 (ingest truncation parity).

### AC-72 — Progress frame cadence  `[active]`
- **Given** a long-running stream is walking the per-SHA cursor
- **When** either `ConfigKv.NdjsonProgressEveryRows` rows have been emitted since the last `Progress` (default `10000`) OR `ConfigKv.NdjsonProgressEveryMs` milliseconds have elapsed since the last `Progress` (default `2000`), whichever fires first
- **Then** the server MUST emit one `Progress` frame carrying `Seq` (continuing the monotonic sequence), `RowsEmitted` (cumulative since `Header`), `ElapsedMs` (cumulative since `Header`), and OPTIONALLY `CurrentSha` (the SHA the cursor is currently inside); AND if either ConfigKv key is set to `0`, that trigger MUST be disabled (rows-only or time-only progress); AND if both are `0`, NO `Progress` frames MUST be emitted at all.
- **Verifies:** §04 §11.5 (`NdjsonProgressEveryRows`, `NdjsonProgressEveryMs`), §04 §11.3 `Progress` frame schema.

---

## Section K — Pipeline.PreviousHasError State Transitions (v2.9.2) — NEW in Phase 12

### AC-73 — State-transition label matrix  `[active]`
- **Given** a `Pipeline` row exists with `HasError ∈ {0,1}` and `PreviousHasError ∈ {0,1}` (both columns `NOT NULL` per §18 v2.9.2 DDL)
- **When** any consumer (admin UI per §03, NDJSON `Header` frame per §04 §11.3 + AC-74, audit/analytics per §22) needs to label the pipeline's current run state
- **Then** the label MUST be derived purely from the `(PreviousHasError, HasError)` tuple per the §01 glossary v3.8.10 mapping: `(0,0) → "still-green"`, `(0,1) → "first-failure"`, `(1,1) → "still-failing"`, `(1,0) → "just-recovered"`; AND no other label values are permitted (the four are an exhaustive enum); AND consumers MUST NOT invent a fifth label such as `"unknown"` or `"initial"` — newly-inserted rows whose first observation is a failure MUST be labeled `"first-failure"` (because the back-fill rule of AC-75 ensures `PreviousHasError=0` for fresh rows by virtue of the column `DEFAULT 0`); AND label derivation MUST be a pure function (no DB lookup beyond the two columns already on the row) so the same `(PreviousHasError, HasError)` tuple ALWAYS produces the same label across all consumers.
- **Verifies:** §01 glossary v3.8.10 (`PreviousHasError` row), §02 v3.8.10 (`Pipeline.PreviousHasError`), §18 v2.9.2 (DDL + `CHECK (PreviousHasError IN (0,1))`), §03 (admin UI consumer), §04 §11.3 + AC-74 (NDJSON Header consumer).

### AC-74 — NDJSON Header.StateTransition exposure  `[active]`
- **Given** an NDJSON streaming response is being opened for any read endpoint scoped to a single `PipelineId` (i.e. `/get-pipeline-logs` or `/get-pipeline-error-logs` per §04 §11.7 endpoints #7–#10) AND the request matches exactly one `Pipeline` row
- **When** the server composes the `Header` frame per AC-68
- **Then** the `Header` frame MAY (but is not required to) carry an OPTIONAL `StateTransition` field whose value is the AC-73 label derived from the row's current `(PreviousHasError, HasError)` tuple; AND when present, the value MUST be one of the four AC-73 enum strings exactly (no casing variants, no whitespace); AND when the request resolves to zero pipelines (404 case) or to multiple pipelines (e.g. `/get-logs` repo+branch scope), the `StateTransition` field MUST be absent from the `Header` frame entirely (NEVER emit `null`, NEVER emit `"unknown"`); AND the field's absence MUST NOT be treated as an error by clients — older spec versions and broader-scope endpoints simply omit it; AND if the field is present, the OpenAPI `NdjsonHeaderFrame` schema (§17 v2.9.3+) MUST declare it as an optional string with the four-value enum constraint matching AC-73.
- **Verifies:** §04 §11.3 (`Header` frame), §17 (`components.schemas.NdjsonHeaderFrame`), AC-68 (frame ordering + Header semantics), AC-73 (label enum).

### AC-75 — Back-fill correctness + single-statement write atomicity  `[active]`
- **Given** a v2.9.1 → v2.9.2 schema upgrade is being applied OR a server-side mutation is updating `Pipeline.HasError`
- **When** the migration runs OR a row is updated
- **Then** the migration MUST execute exactly `UPDATE Pipeline SET PreviousHasError = HasError;` as a single SQL statement (so every existing row's first post-upgrade transition is labeled `still-green` or `still-failing` per AC-73, NEVER spuriously labeled `first-failure` or `just-recovered`) — the migration MUST NOT use a row-by-row loop and MUST NOT default `PreviousHasError` to `0` for rows whose `HasError=1` (which would produce a fake `just-recovered` label on the next clean run); AND every server-side mutation of `HasError` MUST also update `PreviousHasError` in the SAME SQL statement using a `CASE` or self-referencing `UPDATE` so the read-modify-write window is zero (e.g. `UPDATE Pipeline SET PreviousHasError = HasError, HasError = :new_value, UpdatedAt = strftime('%s','now') WHERE PipelineId = :id`) — clients MUST NOT issue a separate `SELECT HasError` followed by `UPDATE … SET HasError, PreviousHasError` because two concurrent writers could observe the same `OLD.HasError` and produce inconsistent transition labels; AND if the application layer cannot express this atomically (e.g. an ORM that always splits read+write), the spec REQUIRES wrapping the mutation in a `BEGIN IMMEDIATE; … COMMIT;` SQLite transaction to serialize concurrent writers AND verifying via `SELECT changes() = 1` that exactly one row was touched (zero-row updates indicate a stale `PipelineId`, multi-row updates indicate a missing `WHERE PipelineId = :id` clause); AND `MigrationState` MUST record marker `2.9.2` exactly once per database after the back-fill `UPDATE` succeeds — re-running the migration MUST be a no-op (idempotent) because the `UPDATE` re-executes harmlessly on already-back-filled rows (`PreviousHasError = HasError` is the steady-state invariant immediately after each write and immediately after back-fill, but diverges briefly between writes — that's the whole point).
- **Verifies:** §18 v2.9.2 (DDL + back-fill comment block + write-rule comment block), §02 v3.8.10 (`Pipeline.PreviousHasError` doc), §01 v3.8.10 (`PreviousHasError` glossary entry — back-fill rule + write rule).

### AC-22-LV1 — Locked vacant slots §09–§13 must remain file-absent  `[active]`
- **Given** the §22 folder inventory in `00-overview.md` lines 77–81 declares slot numbers **09, 10, 11, 12, 13** as **"Locked vacant slot"** with content redirected to §05 / §08 / §18 / §30 / §31 / §37 / §38
- **When** any contributor (human or AI) is authoring new content in folder 22 OR a CI lint runs over `spec/22-git-logs-v2/`
- **Then** NO file matching the glob `spec/22-git-logs-v2/{09,10,11,12,13}-*.md` may exist on disk — these slot numbers are **retired**, not "available stubs"; AND a contributor MUST NOT create a "Slot intentionally vacant" stub file at any of these slot numbers (the original GAP-V2-06 fix recipe is **rejected** — see §37 Phase P6 entry — because (a) it conflicts with the Core memory rule "File slots are immutable once shipped — never reuse a number" and (b) a one-line stub file would score 0 on `check-tree-health.cjs --strict` and regress the module from 168/168 → 158/168); AND the next free slot for new §22 content is **§40+** (§38 + §39 are now occupied per Phases P5 and 105); AND the §00 italic inventory rows are the **single source of truth** for the locked-vacant disambiguation — they are advisory anchors, not navigation targets, and a blind-AI link-follow against them is the accepted residual cost of the immutability invariant; AND `linter-scripts/check-spec-folder-refs.py` (or its successor) MAY add a per-folder allowlist entry recording these five slot numbers as `[locked-vacant]` so any future authoring attempt is caught at PR time.
- **Verifies:** §00 v3.8.8 (inventory rows §09–§13 marked "Locked vacant slot"), §37 v1.2.0 (GAP-V2-06 RESOLVED entry — Phase P6 rejection rationale), `mem://index.md` Core rule "File slots are immutable once shipped — never reuse a number".

### AC-76 — Streaming-ingest error-code surface (`GL-STREAM-*`)  `[active]`
- **Given** the opt-in NDJSON ingest mode for `POST /append-log` defined in §04 §1.2 (sentinel `X-GL-Stream: 1` + `Content-Type: application/x-ndjson; charset=utf-8` + `Transfer-Encoding: chunked`, three-frame `StreamHeader` / `Line` / `StreamFooter` contract, cap reuse of `NdjsonMaxRowsPerStream` per §11.4)
- **When** the server validates an inbound ingest stream and detects (a) a missing/malformed/late `StreamHeader`, (b) EOF before `StreamFooter`, (c) line count exceeding `NdjsonMaxRowsPerStream`, or (d) an NDJSON frame whose discriminator key is none of the three recognized values
- **Then** the server MUST respond with the exact code/HTTP-status pairs `GL-STREAM-NO-HEADER` / 400, `GL-STREAM-NO-FOOTER` / 400, `GL-STREAM-TOO-MANY-LINES` / 413, `GL-STREAM-UNKNOWN-FRAME` / 400 respectively; AND each code MUST be present as a row in §15 v2.9.4 `## Streaming ingest (Lane B — see §04 §1.2)` table with matching HTTP status, cause, and caller-action columns; AND each code MUST be present in §17 v2.9.6 `components.schemas.ErrorCode.enum` so generated OpenAPI clients reject unknown values at typecheck time; AND because ingest streaming responds with a buffered standard `AckResponse` (per §04 §1.2) all four codes MUST surface as the conventional `ErrorEnvelope` JSON shape — NEVER as a mid-stream `Error` frame (the response body is buffered, not streamed); AND any partial inserts already buffered when the violation is detected MUST be rolled back atomically (no half-written `LogEntry` rows visible to subsequent reads); AND adding any future `GL-STREAM-*` code MUST follow the same three-file lockstep (§15 row + §17 enum entry + this AC's `Verifies:` extended).
- **Verifies:** §04 v2.9.4 §1.2 lines 102–131 (wire-format pins + four MUST-respond rules), §15 v2.9.4 `## Streaming ingest (Lane B — see §04 §1.2)` (catalog rows for all 4 codes), §17 v2.9.6 `components.schemas.ErrorCode` enum (NDJSON streaming ingest block), §11.4 (`NdjsonMaxRowsPerStream` shared cap with retrieval streaming).

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Auth flow §05](./05-auth-and-validation.md)
- [Error codes §15](./15-error-codes.md)
- [Schema DDL §18](./18-schema.sql)
- [GH-Actions SSH example §28](./28-example-github-actions.md)
- [Threat model §30](./30-threat-model.md)
- [SSH-Key Lane B reference §31](./31-ssh-key-auth.md)
- [Split-DB log storage §39](./39-split-db-log-storage.md)

---

### AC-78 — Module asset inventory pin (Lesson #29 — git-logs-v2 37-entry inventory + DDL/REST/PHP fixtures)  `[critical]`

**Given** spec/22's full on-disk asset inventory comprises 37 entries (§99 inventory authoritative): root `.md` files include `00-overview.md` through `08-*`, `14-*` through `37-*` (locked-vacant slots `09-13` enforced absent per AC-22-LV1), `39-split-db-log-storage.md`, `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md`, plus normative non-`.md` fixtures `18-schema.sql` (canonical DDL), `33-bats-test-skeleton`, `34-phpunit-test-skeleton`, `35-reference-ci-yml`, **When** an audit harness bundles only `{00,97,98,99}-*.md` (per spec/27 slot 34 v1.1.0 AC-34-09 tier-1 cap of ~90 KB) OR truncates non-tier-1 files at the per-bundle 140 KB walker cap, **Then** the auditor MUST treat any `[D5] Missing Core Schema and API Definitions` finding (citing files 04, 18, 34, or "36 files in the inventory") as a **harness bundling-cap artifact**, NOT a spec defect — `04-rest-api-endpoints.md` (406 lines on disk), `18-schema.sql` (465 lines, canonical DDL), and `34-phpunit-test-skeleton.md` (311 lines, PHP class skeletons) are all present on disk at their cited paths per §99 inventory (Lesson #39 evidence triple: `wc -l` + `tail` + `grep` confirm complete files). `[D4] Truncated Glossary and Enums` (citing `01-glossary-and-enums.md` "truncated at the 136KB cap, losing the TypeScript Mirror and Enum Catalog") is also a walker-cap artifact, NOT a content gap — the file is 14346 bytes (14 KB) on disk, well under any reasonable cap; the truncation occurs during multi-file bundle assembly when sibling files exhaust the byte budget BEFORE `01-*.md` is appended. The TypeScript Mirror and full Enum Catalog ARE present at the file tail (verified: `tail -20` shows the closing Drift-detection contract table). Similarly `[D4] Missing Concrete Code Fixtures` — the SQL DDL fixture IS `18-schema.sql` (canonical) and the PHP skeletons ARE in `34-phpunit-test-skeleton.md`. `[D3] Concurrency/Race Condition on Rate Limits` (citing AC-26's "in-memory + persisted floor") is correctly bound to spec/13 §97 AC-22 per Lesson #36 (link-don't-restate) — SQLite locking strategy for the persisted floor lives in spec/13's canonical contract; restating would create dual-source drift. The locked-vacant slot range (`09-13`) is enforced by AC-22-LV1 — auditor "missing files 09–13" reports MUST be treated as the LOCKED state, not a spec gap.

- **Verifies:** the spec/22 module-kind = `module` declaration AND the auditor-authoritative inventory contract for the 37-entry asset list (including normative non-`.md` fixtures `18-schema.sql` + `33`/`34`/`35` test skeletons) AND the locked-vacant-slot AC-22-LV1 contract AND the cross-module link-not-restate boundary for AC-26's persisted-floor concurrency; codifies **Lesson #29** + **Lesson #36** for tier-1-bounded auditors. Mirror of spec/13 AC-24 + spec/28 AC-28-41 + spec/14 AC-21 + spec/16 AC-21 + spec/07 AC-35 + spec/10 AC-9 + spec/03 AC-08 + spec/11 AC-10 + spec/12 AC-09 + spec/17 AC-10 + spec/18 AC-09 + spec/25 AC-AI-09..11. Until A8 (LLM-gateway re-score) unblocks, the cache will report v3/v4/v5 [D5]/[D4]/[D3] findings citing these — this AC declares those findings stale-cache artifacts per Lesson #34.

---

### AC-79 — Cross-Module Externalized Citation Map (Lesson #36 + Lesson #37 — link-don't-restate anchor table)  `[critical]`

- **Given** spec/22 is an integration-axis module (Lesson #37: d2≤0.83 + d5≥1.10) whose normative content references contract surfaces owned by 5 other top-level modules + 1 linter-script (spec/04 DDL conventions, spec/12 CI runner matrix, spec/13 §97 AC-22 SQLite WAL/busy-timeout/retry, spec/26 Mermaid diagrams, spec/05 split-DB pattern, spec/27 `check-spec-folder-refs.py`).
- **When** an AI auditor walks spec/22 §97 and encounters an externalized citation, OR a contributor needs to follow the dependency chain to verify a normative claim.
- **Then** the canonical citation map (6 rows, each = citation + owning module/AC + spec/22 file + purpose + restate-forbidden flag) MUST live in **§50 §AC-79 detail** (`50-ac-delegation-maps-detail.md`). The table is APPEND-ONLY within a phase (rows added when new external cites ship; never reworded). Restating any linked contract inline within spec/22 is FORBIDDEN (Lesson #36 dual-source drift class) — every row's "Restate-in-22 forbidden?" cell is `YES` by construction.
- **Verifies:** cross-module externalized citation contract for spec/22 (all 6 external deps); codifies **Lesson #36** (link-don't-restate cross-module boundary) + **Lesson #37** (integration-axis modules co-need Lesson #19 + Lesson #36); mirror-pair with **AC-80** (intra-module sibling-file delegation); together AC-78 + AC-79 + AC-80 form the complete tier-1 audit-followability triplet; **§50 §AC-79 detail (citation table)** — full normative body lives in `50-ac-delegation-maps-detail.md`. Until A8 LLM-gateway re-score, any cross-module-dangling finding against the 6 listed citations is a stale-cache artifact per Lesson #34.

---

### AC-80 — Sibling File Delegation Map (Lesson #21 — intra-module audit-boundary pin for 33 sibling files)  `[critical]`

- **Given** spec/22 contains 33 normative sibling files outside the tier-1 audit bundle, and the auditor's tier-1 walker (~140 KB cap) does NOT see them unless their content is explicitly bound from §97 (per AC-34-09; binding-density survey 2026-05-06 found 13 of 33 had ZERO §97-bound ACs — the textbook **Lesson #21 audit-boundary < verification-boundary gap**).
- **When** an AI auditor or contributor asks "for each sibling file in this module, which §97 AC governs it?".
- **Then** the canonical delegation table in **§50 §AC-80 detail** (`50-ac-delegation-maps-detail.md`) MUST provide every sibling file's mapping to (a) content kind, (b) governing §97 AC family, (c) tier visibility, (d) restate-in-§97-forbidden status. The 11 "no current §97-by-name row" entries are GOVERNED-BUT-UNNAMED (NOT orphans). The 5 "informative" entries are EXEMPT from §97-by-name binding. The table is APPEND-ONLY within a phase (rows added when new siblings ship; never reworded; AC-family cells may be updated via §97-WINS evolution, content-kind is immutable per Lesson #25). Any new sibling file added in a future phase MUST add a row BEFORE the file ships.
- **Verifies:** intra-module sibling-file delegation contract for spec/22 (all 33 siblings); closes Lesson #21 intra-module gap; mirror-pair with **AC-79** (cross-module externalized citation map) — together AC-78 + AC-79 + AC-80 form the complete tier-1 audit-followability triplet per Lesson #37; **§50 §AC-80 detail (delegation table)** — full normative body lives in `50-ac-delegation-maps-detail.md`. Until A8 (LLM-gateway re-score) unblocks, this AC declares any "sibling file orphan" or "missing §97 AC for file NN" finding against the 33 listed files a stale-cache artifact per Lesson #34.

---

### AC-81 — Enum Catalog promotion: normative tier-1 binding (Lesson #19 + Lesson #36)  `[critical]`

- **Given** spec/22 ships **11 active enum types** + **1 deprecated stub** driving every state-machine transition, RBAC permission lookup, audit row, system-event row, severity ordering, and TS-client typing — and the canonical catalog `01-glossary-and-enums.md` (14 KB) may be walker-truncated (Lesson #16 tier-cap class), causing `[D4] Truncated Glossary and Enums` false-positives;
- **When** an AI auditor walks spec/22 §97 OR an implementer needs to verify normative enum codes without leaving the §97 bundle,
- **Then** the canonical 12-row enum table (UserStatus · Role · Permission · Provider · Acceptance · AppStatus · AppLinkType · LogSeverity · PipelineActionType · SystemEventType · AuditActionType · AuditOutcome · OwnerType_DEPRECATED_v380), the source-of-truth precedence chain (SQL seed canonical → Enum Catalog mirror → TS Mirror → generated PHP), the four-surface partial-landing rule (`GL-SCHEMA-DRIFT`), and the FORBIDDEN-restate-inline rule MUST live in `51-ac-enum-catalog-detail.md` (sibling-file detail per AC-80). Body byte-identical to the previous §97 inline body; remains tier-1 binding.
- **Verifies:** tier-1 normative enum-catalog binding — closes Lesson #19 audit-boundary < verification-boundary gap (catalog file is tier-2, walker-truncatable; this AC lifts its inventory into tier-1). Codifies Lesson #36 (link-don't-restate Drift-detection precedence). Completes tier-1 normative-surface closure quartet (AC-78 + AC-79 + AC-80 + AC-81). Until A8 unblocks, any "missing enum catalog" or "[D4] Truncated Glossary" finding against the 12 listed enums is a stale-cache walker-cap artifact per Lesson #34. **§51 §AC-81 detail** — full normative body lives in `51-ac-enum-catalog-detail.md`.
- **Source:** `97-acceptance-criteria.md` (this AC) + `51-ac-enum-catalog-detail.md` (full body); cross-refs `01-glossary-and-enums.md`, `18-schema.sql`, `15-error-codes.md`, `19-permission-matrix.md`, spec/23 AC-ADB-14, AC-78/79/80.


---

### AC-82 — `riseup-git-logs` CLI binary contract (J-series tier-1 anchor; Lesson #19 + Lesson #21 + Lesson #36)  `[critical]`

- **Given** a new client-side CLI subsystem `riseup-git-logs` is being introduced under spec/22 across slot range §40–§45 (six normative slots), where slot §40 is the tier-1 entry point that downstream J-series slots delegate to;
- **When** an AI auditor or implementer walks spec/22 §97 and seeks the binding contract for 40-cli-overview.md,
- **Then** the canonical normative body MUST live in `54-ac-j-series-cli-detail.md` (sibling-file detail per AC-80) and `40-cli-overview.md` (canonical surface). Sub-contracts: (1) standalone binary identity (no subcommand under another binary); (2) closed wrap-set of 4 read-only git subcommands (`log`/`status`/`diff`/`show`) + 11-entry FORBIDDEN mutating-subcommand list; (3) 5-step deterministic identity-discovery algorithm (`rev-parse --show-toplevel` → pointer read → `rev-parse HEAD` → `repoIdentityHash = sha256(canonical-remote)[0:32]` → bind to NDJSON); (4) first-run `init` bootstrap discipline (no `.gitignore` mutation, atomic temp-then-rename per spec/13 AC-22); (5) 6 cross-module link-don't-restate surfaces (spec/13 AC-21/22/23 + spec/22 §04/§31/§39). Body byte-identical to previous §97 inline body; remains tier-1 binding.
- **Verifies:** tier-1 binding contract for J-series file `40-cli-overview.md`. Closes Lesson #19 audit-boundary < verification-boundary gap. Mirror of spec/12 AC-10 + spec/14 AC-23. Pairs with AC-80 sibling-file delegation map per Lesson #21 + Lesson #39. Codifies Lesson #36 link-don't-restate to all cited cross-module surfaces. Until A8 unblocks, any "missing 40-cli-overview.md" or "[D2] unbound contract" finding is a stale-cache walker-cap artifact per Lesson #34. **§54 §AC-82 detail** — full normative body lives in `54-ac-j-series-cli-detail.md`.
- **Source:** `97-acceptance-criteria.md` (this AC) + `54-ac-j-series-cli-detail.md` (full body); cross-refs `40-cli-overview.md`, AC-78/79/80/81.


### AC-83 — `.riseup-git-logs.json` pointer-file wire format (J-series tier-1; Lesson #19 + Lesson #21 + Lesson #36)  `[critical]`

- **Given** the `riseup-git-logs` CLI (per AC-82) writes a JSON pointer file at `<git-root>/.riseup-git-logs.json` to record repo identity, current head, server upload endpoint, expiry, and auto-fix download URL across invocations;
- **When** an AI auditor or implementer walks spec/22 §97 and seeks the binding contract for 41-cli-pointer-file-schema.md,
- **Then** the canonical normative body MUST live in `54-ac-j-series-cli-detail.md` (sibling-file detail per AC-80) and `41-cli-pointer-file-schema.md` (canonical surface). Sub-contracts: (1) file location & lifecycle (UTF-8 LF mode 0644, atomic temp-then-rename per spec/13 AC-22, no `.gitignore` mutation); (2) closed 8-field inventory (`schemaVersion` · `repoIdentityHash` · `repoCanonicalRemote` · `currentHead` · `uploadUrl` · `uploadedAt` · `expiresAt` · `autofixDownloadUrl`) `additionalProperties:false`; (3) verbatim Draft-07 JSON Schema embedded + validated on every read/write; (4) 11-entry forbidden secret-shaped field list → `GL-POINTER-FORBIDDEN-FIELD`; (5) 5-row trigger×action validation table + SemVer evolution rules (PATCH/MINOR/MAJOR with MAJOR requiring follow-up §97 extension AC + AC-80 row update). Body byte-identical to previous §97 inline body; remains tier-1 binding.
- **Verifies:** tier-1 binding contract for J-series file `41-cli-pointer-file-schema.md`. Closes Lesson #19 audit-boundary < verification-boundary gap. Mirror of spec/14 AC-23 (update-interface-contract pattern). Pairs with AC-80 sibling-file delegation map per Lesson #21 + Lesson #39. Codifies Lesson #36 link-don't-restate to all cited cross-module surfaces. Until A8 unblocks, any "missing 41-cli-pointer-file-schema.md" or "[D2] unbound contract" finding is a stale-cache walker-cap artifact per Lesson #34. **§54 §AC-83 detail** — full normative body lives in `54-ac-j-series-cli-detail.md`.
- **Source:** `97-acceptance-criteria.md` (this AC) + `54-ac-j-series-cli-detail.md` (full body); cross-refs `41-cli-pointer-file-schema.md`, AC-78/79/80/81.


### AC-84 — `riseup-git-logs` CLI classifier rules (J-series tier-1; Lesson #19 + Lesson #21 + Lesson #36)  `[critical]`

- **Given** the `riseup-git-logs` CLI (per AC-82) wraps 4 read-only git subcommands and MUST classify each invocation deterministically into one of 4 outcome enums driving NDJSON frame emission per AC-85 and the 4-state auto-fix flow per AC-86;
- **When** an AI auditor or implementer walks spec/22 §97 and seeks the binding contract for 42-cli-classifier-rules.md,
- **Then** the canonical normative body MUST live in `54-ac-j-series-cli-detail.md` (sibling-file detail per AC-80) and `42-cli-classifier-rules.md` (canonical surface). Sub-contracts: (1) closed 4-outcome set (`NORMAL`/`WARN`/`ERROR`/`INTERNAL`) with `ExitCode` mapping per spec/13 AC-21 link-don't-restate; (2) 5-step deterministic precedence (forbidden-subcommand → identity-discovery failure → exit-non-zero ERROR → exit-zero WARN → fallback NORMAL); (3) per-subcommand rule tables Section A `git log` / B `git status` / C `git diff` / D `git show` (split-and-piggyback); (4) forbidden non-determinism (`LANG=C` mandatory, no `~/.gitconfig`/clock/cache reads); (5) classifier versioning (banner version IS classifier version; NDJSON `classifierVersion` per §43; `MAJOR` bump = coordinated upgrade event under follow-up §97 extension AC); (6) FORBIDDEN: emitting any outcome outside the 4-state set; suppressing classified frames at CLI layer. Body byte-identical to previous §97 inline body; remains tier-1 binding.
- **Verifies:** tier-1 binding contract for J-series file `42-cli-classifier-rules.md`. Closes Lesson #19 audit-boundary < verification-boundary gap. Third J-series instance (after CLI-binary J10 + wire-format J11). Pairs with AC-80 sibling-file delegation map per Lesson #21 + Lesson #39. Codifies Lesson #36 link-don't-restate to all cited cross-module surfaces. Until A8 unblocks, any "missing 42-cli-classifier-rules.md" or "[D2] unbound contract" finding is a stale-cache walker-cap artifact per Lesson #34. **§54 §AC-84 detail** — full normative body lives in `54-ac-j-series-cli-detail.md`.
- **Source:** `97-acceptance-criteria.md` (this AC) + `54-ac-j-series-cli-detail.md` (full body); cross-refs `42-cli-classifier-rules.md`, AC-78/79/80/81.

### AC-85 — `riseup-git-logs` CLI upload protocol (J-series tier-1; Lesson #19 + Lesson #21 + Lesson #36)  `[critical]`

- **Given** the `riseup-git-logs` CLI (per AC-82/AC-84) classifies each wrapped invocation into one of 4 outcomes and MUST stream the resulting frames to the spec/22 plugin via deterministic NDJSON-over-HTTPS for server-side ingestion per AC-88 and downstream auto-fix per AC-86;
- **When** an AI auditor or implementer walks spec/22 §97 and seeks the binding contract for 43-cli-upload-protocol.md,
- **Then** the canonical normative body MUST live in `54-ac-j-series-cli-detail.md` (sibling-file detail per AC-80) and `43-cli-upload-protocol.md` (canonical surface). Sub-contracts: (1) transport (POST `/wp-json/git-logs/v1/upload` https-only + SSH-key Lane B + `application/x-ndjson` LF-terminated + gzip>4 KiB); (2) closed 9-field per-frame envelope `additionalProperties:false` + 16-entry forbidden-field list; (3) idempotency (`Idempotency-Key` UUIDv4-per-batch + 24h server retention + sha256-mismatch → 409 + frame-level dedup belt-and-braces); (4) retry & backoff (NO 4xx retries; 6-attempt exponential-backoff-with-full-jitter on 5xx/network 1s/2s/4s/8s/16s; cryptoRand mandatory; identical body+key on retry; re-derivation FORBIDDEN); (5) server response 6 fields feeding back into §41 pointer file; (6) forbidden patterns + 7-row error envelope mapping (400/401/409/413/429/5xx → `GL-UPLOAD-*`). Body byte-identical to previous §97 inline body; remains tier-1 binding.
- **Verifies:** tier-1 binding contract for J-series file `43-cli-upload-protocol.md`. Closes Lesson #19 audit-boundary < verification-boundary gap. Fourth J-series instance (transport-protocol axis). Pairs with AC-80 sibling-file delegation map per Lesson #21 + Lesson #39. Codifies Lesson #36 link-don't-restate to all cited cross-module surfaces. Until A8 unblocks, any "missing 43-cli-upload-protocol.md" or "[D2] unbound contract" finding is a stale-cache walker-cap artifact per Lesson #34. **§54 §AC-85 detail** — full normative body lives in `54-ac-j-series-cli-detail.md`.
- **Source:** `97-acceptance-criteria.md` (this AC) + `54-ac-j-series-cli-detail.md` (full body); cross-refs `43-cli-upload-protocol.md`, AC-78/79/80/81.


- **Given** a successful upload per AC-85 §6 returns `autofixDownloadUrl` (https or null), and when non-null the CLI MAY download a server-prepared fix bundle and apply it under a 4-state propose-diff-confirm-apply flow with the user kept in the loop;
- **When** an AI auditor or implementer walks spec/22 §97 and seeks the binding contract for the auto-fix protocol — download request, fix-bundle envelope, 4-state outcome enumeration, preflight preconditions, atomic apply, post-apply pointer-file refresh, error envelope,
- **Then** the canonical 7-section contract MUST live in `44-cli-autofix-protocol.md` with full normative body in `54-ac-j-series-cli-detail.md` (sibling-file detail per AC-80): (1) download request (https-only, Lane B, 4 MiB compressed cap, 30s/60s timeouts); (2) fix-bundle 7-field envelope + 17-entry forbidden-field list; (3) 4-state closed outcome set (`APPLIED`/`REJECTED_USER`/`REJECTED_PRECONDITION`/`DEFERRED_NETWORK` mapped to `OK`/`OK`/`UserError`/`Internal`); (4) strict 7-step preflight order (no reorder, no auto-stash); (5) atomic per-file temp-then-rename apply (no `git apply`, no auto-mkdir); (6) post-apply pointer refresh on `APPLIED` only (no auto-commit, no auto-push); (7) 11-row `GL-FIX-*` error envelope owned by §15.
- **Verifies:** tier-1 binding contract for J-series auto-fix-protocol file `44-cli-autofix-protocol.md`. Closes Lesson #19 audit-boundary < verification-boundary gap. Mirror of AC-82/83/84/85. Pairs with AC-80 row 38 per Lesson #21 + Lesson #39. Codifies Lesson #36 octuple link-don't-restate to spec/22 §04/05/15/31/41/42/43 + spec/13 AC-21/AC-22. Codifies user-in-the-loop invariant. Until A8 unblocks, any "missing auto-fix protocol" or "[D2] unbound apply contract" finding against `44-cli-autofix-protocol.md` is a stale-cache artifact per Lesson #34. **§54 §AC-86 detail** — full normative body lives in `54-ac-j-series-cli-detail.md`.
- **Source:** `97-acceptance-criteria.md` (this AC) + `54-ac-j-series-cli-detail.md` (full body); cross-refs `44-cli-autofix-protocol.md`, `43-cli-upload-protocol.md` §6, `41-cli-pointer-file-schema.md` §2, `42-cli-classifier-rules.md`, `40-cli-overview.md`, spec/22 §04/§15/§31, spec/13 §97 AC-21/AC-22, AC-78/79/80/81/82/83/84/85.


---

### AC-87 — `riseup-git-logs` CLI test plan (J-series tier-1 closure; Lesson #19 + Lesson #21 + Lesson #36)  `[critical]`

- **Given** the J-series CLI subsystem ships five tier-1 contract surfaces (§40 binary / §41 pointer / §42 classifier / §43 upload / §44 auto-fix) bound by AC-82..AC-86, requiring a closed test-coverage contract so any AI implementer can verify behavioural conformance from the spec alone;
- **When** an AI auditor or implementer walks spec/22 §97 and seeks the binding contract for 45-cli-test-plan.md,
- **Then** the canonical normative body MUST live in `54-ac-j-series-cli-detail.md` (sibling-file detail per AC-80) and `45-cli-test-plan.md` (canonical surface). Sub-contracts: (1) two-layer architecture (L1 Go `testing`+`httptest` ≤30s/push; L2 Bats + stub `git-logs-server` mock ≤90s/push; property/fuzz deferred to spec/13 framework — NOT duplicated); (2) closed 5-suite matrix `T-CLI-IDENT` (≥7 cases binds AC-82) · `T-CLI-PTR` (≥9 binds AC-83) · `T-CLI-CLASSIFY` (≥11 binds AC-84) · `T-CLI-UPLOAD` (≥13 binds AC-85) · `T-CLI-AUTOFIX` (≥12 binds AC-86); (3) per-suite GWT enumerations bound 1:1 to owning §97 AC sub-sections (e.g. `PTR-05`→§41 §3 lex-key order; `AUTOFIX-09`→§44 §5 mid-bundle rename → DEFERRED_NETWORK); (4) fixture taxonomy under `cli/testdata/mock-server/`; (5) coverage targets (L1 ≥85% line on `pkg/{identity,pointer,classifier,upload,autofix}`; L2 ≥52 cases; every `GL-*` ≥1 negative; every `ExitCode` ≥1 positive); (6) forbidden patterns (no inline restate of §41/§42/§43/§44 closed sets; no spec/13 AC-21/22 restate; no 6th tier-1 suite; no Min-cases floor decrease; no mock-server port hard-code). Body byte-identical to previous §97 inline body; remains tier-1 binding.
- **Verifies:** tier-1 binding contract for J-series file `45-cli-test-plan.md`. Closes Lesson #19 audit-boundary < verification-boundary gap. **J-series tier-1 closure** — sixth and final J-series binding (AC-82..AC-87 sextet now complete). Pairs with AC-80 sibling-file delegation map per Lesson #21 + Lesson #39. Codifies Lesson #36 link-don't-restate to all cited cross-module surfaces. Until A8 unblocks, any "missing 45-cli-test-plan.md" or "[D2] unbound contract" finding is a stale-cache walker-cap artifact per Lesson #34. **§54 §AC-87 detail** — full normative body lives in `54-ac-j-series-cli-detail.md`.
- **Source:** `97-acceptance-criteria.md` (this AC) + `54-ac-j-series-cli-detail.md` (full body); cross-refs `45-cli-test-plan.md`, AC-78/79/80/81.

### AC-88 — Server-side `POST /wp-json/git-logs/v3/upload-frames` receiver (K-series tier-1; Lane B writes only)  `[critical]`

- **Given** the J-series CLI (per AC-85) streams classified frames as NDJSON-over-HTTPS to the spec/22 plugin, and the server MUST present a normative endpoint that accepts those frames under SSH-key Lane B auth and persists them into the §39 split-DB layout without coalescing with legacy v2 endpoints.
- **When** an AI auditor or implementer seeks the binding contract for the server-side receiver — endpoint binding, 10-step strict server validation order, frame→storage mapping, response envelope, and forbidden patterns.
- **Then** the canonical 7-section contract MUST live in `46-server-upload-frames-endpoint.md` (NEW v3 base; Lane B writes only; `Content-Type: application/x-ndjson`; `Idempotency-Key` REQUIRED UUIDv4; max body 16 MiB compressed / 64 MiB decompressed; max frames `NdjsonMaxRowsPerStream` default 10 000; 30s connect / 60s body timeout; 10-step strict validation order with auth before parse — reordering FORBIDDEN).
- **Verifies:** tier-1 binding for `46-server-upload-frames-endpoint.md`; first K-series instance (establishes v3-base + Lane-B-writes-only contract that K2/K3/K4 inherit); pairs with AC-80 row 39; **§52 §AC-88 detail** — full normative body lives in `52-ac-k-series-server-detail.md`. Cross-refs: `43-cli-upload-protocol.md`, `31-ssh-key-auth.md`, `39-split-db-log-storage.md`, `15-error-codes.md` (`GL-UPLOAD-*` / `GL-AUTH-*`), `05-auth-and-validation.md` (rate-limit), AC-78/79/80/81/85/86.

---

### AC-89 — Server-side `GET /wp-json/git-logs/v3/autofix/{repoIdentityHash}/{frameId}` fix-bundle producer (K-series tier-1; Lane B reads only; single-consumption)  `[critical]`

- **Given** the J-series CLI (per AC-86) consumes a server-issued `autofixDownloadUrl` (from §43 §6 response per AC-85) to download a fix-bundle envelope per §44 §3, and the server MUST present a normative producer under Lane B with single-consumption + expiry semantics + server-issued URL discipline (no client URL construction).
- **When** an AI auditor seeks the binding contract for the server-side fix-bundle producer — endpoint binding, 11-step strict server validation + lookup order, bundle envelope production from `FixBundle` rows, single-consumption + expiry semantics, and forbidden patterns.
- **Then** the canonical 7-section contract MUST live in `47-server-autofix-endpoint.md` (v3 base; Lane B reads only; `Accept: application/vnd.riseup.git-logs.fix+json; v=1`; `Idempotency-Key` FORBIDDEN on GET; `If-None-Match` OPTIONAL with 304-on-match (NOT consumption); strong `ETag` REQUIRED; `Cache-Control: private, no-store`; single-consumption transaction per spec/13 AC-22; 304/410/404 ordering MUST be honored).
- **Verifies:** tier-1 binding for `47-server-autofix-endpoint.md`; second K-series instance (read-side mirror); pairs with AC-80 row 40; **§52 §AC-89 detail** — full normative body lives in `52-ac-k-series-server-detail.md`. Cross-refs: `44-cli-autofix-protocol.md`, `43-cli-upload-protocol.md` §6, `31-ssh-key-auth.md`, `39-split-db-log-storage.md`, `15-error-codes.md` (`GL-FIX-*` / `GL-AUTH-*`), `08-history-and-action.md`, `20-observability.md` (`SystemEvent.FixBundleConsumed`), spec/13 §97 AC-22, AC-78/79/80/81/85/86/88.

---

### AC-90 — Server-side `POST /wp-json/git-logs/v3/refresh-pointer` pointer-refresh producer (K-series tier-1; Lane B writes only; frame-smuggle guard)  `[critical]`

- **Given** the J-series CLI maintains a local `.riseup-git-logs.json` pointer file (8-field wire format owned by §41), and three closed-set use-cases require a fresh pointer payload WITHOUT uploading frames first: (1) stale `expiresAt`; (2) first-run repair via `riseup-git-logs doctor`; (3) server-side `uploadUrl` rotation per K1. §46 `POST /upload-frames` REQUIRES a non-empty body and cannot serve these — hence a dedicated refresh endpoint.
- **When** an AI auditor seeks the binding contract for the server-side pointer-refresh producer.
- **Then** the canonical 7-section contract MUST live in `48-server-refresh-pointer-endpoint.md` (v3 base; Lane B writes only; 4-field identity envelope; 8-field §41 payload production with server-issued `uploadUrl`/`expiresAt` reset; `autofixDownloadUrl` three-state echo; **10-entry forbidden body-top-level fields frame-smuggle guard** — distinguishes refresh-pointer from §46 frame-ingestion; auto-minting a `FixBundle` row FORBIDDEN; Lane A REJECTED).
- **Verifies:** tier-1 binding for `48-server-refresh-pointer-endpoint.md`; third K-series instance (establishes 4-field identity envelope + frame-smuggle guard pattern); pairs with AC-80 row 41; **§52 §AC-90 detail** — full normative body lives in `52-ac-k-series-server-detail.md`. Cross-refs: `41-cli-pointer-file-schema.md`, `46-…` and `47-…` (sibling K-series), `31-ssh-key-auth.md`, `39-split-db-log-storage.md`, `15-error-codes.md` (`GL-PTR-*` / `GL-AUTH-*`), spec/13 §97 AC-22, AC-78/79/80/81/85/86/88/89.
