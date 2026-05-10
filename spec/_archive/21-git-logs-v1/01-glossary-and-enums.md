> ⚠️ **DEPRECATED — Legacy v1 Spec (folder 21)**  
> This document is preserved for historical reference only. **Do not implement against it.**  
> The active specification is **v2** in [`spec/22-git-logs-v2/`](../../22-git-logs-v2/00-overview.md) (SQLite, no JWT, SSH-key auth).  
> See [`spec/22-git-logs-v2/00-overview.md`](../../22-git-logs-v2/00-overview.md) for the current canonical source.  
> Deprecated: 2026-04-25

---

# Glossary and Enum Catalog

**Version:** 1.0.0  
**Updated:** 2026-04-24

---

## Overview

This document defines all domain terms and the canonical enum catalog used across the `git-logs` plugin. Every enum is backed by a join/lookup table in the database (see [02-database-schema-and-erd.md](./02-database-schema-and-erd.md)). No string literals are used as status/type/category values in code — only enum constants.

---

## Glossary

| Term | Definition |
|------|------------|
| Plugin user | An identity managed by `git-logs` itself, distinct from a WordPress user. Identified by `username`; authenticated by a one-time token (only the hash is stored). |
| WordPress user | A standard WP user. Used only by the WP-auth bridge to create plugin users; never receives a plugin token directly. |
| Token | A high-entropy secret (≥ 32 bytes base64url) issued to a plugin user. Shown once; only `tokenHash` (Argon2id) persisted. |
| JWT | RS256-signed JSON Web Token issued by the plugin. Carries `sub`, `roles`, `iat`, `exp`, `jti`. |
| Refresh token | Opaque rotating token; 7-day TTL; revocable; one active per session. |
| Repository | A registered GitHub repo or owner (User/Org) eligible to push logs. |
| `logSenderToken` | Per-repository HMAC secret used to sign the envelope JWT on `POST /logs/push`. |
| Envelope JWT | A JWT signed with the per-repo `logSenderToken` (HS256) wrapping `{ repoUrl, branch, pipelineName, exp }`. |
| Pipeline | Logical grouping of log entries within a `(repository, branch)`. Typically the CI pipeline name. |
| Log entry | A single timestamped, severity-tagged message belonging to a pipeline. |
| Audit trail | Append-only record of every endpoint hit and every transaction outcome. |
| Allowlist | The set of repositories/owners that are permitted to push logs. |
| Wildcard matching | Acceptance of versioned repo variants (`repo-v2`, `repo-v100`) under one base entry. |

---

## Enum Catalog

> **Convention:** Each enum has a lookup table named `{EnumName}` with PK `{enumName}Id` and `name` column. Codes are PascalCase.

### UserStatus

| Code | Description |
|------|-------------|
| Active | User can authenticate and use issued tokens |
| Suspended | Authentication blocked; tokens not revoked |
| Revoked | Authentication blocked; all tokens invalidated |

### Role

| Code | Description |
|------|-------------|
| Admin | Full access to all endpoints |
| CanAddRepo | Create/update/delete repositories |
| CanAddUser | Create/update plugin users |
| CanViewLogs | Query log retrieval endpoints |
| CanPushLogs | Reserved for future authenticated push variant |

### Provider

| Code | Description |
|------|-------------|
| GitHub | Active in v1 |
| GitLab | Reserved; not selectable in v1 |

### OwnerType

| Code | Description |
|------|-------------|
| User | A GitHub user account |
| Organization | A GitHub organization |

### VersionMode

| Code | Description |
|------|-------------|
| Exact | Match the stored `repoName` exactly |
| Wildcard | Match `repoName` or `repoName-v{N}` for any positive integer `N` |

### AcceptanceMode

| Code | Description |
|------|-------------|
| RepoUrl | Only the specific `(ownerName, repoName)` matches |
| OwnerWildcard | Any repository owned by `ownerName` matches |

### RepositoryStatus

| Code | Description |
|------|-------------|
| Active | Accepts log pushes and appears in retrieval lists |
| Disabled | Rejects log pushes; remains queryable |

### LogSeverity

| Code | Numeric | Description |
|------|---------|-------------|
| Trace | 10 | Verbose tracing |
| Debug | 20 | Debug detail |
| Info | 30 | Informational |
| Warn | 40 | Warning |
| Error | 50 | Error |
| Fatal | 60 | Fatal/abort |

### AuditActionType

| Code | Description |
|------|-------------|
| UserCreate | Plugin user created |
| UserUpdate | Plugin user updated |
| UserDelete | Plugin user deleted |
| TokenIssue | Token generated |
| TokenRevoke | Token revoked |
| RepoCreate | Repository registered |
| RepoUpdate | Repository updated |
| RepoDelete | Repository deleted |
| LogPush | Log push attempted |
| LogQuery | Log retrieval performed |
| AuthSuccess | Authentication succeeded |
| AuthFail | Authentication failed |

### AuditOutcome

| Code | Description |
|------|-------------|
| Success | Action completed successfully |
| Rejected | Action rejected by validation/policy |
| Error | Action failed due to runtime error |

---

## Cross-References

- [02-database-schema-and-erd.md](./02-database-schema-and-erd.md) — Lookup tables for each enum
- 13-coding-guidelines-applied.md (`13-coding-guidelines-applied` — removed in v1 deprecation) — Enum usage rules
