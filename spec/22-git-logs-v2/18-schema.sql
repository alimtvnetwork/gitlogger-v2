-- ============================================================================
-- Git Logs Plugin — schema + lookup seeds (v2.9.3 — Phase 11: seed 4 Ndjson* ConfigKv keys for §04 streaming)
-- Source spec: spec/22-git-logs-v2/02-database-schema.md, 37-seed-data.md, 31-ssh-key-auth.md, 01-glossary-and-enums.md, 04-rest-api-endpoints.md §11 (Phase 8 NDJSON streaming)
-- Engine: SQLite 3.35+ (single root file)
-- Conventions: PascalCase tables/columns; PK = {Table}Id INTEGER PK AUTOINCREMENT.
-- All FKs: ON UPDATE CASCADE ON DELETE RESTRICT unless noted.
-- ============================================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

BEGIN TRANSACTION;

-- ---------------------------------------------------------------------------
-- Lookup tables (enums)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS UserStatus (
    UserStatusId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Role (
    RoleId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Permission (
    PermissionId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Provider (
    ProviderId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

-- OwnerType lookup retired in v3.8.0 — replaced by GitProfile.IsOrganization boolean.
-- Table intentionally NOT created. See §01 glossary tombstone + §16 seed-data tombstone.

CREATE TABLE IF NOT EXISTS Acceptance (
    AcceptanceId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS AppStatus (
    AppStatusId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS AppLinkType (
    AppLinkTypeId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS LogSeverity (
    LogSeverityId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Numeric INTEGER NOT NULL UNIQUE
);

-- v3.8.0: ActionType lookup renamed to PipelineActionType (the Action table → PipelineAction).
-- The old name implied "any system action" but the table only records pipeline-bound CI events.
-- Non-pipeline business state changes live in SystemEvent (see SystemEventType below). See §08.
CREATE TABLE IF NOT EXISTS PipelineActionType (
    PipelineActionTypeId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

-- v3.8.0: SystemEventType seeds the SystemEvent table for non-Git business events
-- (ProfileCreated, RoleAssigned, AppCreated, SshKeyRevoked, …). See §08.
CREATE TABLE IF NOT EXISTS SystemEventType (
    SystemEventTypeId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS AuditActionType (
    AuditActionTypeId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS AuditOutcome (
    AuditOutcomeId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

-- ---------------------------------------------------------------------------
-- Identity + access
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS Profile (
    ProfileId        INTEGER PRIMARY KEY AUTOINCREMENT,
    UserName         TEXT NOT NULL UNIQUE,
    Email            TEXT NOT NULL,
    GeneratedKeyApi  TEXT NOT NULL,
    Token            TEXT NOT NULL,
    TempToken        TEXT NOT NULL,
    UserStatusId     INTEGER NOT NULL DEFAULT 1
        REFERENCES UserStatus(UserStatusId),
    CreatedAt        INTEGER NOT NULL,
    UpdatedAt        INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS IxProfileTempToken ON Profile(TempToken);

CREATE TABLE IF NOT EXISTS RoleAssignment (
    RoleAssignmentId INTEGER PRIMARY KEY AUTOINCREMENT,
    ProfileId INTEGER NOT NULL REFERENCES Profile(ProfileId) ON DELETE CASCADE,
    RoleId    INTEGER NOT NULL REFERENCES Role(RoleId),
    UNIQUE (ProfileId, RoleId)
);

CREATE TABLE IF NOT EXISTS RolePermission (
    RolePermissionId INTEGER PRIMARY KEY AUTOINCREMENT,
    RoleId       INTEGER NOT NULL REFERENCES Role(RoleId) ON DELETE CASCADE,
    PermissionId INTEGER NOT NULL REFERENCES Permission(PermissionId),
    UNIQUE (RoleId, PermissionId)
);

-- ---------------------------------------------------------------------------
-- Source-control identity
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS GitProfile (
    GitProfileId        INTEGER PRIMARY KEY AUTOINCREMENT,
    ProfileUrl          TEXT NOT NULL UNIQUE,
    ProviderId          INTEGER NOT NULL REFERENCES Provider(ProviderId),
    OwnerName           TEXT NOT NULL,
    IsOrganization      INTEGER NOT NULL DEFAULT 0 CHECK (IsOrganization IN (0,1)), -- v3.8.0 replaces OwnerTypeId
    AcceptanceId        INTEGER NOT NULL REFERENCES Acceptance(AcceptanceId),
    SelectedRepoUrl     TEXT,
    IsRestrictInBranch  INTEGER NOT NULL DEFAULT 0,
    StrictBranch        TEXT,
    CreatedAt           INTEGER NOT NULL,
    UpdatedAt           INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS IxGitProfileLookup ON GitProfile(ProviderId, OwnerName);

CREATE TABLE IF NOT EXISTS Repo (
    RepoId       INTEGER PRIMARY KEY AUTOINCREMENT,
    GitProfileId INTEGER NOT NULL REFERENCES GitProfile(GitProfileId),
    RootRepoName TEXT NOT NULL,
    RepoUrl      TEXT NOT NULL UNIQUE,
    CreatedAt    INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS RepoVersion (
    RepoVersionId INTEGER PRIMARY KEY AUTOINCREMENT,
    RepoId        INTEGER NOT NULL REFERENCES Repo(RepoId) ON DELETE CASCADE,
    VersionSuffix TEXT NOT NULL DEFAULT '',
    RepoUrl       TEXT NOT NULL UNIQUE,
    CreatedAt     INTEGER NOT NULL
);

-- ---------------------------------------------------------------------------
-- App + polymorphic linkage
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS App (
    AppId        INTEGER PRIMARY KEY AUTOINCREMENT,
    AppName      TEXT NOT NULL,
    AppSlug      TEXT NOT NULL UNIQUE,
    Description  TEXT,
    ProfileId    INTEGER NOT NULL REFERENCES Profile(ProfileId),
    AppStatusId  INTEGER NOT NULL DEFAULT 1 REFERENCES AppStatus(AppStatusId),
    CreatedAt    INTEGER NOT NULL,
    UpdatedAt    INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS AppLink (
    AppLinkId       INTEGER PRIMARY KEY AUTOINCREMENT,
    AppId           INTEGER NOT NULL REFERENCES App(AppId) ON DELETE CASCADE,
    AppLinkTypeId   INTEGER NOT NULL REFERENCES AppLinkType(AppLinkTypeId),
    GitProfileId    INTEGER REFERENCES GitProfile(GitProfileId) ON DELETE CASCADE,
    RepoId          INTEGER REFERENCES Repo(RepoId)             ON DELETE CASCADE,
    CreatedAt       INTEGER NOT NULL,
    -- Exactly-one-target check
    CHECK (
        (GitProfileId IS NOT NULL AND RepoId IS NULL)
     OR (GitProfileId IS NULL     AND RepoId IS NOT NULL)
    )
);

CREATE INDEX IF NOT EXISTS IxAppLinkApp ON AppLink(AppId);

-- ---------------------------------------------------------------------------
-- Pipeline + log entries
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS Pipeline (
    PipelineId        INTEGER PRIMARY KEY AUTOINCREMENT,
    RepoVersionId     INTEGER NOT NULL REFERENCES RepoVersion(RepoVersionId) ON DELETE CASCADE,
    AppId             INTEGER REFERENCES App(AppId),
    Branch            TEXT NOT NULL,
    Pipeline          TEXT NOT NULL,
    HasError          INTEGER NOT NULL DEFAULT 0
                          CHECK (HasError IN (0, 1)),
    -- v2.9.2 (Phase 9): captures the value HasError held *immediately before*
    -- the most recent /append-log or /fixed-log transition. Lets the UI render
    -- "first-failure" vs "still-failing" vs "just-recovered" without scanning
    -- the per-SHA log file. Back-fill rule on migration to v2.9.2: copy the
    -- current HasError into PreviousHasError so the very first transition
    -- after upgrade is correctly labeled "no change" rather than "new failure".
    PreviousHasError  INTEGER NOT NULL DEFAULT 0
                          CHECK (PreviousHasError IN (0, 1)),
    CreatedAt         INTEGER NOT NULL,
    UpdatedAt         INTEGER NOT NULL,
    UNIQUE (RepoVersionId, Branch, Pipeline)
);

-- ---------------------------------------------------------------------------
-- Per-SHA log storage registry (Q3 Split-DB, v2.9.0)
-- LogEntry and ErrorLogEntry tables MOVED out of root DB.
-- They now live in per-SHA SQLite files under <ShaLogsRoot>/<Sha[0:2]>/<Sha>.db
-- See §39-split-db-log-storage.md for the per-SHA file schema.
-- ShaRegistry tracks which SHAs have a per-SHA file and metadata about it.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS ShaRegistry (
    ShaRegistryId  INTEGER PRIMARY KEY AUTOINCREMENT,
    PipelineId     INTEGER NOT NULL REFERENCES Pipeline(PipelineId) ON DELETE CASCADE,
    Sha            TEXT NOT NULL,                 -- 40-char lowercase hex
    DbFilePath     TEXT NOT NULL,                 -- relative to ShaLogsRoot
    RowCount       INTEGER NOT NULL DEFAULT 0,    -- total rows across LogEntry+ErrorLogEntry in the per-SHA file
    FirstSeenAt    INTEGER NOT NULL,
    LastSeenAt     INTEGER NOT NULL,
    FileSizeBytes  INTEGER NOT NULL DEFAULT 0,
    Sha256         TEXT,                          -- nullable; computed at backup/checksum time
    UNIQUE (PipelineId, Sha)
);

CREATE INDEX IF NOT EXISTS IxShaRegistrySha       ON ShaRegistry(Sha);
CREATE INDEX IF NOT EXISTS IxShaRegistryLastSeen  ON ShaRegistry(LastSeenAt);

-- ---------------------------------------------------------------------------
-- Audit triumvirate
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS History (
    HistoryId            INTEGER PRIMARY KEY AUTOINCREMENT,
    RepoVersionId        INTEGER NOT NULL REFERENCES RepoVersion(RepoVersionId) ON DELETE CASCADE,
    PipelineId           INTEGER REFERENCES Pipeline(PipelineId),
    AppId                INTEGER REFERENCES App(AppId),
    PipelineActionTypeId INTEGER NOT NULL REFERENCES PipelineActionType(PipelineActionTypeId), -- v3.8.0 was ActionTypeId
    HasError             INTEGER NOT NULL DEFAULT 0,
    Summary              TEXT,
    OccurredAt           INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS IxHistoryRepoVersion ON History(RepoVersionId, OccurredAt);

-- v3.8.0: renamed from `Action` (table) — pipeline-bound enum log. See §08.
CREATE TABLE IF NOT EXISTS PipelineAction (
    PipelineActionId     INTEGER PRIMARY KEY AUTOINCREMENT,
    HistoryId            INTEGER REFERENCES History(HistoryId) ON DELETE CASCADE,
    PipelineActionTypeId INTEGER NOT NULL REFERENCES PipelineActionType(PipelineActionTypeId),
    RepoVersionId        INTEGER NOT NULL REFERENCES RepoVersion(RepoVersionId) ON DELETE CASCADE,
    PipelineId           INTEGER REFERENCES Pipeline(PipelineId),
    ProfileId            INTEGER REFERENCES Profile(ProfileId),
    Detail               TEXT,
    OccurredAt           INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS IxPipelineActionRepoVersion ON PipelineAction(RepoVersionId, OccurredAt);
CREATE INDEX IF NOT EXISTS IxPipelineActionType        ON PipelineAction(PipelineActionTypeId, OccurredAt);

-- v3.8.0 NEW: business state changes that are NOT Git pushes
-- (ProfileCreated, RoleAssigned, GitProfileAcceptanceChanged, AppCreated, SshKeyRevoked, …).
-- Loose polymorphic target — `TargetType`/`TargetId` carry no FK CHECK so audit history
-- outlives the entity row. See §08 for the four-table responsibility split.
CREATE TABLE IF NOT EXISTS SystemEvent (
    SystemEventId      INTEGER PRIMARY KEY AUTOINCREMENT,
    SystemEventTypeId  INTEGER NOT NULL REFERENCES SystemEventType(SystemEventTypeId),
    ActorProfileId     INTEGER REFERENCES Profile(ProfileId),
    TargetType         TEXT,        -- Profile | GitProfile | Repo | App | SshKey | RoleAssignment
    TargetId           INTEGER,     -- PK in the table named by TargetType (no FK)
    Summary            TEXT,
    DetailJson         TEXT,
    OccurredAt         INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS IxSystemEventType   ON SystemEvent(SystemEventTypeId, OccurredAt);
CREATE INDEX IF NOT EXISTS IxSystemEventActor  ON SystemEvent(ActorProfileId, OccurredAt);
CREATE INDEX IF NOT EXISTS IxSystemEventTarget ON SystemEvent(TargetType, TargetId, OccurredAt);

CREATE TABLE IF NOT EXISTS AuditTrail (
    AuditTrailId       INTEGER PRIMARY KEY AUTOINCREMENT,
    AuditActionTypeId  INTEGER NOT NULL REFERENCES AuditActionType(AuditActionTypeId),
    AuditOutcomeId     INTEGER NOT NULL REFERENCES AuditOutcome(AuditOutcomeId),
    ProfileId          INTEGER REFERENCES Profile(ProfileId),
    AppId              INTEGER REFERENCES App(AppId),
    RouteName          TEXT,
    RequestId          TEXT,
    HttpStatus         INTEGER,
    Detail             TEXT,
    OccurredAt         INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS IxAuditTrailRequest ON AuditTrail(RequestId);

-- ---------------------------------------------------------------------------
-- SSH-Key Lane B (v2.9.1, Phase 5 — see §31)
--   Deploy-key model: one SshKey row binds to exactly one Repo.
--   SshNonce is replay defense — rows pruned to ReplayWindowSeconds.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS SshKey (
    SshKeyId          INTEGER PRIMARY KEY AUTOINCREMENT,
    Fingerprint       TEXT    NOT NULL UNIQUE,                    -- 'SHA256:' + base64(sha256(pubkey))
    RepoId            INTEGER NOT NULL REFERENCES Repo(RepoId) ON DELETE CASCADE,
    KeyType           TEXT    NOT NULL,                           -- ssh-ed25519 | ssh-rsa | ecdsa-sha2-nistp256 | …
    PublicKey         TEXT    NOT NULL,                           -- full OpenSSH single-line pubkey
    Label             TEXT,
    OwnedByProfileId  INTEGER NOT NULL REFERENCES Profile(ProfileId),
    IsActive          INTEGER NOT NULL DEFAULT 1 CHECK (IsActive IN (0,1)),
    LastUsedAt        INTEGER,
    CreatedAt         INTEGER NOT NULL,
    RevokedAt         INTEGER
);

CREATE INDEX IF NOT EXISTS IxSshKeyRepoActive ON SshKey(RepoId, IsActive);
CREATE INDEX IF NOT EXISTS IxSshKeyOwner      ON SshKey(OwnedByProfileId);

CREATE TABLE IF NOT EXISTS SshNonce (
    SshNonceId  INTEGER PRIMARY KEY AUTOINCREMENT,
    SshKeyId    INTEGER NOT NULL REFERENCES SshKey(SshKeyId) ON DELETE CASCADE,
    Nonce       TEXT    NOT NULL,                                  -- client-supplied, ≥16 bytes base64
    SeenAt      INTEGER NOT NULL,
    UNIQUE (SshKeyId, Nonce)
);

CREATE INDEX IF NOT EXISTS IxSshNonceSeenAt ON SshNonce(SeenAt);

-- ---------------------------------------------------------------------------
-- Operational
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS ConfigKv (
    KeyName   TEXT PRIMARY KEY,
    ValueText TEXT NOT NULL,
    UpdatedAt INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS MigrationState (
    PluginVersion TEXT PRIMARY KEY,
    AppliedAt     INTEGER NOT NULL,
    Checksum      TEXT
);

-- ============================================================================
-- Seeds — see 37-seed-data.md (slot moved from 16 in v2.8.6)
-- ============================================================================

INSERT OR IGNORE INTO UserStatus (UserStatusId, Name) VALUES
    (1,'Active'),(2,'Suspended'),(3,'Revoked');

INSERT OR IGNORE INTO Role (RoleId, Name) VALUES
    (1,'Admin'),(2,'Editor');

INSERT OR IGNORE INTO Permission (PermissionId, Name) VALUES
    (1,'AppCreate'),(2,'AppView'),(3,'AppModify'),(4,'AppDelete'),
    (5,'ProfileCreate'),(6,'ProfileView'),(7,'ProfileModify'),(8,'ProfileDelete'),
    (9,'GitProfileCreate'),(10,'GitProfileView'),(11,'GitProfileModify'),(12,'GitProfileDelete'),
    (13,'RepoView'),(14,'RepoModify'),(15,'RepoDelete'),
    (16,'HistoryView'),(17,'LogPush');

INSERT OR IGNORE INTO Provider (ProviderId, Name) VALUES
    (1,'GitHub'),(2,'GitLab');

-- OwnerType seed retired in v3.8.0 — GitProfile.IsOrganization (0/1) replaces lookup.

INSERT OR IGNORE INTO Acceptance (AcceptanceId, Name) VALUES
    (1,'AcceptAllRepos'),(2,'AcceptSelectedRepoOnly'),(3,'AcceptSelectedRepoInAllVersions');

INSERT OR IGNORE INTO AppStatus (AppStatusId, Name) VALUES
    (1,'Active'),(2,'Disabled'),(3,'Archived');

INSERT OR IGNORE INTO AppLinkType (AppLinkTypeId, Name) VALUES
    (1,'GitProfile'),(2,'Repo');

INSERT OR IGNORE INTO LogSeverity (LogSeverityId, Name, Numeric) VALUES
    (1,'Trace',10),(2,'Debug',20),(3,'Info',30),
    (4,'Warn',40),(5,'Error',50),(6,'Fatal',60);

-- v3.8.0: PipelineActionType replaces ActionType
INSERT OR IGNORE INTO PipelineActionType (PipelineActionTypeId, Name) VALUES
    (1,'Append'),(2,'Fixed'),(3,'Clear'),(4,'ClearAll');

-- v3.8.0 NEW: SystemEventType — 16 seeded business-event kinds. See §08 + §01 glossary.
INSERT OR IGNORE INTO SystemEventType (SystemEventTypeId, Name) VALUES
    (1,'ProfileCreated'),(2,'ProfileDeleted'),(3,'ProfileStatusChanged'),
    (4,'RoleAssigned'),(5,'RoleRevoked'),
    (6,'GitProfileCreated'),(7,'GitProfileAcceptanceChanged'),(8,'GitProfileBranchRestrictionChanged'),
    (9,'AppCreated'),(10,'AppStatusChanged'),(11,'AppLinkAdded'),(12,'AppLinkRemoved'),
    (13,'SshKeyRegistered'),(14,'SshKeyRevoked'),(15,'SshKeyRotated'),
    (16,'TempTokenRotated');

INSERT OR IGNORE INTO AuditActionType (AuditActionTypeId, Name) VALUES
    (1,'ProfileCreate'),(2,'ProfileUpdate'),(3,'ProfileDelete'),
    (4,'GitProfileCreate'),(5,'GitProfileUpdate'),(6,'GitProfileDelete'),
    (7,'RepoCreate'),(8,'RepoUpdate'),(9,'RepoDelete'),
    (10,'AppCreate'),(11,'AppUpdate'),(12,'AppDelete'),(13,'AppLinkChange'),
    (14,'LogPush'),(15,'LogQuery'),
    (16,'AuthSuccess'),(17,'AuthFail'),(18,'MigrationRun'),
    (19,'Prune'),(20,'Restore'),
    (21,'PluginUninstall'),
    (22,'SshKeyRegister'),(23,'SshKeyRevoke'),(24,'SshKeyRotate'),
    (25,'ConfigChange');

INSERT OR IGNORE INTO AuditOutcome (AuditOutcomeId, Name) VALUES
    (1,'Success'),(2,'Rejected'),(3,'Error');

-- Admin role gets every permission
INSERT OR IGNORE INTO RolePermission (RoleId, PermissionId)
SELECT 1, PermissionId FROM Permission;

-- Editor role: view + modify, no create/delete, no LogPush
INSERT OR IGNORE INTO RolePermission (RoleId, PermissionId) VALUES
    (2,2),(2,3),(2,6),(2,10),(2,11),(2,13),(2,14),(2,16);

-- ConfigKv defaults
INSERT OR IGNORE INTO ConfigKv (KeyName, ValueText, UpdatedAt) VALUES
    ('LogLevelMin',           'Info',     strftime('%s','now')),
    ('PluginVersion',         '2.9.3',    strftime('%s','now')),
    ('RatePerMinPerProfile',  '60',       strftime('%s','now')),
    ('MaxPushPayloadBytes',   '1048576',  strftime('%s','now')),
    ('MaxLinesPerPush',       '10000',    strftime('%s','now')),
    ('MaxLineBytes',          '65536',    strftime('%s','now')),
    -- v2.5 additions
    ('MaintenanceMode',       '0',        strftime('%s','now')),  -- §23 backup/restore gate
    -- v2.6 additions
    ('UninstallMode',         'Preserve', strftime('%s','now')),  -- §29 ∈ {Preserve,Archive,Wipe}
    ('AllowedReadOrigins',    '',         strftime('%s','now')),  -- §30 S3 CORS allowlist (CSV; empty = none)
    -- v2.7 additions
    ('SshReplayWindowSec',    '300',      strftime('%s','now')),  -- §31 SSH timestamp skew tolerance
    -- v2.9 additions (Q3 Split-DB, §39)
    ('ShaLogsRoot',           'logs',     strftime('%s','now')),  -- root folder for per-SHA .db files (relative to plugin data dir)
    ('MaxOpenShaDbHandles',   '32',       strftime('%s','now')),  -- LRU cache cap for open per-SHA SQLite handles
    ('ShaDbIdleCloseSec',     '120',      strftime('%s','now')),  -- idle seconds before a per-SHA handle is closed
    -- v2.9.1 additions (Phase 5 SSH-Key Lane B, §31)
    ('SshAuthMode',           'optional', strftime('%s','now')),  -- §31 lane gate ∈ {optional, preferred, required}
    ('SshNonceJanitorBatch',  '100',      strftime('%s','now')),  -- §31 max SshNonce rows pruned per request
    -- v2.9.3 additions (Phase 11 NDJSON streaming, §04 §11)
    ('NdjsonProgressEveryRows', '10000',  strftime('%s','now')),  -- §04 §11.5 emit Progress frame every N rows; 0 disables row-based progress
    ('NdjsonProgressEveryMs',   '2000',   strftime('%s','now')),  -- §04 §11.5 emit Progress frame every N ms; 0 disables time-based progress
    ('NdjsonMaxRowsPerStream',  '1000000',strftime('%s','now')),  -- §04 §11.5 hard cap rows per stream; on hit End{Status:"Truncated"}, client resumes via ?after-seq=
    ('NdjsonMaxFrameBytes',     '262144', strftime('%s','now')); -- §04 §11.5 per-frame JSON byte cap (256 KiB); oversized LogText truncated with "Truncated":true

-- Migration marker — last
INSERT OR IGNORE INTO MigrationState (PluginVersion, AppliedAt, Checksum) VALUES
    ('2.0.0', strftime('%s','now'), NULL),
    ('2.5.0', strftime('%s','now'), NULL),
    ('2.6.0', strftime('%s','now'), NULL),
    ('2.7.0', strftime('%s','now'), NULL),
    ('2.8.0', strftime('%s','now'), NULL),  -- doc-only consolidation cycle (no DDL changes)
    ('2.8.7', strftime('%s','now'), NULL),  -- §18/§15 audit alignment
    ('2.8.8', strftime('%s','now'), NULL),  -- Q1 IsOrganization (column rename + table drop)
    ('2.8.9', strftime('%s','now'), NULL),  -- Q2 PipelineAction rename + SystemEvent
    ('2.9.0', strftime('%s','now'), NULL),  -- Q3 Split-DB: drop LogEntry/ErrorLogEntry from root, add ShaRegistry + 3 ConfigKv
    ('2.9.1', strftime('%s','now'), NULL),  -- Phase 5: SSH-Key Lane B canonical schema (SshKey + SshNonce + 2 ConfigKv)
    ('2.9.2', strftime('%s','now'), NULL),  -- Phase 9: add Pipeline.PreviousHasError boolean (back-fill = copy current HasError)
    ('2.9.3', strftime('%s','now'), NULL);   -- Phase 11: seed 4 Ndjson* ConfigKv keys for §04 NDJSON streaming (data-only, no DDL changes)

COMMIT;
