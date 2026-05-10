# Gitlogs App — Endpoint And Behavior Verification Instruction (Verbatim Brief)

**Captured:** 2026-04-25 (UTC+8)
**Status:** Reference only — not yet acted on
**Authority:** This brief overrides any conflicting content in `spec/21-git-logs/` (folders 00–17, 97–99). Where this document and the existing spec disagree, **this document wins**.
**Companion files:**
- `Gitlogs_App.md` — XMind export (mind-map source)
- `Gitlogs_App.png` — mind-map screenshot

---

## 1. Verbatim Task Statement

This task is the verification of the endpoints and how the user wants the application to behave. A screenshot of the endpoints describes the desired visualization. The AI must visualize how it might work, define the menus it needs to have, and verify it against what is already in the spec for the Gitlogs app under folder 21.

If there is any inconsistency, **this conversation wins** over anything written before.

Diagrams must be created under folder 26 (the Gitlogs diagrams folder, e.g. `/spec/26-gitlogs-diagrams/`) containing the Mermaid ER diagram, design diagram, and endpoint diagrams.

Reference inputs:
1. The mind-map screenshot `Gitlogs App.png`.
2. The exported XMind content as an `.md` file.

---

## 2. Application Behavior

### 2.1 Top-level Menu (only these items)

1. Profile
2. Roles
3. AccessToRoles
4. GitProfile
5. Repo
6. RepoVersion
7. History
8. Action

- Level 1 = menu item. Level 2 = what is inside (fields and tables).
- Items marked `format:hide` in the mind-map (e.g. `format:hide` notes under GitProfile) are informational only and **must not** be rendered in the user-facing UI.

### 2.2 Profile

- Fields: `UserName`, `Email`, `GeneratedKeyApi`, `Token`.
- `GeneratedKeyApi` (API key) and `Token` are two separate values.
- **No password field.**
- All profile data is stored in the Gitlogs root SQLite DB, **not** in WordPress.
- Values stored plain for now. Encryption deferred.

### 2.3 Database, Migrations, Logging

- Single root SQLite database for Gitlogs.
- On every application boot, check whether the database needs migration.
- Migration state may live in the DB, in a config entry, or in a JSON file on disk — must include the plugin version number.
- On boot: read current plugin version → if already migrated, skip; if not, run once and mark done.
- New plugin version → marker for that version does not exist yet → migration runs once then is marked done.
- Logger must support log levels (debug, info, warn, error) and must allow disabling info/debug later.
- Avoid duplicate log entries; deduplicate where sensible.

### 2.4 Roles

- Independent from WordPress roles; live only in the Gitlogs SQLite DB.
- Default roles: `Admin`, `Editor`.
- Modeled as Enum in code **and** relational table in DB.

### 2.5 AccessToRoles (Permissions)

- Permissions are assigned to roles.
- Admin has all access by default.
- The application **always checks the permission, not the role**, for authorization.
- Example permissions: `AppCreate`, `AppView`, `AppModify`, `AppDelete`. CRUD-style grouping is acceptable.
- Example: Editor may have View and Modify but not Create or Delete.
- Permissions and role-to-permission mapping must be modeled relationally (1-N or N-M as appropriate).

---

## 3. Domain Model

### 3.1 Top-down Hierarchy

- `GitProfile` is the top-most master entity.
- `Repo` is a child of `GitProfile`.
- `App` may link to `Repo` or directly to `GitProfile`.
- `App` and `Repo` may be connected or disconnected; both states are valid.

### 3.2 GitProfile

- Supports GitHub now. Schema must be **provider-aware** so GitLab and others can be added.
- A `GitProfile` represents either a user or an organization.
- URL patterns:
  - `github.com/{user}/{repo}`
  - `github.com/{org}/{repo}`
- Profile input may be a user URL or an organization URL.
- Trailing slash on input is optional. Normalize to a single canonical format on save (**prefer with trailing slash**).

### 3.3 Add Profile UI

- First input: profile URL (user or organization).
- `Acceptance` dropdown (Enum):
  1. `AcceptAllRepos` — any repo under this profile is accepted automatically.
  2. `AcceptSelectedRepoOnly` — only the explicitly selected repo URL is accepted.
  3. `AcceptSelectedRepoInAllVersions` — accept the main repo plus any `-vN` variants. Pattern detection must derive the main repo and all variants.
- Branch restriction:
  - `IsRestrictInBranch` — boolean checkbox, default disabled.
  - `StrictBranch` — string, hidden in UI unless `IsRestrictInBranch` is enabled.
  - When enabled, only transitions from `StrictBranch` are accepted.

### 3.4 Profiles List

- Profiles list view at the top of the GitProfile section.
- Edit Profile flow mirrors Add Profile.

### 3.5 Repo and RepoVersion

- `Repo` = master repo (no version suffix). Derive the main URL from any incoming repo URL and store it as the main repo.
- `RepoVersion` stores each version variant linked to the main `Repo`.
- Every new version encountered must be inserted into `RepoVersion`.
- `History` and `Action` records are linked to `RepoVersion`.

### 3.6 App

- App is registered by the user.
- App may belong to a `Repo` or directly to a `GitProfile`.
- Detailed App fields deferred.

---

## 4. Authentication and Security

1. All write operations on `Profile`, `Repo`, `RepoVersion`, and `History` require authentication, equivalent to the WordPress application password flow.
2. Without authentication, no profile, repo, or repo history can be modified.
3. Token model on the Profile:
   - `GeneratedKeyApi` (API key)
   - `Token` (generated token)
   - `TempToken` (random value generated automatically and stored on the Profile)
4. Endpoint authentication rules:
   - CI/CD endpoints accept only `TempToken` for validation.
   - `TempToken` is intentionally random so attackers cannot infer where validation happens.
   - **Real validation** happens against the GitHub URL and branch name. If those two are invalid, reject; the token is also checked to add a layer of confusion.
   - Consider issuing a JWT (built from `GeneratedKeyApi` + `Token`) only if it genuinely improves security.

---

## 5. Endpoints

### 5.1 General Rules

- Every write endpoint must respond with a clear acknowledgement so CI/CD knows the transaction succeeded.
- Every response should also indicate how the user can retrieve the corresponding logs.
- Use Enums and Constants for all statuses, kinds, and event types. **No magic strings.**

### 5.2 Endpoint Catalog

| # | Method | Path | Purpose | Body Fields | Response Shape |
|---|--------|------|---------|-------------|----------------|
| 1 | POST | `/append-log` | Append/stream logs for a commit | `RepoUrl`, `RootRepo`, `Branch`, `TempToken`, `Token`, `PipelineName`, `GitSha256`, `Logs[]`, `ErrorLogs[]`, `FilePaths[]`, `HasError` | Ack + retrieval hint |
| 2 | PUT  | `/fixed-log` | Mark pipeline as fixed | `RepoUrl`, `Branch`, `TempToken`, `RootRepo`, `Token`, `PipelineName` | Ack |
| 3 | POST | `/clear-log` | Clear logs for a single pipeline | `RepoUrl`, `Branch`, `TempToken`, `RootRepo`, `Token`, `PipelineName` | Ack |
| 4 | POST | `/clear-log-all` | Clear all logs for repo/branch | `RepoUrl`, `Branch`, `TempToken`, `RootRepo`, `Token` | Ack |
| 5 | GET  | `/get-logs` | All logs for a repo at a commit | `RepoUrl`, `GitSha256` | `RepoUrl`, `RootRepo`, `BranchName`, `PipelineNames[]`, `IsPass`, `HasError`, `ErrorLogs[{PipelineName,LogText}]`, `Logs[{PipelineName,LogText}]` |
| 6 | GET  | `/get-logs?q=github.com/{org}/{repo}` | URL-style variant of #5 | `GitSha256` | Same as #5 |
| 7 | GET  | `/get-pipeline-logs` | Logs for one pipeline | `RepoUrl`, `GitSha256`, `PipelineName` | `RepoUrl`, `RootRepo`, `BranchName`, `PipelineName`, `IsPass`, `HasError`, `ErrorLogs[]`, `Logs[]` |
| 8 | GET  | `/get-pipeline-logs?q=github.com/{org}/{repo}` | URL-style variant of #7 | `GitSha256`, `PipelineName` | Same as #7 |
| 9 | GET  | `/get-error-logs` | Only error logs across all pipelines | `RepoUrl`, `GitSha256` | `RepoUrl`, `RootRepo`, `BranchName`, `PipelineNames[]`, `IsPass`, `HasError`, `ErrorLogs[{PipelineName,LogText}]` |
| 10 | GET | `/get-pipeline-error-logs` | Error logs for one pipeline | `RepoUrl`, `GitSha256`, `PipelineName` | `RepoUrl`, `RootRepo`, `BranchName`, `PipelineName`, `IsPass`, `HasError`, `ErrorLogs[]` |

#### Notes per endpoint

- **#1 `/append-log`** — Streaming required. If `HasError` is true, persist that the branch currently has a pipeline issue; flag stays until `/fixed-log` is sent.
- **#2 `/fixed-log`** — Clears the "has error" state for the given pipeline/branch on that repo.
- **#4 `/clear-log-all`** — Does not require the per-pipeline token shape; authentication still applies.

---

## 6. Repo, History, and Action Views

- **Repo** — list view shows all repos; selecting opens its History.
- **History** — latest events: which app pushed what, when, on which branch, and the result. Linked through `RepoVersion`.
- **Action** — records actions performed on repos and pipelines (`append`, `fixed`, `clear`, `clear-all`).

---

## 7. Database Conventions (Mandatory)

1. SQLite is the default database (Gitlogs root DB).
2. PascalCase for all table names, column names, JSON keys, and JSON values where practical.
3. Every primary key is `INTEGER AUTOINCREMENT` and named `{TableName}Id` (e.g., `GitProfileId`).
4. Use the smallest appropriate integer type; never default everything to a large int.
5. Model `Type`, `Status`, `Category`, `Kind`, `Acceptance`, `Role`, `Permission` as Enums in code and as 1-N or N-M relational tables in DB.
6. Use proper foreign keys, normalization, and joins. No plain string columns for typed values.
7. Prefer ORM access. Read queries should go through views with pre-joined data when views are part of the design.
8. Define DB structure using markdown tables (not SQL) unless SQL is explicitly requested.

> **Note vs existing folder-21 spec:** Folder 21 currently uses string-prefixed PKs (e.g. `userId VARCHAR(36)` UUIDs) and PostgreSQL-style schemas. Per this brief, that must change to SQLite + integer auto-increment PKs.

---

## 8. Diagrams (Folder 26)

Create `/spec/26-gitlogs-diagrams/` with Mermaid diagrams:

| # | Diagram | Coverage |
|---|---------|----------|
| a | ER diagram | Profile, Role, Permission, RoleAccess, GitProfile, Repo, RepoVersion, App, History, Action, Pipeline, LogEntry, ErrorLogEntry, MigrationState, etc. |
| b | Domain/design diagram | Top-down hierarchy `GitProfile → Repo → RepoVersion → History/Action`, with `App` linkable to either `Repo` or `GitProfile` |
| c | Endpoint diagrams | All 10 endpoints in §5.2 |
| d | Authentication/validation flow | TempToken, GitHub URL + branch validation, optional JWT |
| e | Permission flow | Role → Permission → Action check |

Diagrams must reflect this conversation. Where folder 21 conflicts, this conversation wins.

---

## 9. Spec Verification (Folder 21)

1. Verify `/spec/21-git-logs/` against this brief.
2. List every inconsistency.
3. For each inconsistency, propose the corrected version aligned with this brief.
4. Update the spec to match, keeping the original input visible at the top of each updated spec file.

---

## 10. Acceptance Criteria

1. Menu renders only: Profile, Roles, AccessToRoles, GitProfile, Repo, RepoVersion, History, Action.
2. Profile stores `UserName`, `Email`, `GeneratedKeyApi`, `Token`, and an auto-generated `TempToken`, all in the SQLite root DB.
3. Migration runs once per plugin version and is skipped on subsequent boots of the same version.
4. Logger supports log levels and can disable info/debug at runtime.
5. Roles and permissions live in the Gitlogs SQLite DB, not in WordPress; authorization checks the permission, not the role.
6. GitProfile supports user and organization URLs, normalizes input, and stores `Acceptance` as one of `AcceptAllRepos`, `AcceptSelectedRepoOnly`, `AcceptSelectedRepoInAllVersions`.
7. `IsRestrictInBranch` toggles visibility and enforcement of `StrictBranch`.
8. Repo stores the main repo; RepoVersion stores every detected version variant and links back to Repo.
9. Every endpoint listed above is implemented with the exact request and response fields described.
10. `HasError` on `/append-log` persists the error state until `/fixed-log` clears it.
11. All write endpoints require authentication and respond with a structured acknowledgement plus retrieval guidance.
12. Validation rejects requests whose GitHub URL or branch does not match the GitProfile acceptance rules; `TempToken` is checked but is intentionally non-authoritative.
13. Folder 26 contains the Mermaid ER, design, endpoint, auth, and permission diagrams listed above.
14. Folder 21 spec is updated to match this conversation, with all inconsistencies resolved in favor of this conversation.
15. Database follows PascalCase, `{TableName}Id` auto-increment primary keys, smallest appropriate types, Enums for typed fields, and normalized 1-N / N-M relations.

---

## 11. Important Constraints

1. **Do not act on this task yet.** Proofread and structure only.
2. This conversation overrides any prior Gitlogs spec under folder 21 in case of conflict.
3. Reference inputs are `Gitlogs App.png` and the exported XMind `.md` file; treat them as authoritative for the mind-map structure.
4. All typed values (Roles, Permissions, Acceptance, Status, Kind, etc.) must be Enums in code **and** relational tables in the DB.
5. SQLite is the default DB. PascalCase naming and `{TableName}Id` auto-increment primary keys are mandatory.
6. Diagrams must be in Mermaid and placed under folder 26.

---

## 12. High-Impact Conflicts vs Existing Folder-21 Spec (preview, not yet applied)

These will be resolved in favor of this brief once execution begins:

| # | Existing folder-21 decision | This brief mandates |
|---|------------------------------|---------------------|
| C1 | PostgreSQL-style schema, UUID/`VARCHAR(36)` primary keys | SQLite + `INTEGER AUTOINCREMENT` PKs named `{TableName}Id` |
| C2 | RS256 JWT with rotating refresh tokens as primary auth | WP-application-password equivalent for writes; CI/CD uses `TempToken` + URL/branch validation; JWT only if it genuinely helps |
| C3 | Per-repo `logSenderToken` (HMAC) on `POST /logs/push` | Endpoint set is the 10 routes in §5.2; `TempToken` is the CI/CD secret, not HMAC envelope JWT |
| C4 | Endpoint base path `/wp-json/git-logs/v1/logs/push`, `/logs/...` | Endpoints are `/append-log`, `/fixed-log`, `/clear-log`, `/clear-log-all`, `/get-logs`, `/get-pipeline-logs`, `/get-error-logs`, `/get-pipeline-error-logs` (+ `?q=` variants) |
| C5 | Role enum: `Admin`, `CanAddRepo`, `CanAddUser`, `CanViewLogs`, `CanPushLogs` | Roles: `Admin`, `Editor` only. Those are **Permissions**, not Roles. Move to a `Permission` table with `RolePermission` join |
| C6 | Acceptance modes: `RepoUrl`, `OwnerWildcard` + version mode `Exact`/`Wildcard` | Single `Acceptance` enum: `AcceptAllRepos`, `AcceptSelectedRepoOnly`, `AcceptSelectedRepoInAllVersions` |
| C7 | Plugin user table separate from `wp_users`, identified by `username` + token hash (Argon2id) | Plain values for now (encryption deferred). Profile fields: `UserName`, `Email`, `GeneratedKeyApi`, `Token`, `TempToken` |
| C8 | `Repository` single table | Split into `Repo` (master, no version) + `RepoVersion` (variants, FK to `Repo`); `History`/`Action` link to `RepoVersion` |
| C9 | Audit trail (`AuditTrail`) | Replaced/renamed by `History` (latest events) and `Action` (action records). Audit semantics may merge into these two |
| C10 | DB table prefix `{wp_prefix}gitlogs_`, lowercase | PascalCase table names per database conventions |

---

## 13. Continuation Marker

```
If you have any question or confusion, feel free to ask. If you are creating multiple tasks, especially larger ones, organize them so that when I say `next`, you continue with the remaining tasks. Do you understand? Always add this part at the end of the writing inside the code block. Do you understand? Can you please do that?
```

---

## 14. Locked Decisions (2026-04-25, follow-up Q&A)

| # | Decision | Value |
|---|----------|-------|
| L1 | Folder scope | New parallel folder `spec/22-git-logs-v2/`. Folder 21 untouched as legacy. |
| L2 | JWT | **Dropped entirely.** Writes use WP application-password equivalent. CI/CD uses `TempToken` + GitHub URL + branch validation only. RS256/JWKS/refresh-token machinery removed. |
| L3 | Audit model | Keep all three: `AuditTrail` (immutable system-wide), `History` (per-`RepoVersion` event view), `Action` (typed enum table referenced by both). |
| L4 | App linkage | Separate `AppLink` table: `AppLinkId`, `AppId` FK, `LinkTypeId` FK (enum: `GitProfile`, `Repo`), `TargetId` (polymorphic FK by `LinkTypeId`), `IsActive`, `CreatedAt`. Allows multi-link and (re)link history. |
| L5 | App auth | App inherits parent Profile's `GeneratedKeyApi`, `Token`, `TempToken`. App does not carry its own credentials. |
| L6 | App lifecycle | `AppStatus` enum: `Active`, `Disabled`, `Archived`. CI/CD pushes rejected for non-`Active` apps. |
| L7 | App identity (default proposal — pending user amend) | `AppId` PK, `AppName` (req), `AppSlug` (req, unique), `Description` (optional), `EnvironmentId` FK (enum: Dev/Staging/Prod), `ProfileId` FK, `AppStatusId` FK, `CreatedAt`, `UpdatedAt`. |

