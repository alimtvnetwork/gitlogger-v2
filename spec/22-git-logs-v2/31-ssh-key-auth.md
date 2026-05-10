# SSH Key Authentication (v2.x)

**Version:** 2.9.1  
**Updated:** 2026-04-26 (Phase 5: SshKey + SshNonce now in canonical §18 DDL; SshAuthMode + SshNonceJanitorBatch in ConfigKv seeds)  
**Status:** Lane B preferred mechanism. Coexists with TempToken/Token (deprecated, removal in v3.0.0).

---

## Why SSH

- One key proves repo identity end-to-end; no secret rotation per Profile.
- Standard OpenSSH tooling (`ssh-keygen -Y sign` / `-Y verify`) — no custom crypto.
- Maps cleanly to GitHub deploy keys; CI already manages SSH keys.
- Eliminates plain-text TempToken sitting in CI environment.

---

## Model: Deploy Key (One Key → One Repo)

- Each `SshKey` row is bound to exactly one `RepoId`.
- A `Repo` may have multiple active keys (rotation, multi-CI).
- Acceptance and `IsRestrictInBranch` continue to come from the `GitProfile` that owns the `Repo`. No duplication on `SshKey`.

---

## SshKey Table

| Column | Type | Notes |
|--------|------|-------|
| SshKeyId | INTEGER PK AI | Project-wide PK convention. |
| Fingerprint | TEXT UNIQUE NOT NULL | `SHA256:` + base64 of SHA-256 of public key (RFC 4716). Lowercase `sha256:` normalized to uppercase prefix on insert. |
| RepoId | INTEGER FK → Repo NOT NULL | Deploy-key binding. |
| KeyType | TEXT NOT NULL | `ssh-ed25519`, `ssh-rsa`, `ecdsa-sha2-nistp256`, … |
| PublicKey | TEXT NOT NULL | Full OpenSSH single-line public key (`<type> <base64> [comment]`). |
| Label | TEXT NULL | Human label (`gh-actions-prod`). |
| OwnedByProfileId | INTEGER FK → Profile NOT NULL | Profile that registered the key (audit + UI ownership). |
| IsActive | INTEGER 0/1 NOT NULL DEFAULT 1 | Soft-disable on rotation. |
| LastUsedAt | INTEGER NULL | Updated on successful auth. |
| CreatedAt | INTEGER NOT NULL | |
| RevokedAt | INTEGER NULL | Set when IsActive flipped to 0. |

Indexes: `(Fingerprint)` (covered by UNIQUE), `(RepoId, IsActive)`, `(OwnedByProfileId)`.

---

## SshNonce Table (replay defense)

| Column | Type | Notes |
|--------|------|-------|
| SshNonceId | INTEGER PK AI | |
| SshKeyId | INTEGER FK → SshKey NOT NULL | Bound to the verified key. |
| Nonce | TEXT NOT NULL | Client-supplied, ≥16 bytes base64. |
| SeenAt | INTEGER NOT NULL | Unix seconds. |

Unique: `(SshKeyId, Nonce)`.  
Retention: **`ReplayWindowSeconds` only** (default 300s). Rows older than the window are pruned on every request (LIMIT `SshNonceJanitorBatch`) and via daily WP-cron. No long-term forensic copy — replay defense only.

---

## Request Shape (Lane B with SSH)

```
POST /wp-json/git-logs/v2/append-log
Headers:
  X-GL-Auth-Mode: ssh
  X-GL-Fingerprint: SHA256:abc123...
  X-GL-Timestamp: 1745568000        # Unix seconds (UTC)
  X-GL-Nonce: 9b1f...               # base64, ≥16 bytes
  X-GL-Signature: -----BEGIN SSH SIGNATURE-----
                  ...
                  -----END SSH SIGNATURE-----
Content-Type: application/json
Body: { "RepoUrl": "...", "Branch": "...", "Lines": [...] }
```

### Signed Payload

The signature covers the **canonical signing string** (LF-joined, no trailing newline):

```
GL-SSHSIG-V1
<HTTP_METHOD_UPPER>
<REQUEST_PATH>
<X-GL-Timestamp>
<X-GL-Nonce>
<sha256-hex(request-body-bytes)>
```

- `namespace` for `ssh-keygen -Y sign` MUST be `git-logs@v2`.
- `hash-algorithm` MUST be `sha512` (OpenSSH default).

### CI signing example

```bash
BODY=$(cat payload.json)
TS=$(date -u +%s)
NONCE=$(head -c 16 /dev/urandom | base64)
BODY_SHA=$(printf '%s' "$BODY" | sha256sum | awk '{print $1}')

printf 'GL-SSHSIG-V1\nPOST\n/wp-json/git-logs/v2/append-log\n%s\n%s\n%s' \
  "$TS" "$NONCE" "$BODY_SHA" \
  | ssh-keygen -Y sign -f ~/.ssh/id_ed25519 -n git-logs@v2 \
  > sig.asc

curl -X POST https://site/wp-json/git-logs/v2/append-log \
  -H "X-GL-Auth-Mode: ssh" \
  -H "X-GL-Fingerprint: $(ssh-keygen -lf ~/.ssh/id_ed25519.pub | awk '{print $2}')" \
  -H "X-GL-Timestamp: $TS" \
  -H "X-GL-Nonce: $NONCE" \
  -H "X-GL-Signature: $(cat sig.asc)" \
  -H "Content-Type: application/json" \
  --data-binary "$BODY"
```

---

## Server Validation Order (SSH lane)

Order matters; first failure aborts and writes `AuditTrail.AuthFail`.

1. **Mode header** — `X-GL-Auth-Mode: ssh` present → enter SSH lane. Else fall through to TempToken lane (§05).
2. **Header completeness** — fingerprint, timestamp, nonce, signature all present → else `GL-SSH-HEADER-MISSING`.
3. **Timestamp skew** — `|now - X-GL-Timestamp| ≤ ReplayWindowSeconds` (default 300). Else `GL-SSH-TIMESTAMP-SKEW`.
4. **SshKey lookup** — `SELECT … WHERE Fingerprint=? AND IsActive=1`. Miss → `GL-SSH-KEY-UNKNOWN`. Inactive row → `GL-SSH-KEY-INACTIVE`.
5. **Repo binding** — parse `RepoUrl` → resolve to `RepoId`; must equal `SshKey.RepoId`. Else `GL-SSH-REPO-MISMATCH`.
6. **Acceptance + branch** — apply GitProfile rules (acceptance, `IsRestrictInBranch`) exactly as §05 steps 3–4.
7. **Nonce uniqueness** — `INSERT OR IGNORE INTO SshNonce(SshKeyId, Nonce, SeenAt)`. Affected rows = 0 → `GL-SSH-NONCE-REUSED`.
8. **Signature verify** — reconstruct canonical signing string; call `ssh-keygen -Y verify` (or PHP equivalent via `phpseclib`) with `PublicKey`, namespace `git-logs@v2`. Failure → `GL-SSH-SIGNATURE-INVALID`.
9. **Profile status** — `OwnedByProfileId.UserStatus` must be `Active`. Else `GL-AUTH-PROFILE-INACTIVE`.
10. **App lifecycle** — if request resolves to an `App`, `AppStatus=Active` required. Else `GL-APP-NOT-ACTIVE`.

On success: `UPDATE SshKey SET LastUsedAt=? WHERE SshKeyId=?`; `AuditTrail.SshAuthSuccess`.

---

## Coexistence with TempToken (v2.x)

- Endpoints inspect `X-GL-Auth-Mode`. Missing or `temptoken` → §05 TempToken lane runs unchanged.
- A request MUST NOT mix lanes; presence of `X-GL-Auth-Mode: ssh` AND `TempToken` body field → `GL-SSH-LANE-CONFLICT`.
- `ConfigKv.SshAuthMode`:
  - `optional` (default in 2.7.0) — both lanes accepted.
  - `preferred` — TempToken accepted but emits `Deprecation` HTTP header.
  - `required` — TempToken rejected with `GL-AUTH-LANE-DISABLED`.
- v3.0.0 will hard-default to `required` and drop the TempToken code path.

---

## Key Lifecycle

| Action | Effect |
|--------|--------|
| Register | Admin UI uploads public key; server computes fingerprint; row inserted, `IsActive=1`. |
| Rotate | Register new key, then PATCH old one to `IsActive=0` (sets `RevokedAt`). |
| Revoke | Same as rotate without replacement. |
| Audit | `AuditTrail.SshKeyRotated` row written on every IsActive transition. |

Public key is rendered in UI but never downloaded as a "secret" — it is public by definition.

---

## Error Codes

| Code | HTTP | Step |
|------|------|------|
| GL-SSH-HEADER-MISSING | 400 | 2 |
| GL-SSH-TIMESTAMP-SKEW | 401 | 3 |
| GL-SSH-KEY-UNKNOWN | 401 | 4 |
| GL-SSH-KEY-INACTIVE | 403 | 4 |
| GL-SSH-REPO-MISMATCH | 403 | 5 |
| GL-SSH-NONCE-REUSED | 401 | 7 |
| GL-SSH-SIGNATURE-INVALID | 401 | 8 |
| GL-SSH-LANE-CONFLICT | 400 | mode parse |
| GL-AUTH-LANE-DISABLED | 403 | mode parse (when `SshAuthMode=required`) |

(Existing `GL-AUTH-PROFILE-INACTIVE`, `GL-APP-NOT-ACTIVE`, `GL-VALIDATION-*` reused.)

---

## ConfigKv Defaults

| KeyName | ValueText | Purpose |
|---------|-----------|---------|
| SshAuthMode | `optional` | Lane gate (optional / preferred / required) |
| ReplayWindowSeconds | `300` | Timestamp tolerance |
| SshNonceJanitorBatch | `100` | Rows pruned per request |

---

## AuditActionType Seeds (added)

| Id | Name |
|----|------|
| 22 | SshAuthSuccess |
| 23 | SshAuthFail |
| 24 | SshKeyRotated |

---

## Open Items (handled in dependent specs)

- §02 — append `SshKey`, `SshNonce` tables (task: §02 schema update).
- §05 — insert SSH lane block before TempToken lane, link to this doc (task: §05 update).
- §15 — append `GL-SSH-*` table (task: §15 errors).
- §28 — replace TempToken curl example with SSH-signing example (task: §28 GH Actions).
- §30 — threat model entries for replay, key theft, signature stripping, lane downgrade (task: §30).
