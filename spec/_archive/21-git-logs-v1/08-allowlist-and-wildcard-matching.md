> ⚠️ **DEPRECATED — Legacy v1 Spec (folder 21)**  
> This document is preserved for historical reference only. **Do not implement against it.**  
> The active specification is **v2** in [`spec/22-git-logs-v2/`](../../22-git-logs-v2/00-overview.md) (SQLite, no JWT, SSH-key auth).  
> See [`spec/22-git-logs-v2/00-overview.md`](../../22-git-logs-v2/00-overview.md) for the current canonical source.  
> Deprecated: 2026-04-25

---

# Allowlist & Wildcard Matching — Endpoint-Level Approval for `POST /logs/push`

**Version:** 1.1.0  
**Updated:** 2026-04-25  
**Status:** Active  
**AI Confidence:** Production-Ready  
**Ambiguity:** Low

---

## Overview

`POST /wp-json/git-logs/v1/logs/push` is **unauthenticated** in the JWT/cookie sense — CI runners do not log in as plugin users — but it is **strictly controlled** by a server-side **allowlist** of approved GitHub repositories combined with a per-repo HMAC envelope JWT.

This document defines the **endpoint-level approval check** that gates that endpoint:

1. The repository must exist in the `Repository` table with `RepositoryStatusId = Active`.
2. The inbound `repoUrl` must match an entry under one of the supported acceptance modes (`RepoUrl`, `OwnerWildcard`) and version modes (`Exact`, `Wildcard`).
3. The envelope JWT must be HS256-signed with the per-repo `LogSenderToken` and not expired.
4. The push must be within the per-repo rate limit.

If any check fails, the request is rejected, audited, and counted toward security telemetry. **No error is swallowed.**

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Database schema (Repository, lookup tables) | [./02-database-schema-and-erd.md](./02-database-schema-and-erd.md) §3.3, §5 |
| Glossary (`logSenderToken`, envelope JWT, wildcard) | [./01-glossary-and-enums.md](./01-glossary-and-enums.md) |
| Logging strategy (allowlist & ingestion events) | [./12-logging-strategy.md](./12-logging-strategy.md) §4.3, §4.4 |
| Log push flow (planned) | ./07-log-push-flow.md (`07-log-push-flow` — removed in v1 deprecation) |
| Locked decisions (rate limit, payload cap, HS256) | [./00-overview.md](./00-overview.md) §Locked Decisions |

---

## 1. Endpoint Contract

| Property | Value |
|----------|-------|
| Method | `POST` |
| Path | `/wp-json/git-logs/v1/logs/push` |
| Auth | **None** (no `Authorization: Bearer <userJwt>`) |
| Required header | `X-GitLogs-Envelope: <hs256JwtSignedWithLogSenderToken>` |
| Body content type | `application/json` |
| Max body size | **1 MB** (Locked Decision #5) |
| Rate limit | **60 requests/min per repository** (Locked Decision #6) |
| Provider scope | GitHub only (Locked Decision #9) |

### 1.1 Envelope JWT (HS256)

| Claim | Required | Description |
|-------|----------|-------------|
| `repoUrl` | yes | Canonical GitHub URL of the pushing repo, e.g. `https://github.com/acme/widget-v3` |
| `branch` | yes | Branch name (≤ 255 chars) |
| `pipelineName` | yes | Pipeline identifier (≤ 255 chars) |
| `iat` | yes | Issued-at, unix seconds |
| `exp` | yes | Expiry, unix seconds, ≤ 5 min after `iat` |
| `nonce` | yes | 16+ char random; replay-protection (see §6) |

The envelope is signed with the per-repo `LogSenderToken` (HMAC-SHA256). Only the **hash** of `LogSenderToken` is stored server-side (`Repository.LogSenderTokenHash`, Argon2id).

> Because Argon2id is one-way, the server cannot directly verify HS256 against the stored hash. To bridge this, on every push the server: (a) extracts `repoUrl` from the JWT **header claim** `kid` (or unverified payload — see §3 step 3), (b) loads the candidate `Repository` row, (c) recomputes the verifier as described in §3 step 6.

---

## 2. Approval Model

### 2.1 Acceptance modes (`AcceptanceMode` lookup)

| Code | Meaning |
|------|---------|
| `RepoUrl` | Approval is for an exact `(OwnerName, RepoName)` pair. |
| `OwnerWildcard` | Approval covers **every** repository owned by `OwnerName` (user or org). |

### 2.2 Version modes (`VersionMode` lookup)

| Code | Meaning |
|------|---------|
| `Exact` | The inbound `RepoName` must equal `Repository.RepoName`. |
| `Wildcard` | The inbound `RepoName` must match `^<base>(-v[1-9][0-9]*)?$` where `<base> = Repository.RepoName`. |

### 2.3 Combined matrix

| `AcceptanceMode` | `VersionMode` | Inbound `(owner, repo)` accepted iff |
|------------------|---------------|--------------------------------------|
| `RepoUrl` | `Exact` | `owner = OwnerName` AND `repo = RepoName` |
| `RepoUrl` | `Wildcard` | `owner = OwnerName` AND `repo` matches `^RepoName(-v[1-9][0-9]*)?$` |
| `OwnerWildcard` | `Exact` | `owner = OwnerName` (repo ignored) |
| `OwnerWildcard` | `Wildcard` | `owner = OwnerName` (repo ignored; wildcard implied) |

> `RepoName-v0`, `RepoName-v01`, `RepoName-V2` (uppercase V) are **not** matches. Regex is case-sensitive; comparisons on `OwnerName` and `RepoName` are case-**insensitive** because GitHub identifiers are case-preserving but case-insensitive.

### 2.4 Resolution precedence

When more than one `Repository` row could match (e.g., an `Exact RepoUrl` and an `OwnerWildcard` for the same owner), the resolver MUST select in this order:

1. `RepoUrl` + `Exact` (most specific)
2. `RepoUrl` + `Wildcard`
3. `OwnerWildcard` + `Exact`
4. `OwnerWildcard` + `Wildcard` (least specific)

Within each tier, the row with the **most recent `UpdatedAt`** wins. The chosen row's `RepositoryId` is the one used for HMAC verification, audit attribution, rate limiting, and pipeline auto-creation.

---

## 3. Server Algorithm (per request)

```
1.  Generate / propagate traceId.
2.  Reject if Content-Length > 1 MB                 → 413 PAYLOAD_TOO_LARGE
3.  Parse X-GitLogs-Envelope WITHOUT verifying signature yet.
    Extract: repoUrl, branch, pipelineName, iat, exp, nonce.
    Reject if any required claim missing or malformed → 400 ENVELOPE_MALFORMED
4.  Normalize repoUrl → (provider, owner, repo)     (see §4)
    Reject if provider != GitHub                    → 400 PROVIDER_UNSUPPORTED
5.  Resolve candidate Repository rows per §2 precedence.
    Reject if none                                   → 403 ALLOWLIST_REJECTED_NOT_REGISTERED
    Reject if chosen.RepositoryStatusId != Active    → 403 ALLOWLIST_REJECTED_DISABLED
6.  HMAC verify:
    For the chosen row, the server holds Argon2id(LogSenderToken).
    The server CANNOT recompute LogSenderToken from the hash, so:
    - The server stores BOTH:
        (a) Repository.LogSenderTokenHash       (Argon2id, for offline audits / future migrations)
        (b) Repository.LogSenderTokenVerifier   (HMAC-SHA256 key wrapped with WP AUTH_KEY)
    - Use (b) to verify the HS256 envelope signature.
    Reject on bad signature                          → 401 ENVELOPE_BAD_SIGNATURE
    Reject if exp < now - 60s skew                   → 401 ENVELOPE_EXPIRED
    Reject if exp - iat > 300s                       → 401 ENVELOPE_TTL_TOO_LONG
    Reject if nonce already seen for this repo in last 10 min → 401 ENVELOPE_REPLAYED
7.  Rate limit check (§5).
    Reject if exceeded                                → 429 RATE_LIMITED
8.  Auto-create / fetch Pipeline (RepositoryId, BranchName, PipelineName).
9.  Validate body schema; persist LogEntry rows in a single transaction.
    On any DB error                                   → 500 INTERNAL_ERROR (re-throw, do not swallow)
10. Write ONE terminal AuditTrail row (LogPush, Success|Rejected|Error).
11. Respond 202 Accepted with { traceId, persistedCount, rejectedCount }.
```

> **Note on step 6:** The original spec said only `LogSenderTokenHash` (Argon2id) is stored. That alone makes HS256 verification mathematically impossible. This document amends the schema requirement to also persist a wrapped HMAC key. See §9 Open Item OI-ALLOW-01 for the alternative (asymmetric envelope, e.g., Ed25519 with public key stored in DB) which avoids storing any verifier key at all.

---

## 4. `repoUrl` Normalization

The same GitHub repo can be expressed many ways. The resolver MUST normalize before matching.

| Input | Normalized `(provider, owner, repo)` |
|-------|--------------------------------------|
| `https://github.com/Acme/Widget` | `(GitHub, acme, widget)` |
| `https://github.com/Acme/Widget.git` | `(GitHub, acme, widget)` |
| `https://github.com/Acme/Widget/` | `(GitHub, acme, widget)` |
| `git@github.com:Acme/Widget.git` | `(GitHub, acme, widget)` |
| `ssh://git@github.com/Acme/Widget` | `(GitHub, acme, widget)` |
| `https://github.com/Acme/Widget/tree/main` | **REJECT** (path components beyond `<owner>/<repo>` not allowed) |
| `https://gitlab.com/Acme/Widget` | **REJECT** (provider not supported in v1) |

### 4.1 Formal Grammar (PCRE, anchored, case-sensitive unless noted)

These are the **only** patterns the resolver MUST use. Implementations MUST NOT introduce additional regexes for the same purpose.

| ID | Purpose | Regex (PCRE) | Notes |
|---|---|---|---|
| `RX-OWNER` | GitHub login (user or org) | `^[A-Za-z0-9](?:[A-Za-z0-9]\|-(?=[A-Za-z0-9])){0,38}$` | 1–39 chars; no leading/trailing `-`; no `--`. Mirrors GitHub's own rule. Compared case-**insensitively** after lowercasing. |
| `RX-REPO` | GitHub repo name | `^[A-Za-z0-9._-]{1,100}$` | Cannot be `.` or `..`. Compared case-**insensitively**. |
| `RX-VERSION-SUFFIX` | Optional `-vN` tail used by `VersionMode=Wildcard` | `(?:-v[1-9][0-9]{0,3})?` | Group is optional; `N` is 1–9999, no leading zeros. |
| `RX-VERSION-WILDCARD` | Full repo match under `VersionMode=Wildcard` | `^<base><RX-VERSION-SUFFIX>$` | `<base>` = the literal `Repository.RepoName` (lowercased) re-quoted via `preg_quote($base, '/')`. Case-**sensitive** (because `<base>` is already lowercased). |
| `RX-HTTPS-URL` | HTTPS GitHub URL | `^https?://(?:www\.\|api\.)?github\.com/(?<owner>[^/]+)/(?<repo>[^/?#]+?)(?:\.git)?/?$` | Path beyond `<owner>/<repo>` rejected by the resolver before regex. |
| `RX-SSH-URL` | SSH GitHub URL | `^(?:ssh://)?git@github\.com[:/](?<owner>[^/]+)/(?<repo>[^/?#]+?)(?:\.git)?/?$` | Both `git@github.com:owner/repo.git` and `ssh://git@github.com/owner/repo` forms. |

**Reserved-name check** (after `RX-REPO` passes): the literal values `.`, `..`, and any value matching `^_+$` MUST be rejected with `400 PROVIDER_UNSUPPORTED` regardless of allowlist hits — these cannot be valid GitHub repos and indicate a malformed normalization.

### 4.2 Deterministic Normalization Algorithm

```
function normalizeRepoUrl(input: string): NormalizedRepo | NormalizationError
    1. Trim leading/trailing whitespace.
    2. If length > 2048 → return NormalizationError("URL_TOO_LONG").
    3. Split scheme:
         a. If input starts with "git@" or "ssh://"  → kind = SSH
         b. Else if input starts with "http://" or "https://" → kind = HTTPS
         c. Else → return NormalizationError("UNSUPPORTED_SCHEME")
    4. Apply RX-HTTPS-URL or RX-SSH-URL by kind.
       Capture-fail → return NormalizationError("MALFORMED_URL").
    5. Extract host (only meaningful for HTTPS); reject if host is not in
       {github.com, www.github.com, api.github.com}
       → NormalizationError("PROVIDER_UNSUPPORTED").
    6. Take captured `owner`, `repo`.
       If `repo` ends with ".git" (defensive — regex already strips), strip it.
    7. Validate `owner` against RX-OWNER (pre-lowercase).
       Fail → NormalizationError("OWNER_INVALID").
    8. Validate `repo` against RX-REPO (pre-lowercase).
       Fail → NormalizationError("REPO_INVALID").
    9. Reject reserved repo names (".", "..", "^_+$").
   10. Produce:
         provider     = "GitHub"
         ownerLower   = lower(owner)
         repoLower    = lower(repo)
         ownerOriginal = owner   ← preserved for AuditTrail.DetailsJson.originalRepoUrl
         repoOriginal  = repo
   11. Return NormalizedRepo(provider, ownerLower, repoLower, ownerOriginal, repoOriginal).
```

Normalization is **pure** (no DB access, no I/O) and MUST be deterministic. Every `NormalizationError` maps to `400 PROVIDER_UNSUPPORTED` (one error code; the specific reason is logged in `AuditTrail.DetailsJson.normalizationReason`, never returned to the client).

### 4.3 Resolution after Normalization

After normalization, the resolver runs four parameterized SELECTs in tier order (§2.4) and stops at the first hit:

```sql
-- Tier 1: RepoUrl + Exact
SELECT RepositoryId, RepositoryStatusId, UpdatedAt
FROM Repository
WHERE LOWER(OwnerName) = :ownerLower
  AND LOWER(RepoName)  = :repoLower
  AND AcceptanceModeId = :RepoUrl
  AND VersionModeId    = :Exact
ORDER BY UpdatedAt DESC
LIMIT 1;

-- Tier 2: RepoUrl + Wildcard
SELECT RepositoryId, RepositoryStatusId, UpdatedAt
FROM Repository
WHERE LOWER(OwnerName) = :ownerLower
  AND :repoLower REGEXP CONCAT('^', LOWER(RepoName), '(-v[1-9][0-9]{0,3})?$')
  AND AcceptanceModeId = :RepoUrl
  AND VersionModeId    = :Wildcard
ORDER BY UpdatedAt DESC
LIMIT 1;

-- Tier 3 / 4: OwnerWildcard (Exact / Wildcard treated identically — VersionMode is ignored)
SELECT RepositoryId, RepositoryStatusId, UpdatedAt
FROM Repository
WHERE LOWER(OwnerName) = :ownerLower
  AND AcceptanceModeId = :OwnerWildcard
ORDER BY UpdatedAt DESC
LIMIT 1;
```

Implementations that cannot rely on `REGEXP` (e.g., very old MariaDB) MUST fetch all candidate rows for `(ownerLower, RepoUrl, Wildcard)` and apply `RX-VERSION-WILDCARD` in PHP. The result MUST be identical.



---

## 5. Rate Limit (per repository)

| Property | Value |
|----------|-------|
| Window | 60 seconds, sliding |
| Cap | 60 requests |
| Bucket key | `gitlogs:rl:repo:<RepositoryId>` |
| Substrate | If `wp_using_ext_object_cache()` → atomic `INCR` with TTL; else dedicated `RateLimit` table with row-level lock (per `12-logging-strategy.md` §16). |
| Response on overage | `429 RATE_LIMITED` with `Retry-After` seconds until window reset. |

The bucket is keyed by **`RepositoryId` after resolution**, not by `OwnerName/RepoName`, so an `OwnerWildcard` org-wide approval shares one bucket across all its repos. This is intentional: it caps the blast radius of a leaked org-level `LogSenderToken`.

---

## 6. Replay & Nonce Protection

- Every envelope MUST carry a `nonce` of ≥ 16 chars (recommend UUIDv4).
- The server stores `(RepositoryId, nonce, exp)` in a short-lived store (object cache or `EnvelopeNonce` table) for the **larger** of (envelope `exp` window) and 10 minutes.
- A second push with the same `(RepositoryId, nonce)` within that window → `401 ENVELOPE_REPLAYED`, severity `Error`, emits `SuspectedReplayAttack` security event.

---

## 7. Admin Approval Flow (how a repo gets onto the allowlist)

1. WP admin opens `/wp-admin/admin.php?page=git-logs-repositories`.
2. Clicks **Add Repository**, fills:
   - `OwnerName` (GitHub login, case preserved)
   - `RepoName` (or leave blank if `AcceptanceMode = OwnerWildcard`)
   - `OwnerType` (`User` | `Organization`)
   - `AcceptanceMode` (`RepoUrl` | `OwnerWildcard`)
   - `VersionMode` (`Exact` | `Wildcard`)
   - Optional `EndpointUrl`, `Description`
3. Server validates uniqueness against `IdxRepository_OwnerRepo`.
4. Server generates a fresh 32-byte `LogSenderToken`, computes:
   - `LogSenderTokenHash = Argon2id(token)` (long-term audit anchor)
   - `LogSenderTokenVerifier = AEAD-Encrypt(token, key = derive(AUTH_KEY, RepositoryId))` (used for HS256 verification per §3 step 6)
5. Inserts `Repository` row with `RepositoryStatusId = Active`, `IsActive = 1`.
6. Writes `AuditTrail (RepoCreate, Success)`.
7. Returns the raw `LogSenderToken` to the admin **once**, with explicit "shown only now" UX warning.
8. Admin pastes the token into the CI runner's secret store (e.g., GitHub Actions secret `GITLOGS_SENDER_TOKEN`).

> Disabling a repo: admin sets `RepositoryStatusId = Disabled`. Subsequent pushes are rejected (`ALLOWLIST_REJECTED_DISABLED`) but historical logs remain queryable.

> Rotating a `LogSenderToken`: admin clicks **Rotate Token**; both the new and old verifier are accepted for a configurable grace window (default 24 h) to allow CI to roll over.

---

## 8. Audit Events Emitted

| Event | When | `AuditOutcome` | Severity |
|-------|------|----------------|----------|
| `AllowlistMatched_Exact` | §3 step 5, tier 1 hit | continues | `Info` |
| `AllowlistMatched_VersionWildcard` | tier 2 hit | continues | `Info` |
| `AllowlistMatched_OwnerWildcard` | tier 3 or 4 hit | continues | `Info` |
| `AllowlistRejected_NotRegistered` | no row matched | `Rejected` | `Warn` |
| `AllowlistRejected_Disabled` | row matched but Disabled | `Rejected` | `Warn` |
| `EnvelopeJwtVerified` | step 6 success | continues | `Info` |
| `EnvelopeJwtRejected_BadHmac` | bad signature | `Rejected` | `Warn` |
| `EnvelopeJwtRejected_Expired` | expired | `Rejected` | `Info` |
| `EnvelopeJwtRejected_Replayed` | nonce reuse | `Rejected` | `Error` + `SuspectedReplayAttack` |
| `PayloadCapExceeded` | step 2 | `Rejected` | `Warn` |
| `RateLimitExceeded` | step 7 | `Rejected` | `Warn` |
| `LogEntriesPersisted` | step 9 success | `Success` | `Info` |
| `IngestionFailed_DbError` | step 9 DB error | `Error` | `Error` |

Each request produces exactly one **terminal** `AuditTrail` row at step 10 in addition to the informational events above (per `12-logging-strategy.md` §4.3 rule).

---

## 9. Acceptance Criteria

| # | Criterion |
|---|-----------|
| AC-ALW-01 | A push for an `(owner, repo)` with no matching `Repository` row returns `403 ALLOWLIST_REJECTED_NOT_REGISTERED` and writes one `LogPush`-`Rejected` audit row. |
| AC-ALW-02 | A push for a matching but `Disabled` repo returns `403 ALLOWLIST_REJECTED_DISABLED` and is auditable. |
| AC-ALW-03 | A push for `acme/widget-v7` is accepted iff a `Repository` row with `OwnerName=acme, RepoName=widget, VersionMode=Wildcard, AcceptanceMode=RepoUrl` exists and is Active. |
| AC-ALW-04 | A push for `acme/anything` is accepted iff a `Repository` row with `OwnerName=acme, AcceptanceMode=OwnerWildcard` exists and is Active. |
| AC-ALW-05 | When an `Exact RepoUrl` row and an `OwnerWildcard` row both could match, the `Exact RepoUrl` row is chosen (precedence §2.4). |
| AC-ALW-06 | An envelope JWT signed with the wrong `LogSenderToken` returns `401 ENVELOPE_BAD_SIGNATURE`. |
| AC-ALW-07 | An envelope JWT replay (same nonce within 10 min) returns `401 ENVELOPE_REPLAYED`, revokes nothing, but emits a `SuspectedReplayAttack` event. |
| AC-ALW-08 | The 61st push within 60 s for the same `RepositoryId` returns `429 RATE_LIMITED` with a `Retry-After` header. |
| AC-ALW-09 | A request body > 1 MB returns `413 PAYLOAD_TOO_LARGE` **before** any DB write. |
| AC-ALW-10 | All normalization variants in §4 row 1–5 resolve to the same `RepositoryId`. |
| AC-ALW-11 | Provider != `GitHub` returns `400 PROVIDER_UNSUPPORTED`. |
| AC-ALW-12 | Successful push returns `202 Accepted` with `{ traceId, persistedCount, rejectedCount }` and writes exactly one `LogPush`-`Success` audit row regardless of how many `LogEntry` rows were inserted. |

---

## 10. Test Vectors

Implementers MUST add these as automated tests. Vectors are grouped by stage; each vector lists `Input`, `Repository row(s) present`, and the **exact** expected outcome (`AcceptOrRejectCode`, `MatchedRepositoryId`, `MatchedTier`).

For brevity, a `Repository` row is written as `R{id}: owner/repo, AcceptanceMode, VersionMode, Status` (UpdatedAt strictly increases by id unless noted).

### 10.1 URL Normalization (pure, no DB)

| # | Input `repoUrl` | Expected normalized `(provider, ownerLower, repoLower)` | Result |
|---|---|---|---|
| N-01 | `https://github.com/Acme/Widget` | `(GitHub, acme, widget)` | OK |
| N-02 | `https://github.com/Acme/Widget.git` | `(GitHub, acme, widget)` | OK |
| N-03 | `https://github.com/Acme/Widget/` | `(GitHub, acme, widget)` | OK |
| N-04 | `https://www.github.com/Acme/Widget` | `(GitHub, acme, widget)` | OK |
| N-05 | `git@github.com:Acme/Widget.git` | `(GitHub, acme, widget)` | OK |
| N-06 | `ssh://git@github.com/Acme/Widget` | `(GitHub, acme, widget)` | OK |
| N-07 | `https://github.com/Acme/Widget/tree/main` | — | `400 PROVIDER_UNSUPPORTED` (`MALFORMED_URL`) |
| N-08 | `https://gitlab.com/Acme/Widget` | — | `400 PROVIDER_UNSUPPORTED` (`PROVIDER_UNSUPPORTED`) |
| N-09 | `http://github.com/acme/widget` | `(GitHub, acme, widget)` | OK (HTTP accepted by `RX-HTTPS-URL`; TLS is enforced by hosting, not by the resolver) |
| N-10 | `https://github.com/-acme/widget` | — | `400 PROVIDER_UNSUPPORTED` (`OWNER_INVALID` — leading `-`) |
| N-11 | `https://github.com/acme--bad/widget` | — | `400 PROVIDER_UNSUPPORTED` (`OWNER_INVALID` — `--` consecutive) |
| N-12 | `https://github.com/acme/.` | — | `400 PROVIDER_UNSUPPORTED` (`REPO_INVALID` — reserved name) |
| N-13 | `https://github.com/acme/..` | — | `400 PROVIDER_UNSUPPORTED` (`REPO_INVALID` — reserved name) |
| N-14 | (string of 2049 chars) | — | `400 PROVIDER_UNSUPPORTED` (`URL_TOO_LONG`) |
| N-15 | `https://github.com/Acme/Widget?ref=foo` | — | `400 PROVIDER_UNSUPPORTED` (`MALFORMED_URL`) |
| N-16 | `https://github.com/Acme/Widget#frag` | — | `400 PROVIDER_UNSUPPORTED` (`MALFORMED_URL`) |
| N-17 | `https://github.com/Acme` | — | `400 PROVIDER_UNSUPPORTED` (`MALFORMED_URL` — missing `<repo>`) |

### 10.2 Wildcard Suffix Regex (`RX-VERSION-WILDCARD` against base `widget`)

Pattern: `^widget(-v[1-9][0-9]{0,3})?$`

| # | Candidate `repo` | Expected match? |
|---|---|---|
| W-01 | `widget` | yes |
| W-02 | `widget-v1` | yes |
| W-03 | `widget-v9999` | yes |
| W-04 | `widget-v0` | no (leading-zero / zero) |
| W-05 | `widget-v01` | no (leading zero) |
| W-06 | `widget-V2` | no (uppercase `V`) |
| W-07 | `widget-v` | no (no number) |
| W-08 | `widget-v10000` | no (5+ digits) |
| W-09 | `widget-v2-rc1` | no (extra suffix) |
| W-10 | `widgets-v2` | no (base differs) |
| W-11 | `Widget-v2` | yes (case-insensitive owner/repo compared after lowercase; `widget` matches `Widget`) |
| W-12 | `widgetV2` | no (missing `-`) |

### 10.3 Resolution Precedence

Setup A:
- `R10: acme/widget, RepoUrl, Exact, Active` (UpdatedAt: 2026-04-01)
- `R11: acme/widget, RepoUrl, Wildcard, Active` (UpdatedAt: 2026-04-02)
- `R12: acme/*,    OwnerWildcard, Exact, Active` (UpdatedAt: 2026-04-03)

| # | Inbound `(owner, repo)` | Expected `MatchedRepositoryId` | Tier |
|---|---|---|---|
| P-01 | `acme/widget` | `R10` | 1 (RepoUrl + Exact) |
| P-02 | `acme/widget-v3` | `R11` | 2 (RepoUrl + Wildcard) |
| P-03 | `acme/anything-else` | `R12` | 3 (OwnerWildcard) |
| P-04 | `other/widget` | — (none match) | `403 ALLOWLIST_REJECTED_NOT_REGISTERED` |

Setup B (tie-break within tier — most-recent `UpdatedAt` wins):
- `R20: acme/widget, RepoUrl, Exact, Active` (UpdatedAt: 2026-01-01)
- `R21: acme/widget, RepoUrl, Exact, Active` (UpdatedAt: 2026-04-15)

| # | Inbound | Expected `MatchedRepositoryId` |
|---|---|---|
| P-05 | `acme/widget` | `R21` (newer) |

> Setup B should be considered a **data-quality smell** (duplicate exact rows); admin UI MUST prevent it at write time via `IdxRepository_OwnerRepo` (per `02-database-schema-and-erd.md`). The precedence rule exists only to be deterministic if the constraint is ever bypassed by a migration.

Setup C (`Disabled` priority):
- `R30: acme/widget, RepoUrl, Exact, Disabled`
- `R31: acme/*,     OwnerWildcard, Exact, Active`

| # | Inbound | Expected outcome |
|---|---|---|
| P-06 | `acme/widget` | `403 ALLOWLIST_REJECTED_DISABLED` (more-specific tier wins **before** status check; the status check then rejects) |
| P-07 | `acme/sibling` | Accept via `R31` (tier 3) |

> Implementers MUST select tier first, then status-check the chosen row. Falling back from a Disabled exact match to an Active wildcard is **forbidden** (this is a deliberate denial behaviour: a temporarily disabled repo MUST NOT silently route through an org-wide allowance).

### 10.4 Envelope JWT

Setup: `R40: acme/widget, RepoUrl, Exact, Active`, `LogSenderTokenVerifier` known to test.

| # | Envelope | Expected outcome |
|---|---|---|
| E-01 | Valid signature, `iat = now`, `exp = now+60`, fresh `nonce` | `202 Accepted` |
| E-02 | Signed with wrong secret | `401 ENVELOPE_BAD_SIGNATURE` |
| E-03 | `exp = now − 120` | `401 ENVELOPE_EXPIRED` |
| E-04 | `exp = now + 600` (`exp − iat = 600`) | `401 ENVELOPE_TTL_TOO_LONG` |
| E-05 | Same `(RepositoryId, nonce)` as a successful push within last 10 min | `401 ENVELOPE_REPLAYED` + `SuspectedReplayAttack` event |
| E-06 | Missing `nonce` claim | `400 ENVELOPE_MALFORMED` |
| E-07 | `nonce` length 8 | `400 ENVELOPE_MALFORMED` (min 16) |
| E-08 | `iat` 70 s in the future (clock skew) | `401 ENVELOPE_EXPIRED` (skew window is ±60 s) |

### 10.5 Rate Limit (per resolved `RepositoryId`)

Setup: 60-req/60s sliding window, `R50` resolved.

| # | Sequence | Expected outcome on each |
|---|---|---|
| RL-01 | Requests 1–60 within 30 s | All `202` |
| RL-02 | Request 61 within same window | `429 RATE_LIMITED`, `Retry-After` between 1 and 60 |
| RL-03 | Wait 60 s after RL-01, then push | `202` (window slid) |
| RL-04 | `OwnerWildcard` row resolves all of `acme/*` to `R12`; 60 pushes from 60 different repos in the org | First 60 `202`, 61st `429` (one bucket per resolved id) |

### 10.6 Body Cap

| # | Body size after decompression | Outcome |
|---|---|---|
| B-01 | 1,048,575 B | OK |
| B-02 | 1,048,576 B | OK (== 1 MB exact) |
| B-03 | 1,048,577 B | `413 PAYLOAD_TOO_LARGE` |
| B-04 | gzip request, 200 KB compressed → 1.5 MB decompressed | `413 PAYLOAD_TOO_LARGE` (cap is post-decompression per `07-log-push-flow.md`) |

### 10.7 End-to-End Audit Linkage

| # | Scenario | Required side-effect |
|---|---|---|
| L-01 | Any successful push | Exactly one `AuditTrail (LogPush, Success)` row, `DetailsJson.matchedRepositoryId = R{id}`, `DetailsJson.matchedTier ∈ {1,2,3,4}`. |
| L-02 | Any rejected push | Exactly one `AuditTrail (LogPush, Rejected)` row with `DetailsJson.rejectReason ∈ {NotRegistered, Disabled, BadSignature, Expired, TtlTooLong, Replayed, RateLimited, PayloadTooLarge, ProviderUnsupported}`. |
| L-03 | DB error during persistence | One `AuditTrail (LogPush, Error)` row; the controller re-throws (no swallow). |

---

## 11. Open Items

| # | Item | Notes |
|---|------|-------|
| OI-ALLOW-01 | HS256 verifier storage | Section 3 step 6 introduces `Repository.LogSenderTokenVerifier` (AEAD-encrypted). Alternative: switch envelope to **Ed25519 / RS256** so only a public key is stored — eliminates symmetric secret at rest. Decide before implementation; affects schema. Tracked as finding [F-02](../../25-app-issues/02-consolidated-audit-findings/00-overview.md). |
| OI-ALLOW-02 | Token rotation grace window | Default 24 h; should it be admin-configurable per-repo? |
| OI-ALLOW-03 | `OwnerWildcard` + per-repo rate limit | Currently buckets by resolved `RepositoryId`; should an `OwnerWildcard` row instead bucket by `(RepositoryId, owner, repo-from-payload)` to avoid one noisy repo starving siblings? |
| OI-ALLOW-04 | Whether to expose a `/repos/check` dry-run endpoint for CI to validate config | UX nicety; needs rate limit of its own. |
| OI-ALLOW-05 | Schema amendment | If OI-ALLOW-01 chooses AEAD verifier, add column `LogSenderTokenVerifier VARBINARY(255) NULL` to `Repository` and bump schema to v3.0.0. |
| OI-ALLOW-06 | Disabled-priority denial (P-06) | Confirm UX: should the admin UI surface that a Disabled exact-row is **shadowing** a wildcard row, so the admin understands why pushes for that one repo are 403 while sibling repos succeed? |

---

*Endpoint-level approval for unauthenticated, controlled CI/CD log ingestion. No error swallowed; every decision audited. Regex, normalization, and test vectors are exhaustive — implementations that diverge are non-conformant.*
