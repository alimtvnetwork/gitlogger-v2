> ⚠️ **DEPRECATED — Legacy v1 Spec (folder 21)**  
> This document is preserved for historical reference only. **Do not implement against it.**  
> The active specification is **v2** in [`spec/22-git-logs-v2/`](../../22-git-logs-v2/00-overview.md) (SQLite, no JWT, SSH-key auth).  
> See [`spec/22-git-logs-v2/00-overview.md`](../../22-git-logs-v2/00-overview.md) for the current canonical source.  
> Deprecated: 2026-04-25

---

# Acceptance Criteria — Log Push & Log Retrieval (Given / When / Then)

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Status:** Active  
**AI Confidence:** Production-Ready  
**Ambiguity:** Low

---

## Overview

Behavior-driven acceptance criteria for the two highest-traffic, highest-risk endpoints in the `git-logs` plugin:

1. **`POST /wp-json/git-logs/v1/logs/push`** — unauthenticated (no plugin JWT) but allowlist-gated CI ingestion.
2. **`GET /wp-json/git-logs/v1/logs`** and **`GET /wp-json/git-logs/v1/logs/{id}`** — JWT-authenticated, RBAC-gated retrieval.

Each criterion is written **Given / When / Then** so it can be lifted directly into a PHPUnit / Playwright / Postman test without translation. Every criterion references the canonical normative source (allowlist, JWT flow, error envelope, schema). When this file and a normative source disagree, **the normative source wins** and this file MUST be patched.

---

## Keywords

`acceptance-criteria` · `gwt` · `bdd` · `log-push` · `log-retrieval` · `security` · `rbac` · `rate-limit` · `allowlist` · `git-logs`

---

## Scoring

| Metric | Value |
|--------|-------|
| AI Confidence | Production-Ready |
| Ambiguity | Low |
| Health Score | 100/100 (A+) |

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Allowlist + envelope JWT (push gating) | [./08-allowlist-and-wildcard-matching.md](./08-allowlist-and-wildcard-matching.md) |
| JWT auth (retrieval gating) | [./05-auth-jwt-flow.md](./05-auth-jwt-flow.md) |
| Error envelope & all `GL-*` codes | [./11-error-management.md](./11-error-management.md) |
| Error codes registry (machine-readable) | [./error-codes.json](./error-codes.json) |
| `Repository` / `Pipeline` / `LogEntry` schema | [./02-database-schema-and-erd.md](./02-database-schema-and-erd.md) |
| Audit trail | ./10-audit-trail.md (`10-audit-trail` — removed in v1 deprecation) *(planned)* |
| Logging strategy (PII redaction) | [./12-logging-strategy.md](./12-logging-strategy.md) |
| Onboarding flow (token issuance prerequisites) | [./16-jwt-onboarding-and-token-usage.md](./16-jwt-onboarding-and-token-usage.md) |

---

## Conventions

- **Universal envelope.** Every response (except `GET /.well-known/jwks.json`) is the envelope from `11-…` §3. When a Then clause says `code: GL-XXX-YYY`, that is the value of `Error.Code` inside the envelope; the HTTP status is the one mapped in `11-…` §6.
- **Audit clause.** Where a Then mentions an `AuditTrail` row, it is **always** a single `INSERT` in the same transaction as the response decision. No swallow (per `11-…` R3).
- **No oracle.** Rejection responses MUST NOT differentiate cause beyond what is stated. E.g., "repo not in allowlist" and "repo disabled" are intentionally distinct (admin operability), but "wrong envelope signature" and "wrong key id" both surface as `GL-PUSH-003` (do not leak which it was).
- **Time skew.** All time-comparison checks use ±5 s skew tolerance unless a different value is specified by the normative source (e.g., envelope JWT uses ±60 s per `08-…`).
- **PascalCase.** All JSON field names sent or received use PascalCase per coding guideline `02-coding-guidelines/01-cross-language/11-key-naming-pascalcase.md`.

---

## Section 1 — `POST /logs/push` (Ingestion)

### 1.1 Happy Path

#### AC-PUSH-01 — Valid push for an Active, RepoUrl+Exact allowlisted repo

> **Given** a `Repository` row `R10` exists with `OwnerName="acme"`, `RepoName="widget"`, `AcceptanceModeId=RepoUrl`, `VersionModeId=Exact`, `RepositoryStatusId=Active`,  
> **And** the request carries a valid envelope JWT signed with the per-repo `LogSenderToken` of `R10`, with `iat=now`, `exp=now+60`, and a fresh 16-char `nonce`,  
> **And** the body is `{ "RepoUrl": "https://github.com/Acme/Widget", "BranchName": "main", "PipelineName": "build", "Entries": [ … 3 entries … ] }` (≤ 1 MB),  
> **When** the client `POST`s to `/wp-json/git-logs/v1/logs/push`,  
> **Then** the response is `202 Accepted` with envelope `Success=true`, `Data.AcceptedCount=3`, `Data.PipelineId` set,  
> **And** a `Pipeline` row for `(R10, "main", "build")` exists (created on this call if not already present),  
> **And** exactly 3 `LogEntry` rows exist with that `PipelineId` and the correct `OccurredAt`/`Message`/`LogSeverityId`,  
> **And** exactly **one** `AuditTrail` row exists with `Action="LogPush"`, `Outcome="Success"`, `RepositoryId=R10`, `DetailsJson.matchedTier=1`, `DetailsJson.acceptedCount=3`.

#### AC-PUSH-02 — Pipeline auto-creation is idempotent

> **Given** AC-PUSH-01 has already run once (so the `Pipeline` row exists),  
> **When** a second valid push for the same `(RepositoryId, BranchName, PipelineName)` arrives with 5 new entries,  
> **Then** the response is `202 Accepted` with `Data.AcceptedCount=5`,  
> **And** the same `PipelineId` is returned,  
> **And** the total `LogEntry` count for that pipeline is 8,  
> **And** no `Pipeline` `INSERT` was attempted (the `IdxPipeline_RepoBranchName` UNIQUE index is not violated).

#### AC-PUSH-03 — Wildcard version match (Tier 2)

> **Given** `Repository` row `R11` with `AcceptanceModeId=RepoUrl`, `VersionModeId=Wildcard`, `RepoName="widget"`, `Active`,  
> **And** no Tier-1 row matches,  
> **When** a valid push arrives for `https://github.com/acme/widget-v3`,  
> **Then** the response is `202 Accepted`,  
> **And** the `AuditTrail` row has `DetailsJson.matchedRepositoryId=R11`, `DetailsJson.matchedTier=2`.

#### AC-PUSH-04 — OwnerWildcard fallback (Tier 3)

> **Given** only `Repository` row `R12` exists with `AcceptanceModeId=OwnerWildcard`, `OwnerName="acme"`, `Active`,  
> **When** a valid push arrives for `https://github.com/acme/anything-else`,  
> **Then** the response is `202 Accepted`,  
> **And** `AuditTrail.DetailsJson.matchedTier=3`.

---

### 1.2 Allowlist Rejection

#### AC-PUSH-05 — Repository not in allowlist

> **Given** no `Repository` row matches `(owner=other, repo=widget)` at any tier,  
> **When** a structurally valid push arrives for `https://github.com/other/widget`,  
> **Then** the response is `403` with `Error.Code="GL-PUSH-001"`,  
> **And** `AuditTrail` records `Action="LogPush"`, `Outcome="Rejected"`, `DetailsJson.rejectReason="NotRegistered"`,  
> **And** no `Pipeline` or `LogEntry` row was created.

#### AC-PUSH-06 — Repository is disabled (more-specific shadowing wins)

> **Given** `Repository` `R30` matches at Tier 1 with `RepositoryStatusId=Disabled`,  
> **And** `Repository` `R31` would match at Tier 3 (`OwnerWildcard`) with `Active`,  
> **When** a valid envelope push arrives for `acme/widget`,  
> **Then** the response is `403` with `Error.Code="GL-PUSH-002"` (Disabled, **not** fallback to R31),  
> **And** `AuditTrail.DetailsJson.matchedRepositoryId=R30`, `rejectReason="Disabled"`.

#### AC-PUSH-07 — Sibling repo still accepted under same OwnerWildcard

> **Given** the same setup as AC-PUSH-06,  
> **When** a valid push arrives for `acme/sibling` (no Tier-1 match for sibling),  
> **Then** the response is `202 Accepted` via `R31` (`matchedTier=3`).

---

### 1.3 Envelope JWT Failures

#### AC-PUSH-08 — Bad signature

> **Given** an allowlisted repo `R10`,  
> **When** the request envelope JWT is signed with the wrong secret,  
> **Then** the response is `401` with `Error.Code="GL-PUSH-003"`,  
> **And** the response body MUST NOT reveal whether the failure was wrong-key vs wrong-signature (no oracle),  
> **And** `AuditTrail.DetailsJson.rejectReason="BadSignature"`.

#### AC-PUSH-09 — Expired envelope

> **When** the envelope JWT has `exp = now − 120`,  
> **Then** the response is `401 GL-PUSH-004`,  
> **And** `AuditTrail.DetailsJson.rejectReason="Expired"`.

#### AC-PUSH-10 — TTL too long (anti-downgrade)

> **When** the envelope JWT has `exp - iat > 300` (max envelope TTL = 5 min per `08-…`),  
> **Then** the response is `401 GL-PUSH-005` even if the signature is valid,  
> **And** `AuditTrail.DetailsJson.rejectReason="TtlTooLong"`.

#### AC-PUSH-11 — Replay detected

> **Given** a successful push has been recorded with `(RepositoryId=R10, nonce="abc…16chars")` within the last 10 minutes,  
> **When** the same `(RepositoryId, nonce)` is presented again (even with a fresh signature),  
> **Then** the response is `401 GL-PUSH-006`,  
> **And** `AuditTrail` records `Action="LogPush"`, `Outcome="Rejected"`, `DetailsJson.rejectReason="Replayed"`,  
> **And** an additional `AuditTrail` row of `Action="SuspectedReplayAttack"` is written for SIEM consumption.

#### AC-PUSH-12 — Malformed envelope

> **When** the envelope JWT is missing the `nonce` claim, or `nonce` length is < 16,  
> **Then** the response is `400 GL-PUSH-007`,  
> **And** the response MUST NOT echo the offending claim back (no payload reflection).

#### AC-PUSH-13 — Algorithm-confusion attempt

> **When** the envelope JWT header has `alg="none"` or `alg="RS256"` (envelope is HS256-only),  
> **Then** the response is `401 GL-PUSH-003` (treated as bad signature; same code, no extra detail),  
> **And** `AuditTrail.DetailsJson.rejectReason="BadSignature"`,  
> **And** `AuditTrail.DetailsJson.attemptedAlg` records the offending value (server-side only — never returned to the client).

---

### 1.4 Body & Provider

#### AC-PUSH-14 — Provider unsupported

> **When** `RepoUrl` resolves to anything other than `github.com` (e.g., `gitlab.com/acme/widget`),  
> **Then** the response is `400 GL-PUSH-008`,  
> **And** the rejection happens **before** envelope verification (no signature oracle for non-GitHub URLs).

#### AC-PUSH-15 — Body exactly at 1 MB (boundary inclusive)

> **Given** a request whose post-decompression body is exactly 1,048,576 bytes,  
> **When** the push is otherwise valid,  
> **Then** the response is `202 Accepted` (the cap is **inclusive** at exactly 1 MB).

#### AC-PUSH-16 — Body 1 byte over

> **When** the post-decompression body is 1,048,577 bytes,  
> **Then** the response is `413 GL-PUSH-009`,  
> **And** the request body is NOT parsed beyond the size check (no JSON parse, no envelope verify, no DB writes),  
> **And** `AuditTrail.DetailsJson.rejectReason="PayloadTooLarge"`.

#### AC-PUSH-17 — Compressed body that decompresses past the cap

> **Given** a `Content-Encoding: gzip` request whose compressed length is 200 KB and decompressed length is 1.5 MB,  
> **When** the request is processed,  
> **Then** the decompression is bounded — implementations MUST stop reading at `1,048,577` bytes and respond `413 GL-PUSH-009`,  
> **And** memory usage during the rejection MUST NOT exceed `2 × cap = 2 MB` (no zip-bomb).

---

### 1.5 Rate Limit (per resolved `RepositoryId`)

#### AC-PUSH-18 — 60th request still passes, 61st throttled

> **Given** the per-repo bucket is 60 requests / 60 s sliding window,  
> **When** 61 valid pushes for the same resolved `RepositoryId` arrive within 30 s,  
> **Then** requests 1–60 each return `202 Accepted`,  
> **And** request 61 returns `429 GL-RATE-001` with `Retry-After` header in `[1, 60]`,  
> **And** `AuditTrail.DetailsJson.rejectReason="RateLimited"` for request 61.

#### AC-PUSH-19 — Window slides

> **Given** AC-PUSH-18 has just rejected request 61,  
> **When** the client waits 60 s and pushes again,  
> **Then** the response is `202 Accepted`.

#### AC-PUSH-20 — OwnerWildcard shares one bucket per resolved id

> **Given** an `OwnerWildcard` row `R12` resolves both `acme/repoA` and `acme/repoB`,  
> **When** 60 pushes arrive across `repoA` and `repoB` combined within 60 s,  
> **Then** the 61st (regardless of which repo it claims) returns `429 GL-RATE-001`. *(Documented trade-off — see `08-…` Open Item OI-ALLOW-03.)*

---

### 1.6 Push — Cross-cutting Security

#### AC-PUSH-21 — No auth header is required, but if present it MUST be ignored

> **When** the push request includes an `Authorization: Bearer …` header (e.g., a stale plugin JWT),  
> **Then** the header is ignored entirely; gating is envelope-JWT-only,  
> **And** the response and `AuditTrail` are identical to an otherwise-equivalent request without the header.

#### AC-PUSH-22 — `ActorUserId` is NULL on every push audit row

> **For** every `AuditTrail` row whose `Action="LogPush"`,  
> **Then** `ActorUserId IS NULL` (push is anonymous-by-design),  
> **And** `RepositoryId` is set whenever the allowlist resolved (success **or** Disabled rejection),  
> **And** `RepositoryId IS NULL` for `NotRegistered` and `ProviderUnsupported` rejections.

#### AC-PUSH-23 — DB error during persistence is not swallowed

> **Given** the envelope and allowlist both pass,  
> **When** the `INSERT` into `LogEntry` raises a DB error (e.g., disk full),  
> **Then** the controller MUST NOT return `202`,  
> **And** the response is `500 GL-INT-001`,  
> **And** `AuditTrail` records `Action="LogPush"`, `Outcome="Error"`, `DetailsJson.exceptionClass`/`stackHash` (per `11-…` R3),  
> **And** the original exception is re-thrown into the WP error log.

#### AC-PUSH-24 — Secrets never leak

> **For** every push response (success, rejection, or error),  
> **Then** the response body MUST NOT contain the raw envelope JWT, the per-repo `LogSenderToken`, the `Authorization` header value, or any private key bytes (verified by a redaction lint over response fixtures, per `12-…` §6).

---

## Section 2 — `GET /logs` and `GET /logs/{id}` (Retrieval)

### 2.1 Happy Path

#### AC-RETR-01 — List with valid JWT and minimal filter

> **Given** a `User` `U7` with role `LogReader`, a valid access JWT (`sub="user:7"`, `exp=now+3600`, `kid` in JWKS, signature valid),  
> **And** at least 25 `LogEntry` rows visible to U7's role scope,  
> **When** the client `GET`s `/wp-json/git-logs/v1/logs?RepositoryId=10&Limit=20`,  
> **Then** the response is `200` with envelope `Success=true`,  
> **And** `Data.Items` contains exactly 20 rows ordered by `OccurredAt DESC, LogEntryId DESC`,  
> **And** `Data.NextCursor` is a non-empty opaque string,  
> **And** exactly **one** `AuditTrail` row exists with `Action="LogQuery"`, `Outcome="Success"`, `ActorUserId=7`, `DetailsJson.filter`/`limit`/`returnedCount` populated.

#### AC-RETR-02 — Cursor pagination is stable

> **Given** the response from AC-RETR-01,  
> **When** the client re-requests with `Cursor=<NextCursor>&Limit=20`,  
> **Then** the next page returns rows that strictly follow the last row of the previous page in `(OccurredAt DESC, LogEntryId DESC)` order,  
> **And** there is **no** overlap (no `LogEntryId` appears on both pages),  
> **And** there are **no** gaps caused by inserts that happened between the two calls (cursor encodes both `OccurredAt` and `LogEntryId` for tie-break).

#### AC-RETR-03 — Single entry by id

> **Given** `LogEntry` `LE99` exists and is visible to U7's role scope,  
> **When** the client `GET`s `/wp-json/git-logs/v1/logs/99`,  
> **Then** the response is `200` with `Data` equal to the `VwLogEntryDetail` projection of LE99,  
> **And** `AuditTrail.Action="LogQuery"`, `DetailsJson.logEntryId=99`.

---

### 2.2 Auth Failures

#### AC-RETR-04 — Missing Authorization header

> **When** the request has no `Authorization` header,  
> **Then** the response is `401 GL-AUTH-007`.

#### AC-RETR-05 — Malformed Authorization header

> **When** the header is `Authorization: Token abc` (wrong scheme) or `Authorization: Bearer` (no value),  
> **Then** the response is `401 GL-AUTH-007`.

#### AC-RETR-06 — JWT alg=none / algorithm confusion

> **When** the JWT header has `alg="none"` or any non-`RS256` value,  
> **Then** the response is `401 GL-AUTH-002` returned **before** any signature operation is attempted,  
> **And** the JWT library MUST be invoked with `RS256` pinned (no auto-select), per `05-…` §7.1.

#### AC-RETR-07 — Unknown `kid`

> **When** the JWT's `kid` is not in the cached JWKS,  
> **Then** the verifier performs **one** JWKS refresh; if still not found, the response is `401 GL-AUTH-002`.

#### AC-RETR-08 — Expired JWT

> **When** the JWT's `exp` is in the past (beyond ±5 s skew),  
> **Then** the response is `401 GL-AUTH-002`,  
> **And** `AuditTrail.Action="AuthFail"`, `Outcome="Rejected"`.

#### AC-RETR-09 — `exp - iat > 86400` (anti-downgrade)

> **When** an attacker forges (and self-signs with a stolen key) a JWT whose `exp - iat = 30 days`,  
> **Then** even with a valid signature against a JWKS key, the response is `401 GL-AUTH-002`.

#### AC-RETR-10 — Locked user

> **Given** `User.IsLocked=1` for U7,  
> **When** U7's JWT (still cryptographically valid) is presented,  
> **Then** the response is `423 GL-AUTH-005`,  
> **And** `AuditTrail.Action="AuthFail"`, `Outcome="Rejected"`, `DetailsJson.reason="UserLocked"`.

#### AC-RETR-11 — `jti` on the denylist (logout)

> **Given** U7 has called `POST /auth/logout` with the JWT in question,  
> **When** the same JWT is replayed against `GET /logs`,  
> **Then** the response is `401 GL-AUTH-002`,  
> **And** the denylist hit is served from the object cache (per `05-…` §9.3) — no DB SELECT for the denylist on the hot path.

#### AC-RETR-12 — Bulk-revocation watermark

> **Given** an admin has bulk-revoked U7's sessions (sets `gitlogs_user_jwt_min_iat[7]=T`),  
> **When** any JWT for `sub="user:7"` with `iat < T` is presented,  
> **Then** the response is `401 GL-AUTH-002` even though the `jti` is not individually denylisted.

---

### 2.3 RBAC

#### AC-RETR-13 — User without `LogReader` role

> **Given** U8 has only role `RepoAdmin` (no `LogReader`),  
> **When** U8 calls `GET /logs?RepositoryId=10`,  
> **Then** the response is `403 GL-RBAC-001`,  
> **And** the response MUST NOT include `Data.Items` (no partial-data leak),  
> **And** `AuditTrail.Action="LogQuery"`, `Outcome="Rejected"`, `DetailsJson.reason="MissingRole"`.

#### AC-RETR-14 — Role snapshot vs live re-check on sensitive ops

> **Given** U7 holds a JWT issued when U7 had `LogReader`,  
> **And** an admin has since removed the `LogReader` role from U7 (live DB),  
> **When** U7 calls `GET /logs`,  
> **Then** the response is `403 GL-RBAC-001` (sensitive ops re-check live `UserRole`, per `05-…` §5 note).

#### AC-RETR-15 — RepositoryId scoping (multi-tenant safety)

> **Given** U7's `LogReader` grant is scoped to `RepositoryId=10` (via `UserRole.ScopeJson` or equivalent),  
> **When** U7 requests `/logs?RepositoryId=11`,  
> **Then** the response is `403 GL-RBAC-001`,  
> **And** the response body MUST NOT confirm whether `RepositoryId=11` exists (no enumeration oracle).

#### AC-RETR-16 — `GET /logs/{id}` for an entry outside scope

> **Given** `LogEntry` `LE500` belongs to `RepositoryId=11` (outside U7's scope),  
> **When** U7 requests `/logs/500`,  
> **Then** the response is `404 GL-RES-001` (not `403`) — out-of-scope MUST be indistinguishable from non-existent (avoid id-enumeration oracle).

---

### 2.4 Input Validation

#### AC-RETR-17 — `Limit` out of range

> **When** `Limit=0`, `Limit=-1`, `Limit=10001`, or `Limit="abc"`,  
> **Then** the response is `400 GL-VAL-001` with `Error.Details[]` listing the offending field,  
> **And** no DB query is run.

#### AC-RETR-18 — Default `Limit` cap

> **When** `Limit` is omitted,  
> **Then** the server applies `Limit=50`,  
> **When** `Limit=10000`,  
> **Then** the server applies `Limit=10000` (max),  
> **When** `Limit=10001`,  
> **Then** the response is `400 GL-VAL-001`.

#### AC-RETR-19 — Invalid cursor

> **When** `Cursor` is not a base64url-decodable HMAC-signed token, or its HMAC fails verification,  
> **Then** the response is `400 GL-VAL-001`,  
> **And** the response MUST NOT distinguish "malformed" vs "tampered" (one code, no oracle).

#### AC-RETR-20 — Date-range filter validation

> **When** `OccurredAfter` > `OccurredBefore`, or either is not RFC 3339 UTC,  
> **Then** the response is `400 GL-VAL-001`.

#### AC-RETR-21 — SQL injection attempt

> **When** any string filter (`BranchName`, `PipelineName`, `CommitSha`, `Search`) contains SQL metacharacters (`'`, `"`, `;`, `--`, `/*`, `*/`, `\`),  
> **Then** the request is processed via parameterized queries (`$wpdb->prepare` with `%s`/`%d` placeholders) and either returns an empty result (`Data.Items=[]`) or `400 GL-VAL-001` if the field has a strict format (e.g., `CommitSha` must match `^[0-9a-f]{40}$`),  
> **And** the SQL query log MUST show the metacharacters as **bound parameters**, never as inlined literals (verified by enabling `SAVEQUERIES` in test).

#### AC-RETR-22 — `RepositoryId` must be a positive integer

> **When** `RepositoryId="10; DROP TABLE LogEntry"`,  
> **Then** the response is `400 GL-VAL-001`,  
> **And** the request never reaches the SQL layer (rejected by the schema validator).

---

### 2.5 Rate Limit & Abuse

#### AC-RETR-23 — Per-user retrieval bucket

> **Given** a per-user bucket of 600 requests / 60 s,  
> **When** U7 issues 601 retrievals in 30 s,  
> **Then** the 601st returns `429 GL-RATE-001` with `Retry-After`.

#### AC-RETR-24 — IP-based fallback for failed-auth requests

> **When** more than 30 requests from the same IP in 60 s fail at the JWT-verify stage (any `GL-AUTH-*`),  
> **Then** the 31st is short-circuited to `429 GL-RATE-001` **without** attempting JWT verification (defence against credential-stuffing).

---

### 2.6 Retrieval — Cross-cutting Security

#### AC-RETR-25 — Response never includes secrets

> **For** every retrieval response,  
> **Then** the body MUST NOT contain values from any field in the redaction allowlist (`12-…` §6): no `TokenHash`, no `LogSenderTokenVerifier`, no JWT private blob, no full `Authorization` header value (verified by redaction lint over fixtures).

#### AC-RETR-26 — `MetadataJson` is returned as-is (no HTML rendering)

> **Given** a `LogEntry` whose `MetadataJson` contains `{"html":"<script>alert(1)</script>"}`,  
> **When** the entry is returned,  
> **Then** the JSON value is returned **exactly** (the API is not responsible for sanitization),  
> **And** the Content-Type is `application/json; charset=utf-8` (not HTML),  
> **And** `X-Content-Type-Options: nosniff` is set,  
> **And** any UI that consumes this MUST sanitize before DOM injection (per global `input-validation-security` guidance).

#### AC-RETR-27 — CORS disallows credentials by default

> **When** a browser issues a cross-origin retrieval request with `Origin: https://evil.example`,  
> **Then** the response does **not** include `Access-Control-Allow-Credentials: true` for any unallowlisted origin,  
> **And** `Access-Control-Allow-Origin` is set only to origins listed in the `gitlogs_cors_allowed_origins` filter (default empty → no CORS, same-origin only).

#### AC-RETR-28 — Audit row written on every call (success, reject, error)

> **For** every invocation of `GET /logs` or `GET /logs/{id}` — auth-pass or auth-fail, RBAC-pass or RBAC-fail, internal error — exactly **one** `AuditTrail` row exists for that request, with the matching `Outcome ∈ {Success, Rejected, Error}` and a `TraceId` that matches the response envelope's `TraceId`.

#### AC-RETR-29 — Server-side pagination never loads all rows

> **For** any retrieval, regardless of total matching rows,  
> **Then** the SQL query MUST include `LIMIT (Limit + 1)` (the +1 detects whether a next page exists),  
> **And** memory usage for the response MUST scale with `Limit`, not with the total match count (verified by a fixture with 1,000,000 matching rows and `Limit=50`: peak memory delta < 5 MB).

#### AC-RETR-30 — DB error is not swallowed

> **Given** a syntactically valid request,  
> **When** the underlying SELECT raises a DB error (e.g., view missing after a botched migration),  
> **Then** the response is `500 GL-INT-001`,  
> **And** `AuditTrail.Outcome="Error"`, `DetailsJson.exceptionClass`/`stackHash` set,  
> **And** the exception is re-thrown into the WP error log,  
> **And** the response body MUST NOT contain the SQL string, table names, or stack trace (per `11-…` R9).

---

## Section 3 — Coverage Matrix

| Endpoint | Happy | Allowlist | Envelope JWT | Auth JWT | RBAC | Validation | Rate Limit | Security | Total |
|---|---|---|---|---|---|---|---|---|---|
| `POST /logs/push` | 4 | 3 | 6 | — | — | 4 | 3 | 4 | **24** |
| `GET /logs[/{id}]` | 3 | — | — | 9 | 4 | 6 | 2 | 6 | **30** |
| **Total** | | | | | | | | | **54** |

Every criterion is implementable against the existing schema (`02-…`), allowlist (`08-…`), JWT subsystem (`05-…`), and error envelope (`11-…`). No criterion depends on a planned-but-unwritten module beyond the `Open Items` listed below.

---

## Section 4 — Open Items

| # | Item | Notes |
|---|------|-------|
| OI-AC-01 | `UserRole.ScopeJson` (referenced by AC-RETR-15) is not yet in `02-database-schema-and-erd.md`. Either add the column (preferred) or downgrade scoping ACs to "out of scope for v1". |
| OI-AC-02 | The `IP-based fallback` bucket of AC-RETR-24 needs storage choice (object cache vs DB transient). Same backend as the JWT denylist (`05-…` §9) is the obvious answer; confirm and write into `12-…`. |
| OI-AC-03 | `SuspectedReplayAttack` audit action (AC-PUSH-11) needs to be added to the `AuditAction` enum in `01-glossary-and-enums.md`. |
| OI-AC-04 | Decide cursor signing key rotation cadence — currently the cursor HMAC key (AC-RETR-19) lives in the same option as the JWT keypair; that conflates two unrelated rotations. Split into `gitlogs_cursor_hmac_key`. |
| OI-AC-05 | `gitlogs_cors_allowed_origins` filter (AC-RETR-27) needs default documentation in admin UI (`03-admin-ui.md`, planned). |

---

*Behavior-driven, blind-implementable. Every Then clause maps to an existing `GL-*` code or schema row. Security checks are explicit — no oracle, no swallow, no secret leak.*
