# Phase 2 — Dual Auth Lanes (Acceptance)

Adds two authentication paths to the plugin and `glci`. From here on, every new endpoint should be protected by `AuthContext::require_authenticated`.

## Components shipped in P2

| Component | Path | Purpose |
|-----------|------|---------|
| AuthContext | `git-logs-plugin/includes/auth/class-auth-context.php` | REST `permission_callback` — accepts WP-core auth (App Password / cookie) OR `X-GitLogs-Auth` |
| Ed25519Resolver | `git-logs-plugin/includes/auth/class-ed25519-resolver.php` | Parses `X-GitLogs-Auth`, verifies via `sodium_crypto_sign_verify_detached` |
| NonceStore | `git-logs-plugin/includes/auth/class-nonce-store.php` | Replay protection (transients, 600s TTL) |
| PublicKeys | `git-logs-plugin/includes/auth/class-public-keys.php` | Per-user Ed25519 key registry in `user_meta` |
| `/whoami` | `git-logs-plugin/includes/rest/class-rest-whoami.php` | Authenticated identity probe |
| `/keys` | `git-logs-plugin/includes/rest/class-rest-keys.php` | List/add/delete current user's keys |
| glci auth | `glci/internal/auth/auth.go` | Lane resolution + Ed25519 signing client-side |
| `glci whoami` | `glci/internal/cmd/whoami.go` | Calls `/whoami` with either lane |
| `glci keys generate` | `glci/internal/cmd/keys.go` | Generates a fresh Ed25519 keypair |

## Auth contract — Ed25519 lane

### Header

```
X-GitLogs-Auth: GLCI1-ED25519 keyId=<id>,nonce=<n>,ts=<unix>,sig=<base64>
```

### Canonical signing string (LF-separated, **no trailing LF**)

```
GLCI1-ED25519
<METHOD>                  # uppercase: GET, POST, ...
<PATH-AND-QUERY>          # e.g. "/wp-json/git-logs/v1/whoami"
<SHA256_HEX_OF_BODY>      # sha256("") for empty body
<NONCE>                   # [A-Za-z0-9_-]{1,64}, single-use within 600s
<TIMESTAMP>               # unix seconds, ±300s of server clock
<KEY_ID>                  # 8-hex char id assigned by server when key was registered
```

### Verification rules (server)

1. Parse header; require `keyId`, `nonce`, `ts`, `sig`.
2. `|now - ts| ≤ 300s` else reject `clock_skew`.
3. `(keyId, nonce)` not in NonceStore else reject `replay`; otherwise remember for 600s.
4. Look up `(user_id, raw_pubkey_32)` from `user_meta` by `keyId`; reject `unknown_key` if missing.
5. Reconstruct canonical string from request, verify with libsodium; reject `invalid_sig` on failure.
6. On success: `wp_set_current_user(user_id)`, touch `last_used_utc`, return `user_id`.

### Key file formats (`glci`)

```
# Private (mode 0600):
glci-ed25519-priv <base64 of 32-byte seed>

# Public (uploaded to plugin):
glci-ed25519 <base64 of 32-byte pubkey>
```

## Acceptance checklist

### 1. Plugin loads without fatals
After replacing the P1 plugin, activate v0.2.0. No errors. `wp-admin/admin.php?page=git-logs` still loads.

### 2. App Password lane works
```bash
# In WP admin: Users → Profile → Application Passwords → "Add New" → label "glci-test"
curl -s -u alice:'XXXX YYYY ZZZZ AAAA' \
  https://your-site.test/wp-json/git-logs/v1/whoami | jq
# expect: { "user_id": ..., "user_login": "alice", "auth_lane": "wp_session", ... }
```

Or via glci:
```bash
./glci whoami --base https://your-site.test --user alice --app-password 'XXXX YYYY ZZZZ AAAA'
```

### 3. Ed25519 lane works
```bash
# Generate a keypair
./glci keys generate --out ~/.glci/key --label ci-runner
# Register the public key (using App Password to bootstrap)
PUB=$(awk 'NR==1{print $2}' ~/.glci/key.pub)
KEY_ID=$(curl -s -u alice:'XXXX YYYY ZZZZ AAAA' \
  -H 'Content-Type: application/json' \
  -X POST https://your-site.test/wp-json/git-logs/v1/keys \
  -d "{\"label\":\"ci-runner\",\"pubkey_b64\":\"$PUB\"}" | jq -r .id)

# Use Ed25519 lane
./glci whoami --base https://your-site.test --key-id "$KEY_ID" --key-file ~/.glci/key
# expect: { "user_id": ..., "auth_lane": "ed25519", ... }
```

### 4. Replay protection
Re-running the exact same request within 600s with a captured nonce returns HTTP 401 `git_logs_auth_replay`. (`glci` always generates a fresh nonce, so to test, capture the header with `tcpdump`/`mitmproxy` and replay via `curl`.)

### 5. Clock skew rejection
Set system clock ±10 minutes off, run `glci whoami` with Ed25519 lane → HTTP 401 `git_logs_auth_clock_skew`.

### 6. Unauthenticated request to a protected route
```bash
curl -i https://your-site.test/wp-json/git-logs/v1/whoami
# expect: HTTP/1.1 401 git_logs_unauthorized
```

## What is NOT in P2

- Admin UI for managing keys → P7 (settings page)
- Audit log of auth events → P3 (audit table) + P4 (`/audit` endpoint)
- Per-key scopes / role restrictions → can be added later as a `scopes` field on the key record (additive, not breaking)
- Rate limiting → P8 (security pass)

## Decisions locked in P2

- **Scheme tag**: `GLCI1-ED25519` (single literal, versioned via `1`; if we ever need a v2 we'll mint `GLCI2-...`)
- **Header name**: `X-GitLogs-Auth` (single header, not split across `Authorization` to avoid colliding with App Password Basic)
- **Timestamp window**: ±300s
- **Nonce TTL**: 600s (2× window)
- **Body hash**: `sha256` hex of raw bytes (empty body → sha256 of empty string)
- **Key id**: 8 hex chars, server-assigned at registration
- **Public key wire format**: base64 of 32-byte raw Ed25519 (NOT OpenSSH, NOT PEM — keeps verifier dependency-free)
