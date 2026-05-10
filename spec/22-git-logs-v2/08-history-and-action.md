# History, PipelineAction, SystemEvent, and AuditTrail (v2)

**Version:** 3.0.0  
**Updated:** 2026-04-26

> **v3.8.0 rename:** `Action` → `PipelineAction` (and `ActionType` lookup → `PipelineActionType`). The old name implied "any action in the system" but the table only records pipeline-bound CI events. **`SystemEvent`** is the new home for non-pipeline business events.

Four distinct tables, four distinct purposes. None replaces the others.

---

## History — Domain timeline (per RepoVersion)

- Answers: "What happened to this **repo version** specifically?"
- Rendered in the **History** UI menu.
- Rich row: App, Branch, Pipeline, GitSha256, PipelineActionType, HasError snapshot, Summary.
- One row per CI/CD ingest event.

## PipelineAction — Enum-typed pipeline log

- Answers: "Tally / filter all `Append`/`Fixed`/`Clear`/`ClearAll` actions across the system."
- Rendered in the **Action** UI menu (label kept for UX continuity) with enum filters.
- Lighter columns (no Summary, no HasError snapshot).
- One row per CI/CD write action; useful for analytics and rate limits.
- Always bound to a `RepoVersion` (and usually a `Pipeline`).

## SystemEvent — Business state changes (NEW v3.8.0)

- Answers: "Show me the user-visible feed of meaningful changes that aren't a Git push."
- Examples: `ProfileCreated`, `ProfileDeleted`, `RoleAssigned`, `GitProfileAcceptanceChanged`, `BranchRestrictionChanged`, `AppCreated`, `AppStatusChanged`, `SshKeyRegistered`, `SshKeyRevoked`, `TempTokenRotated`.
- Rendered in a new **Activity** tab inside History UI (filter chip: "Git events / System events / All").
- `TargetType` + `TargetId` form a loose polymorphic pointer (no FK CHECK — survives target row deletion so audit history outlives the entity).

## AuditTrail — System forensics (HTTP layer)

- Answers: "Who hit which endpoint when, with what outcome and IP?"
- Not surfaced in normal UI menus; reserved for admin/audit screens.
- Captures **every** endpoint hit (read or write), Auth Success/Fail, migration runs, profile/role/repo CRUD HTTP calls.
- Difference vs `SystemEvent`: `AuditTrail` is *one row per HTTP request*; `SystemEvent` is *one row per business state change* (a single profile-create HTTP call writes both — `AuditTrail` row records the request, `SystemEvent` row records the *resulting state change*).

---

## Why four tables

| Concern | History | PipelineAction | SystemEvent | AuditTrail |
|---------|:-------:|:--------------:|:-----------:|:----------:|
| Domain-meaningful timeline (per RepoVersion) | ✅ | partial | no | no |
| Enum-typed pipeline counters | partial | ✅ | no | no |
| Business state-change feed (non-Git) | no | no | ✅ | no |
| Endpoint forensics (per HTTP request) | no | no | no | ✅ |
| Includes reads | no | no | no | ✅ |
| Includes auth attempts | no | no | partial | ✅ |
| Includes migrations | no | no | partial | ✅ |
| Survives target row deletion | yes | no | ✅ (loose polymorphic) | yes |

Merging would either bloat domain views (mixing pipeline noise into business-event feeds), lose forensic granularity (collapsing every HTTP hit into business-only state changes), or scope-creep `History` outside its per-RepoVersion guarantee.
