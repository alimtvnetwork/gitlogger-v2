# Headless WordPress — Auth Notes (v2)

**Version:** 2.5.0  
**Updated:** 2026-04-25

Many WP installs run headless: no admin browser sessions, REST consumers authenticate via JWT plugins. This document describes which auth setups Git Logs v2 supports and which it does not.

---

## v2 auth lanes (recap)

| Lane | Endpoints | Credential |
|------|-----------|------------|
| A — Admin/read | `/get-logs`, `/get-pipeline-logs`, `/get-error-logs`, `/get-pipeline-error-logs`, admin UI, `/metrics` | WP cookie OR WP Application Password |
| B — CI/CD write | `/append-log`, `/fixed-log`, `/clear-log`, `/clear-log-all` | `TempToken` + `Token` in JSON body |

Lane B never participates in WP's auth pipeline; it self-validates against the `Profile` table. Headless setups affect Lane A only.

---

## Supported headless setups

### 1. WP Application Passwords (recommended)

Built into WP core since 5.6. No plugin needed.

```
curl -u "alice:xxxx xxxx xxxx xxxx xxxx xxxx" \
  https://wp.example.com/wp-json/git-logs/v2/get-logs?q=https://github.com/acme/api@main
```

Permissions resolve via the WP user's role mapped to a Git Logs `Profile` (matching by `Email`). If no Profile match, request is rejected with `GL-AUTH-NO-PROFILE-LINK`.

### 2. WP REST nonce + cookie (browser SPAs only)

Standard WP nonce in `X-WP-Nonce` header. Same Profile-link rule applies.

### 3. **JWT Authentication for WP REST API** by Enrique Chavez (`wp-api-jwt-auth`)

Supported. The plugin verifies WP user identity via the JWT plugin's filter, then resolves to a Git Logs Profile via `Email` match.

Caveats:

- The JWT plugin must be configured with a strong `JWT_AUTH_SECRET_KEY` (≥ 256 bits).
- `JWT_AUTH_CORS_ENABLE` must align with the consumer origin.
- Token expiry is enforced by the JWT plugin, not by Git Logs.

### 4. WP OAuth Server (e.g. **WP OAuth Server** by WP-API)

Supported for Lane A reads. Same Profile-link rule applies. Bearer token is verified by the OAuth plugin's filter chain before the Git Logs route handler runs.

---

## Unsupported / use at your own risk

| Setup | Why unsupported |
|-------|-----------------|
| **JWT Auth** by useotp / random forks | Multiple plugins share the name; their filter hooks differ. Pick the Enrique Chavez one or expect failures. |
| Custom auth middlewares that bypass `determine_current_user` | Git Logs trusts `wp_get_current_user()`; bypassing it leaves Lane A wide open. |
| Service-account "shared secret" header schemes | Use Application Passwords or Lane B's TempToken instead. |
| External SSO that doesn't create a WP user | No WP user → no Profile link → reject. Provision a WP user first. |

---

## Profile linkage rules

When a Lane A request arrives:

1. Resolve `wp_get_current_user()` → must be non-zero. Reject with `GL-AUTH-NOT-LOGGED-IN` otherwise.
2. Look up `Profile` row where `Email = wp_user.user_email`. Reject with `GL-AUTH-NO-PROFILE-LINK` if missing.
3. Check `Profile.UserStatusId = Active`. Reject with `GL-AUTH-PROFILE-SUSPENDED` otherwise.
4. Check the route's required `Permission` against `RolePermission` for the Profile's roles.
5. Proceed.

This means: **every WP user who needs read access must have a matching Git Logs Profile with the same email.** Bootstrap (§03) creates the first one; subsequent admins create more via the Profile screen.

---

## Recommendation matrix

| Caller | Use |
|--------|-----|
| CI/CD workflow pushing logs | Lane B (TempToken in body) |
| CI/CD workflow reading logs | Lane A with WP Application Password |
| SPA dashboard | Lane A with cookie + nonce |
| Mobile app | Lane A with JWT (Chavez plugin) |
| Server-to-server batch reader | Lane A with WP Application Password |
| Curl one-liner from operator's laptop | Lane A with WP Application Password |

Lane B is **only** for the four push endpoints. Trying to call `/get-logs` with a TempToken returns `GL-AUTH-WRONG-LANE`.

---

## CORS

Read endpoints emit `Access-Control-Allow-Origin` only when `ConfigKv.AllowedReadOrigins` lists the request `Origin`. Default empty (same-origin only). Push endpoints (Lane B) never participate in CORS — they're called server-to-server.
