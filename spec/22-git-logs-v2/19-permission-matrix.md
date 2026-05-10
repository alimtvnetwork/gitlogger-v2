# Permission Matrix (v2)

**Version:** 2.3.0  
**Updated:** 2026-04-25

Cross-tab of every Permission × seeded Role × admin screen action. Source of truth: §09 seed data + §03 admin UI. Authorization checks always go through `RolePermission` — never role name.

---

## Role × Permission grid

Legend: ✅ granted, ❌ not granted.

| # | Permission | Admin | Editor | Why |
|---|------------|:-----:|:------:|-----|
| 1  | AppCreate         | ✅ | ❌ | Editor can use Apps but not provision them. |
| 2  | AppView           | ✅ | ✅ | Required to render Apps anywhere in UI. |
| 3  | AppModify         | ✅ | ✅ | Editors can flip status / change description. |
| 4  | AppDelete         | ✅ | ❌ | Destructive; Admin only. |
| 5  | ProfileCreate     | ✅ | ❌ | Plugin Profile = credential boundary. |
| 6  | ProfileView       | ✅ | ✅ | Needed to pick Profile when creating Apps. |
| 7  | ProfileModify     | ✅ | ❌ | Token regeneration is Admin-only. |
| 8  | ProfileDelete     | ✅ | ❌ | Lockout risk; Admin only. |
| 9  | GitProfileCreate  | ✅ | ❌ | Onboarding new GitHub orgs is governance. |
| 10 | GitProfileView    | ✅ | ✅ | Required for History filters. |
| 11 | GitProfileModify  | ✅ | ✅ | Editors can adjust Acceptance / Branch rules. |
| 12 | GitProfileDelete  | ✅ | ❌ | Cascades to Repos; Admin only. |
| 13 | RepoView          | ✅ | ✅ | Required to render History. |
| 14 | RepoModify        | ✅ | ✅ | Renaming / metadata edits OK. |
| 15 | RepoDelete        | ✅ | ❌ | Destroys all history; Admin only. |
| 16 | HistoryView       | ✅ | ✅ | Read-only timeline. |
| 17 | LogPush           | ✅ | ❌ | Not enforced via role; CI/CD path uses TempToken+URL+Branch. Listed for completeness; no UI grant. |

Re-check: Admin row count = 17 (matches §09 seed `INSERT … SELECT 1, PermissionId FROM Permission`). Editor row count = 8 (matches §09 explicit list).

---

## Screen × required Permission

| Admin screen | View action | Mutate action(s) |
|--------------|-------------|------------------|
| Profile (list) | `ProfileView` | `ProfileCreate`, `ProfileModify`, `ProfileDelete` |
| Roles (list) | always (system) | system-only (Admin) |
| AccessToRoles (matrix) | `ProfileView` | system-only (Admin) — flipping rows mutates `RolePermission` |
| GitProfile | `GitProfileView` | `GitProfileCreate`, `GitProfileModify`, `GitProfileDelete` |
| Repo (list) | `RepoView` | `RepoModify`, `RepoDelete` |
| RepoVersion (list) | `RepoView` | `RepoModify`, `RepoDelete` |
| History (timeline) | `HistoryView` | none (read-only) |
| Action (raw enum log) | `HistoryView` | none (read-only) |
| App (list/edit) | `AppView` | `AppCreate`, `AppModify`, `AppDelete` |

Buttons that require a missing Permission must be **hidden, not disabled**, to keep the UI honest about what the current user can do.

---

## CI/CD endpoint × authorization rule

| Endpoint | Permission check | Identity check |
|----------|-----------------|----------------|
| `/append-log`, `/fixed-log`, `/clear-log`, `/clear-log-all` | none (no role gate) | `TempToken` + `Token` resolve to a Profile, Profile.UserStatus=Active, GitProfile Acceptance + Branch + App lifecycle |
| `/get-logs`, `/get-pipeline-logs`, `/get-error-logs`, `/get-pipeline-error-logs` | `HistoryView` | WP App Password / cookie → Profile |

CI/CD writes are intentionally **not** role-gated. The credential boundary IS the Profile + URL/branch/Acceptance triplet.

---

## Adding a new Permission

1. Append a row to `Permission` lookup in `09-seed-data.md` AND `18-schema.sql`.
2. Add it to this grid with explicit Admin/Editor allocation.
3. Add a `case` in `inc/Domain/Auth/PermissionGate.php` and a constant in `inc/Support/Capabilities.php`.
4. Add an integration test asserting both granted and denied paths.
5. Bump `98-changelog.md`.
