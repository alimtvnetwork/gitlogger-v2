> ⚠️ **DEPRECATED — Legacy v1 Spec (folder 21)**  
> This document is preserved for historical reference only. **Do not implement against it.**  
> The active specification is **v2** in [`spec/22-git-logs-v2/`](../../22-git-logs-v2/00-overview.md) (SQLite, no JWT, SSH-key auth).  
> See [`spec/22-git-logs-v2/00-overview.md`](../../22-git-logs-v2/00-overview.md) for the current canonical source.  
> Deprecated: 2026-04-25

---

# Auth — JWT Flow

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Status:** Active  
**AI Confidence:** Production-Ready  
**Ambiguity:** Low

---

## Overview

Defines the **complete JWT subsystem** for the `git-logs` plugin: keypair generation, key storage, `kid` derivation, JWKS endpoint and caching, access-token claim set and validation order, refresh-token rotation chain, reuse-detection (replay) protection, and the revocation denylist.

This file is the **single source of truth** for everything cryptographic and claim-level around plugin-issued JWTs. The operational flow (who-talks-to-whom) lives in [`16-jwt-onboarding-and-token-usage.md`](./16-jwt-onboarding-and-token-usage.md). The error envelope and `GL-AUTH-*` codes live in [`11-error-management.md`](./11-error-management.md). The refresh/access-token DB tables live in [`02-database-schema-and-erd.md`](./02-database-schema-and-erd.md).

Locked decisions from `00-overview.md` referenced here:
- **D1** RS256, plugin keypair, JWKS at `/wp-json/git-logs/v1/.well-known/jwks.json`.
- **D2** Access token TTL = 24 h.
- **D3** Refresh token TTL = 7 d, rotating, revocable.

---

## Keywords

`jwt` · `rs256` · `jwks` · `kid` · `key-rotation` · `refresh-token-rotation` · `replay-protection` · `denylist` · `claims-validation` · `git-logs`

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
| Onboarding flow & sequence diagrams | [./16-jwt-onboarding-and-token-usage.md](./16-jwt-onboarding-and-token-usage.md) |
| Error envelope & `GL-AUTH-*` codes | [./11-error-management.md](./11-error-management.md) |
| `User` / `RefreshToken` schema | [./02-database-schema-and-erd.md](./02-database-schema-and-erd.md) |
| WordPress bridge (alternative auth) | ./06-auth-wordpress-bridge.md (`06-auth-wordpress-bridge` — removed in v1 deprecation) |
| Allowlist (envelope JWT, separate subsystem) | [./08-allowlist-and-wildcard-matching.md](./08-allowlist-and-wildcard-matching.md) |
| Audit trail | ./10-audit-trail.md (`10-audit-trail` — removed in v1 deprecation) |
| Locked decisions | [./00-overview.md](./00-overview.md) §Locked Decisions |

---

## 1. Subsystem Boundaries

| In scope | Out of scope |
|----------|--------------|
| Plugin-issued **access JWT** (RS256) | Envelope JWT for `POST /logs/push` (HS256 — see `08-…`) |
| Plugin-issued **refresh token** (opaque, rotating) | WP cookie / Application Password (see `06-…`) |
| Keypair lifecycle (generate, rotate, retire) | WP user passwords or WP nonces |
| JWKS publication & cache headers | Third-party SSO, OAuth |
| `jti` revocation denylist | Audit-trail row content (see `10-…`) |

> The **plugin token** (long-lived secret stored in `User.TokenHash`) is **not** a JWT. It is exchanged once per session for an access JWT + refresh token via `POST /auth/token`. Its hashing and verification are covered in `02-database-schema-and-erd.md` §3.1 and `16-…` §2.

---

## 2. Cryptographic Parameters

| Parameter | Value |
|-----------|-------|
| Signing algorithm | **RS256** (RSASSA-PKCS1-v1_5 with SHA-256) |
| Key type | RSA |
| Key size | **2048 bits** (minimum); 4096 bits accepted but not required |
| Public exponent | 65537 (`0x010001`) |
| Hash for `kid` | SHA-256 (truncated to 16 bytes, base64url-encoded) |
| Encoding | Keys stored PEM (PKCS#8 for private, SPKI for public) |
| Private key at rest | WordPress option `gitlogs_jwt_keys` (autoload = no), value AEAD-encrypted with a key derived from `AUTH_KEY` + `SECURE_AUTH_SALT` (HKDF-SHA256, 32 B) |
| JWT library | `firebase/php-jwt` ≥ 6.10 (or equivalent OpenSSL-based implementation) |

**Why RS256 (not HS256) for access tokens:** the plugin publishes a JWKS so external mediums (CI, scripts) can verify tokens themselves without holding any plugin secret. HS256 would force every verifier to share a symmetric secret with the plugin.

> The envelope JWT used by `POST /logs/push` deliberately uses **HS256** because the verifier is the plugin itself and the secret is the per-repo `LogSenderToken` — different threat model, covered in `08-…`.

---

## 3. Key Lifecycle

### 3.1 States

| State | Meaning |
|-------|---------|
| **Active** | The current signing key. Exactly **one** key is Active at any time. New tokens use this key. |
| **Retiring** | The previous Active key. Still in JWKS so existing tokens verify, but no new tokens are signed with it. |
| **Retired** | Removed from JWKS. Tokens signed by this key now fail with `GL-AUTH-002`. |

### 3.2 Storage shape (`gitlogs_jwt_keys` option)

```json
{
  "version": 1,
  "active":   { "kid": "k_2026_04_25_a", "createdAt": "2026-04-25T03:00:00Z", "publicKeyPem": "…", "privateKeyEnc": "…" },
  "retiring": { "kid": "k_2025_10_30_a", "createdAt": "2025-10-30T03:00:00Z", "publicKeyPem": "…", "privateKeyEnc": "…", "retiringSince": "2026-04-25T03:00:00Z" },
  "rotation": { "scheduledAt": "2026-10-25T03:00:00Z", "previousRotationAt": "2026-04-25T03:00:00Z" }
}
```

`privateKeyEnc` is the PEM private key after AEAD (XChaCha20-Poly1305 if `sodium` is available, otherwise AES-256-GCM via OpenSSL). The AEAD key is derived per request from WP salts; it is never persisted.

### 3.3 Generation

Triggered by:
- **First-run installer** (always — plugin will not boot without a key).
- **Admin action** “Rotate JWT keys” in WP admin.
- **Cron** `gitlogs_cron_rotate_jwt` (default: every 180 days; configurable via filter `gitlogs_jwt_rotation_interval_days`).

Algorithm:

```
1. Generate RSA-2048 keypair via openssl_pkey_new with type=OPENSSL_KEYTYPE_RSA, private_key_bits=2048.
2. Export private (PKCS#8 PEM) and public (SPKI PEM).
3. kid = base64url( first 16 bytes of SHA256(SPKI-DER of public key) )
        prefixed with "k_" + UTC date "Y_m_d" + "_a"   (e.g. "k_2026_04_25_a")
        (the date prefix is human-readable; uniqueness comes from the hash suffix)
   Full kid format: "k_<YYYY>_<MM>_<DD>_<base64url16>"
4. AEAD-encrypt private PEM with the WP-salt-derived key.
5. Atomic option update inside DB transaction:
     a. Move current Active → Retiring (overwrites previous Retiring; see §3.4).
     b. Set new key as Active.
     c. Set rotation.previousRotationAt = now, scheduledAt = now + intervalDays.
6. Bust the JWKS edge cache (see §6.4): bump option gitlogs_jwks_etag (HMAC of new JWKS).
7. Audit row: AuditTrail (action="JwtKeyRotate", outcome="Success", details={ newKid, previousKid }).
```

### 3.4 Retirement window

When a rotation happens, the previously Active key becomes Retiring. The Retiring key is published in JWKS for **exactly one access-token TTL window** (= 24 h, locked decision D2) plus a 1-hour clock-skew margin = **25 h total**.

A scheduled cron `gitlogs_cron_retire_jwt` runs every hour:

```
For the Retiring key K:
    if (now - K.retiringSince) >= 25 hours:
        Remove K from option (set retiring = null).
        Audit row: JwtKeyRetire / Success / { retiredKid }.
        Bust JWKS edge cache.
```

After retirement, any access token signed by K (still floating in the wild) verifies-fails with `GL-AUTH-002`. The holder simply re-exchanges its plugin token for a fresh JWT.

### 3.5 Emergency revocation

Admin action "Revoke JWT key" (UI button, RBAC-gated):

```
1. Move target key (Active or Retiring) → null immediately.
2. If the revoked key was Active and no Retiring key exists, generate a new Active key in the same transaction (so signing continues to work).
3. Bust JWKS edge cache.
4. Audit row: JwtKeyRevoke / Success / { revokedKid, reason }.
5. Optional: bulk-revoke all RefreshToken rows whose CreatedAt is within the suspected compromise window (admin checkbox).
```

---

## 4. JWT Header

| Field | Value | Notes |
|-------|-------|-------|
| `alg` | `"RS256"` | Hardcoded. The verifier MUST reject any other value (see §7.1, claim-validation step 1). |
| `typ` | `"JWT"` | Standard. |
| `kid` | `"k_YYYY_MM_DD_<b64u16>"` | Required; identifies the JWKS entry to use. |

Tokens with missing `kid`, missing `alg`, or `alg != "RS256"` are rejected before signature verification. The `none` algorithm is **never** accepted. The `kid` MUST be matched against the JWKS by **exact string equality** — never by substring or prefix.

---

## 5. Access-Token Claim Set

All claims are mandatory unless marked Optional. Times are seconds since Unix epoch (NumericDate).

| Claim | Type | Value | Notes |
|-------|------|-------|-------|
| `iss` | string | `home_url('/wp-json/git-logs/v1')` (no trailing slash) | Verified by exact string match. |
| `sub` | string | `"user:<UserId>"` (`UserId` is integer from `User.UserId`) | Used for RBAC lookup. |
| `aud` | string | `"git-logs"` | Verified by exact string match. |
| `iat` | number | Now (server time, UTC) | |
| `nbf` | number | Now − 5 (5 s skew) | |
| `exp` | number | `iat + 86400` | 24 h, per locked decision D2. **Verifier MUST reject any token where `exp - iat > 86400`** to defeat issuer downgrade. |
| `jti` | string | UUIDv4, hex | Identifies the token; used by the revocation denylist (§9). |
| `gl_v` | number | `1` | Claim-set version. Increment on breaking change. |
| `gl_roles` | array<string> | e.g. `["LogReader","RepoAdmin"]` | Snapshot at issue time. RBAC lookup also re-checks live DB roles before sensitive ops. |
| `gl_username` | string | `User.Username` | For audit/log readability only — never used for authorization. |
| `gl_kid_v` | number | `1` | Reserved; bumped if `kid` derivation changes. |

Claims **forbidden** in plugin-issued tokens (verifier rejects if present and non-empty):

| Claim | Reason |
|-------|--------|
| `azp` | OIDC-only; not used. |
| `nonce` | OIDC-only; not used. |
| `act` | Token-exchange not supported. |
| `cnf` | mTLS / proof-of-possession not supported in v1. |

> Snapshotted `gl_roles` MUST NOT be the sole authorization input for destructive operations (delete, revoke, role-change). Such operations re-check `UserRole` in the DB at execution time. This protects against admin role-revocations that happen mid-token-lifetime.

---

## 6. JWKS Endpoint

### 6.1 Route

`GET /wp-json/git-logs/v1/.well-known/jwks.json` — public, unauthenticated, no envelope wrapping (per `11-…` §5.1).

### 6.2 Response body shape

```json
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "alg": "RS256",
      "kid": "k_2026_04_25_a4Bz9Q1xPwR0vH7s",
      "n":   "<base64url modulus>",
      "e":   "AQAB"
    },
    {
      "kty": "RSA",
      "use": "sig",
      "alg": "RS256",
      "kid": "k_2025_10_30_aXyZ…",
      "n":   "<base64url modulus>",
      "e":   "AQAB"
    }
  ]
}
```

The Active key is always listed first. The Retiring key (if any) follows. Retired keys MUST NOT appear.

### 6.3 Response headers

| Header | Value |
|--------|-------|
| `Content-Type` | `application/jwk-set+json; charset=utf-8` |
| `Cache-Control` | `public, max-age=300, stale-while-revalidate=60, stale-if-error=600` |
| `ETag` | `"<gitlogs_jwks_etag>"` (the option set during rotation; HMAC-SHA256 of the JWKS body, base64url, prefixed `W/` is **not** used — strong validator) |
| `Vary` | `Accept-Encoding` |
| `X-Request-Id` | per `12-…` |
| `X-Robots-Tag` | `noindex` |

### 6.4 Cache invalidation

The 5-minute `max-age` is deliberate: it bounds the time a freshly-rotated key takes to propagate through any HTTP cache between the plugin and a verifier. During that window, verifiers using a stale JWKS will fall back to the Retiring key (which is still listed) — that is exactly why the Retirement window in §3.4 is **24 h + 1 h**, not just 1 h. Defence in depth.

Implementations behind a CDN or reverse proxy MUST configure the proxy to honour `ETag` revalidation. If it cannot, set the `gitlogs_jwks_max_age` filter to `0` to opt out of caching (at the cost of every verifier hitting WP on every JWT verification).

### 6.5 Conditional GET

If the request includes `If-None-Match: "<etag>"` and it matches the current `gitlogs_jwks_etag`, return `304 Not Modified` with no body and the same `Cache-Control` / `ETag` headers.

### 6.6 What a verifier MUST do

1. Cache the JWKS for at most `Cache-Control: max-age` seconds.
2. On JWT verify failure where the token's `kid` is not in the cached JWKS, force-refresh the JWKS **once** before deciding the token is invalid (handles a freshly-rotated key the verifier hasn't seen yet).
3. Never accept a JWKS that lacks `alg=RS256` for the matched `kid`.

---

## 7. Access-Token Verification (Order Matters)

The verifier MUST execute these checks **in this order**, returning at the first failure with the indicated error code (all routed through the envelope per `11-…`):

| # | Check | On failure |
|---|-------|------------|
| 1 | `Authorization` header present and starts with `Bearer ` (single space, case-sensitive scheme) | `GL-AUTH-007` |
| 2 | Token has exactly 3 dot-separated base64url segments | `GL-AUTH-002` |
| 3 | Decoded header contains `alg == "RS256"`, `typ == "JWT"`, and a non-empty string `kid` | `GL-AUTH-002` |
| 4 | `kid` exists in current JWKS (with one forced refresh per §6.6) | `GL-AUTH-002` |
| 5 | RS256 signature verifies against the matched JWK | `GL-AUTH-002` |
| 6 | `iss` exact-match | `GL-AUTH-002` |
| 7 | `aud` exact-match | `GL-AUTH-002` |
| 8 | `nbf <= now + 5` (5 s skew tolerance) | `GL-AUTH-002` |
| 9 | `exp >  now - 5` (5 s skew tolerance) | `GL-AUTH-002` |
| 10 | `exp - iat <= 86400` (anti-downgrade) | `GL-AUTH-002` |
| 11 | `gl_v == 1` | `GL-AUTH-002` |
| 12 | `sub` matches `^user:[1-9][0-9]*$` and references a row in `User` | `GL-AUTH-002` |
| 13 | `User.UserStatusId == Active` | `GL-AUTH-005` if `IsLocked`, else `GL-AUTH-002` |
| 14 | `jti` is **not** in the revocation denylist (§9) | `GL-AUTH-002` |

### 7.1 Algorithm-confusion defence

The JWT library MUST be configured with the **expected algorithm pinned to RS256 only**. Passing the JWKS to a library that auto-selects the algorithm based on the token header is **forbidden** — that is the classic "alg=none" / "alg=HS256-with-public-key-as-secret" bypass. Pseudocode:

```php
// CORRECT
$decoded = JWT::decode($jwt, JWK::parseKeySet($jwksArray), ['RS256']);

// WRONG — never allow the token to dictate the algorithm
$decoded = JWT::decode($jwt, $secret, /* no allowed-algs list */);
```

---

## 8. Refresh Tokens

### 8.1 Format

A refresh token is an **opaque** value (not a JWT): 32 random bytes, base64url-encoded, no padding (43 characters). Generated with `random_bytes(32)`. The plaintext is returned to the client **once** (in the `POST /auth/token` or `POST /auth/refresh` response). Only Argon2id hash is stored, in `RefreshToken.TokenHash`.

### 8.2 TTL

7 days from issuance (`ExpiresAt = CreatedAt + INTERVAL 7 DAY`), per locked decision D3.

### 8.3 Issuance

A new `RefreshToken` row is INSERTed in two situations:

- **Initial token exchange** (`POST /auth/token` with plugin token): `RotatedFromRefreshTokenId = NULL`.
- **Rotation** (`POST /auth/refresh` succeeds): the new row's `RotatedFromRefreshTokenId` is set to the predecessor's `RefreshTokenId`.

In both cases, the same DB transaction MUST also:
1. Insert the new row with `IsRevoked=0`, `IsRotated=0`.
2. (Rotation only) `UPDATE` predecessor: `IsRotated=1` (NOT `IsRevoked`; see §8.5 for why these are different bits).
3. Insert `AuditTrail (TokenIssue, Success, { userId, refreshTokenId, rotatedFromId })`.

### 8.4 Use (`POST /auth/refresh`)

```
INPUT: { refreshToken: <opaque string> }

1. Hash candidate via Argon2id and look up rows by hash prefix? — NO.
   Instead: SELECT all non-expired non-revoked rows for the candidate user is impossible
   (we have no userId yet). To make lookup O(1):
     a. The first 16 chars of the base64url token are stored ALSO in column TokenHashPrefix
        (NOT in the spec yet — see Open Item OI-JWT-01) OR
     b. Store and look up by SHA-256 of the token (length-bounded, fast index), then
        constant-time-compare Argon2id of the full token against TokenHash.
   v1 implementation: option (b). Add column RefreshToken.TokenLookupHash (CHAR(64),
   indexed UNIQUE) holding hex(SHA256(token)). Argon2id remains the slow verifier.
2. If no row found: 401 GL-AUTH-003 (treat unknown identically to revoked — no oracle).
3. Found row R:
     If R.IsRevoked = 1                           → §8.5 reuse-detection chain revoke,
                                                    then 401 GL-AUTH-003.
     If R.IsRotated = 1 AND R.IsRevoked = 0       → §8.5 reuse-detection chain revoke,
                                                    then 401 GL-AUTH-003.
     If R.ExpiresAt <= NOW()                       → 401 GL-AUTH-004.
     If R.User.UserStatusId != Active              → 401 GL-AUTH-005 / GL-AUTH-002.
4. Argon2id verify candidate vs R.TokenHash; on mismatch → 401 GL-AUTH-003 (with chain revoke).
5. Begin TX:
     a. UPDATE R SET IsRotated=1.
     b. INSERT new RefreshToken (RotatedFromRefreshTokenId = R.RefreshTokenId, …).
     c. Sign new access JWT (per §4–§5).
     d. INSERT AuditTrail (TokenRefresh, Success, …).
   COMMIT.
6. Return { accessToken, refreshToken: <new plaintext>, expiresIn: 86400 }.
```

> The schema column `RefreshToken.TokenLookupHash CHAR(64) NOT NULL UNIQUE` introduced in step 1b is required by this spec. If `02-database-schema-and-erd.md` does not yet include it, that is a tracked spec gap (see Open Items §11, OI-JWT-01).

### 8.5 Reuse Detection (Replay Protection)

The combination `IsRotated=1` plus a fresh use is the **canonical signal** that an old refresh token has been replayed — either the legitimate client has been compromised and an attacker is using a stolen token, or the legitimate client retried a request that succeeded server-side but failed in transit. We treat both the same: assume compromise, revoke the entire rotation chain.

**Chain-revoke algorithm:**

```
function revokeChain(refreshTokenId):
    visited = {}
    queue = [refreshTokenId]

    # Walk forward through descendants
    while queue not empty:
        id = queue.pop()
        if id in visited: continue
        visited.add(id)
        UPDATE RefreshToken SET IsRevoked=1, RevokedAt=NOW()
            WHERE RefreshTokenId=id AND IsRevoked=0
        children = SELECT RefreshTokenId FROM RefreshToken
                   WHERE RotatedFromRefreshTokenId = id
        for c in children: queue.append(c)

    # Walk backward through ancestors (in case the attacker revealed an old node)
    cur = refreshTokenId
    while cur is not NULL:
        parent = SELECT RotatedFromRefreshTokenId FROM RefreshToken
                 WHERE RefreshTokenId = cur
        if parent is NULL: break
        if parent in visited: break
        visited.add(parent)
        UPDATE RefreshToken SET IsRevoked=1, RevokedAt=NOW()
            WHERE RefreshTokenId=parent AND IsRevoked=0
        cur = parent

    INSERT AuditTrail (TokenChainRevoke, Success,
        { triggerRefreshTokenId: refreshTokenId, revokedIds: visited, reason: "ReuseDetected" })

    # Optional but recommended: also denylist any access JWTs (jti) issued from any
    # node in the chain whose exp is still in the future. Requires storing
    # RefreshToken.IssuedAccessJti — not in v1 schema; see OI-JWT-02.
```

This algorithm runs in **the same DB transaction** as the rejecting `/auth/refresh` response (so the chain is closed before the 401 is returned).

### 8.6 Logout

`POST /auth/logout` (authenticated):

```
1. From the access JWT, extract jti and sub.
2. Append jti to the denylist (§9) with TTL = original exp.
3. UPDATE RefreshToken SET IsRevoked=1, RevokedAt=NOW()
     WHERE UserId=<sub-userId> AND IsRevoked=0 AND IsRotated=0 AND ExpiresAt>NOW()
   (Revokes the user's currently-live, un-rotated refresh tokens. Past chain
    members already have IsRotated=1 and are unusable.)
4. INSERT AuditTrail (TokenRevoke, Success, { userId, jti }).
5. Return 204.
```

### 8.7 Bulk revocation

Triggered by: admin action ("Revoke all user sessions"), password / plugin-token reset, or §3.5 emergency key revocation:

```
UPDATE RefreshToken SET IsRevoked=1, RevokedAt=NOW()
WHERE UserId=? AND IsRevoked=0;
INSERT AuditTrail (TokenBulkRevoke, Success, { userId, count, reason });
```

Access tokens are NOT individually denylisted in this case (could be thousands). Instead, the denylist accepts a **per-user revocation watermark**: `gitlogs_user_jwt_min_iat[<UserId>] = now`. Verification step 9 (§7) is augmented: a JWT is also rejected if `iat < watermark[sub]`.

---

## 9. Revocation Denylist

### 9.1 Storage

Two complementary stores, both checked in verification step 14 (§7):

| Store | Key | Purpose | Backend |
|-------|-----|---------|---------|
| `gitlogs_jwt_denylist` | `jti` | Per-token revocation (logout, targeted revoke) | WP transient (Redis-backed if `wp_using_ext_object_cache()` is true; otherwise DB transient table `wp_options`) |
| `gitlogs_user_jwt_min_iat` | `UserId` | Bulk revocation watermark (§8.7) | Same backend, longer TTL |

### 9.2 Entry shape

```php
// gitlogs_jwt_denylist:<jti>
[
  'sub'       => 'user:42',
  'revokedAt' => 1714003200,   // unix seconds
  'expiresAt' => 1714089600,   // = original JWT exp; entry can be evicted after this
  'reason'    => 'Logout' | 'Admin' | 'ChainRevoke',
]
```

TTL on the transient = `expiresAt - now`. After the JWT's natural expiry, the entry is no longer needed (the token would fail step 9 of §7 anyway).

### 9.3 Lookup latency

The denylist check is the slowest step in the verification chain. To keep p99 under 5 ms:

- **Required**: an external object cache (Redis or Memcached). The plugin MUST `wp_admin_notice` if `wp_using_ext_object_cache()` returns false on bootstrap.
- **Permitted**: in-process LRU cache of recent denylist hits with TTL ≤ 30 s.
- **Forbidden**: SELECTing from `wp_options` on every request without a cache.

### 9.4 Denylist size bounds

A single denylist entry is < 200 B. With 24 h max TTL and a generous 1000 logouts/min plugin-wide, peak size ≈ 24 × 60 × 1000 × 200 B ≈ **288 MB**. This is the worst case. If projected load exceeds this, switch to a Bloom-filter front (false positives accepted — they cause a single JWT re-exchange).

---

## 10. Acceptance Criteria

| # | Criterion |
|---|-----------|
| AC-JWT-01 | Plugin bootstraps with no JWT key present → installer generates an Active RSA-2048 keypair and writes it to `gitlogs_jwt_keys` before any route is registered. |
| AC-JWT-02 | A token whose header has `alg=none`, `alg=HS256`, or missing `alg` is rejected with `GL-AUTH-002` **before** signature verification is attempted. |
| AC-JWT-03 | A token whose `kid` is not in the cached JWKS triggers exactly **one** JWKS refresh; if still not found, the response is `GL-AUTH-002`. |
| AC-JWT-04 | A token where `exp - iat > 86400` is rejected with `GL-AUTH-002` even if the signature is valid. |
| AC-JWT-05 | After key rotation, tokens signed by the previous (Retiring) key continue to verify for ≥ 24 h and < 25 h. |
| AC-JWT-06 | After key retirement, tokens signed by the retired key are rejected with `GL-AUTH-002`. |
| AC-JWT-07 | `GET /.well-known/jwks.json` returns `Cache-Control: public, max-age=300, stale-while-revalidate=60, stale-if-error=600` and a strong `ETag`. |
| AC-JWT-08 | `GET /.well-known/jwks.json` with a matching `If-None-Match` returns `304` and no body. |
| AC-JWT-09 | A refresh token used a second time (after rotation) triggers chain-revocation: the predecessor, all descendants, and any ancestor still un-revoked are flipped to `IsRevoked=1` in a single transaction; `AuditTrail.TokenChainRevoke` row is written; response is `GL-AUTH-003`. |
| AC-JWT-10 | A refresh-token row whose `ExpiresAt < NOW()` returns `GL-AUTH-004`, never `GL-AUTH-003` (so legitimate clients can distinguish "expired, log in again" from "revoked, contact admin"). |
| AC-JWT-11 | `POST /auth/logout` adds the JWT's `jti` to the denylist with TTL = remaining lifetime, and revokes all of the user's un-rotated live refresh tokens. |
| AC-JWT-12 | A bulk-revocation sets `gitlogs_user_jwt_min_iat[UserId] = now`; subsequent JWTs with `iat < watermark` are rejected with `GL-AUTH-002` even if their `jti` is not individually denylisted. |
| AC-JWT-13 | The plugin emits a WP admin notice on every page load if `wp_using_ext_object_cache()` is false (denylist performance warning). |
| AC-JWT-14 | The private key blob in `gitlogs_jwt_keys` is never returned by any REST endpoint (verified by a reflection test: `JSON.stringify` of every response fixture must not contain the bytes `BEGIN PRIVATE KEY` or the base64 of the encrypted private blob). |
| AC-JWT-15 | The token-exchange endpoint, the refresh endpoint, the logout endpoint, and the JWKS endpoint MUST each be covered by an `AuditTrail` row on every invocation (Success / Rejected / Error). |

---

## 11. Open Items

| # | Item | Notes |
|---|------|-------|
| OI-JWT-01 | Schema gap: `RefreshToken.TokenLookupHash CHAR(64) NOT NULL UNIQUE` is required by §8.4 step 1b but not yet in `02-database-schema-and-erd.md`. Bump schema to v2.x and add a migration. |
| OI-JWT-02 | Schema gap: `RefreshToken.IssuedAccessJti CHAR(36) NULL` would let chain-revoke also denylist the access tokens issued from each chain node (§8.5 final paragraph). Adds one row per refresh, low cost, real defence-in-depth gain. |
| OI-JWT-03 | Should rotation interval (default 180 d) be exposed in admin UI as a setting, or kept as a filter only? Filter-only is more "ops-grade"; UI is friendlier. |
| OI-JWT-04 | Confirm `firebase/php-jwt` minimum version once the WP plugin scaffold is generated; pin in `composer.json`. |
| OI-JWT-05 | If a future version moves to Ed25519 (EdDSA), the JWKS shape changes (`kty=OKP`, `crv=Ed25519`, `x`); §6.2 example must be revised, and verifiers MUST be told to support both `kty=RSA` and `kty=OKP` during the migration window. Plan the cutover document before bumping `gl_v`. |
| OI-JWT-06 | Cross-region WP installs (multi-site, geo-replicated DB): the denylist and watermark must be replicated synchronously, otherwise revocation has propagation lag. Document the constraint or scope the plugin to single-region. |

---

*JWT subsystem — keys, claims, JWKS, refresh-rotation, denylist. Algorithm is pinned. Reuse detection chain-revokes. No oracle in error responses. No swallow.*
