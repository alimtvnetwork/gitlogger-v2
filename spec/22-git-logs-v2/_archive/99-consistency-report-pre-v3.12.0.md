# Consistency Report (v2) — Archive (audit blocks pre-v3.12.0)

**Frozen.** Extracted from `99-consistency-report.md` at Phase 153 Task A24-fu39 to free AI-implementability walker bundle headroom (Lesson #65 / fu28-fu29 pattern). Historical reference only — never edited.

**Source:** `spec/22-git-logs-v2/99-consistency-report.md` lines 83–390 at file v3.12.0.
**Coverage:** v2.8.7 Audit through Phase P7b (v3.9.14 Audit), 19 audit blocks.
**Excluded from all gates:** `_archive/` is invisible to `check-version-parity.py`, `check-lockstep.cjs`, `check-tree-health.cjs` (ARCHIVE_PREFIX), and `audit-ai-implementability.py` walker.

---

## v2.8.7 Audit — §18 seeds vs §15 codes

Cross-checked all `18-schema.sql` lookup seeds against `15-error-codes.md` runtime codes. Result: **full coverage, zero unmapped codes**.

| Seed table | Rows | Maps to §15 codes | Status |
|------------|-----:|-------------------|--------|
| `UserStatus` | 3 | `GL-AUTH-PROFILE-SUSPENDED`, `GL-AUTH-PROFILE-INACTIVE` | ✅ |
| `AppStatus` | 3 | `GL-APP-NOT-ACTIVE` | ✅ |
| `Permission` | 17 | `GL-AUTHZ-PERMISSION-DENIED` (every screen) | ✅ |
| `AuditActionType` | 25 | All reject paths via `LogPush`/`LogQuery`/`AuthFail` | ✅ |
| `Acceptance` | 3 | `GL-VALIDATION-REPO-NOT-ALLOWED` | ✅ |
| `AppLinkType` | 2 | (linkage resolution, no direct code) | ✅ |
| `Provider` | 2 | `GL-VALIDATION-REPOURL-MALFORMED` parser | ✅ |
| ~~`OwnerType`~~ | 0 | (retired v3.8.1 — replaced by `GitProfile.IsOrganization` boolean; tombstoned in §16) | 🗑️ |
| `LogSeverity` | 6 | (per-line truncation, no GL code per §15 note) | ✅ |
| `PipelineActionType` | 4 | (Append/Fixed/Clear/ClearAll dispatch — renamed from `ActionType` in v3.8.2) | ✅ |
| `SystemEventType` | 16 | (NEW v3.8.2 — feeds `SystemEvent` business-event feed; no GL code, internal) | ✅ |
| `AuditOutcome` | 3 | (envelope outcome) | ✅ |
| `ConfigKv` | 10 defaults | `GL-CONFIG-MISSING`, `GL-RATE-LIMIT-EXCEEDED`, `GL-PAYLOAD-TOO-LARGE`, `GL-LINES-TOO-MANY`, `GL-SSH-TIMESTAMP-SKEW` | ✅ |
| `MigrationState` | 6 markers (2.0.0/2.5.0/2.6.0/2.7.0/2.8.0/2.8.7) | `GL-MIGRATION-PENDING` | ✅ |

**Repairs applied this cycle:**
- `18-schema.sql` header: `16-seed-data.md` → `37-seed-data.md` (slot moved in v2.8.6).
- `18-schema.sql` seeds-comment: same fix.
- `18-schema.sql` banner: `v2.7.0` → `v2.8.7`.
- `15-error-codes.md` banner: `v2.7.0` → `v2.8.7`.
- `ConfigKv.PluginVersion` seed: `'2.7.0'` → `'2.8.7'`.
- `MigrationState`: appended `2.8.0` (doc-only) and `2.8.7` (this audit) markers.

## v3.8.0 Audit — Domain-model overhaul (user diagram review)

User reviewed `26-gitlogs-diagrams/02-domain-design.mmd` + `01-er-diagram.mmd` and raised four concerns:

| # | Concern | Resolution |
|---|---------|------------|
| 1 | "Why is `RepoVersionId` inside `Action`? Naming is the issue." | Renamed `Action` → `PipelineAction` + `ActionType` → `PipelineActionType`. Documented scope (RepoVersion + Pipeline only) in §08. |
| 2 | "History should also cover non-Git events (ProfileCreated, KeyRevoked, …)" | Introduced `SystemEvent` table with 16-value `SystemEventType` lookup; loose polymorphic (`TargetType` + `TargetId`, no FK CHECK). Four-table model documented in §08. |
| 3 | "Where are logs streamed? Use the split-DB pattern, per-SHA SQLite." | Created §39. `LogEntry`/`ErrorLogEntry` deleted from root DB; root DB keeps only `ShaRegistry` (registry + rolled-up summary). Per-SHA file at `logs/<RepoVersionId>/<GitSha256>.sqlite` with semantic tables (`PipelineRun`, `StatusSnapshot`) that answer last-status / failure-count / pipelines-failing in O(1). |
| 4 | "`GitProfile` doesn't mark organization vs user — needs `IsOrganization` checkbox." | Added `IsOrganization INTEGER 0/1` column on `GitProfile`; retired `OwnerType` lookup. Drives URL canonicalization + admin-UI checkbox. **§18 DDL + §03 UI + §16 seed tombstone landed v3.8.1.** |

Files touched in this cycle: `00-overview.md` (+§39 row), `01-glossary-and-enums.md` (OwnerType retired, PipelineActionType renamed, SystemEventType added, ShaRegistry+SystemEvent+PipelineAction terms), `02-database-schema.md` (GitProfile.IsOrganization, lookup list updated, LogEntry+ErrorLogEntry removed, ShaRegistry added, History rename, PipelineAction rename, SystemEvent added), `08-history-and-action.md` (4-table model), `97-acceptance-criteria.md` (AC-07 + AC-21 reworded, AC-49–AC-53 added), `98-changelog.md`, `99-consistency-report.md`, `26-gitlogs-diagrams/01-er-diagram.mmd` (regenerated with split boundary), `26-gitlogs-diagrams/02-domain-design.mmd` (regenerated with subgraphs).

**Queued (NOT in this commit, tracked in `mem://specs/git-logs.md` queued decisions):**
- §18 `18-schema.sql`: ~~drop `OwnerType` table+seed~~ ✅ landed v3.8.1; ~~add `GitProfile.IsOrganization`~~ ✅ landed v3.8.1; ~~rename `Action`→`PipelineAction` + `ActionType`→`PipelineActionType`~~ ✅ landed v3.8.2; ~~add `SystemEvent`+`SystemEventType` tables + 16 seeds~~ ✅ landed v3.8.2; ~~drop `LogEntry`+`ErrorLogEntry`, add `ShaRegistry` table, add `MaxOpenShaDbHandles`/`ShaDbIdleCloseSec`/`ShaLogsRoot` `ConfigKv` defaults~~ ✅ landed v3.8.3 (Phase 2); add 4 `GL-SHA-DB-*` codes to §15 (queued for Phase 3).
- §22 retention: prune walks `ShaRegistry` + deletes per-SHA files.
- §23 backup: manifest must list per-SHA file inventory + per-file row counts + sha256.
- §29 uninstall: Wipe mode deletes the `logs/` folder.
- ~~§03 admin-ui: add "Is organization" checkbox to GitProfile create/edit screen.~~ ✅ landed v3.8.1.
- §15 error-codes: add `GL-SHA-DB-CREATE-FAILED`, `GL-SHA-DB-OPEN-FAILED`, `GL-SHA-DB-CORRUPT`, `GL-SHA-DB-NOT-FOUND`.
- Per-SHA SVG re-render of `01-er-diagram.mmd` + `02-domain-design.mmd`.
- `26-gitlogs-diagrams/00-overview.md` banner bump v1.1.0 → v1.2.0 + inventory note for the new split-DB callouts.

## v3.8.1 Audit — Q1 IsOrganization lockstep

| File | Change |
|------|--------|
| `03-admin-ui.md` | Removed `OwnerType (derived)` row; added `Is organization` checkbox row bound to `GitProfile.IsOrganization`. Banner v2.0.0 → v2.1.0. |
| `16-seed-data.md` | `OwnerType` section converted to retirement tombstone (no seed rows). Banner v2.7.0 → v2.7.1. |
| `18-schema.sql` | `CREATE TABLE OwnerType` deleted; `GitProfile.OwnerTypeId` → `IsOrganization INTEGER NOT NULL DEFAULT 0 CHECK (IsOrganization IN (0,1))`; `OwnerType` seed deleted; `ConfigKv.PluginVersion` 2.8.7 → 2.8.8; banner v2.8.7 → v2.8.8. |
| `97-acceptance-criteria.md` | Added AC-54 (UI checkbox binding) + AC-55 (DDL constraint). Banner v3.8.0 → v3.8.1. |
| `98-changelog.md` | Added v3.8.1 row. |
| `99-consistency-report.md` | Tombstoned `OwnerType` seed-coverage row; flipped Q1 status in v3.8.0 audit table; this audit table added. Banner v3.8.0 → v3.8.1. |

## v3.8.2 Audit — Q2 PipelineAction rename + SystemEvent lockstep

| File | Change |
|------|--------|
| `18-schema.sql` | `CREATE TABLE ActionType` → `PipelineActionType`; `CREATE TABLE Action` → `PipelineAction` (PK rename, FK rename, added `RepoVersionId NOT NULL` + `ProfileId` FK + 2 indexes); `History.ActionTypeId` → `PipelineActionTypeId`; **NEW** `CREATE TABLE SystemEventType` lookup; **NEW** `CREATE TABLE SystemEvent` with loose-polymorphic Target + 3 indexes; `INSERT INTO ActionType` → `INSERT INTO PipelineActionType` (4 rows); **NEW** `INSERT INTO SystemEventType` (16 rows); `ConfigKv.PluginVersion` 2.8.8 → 2.8.9; `MigrationState` markers 2.8.8 + 2.8.9 appended; banner v2.8.8 → v2.8.9. |
| `03-admin-ui.md` | History menu item gains "Activity tab" note for SystemEvent; Action menu item reworded (UI label retained, backing table renamed); History columns relabel `ActionType` → `PipelineActionType`. Banner v2.1.0 → v2.2.0. |
| `01-glossary-and-enums.md` | Banner v3.8.0 → v3.8.1 (entries already correct from v3.8.0 doc-only pass). |
| `97-acceptance-criteria.md` | Added AC-56 (no `Action`/`ActionType` tables), AC-57 (`SystemEvent` columns + indexes), AC-58 (16 `SystemEventType` seeds in canonical order), AC-59 (Activity tab + Action menu wording). Banner v3.8.1 → v3.8.2. |
| `98-changelog.md` | Added v3.8.2 row. |
| `99-consistency-report.md` | Flipped Q2 status in v3.8.0 audit table; this audit table added; seed-coverage table updated for new lookup counts. Banner v3.8.1 → v3.8.2. |

**SQLite validation (in-memory `executescript` of `18-schema.sql`):**
- `PipelineActionType` = 4 rows (Append/Fixed/Clear/ClearAll) ✅
- `SystemEventType` = 16 rows ✅
- `AuditActionType` = 25 rows (unchanged) ✅
- `Permission` = 17, `LogSeverity` = 6, `Acceptance` = 3, `AppStatus` = 3, `AppLinkType` = 2, `UserStatus` = 3, `Provider` = 2 ✅
- `ConfigKv` = 10 defaults (`PluginVersion='2.8.9'`) ✅
- `MigrationState` = 8 markers (2.0.0/2.5.0/2.6.0/2.7.0/2.8.0/2.8.7/2.8.8/2.8.9) ✅
- Legacy tables `Action`/`ActionType`/`OwnerType` confirmed **absent**. ✅
- New tables `PipelineAction`/`PipelineActionType`/`SystemEvent`/`SystemEventType` confirmed **present**. ✅

## v3.8.3 Audit — Phase 2 Q3 Split-DB schema surgery (root DB)

| File | Change |
|------|--------|
| `18-schema.sql` | **DROP** `CREATE TABLE LogEntry` + `IxLogEntryPipeline`; **DROP** `CREATE TABLE ErrorLogEntry` + `IxErrorLogEntryPipeline` (replaced with retirement comment block referencing §39). **ADD** `CREATE TABLE ShaRegistry` (PK `ShaRegistryId`, cols `PipelineId FK`, `Sha`, `DbFilePath`, `RowCount`, `FirstSeenAt`, `LastSeenAt`, `FileSizeBytes`, `Sha256 NULL`, `UNIQUE(PipelineId, Sha)`) + indexes `IxShaRegistrySha`/`IxShaRegistryLastSeen`. **ADD** 3 `ConfigKv` defaults (`ShaLogsRoot='logs'`, `MaxOpenShaDbHandles='32'`, `ShaDbIdleCloseSec='120'`). `ConfigKv.PluginVersion` 2.8.9 → 2.9.0; `MigrationState` marker 2.9.0 appended; banner v2.8.9 → v2.9.0. |
| `02-database-schema.md` | Banner 3.8.0 → 3.8.3. Engine line clarified: root DDL no longer ships `LogEntry`/`ErrorLogEntry`; ships `ShaRegistry` + 3 new ConfigKv keys. `ConfigKv` section gained a v3.8.3 sub-table with new keys + defaults + purpose. |
| `01-glossary-and-enums.md` | Banner 3.8.1 → 3.8.3. `ShaRegistry` definition refined ("One row per (PipelineId, Sha)"). NEW glossary rows: `PerShaDb` (per-SHA SQLite file + path layout) + `ShaLogsRoot` (ConfigKv key + sharded folder tree). |
| `98-changelog.md` | Added v3.8.3 row. |
| `99-consistency-report.md` | This audit table added; v3.8.0 audit table flipped (`LogEntry`/`ErrorLogEntry` drop + `ShaRegistry` + 3 ConfigKv defaults marked landed in v3.8.3); banner 3.8.2 → 3.8.3. |

**Phase 2 scope discipline:** §15 error codes (`GL-SHA-DB-*`), §22 prune walk, §23 backup manifest, §29 wipe, §97 ACs (AC-49..AC-53 promotion), §00 inventory row, Mermaid re-render, root `spec-index.md` bump are **deferred to Phases 3–4** per `mem://specs/phased-roadmap.md`.

## v3.8.4 Audit — Phase 3 Split-DB error codes & cross-section updates

| File | Change |
|------|--------|
| `15-error-codes.md` | Added new section *Per-SHA log storage (split-DB — see §39)* with 4 codes: `GL-SHA-DB-OPEN-FAILED` (503), `GL-SHA-DB-CREATE-FAILED` (500), `GL-SHA-DB-CHECKSUM-MISMATCH` (500), `GL-SHA-DB-QUOTA-EXCEEDED` (507). Banner v2.8.7 → v2.9.0. |
| `22-retention-and-pruning.md` | Rewrite: row-level `DELETE FROM LogEntry`/`ErrorLogEntry` removed; eligibility now `ShaRegistry.LastSeenAt` + `Pipeline.HasError` + history-window guard; rename → delete-row → unlink crash-safety with `*.pruning` recovery; new exit code 4 for FS errors; empty-shard `<aa>/` cleanup; audit JSON keys updated. Banner v2.5.0 → v2.9.0. |
| `23-backup-restore.md` | Backup is now a directory tree (`git-logs.sqlite` + `manifest.json` + `logs/<aa>/<sha>.db…`); each per-SHA file copied via Online Backup API + integrity_check + sha256. Manifest gains `ShaFiles[]` + `ShaFileTotal`. Restore is all-or-nothing with `.bak` rollback. New `--skip-sha-checksum` flag. New cross-version row pre-v2.9.0 → v2.9.0+. `verify` walks `ShaRegistry`. Banner v2.5.0 → v2.9.0. |
| `29-uninstall-policy.md` | Lifecycle table gained "Per-SHA tree" column. `Preserve` retains tree + records `ShaFileCount`; `Archive` renames tree to `<ShaLogsRoot>.archive-<unix>/`; `Wipe` deletes tree first then root, then `rmdir` parent. Banner v2.5.0 → v2.9.0. |
| `98-changelog.md` | Added v3.8.4 row. |
| `99-consistency-report.md` | This audit table added; Phase-3 deferred-list line in v3.8.3 audit superseded by Phase-4-only deferral note in Health Score; banner v3.8.3 → v3.8.4. |

**Phase 3 scope discipline:** §00 inventory row for §39, §97 ACs (AC-49..AC-53 promotion to active), Mermaid re-render, root `spec-index.md` bump are **deferred to Phase 4** per `mem://specs/phased-roadmap.md`. Phases 5–10 untouched.

## v3.8.5 Audit — Phase 4 Split-DB doc closure

| File | Change |
|------|--------|
| `00-overview.md` | §39 inventory row rewritten — old "NEW v3.8.0; logs/<RepoVersionId>/<GitSha256>.sqlite" replaced with v2.9.0-active wording (path `<dataDir>/<ShaLogsRoot>/<Sha[0:2]>/<Sha>.db`, ConfigKv keys, cross-refs to §15/§22/§23/§29). Banner v3.8.0 → v3.8.5. |
| `97-acceptance-criteria.md` | AC-49..AC-53 promoted from draft to **Active (v2.9.0)**; rewritten to match shipped DDL/runtime (key on `(PipelineId, Sha)`, `RowCount`/`LastSeenAt`/`FileSizeBytes`/`Sha256` mirrors, defaults `MaxOpenShaDbHandles=32` / `ShaDbIdleCloseSec=120`, `GL-SHA-DB-QUOTA-EXCEEDED` 507, prune crash-safety, manifest `ShaFiles[]`, Wipe per-SHA-tree-first). Banner v3.8.2 → v3.8.5. |
| `spec/spec-index.md` | Refreshed 9 version cells (00→3.8.5, 01→3.8.3, 02→3.8.3, 15→2.9.0, 22→2.9.0, 23→2.9.0, 29→2.9.0, 97→3.8.5, 99→3.8.5). |
| `26-gitlogs-diagrams/01-er-diagram.mmd` | Top annotation declares root-DB scope + split-DB boundary; stale `RepoVersion → ShaRegistry seenShas` and `LogSeverity → ShaRegistry lastSeverity` edges removed; `Pipeline → ShaRegistry lastSha` collapsed to canonical `sha` edge; `ShaRegistry` entity block rewritten to v2.9.0 §18 DDL columns (`PipelineId`, `Sha`, `DbFilePath`, `RowCount`, `FirstSeenAt`, `LastSeenAt`, `FileSizeBytes`, `Sha256`). |
| `98-changelog.md` | v3.8.5 row added. |
| `99-consistency-report.md` | This audit table added; banner v3.8.4 → v3.8.5. |

**Phase 4 scope discipline:** Phases 5–10 untouched. Phase B1 (§07 App identity fields) remains blocked on user decision.

## v3.8.6 Audit — Phase 5 SSH-Key Lane B schema & errors

| File | Change |
|------|--------|
| `18-schema.sql` | Added `CREATE TABLE SshKey` (11 cols: `SshKeyId PK AI`, `Fingerprint UNIQUE`, `RepoId FK ON DELETE CASCADE`, `KeyType`, `PublicKey`, `Label`, `OwnedByProfileId FK`, `IsActive CHECK 0/1 DEFAULT 1`, `LastUsedAt`, `CreatedAt`, `RevokedAt`) + 2 indexes (`IxSshKeyRepoActive`, `IxSshKeyOwner`); added `CREATE TABLE SshNonce` (`SshNonceId PK`, `SshKeyId FK ON DELETE CASCADE`, `Nonce`, `SeenAt`, `UNIQUE(SshKeyId, Nonce)`) + 1 index. Added 2 ConfigKv defaults (`SshAuthMode='optional'`, `SshNonceJanitorBatch='100'`). Bumped `PluginVersion` 2.9.0 → 2.9.1; appended `MigrationState` 2.9.1. Banner v2.9.0 → v2.9.1. |
| `01-glossary-and-enums.md` | 3 new entries: `SshKey` (deploy-key model + full column list + Lane B authoritative semantics), `Ed25519Signature` (OpenSSH PEM signature over `GL-SSHSIG-V1` canonical string, namespace `git-logs@v2`, `-H sha512`), `SshNonce` (replay-defense semantics, prune cadence). Banner v3.8.3 → v3.8.6. |
| `02-database-schema.md` | Banner v3.8.3 → v3.8.6 (existing SshKey/SshNonce sub-sections from earlier §31 doc work now backed by canonical §18 DDL). |
| `15-error-codes.md` | Banner v2.9.0 → v2.9.1 — confirms 9 SSH lane codes (`GL-SSH-HEADER-MISSING`, `-TIMESTAMP-SKEW`, `-KEY-UNKNOWN`, `-KEY-INACTIVE`, `-REPO-MISMATCH`, `-NONCE-REUSED`, `-SIGNATURE-INVALID`, `-LANE-CONFLICT`, plus `GL-AUTH-LANE-DISABLED`) are backed by canonical schema. |
| `31-ssh-key-auth.md` | Banner v2.7.0 → v2.9.1 — canonical-DDL note added. |
| `98-changelog.md` | v3.8.6 row added. |
| `99-consistency-report.md` | This audit table added; banner v3.8.5 → v3.8.6. |

**In-memory SQLite validation:** 31 tables (was 29 in v2.9.0); `SshKey` + `SshNonce` present; `LogEntry`/`ErrorLogEntry` still absent; 15 ConfigKv keys (was 13); `PluginVersion=2.9.1`; 10 MigrationState markers; 3 SshKey* AuditActionType seeds (`SshKeyRegister`/`SshKeyRevoke`/`SshKeyRotate`).

**Phase 5 scope discipline:** §05 SSH lane block insertion, §28 GH-Actions SSH-signed example, §30 STRIDE entries are **deferred to Phase 6**. AC additions for SshKey/SshNonce deferred to Phase 7 (AC GWT pass). Phases 7–10 untouched. Phase B1 still blocked on user.

## v3.8.7 Audit — Phase 6 SSH-Key Lane B flow & threat doc

| File | Change |
|------|--------|
| `05-auth-and-validation.md` | Banner v2.1.0 → v2.9.1. SSH lane block (10-step validation order) confirmed authoritative; cross-refs to §31 (signing string), §15 (9 SSH error codes), §18 v2.9.1 (canonical SshKey/SshNonce DDL) verified. Coexistence rules (`X-GL-Auth-Mode` parse, `SshAuthMode` gate, `GL-SSH-LANE-CONFLICT`, `GL-AUTH-LANE-DISABLED`) preserved. |
| `28-example-github-actions.md` | Banner v2.7.0 → v2.9.1. Drop-in `git-logs-ssh.yml` workflow confirmed authoritative — namespace `git-logs@v2`, four required headers, canonical signing string `GL-SSHSIG-V1\nMETHOD\nPATH\nTIMESTAMP\nNONCE\nsha256(body)`, deploy-key rotation, `~/.ssh-gitlogs` cleanup with `if: always()`. SSH-mode gotchas table covers all 7 SSH error codes + `GL-AUTH-LANE-DISABLED`. Legacy TempToken workflow retained as deprecation reference. |
| `30-threat-model.md` | Banner v2.7.0 → v2.9.1. Added 4 STRIDE Spoofing rows that the v2.7.0 summary already promised but never wrote: **S5 Signature replay** (`SshReplayWindowSec` skew, per-key `(SshKeyId, Nonce)` uniqueness, `SshNonceJanitorBatch` table-bound); **S6 Private-key theft from CI runner** (deploy-key one-Repo blast radius, immediate `IsActive=0` rotation, `LastUsedAt` anomaly surface, GH-Actions key-wipe, per-Profile rate cap); **S7 Signature stripping / lane downgrade** (mandatory HTTPS, `SshAuthMode=required` hard reject, `GL-SSH-LANE-CONFLICT` mixed-lane block, header-completeness ordered before signature check); **S8 Lane-mode forgery** (`ConfigKv.SshAuthMode` direct DB edit covered by T1, `AuditTrail.ConfigKvUpdate` for in-band changes). Closes the "S5–S8 SSH-lane additions" forward reference in §30 summary. |
| `98-changelog.md` | v3.8.7 row added. |
| `99-consistency-report.md` | This audit table added; banner v3.8.6 → v3.8.7. |

**Phase 6 scope discipline:** AC additions for SshKey/SshNonce/replay/lane-downgrade are **deferred to Phase 7** (AC GWT pass). §15/§18/§31 untouched (already at v2.9.1 from Phase 5). Phases 7–10 untouched. Phase B1 still blocked on user.

## v3.8.8 Audit — Phase 7 AC Quality Pass

| File | Change |
|------|--------|
| `97-acceptance-criteria.md` | **Full rewrite.** Banner v3.8.5 → v3.8.8. Every AC (AC-01..AC-59) converted from one-line table rows into full **Given / When / Then** stanzas with explicit `Verifies:` cross-refs to source sections. Status badges `[active]`/`[draft]`/`[deprecated]` introduced; all current ACs land at `[active]` for v2.9.1. Reorganized into 9 thematic sections (A UI · B Domain · C Auth/Lane · D Endpoints · E Logging/Migrations · F Audit · G Schema/Diagrams · H Per-SHA Split-DB · I SSH-Key Lane B). **7 new ACs added** (AC-60..AC-66) — all in Section I, all `[active]` — covering: SshKey registration shape + audit hooks (AC-60); SshNonce replay defense via skew + per-key uniqueness + janitor (AC-61); lane gating via `SshAuthMode` + mixed-lane conflict (AC-62); signature stripping defense via header-completeness ordering + mandatory HTTPS (AC-63); SshKey rotation via `IsActive=0` no-cache reject + dual SystemEvent + dual AuditTrail (AC-64); deploy-key one-Repo blast radius via FK CASCADE + `LastUsedAt` anomaly + rate cap (AC-65); canonical signing string `GL-SSHSIG-V1\nMETHOD\nPATH\nTIMESTAMP\nNONCE\nsha256(body)` + `git-logs@v2` namespace + `-H sha512` (AC-66). AC-38 amended to list SSH lane AuditActionType seeds (22/23/24). AC count 59 → 66. |
| `98-changelog.md` | v3.8.8 row added. |
| `99-consistency-report.md` | This audit table added; banner v3.8.7 → v3.8.8. |

**Phase 7 scope discipline:** §05/§15/§18/§28/§30/§31 untouched (already at v2.9.1 from Phases 5–6); only §97 was rewritten. Phases 8–10 untouched. Phase B1 still blocked on user.

**AC inventory check:** 66 ACs total (AC-01..AC-66). No AC numbers reused; gaps preserved. All carry GWT format + `Verifies:` pointer + status badge.

## v3.8.9 Audit — Phase 8 API Streaming Spec

| File | Change |
|------|--------|
| `04-rest-api-endpoints.md` | Banner v2.8.3 → v2.9.2. Added new top-level **§11 NDJSON Streaming Retrieval (v2.9.2)** with 9 sub-sections: §11.1 rationale, §11.2 opt-in via `Accept: application/x-ndjson` content negotiation (writes #1–#4 silently ignore), §11.3 5-frame schema (`Header`/`Log`/`ErrorLog`/`Progress`/`End` + optional mid-stream `Error`) with `Schema:"git-logs-v2/ndjson@1"` + monotonic `Seq` + `TotalRowsHint` mirror per AC-50 + `SeverityId` denormalized per AC-51 + `OccurrenceCount` per AC-05, §11.4 ordering & atomicity (flush-after-frame, oversize-frame `LogText` truncation with `"Truncated":true`, client-disconnect closes per-SHA handle within 1 flush cycle), §11.5 four new ConfigKv keys defined doc-side (`NdjsonProgressEveryRows=10000`, `NdjsonProgressEveryMs=2000`, `NdjsonMaxRowsPerStream=1000000`, `NdjsonMaxFrameBytes=262144`), §11.6 resume via `?after-seq=N` + `?stream-id=<uuid>` (best-effort; `GL-NDJSON-CURSOR-LOST` on prune-mid-stream), §11.7 endpoint applicability matrix (#5–#10 all `✅`; #1–#4 `❌`), §11.8 wire example, §11.9 cross-refs. Two new error codes introduced doc-side: `GL-NDJSON-CLIENT-DISCONNECT` (499 informational), `GL-NDJSON-CURSOR-LOST` (500). |
| `98-changelog.md` | v3.8.9 row added. |
| `99-consistency-report.md` | This audit table added; banner v3.8.8 → v3.8.9. |

**Phase 8 scope discipline:** §11.5 four ConfigKv keys are doc-only — physical seeding into `18-schema.sql` and `02-database-schema.md` deferred. §15 new codes `GL-NDJSON-CLIENT-DISCONNECT` / `GL-NDJSON-CURSOR-LOST` introduced doc-side in §11 only — physical addition to §15 error-codes table deferred. §17 OpenAPI must add `application/x-ndjson` content variants for endpoints #5–#10 — deferred. §97 ACs for streaming behavior (frame ordering, opt-in negotiation, resume cursor, oversize frame truncation, client-disconnect cleanup, four new ConfigKv keys, two new GL-NDJSON-* codes) deferred to a future AC quality pass — Phase 7 closed at AC-66 before Phase 8 doc landed. Phases 9–10 untouched. Phase B1 still blocked on user.

**Streaming surface check:** §11 covers all 6 GET endpoints (#5/#6/#7/#8/#9/#10) per the §11.7 applicability matrix; all 4 write endpoints (#1/#2/#3/#4) explicitly excluded with `Accept` header silently ignored.

## v3.8.10 Audit — Phase 9 Pipeline `PreviousHasError` Flag

| File | Change |
|------|--------|
| `18-schema.sql` | Banner v2.9.1 → v2.9.2. `Pipeline` table gained `PreviousHasError INTEGER NOT NULL DEFAULT 0 CHECK (PreviousHasError IN (0,1))` immediately after `HasError`; `HasError` itself gained explicit `CHECK (HasError IN (0,1))` to match. Inline comment block documents back-fill rule (`UPDATE Pipeline SET PreviousHasError = HasError;` on v2.9.1→v2.9.2 upgrade) and write rule (every mutation of `HasError` MUST set `PreviousHasError = OLD.HasError` in the same SQL transaction — single `UPDATE`, no read-modify-write). `ConfigKv.PluginVersion` 2.9.1 → 2.9.2; `MigrationState` marker `2.9.2` appended (11 markers total). |
| `02-database-schema.md` | Banner v3.8.6 → v3.8.10. Pipeline table doc gains `PreviousHasError` row with full back-fill + write-rule narrative + state-transition labels (`first-failure`/`still-failing`/`just-recovered`/`still-green`); `HasError` row also annotated with the new `CHECK` constraint. |
| `01-glossary-and-enums.md` | Banner v3.8.6 → v3.8.10. The single bare `Pipeline` glossary row split into 3 rows: `Pipeline` (cross-references both state booleans), `HasError` (sticky semantics + AC-13 cross-ref), `PreviousHasError` (full transition-labeling rationale + write rule + back-fill rule). |
| `98-changelog.md` | v3.8.10 row added. |
| `99-consistency-report.md` | This audit table added; banner v3.8.9 → v3.8.10. |

**Phase 9 scope discipline:** §97 ACs for `PreviousHasError` (state-transition matrix correctness, back-fill correctness, single-statement write atomicity) deferred to a future AC quality pass — Phase 7 closed at AC-66 before Phase 9 doc landed. §03 admin UI rendering of the four state-transition labels deferred. §04 NDJSON `Header` frame extension to expose the labels deferred. §15 / §22 / §28 / §30 / §31 untouched. Streaming follow-ups deferred from Phase 8 still pending. Phase 10 untouched. Phase B1 still blocked on user.

**Schema validation check:** `Pipeline` now carries 10 columns (`PipelineId, RepoVersionId, AppId, Branch, Pipeline, HasError, PreviousHasError, CreatedAt, UpdatedAt` + UNIQUE constraint as 10th element); `PluginVersion=2.9.2`; 11 MigrationState markers; both `HasError` and `PreviousHasError` carry CHECK constraints restricting to 0/1.

## v3.8.11 Audit — Phase 11 Streaming Follow-ups Pickup

| File | Change |
|------|--------|
| `18-schema.sql` | Banner v2.9.2 → v2.9.3. Seeded 4 NDJSON `ConfigKv` defaults matching §04 §11.5 exactly: `NdjsonProgressEveryRows='10000'`, `NdjsonProgressEveryMs='2000'`, `NdjsonMaxRowsPerStream='1000000'`, `NdjsonMaxFrameBytes='262144'`. `ConfigKv.PluginVersion` 2.9.2 → 2.9.3; `MigrationState` marker `2.9.3` appended (12 markers). Comment notes "data-only, no DDL changes". |
| `15-error-codes.md` | Banner v2.9.1 → v2.9.3. New section *"NDJSON streaming retrieval (see §04 §11)"* added at end of code tables, registering `GL-NDJSON-CLIENT-DISCONNECT` (HTTP 499, informational, server-only audit row, no `Error` frame possible) + `GL-NDJSON-CURSOR-LOST` (HTTP 500, raised on `?after-seq=N` resume after AC-53 prune; wire shape `Header → Error → End{Status:"Error"}`). |
| `17-openapi.yaml` | `info.version` 2.8.2 → 2.9.3 (long-lagging — last touched in v2.8.2; this single bump absorbs Phases 4/5/9/11). `ErrorCode` enum extended with 4 `GL-SHA-DB-*` codes (Phase 4 retroactive sync) + 2 `GL-NDJSON-*` codes. Added 7 schemas in `components.schemas`: `NdjsonHeaderFrame`, `NdjsonLogFrame`, `NdjsonErrorLogFrame`, `NdjsonProgressFrame`, `NdjsonEndFrame`, `NdjsonErrorFrame`, plus `NdjsonFrame` discriminated `oneOf` union with `discriminator.propertyName=Type` mapping. Added reusable `components.responses.NdjsonStream` declaring `Transfer-Encoding: chunked` + `X-Content-Type-Options: nosniff` headers + `application/x-ndjson` content with NDJSON wire example. All 4 GET path objects (`/get-logs`, `/get-pipeline-logs`, `/get-error-logs`, `/get-pipeline-error-logs` — covering all 6 logical endpoints #5–#10) gained: 2 new query params (`after-seq` int64 ≥0, `stream-id` uuid) marked "NDJSON only", a second `application/x-ndjson` content variant on the 200 response, and per-endpoint description naming the streaming behavior. |
| `97-acceptance-criteria.md` | Banner v3.8.8 → v3.8.11. Status legend bumped from "v2.9.1 schema" to "v2.9.3 schema". New **Section J — NDJSON Streaming Retrieval (v2.9.3)** with 6 ACs all `[active]`: AC-67 opt-in via Accept header; AC-68 frame ordering + `Type` discriminator; AC-69 resume via `?after-seq=N` + `?stream-id=<uuid>`; AC-70 client-disconnect handling + `GL-NDJSON-CLIENT-DISCONNECT` audit row; AC-71 per-frame size cap + `"Truncated":true` parity with AC-27; AC-72 `Progress` frame cadence (rows-OR-time triggers, individual `0` disables, both `0` disables entirely). AC count 66 → 72 (sequential AC-67..AC-72; no IDs reused). |
| `98-changelog.md` | v3.8.11 row added. |
| `99-consistency-report.md` | This audit table added; banner v3.8.10 → v3.8.11; Health Score footer rewritten. |

**Validation evidence:**
- *In-memory SQLite:* `pip3 install pyyaml` then `sqlite3.executescript(open('18-schema.sql').read())` clean; `PluginVersion=2.9.3`; 12 MigrationState markers; 19 ConfigKv rows including all 4 `Ndjson*` keys with the exact §04 §11.5 default values.
- *OpenAPI YAML:* `yaml.safe_load` clean parse; all 4 GET paths confirmed carrying both `application/json` and `application/x-ndjson` content keys; 7 `Ndjson*` schemas + `NdjsonStream` response present; `ErrorCode` enum contains both `GL-NDJSON-*` codes and all 4 `GL-SHA-DB-*` codes.

**Phase 11 scope discipline:** §04 §11 doc body untouched (Phase 8 already authoritative). §02/§22/§23/§28/§29/§30/§31/§39 untouched. Phase 9 follow-ups remain deferred (§97 ACs for `PreviousHasError` state-transition matrix / back-fill correctness / single-statement write atomicity; §03 admin UI rendering of the four state-transition labels; §04 NDJSON `Header` frame extension to expose state-transition labels). Phase B1 (§07 App identity) still blocked on user decision.

## v3.8.12 Audit — Phase 12 Phase 9 Follow-ups (AC + Header label exposure)

| File | Change |
|------|--------|
| `04-rest-api-endpoints.md` | Banner v2.9.2 → v2.9.3. §11.3.1 `Header` frame example JSON gained `"StateTransition":"first-failure"`; new bullet documents the field as OPTIONAL, single-pipeline-scope-only (#7/#8/#9/#10), ABSENT entirely on repo-scope (#5/#6) and on 404 / multi-pipeline resolutions, four-value enum drawn from §01 glossary v3.8.10 per §97 AC-73, absence MUST NOT be treated as error. |
| `17-openapi.yaml` | `info.version` 2.9.3 → 2.9.4. `NdjsonHeaderFrame` schema gained `StateTransition: { type: string, enum: [still-green, first-failure, still-failing, just-recovered] }` as OPTIONAL property (NOT in `required`); description cross-references §97 AC-73/AC-74 and notes single-pipeline-scope-only emission. |
| `97-acceptance-criteria.md` | Banner v3.8.11 → v3.8.12. New **Section K — Pipeline.PreviousHasError State Transitions (v2.9.2)** with 3 ACs all `[active]`: AC-73 state-transition label matrix (pure function, exhaustive 4-value enum, no `unknown` / no fifth label, fresh rows label as `first-failure`); AC-74 NDJSON `Header.StateTransition` exposure (single-pipeline-scope-only, exact-string enum, ABSENT on multi/zero pipelines, OpenAPI optional+enum constraint); AC-75 back-fill correctness + single-statement write atomicity (single `UPDATE` migration NOT row-by-row, `HasError` mutations MUST update `PreviousHasError` in SAME SQL statement to close R-M-W window, ORM-split fallback REQUIRES `BEGIN IMMEDIATE` + `SELECT changes()=1`, idempotent `MigrationState` marker `2.9.2`). AC count 72 → 75. |
| `98-changelog.md` | v3.8.12 row added. |
| `99-consistency-report.md` | This audit table added; banner v3.8.11 → v3.8.12; Health Score footer rewritten. |

**Validation evidence:**
- *OpenAPI YAML:* `pyyaml.safe_load` clean; `NdjsonHeaderFrame.properties` lists `StateTransition` with all 4 enum values; `StateTransition` correctly absent from `required` (verified optional).
- *Schema unchanged:* No DDL changes — Phase 12 is doc + AC + OpenAPI surface only. `PluginVersion` remains 2.9.3; `MigrationState` markers unchanged at 12.

**Phase 12 scope discipline:** §03 admin UI rendering of the four state labels intentionally out-of-scope (this is a spec-only project; consumer-side UI is not authored here — AC-73 documents the contract for any future UI consumer). §02 / §18 untouched (DDL contract remains v2.9.2 from Phase 9). §15 untouched (no new error codes — `StateTransition` absence is "not-applicable", not an error). §01 untouched (glossary v3.8.10 labels already authoritative; AC-73 cites them verbatim). All Phase 9 follow-ups now closed (modulo the §03 UI bullet which is consumer-side). Phase B1 (§07 App identity) remains blocked on user.

## v3.8.13 Audit — Phase 13 Deepen Scaffolded ACs

| File | Change |
|------|--------|
| `97-acceptance-criteria.md` | Banner v3.8.12 → v3.8.13. 8 high-traffic one-liner ACs deepened from ~200-260 chars to 1400-2200 chars each (5–10× depth) with full GWT bodies + concrete §-cross-refs: AC-02 Profile schema (no-password rule), AC-03 Migration semver ordering + 12-marker baseline, AC-12 Streaming ingest incremental size caps + atomicity, AC-14 AckResponse Retrieval URL contract, AC-17 App columns + forbidden Phase B1 fields, AC-18 AppLink XOR CHECK + CASCADE, AC-22 §26 6-file Mermaid manifest + render contract, AC-30 ErrorEnvelope shape + RequestId mirroring + NDJSON error split. AC count unchanged at 75 (AC-01..AC-75 sequential, verified). |
| `98-changelog.md` | v3.8.13 row added. |
| `99-consistency-report.md` | This audit table added; banner v3.8.12 → v3.8.13. |

**Validation evidence:** Python regex parse confirms 75 distinct AC IDs sequential AC-01..AC-75; the 8 deepened ACs all measure 1400-2200 chars (vs prior 200-260). No new IDs, no removed IDs, no schema/DDL/OpenAPI changes.


## v3.9.8 Audit — Phase P2 (GAP-V2-03 closed: NDJSON ingest streaming wire format)

| File | Change |
|------|--------|
| `04-rest-api-endpoints.md` | Banner v2.9.3 → v2.9.4. New `### 1.1 Streaming wire format (v2.9.4 — Phase P2)` subsection under §1 `POST /append-log`. Pins: opt-in sentinel `X-GL-Stream: 1` request header; required `Content-Type: application/x-ndjson; charset=utf-8` + `Transfer-Encoding: chunked`; LF-only frame separator; three-frame contract (`StreamHeader` exactly-one with identity ex `Logs`/`ErrorLogs`/`HasError`; `Line` zero-or-more with `{Line, Severity}` mirroring §01 `LogSeverity`; `StreamFooter` exactly-one with authoritative `HasError` boolean); strict server validation (header-before-line, EOF-without-footer rollback, unknown-discriminator rejection, forward-compat unknown-key tolerance); reuses §11.4 `NdjsonMaxRowsPerStream` cap. Documents 4 new `GL-STREAM-*` error codes (NO-HEADER 400, NO-FOOTER 400, TOO-MANY-LINES 413, UNKNOWN-FRAME 400). |
| `98-changelog.md` | v3.9.1 row added (Phase P2). |
| `99-consistency-report.md` | This audit table; banner v3.9.7 → v3.9.8; inventory row for §04 updated to call out Phase P2. |

**Phase P2 scope discipline:** §15 error-codes file, §17 OpenAPI, §97 ACs intentionally untouched — the §1.1 doc-side contract is the source of truth for the next downstream consumer (`28-universal-ci-cli/06-log-shipping-contract.md` AC-28-06, which becomes implementable). §15/§17/§97 lockstep is a follow-on micro-phase; deferring it preserves single-concern phase discipline. §11 retrieval contract (Phase 8/12) untouched. §02 / §18 / §01 untouched (no DDL change, no enum change — `Severity` field reuses existing `LogSeverity` enum verbatim).

## v3.9.9 Audit — Phase P3 (GAP-V2-04 closed: `PreviousHasError` in Ack envelope + OpenAPI)

| File | Change |
|------|--------|
| `04-rest-api-endpoints.md` | Banner v2.9.4 → v2.9.5. Standard Ack Envelope JSON example gains `"PreviousHasError": false`. New ~25-line "Field contract — `PreviousHasError`" subsection covers: type/required (write endpoints #1–#4 only); semantics (true iff prior `Pipeline.PreviousHasError` for `(RepoVersionId, BranchName, PipelineName)` was 1 immediately before request; fresh triple → false, mirrors AC-73 `first-failure` boundary); per-endpoint usage (#1 enables AC-13 auto-`/fixed-log` chaining; #2 detects no-op fixed calls; #3/#4 echo pre-clear state for audit correlation); atomicity (MUST be read in same `BEGIN IMMEDIATE` SQL transaction as the write per AC-75); cross-refs to §01 / §97 AC-13/73/74/75 / §17. |
| `17-openapi.yaml` | `info.version` 2.9.4 → 2.9.5. `AckResponse.PreviousHasError` added as REQUIRED boolean property (added to `required: [Status, PipelineId, Retrieval, PreviousHasError]`); description block reuses §04 contract verbatim with deep-link to "PreviousHasError field contract" subsection. |
| `98-changelog.md` | v3.9.2 row added (Phase P3). |
| `99-consistency-report.md` | This audit table; banner v3.9.8 → v3.9.9; inventory rows for §04 + §17 updated. |

**Phase P3 scope discipline:** §97 ACs untouched — AC-13 already references the auto-fix behavior (the field exposes existing semantics, no new contract). §15 untouched (no new error codes — missing `PreviousHasError` is a server-side schema bug, not a client-visible error mode). §01 glossary `Pipeline.PreviousHasError` entry already authoritative from Phase 9 (v2.9.2). §02 / §18 untouched (no DDL change — the field is computed from existing `Pipeline.PreviousHasError` column already shipped in §18 v2.9.2). The pending `GL-STREAM-*` lockstep micro-phase (deferred from Phase P2) is still open and unrelated to P3.

## v3.9.10 Audit — Phase P4 (GAP-V2-10 closed: pre-parse caps & validation order surfaced in §04)

| File | Change |
|------|--------|
| `04-rest-api-endpoints.md` | Banner v2.9.5 → v2.9.6. New `### 1.2 Pre-parse caps & validation order (v2.9.6 — Phase P4)` subsection added between §1.1 and §2. Single table surfaces the four `ConfigKv` enforcement caps (`RatePerMinPerProfile=60`, `MaxPushPayloadBytes=1048576`, `MaxLinesPerPush=10000`, `MaxLineBytes=65536`) with their error codes (`GL-RATE-LIMIT-EXCEEDED` 429, `GL-PAYLOAD-TOO-LARGE` 413, `GL-LINES-TOO-MANY` 413, soft-truncate per AC-27) and check-time semantics (Content-Length pre-check vs streaming running-total). Pins 11-step strict validation order from TLS/SSH-sig through atomic `BEGIN IMMEDIATE` INSERT. Documents orthogonal `AppendLogMaxStreamSec` (default 30s) wall-clock cap with `GL-INGEST-TIMEOUT` for slow-loris defense, scoped to streaming requests only. |
| `98-changelog.md` | v3.9.3 row added (Phase P4). |
| `99-consistency-report.md` | This audit table; banner v3.9.9 → v3.9.10; inventory row for §04 updated. |

**Phase P4 scope discipline:** §15 / §18 / §97 untouched — no new error codes, no new ConfigKv keys, no new ACs. The four caps and their `GL-*` codes were already authoritative in those files (§18 lines 426–429 for defaults, §15 "Rate limiting + payload (Lane B)" table for codes, §97 AC-12/AC-27/AC-13/AC-75 for behavior). §1.2 is a pure cross-walk-elimination doc surface — a blind implementer reading §04 top-to-bottom no longer needs to flip between three files to learn gate ordering. §17 OpenAPI untouched (validation order is server-side behavior, not wire-format — it does not belong in the API contract that clients consume). §01 / §02 / §18 / §97 untouched. The pending `GL-STREAM-*` lockstep micro-phase (deferred from Phase P2) and §03 admin UI rendering follow-up remain open.

## v3.9.11 Audit — Phase P5 (slot-16 collision resolved)

| File | Change |
|------|--------|
| `16-test-plan.md` → `38-test-plan-superseded.md` | Renamed to resolve §22 slot-16 collision with `16-seed-data.md`. Banner v2.7.0 → **v2.8.0** with full Phase P5 update note + new "History of slot moves" subsection documenting the rename trail. Mirrors the v2.8.6 §16 → §37 precedent recorded in `mem://index.md` Core. Live `16-seed-data.md` content unchanged. |
| `00-overview.md` | Banner v3.8.7 → v3.8.8. Inventory row 16 rewritten (`16-test-plan.md` → `16-seed-data.md` with seed-data description); new inventory row 38 inserted before row 39. |
| `spec/spec-index.md` | Removed `16-test-plan.md` row; inserted new `38-test-plan-superseded.md` row between §37 and §39 with v2.8.0 + Phase P5 note. |
| `spec/dashboard-data.json` | Removed `"16-test-plan.md"` entry from §22 file array; inserted `"38-test-plan-superseded.md"` entry after `"37-blind-ai-gap-analysis.md"`. |
| `spec/28-universal-ci-cli/06-log-shipping-contract.md` | Line 119 rewritten to point at the actual authoritative test-plan locations (`32-cli-test-plan.md` + `33-bats-test-skeleton.md`) instead of the legacy §16 path; explicit "do not link to the legacy slot" note. |
| `99-consistency-report.md` | This audit table; banner v3.9.10 → v3.9.11; inventory row 16 rewritten + new row 38 inserted between 37 and 39; Health Score footer updated for new file-count + locked-vacant range. |

**Phase P5 scope discipline:** §97 ACs untouched (no AC ID added/removed; the rename is filesystem hygiene, not a contract change). §15 / §17 / §18 / §01 / §02 untouched (no DDL, no error code, no enum, no schema change). §37 GAP-V2-08 retrospective row left intact — it documents how the collision was resolved and removing it would erase the audit trail (Phase 39b lesson: historical narrative inside `*-blind-ai-gap-analysis.md` is the audit trail, not actionable). The 7 remaining `grep -rn "16-test-plan"` hits are ALL intentional historical narrative (banners, audit rows, history-of-moves table, retrospective) — zero active links. Slot 16 is now sole-occupied by `16-seed-data.md`; old `16-test-plan.md` slot is PERMANENTLY RETIRED for any new file in §22 (file-slot-immutability rule).

## v3.9.12 Audit — Phase P6 (GAP-V2-06 resolved via locked-vacant precedent)

| File | Change |
|------|--------|
| `37-blind-ai-gap-analysis.md` | Banner v1.1.0 → **v1.2.0**. GAP-V2-06 entry rewritten with `[LOW — RESOLVED 2026-04-28, Phase P6]` flag. Original "5 stub files" recipe REJECTED — added "Original fix recipe (REJECTED)" subsection with two conflict reasons: (1) violates Core memory rule "File slots are immutable once shipped — never reuse a number"; (2) one-line stubs would score 0 on `check-tree-health.cjs --strict` and regress folder 22 from 168/168 → 158/168. Effort-table row 6 struck through. |
| `97-acceptance-criteria.md` | Banner v3.9.1 → **v3.9.2**. New **AC-22-LV1** added ("Locked vacant slots §09–§13 must remain file-absent") declaring: no file may match `spec/22-git-logs-v2/{09,10,11,12,13}-*.md`; next free slot for new §22 content is §40+; §00 italic inventory rows are single source of truth; `check-spec-folder-refs.py` MAY add a per-folder `[locked-vacant]` allowlist entry. AC count 75 → **76**. Verifies §00 v3.8.8 inventory + §37 v1.2.0 + Core memory immutability rule. |
| `98-changelog.md` | New row v3.9.5 documenting Phase P6 with full rejection rationale + chosen resolution + scope discipline. |
| `99-consistency-report.md` | This audit table; banner v3.9.11 → **v3.9.12**; §37 + §97 inventory rows updated; Health Score footer updated for AC count 75 → 76 + GAP-V2-06 closure. |

**Phase P6 scope discipline:** No DDL change, no schema bump, no error code added, no enum changed, no §15 / §17 / §18 / §01 / §02 / §00 edit. §00 inventory unchanged (rows 77–81 already correctly mark §09–§13 as "Locked vacant slot"). The phase is documentation + one new declarative AC. AC-22-LV1 is the canonical machine-checkable artifact for the locked-vacant invariant — future contributors are prohibited from re-opening the GAP-V2-06 stub-file recipe.

## v3.9.13 Audit — Phase P7 (GAP-V2-01 verified RESOLVED + headline refresh)

| File | Change |
|------|--------|
| `37-blind-ai-gap-analysis.md` | Banner v1.2.0 → **v1.3.0**. GAP-V2-01 entry rewritten with `[HIGH — RESOLVED 2026-04-28, Phase P7]` flag. Added audit evidence (mechanical regex sweep over `### AC-` blocks: `incomplete = 0` → 76/76 ACs are well-formed GWT), auditor-impact note (`gwt_block_count: 0 → 76`, gate `G-AC-02` no longer fires; testability uncapped from 60 to 100), outcome (folder-22 GWT conversion frozen; future ACs MUST follow GWT shape), and tree-wide follow-up note pointing at Phase P7b. **Headline verdict refreshed**: blind-AI score `76/100 (B) → 99/100 (A+)`; per-dimension corrections Implementability `85 → 100`, Completeness `40 → 100`, Testability `10 → 100`. Effort-table row 1 struck through. |
| `98-changelog.md` | New row v3.9.6 documenting Phase P7 with full audit-evidence + headline-refresh + scope discipline. |
| `99-consistency-report.md` | This audit table; banner v3.9.12 → **v3.9.13**; §37 inventory row updated to v1.3.0; Health Score footer updated for GAP-V2-01 closure + new P7b follow-up. |

**Phase P7 scope discipline:** No §97 ACs added/removed (AC count unchanged at 76); no DDL change, no schema bump, no error code added, no enum changed, no §15 / §17 / §18 / §01 / §02 / §00 / §04 edit. The phase is documentation + audit verification + headline refresh in `37-blind-ai-gap-analysis.md`. The original GAP-V2-01 fix recipe (use `linter-scripts/generate-gwt-acceptance.py`) was already executed implicitly by the §97 v3.8.5 → v3.8.8 full-rewrite phase (Phase 12, 2026-04-26) and extended through Phases 8/9/12/13/P1–P6 — by the time P7 ran there was nothing left to convert; the work had been completed without being formally closed in §37. P7 closes that bookkeeping gap.

## v3.9.14 Audit — Phase P7b (cross-folder mirror of `## Legacy Index` GWT-completeness exemption codification)

| File | Change |
|------|--------|
| `spec/01-spec-authoring-guide/97-acceptance-criteria.md` | Banner v4.7.0 → **v4.8.0**. New **AC-SAG-28** added codifying that AC headings matching `^AC-[A-Z]+-LEGACY(-\d+)?$` MUST be excluded from any GWT-completeness audit denominator. Carries canonical exemption regex + four-module exemption snapshot (§01 4 / §02 5 / §05 2 / §06 2 = 13 LEGACY rows total) + pre-conditions for new modules introducing a Legacy Index + downstream-tools contract for any future `check-ac-gwt-completeness.py` (MUST hardcode the regex AND emit a banner line `excluding N LEGACY ACs across M modules per AC-SAG-28`). |
| `spec/01-spec-authoring-guide/98-changelog.md` | New row v4.13.0 documenting Phase P7b with full investigation narrative + four-module exemption snapshot + downstream-tools contract. |
| `spec/01-spec-authoring-guide/99-consistency-report.md` | Banner v4.9.0 → **v4.10.0**. New blockquote summarising AC-SAG-28 + closure of Phase P7b + cross-folder mirror to §22. |
| `spec/22-git-logs-v2/98-changelog.md` (this folder) | New row v3.9.7 mirroring the §01 codification so the §22 GAP-V2-01 closure narrative carries the full disposition of the 13-row tree-wide follow-up. |
| `spec/22-git-logs-v2/99-consistency-report.md` (this file) | Banner v3.9.13 → **v3.9.14**; this audit table; Health Score footer updated for Phase P7b closure + open-follow-ups list pruned (P7b removed, P8 promoted to next). |

**Phase P7b scope discipline:** No §22 ACs added/removed (AC count unchanged at 76); no §22 DDL change, no §22 schema bump, no §22 error code, no §22 enum change, no §22 §15/§17/§18/§01/§02/§00/§04 edit. All edits are at §01 (the meta-spec) + this §22 mirror row. §22 itself is unaffected: it carries zero LEGACY rows (verified Phase P7 — the 76/76 GWT score holds, AC-SAG-28's exemption regex matches nothing in §22). The four affected modules (§01/§02/§05/§06) now report 100% GWT-completeness post-exemption.
