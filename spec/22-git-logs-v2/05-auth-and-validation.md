# Authentication and Validation (v2)

**Version:** 2.9.1  
**Updated:** 2026-04-26 (Phase 6: SSH lane block confirmed authoritative; §31 + §15 + §18 v2.9.1 cross-refs verified)  
**JWT:** dropped entirely.

---

## Two Auth Lanes

### Lane A — Admin / Write UI

- WordPress **Application Password** OR cookie auth.
- Resolves to a WP user → mapped to a plugin `Profile` via `Profile.UserName`.
- Authorization always via `RolePermission` (never role-name comparison).

### Lane B — CI/CD Endpoints (`/append-log`, `/fixed-log`, `/clear-log`, `/clear-log-all`)

Lane B has **two sub-modes** selected by header `X-GL-Auth-Mode`:

- `ssh` (preferred from v2.7.0) — SSH deploy-key signature. **Full spec: [§31 SSH Key Authentication](31-ssh-key-auth.md).**
- `temptoken` (default when header absent; deprecated, removal in v3.0.0) — body-carried `TempToken` + `Token`.

Lane gating is governed by `ConfigKv.SshAuthMode` ∈ { `optional` (default), `preferred`, `required` }. When `required`, TempToken submissions reject with `GL-AUTH-LANE-DISABLED`.

A request MUST NOT mix lanes — `X-GL-Auth-Mode: ssh` together with a body `TempToken` field rejects as `GL-SSH-LANE-CONFLICT`.

Regardless of sub-mode, **the authoritative gate is GitHub URL + branch + GitProfile acceptance**. Credentials (TempToken or SSH signature) confirm the caller; they do not authorize the repo.

#### TempToken Sub-mode — Validation Steps

In order. No early exit may mask the rejection reason in the response body.

1. **Parse** `RepoUrl` → `(provider, owner, repoName, versionSuffix)`.
2. **Locate GitProfile** by `(Provider, OwnerName)`.
   - Not found → reject `GL-VALIDATION-PROFILE-NOT-FOUND`.
3. **Acceptance check**:
   - `AcceptAllRepos`: pass.
   - `AcceptSelectedRepoOnly`: `RepoUrl` must equal `SelectedRepoUrl` exactly. Else reject `GL-VALIDATION-REPO-NOT-ALLOWED`.
   - `AcceptSelectedRepoInAllVersions`: derive `RootRepoName` from both stored `SelectedRepoUrl` and inbound `RepoUrl` (strip `-v\d+$`); both must match; `versionSuffix` ∈ {empty, `v\d+`}. Else reject same code.
4. **Branch restriction**: if `IsRestrictInBranch=1`, inbound `Branch` must equal `StrictBranch`. Else reject `GL-VALIDATION-BRANCH-RESTRICTED`.
5. **TempToken** check: must match a `Profile.TempToken` (any active Profile). If not → reject `GL-AUTH-TEMPTOKEN-INVALID`. (Intentionally non-localized to a Profile in error response.)
6. **Token** check: must match `Profile.Token` of the **same Profile** that owns the matched `TempToken`. Else reject `GL-AUTH-TOKEN-MISMATCH`.
7. **Profile UserStatus** must be `Active`. Else `GL-AUTH-PROFILE-INACTIVE`.
8. **App lifecycle (optional)**: if request resolves to a linked `App`, require `AppStatus=Active`. Else `GL-APP-NOT-ACTIVE`.

#### SSH Sub-mode — Validation Steps

Full payload shape, signing string, and code samples in §31. The 10-step order is reproduced here for cross-reference:

1. Mode header present (`X-GL-Auth-Mode: ssh`) → enter SSH lane.
2. Header completeness (fingerprint, timestamp, nonce, signature) → else `GL-SSH-HEADER-MISSING`.
3. Timestamp skew within `ReplayWindowSeconds` → else `GL-SSH-TIMESTAMP-SKEW`.
4. SshKey lookup by `Fingerprint` AND `IsActive=1` → else `GL-SSH-KEY-UNKNOWN` / `GL-SSH-KEY-INACTIVE`.
5. Repo binding: parsed `RepoUrl` → `RepoId` must equal `SshKey.RepoId` → else `GL-SSH-REPO-MISMATCH`.
6. Acceptance + branch rules (reuses TempToken steps 3–4 above).
7. Nonce uniqueness (`INSERT OR IGNORE INTO SshNonce`) → else `GL-SSH-NONCE-REUSED`.
8. Signature verify against canonical signing string `GL-SSHSIG-V1` → else `GL-SSH-SIGNATURE-INVALID`.
9. Profile `UserStatus = Active` → else `GL-AUTH-PROFILE-INACTIVE`.
10. App lifecycle (when applicable) → else `GL-APP-NOT-ACTIVE`.

All outcomes (both sub-modes) write to `AuditTrail`:
- TempToken: `AuthSuccess` / `AuthFail`.
- SSH: `SshAuthSuccess` / `SshAuthFail` (seeded in §16).
- Common fields: `RouteName`, `RequestId`, `HttpStatus`, `ActorIp`.

---

## TempToken Rotation

- Generated automatically on Profile create.
- Regenerable from Profile UI; old value invalid immediately.
- Stored plain in v2 (encryption deferred).

---

## Why no JWT in v2

- CI/CD agents don't need a self-contained signed token; URL+branch+Profile validation is the real gate.
- Removes RS256 keypair, JWKS endpoint, refresh-token rotation, and signing infra.
- Re-introducible later behind a feature flag without breaking v2 endpoints.

---

## Error Codes (excerpt)

| Code | HTTP | Lane |
|------|------|------|
| GL-VALIDATION-PROFILE-NOT-FOUND | 404 | B |
| GL-VALIDATION-REPO-NOT-ALLOWED | 403 | B |
| GL-VALIDATION-BRANCH-RESTRICTED | 403 | B |
| GL-AUTH-TEMPTOKEN-INVALID | 401 | B |
| GL-AUTH-TOKEN-MISMATCH | 401 | B |
| GL-AUTH-PROFILE-INACTIVE | 403 | B |
| GL-APP-NOT-ACTIVE | 403 | B |
| GL-SSH-HEADER-MISSING | 400 | B (ssh) |
| GL-SSH-TIMESTAMP-SKEW | 401 | B (ssh) |
| GL-SSH-KEY-UNKNOWN | 401 | B (ssh) |
| GL-SSH-KEY-INACTIVE | 403 | B (ssh) |
| GL-SSH-REPO-MISMATCH | 403 | B (ssh) |
| GL-SSH-NONCE-REUSED | 401 | B (ssh) |
| GL-SSH-SIGNATURE-INVALID | 401 | B (ssh) |
| GL-SSH-LANE-CONFLICT | 400 | B (ssh) |
| GL-AUTH-LANE-DISABLED | 403 | B (mode gate) |
| GL-AUTH-WP-MISSING | 401 | A |
| GL-AUTHZ-PERMISSION-DENIED | 403 | A |

> Full catalog with HTTP status, cause, and caller action: [`15-error-codes.md`](./15-error-codes.md).

---

## CI/CD pipeline integration

Callers invoking Lane B endpoints from CI runners should follow the conventions in [`spec/12-cicd-pipeline-workflows/`](../12-cicd-pipeline-workflows/00-overview.md), specifically:

| Topic | Authoritative file |
|-------|--------------------|
| Where to inject `TempToken` / `Token` (job secrets, never repo-checked-in) | [`07-environment-variable-setup.md`](../12-cicd-pipeline-workflows/07-environment-variable-setup.md) |
| Standard CI job naming + ordering | [`01-ci-pipeline.md`](../12-cicd-pipeline-workflows/01-ci-pipeline.md) |
| Reusable guards (e.g., skip push if branch ∉ allowlist) | [`03-reusable-ci-guards/`](../12-cicd-pipeline-workflows/03-reusable-ci-guards/) |
| Failure-vs-success log routing (`HasError` flag wiring) | this doc + `01-ci-pipeline.md` §Failure handling |
| End-to-end curl examples per endpoint | [`14-endpoint-examples.md`](./14-endpoint-examples.md) |

Pipeline templates should send the `Pipeline` field as the CI job name (e.g. `build-and-test`, `deploy-prod`) so History views align with CI dashboards.
