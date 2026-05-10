---
kind: tracker
description: Consolidated audit findings tracker for git-logs App spec. Not a contract module — exempt from missing-contract / untestable rubric findings.
---

# Consolidated Audit Findings — `git-logs` App Specification

**Document ID:** `AUDIT-GL-2026-04-25`  
**Version:** 1.3.1  
**Updated:** 2026-05-10 (Session 44 audit-task A-24 — lockstep tail sweep: invariant #5 stale "D5 implementation deferred" qualifier retired in-place — D5 shipped as Active gate #13 in Sess-38 A-18. No invariant text/contract change; editorial-only patch bump.)
<!-- h10-verified-phase: 32 -->
**Audit Mode:** Spec-only (no code reviewed)  
**Scope:** every file in `spec/_archive/21-git-logs-v1/`  
**Status:** Open · awaiting remediation  
**AI Confidence:** Production-Ready  
**Ambiguity:** Low

---

## How to Use This Document

This is the **single source of truth** for every critical observation against the current `git-logs` App spec. Each finding is independently numbered, linked to a file path with a precise line anchor, and includes an **evidence snippet** copied verbatim from the audited file. Auditors and downstream AIs MUST resolve findings in the order printed (severity ↓, then ID ↑).

| Field | Meaning |
|---|---|
| **ID** | Stable identifier `F-NN` for cross-referencing |
| **Status** | One of: **Open** (default — awaiting remediation), **In progress** (PR open or active work), **Resolved** (fix landed; kept for traceability with link to the closing commit), **De-scoped (archive-only)** (target file is under `spec/_archive/` and out of active scope-lock — see [Appendix Z](#appendix-z--de-scoped-low-findings-archive-only)). De-scoped findings MUST collapse to a 1-line stub (no evidence/why-fail/fix bodies) and MUST NOT count toward the active severity rollup. |
| **Severity** | Critical / High / Medium / Low |
| **Category** | Coverage · Correctness · Security · Edge Cases · Governance · Maintainability · Testability · Scalability |
| **File** | Audited spec path (clickable) |
| **Line(s)** | Where the issue is anchored (inclusive) |
| **Evidence** | Verbatim snippet from the file (truncated to ≤ 4 lines per snippet) |
| **Why it fails** | One sentence describing the gap or contradiction |
| **Required fix** | Concrete, actionable remediation |
| **Linked audit IDs** | Cross-references to Phase-2 audit (`P2-GL-NN`) and consistency checklist rows |

> **Correction notice.** This document supersedes the Phase-2 audit (`spec/25-app-issues/01-phase-2-git-logs-audit/00-overview.md`) wherever they disagree. The Phase-2 audit treated `02-database-schema-and-erd.md` and parts of `08-allowlist-and-wildcard-matching.md` as "missing"; line-anchored evidence below proves both files exist and are substantive. Findings have been re-scored accordingly.

---

## Severity Roll-Up

| Severity | Count |
|---|---:|
| Critical | 5 |
| High | 9 |
| Medium | 8 |
| Low | 0 *(2 de-scoped — see [Appendix Z](#appendix-z--de-scoped-low-findings-archive-only))* |
| **Active total** | **22** |
| De-scoped (archive-only) | 2 |
| **Grand total** | **24** |

---

## Findings

---

### F-01 — REST endpoint contracts are not consolidated

**Severity:** Critical · **Category:** Coverage · **Linked:** P2-GL-09, Checklist A1

**File:** `spec/_archive/21-git-logs-v1/00-overview.md` · **Lines:** 62

**Evidence:**
```
| 04 | [04-rest-api-endpoints.md](./04-rest-api-endpoints.md) | REST endpoints with request/response schemas |
```

**Why it fails.** The inventory promises `04-rest-api-endpoints.md`, but `ls spec/_archive/21-git-logs-v1/` shows the file does not exist. Endpoints are name-dropped in `08`, `11`, `12`, and `16` (`/logs/push`, `/auth/token`, `/auth/refresh`, `/.well-known/jwks.json`, `/repositories`, `/users`, `/audit`) yet no canonical request/response schema, parameter validation, or HTTP-status table exists.

**Required fix.** Author `04-rest-api-endpoints.md` listing every route under `/wp-json/git-logs/v1` with: HTTP method, auth class, request body schema, query/path params, success envelope (PascalCase), error envelope, rate-limit class, audit-event name. Cross-link from every other file that references the route.

---

### F-02 — Cryptographic contradiction acknowledged in-line but not resolved

**Severity:** Critical · **Category:** Correctness · **Linked:** P2-GL-05, OI-ALLOW-01

**File:** `spec/_archive/21-git-logs-v1/08-allowlist-and-wildcard-matching.md` · **Lines:** 62–64, 141, 260

**Evidence:**
```
62: The envelope is signed with the per-repo `LogSenderToken` (HMAC-SHA256). Only the **hash** of `LogSenderToken` is stored server-side (`Repository.LogSenderTokenHash`, Argon2id).
64: > Because Argon2id is one-way, the server cannot directly verify HS256 against the stored hash. To bridge this, on every push the server: …
141: > The original spec said only `LogSenderTokenHash` (Argon2id) is stored. That alone makes HS256 verification mathematically impossible.
260: | OI-ALLOW-01 | HS256 verifier storage | … Decide before implementation; affects schema. |
```

**Why it fails.** The same document declares HS256 verification AND Argon2id-only storage in the schema doc, then introduces a "verifier" column in narrative form without amending `02-database-schema-and-erd.md` (which still shows only `LogSenderTokenHash` at line 143). Two implementers will produce two incompatible schemas.

**Required fix.** Pick one of:
1. **AEAD path** — amend `02-database-schema-and-erd.md` §3.3 to add column `LogSenderTokenVerifier VARBINARY(255) NOT NULL`, document derivation (`derive(AUTH_KEY, RepositoryId)`), bump schema to v3.0.0, document re-key on `AUTH_KEY` rotation.
2. **Asymmetric path** — replace HS256 with **Ed25519** envelope, store only the public key in `Repository.LogSenderPublicKey`, drop `LogSenderTokenHash` and `LogSenderTokenVerifier` entirely.

Then close `OI-ALLOW-01` and `OI-ALLOW-05`.

---

### F-03 — `RevokedJti` table is referenced everywhere but defined nowhere

**Severity:** Critical · **Category:** Correctness · **Linked:** P2-GL-06, OI-ERR-04, OI-JWT-02

**Files:**
- `spec/_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md` · Lines 49, 138, 257, 300, 398, 412
- `spec/_archive/21-git-logs-v1/11-error-management.md` · Line 475
- `spec/_archive/21-git-logs-v1/12-logging-strategy.md` · Line 128

**Evidence (16-jwt-onboarding-and-token-usage.md):**
```
49:  | **Access JWT** | RS256 | **24 h** | … Yes (`exp` + `jti` denylist on revoke) |
138: Plugin->>DB: INSERT revoked jti into JWT denylist (until exp)
257: Validate … that `jti` is not in the revocation denylist.
300: Insert the access JWT's `jti` into the revocation denylist (TTL = its remaining `exp`).
412: | OI-JWT-02 | Storage of revoked `jti` denylist | WP transient vs. dedicated table.
```

**Why it fails.** `02-database-schema-and-erd.md` lists 7 entity tables and contains no `RevokedJti` table. The denylist is required by 4 ACs and the logout flow yet has no schema, no TTL purge job, and no index strategy.

**Required fix.** Add `RevokedJti` to `02-database-schema-and-erd.md` §3 with columns `Jti CHAR(36) PK`, `RevokedAt DATETIME NOT NULL`, `ExpiresAt DATETIME NOT NULL`, `ReasonId TINYINT FK`, plus `CREATE INDEX IdxRevokedJti_ExpiresAt ON RevokedJti(ExpiresAt);`. Specify a WP-Cron job that deletes rows where `ExpiresAt < NOW() - INTERVAL 5 MINUTE`. Close `OI-JWT-02` and `OI-ERR-04`.

---

### F-04 — 10 of 16 promised content files are absent

**Severity:** Critical · **Category:** Coverage · **Linked:** P2-GL-01

**File:** `spec/_archive/21-git-logs-v1/00-overview.md` · **Lines:** 56–76

**Evidence:**
```
| 03 | [03-admin-ui.md](./03-admin-ui.md) | …
| 04 | [04-rest-api-endpoints.md](./04-rest-api-endpoints.md) | …
| 05 | [05-auth-jwt-flow.md](./05-auth-jwt-flow.md) | …
| 06 | [06-auth-wordpress-bridge.md](./06-auth-wordpress-bridge.md) | …
| 07 | [07-log-push-flow.md](./07-log-push-flow.md) | …
| 09 | [09-log-retrieval-flow.md](./09-log-retrieval-flow.md) | …
| 10 | [10-audit-trail.md](./10-audit-trail.md) | …
| 13 | [13-coding-guidelines-applied.md](./13-coding-guidelines-applied.md) | …
| 14 | [14-acceptance-criteria.md](./14-acceptance-criteria.md) | …
| 15 | [15-blind-audit-checklist.md](./15-blind-audit-checklist.md) | …
| 97 | [97-acceptance-criteria.md](./97-acceptance-criteria.md) | …
| 98 | [98-changelog.md](./98-changelog.md) | …
| 99 | [99-consistency-report.md](./99-consistency-report.md) | …
```

`ls` confirms only `00, 01, 02, 08, 11, 12, 16, 17` are present.

**Why it fails.** The inventory and the filesystem disagree by 13 rows (10 content + 3 governance). A blind AI consuming this index will fabricate content for the missing rows.

**Required fix.** Author every missing file using the templates in `spec/01-spec-authoring-guide/03-required-files.md`. Priority order: `10-audit-trail.md` (consider de-duplication with `12-logging-strategy.md`) → `04` → `05` → `09` → `07` → `06` → `03` → `13` → `14`/`15`. Generate `97`, `98`, `99` last.

---

### F-05 — Mandatory governance trio missing

**Severity:** Critical · **Category:** Governance · **Linked:** P2-GL-02, P2-GL-03, P2-GL-04

**File:** `spec/_archive/21-git-logs-v1/` (folder) · **Lines:** N/A (file absence)

**Evidence:** `ls spec/_archive/21-git-logs-v1/` returns no `97-acceptance-criteria.md`, `98-changelog.md`, or `99-consistency-report.md`.

**Why it fails.** Per `spec/01-spec-authoring-guide/03-required-files.md` the health-score formula requires `99-consistency-report.md`; the inventory in `00-overview.md` row 97/98/99 promises all three. Module health cannot exceed 75 % until they exist.

**Required fix.** Generate the three files from the canonical templates. Seed `98-changelog.md` with v1.0.0 entries plus the additions for files `08`, `11`, `12`, `16`, `17`. Roll up every `AC-*` ID from `08`, `11`, `12`, `16`, `17` into `97-acceptance-criteria.md`.

---

### F-06 — `error-codes.json` registry not present

**Severity:** High · **Category:** Governance · **Linked:** P2-GL-22, Checklist A6

**File:** `spec/_archive/21-git-logs-v1/11-error-management.md` · **Lines:** ~395 (representative)

**Evidence:**
```
395: | `GL-PUSH-009` | 413 | Request body exceeds 1 MB. | `PAYLOAD_TOO_LARGE`. |
```

**Why it fails.** The file declares 30+ error codes (`GL-AUTH-*`, `GL-VAL-*`, `GL-PUSH-*`, `GL-RATE-*`, `GL-SYS-*`) but no machine-readable `error-codes.json` exists, contrary to `spec/01-spec-authoring-guide/03-required-files.md`.

**Required fix.** Generate `spec/_archive/21-git-logs-v1/error-codes.json` listing every code with `code`, `httpStatus`, `namespace`, `userMessageKey`, `debugOnly`. Add a linter rule: every `GL-*` mention in markdown must appear in the JSON.

---

### F-07 — Trusted-proxy CIDR source is configurable but never specified

**Severity:** High · **Category:** Security · **Linked:** P2-GL-07, OI-LOG-02

**File:** `spec/_archive/21-git-logs-v1/12-logging-strategy.md` · **Lines:** 260, 267

**Evidence:**
```
260: Trust chain MUST be configurable. Default order, evaluated only when the immediate peer matches a configured trusted-proxy CIDR list:
267: If the immediate peer is **not** in the trusted-proxy list, only `REMOTE_ADDR` is used and proxy headers are logged as `details.untrustedProxyHeaders` for audit.
```

**Why it fails.** The spec says the CIDR list is "configured" but never names the WP option, default value, Admin-UI surface, or precedence rule. IP-spoofing risk; rate-limit + audit attribution become forgeable.

**Required fix.** Declare WP option `gitlogs_trusted_proxies` (CSV of CIDRs, default empty). Document the option and editor in `03-admin-ui.md` (when authored). Specify precedence: peer IP > `X-Forwarded-For` only when peer ∈ CIDRs.

---

### F-08 — Refresh-token retry / clock-skew rules incomplete

**Severity:** High · **Category:** Correctness · **Linked:** P2-GL-08, OI-JWT-03

**File:** `spec/_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md` · **Lines:** 257, 283

**Evidence:**
```
257: Validate `iss`, `aud`, `exp` (with ≤ 60 s skew tolerance), and that `jti` is not in the revocation denylist.
283: Write `AuditTrail (AuthFail, Rejected)` with `eventName = RefreshTokenReuseDetected` (severity `Error`).
```

**Why it fails.** Clock skew is partially specified for access JWT validation; **refresh-token reuse detection** has no idempotency window. A network retry after a successful refresh that lost the response will trigger reuse-detection lockout for legitimate users.

**Required fix.** Add a 5-second idempotency window: refresh requests received within 5 s of a prior success, with identical token + identical client fingerprint (`User-Agent` + `Ip`), return the previously issued pair instead of triggering reuse detection. Document the window in §6.4 and add `AC-JWT-11` covering it.

---

### F-09 — `Provider::GitLab` reserved in enum but never explicitly rejected

**Status:** **De-scoped (archive-only)** · See [Appendix Z](#appendix-z--de-scoped-low-findings-archive-only). Target file lives under `spec/_archive/21-git-logs-v1/`, which is out of the active scope-lock; current §22 (`spec/22-git-logs-v2/`) supersedes the Provider enum semantics. Retained as a 1-line pointer for traceability.

---

### F-10 — 1 MB payload cap silent on encoding and chunked transfer

**Severity:** Medium · **Category:** Edge Cases · **Linked:** P2-GL-21

**File:** `spec/_archive/21-git-logs-v1/08-allowlist-and-wildcard-matching.md` · **Lines:** 47, 112

**Evidence:**
```
47:  | Max body size | **1 MB** (Locked Decision #5) |
112: Reject if Content-Length > 1 MB                 → 413 PAYLOAD_TOO_LARGE
```

**Why it fails.** The check uses `Content-Length` only. Behavior is undefined when (a) the request uses chunked transfer encoding without `Content-Length`, (b) the body is gzip-compressed (compare pre- or post-decompression?), or (c) the client lies about `Content-Length`.

**Required fix.** Specify: enforce `Content-Length` first; if absent, stream-read with hard cap at 1 MB **decompressed**; permit `Content-Encoding: gzip` with the same 1 MB decompressed cap; reject with `GL-PUSH-009`. Add `AC-ALW-13` covering the gzip case.

---

### F-11 — `traceId` precedence on conflicting headers undefined

**Severity:** Medium · **Category:** Correctness · **Linked:** P2-GL-23

**File:** `spec/_archive/21-git-logs-v1/12-logging-strategy.md` · **Lines:** 59–68

**Evidence:**
```
59: 1. Inbound `X-Request-Id` header (validated as UUIDv4 or 16+ char alphanumeric).
60: 2. Inbound `Traceparent` header (W3C Trace Context — extract `trace-id`).
65: - Echoed back as `X-Request-Id` response header.
```

**Why it fails.** When **both** headers are present with different trace IDs, behavior is undefined. The numbered list implies `X-Request-Id` wins, but the W3C standard mandates `Traceparent` precedence in distributed traces.

**Required fix.** State precedence explicitly: when both are present and well-formed, **`Traceparent.trace-id` wins**; the value of `X-Request-Id`, if different, is preserved in `details.clientRequestId`. Add `AC-LOG-09` covering the conflict case.

---

### F-12 — Indefinite log retention has no partitioning strategy

**Severity:** Medium · **Category:** Scalability · **Linked:** P2-GL-24

**Files:**
- `spec/_archive/21-git-logs-v1/00-overview.md` · Line 42
- `spec/_archive/21-git-logs-v1/02-database-schema-and-erd.md` · Line 58

**Evidence (00-overview.md):**
```
42: | 4 | Log retention | Indefinite (no rolling deletion in v1) |
```

**Evidence (02-database-schema-and-erd.md):**
```
58: | `AuditTrail` | > 2,000,000,000 (every endpoint hit) | `BIGINT` |
```

**Why it fails.** Indefinite retention combined with a 2-billion-row volume estimate and no partition strategy guarantees future migration pain. There is no documented archival, partitioning, or cold-storage plan.

**Required fix.** Add monthly partitioning by `CreatedAt` to both `AuditTrail` and `LogEntry` in `02-database-schema-and-erd.md`. Document a deferred archival job (S3-compatible) without requiring v1 implementation. Even unimplemented, the partition key prevents future cutover pain.

---

### F-13 — Rate-limit transient strategy assumes external object cache

**Severity:** Medium · **Category:** Scalability · **Linked:** P2-GL-19

**File:** `spec/_archive/21-git-logs-v1/00-overview.md` · **Lines:** 44

**Evidence:**
```
44: | 6 | Rate limit | 60 requests/min per repository (token-bucket via WP transients) |
```

**Why it fails.** WP transients fall back to autoloaded options (DB-backed) when no external object cache is present. Under burst load this creates DB hot-spots and `wp_options` autoload bloat. The assumption is undocumented.

**Required fix.** At plugin activation, call `wp_using_ext_object_cache()`; refuse to enable the rate-limiter without an external object cache, OR provide a DB fallback table `RateLimitBucket(RepositoryId INT, WindowStart DATETIME, Count INT, PK(RepositoryId, WindowStart))`. Document the choice in the locked decisions.

---

### F-14 — CORS / origin policy not declared

**Severity:** Medium · **Category:** Security · **Linked:** P2-GL-25

**File:** `spec/_archive/21-git-logs-v1/` (folder) · **Lines:** N/A (file absence)

**Evidence:** `rg -n "CORS|gitlogs_allowed_origins|Access-Control-Allow-Origin" spec/_archive/21-git-logs-v1/` returns zero hits.

**Why it fails.** WP defaults expose REST routes to any origin; App Passwords + Bearer flows are cross-origin-friendly. Without a declared CORS stance the App will either (a) be denied from legitimate dashboards or (b) leak data to malicious origins.

**Required fix.** Specify allow-list option `gitlogs_allowed_origins` (CSV of origins, default empty); reject `Origin` values not in the list with `GL-AUTH-ORIGIN-DENIED`. Push endpoint exempt (CI runners do not send `Origin`).

---

### F-15 — Schema doc disagrees with allowlist doc on `LogSenderTokenVerifier` column

**Severity:** High · **Category:** Correctness · **Linked:** F-02

**Files:**
- `spec/_archive/21-git-logs-v1/02-database-schema-and-erd.md` · Lines 128–162 (Repository table)
- `spec/_archive/21-git-logs-v1/08-allowlist-and-wildcard-matching.md` · Lines 125–127

**Evidence (02-database-schema-and-erd.md, line 143):**
```
| `LogSenderTokenHash` | VARCHAR(255) | NOT NULL | Argon2id of per-repo HMAC secret |
```

**Evidence (08-allowlist-and-wildcard-matching.md, lines 125–127):**
```
(a) Repository.LogSenderTokenHash       (Argon2id, for offline audits / future migrations)
(b) Repository.LogSenderTokenVerifier   (HMAC-SHA256 key wrapped with WP AUTH_KEY)
```

**Why it fails.** `08` introduces a column that `02` does not declare. Two implementers reading the two files will produce two different `Repository` schemas.

**Required fix.** After F-02 is decided, amend `02-database-schema-and-erd.md` §3.3 to either (a) add the `LogSenderTokenVerifier` column or (b) replace `LogSenderTokenHash` with `LogSenderPublicKey` (Ed25519 path). Bump schema version. Echo the change in `08` §3 step 6.

---

### F-16 — Inventory orphans: `00-overview.md` doesn't list `17-spec-consistency-checklist.md` cross-link table

**Status:** **De-scoped (archive-only)** · See [Appendix Z](#appendix-z--de-scoped-low-findings-archive-only). Target file lives under `spec/_archive/21-git-logs-v1/`, which is out of the active scope-lock; §22 has its own §99 inventory + Cross-References. Retained as a 1-line pointer for traceability.

---

### F-17 — `04-rest-api-endpoints.md` absence forces ad-hoc API contracts inside other files

**Severity:** High · **Category:** Coverage

**File:** `spec/_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md` · **Lines:** 240–260, 345

**Evidence:**
```
249: X-Request-Id: <optional client-supplied trace id>
345: Every response includes the `X-Request-Id` header for cross-referencing in `AuditTrail`.
```

**Why it fails.** Header contracts and response shapes are described in narrative form across `08`, `11`, `12`, `16` instead of in `04`. Diverging definitions are inevitable.

**Required fix.** When F-01 is closed, move every header/response declaration into `04-rest-api-endpoints.md` and replace per-file mentions with anchored links.

---

### F-18 — JWKS key rotation policy unspecified

**Severity:** High · **Category:** Security · **Linked:** P2-GL-11

**File:** `spec/_archive/21-git-logs-v1/00-overview.md` · **Lines:** 39

**Evidence:**
```
39: | 1 | JWT signing | RS256, plugin keypair (private key in WP option, public key at `/wp-json/git-logs/v1/.well-known/jwks.json`) |
```

**Why it fails.** Decision #1 locks RS256 + JWKS but `05-auth-jwt-flow.md` does not exist. There is no documented `kid` strategy, rotation cadence, or dual-key overlap window. Lost or compromised keys cannot be rotated safely.

**Required fix.** Author `05-auth-jwt-flow.md` covering: keypair generation, encrypted-at-rest storage of the private key (derived from `AUTH_KEY`), JWKS payload shape, `kid` rotation cadence (default 90 days), dual-key overlap (default 24 h).

---

### F-19 — WordPress auth bridge undocumented

**Severity:** High · **Category:** Coverage · **Linked:** P2-GL-12

**File:** `spec/_archive/21-git-logs-v1/00-overview.md` · **Lines:** 46

**Evidence:**
```
46: | 8 | WP auth bridge | Application Passwords AND cookie auth (both accepted) |
```

**Why it fails.** Two auth methods are locked but `06-auth-wordpress-bridge.md` does not exist. Capability mapping (`manage_options` → admin, custom caps → moderator/operator), nonce strategy for cookie path, and App-Password header handling are undefined.

**Required fix.** Author `06-auth-wordpress-bridge.md`. Enumerate every accepted auth method, its detection precedence, capability map, and failure code.

---

### F-20 — Admin UI specification missing, blocking every user-facing config decision

**Severity:** High · **Category:** Coverage · **Linked:** P2-GL-10, F-07, F-14

**File:** `spec/_archive/21-git-logs-v1/00-overview.md` · **Lines:** 61

**Evidence:**
```
61: | 03 | [03-admin-ui.md](./03-admin-ui.md) | WP admin menu, screens, fields, validation |
```

**Why it fails.** Several findings (F-07 trusted-proxy CIDR, F-14 CORS allow-list, future rate-limit toggle) require an Admin UI surface that does not yet exist in the spec.

**Required fix.** Author `03-admin-ui.md` covering: menu placement under Tools → Git Logs, capability checks, screens (Repositories, Users, Tokens, Audit, Settings), per-field validation, confirmation modals, secret rotation UX.

---

### F-21 — Coding-guidelines-applied document missing

**Severity:** Medium · **Category:** Maintainability · **Linked:** P2-GL-16, Checklist A2

**File:** `spec/_archive/21-git-logs-v1/00-overview.md` · **Lines:** 71

**Evidence:**
```
71: | 13 | [13-coding-guidelines-applied.md](./13-coding-guidelines-applied.md) | Master guidelines applied to PHP/WP context |
```

**Why it fails.** Without the applied-guidelines doc, downstream AI cannot resolve which master rules apply to which file (e.g., PSR-12 vs WP coding standards subset, error envelope usage, dependency injection).

**Required fix.** Author `13-coding-guidelines-applied.md` mapping each master rule to a concrete PHP/WP enforcement.

---

### F-22 — Acceptance-criteria roll-up missing — testability blocked

**Severity:** High · **Category:** Testability · **Linked:** P2-GL-03, P2-GL-17, F-05

**Files:**
- `spec/_archive/21-git-logs-v1/08-allowlist-and-wildcard-matching.md` · `AC-ALW-01..12`
- `spec/_archive/21-git-logs-v1/11-error-management.md` · `AC-ERR-*`
- `spec/_archive/21-git-logs-v1/12-logging-strategy.md` · `AC-LOG-01..08`
- `spec/_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md` · `AC-JWT-01..10`
- `spec/_archive/21-git-logs-v1/17-spec-consistency-checklist.md` · `AC-CHK-01..08`

**Why it fails.** Per-file ACs exist; no canonical roll-up in `97-acceptance-criteria.md` or `14-acceptance-criteria.md`. Test orchestration cannot iterate the full set.

**Required fix.** Generate `97-acceptance-criteria.md` listing every `AC-*` ID with stable hyperlinks back to the source file/line. Mirror in `14-acceptance-criteria.md` per the inventory.

---

### F-23 — `User-Agent` is part of the refresh idempotency fingerprint but never validated as stable

**Severity:** Medium · **Category:** Edge Cases · **Linked:** F-08

**File:** `spec/_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md` · **Lines:** 280–300

**Evidence:** Section 6.4 describes refresh-token reuse detection but does not state which client-side properties are stable enough to use as an idempotency fingerprint. A CLI agent that updates between requests will change `User-Agent` and trip lockout.

**Why it fails.** Coupling lockout to a volatile string causes false positives.

**Required fix.** Use a hash of `(Ip /24 prefix, ParsedUserAgent.product)` instead of the raw header. Document the parser. Add `AC-JWT-12` covering a `User-Agent` minor-version change.

---

### F-24 — `RevokedJti` purge cadence not specified

**Severity:** Medium · **Category:** Maintainability · **Linked:** F-03

**File:** `spec/_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md` · **Lines:** 300

**Evidence:**
```
300: Insert the access JWT's `jti` into the revocation denylist (TTL = its remaining `exp`).
```

**Why it fails.** TTL semantics are stated but no purge cadence is defined. Without a WP-Cron purge the table grows unbounded even though entries are logically expired.

**Required fix.** Schedule WP-Cron `gitlogs_purge_revoked_jti` to run hourly; delete rows where `ExpiresAt < NOW() - INTERVAL 5 MINUTE` (skew buffer). Document in `02-database-schema-and-erd.md` activation seed section.

---

## Findings — derived views (pointer)

The three cross-tab views previously inlined here (`## Findings by Severity`, `## Findings by File`, `## Findings by Category`, ~1.4 KB) duplicate data already present in the canonical `## Findings` table above (lines 52–502). Promoted to derived-view status (Phase 153 Task S25-05, Lesson #36 — link-don't-restate) to keep the §25 audit-corpus bundle under the 140 KB walker cap. Sortable/filterable views are auto-generated by §27 dashboard slot 11 (`generate-dashboard-data.cjs`) from the canonical table; consult that artifact for live severity/file/category roll-ups. The `## Remediation Order` section below remains inlined because it carries non-derivable sequencing rationale.

---

## Remediation Order

1. **Decide F-02** (cryptographic path) — unblocks F-15 and the schema bump.
2. **Resolve F-03 + F-24** (RevokedJti table + purge) — unblocks all logout/refresh ACs.
3. **Author F-01** (REST endpoints) — unblocks F-17 by absorbing scattered contracts.
4. **Backfill F-04 priority files** in dependency order (`10`→`05`→`09`→`07`→`06`→`03`→`13`).
5. **Generate F-05 governance trio** + F-06 `error-codes.json`.
6. **Close security gaps** F-07 (proxy CIDR) · F-14 (CORS) · F-18 (JWKS rotation).
7. **Address edge cases** F-08 · F-10 · F-11 · F-23.
8. **Address scalability** F-12 (partitioning) · F-13 (object cache).
9. **Polish** F-09 · F-16 · F-21 · F-22.

---

## Verification

After remediation, run:

```bash
python3 linter-scripts/check-spec-cross-links.py --root spec --repo-root .
rg -n '\b(ID|URL|JSON|JWT|IP|DB|API|HTTP|HTML|SQL|MD5)\b' spec/_archive/21-git-logs-v1
rg -n '\$is(Not|No|Non)[A-Z]' spec/_archive/21-git-logs-v1
```

**Expected:** all three return zero non-exempted hits and exit 0.

---

## Cross-References

| Reference | Location |
|---|---|
| Phase-2 audit (predecessor) | [../01-phase-2-git-logs-audit/00-overview.md](../01-phase-2-git-logs-audit/00-overview.md) |
| Spec consistency checklist (v1 git-logs) | [../../_archive/21-git-logs-v1/17-spec-consistency-checklist.md](../../_archive/21-git-logs-v1/17-spec-consistency-checklist.md) |
| Locked decisions | [./00-overview.md](./00-overview.md) §Locked Decisions |
| Database schema (v1 git-logs) | [../../_archive/21-git-logs-v1/02-database-schema-and-erd.md](../../_archive/21-git-logs-v1/02-database-schema-and-erd.md) |
| Error management (v1 git-logs) | [../../_archive/21-git-logs-v1/11-error-management.md](../../_archive/21-git-logs-v1/11-error-management.md) |
| Logging strategy (v1 git-logs) | [../../_archive/21-git-logs-v1/12-logging-strategy.md](../../_archive/21-git-logs-v1/12-logging-strategy.md) |
| JWT onboarding & usage (v1 git-logs) | [../../_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md](../../_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md) |
| Allowlist & wildcard (v1 git-logs) | [../../_archive/21-git-logs-v1/08-allowlist-and-wildcard-matching.md](../../_archive/21-git-logs-v1/08-allowlist-and-wildcard-matching.md) |
| Triage format | [../00-overview.md](../00-overview.md) |

---

## Status

**24 findings recorded.** Awaiting remediation in the order above. No code changes performed.

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Status:** Forward-looking spec — drift expected.

Phase-2 audit file (`01-phase-2-git-logs-audit`) lives one folder up at `spec/25-app-issues/01-phase-2-git-logs-audit/`. Reference is intentional cross-folder link.

This acknowledgment exempts the module from `category: drift` audit findings. See `.lovable/memory/index.md` Phase 27c note.

### Cross-cutting boilerplate — pointers (Phase 153 Task S25-04)

Two cross-cutting boilerplate sections previously inlined here (Phase-74 5-stage CI workflow yaml + Phase-82 `tracker_issue_p82` SQL DDL, ~3.6 KB combined) have been promoted to their canonical owners to keep the §25 audit-corpus bundle under the 140 KB walker cap (Lesson #29 — module-kind pin):

- **CI workflow stages (Phase 74):** the detect → validate → lint → promote → report pipeline lives in [`.github/workflows/spec-health.yml`](../../../.github/workflows/spec-health.yml). Sub-02 contributes via the `validate` stage (slot 50) and `lint` stage (slot 30 auditor). Per §27 ownership the workflow yaml is NOT duplicated in §25.
- **Tracker issue log SQL (Phase 82):** the canonical `tracker_issue_p82` DDL + indexes are owned by §28 (universal-ci-cli) and consumed cross-tracker. Sub-02 emits `tracker_slug='25-app-issues/02-consolidated-audit-findings'` rows via the standard CI runner. See [`spec/28-universal-ci-cli/00-overview.md`](../../28-universal-ci-cli/00-overview.md) for the canonical DDL and consumer contract.

See [`./lifecycle-25-app-issues-02-consolidated-audit-findings-lifecycle.mmd`](./lifecycle-25-app-issues-02-consolidated-audit-findings-lifecycle.mmd) for the visual lifecycle.

---

## v1→v2 Finding Disposition Map (A-02, Session 24)

**Purpose.** Every F-NN finding above targets a file under `spec/_archive/21-git-logs-v1/`, which is **outside** the active scope-lock (only `spec/22..28` are in scope). Without an explicit reconciliation, a blind-AI implementer reading this tracker has no way to know whether a finding is (a) already closed by a successor §22 file, (b) still-open as a v2 gap that must be carried into the §22 backlog, (c) made irrelevant by the v2 architecture, or (d) formally de-scoped. The Phase-3 audit measured this missing reconciliation as the single largest contributor to §25's blind-failure probability (~75 %). This map closes that gap by routing each F-NN to its v2 disposition and, where applicable, to the §22 file that now owns the topic.

**Disposition vocabulary.**

| Disposition | Meaning | Counts toward active rollup? |
|---|---|---:|
| **Closed-by-§22** | Topic is fully addressed in the named §22 v2 file(s); no further v1 remediation is required because v1 is archived. | No |
| **Irrelevant-in-v2** | The v1 architectural assumption that produced the finding no longer applies in v2. | No |
| **De-scoped** | Already promoted to Appendix Z; archive-only with no v2 successor needed. | No |
| **Carried-open** | The underlying concern is still a real gap in v2 and MUST be tracked as a §22 backlog item; the v1 finding text is preserved here only for traceability. | No (counted under §22, not §25) |
| **Conditional** | Disposition depends on an unresolved upstream decision (typically F-02's auth-model choice cascading to v2). | No until resolved |

**Map (F-01..F-24 → v2 disposition).**

The `Last touched` column records **`max(last material edit, last freshness verification)`** as a `Sess-NN` ID. A material edit (disposition change, owner change, notes change ≥ 1 sentence) bumps it. A **freshness verification sweep** — explicit re-confirmation in the current session that a `Carried-open` row's underlying concern still applies in v2 with no material change — also bumps it (logged in the Verification cadence ledger below). Editorial-only edits (typo, link rename) do NOT bump it. This column is the sole input signal for §27 lint rule **D5 `cohort-orphaned-finding`** (Active gate #13): any `Carried-open` row whose `Last touched` is more than **1 spec-improvement session** older than the current session triggers a §22 backlog warning. The dual-source semantics (material-edit OR verification) prevents the latent failure mode where every Carried-open row would perma-fire D5 once the original Sess-24 seed-date drifted past the 1-session window. Wired A-10 Sess-31; semantics extended A-46 Sess-56 to add the verification-sweep input.

| ID | One-line topic | Disposition | v2 owner / successor | Last touched | Notes |
|---|---|---|---|---|---|
| F-01 | REST endpoints not consolidated | Closed-by-§22 | `04-rest-api-endpoints.md` + `17-openapi.yaml` | Sess-24 | v2 ships a canonical OpenAPI source-of-truth. |
| F-02 | HMAC-vs-Argon2id contradiction | Closed-by-§22 | `05-auth-and-validation.md` + `31-ssh-key-auth.md` | Sess-24 | v2 replaces per-repo HMAC with SSH-key auth; storage contradiction dissolved. |
| F-03 | `RevokedJti` table undefined | Conditional | `02-database-schema.md` + `18-schema.sql` | Sess-24 | Closed iff v2 retains JWT denylist; otherwise Irrelevant-in-v2. Verify in §22 schema files (A-11 follow-up). |
| F-04 | 10/16 promised files absent | Irrelevant-in-v2 | §22 `99-consistency-report.md` | Sess-24 | v2 inventory is whole; v1 inventory drift is archive-bound. |
| F-05 | Governance trio missing | Closed-by-§22 | `97-acceptance-criteria.md` · `98-changelog.md` · `99-consistency-report.md` | Sess-24 | v2 ships all three. |
| F-06 | `error-codes.json` registry absent | Closed-by-§22 | `15-error-codes.md` | Sess-24 | v2 publishes the canonical error catalog (markdown source-of-truth; JSON emitted by §27 toolchain). |
| F-07 | Trusted-proxy CIDR option unspecified | Carried-open | `03-admin-ui.md` + `20-observability.md` | **Sess-56** | Verify v2 declares `gitlogs_trusted_proxies` (or v2 equivalent) and IP-resolution precedence. Open §22 backlog ticket if absent. *Sess-56 freshness sweep: still applies, no material change.* |
| F-08 | Refresh-token idempotency window | Carried-open | `05-auth-and-validation.md` | **Sess-56** | Carry only if v2 retains a refresh-token flow; otherwise reclassify Irrelevant-in-v2 jointly with F-03/F-24. *Sess-56 freshness sweep: still applies pending F-02 cascade resolution.* |
| F-09 | `Provider::GitLab` reserved-but-unrejected | De-scoped | Appendix Z | Sess-24 | Already de-scoped; pointer retained. |
| F-10 | 1 MB cap encoding/chunked-transfer silent | Carried-open | `04-rest-api-endpoints.md` + `46-server-upload-frames-endpoint.md` | **Sess-56** | Verify v2 specifies decompressed-byte cap and chunked-transfer behaviour for the upload-frames endpoint. *Sess-56 freshness sweep: still applies.* |
| F-11 | `traceId` precedence on conflicting headers | Carried-open | `20-observability.md` | **Sess-56** | Verify v2 states explicit `Traceparent` ↔ `X-Request-Id` precedence rule. *Sess-56 freshness sweep: still applies.* |
| F-12 | Indefinite log retention / no partitioning | Closed-by-§22 | `22-retention-and-pruning.md` + `39-split-db-log-storage.md` | Sess-24 | v2 ships retention policy + split-DB log storage; partitioning concern dissolved at the architecture layer. |
| F-13 | Rate-limit transient assumes ext object cache | Carried-open | `05-auth-and-validation.md` + `20-observability.md` | **Sess-56** | Verify v2 declares the rate-limit storage substrate (transient-vs-DB-vs-Redis) and an activation guard. *Sess-56 freshness sweep: still applies.* |
| F-14 | CORS / origin policy not declared | Carried-open | `04-rest-api-endpoints.md` + `30-threat-model.md` | **Sess-56** | Verify v2 declares an origin allow-list option and default stance. *Sess-56 freshness sweep: still applies.* |
| F-15 | Schema vs allowlist disagreement on `LogSenderTokenVerifier` | Closed-by-§22 | `02-database-schema.md` + `31-ssh-key-auth.md` | Sess-24 | Closed jointly with F-02; v2 schema drops the disputed column. |
| F-16 | Inventory orphan — `17-spec-consistency-checklist.md` | De-scoped | Appendix Z | Sess-24 | Already de-scoped; pointer retained. |
| F-17 | Ad-hoc API contracts inside non-API files | Closed-by-§22 | `04-rest-api-endpoints.md` + `17-openapi.yaml` | Sess-24 | Closed jointly with F-01; OpenAPI source-of-truth absorbs scattered contracts. |
| F-18 | JWKS key-rotation policy unspecified | Carried-open | `05-auth-and-validation.md` + `31-ssh-key-auth.md` | **Sess-56** | Reclassify Irrelevant-in-v2 if v2 fully replaces JWT/JWKS with SSH-key auth (verify before closure). *Sess-56 freshness sweep: still applies pending F-02 cascade resolution.* |
| F-19 | WP auth bridge undocumented | Closed-by-§22 | `25-headless-auth-notes.md` + `05-auth-and-validation.md` | Sess-24 | v2 documents the headless-auth surface explicitly. |
| F-20 | Admin UI specification missing | Closed-by-§22 | `03-admin-ui.md` | Sess-24 | v2 ships the Admin-UI spec. |
| F-21 | Coding-guidelines-applied missing | Irrelevant-in-v2 | §24 design-system + §27 toolchain | Sess-24 | Cross-cutting guideline application is owned by §24 (design system / UI rules) and §27 (toolchain enforcement) in the v2 cohort; per-folder applied-guidelines docs are not part of the v2 contract. |
| F-22 | AC roll-up missing | Closed-by-§22 | `97-acceptance-criteria.md` + `49..59-ac-*-detail.md` | Sess-24 | v2 publishes the canonical AC roll-up plus per-section AC-detail files. |
| F-23 | `User-Agent` in refresh fingerprint | Carried-open | `05-auth-and-validation.md` | **Sess-56** | Carry jointly with F-08; reclassify Irrelevant-in-v2 if v2 drops the refresh-token model. *Sess-56 freshness sweep: still applies pending F-02 cascade resolution.* |
| F-24 | `RevokedJti` purge cadence | Conditional | `22-retention-and-pruning.md` | Sess-24 | Disposition follows F-03: Closed-by-§22 if v2 retains the denylist (purge owned by retention policy); otherwise Irrelevant-in-v2. |

**Verification cadence ledger.** Every spec-improvement session that does NOT materially edit a `Carried-open` row MUST either (a) run a freshness sweep over all 8 Carried-open rows and bump their `Last touched` to the current `Sess-NN`, or (b) accept that gate #13 D5 will fire a §22 backlog warning for any row that drifts past the 1-session window. The ledger appends one row per sweep:

| Sweep session | Rows verified | Result | Next due |
|---|---|---|---|
| Sess-56 (A-46) | F-07, F-08, F-10, F-11, F-13, F-14, F-18, F-23 (all 8 Carried-open) | All still apply; no material change; F-08/F-18/F-23 remain pending F-02 cascade | Sess-57 (or next material edit, whichever is sooner) |

**Disposition rollup.**

| Disposition | Count | F-IDs |
|---|---:|---|
| Closed-by-§22 | 10 | F-01, F-02, F-05, F-06, F-12, F-15, F-17, F-19, F-20, F-22 |
| Carried-open | 8 | F-07, F-08, F-10, F-11, F-13, F-14, F-18, F-23 |
| Irrelevant-in-v2 | 2 | F-04, F-21 |
| De-scoped (Appendix Z) | 2 | F-09, F-16 |
| Conditional (depends on F-02 cascade) | 2 | F-03, F-24 |
| **Total** | **24** |  |

**Carry-forward backlog (8 v2-bound tickets).** The eight Carried-open findings (F-07, F-08, F-10, F-11, F-13, F-14, F-18, F-23) MUST be opened as §22 backlog items in the next §22 spec-improvement session and removed from any "still-applies-to-v1" interpretation. They are NOT counted in the §25 active severity rollup (the Severity Roll-Up table at the top of this document remains the authoritative §25 active count) because their remediation surface lives in §22, not in `_archive/21-git-logs-v1/`.

**Audit invariants (binding on future sessions).**

1. A blind-AI implementer reading this tracker MUST consult the disposition map before treating any F-NN as actionable; rows with disposition `Closed-by-§22` or `Irrelevant-in-v2` MUST NOT cause new edits inside `_archive/21-git-logs-v1/`.
2. Reclassifying any row (e.g. flipping a Conditional to Closed) requires citing the specific §22 file + line that resolves it, recorded in the "Notes" column of the row.
3. The disposition map MUST stay synchronised with §22's `99-consistency-report.md`; if §22 adds a new file that closes a Carried-open row, this map MUST be updated in the same PR.
4. The Severity Roll-Up table MUST NOT be retroactively edited from this map — it remains a historical snapshot of the v1 audit. Disposition is additive context, not a rewrite of the original count.
5. The `Last touched` cell is `max(last material edit, last freshness verification)`. (a) Material edit (disposition change, owner change, notes change ≥ 1 sentence) bumps it. (b) A freshness verification sweep — appending a row to the Verification cadence ledger above re-confirming the Carried-open concern still applies in v2 with no material change — also bumps it. Editorial-only edits (typo, link rename) MUST NOT bump it. The column is the sole input for §27 lint rule **D5 `cohort-orphaned-finding`** (Active gate #13): any `Carried-open` row whose `Last touched` is more than 1 spec-improvement session older than the current session triggers a §22 backlog warning. The dual-source rule eliminates the latent failure mode where every Carried-open row would perma-fire D5 once the Sess-24 seed-date drifted past the 1-session window. (Wired A-10 Sess-31; D5 shipped as Active gate #13 Sess-38 A-18; semantics extended A-46 Sess-56 to add the verification-sweep input; sweep MUST run every spec-improvement session that does not materially edit a Carried-open row.)

---

## Appendix Z — De-scoped Low Findings (archive-only)

The two findings below were carried from the Phase-2 audit but target files under `spec/_archive/21-git-logs-v1/`, which is outside the active scope-lock (only `spec/22..28` are in scope). They are **non-actionable in the current spec lifecycle** and have been promoted to this de-scoped appendix to keep the active findings walker focused on remediable work. Pointers remain at their original IDs (F-09, F-16) for cross-reference traceability with the Phase-2 audit and the §27 dashboard.

| ID | Title | Original severity | De-scope rationale | Reopen condition |
|---|---|---|---|---|
| F-09 | `Provider::GitLab` reserved in enum but never explicitly rejected | Low | Targets `_archive/21-git-logs-v1/01-glossary-and-enums.md`; superseded by §22 enum catalog (`51-ac-enum-catalog-detail.md`) which is the active source of truth. | Only if a §22 successor enum reintroduces an unhandled `Provider::GitLab` reject path. |
| F-16 | Inventory orphan — `17-spec-consistency-checklist.md` missing cross-link | Low | Targets `_archive/21-git-logs-v1/00-overview.md`; §22 owns its own `99-consistency-report.md` and Cross-References table independently. | Only if archive-tracking ever moves back in-scope. |

**Audit invariant:** de-scoped findings MUST NOT count toward active severity rollups, MUST NOT block remediation order sequencing, and MUST NOT be re-counted by the §27 dashboard's "open findings" metric. They remain visible in the canonical findings table as `Status: De-scoped` one-line stubs (no evidence/why-fail/fix bodies) so the ID space stays contiguous.

