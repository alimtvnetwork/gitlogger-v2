---
kind: reference
description: Inlined Mermaid source for all 7 active diagrams in this module. Auditor walker (linter-scripts/audit-ai-implementability.py WALK_GLOBS) reads .md only — not .mmd — so this file embeds the diagram sources as fenced ```mermaid``` blocks for full audit visibility. Closes audit-v7 LOW/D4 "Missing .mmd Source Content" finding (Phase 153 Task S26-D4).
content_axis: normative-contract
axis_rationale: "Reference embed of normative diagram sources (Lesson #36 link-don't-restate is INVERTED here intentionally: walker can't follow .mmd extension, so we embed)"
---

# Diagram Sources (inlined .mmd)

**Version:** 1.0.0
**Updated:** 2026-05-10 (Phase 153 Task S26-D4 — embed .mmd sources for auditor walker visibility; sibling .mmd files remain canonical, this file is regenerated from them)
**Canonical sources:** the `.mmd` files alongside this document remain the single source of truth. This file is a **mechanical mirror** kept in lockstep by the regen pipeline (AC-DG-12). Edits MUST go to the `.mmd` source, then regenerate this file via `bash linter-scripts/regen-diagram-sources-mirror.sh` (or equivalent paste). Any drift between this file and the `.mmd` files is an AC-DG-12 violation.

> **Why this file exists:** the auditor walker (`linter-scripts/audit-ai-implementability.py:47` `WALK_GLOBS = ("*.md", "*.json", "*.yaml", "*.yml", "*.tmpl", "*.toml")`) does NOT include `*.mmd`. Without this mirror, the AI auditor cannot read the diagram sources and flags D4 LOW "Missing .mmd Source Content" on every run. Embedding here gives the auditor full visibility AND keeps the canonical .mmd files renderable by Mermaid CLI / Puppeteer (per `puppeteer.json`).


## `01-er-diagram.mmd`

**Source:** [`./01-er-diagram.mmd`](./01-er-diagram.mmd) · **Rendered:** [`./01-er-diagram.svg`](./01-er-diagram.svg)

```mermaid
%% v3.8.5 — Phase 4 re-render. Split-DB boundary: every entity below lives in the ROOT DB
%% (wp-content/uploads/git-logs/git-logs.sqlite). LogEntry / ErrorLogEntry no longer exist;
%% log lines live in per-SHA files at <ShaLogsRoot>/<aa>/<sha>.db (see §39). The ShaRegistry
%% entity is the only pointer from root → per-SHA tree.
erDiagram
    Profile ||--o{ RoleAssignment : has
    Role ||--o{ RoleAssignment : assigned
    Role ||--o{ RolePermission : grants
    Permission ||--o{ RolePermission : in
    Profile ||--o{ GitProfile : owns
    Provider ||--o{ GitProfile : provider
    Acceptance ||--o{ GitProfile : acceptance
    GitProfile ||--o{ Repo : contains
    Repo ||--o{ RepoVersion : versions
    RepoVersion ||--o{ Pipeline : runs
    Pipeline ||--o{ ShaRegistry : sha
    Profile ||--o{ App : owns
    AppStatus ||--o{ App : status
    App ||--o{ AppLink : links
    AppLinkType ||--o{ AppLink : kind
    GitProfile ||--o{ AppLink : targetGP
    Repo ||--o{ AppLink : targetRepo
    RepoVersion ||--o{ History : timeline
    App ||--o{ History : actor
    PipelineActionType ||--o{ History : actionKind
    PipelineActionType ||--o{ PipelineAction : actionKind
    RepoVersion ||--o{ PipelineAction : on
    Pipeline ||--o{ PipelineAction : on
    Profile ||--o{ PipelineAction : by
    SystemEventType ||--o{ SystemEvent : kind
    Profile ||--o{ SystemEvent : actor
    AuditActionType ||--o{ AuditTrail : kind
    AuditOutcome ||--o{ AuditTrail : outcome
    Profile ||--o{ AuditTrail : actor

    Profile {
        int ProfileId PK
        string UserName
        string Email
        string GeneratedKeyApi
        string Token
        string TempToken
        int UserStatusId FK
    }
    GitProfile {
        int GitProfileId PK
        int ProviderId FK
        int IsOrganization "0|1 v3.8.0 replaces OwnerType"
        string OwnerName
        string ProfileUrl
        int AcceptanceId FK
        string SelectedRepoUrl
        int IsRestrictInBranch
        string StrictBranch
        int OwnedByProfileId FK
    }
    Repo {
        int RepoId PK
        int GitProfileId FK
        string RootRepoName
        string RootRepoUrl
    }
    RepoVersion {
        int RepoVersionId PK
        int RepoId FK
        string VersionSuffix
        string RepoUrl
    }
    Pipeline {
        int PipelineId PK
        int RepoVersionId FK
        string BranchName
        string PipelineName
        int HasError
        string LastGitSha256
    }
    ShaRegistry {
        int ShaRegistryId PK "v2.9.0 split-DB pointer"
        int PipelineId FK "UNIQUE PipelineId Sha"
        string Sha "40 char lowercase hex"
        string DbFilePath "ShaLogsRoot aa sha db"
        int RowCount "mirror of per SHA file"
        int FirstSeenAt
        int LastSeenAt
        int FileSizeBytes
        string Sha256 "audit checksum"
    }
    App {
        int AppId PK
        string AppName
        string AppSlug
        string Description
        int ProfileId FK
        int AppStatusId FK
    }
    AppLink {
        int AppLinkId PK
        int AppId FK
        int AppLinkTypeId FK
        int TargetGitProfileId FK
        int TargetRepoId FK
        int IsActive
    }
    History {
        int HistoryId PK
        int RepoVersionId FK
        int AppId FK
        string BranchName
        string PipelineName
        string GitSha256
        int PipelineActionTypeId FK
        int HasError
        string Summary
        int OccurredAt
    }
    PipelineAction {
        int PipelineActionId PK "v3.8.0 renamed from Action"
        int PipelineActionTypeId FK
        int RepoVersionId FK
        int PipelineId FK
        int ProfileId FK
        int OccurredAt
    }
    SystemEvent {
        int SystemEventId PK "NEW v3.8.0"
        int SystemEventTypeId FK
        int ActorProfileId FK
        string TargetType "Profile GitProfile Repo App SshKey"
        int TargetId
        string Summary
        string DetailJson
        int OccurredAt
    }
    AuditTrail {
        int AuditTrailId PK
        int AuditActionTypeId FK
        int AuditOutcomeId FK
        int ActorProfileId FK
        string RouteName
        int HttpStatus
        string RequestId
        string Detail
        int OccurredAt
    }
    MigrationState {
        int MigrationStateId PK
        string PluginVersion
        int AppliedAt
        string Checksum
    }
```

## `05-auth-validation.mmd`

**Source:** [`./05-auth-validation.mmd`](./05-auth-validation.mmd) · **Rendered:** [`./05-auth-validation.svg`](./05-auth-validation.svg)

```mermaid
%% Diagram type: flowchart TD (NOT an ER diagram)
%% What this answers: "For a CI/CD write request, what is the exact
%%   validation order and which GL-* error code is raised at each
%%   rejection point?"
%% Authoritative source: spec/22-git-logs-v2/05-auth-and-validation.md

flowchart TD
    Start([CI/CD request to write endpoint]) --> Parse[Parse RepoUrl<br/>provider, owner, repoName, versionSuffix]
    Parse --> FindGP{GitProfile found<br/>by Provider+OwnerName?}
    FindGP -- No --> R1[Reject GL-VALIDATION-PROFILE-NOT-FOUND]
    FindGP -- Yes --> AccCheck{Acceptance check}
    AccCheck -->|AcceptAllRepos| BranchCheck
    AccCheck -->|AcceptSelectedRepoOnly: exact match?| BranchCheck
    AccCheck -->|AcceptSelectedRepoInAllVersions: root match + vN suffix?| BranchCheck
    AccCheck -->|fail| R2[Reject GL-VALIDATION-REPO-NOT-ALLOWED]
    BranchCheck{IsRestrictInBranch=1?}
    BranchCheck -- No --> TempTok
    BranchCheck -- Yes, Branch=StrictBranch --> TempTok
    BranchCheck -- Yes, mismatch --> R3[Reject GL-VALIDATION-BRANCH-RESTRICTED]
    TempTok{TempToken matches a Profile?}
    TempTok -- No --> R4[Reject GL-AUTH-TEMPTOKEN-INVALID]
    TempTok -- Yes --> TokCheck{Token matches same Profile?}
    TokCheck -- No --> R5[Reject GL-AUTH-TOKEN-MISMATCH]
    TokCheck -- Yes --> Status{Profile UserStatus = Active?}
    Status -- No --> R6[Reject GL-AUTH-PROFILE-INACTIVE]
    Status -- Yes --> AppGate{Linked App resolvable?}
    AppGate -- No active link --> Pass
    AppGate -- App.Status=Active --> Pass
    AppGate -- App.Status<>Active --> R7[Reject GL-APP-NOT-ACTIVE]
    Pass([Accept -> proceed to handler<br/>AuditTrail AuthSuccess])
    R1 --> AuditReject
    R2 --> AuditReject
    R3 --> AuditReject
    R4 --> AuditReject
    R5 --> AuditReject
    R6 --> AuditReject
    R7 --> AuditReject
    AuditReject([AuditTrail AuthFail / Rejected])
```

## `06-permission-flow.mmd`

**Source:** [`./06-permission-flow.mmd`](./06-permission-flow.mmd) · **Rendered:** [`./06-permission-flow.svg`](./06-permission-flow.svg)

```mermaid
%% Diagram type: flowchart LR (NOT an ER diagram)
%% What this answers: "When a request hits the Admin UI, how do we decide
%%   whether it's allowed? Walk: WP user -> plugin Profile -> Roles ->
%%   Permission union -> required-permission check -> allow or deny."
%% Authoritative source: spec/22-git-logs-v2/05-auth-and-validation.md
%%                       spec/22-git-logs-v2/19-permission-matrix.md

flowchart LR
    Req([Admin UI HTTP request<br/>WP App Password / cookie]):::input
    Req --> WP{{Resolve WP user}}:::step
    WP -->|valid| Map{{Map WP user -> plugin Profile}}:::step
    WP -->|missing| D1[Reject 401<br/>GL-AUTHZ-WP-AUTH-FAILED]:::deny

    Map -->|found| Roles{{Load RoleAssignment rows<br/>for ProfileId}}:::step
    Map -->|none| D2[Reject 403<br/>GL-AUTHZ-NO-PROFILE]:::deny

    Roles --> Perms{{Resolve RolePermission union<br/>across all assigned Roles}}:::step
    Perms --> Check{Required Permission<br/>in resolved set?}:::decision

    Check -- Yes --> Handler([Handler executes<br/>+ AuditTrail Success]):::allow
    Check -- No  --> D3[Reject 403<br/>GL-AUTHZ-PERMISSION-DENIED<br/>+ AuditTrail Rejected]:::deny

    subgraph Seed[Seeded role -> permission map]
        direction TB
        Admin[Admin role<br/>= ALL Permissions]
        Editor[Editor role<br/>= AppView, AppModify,<br/>HistoryView, RepoView]
        Viewer[Viewer role<br/>= AppView, HistoryView, RepoView]
    end

    Perms -.lookup.-> Seed

    classDef input  fill:#e0f2fe,stroke:#0369a1,stroke-width:2px;
    classDef step   fill:#f1f5f9,stroke:#475569;
    classDef decision fill:#fef9c3,stroke:#a16207,stroke-width:2px;
    classDef allow  fill:#dcfce7,stroke:#15803d,stroke-width:2px;
    classDef deny   fill:#fee2e2,stroke:#b91c1c,stroke-width:2px;
```

## `07-rate-limit-flow.mmd`

**Source:** [`./07-rate-limit-flow.mmd`](./07-rate-limit-flow.mmd) · **Rendered:** [`./07-rate-limit-flow.svg`](./07-rate-limit-flow.svg)

```mermaid
%% Diagram type: sequenceDiagram (NOT an ER diagram)
%% What this answers: "When a CI caller hits a write endpoint, how does
%%   the per-Profile token bucket decide allow vs 429, and what gets
%%   written to the WP transient store at each step?"
%% Authoritative source: spec/22-git-logs-v2/10-rate-limit-and-payload.md

sequenceDiagram
    autonumber
    participant CI as CI/CD Caller
    participant API as REST Controller
    participant RL as RateLimiter
    participant TR as WP Transient
    participant SVC as LogIngestService
    participant AUD as AuditTrail

    CI->>API: POST /append-log (TempToken, body)
    API->>API: Resolve Profile from TempToken
    API->>RL: check(ProfileId)
    RL->>TR: read Tokens, LastRefillAt
    TR-->>RL: Tokens=0.4, LastRefillAt=t0
    RL->>RL: refill Tokens

    alt Tokens >= 1
        RL->>TR: write Tokens-1, now
        RL-->>API: allow
        API->>SVC: ingest(body)
        SVC-->>API: ack
        API-->>CI: 200 OK with Retrieval hints
    else Tokens less than 1
        RL-->>API: deny with retryAfter
        API->>AUD: log LogPush Rejected rate
        API-->>CI: 429 with Retry-After header
    end
```

## `08-encryption-v3-flow.mmd`

**Source:** [`./08-encryption-v3-flow.mmd`](./08-encryption-v3-flow.mmd) · **Rendered:** [`./08-encryption-v3-flow.svg`](./08-encryption-v3-flow.svg)

```mermaid
%% Diagram type: flowchart / sequenceDiagram (NOT an ER diagram)
%% What this answers: "If/when v3 encryption-at-rest ships, what is the
%%   key-derivation chain (MasterKey -> DataKey -> LookupKey), where does
%%   the migration ALTER + per-row encrypt run, and how is idempotency
%%   guaranteed via MigrationState?"
%% Authoritative source: spec/22-git-logs-v2/11-encryption-deferred-plan.md

flowchart TD
    A[Install or Upgrade to v3] --> B{GITLOGS_MASTER_KEY env set}
    B -- no --> B1[Abort migration with clear error]
    B -- yes --> C[Store MasterKey in WP option]
    C --> D[Generate DataKey]
    D --> E[Wrap DataKey with MasterKey]
    E --> F[Save WrappedDataKey in ConfigKv]
    F --> G[Derive LookupKey via HKDF]

    G --> H[ALTER Profile ADD TempTokenLookupHash TEXT]
    H --> I[For each Profile row]
    I --> J[Encrypt TempToken AES-256-GCM]
    I --> K[HMAC-SHA256 TempToken with LookupKey]
    J --> L[UPDATE Profile TempToken to ciphertext]
    K --> M[UPDATE Profile TempTokenLookupHash to hmac]
    I --> N[Hash GeneratedKeyApi and Token Argon2id]
    N --> O[UPDATE Profile credentials to hash]

    L --> P[INSERT MigrationState 3.0.0]
    M --> P
    O --> P
    P --> Q[v3 ready lookup-by-hash decrypt-on-match]
```

## `09-endpoints-mindmap.mmd`

**Source:** [`./09-endpoints-mindmap.mmd`](./09-endpoints-mindmap.mmd) · **Rendered:** [`./09-endpoints-mindmap.svg`](./09-endpoints-mindmap.svg)

```mermaid
%% Diagram type: mindmap (NOT an ER diagram)
%% What this answers: "Show me every git-logs/v2 REST endpoint at a glance —
%%   verb, path, request body, response shape, required permission/auth,
%%   audit category, and possible error codes."
%% Authoritative source: spec/22-git-logs-v2/04-rest-api-endpoints.md + 14-endpoint-examples.md
%% Note: in v3.8.0 LogEntry/ErrorLogEntry live in per-SHA SQLite files (see §39).
%%       Reads transparently fan out across the matched ShaRegistry rows.

mindmap
  root((git-logs/v2<br/>REST API))
    Writes (CI/CD callers)
      append-log
        Verb POST
        Path /wp-json/git-logs/v2/append-log
        Auth TempToken plus Token plus Profile Active plus App Active
        Body
          RepoUrl string
          RootRepo string
          Branch string
          PipelineName string
          GitSha256 string 64-hex
          TempToken string
          Token string
          HasError 0 or 1
          Logs array of LogText FilePath Severity
          ErrorLogs array of LogText FilePath
        Response 200
          Status Success
          TraceId uuid
          Retrieval URLs array
        Errors
          GL-VALIDATION-PROFILE-NOT-FOUND 400
          GL-VALIDATION-REPO-NOT-ALLOWED 400
          GL-VALIDATION-BRANCH-RESTRICTED 400
          GL-AUTH-TEMPTOKEN-INVALID 401
          GL-AUTH-TOKEN-MISMATCH 401
          GL-RATE-LIMIT-EXCEEDED 429
          GL-SHA-DB-CREATE-FAILED 500
        Audit LogPush Success or Rejected
      fixed-log
        Verb PUT
        Path /wp-json/git-logs/v2/fixed-log
        Auth same as append-log
        Body RepoUrl Branch RootRepo PipelineName TempToken Token
        Effect Pipeline.HasError 0 plus History Fixed plus PipelineAction Fixed
        Response 200 ack
        Audit LogPush Fixed
      clear-log
        Verb POST
        Path /wp-json/git-logs/v2/clear-log
        Auth same as append-log
        Body RepoUrl Branch RootRepo PipelineName TempToken Token
        Effect drop the per-SHA file rows for one Pipeline plus History Clear
        Response 200 ack
        Audit LogPush Clear
      clear-log-all
        Verb POST
        Path /wp-json/git-logs/v2/clear-log-all
        Auth same as append-log
        Body RepoUrl Branch RootRepo TempToken Token (no PipelineName)
        Effect drop all Pipeline rows on a RepoVersion plus Branch plus History ClearAll
        Response 200 ack
        Audit LogPush ClearAll
    Reads (Admin UI plus viewers)
      get-logs
        Verb GET
        Path /wp-json/git-logs/v2/get-logs (body or ?q= base64 JSON)
        Auth WP App Password or cookie plus Permission HistoryView
        Body RepoUrl GitSha256
        Response 200
          RepoUrl RootRepo BranchName
          PipelineNames array
          IsPass HasError
          Logs array
          ErrorLogs array
        Errors
          GL-AUTHZ-PERMISSION-DENIED 403
          GL-VALIDATION-REPO-NOT-ALLOWED 400
          GL-SHA-DB-NOT-FOUND 404
        Audit LogQuery Success or Rejected
      get-pipeline-logs
        Verb GET
        Path /wp-json/git-logs/v2/get-pipeline-logs
        Auth same as get-logs
        Body RepoUrl GitSha256 PipelineName
        Response 200 scoped to one Pipeline
        Audit LogQuery
      get-error-logs
        Verb GET
        Path /wp-json/git-logs/v2/get-error-logs
        Auth same as get-logs
        Body RepoUrl GitSha256
        Response 200 ErrorLogs only across all pipelines
        Audit LogQuery
      get-pipeline-error-logs
        Verb GET
        Path /wp-json/git-logs/v2/get-pipeline-error-logs
        Auth same as get-logs
        Body RepoUrl GitSha256 PipelineName
        Response 200 ErrorLogs for one Pipeline
        Audit LogQuery
    Cross-cutting
      Common request shape application slash json
      Common error envelope ErrorCode TraceId Message Details
      Rate limit per Profile token bucket Retry-After header
      ID generation TraceId uuid v4 server side
      Idempotency append-log keyed on PipelineId LineNumber GitSha256
```

## `10-ssh-auth-validation.mmd`

**Source:** [`./10-ssh-auth-validation.mmd`](./10-ssh-auth-validation.mmd) · **Rendered:** [`./10-ssh-auth-validation.svg`](./10-ssh-auth-validation.svg)

```mermaid
%% Diagram type: flowchart TD (NOT an ER diagram)
%% What this answers: "For a Lane B request using X-GL-Auth-Mode: ssh,
%%   what is the exact 10-step server validation order from §22/§31, and
%%   which GL-SSH-* / GL-AUTH-* / GL-APP-* error code is raised at each
%%   rejection point?"
%% Owner module: spec/26-gitlogs-diagrams/10-ssh-auth-validation.mmd
%% Render target: svg
%% Authoritative source: spec/22-git-logs-v2/31-ssh-key-auth.md (Server Validation Order)

flowchart TD
    Start([CI/CD request to write endpoint]) --> Mode{X-GL-Auth-Mode header}
    Mode -- absent or temptoken --> FallTT([Fall through to TempToken lane<br/>see 05-auth-validation.mmd])
    Mode -- ssh + TempToken body field both present --> R0[Reject GL-SSH-LANE-CONFLICT]
    Mode -- ssh + ConfigKv.SshAuthMode=required missing TempToken --> SshLane
    Mode -- ssh --> SshLane

    SshLane[Enter SSH lane] --> Hdr{Headers complete?<br/>Fingerprint + Timestamp + Nonce + Signature}
    Hdr -- No --> R1[Reject GL-SSH-HEADER-MISSING]
    Hdr -- Yes --> Skew{abs now - X-GL-Timestamp<br/>less or equal ReplayWindowSeconds<br/>default 300s?}
    Skew -- No --> R2[Reject GL-SSH-TIMESTAMP-SKEW]
    Skew -- Yes --> KeyLookup{SshKey row found<br/>by Fingerprint?}
    KeyLookup -- No row --> R3[Reject GL-SSH-KEY-UNKNOWN]
    KeyLookup -- Row found, IsActive=0 --> R4[Reject GL-SSH-KEY-INACTIVE]
    KeyLookup -- Row found, IsActive=1 --> RepoBind{Parsed RepoUrl<br/>resolves to RepoId<br/>equal SshKey.RepoId?}
    RepoBind -- No --> R5[Reject GL-SSH-REPO-MISMATCH]
    RepoBind -- Yes --> AccCheck{Acceptance + Branch<br/>per GitProfile rules<br/>see 05-auth-validation.mmd steps 3-4}
    AccCheck -- Reject acceptance --> R6[Reject GL-VALIDATION-REPO-NOT-ALLOWED]
    AccCheck -- Reject branch --> R7[Reject GL-VALIDATION-BRANCH-RESTRICTED]
    AccCheck -- Pass --> Nonce{INSERT OR IGNORE<br/>SshNonce SshKeyId Nonce<br/>affected rows = 1?}
    Nonce -- 0 rows, replay --> R8[Reject GL-SSH-NONCE-REUSED]
    Nonce -- 1 row, fresh --> SigVerify{ssh-keygen -Y verify<br/>namespace git-logs@v2<br/>over canonical signing string}
    SigVerify -- Verify failed --> R9[Reject GL-SSH-SIGNATURE-INVALID]
    SigVerify -- Verified --> ProfStatus{OwnedByProfileId.UserStatus<br/>= Active?}
    ProfStatus -- No --> R10[Reject GL-AUTH-PROFILE-INACTIVE]
    ProfStatus -- Yes --> AppGate{Linked App resolvable?}
    AppGate -- No active link --> Pass
    AppGate -- App.Status=Active --> Pass
    AppGate -- App.Status not Active --> R11[Reject GL-APP-NOT-ACTIVE]

    Pass([Accept -> proceed to handler<br/>UPDATE SshKey LastUsedAt<br/>AuditTrail SshAuthSuccess])

    R0 --> AuditReject
    R1 --> AuditReject
    R2 --> AuditReject
    R3 --> AuditReject
    R4 --> AuditReject
    R5 --> AuditReject
    R6 --> AuditReject
    R7 --> AuditReject
    R8 --> AuditReject
    R9 --> AuditReject
    R10 --> AuditReject
    R11 --> AuditReject
    AuditReject([AuditTrail AuthFail / Rejected])

    classDef reject fill:#fee,stroke:#c33,color:#900
    classDef accept fill:#efe,stroke:#393,color:#063
    classDef gate fill:#eef,stroke:#33c,color:#006
    class R0,R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,AuditReject reject
    class Pass,FallTT accept
    class Mode,Hdr,Skew,KeyLookup,RepoBind,AccCheck,Nonce,SigVerify,ProfStatus,AppGate gate
```

---

## Verification

```bash
# Confirm this file is in lockstep with the canonical .mmd sources
for mmd in 01-er-diagram 05-auth-validation 06-permission-flow 07-rate-limit-flow 08-encryption-v3-flow 09-endpoints-mindmap 10-ssh-auth-validation; do
  if ! awk "/^## \\\`${mmd}\\.mmd\\\`/,/^\\\`\\\`\\\`$/" 00-diagram-sources.md \
     | sed -n '/^```mermaid$/,/^```$/p' | sed '1d;$d' \
     | diff -q - "${mmd}.mmd" > /dev/null; then
    echo "DRIFT: ${mmd}.mmd diverges from inlined mirror"
    exit 1
  fi
done
echo "OK: all 7 .mmd sources match their inlined mirror in 00-diagram-sources.md"
```

Drift here is an **AC-DG-12 (regen lockstep) violation** and MUST block merge.
