# Admin UI (v2)

**Version:** 2.3.0  
**Updated:** 2026-04-28 (Phase P18 — added `## State-Transition Label Rendering` section binding the History `HasError` column rendering to AC-73's four-value label enum (`still-green` / `first-failure` / `still-failing` / `just-recovered`); History columns table revised to call out the derived state label adjacent to the raw `HasError` boolean. Closes the §99 v3.9.6+ open follow-up "(a) §03 admin UI rendering of state labels — consumer-side". Pure consumer-side contract; no DDL, no schema bump, no enum change.)

---

## Top-Level Menu (in order)

1. **Profile** — list, create, edit plugin Profiles. Fields: `UserName`, `Email`, `GeneratedKeyApi` (read-only after generation, regenerate button), `Token` (regenerate), `TempToken` (regenerate; shown). No password field.
2. **Roles** — list, create, edit Roles. Default seeded: `Admin`, `Editor`.
3. **AccessToRoles** — assign Permissions to Roles via `RolePermission`. UI = matrix of Roles × Permissions checkboxes. Admin row is locked-on for all permissions.
4. **GitProfile** — list, add, edit GitProfiles.
5. **Repo** — list of master Repos. Click → opens History for that Repo.
6. **RepoVersion** — list of RepoVersion variants per Repo, with link to History filtered by version.
7. **History** — per-RepoVersion timeline (App, Branch, Pipeline, PipelineActionType, HasError, OccurredAt). Includes an **Activity** tab (filter chip: *Git events / System events / All*) backed by `SystemEvent` for non-Git business changes (ProfileCreated, RoleAssigned, AppCreated, SshKeyRevoked, GitProfileAcceptanceChanged, …). **v3.8.0**: column relabel `ActionType` → `PipelineActionType`.
8. **Action** — enum-typed pipeline-action log (label kept for UX continuity; backed by `PipelineAction` table renamed in v3.8.0). Filters: PipelineActionType, RepoVersion, Pipeline, Profile, date range.

> Items marked `format:hide` in the mind-map (notes under GitProfile, etc.) are not rendered in UI.

---

## GitProfile — Add/Edit Form

| Field | Control | Notes |
|-------|---------|-------|
| Profile URL | text input | User or Org URL; trailing slash optional; canonicalized on save (with trailing slash). Canonical form depends on **Is organization** below: `github.com/$org/$repo` when checked, else `github.com/$username/$repo`. |
| Provider | select (read-only `GitHub` in v2) | |
| Is organization | checkbox (default off) | **v3.8.0** — replaces derived `OwnerType`. When checked, the Profile URL is treated as an organization URL and canonicalized as `github.com/$org/$repo`; when unchecked, treated as a user URL (`github.com/$username/$repo`). Persisted as `GitProfile.IsOrganization` (0/1). |
| Acceptance | select | `AcceptAllRepos`, `AcceptSelectedRepoOnly`, `AcceptSelectedRepoInAllVersions` |
| Selected Repo URL | text input | Visible iff Acceptance ≠ `AcceptAllRepos` |
| IsRestrictInBranch | checkbox (default off) | |
| StrictBranch | text input | Visible iff `IsRestrictInBranch` is on |

Validation: server normalizes URL, parses owner/repo, derives `RootRepoName` for selected variants.

---

## Profile — Add/Edit Form

| Field | Control |
|-------|---------|
| UserName | text |
| Email | email |
| GeneratedKeyApi | read-only + Regenerate button |
| Token | read-only + Regenerate button |
| TempToken | read-only + Regenerate button |
| UserStatus | select (Active/Suspended/Revoked) |
| Roles | multi-select (RoleAssignment) |

---

## Roles + AccessToRoles

- **Roles screen**: CRUD on Role table.
- **AccessToRoles screen**: matrix `Role × Permission` writing to `RolePermission`.
- Authorization layer always queries `RolePermission` (never the role name).

---

## Repo / RepoVersion / History / Action

- **Repo list** → click row → **History** view filtered to that Repo's RepoVersions.
- **RepoVersion list** → click row → **History** filtered to one variant.
- **History** columns: OccurredAt, App, Branch, Pipeline, PipelineActionType, **HasError + StateLabel**, Summary. **v3.8.0**: column relabel from `ActionType` → `PipelineActionType`. **v2.3.0 (Phase P18)**: the `HasError` column now renders BOTH the raw boolean (icon: ✅ when `HasError=0`, ❌ when `HasError=1`) AND the derived AC-73 state-transition label as a chip immediately to the right (`still-green`, `first-failure`, `still-failing`, `just-recovered`). See `## State-Transition Label Rendering` below for the binding contract.
- **History → Activity tab**: SystemEvent feed (Actor, EventType, Target, Summary, OccurredAt). Filter chip toggles between *Git events* (History rows), *System events* (SystemEvent rows), or *All* (interleaved by `OccurredAt`).
- **Action** view: raw `PipelineAction` enum log with filters (PipelineActionType, RepoVersion, Pipeline, Profile, date range). **v3.8.0**: backing table renamed `Action` → `PipelineAction`; UI label retained.

---

## State-Transition Label Rendering (v2.3.0 — Phase P18)

The History view (and any other admin screen that surfaces a `Pipeline` row, e.g. RepoVersion drill-down, Activity *All* tab) MUST render the AC-73 derived state-transition label adjacent to the raw `HasError` boolean. This is the consumer-side counterpart of §04 §11.3 + AC-74's NDJSON `Header.StateTransition` field — both consumers compute the label from the same `(PreviousHasError, HasError)` tuple per AC-73's pure-function rule, so the admin UI label and the streaming `Header.StateTransition` field MUST always agree for the same row at the same instant.

**Label derivation** (verbatim from AC-73, repeated here so admin-UI implementers do not need to flip files):

| `PreviousHasError` | `HasError` | Label | Chip color (suggested) |
|---|---|---|---|
| 0 | 0 | `still-green` | green |
| 0 | 1 | `first-failure` | red (with new-failure emphasis — bold border) |
| 1 | 1 | `still-failing` | red (muted — desaturated) |
| 1 | 0 | `just-recovered` | green (with recovery emphasis — animated pulse on first paint) |

**Rendering rules:**

1. **Single source of truth.** The label MUST be derived from the row's `(PreviousHasError, HasError)` columns at render time — NEVER cached, NEVER recomputed from a separate query, NEVER stored as a denormalized `StateLabelCache` column. AC-75's single-statement write atomicity guarantees the tuple is consistent at read time.
2. **Exhaustive enum.** Renderers MUST handle all four labels. There is no `unknown` / `initial` / `n/a` fallback — by AC-75's back-fill rule every shipped row has a valid `(PreviousHasError, HasError)` tuple. If a renderer encounters a tuple outside `{(0,0), (0,1), (1,1), (1,0)}` it MUST raise an internal error (DB constraint violation per §18 `CHECK (PreviousHasError IN (0,1)) + CHECK (HasError IN (0,1))`) and surface it via §15 `GL-INTERNAL` rather than rendering a fifth label.
3. **No translation of label keys.** The four label strings are stable wire identifiers (matching the OpenAPI `NdjsonHeaderFrame.StateTransition` enum per §17 v2.9.3+). Localization MAY translate the *display chip text* (e.g. `"still-green"` → "Stable" in EN, "Estable" in ES) but MUST keep the `data-state-label="<key>"` HTML attribute set to the canonical English key for CSS / e2e selector stability.
4. **Color-blind safety.** Color alone MUST NOT carry meaning — every chip MUST also include a glyph (✅ / 🔴 / ⚠️ / 💚) or the literal label text so users without color perception can distinguish `still-green` from `just-recovered` (both green) and `first-failure` from `still-failing` (both red).
5. **Sort + filter.** History column-header click on the `HasError + StateLabel` column MUST offer a 4-way sort by label (alphabetical: `first-failure` → `just-recovered` → `still-failing` → `still-green`) AND a filter dropdown listing all four labels as multi-select chips. The filter MUST default to "all four selected" (no implicit hiding of `still-failing` rows).
6. **Consistency with NDJSON consumer.** Operators occasionally cross-check the admin UI against a `curl -H "Accept: application/x-ndjson"` stream of the same pipeline. The label rendered in History column N MUST equal the `Header.StateTransition` value emitted on the streaming endpoint for the same `PipelineId` at the same instant. If they ever diverge, the divergence is a bug — file under §15 `GL-INTERNAL`.

Cross-refs: AC-73 (label enum + pure-function rule), AC-74 (NDJSON `Header.StateTransition` consumer), AC-75 (back-fill + single-statement-write atomicity), §17 `components.schemas.NdjsonHeaderFrame.StateTransition` (wire enum), §01 glossary v3.8.10 `PreviousHasError` row.
