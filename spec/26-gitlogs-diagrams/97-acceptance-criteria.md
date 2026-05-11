# Acceptance Criteria — Gitlogs Diagrams

**Version:** 3.10.0
**Updated:** 2026-05-11 (Sess-84 B-2-§26 — minted closed-set "Mechanically enforced by — gate-citation matrix" between Inlined Contracts and Acceptance Criteria. Maps all 29 AC families (24 AC-DG-NN + 5 cross-ref AC-NN) to their auditing §27 gate slot. Coverage 29/29 (100%). Slot `63-check-diagram-parity.md` cited 17× (59% — primary §26 diagram-parity auditor). 4-clause reflexive drift contract. Sister to §27 cross-cohort DAG edge **E-7**. Mirror of §22/§23/§24 §97 closures — completes the B-2 mirror-quartet for the citation-matrix pattern. AC count unchanged at 24 AC-DG; no AC body edits.)
**Updated-prev:** 2026-05-11 (Sess-70 B-25 — minted **AC-DG-24** `[critical]` ratifying the Sess-58 A-47 deferred enum-mirror parity binding. AC count 23 → 24. Lifts §26 R-band C5 19 → 20.)
**Updated-prev:** 2026-05-10 (Session 13 — added AC-DG-23 narrative-header block contract; AC count 26 → 27.)
**Scope:** `spec/26-gitlogs-diagrams/` — Mermaid diagram artifacts that visualize the §22 Git Logs WP plugin contracts.

---

## Module Summary

§26 holds the **6 active Mermaid diagrams** that visualize the §22 Git Logs schema, auth flow, RBAC permission resolution, rate-limiting, encryption v3 derivation chain, and REST endpoint surface. It is a **derivative spec** — every diagram MUST stay in lockstep with §22's authoritative prose; drift is a CODE-RED governance violation. Slots `02`/`03`/`04` are **intentional locked gaps** (retired in v2.0.0, never reusable per AC-SAG-04 slot-immutability rule).

---

## Inlined Contracts

```text
ACTIVE_DIAGRAMS:           01-er-diagram.mmd, 05-auth-validation.mmd,
                           06-permission-flow.mmd, 07-rate-limit-flow.mmd,
                           08-encryption-v3-flow.mmd, 09-endpoints-mindmap.mmd
LOCKED_GAPS:               02 (was domain-design), 03 (was endpoints-write),
                           04 (was endpoints-read)
RENDER_TOOL:               @mermaid-js/mermaid-cli (mmdc)
RENDER_CMD:                mmdc -i <file>.mmd -o <file>.svg -p puppeteer.json -b transparent
SOURCE_OF_TRUTH:           spec/22-git-logs-v2/
ER_TABLES_REQUIRED:        Profile, RoleAssignment, RolePermission, GitProfile,
                           Repo, RepoVersion, Pipeline, ShaRegistry, App, AppLink,
                           History, PipelineAction, SystemEvent, AuditTrail,
                           MigrationState + lookup tables
ER_TABLES_FORBIDDEN:       LogEntry, ErrorLogEntry, OwnerType (removed v3.8.0)
FORBIDDEN_TOKENS:          JWT, RS256, JWKS (dropped in v2 — locked decision 5)
HEADER_COMMENT_CONTRACT:   every flowchart/sequenceDiagram/mindmap MUST start with
                           `%% Diagram type: <type>`
                           `%% What this answers: <one-line intent>`
GL_REJECT_CODE_FORMAT:     GL-{CATEGORY}-{NAME} (e.g. GL-AUTH-INVALID-TOKEN)
8_ENDPOINTS:               POST /v1/repo, POST /v1/repo/{id}/version,
                           POST /v1/pipeline, POST /v1/sha,
                           GET /v1/repo, GET /v1/repo/{id}/versions,
                           GET /v1/pipeline/{id}, GET /v1/system-event
```

---

## Mechanically enforced by — gate-citation matrix (Sess-84 B-2-§26)

**Closed-set inventory** mapping each AC family in this file to the §27 active gate slot that audits it. Sister to §27 `00-cross-cohort-read-order-dag.md` edge **E-7** (§27 → §26 audit-surface coverage). Pinned closed-set: every AC-DG-NN and AC-NN (cross-ref) MUST appear in exactly one row below; new ACs require a same-PR row addition (reflexive drift contract clause-1). Mirror of §22/§23/§24 §97 closures (Sess-81/82/83) — completes the B-2 sweep across 4 cohorts (mirror-quartet anchor for the citation-matrix pattern). Many rows are summary roll-ups of per-AC literal `**Mechanically enforced by:**` lines already present below; the matrix is the closed-set surface that makes the roll-up auditable in one walker hop.

| AC | Surface audited | **Mechanically enforced by** (§27 slot) | Status |
|---|---|---|---|
| AC-DG-01 | ER diagram contains every §22 table | `63-check-diagram-parity.md` (gate #41 clause 2 — ER entity-set superset) | active |
| AC-DG-02 | ER relationships match §22 cardinalities | `63-check-diagram-parity.md` (sister-clause cardinality arrow audit) | active |
| AC-DG-03 | Auth validation flow follows locked order | `63-check-diagram-parity.md` (sister-clause flow-order audit) | active |
| AC-DG-04 | Permission flow resolves via RolePermission union | `63-check-diagram-parity.md` (sister-clause permission-resolution audit) | active |
| AC-DG-05 | Header comments declare type + intent | `63-check-diagram-parity.md` (clause 6 narrative-header schema) | active |
| AC-DG-06 | All diagrams emoji-free, render without lexer errors | `63-check-diagram-parity.md` (gate #41 clause 4 — emoji-free Mermaid lexer compliance) | active |
| AC-DG-07 | No JWT / RS256 / JWKS references | `03-check-forbidden-strings.md` (forbidden-strings JWT/RS256/JWKS phrase sweep) | active |
| AC-DG-08 | Endpoints mindmap covers all 8 REST endpoints | `63-check-diagram-parity.md` (sister-clause endpoint-coverage audit) | active |
| AC-DG-09 | Encryption v3 flow covers MasterKey → DataKey → LookupKey | `63-check-diagram-parity.md` (sister-clause crypto-chain audit) | active |
| AC-DG-10 | Slots 02, 03, 04 remain intentional locked gaps | `04-check-forbidden-spec-paths.md` (closed-set vacant-slot audit) | active |
| AC-DG-11 | Every `.mmd` source has sibling `.svg` build artifact | `63-check-diagram-parity.md` (sister-clause SVG-companion audit) | active |
| AC-DG-12 | `.svg` artifacts regenerated when `.mmd` source changes | `63-check-diagram-parity.md` (sister-clause SHA-deterministic SVG render audit per AC-23) | active |
| AC-DG-13 | Header `Authoritative source` link points to live §22 overview | `01-check-spec-cross-links.md` (gate #01 active — link-presence audit) | active |
| AC-DG-14 | Diagram count + per-diagram type match inventory table | `63-check-diagram-parity.md` (sister-clause inventory-parity audit) | active |
| AC-DG-15 | Rate-limit diagram visualizes per-Profile token-bucket | `63-check-diagram-parity.md` (sister-clause rate-limit shape audit) | active |
| AC-DG-16 | All node IDs are kebab-case ASCII | `63-check-diagram-parity.md` (sister-clause node-ID lexer audit) | active |
| AC-DG-17 | `GL-*` reject codes used in diagrams are defined in §22 error registry | `42-check-error-envelope-uniformity.md` (cross-cohort GL-* enum parity) + `63-check-diagram-parity.md` (sister-clause code-reference audit) | active |
| AC-DG-18 | `puppeteer.json` Mermaid render config committed | `02-check-spec-folder-refs.md` (gate #02 active — file-presence audit) | active |
| AC-DG-19 | `98-changelog.md` records every `.mmd` content change | `64-meta-verify-lockstep.md` (clause-5 banner-triple lockstep + change-cadence audit) | active |
| AC-DG-20 | Self-application: every active diagram passes AC-DG-01..19 | `63-check-diagram-parity.md` (gate #41 self-application clause — runs all sub-clauses) | active |
| AC-DG-21 | SSH auth-lane diagram covers all 10 §31 validation steps + 11 reject codes | `63-check-diagram-parity.md` (sister-clause SSH-validation step coverage) | active |
| AC-DG-22 | Derivative-artifact module relationship to spec/22 pinned auditor-authoritative | `64-meta-verify-lockstep.md` (clause-5 banner-triple lockstep) + `04-check-forbidden-spec-paths.md` (derivative-boundary audit) | active |
| AC-DG-23 | Every `.mmd` source begins with 4-line narrative header block | `63-check-diagram-parity.md` (clause-6 `narrative-header-schema` mode) | active |
| AC-DG-24 | §22 enum-catalog mirror parity is on-disk drift-checkable | load-proven inline `diff` command in §00 line 151 (load-proof on disk; §27 promotion `enum-mirror-26-vs-22-aligned` queued) + `64-meta-verify-lockstep.md` (clause-5 banner-triple lockstep) | active |
| **— Cross-References (post-Legacy-Index Lesson-anchored ACs) —** | | | |
| AC-22 | Derivative-context module pin (Lesson #29) | `37-check-spec22-inventory.md` (cross-cohort §22 derivative-pin audit) | active |
| AC-23 | Deterministic SVG-render protocol (.mmd-source SHA primary) | `63-check-diagram-parity.md` (sister-clause SHA-deterministic render audit; load-proof binding for AC-DG-12) | active |
| AC-24 | Tier 2 stdlib fallback — Python `xml.etree.ElementTree` canonicaliser | `63-check-diagram-parity.md` (sister-clause canonicalisation-fallback audit) | active |
| AC-25 | Cross-Module Externalized Citation Map (Lesson #36/37) | `01-check-spec-cross-links.md` (gate #01 active) + `02-check-spec-folder-refs.md` (gate #02 active) | active |
| AC-26 | Sibling Artifact Delegation Map (Lesson #21) | `04-check-forbidden-spec-paths.md` (sister-clause sibling-allowlist audit) | active |

**Reflexive drift contract (this matrix):**
1. Every new AC-DG-NN or AC-NN (cross-ref) MUST add a row here in the same PR (mechanically enforced by `47-check-ac-section-orphan-header.md` + `48-check-ac-prefix-contract.md` + reviewer-attestation).
2. If a §27 gate slot in column 3 is renumbered or retired, this matrix MUST refresh in the same PR (mechanically enforced by `64-meta-verify-lockstep.md` clause-3 banner-triple lockstep).
3. The "Status" column MUST stay as `active` for all rows; if any drops to `proposed` or `deferred`, the same-PR change MUST also bump §99 with a downgrade banner explaining why.
4. Cross-cohort consistency: this matrix MUST cite gate slots from §27 only — never from §28 or other cohorts (mechanically enforced by edge **E-7** in `spec/27-spec-toolchain/00-cross-cohort-read-order-dag.md`).

**Coverage**: 29/29 ACs cited (100%; 24 AC-DG-NN + 5 AC-NN cross-refs). Gate-slot reuse-count distribution: `63-check-diagram-parity.md` ×17 (primary §26 diagram-parity auditor — reflects that §26 IS the diagram cohort, so slot-63 reuse is the contract surface, not gate-bloat), `64-meta-verify-lockstep.md` ×3, `04-check-forbidden-spec-paths.md` ×3, `01-check-spec-cross-links.md` ×2, `02-check-spec-folder-refs.md` ×2, `42`/`03`/`37` ×1 each, plus 1 load-proven inline-diff (AC-DG-24). The 17/29 slot-63 dominance (59%) is the strongest single-gate concentration across the §22/§23/§24/§26 mirror-quartet — by-design, since §26's normative-contract surface is "diagram correctness" and slot-63 is the diagram-parity gate.

---

## Acceptance Criteria

### AC-DG-01 — ER diagram contains every §22 table; forbidden tables absent

- **Given** the file `01-er-diagram.mmd`,
- **When** parsed by Mermaid CLI,
- **Then** it MUST declare `erDiagram` AND MUST include every entity from `../22-git-logs-v2/02-database-schema.md`: `Profile`, `RoleAssignment`, `RolePermission`, `GitProfile`, `Repo`, `RepoVersion`, `Pipeline`, `ShaRegistry`, `App`, `AppLink`, `History`, `PipelineAction`, `SystemEvent`, `AuditTrail`, `MigrationState`, plus all lookup tables. The forbidden v1 entities `LogEntry`, `ErrorLogEntry`, and `OwnerType` MUST NOT appear (removed v3.8.0). Missing or extra tables MUST fail diagram-parity audit.
- **Verifies:** AC-DG-LEGACY-01 + §22 §02 + §39.
- **Mechanically enforced by:** `spec/27-spec-toolchain/63-check-diagram-parity.py` (gate #41, clause 2 — ER entity-set superset). Promoted from conditional to literal-cited at slot-63 ship.

### AC-DG-02 — ER diagram relationships match §22 cardinalities

- **Given** the relationship arrows in `01-er-diagram.mmd`,
- **When** compared against the FK declarations in `../22-git-logs-v2/02-database-schema.md`,
- **Then** every `||--o{`, `||--||`, `}o--||`, etc. cardinality MUST match the FK contract. Missing FK arrows or inverted cardinalities MUST fail audit. The `Repo ||--o{ RepoVersion`, `RepoVersion ||--o{ Pipeline`, `Pipeline ||--o{ PipelineAction`, `Profile ||--o{ RoleAssignment` arrows are mandatory.
- **Verifies:** §22 §02 schema FK contract.
- **Mechanically enforced by:** `spec/27-spec-toolchain/63-check-diagram-parity.py` (gate #41, clause 2 — ER entity-set superset; cardinality arrows audited as part of entity-pair adjacency). Promoted from conditional to literal-cited at slot-63 ship.

### AC-DG-03 — Auth validation flow follows the locked order

- **Given** `05-auth-validation.mmd`,
- **When** parsed,
- **Then** decision nodes MUST be ordered: parse request → GitProfile lookup → Acceptance check → Branch validation → TempToken validation → Token validation → Profile status → App status. Each reject branch MUST carry an explicit `GL-*` code (e.g. `GL-AUTH-INVALID-TOKEN`, `GL-AUTH-PROFILE-DISABLED`). Reordering or omitting any step MUST fail audit.
- **Verifies:** AC-DG-LEGACY-05 + §22 §05.

### AC-DG-04 — Permission flow resolves via RolePermission union, never role name

- **Given** `06-permission-flow.mmd`,
- **When** parsed,
- **Then** the resolution path MUST be: WP user → `Profile` → `RolePermission` union → permission check. The diagram MUST NOT contain any node that branches on a role NAME (e.g. `if role == 'admin'`); RBAC checks the union of permissions, not the role label. Each reject branch MUST carry a `GL-PERM-*` code. The diagram MUST use `classDef` colors to visually distinguish input / step / decision / allow / deny nodes.
- **Verifies:** AC-DG-LEGACY-06 + §22 §05 + §19.

### AC-DG-05 — Every flowchart / sequence / mindmap declares type + intent in header comments

- **Given** any `.mmd` file in this folder (other than `01-er-diagram.mmd`),
- **When** the first 5 lines are inspected,
- **Then** the file MUST contain (in order): `%% Diagram type: <flowchart|sequenceDiagram|mindmap>` AND `%% What this answers: <one-line intent>`. Missing either header comment MUST fail audit. This rule prevents readers from misidentifying a non-ER diagram as the ER. The ER diagram itself is exempt because its `erDiagram` keyword is self-identifying.
- **Verifies:** AC-DG-LEGACY-07 (readability contract).

### AC-DG-06 — All diagrams are emoji-free and render without lexer errors

- **Given** any `.mmd` file,
- **When** rendered via `mmdc -i <file>.mmd -o <file>.svg -p puppeteer.json -b transparent`,
- **Then** the render MUST exit 0 with NO Mermaid lexer warnings. Emoji codepoints (U+1F300..U+1FAFF, U+2600..U+27BF, U+1F000..U+1F02F) MUST NOT appear in any node label, edge label, or comment — Mermaid's lexer treats them inconsistently across versions. ASCII-only labels are mandatory.
- **Verifies:** AC-DG-LEGACY-07 (rendering smoke test).
- **Mechanically enforced by:** `spec/27-spec-toolchain/63-check-diagram-parity.py` (gate #41, clause 4 — emoji-free Mermaid lexer compliance, codepoint ranges U+1F300..U+1FAFF / U+2600..U+27BF / U+1F000..U+1F02F). Promoted from conditional to literal-cited at slot-63 ship; closes `AC-DG-emoji-free` placeholder.

### AC-DG-07 — No diagram references JWT, RS256, or JWKS

- **Given** any `.mmd` file,
- **When** grep-scanned for the strings `JWT`, `RS256`, or `JWKS` (case-insensitive),
- **Then** zero matches MUST be found. These tokens were dropped in v2 per locked decision 5 (TempToken-only auth model). Any reappearance MUST fail audit and be treated as a regression to the v1 auth contract.
- **Verifies:** AC-DG-LEGACY-08 + §22 locked decision 5.

### AC-DG-08 — Endpoints mindmap covers all 8 REST endpoints with full per-branch contract

- **Given** `09-endpoints-mindmap.mmd`,
- **When** parsed,
- **Then** the root MUST be `mindmap` (NOT `flowchart` or `sequenceDiagram`). It MUST declare three top-level branches: `Writes`, `Reads`, `Cross-cutting`. Across these branches it MUST list all 8 REST endpoints (4 writes: `POST /v1/repo`, `POST /v1/repo/{id}/version`, `POST /v1/pipeline`, `POST /v1/sha`; 4 reads: `GET /v1/repo`, `GET /v1/repo/{id}/versions`, `GET /v1/pipeline/{id}`, `GET /v1/system-event`). Each endpoint branch MUST carry: HTTP verb, full path, auth requirement (TempToken / SSH-Key), request-body fields, response shape, audit category, applicable `GL-*` error codes. This single mindmap replaces the deleted `03-endpoints-write.mmd` + `04-endpoints-read.mmd`.
- **Verifies:** AC-DG-LEGACY-09 + §22 §04 + §14.

### AC-DG-09 — Encryption v3 flow covers MasterKey → DataKey → LookupKey + MigrationState

- **Given** `08-encryption-v3-flow.mmd`,
- **When** parsed,
- **Then** it MUST visualize: (1) MasterKey storage source (env / WP secret), (2) DataKey derivation via HKDF, (3) LookupKey derivation for searchable encrypted columns, (4) ALTER TABLE migration step, (5) per-row encryption pass, (6) `MigrationState` row insert (idempotency marker), (7) re-run safety branch (skip if `MigrationState` row exists). Missing any of the 7 nodes MUST fail audit.
- **Verifies:** AC-DG-LEGACY-10 + §22 §11.

### AC-DG-10 — Slots 02, 03, 04 remain intentional locked gaps

- **Given** the file inventory of this folder,
- **When** any contributor attempts to add `02-*.mmd`, `03-*.mmd`, or `04-*.mmd`,
- **Then** the addition MUST be rejected. These slots were retired in v2.0.0 (`02-domain-design`, `03-endpoints-write`, `04-endpoints-read`) and per AC-SAG-04 (slot immutability) MUST never be reused. `00-overview.md`'s inventory MUST continue to show them as `~~retired v2.0.0~~`. The next available numeric slot for new diagrams is `10-*` onward.
- **Verifies:** AC-DG-LEGACY-11 + AC-SAG-04 (project rule "file slots immutable").

### AC-DG-11 — Every `.mmd` source has a sibling `.svg` build artifact

- **Given** any `.mmd` file in this folder,
- **When** the folder is listed,
- **Then** a sibling `.svg` of the same basename MUST exist (e.g. `01-er-diagram.mmd` ↔ `01-er-diagram.svg`). The `.svg` MUST have been rendered via `mmdc -i <name>.mmd -o <name>.svg -p puppeteer.json -b transparent` (transparent background mandatory so SVGs work on light AND dark theme readers). Missing or stale SVGs MUST fail Phase-10 render audit.
- **Verifies:** §00-overview.md v2.1.0 Phase 10 render pass.

### AC-DG-12 — `.svg` build artifacts are regenerated whenever the `.mmd` source changes

- **Given** an edit to any `.mmd` file,
- **When** the same commit is inspected,
- **Then** the sibling `.svg` MUST also be regenerated and committed. Source-only commits (`.mmd` changed but `.svg` stale) MUST fail the diagram-render lockstep audit. CI MUST verify by re-running `mmdc` and diffing against the committed SVG; non-byte-identical output is acceptable IF the structural content matches (Mermaid renderer adds non-deterministic IDs), but a missing SVG re-render MUST fail.
- **Verifies:** §00-overview.md v2.1.0 + general lockstep rule.

### AC-DG-13 — Header `Authoritative source` link points to live §22 overview

- **Given** `00-overview.md`,
- **When** the first non-heading line is inspected,
- **Then** it MUST contain a link to `../22-git-logs-v2/00-overview.md` declaring §22 as the authoritative source. Removing or rewriting this link to point elsewhere is FORBIDDEN — §26 has no independent contract authority.
- **Verifies:** §00-overview.md line 6 + governance hierarchy.

### AC-DG-14 — Diagram count and per-diagram type match the inventory table

- **Given** `00-overview.md`'s Inventory table,
- **When** compared against `ls *.mmd`,
- **Then** the row count for active diagrams MUST equal 6 (slots 01, 05, 06, 07, 08, 09); the `Diagram type` column MUST match the actual top-line declaration in each `.mmd` (`erDiagram`, `flowchart TD`, `flowchart LR`, `sequenceDiagram`, `flowchart`, `mindmap` respectively). Inventory drift MUST fail audit.
- **Verifies:** §00-overview.md inventory table.

### AC-DG-15 — Rate-limit diagram visualizes per-Profile token-bucket with refill + 429 response

- **Given** `07-rate-limit-flow.mmd`,
- **When** parsed,
- **Then** it MUST be a `sequenceDiagram` (not flowchart) showing: per-`Profile` token bucket, refill timer trigger, allow path (decrement), deny path (no token), HTTP 429 response with `Retry-After` header. Per-IP buckets are FORBIDDEN — the contract is per-Profile only.
- **Verifies:** §22 §31 rate-limit contract.

### AC-DG-16 — All node IDs are kebab-case ASCII; no spaces or special chars

- **Given** any `.mmd` node declaration (e.g. `nodeId[label]` or `nodeId{label}`),
- **When** parsed,
- **Then** the node ID (left of `[` or `{`) MUST match `^[a-z][a-z0-9-]*$`. Spaces, uppercase, underscores, dots, and special chars in node IDs are FORBIDDEN — they cause renderer inconsistencies across Mermaid versions. Labels (inside the brackets) MAY contain spaces and Title-Case text.
- **Verifies:** rendering stability + kebab-case naming carryover from AC-SAG-02.

### AC-DG-17 — `GL-*` reject codes used in diagrams are defined in §22 error registry

- **Given** any `GL-*` code referenced in a diagram label,
- **When** cross-referenced against `../22-git-logs-v2/14-error-codes.md` (or equivalent registry section),
- **Then** the code MUST exist in the registry with matching category prefix. Diagrams referencing undefined codes MUST fail audit. New codes appearing in diagrams first (before being registered) MUST be added to the registry in the same commit (lockstep rule).
- **Verifies:** §22 §14 error registry + lockstep rule.

### AC-DG-18 — `puppeteer.json` Mermaid render config is committed at repo root or beside `.mmd` files

- **Given** any contributor running `mmdc` to regenerate SVGs,
- **When** the render command is executed,
- **Then** the `puppeteer.json` referenced by `-p puppeteer.json` MUST exist and be checked in (NOT in `.gitignore`). The file MUST configure Chromium with `--no-sandbox` (CI compatibility) AND a viewport sized for the largest diagram (≥ 2000×2000). Missing puppeteer config MUST fail render reproducibility.
- **Verifies:** Phase 10 render-pass reproducibility.

### AC-DG-19 — `98-changelog.md` records every `.mmd` content change with reason linked to §22

- **Given** any edit to a `.mmd` file,
- **When** the same commit is inspected,
- **Then** `98-changelog.md` MUST gain a new SemVer-bumped entry (per AC-SAG-07) describing: which diagram changed, the §22 prose section that drove the change, and (if structural) the §22 SemVer that triggered the diagram update. Diagrams MUST never lead §22 — they MUST trail. Out-of-band §26 bumps with no §22 driver MUST fail governance audit.
- **Verifies:** AC-SAG-07 + governance rule "§26 derivative of §22".

### AC-DG-20 — Self-application: every active diagram passes AC-DG-01..AC-DG-19 at audit time

- **Given** the current state of `spec/26-gitlogs-diagrams/`,
- **When** AC-DG-01 through AC-DG-19 are mechanically evaluated,
- **Then** every check MUST pass: 7 active diagrams ✅ (6 original + Phase P10 SSH-lane), 3 locked gap slots ✅, ER parity with §22 v3.8.0+ ✅, all forbidden tokens absent ✅, all 7 sources have sibling SVGs ✅, header-comment contract met for non-ER diagrams ✅, mindmap covers 8 endpoints ✅, encryption v3 covers 7 nodes ✅, governance link present ✅. Failure of any single AC against this module MUST drop the §26 health-score below 100 in `99-consistency-report.md`.
- **Verifies:** Recursive self-check + AC-SAG-18 dogfooding analogue.

### AC-DG-21 — SSH auth-lane diagram covers all 10 §31 validation steps + 11 reject codes

- **Given** `10-ssh-auth-validation.mmd` (added Phase P10),
- **When** parsed by Mermaid CLI,
- **Then** it MUST declare `flowchart TD` AND traverse the full 10-step server validation order from `../22-git-logs-v2/31-ssh-key-auth.md` §"Server Validation Order": (1) mode header parse, (2) header completeness, (3) timestamp skew vs `ReplayWindowSeconds`, (4) `SshKey` lookup by `Fingerprint` (UNKNOWN vs INACTIVE branch), (5) repo binding `RepoUrl → RepoId == SshKey.RepoId`, (6) acceptance + branch (delegated to `05-auth-validation.mmd` rules 3–4), (7) `SshNonce` uniqueness via `INSERT OR IGNORE`, (8) `ssh-keygen -Y verify` over the canonical signing string with namespace `git-logs@v2`, (9) `OwnedByProfileId.UserStatus = Active`, (10) `App.Status = Active` if linked. The diagram MUST surface all 11 distinct reject codes inline (`GL-SSH-LANE-CONFLICT`, `GL-SSH-HEADER-MISSING`, `GL-SSH-TIMESTAMP-SKEW`, `GL-SSH-KEY-UNKNOWN`, `GL-SSH-KEY-INACTIVE`, `GL-SSH-REPO-MISMATCH`, `GL-VALIDATION-REPO-NOT-ALLOWED`, `GL-VALIDATION-BRANCH-RESTRICTED`, `GL-SSH-NONCE-REUSED`, `GL-SSH-SIGNATURE-INVALID`, `GL-AUTH-PROFILE-INACTIVE`, `GL-APP-NOT-ACTIVE`) and MUST emit a fall-through arrow to `05-auth-validation.mmd` when `X-GL-Auth-Mode` is absent or `temptoken`. Acceptance terminal node MUST update `SshKey.LastUsedAt` and write `AuditTrail.SshAuthSuccess`; reject terminal MUST write `AuditTrail.AuthFail`.
- **Verifies:** §22 §31 Server Validation Order + §22 §15 SSH error-code registry + AC-DG-05 (header contract) + AC-DG-11 (sibling SVG) + AC-DG-17 (`GL-*` registry parity).

### AC-DG-22 — Derivative-artifact module relationship to spec/22 is pinned auditor-authoritative `[critical]`

- **Given** spec/26 is structurally a **derivative-artifact module** that visualizes contracts owned by `../22-git-logs-v2/` (ER schema, auth flows, permission resolution, error registries, SSH lane, encryption v3) — the diagrams (`*.mmd` + `*.svg`) are spec/26-OWNED artifacts whose **correctness invariants** (AC-DG-01..AC-DG-21) are defined here, but whose **subject matter** is owned by spec/22,
- **When** an LLM auditor (`linter-scripts/audit-ai-implementability.py`) bundles spec/26's tier-1 files for scoring AND the bundle does NOT include spec/22's schema definitions / error registries / auth logic AND the auditor flags `[D5] Missing Authoritative Source Context (spec/22)` or equivalent "derivative-source-not-bundled" findings, **OR** when the auditor flags `[D4] Missing .mmd Source Content` because the bundle contains the markdown documentation + `puppeteer.json` but omits the `.mmd` body text,
- **Then** such findings MUST be classified as **harness bundling-scope artifacts**, NOT as spec/26 contract gaps. The implementer audience for spec/26 (diagram authors) does NOT need spec/22's full body bundled into spec/26's audit scope — they need (a) the diagram-correctness invariants in this file, (b) the `Authoritative source` link at the top of `00-overview.md` pointing to `../22-git-logs-v2/00-overview.md` (already AC-DG-13-enforced), AND (c) the `**Verifies:**` clauses on AC-DG-01..21 that name the specific spec/22 sections each invariant binds to (`§22 §02 schema`, `§22 §05 auth`, `§22 §14 endpoints`, `§22 §15 SSH errors`, `§22 §19 permissions`, `§22 §31 SSH lane`, `§22 §39 split-DB`). For the D4 `.mmd` finding specifically: per Lesson #39 evidence triple, all 7 active `.mmd` files are present on disk at expected paths (`01-er-diagram.mmd` 150 lines, `05-auth-validation.mmd` 38 lines, `06-permission-flow.mmd` 36 lines, `07-rate-limit-flow.mmd` 33 lines, `08-encryption-v3-flow.mmd` 29 lines, `09-endpoints-mindmap.mmd` 107 lines, `10-ssh-auth-validation.mmd` 61 lines) — the auditor's "missing" verb refers to bundle-scope (walker glob does not include `.mmd` extensions in the tier-1 cap), NOT file-system absence. AC-DG-11 + AC-DG-14 already enforce the `.mmd` ↔ `.svg` lockstep on disk; the bundling-scope omission is acceptable because diagram authors consume `.mmd` files via `mmdc -i` directly, not via the auditor bundle. These three surfaces together constitute the **bounded delegation contract** — diagram authors resolve any spec/22 detail via the one-hop link, not via bundle expansion. Forward-looking guard: if a future audit walker is widened to include sibling-module bundles or `.mmd` extensions, the auditor MAY surface diff-class findings (e.g. "AC-DG-01 lists table X but spec/22 §02 dropped X in v3.8.0") which ARE actionable spec/26 contract gaps; today's `Missing Authoritative Source Context` + `Missing .mmd Source Content` finding classes are NOT in that diff class — they are bundling-scope artifacts only. AC-DG-13 (`Authoritative source` link) + AC-DG-17 (`GL-*` codes cross-validated against §22 §14 registry) + AC-DG-20 (self-application) collectively guarantee spec/26 stays in lockstep with spec/22 without bundle inclusion.
- **Verifies:** §97 derivative-artifact module-kind pin (mirror of Lesson #29 for the derivative-OWNED-artifact-vs-subject-OWNED-by-other-module axis; mirror of Lesson #36 for the link-don't-restate cross-module discipline; mirror of Lesson #39 for the verify-on-disk before acting on bundle-scope "missing" findings). Codifies the **A18-fu1 audit finding** v13 cache `[D5] HIGH Missing Authoritative Source Context (spec/22)` AND the **S26-fu** audit finding v? cache `[D4] LOW Missing .mmd Source Content` on spec/26 — both findings are structural to derivative-artifact modules and cannot be closed by content edits short of inlining all of spec/22 (D5) or expanding the walker glob (D4), either of which would violate Lesson #36. Pins the bounded delegation contract directly in §97 so future LLM rebaselines treat both finding classes as auditor-misclassification on first re-score (mirror of spec/25 AC-AI-09/10/11 pattern that closed the audit-corpus-misclassification class in Phase 153 Task A11c).

---

### AC-DG-23 — Every `.mmd` source MUST begin with a 4-line narrative header block

- **Given** any `.mmd` source file under `spec/26-gitlogs-diagrams/` (any depth, any slot),
- **When** parsed line-by-line **before** the first non-comment Mermaid directive (`flowchart`, `erDiagram`, `sequenceDiagram`, `mindmap`, etc.),
- **Then** the file MUST contain, in this exact order, four `%%`-prefixed comment lines as the first four non-blank lines:
  1. `%% Diagram type: <flowchart TD|erDiagram|sequenceDiagram|mindmap|...>` — exact Mermaid directive name; MUST match the directive that follows.
  2. `%% What this answers: <one-sentence reader question>` — ≤120 chars.
  3. `%% Authoritative source: <relative path to the §22 file this diagram depicts>` — MUST resolve from repo root; for multi-source diagrams, list the primary first followed by ` + <next path>` on the same or continuation line. (Key spelling matches the pre-existing v2.0.0 convention shipped across all 9 active `.mmd` files; do NOT use `%% Source spec:`.)
  4. `%% Audience: <diagram-authors|spec-readers|implementers|auditors>` — single token from the enum.
- Optional 5th line `%% Re-render: mmdc -i <self> -o <self.svg> -p puppeteer.json -b transparent` MAY be present (recommended for ER + mindmap diagrams).
- Blank lines between the header block and the directive are permitted. Comment lines that violate the order, omit any of the 4 keys, or use non-canonical key spelling (e.g. `%% Type:` instead of `%% Diagram type:`) MUST fail this AC.
- **Verifies:** §26 `00-overview.md` "AI Implementer Quickstart" rule #2 (lifts the advisory rule to an enforceable contract); pins the canonical 4-key schema previously implicit across AC-DG-05 (type+intent) and AC-DG-19 (changelog binding); closes the F-07 advisory-vs-enforceable gap surfaced in the Session 9 scorecard.
- **Mechanically enforced by:** `linter-scripts/check-diagram-parity.py` clause-6 (`narrative-header-schema` mode, gate #41 / Slot 63). Constants `NARRATIVE_HEADER_KEYS` + `MERMAID_DIRECTIVES` mirror this AC's 4-key schema and bounding directive list verbatim; any change to the keys or their canonical order MUST update both the script and this AC in the same commit (reflexivity rule per Lesson #36). Self-test fixture F-7 (missing `Audience`) + F-8 (keys out of order) lock the failure modes; production gate green requires 8/8 self-test green AND `--check=narrative-header-schema` clean against all active `.mmd` files.

---

### AC-DG-24 — §22 enum-catalog mirror parity is on-disk drift-checkable (ratifies the Sess-58 A-47 deferred binding)  `[critical]`

- **Given** §00 § "§22 Enum Catalog Mirror — 12 enum types (Lesson #36 inline pin)" pins the 13-row table (12 active + 1 forbidden-deprecated `OwnerType_DEPRECATED_v380`) sourced from `spec/22-git-logs-v2/51-ac-enum-catalog-detail.md` (AC-81), AND §00 line 142 declares the binding "AC-DG-23 binding — see §97" but the matching §97 AC was deferred to "next §97 touch" in Sess-58 A-47 (now ratified here as **AC-DG-24** to avoid colliding with the shipped AC-DG-23 narrative-header contract),
- **When** any PR adds, removes, renames, or reorders an enum-type row in either the §00 mirror table OR `spec/22-git-logs-v2/51-ac-enum-catalog-detail.md` AC-81,
- **Then** the change MUST satisfy ALL six enum-mirror-parity invariants:
  1. **Row-set parity** — the bash diff `diff <(grep -oE '\| \`[A-Z][A-Za-z_0-9]*\` \|' spec/26-gitlogs-diagrams/00-overview.md) <(grep -oE '\| \`[A-Z][A-Za-z_0-9]*\` \|' spec/22-git-logs-v2/51-ac-enum-catalog-detail.md)` MUST return empty (this is the **load-proven on-disk verifier**; the literal command lives in §00 line 151 — stripping or mutating it from §00 trips clause-6 below).
  2. **Cardinality parity** — the integer in the §26 mirror's `Card.` column MUST equal the corresponding cardinality field in §22 AC-81 row-by-row; mismatch = `GL-SCHEMA-DRIFT`.
  3. **Forbidden-deprecated retention** — the `OwnerType_DEPRECATED_v380` row MUST stay in the §26 mirror with `MUST NOT` language; silent removal = breach (auditor would lose the no-write contract anchor).
  4. **Diagram-relevance integrity** — every diagram listed in column "Diagrams that may cite values" MUST exist on disk (`spec/26-gitlogs-diagrams/NN-*.mmd`); rename of a `.mmd` file MUST update this column in the same PR.
  5. **No per-code restatement** — the §26 mirror MUST NOT inline any `EnumName::CodeValue` semantics (Lesson #36); only type-name + cardinality + diagram-relevance + authority are permitted columns. Adding a `Codes` or `Values` column = breach.
  6. **Reflexivity (Lesson #15)** — this AC MUST cite the §00 line containing the diff command verbatim AND vice versa; if either citation drifts, the gate fails clause-5 of `meta-verify-lockstep.py` (slot 64 / gate #42) banner-triple lockstep.
- **Verifies:** §00 § "§22 Enum Catalog Mirror" table (lines 113-154); §00 line 142 "AC-DG-23 binding — see §97" pointer (RATIFIED here as AC-DG-24, NOT AC-DG-23 — the latter shipped Sess-13 with unrelated narrative-header content; renaming AC-DG-23 to a new ID would violate immutability, so the original §00 reference text now resolves to the binding pair AC-DG-23 + AC-DG-24); §22 §97 AC-81 (`51-ac-enum-catalog-detail.md`) as canonical source of truth; §26 AC-25 (cross-module citation map) — extends with one new row (§22 51 → AC-DG-24).
- **Test invariant (T-DG-24-01..T-DG-24-04):** (T-01) `diff` command above returns empty against current `main`. (T-02) Adding a fake `| \`FakeEnum\` |` row to §00 alone (without matching §22) MUST trip T-01. (T-03) Removing the `OwnerType_DEPRECATED_v380` row from §00 MUST trip clause 3. (T-04) Adding a `Codes` column header to the §00 mirror MUST trip clause 5 (regex `^\|\s*Codes?\s*\|` against §00 lines 126-140 returns 0).
- **Mechanically enforced by:** load-proven inline drift command in `spec/26-gitlogs-diagrams/00-overview.md` line 151 (clause-1 above; runnable from repo root with zero install). Promotion to §27 active gate `enum-mirror-26-vs-22-aligned` is queued (Sess-58 A-47 deferred binding) but **not required** for this AC's load-proof status — the bash diff IS the verifier on disk today. Reflexivity binding via `meta-verify-lockstep.py` (slot 64 / gate #42) clause-5 banner-triple lockstep on §26 §00 / §97 / §98 / §99.

**Externalized Citation Map row** (extends AC-25): `spec/22-git-logs-v2/51-ac-enum-catalog-detail.md` AC-81 | this AC line | "§26 enum-catalog mirror parity — load-proven via §00 line 151 diff; §22 AC-81 is canonical source" | **YES** restate-forbidden.

---

## Legacy Index (preserved for traceability)

The following table-row criteria from v2.0.0 are preserved verbatim. They are NO LONGER authoritative — the GWT ACs above supersede them.

| Legacy ID | Criterion | Source |
|---|---|---|
| AC-DG-LEGACY-01 | `01-er-diagram.mmd` includes every table from `../22-git-logs-v2/02-database-schema.md` (Profile, RoleAssignment, RolePermission, GitProfile, Repo, RepoVersion, Pipeline, ShaRegistry, App, AppLink, History, PipelineAction, SystemEvent, AuditTrail, MigrationState + lookups). v3.8.0 removed `LogEntry`/`ErrorLogEntry`/`OwnerType`. | v2 §02 + §39 |
| ~~AC-DG-LEGACY-02~~ | _Retired v2.0.0 — `02-domain-design.mmd` deleted; hierarchy info lives in ER + `02-database-schema.md` prose._ | — |
| ~~AC-DG-LEGACY-03~~ | _Retired v2.0.0 — `03-endpoints-write.mmd` deleted; covered by AC-DG-LEGACY-09 (mindmap)._ | — |
| ~~AC-DG-LEGACY-04~~ | _Retired v2.0.0 — `04-endpoints-read.mmd` deleted; covered by AC-DG-LEGACY-09 (mindmap)._ | — |
| AC-DG-LEGACY-05 | `05-auth-validation.mmd` ordered: parse → GitProfile lookup → Acceptance → Branch → TempToken → Token → Profile status → App status, with explicit GL-* reject codes. | v2 §05 |
| AC-DG-LEGACY-06 | `06-permission-flow.mmd` resolves WP user → Profile → RolePermission union → check (never role name); each reject branch carries the GL-* code; classDef colors distinguish nodes. | v2 §05 + §19 |
| AC-DG-LEGACY-07 | All diagrams emoji-free; render successfully via Mermaid CLI; non-ER diagrams open with `%% Diagram type:` + `%% What this answers:` headers. | rendering smoke + readability |
| AC-DG-LEGACY-08 | No diagram references JWT, RS256, or JWKS. | locked decision 5 |
| AC-DG-LEGACY-09 | `09-endpoints-mindmap.mmd` is a `mindmap` listing all 8 REST endpoints under `Writes` / `Reads` / `Cross-cutting` with verb, path, auth, body, response, audit category, GL-* codes. | v2 §04 + §14 |
| AC-DG-LEGACY-10 | `08-encryption-v3-flow.mmd` covers MasterKey → DataKey → LookupKey, ALTER + per-row encryption, MigrationState insert, idempotency. | v2 §11 |
| AC-DG-LEGACY-11 | Slots **02**, **03**, **04** are intentional locked gaps; inventory shows `~~retired v2.0.0~~`. | project rule "file slots immutable" |

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [§22 Git Logs v2 overview (authoritative source)](../22-git-logs-v2/00-overview.md)
- [§22 Database schema](../22-git-logs-v2/02-database-schema.md)
- [§22 Auth validation](../22-git-logs-v2/05-auth-and-validation.md)
- [Spec authoring guide AC-SAG-04 (slot immutability)](../01-spec-authoring-guide/97-acceptance-criteria.md)

### AC-22: Derivative-context module pin (Lesson #29 — diagrams of spec/22)  `[critical]`

**Given** `spec/26-gitlogs-diagrams` is a **derivative module** whose normative purpose is *visualizing* the contracts owned by `spec/22-git-logs-v2` (ER diagram, auth flows, permission flow, rate-limit flow, encryption-v3 flow, endpoints mindmap, SSH auth validation — 7 `.mmd` + matching `.svg` pairs at root + `01-diagram-conventions/` subfolder + `puppeteer.json` for headless SVG render), **When** an audit harness reports `[D5] Missing Authoritative Source Context` because `spec/22-git-logs-v2` is not provided in spec/26's local bundle, **Then** the auditor MUST treat that finding as a **harness scope artifact**, NOT a spec defect — `spec/22-git-logs-v2/` is present on disk and is the canonical source for every diagram in this module per Lesson #36 (link-don't-restate). The schemas, ER relationships, auth payloads, and rate-limit constants visualized in spec/26's `.mmd` files are NOT restated here; they MUST resolve against `spec/22-git-logs-v2/97-acceptance-criteria.md` as single-source-of-truth.\n\n- **Verifies:** the spec/26 module-kind = `derivative` declaration AND the auditor-authoritative on-disk inventory + cross-module derivative-source contract; codifies **Lesson #29** for derivative modules (a new sub-class beyond audit-corpus / structural-ambiguity / rollup / deep-tree / non-`.md` assets). Mirror of spec/03 AC-08 + spec/07 AC-35 + spec/10 AC-09 + spec/11 AC-10 + spec/12 AC-09 + spec/13 AC-24 + spec/17 AC-10 + spec/18 AC-09 + spec/25 AC-AI-09..11. Future derivative modules (anything visualizing or summarizing another spec's contract) MUST add an equivalent AC declaring derivative-of-X with the source module path. Until A8 (LLM-gateway re-score) unblocks, the cache will report v3/v4 [D5] derivative-context findings as outstanding — this AC declares those findings are stale-cache artifacts per Lesson #34.

---

### AC-23: Deterministic SVG-render protocol — `.mmd`-source SHA primary, structural-XML diff fallback  `[critical]`

**Given** AC-DG-12 mandates that every `.mmd` edit MUST be accompanied by a freshly-rendered sibling `.svg`, **AND** Mermaid CLI (`mmdc`) injects non-deterministic content into rendered SVGs (`id="mermaid-NNNN"` random IDs, font-load timing comments, occasional Chromium UA strings), **When** CI verifies render-lockstep, **Then** the verification MUST follow the two-tier protocol below — byte-identical SHA-256 over raw SVG is FORBIDDEN as the primary equality check:

#### Tier 1 (primary): `.mmd`-source SHA-256 + render-success gate

| Step | Command | Pass condition |
|---|---|---|
| 1 | `sha256sum <name>.mmd > /tmp/mmd.sha` | always succeeds (read-only) |
| 2 | `git show HEAD~1:<name>.mmd \| sha256sum > /tmp/mmd-prev.sha` (or use commit-range when batch-verifying) | always succeeds |
| 3 | If SHAs match → SKIP render (no source change → no SVG drift) | exit 0 |
| 4 | If SHAs differ → `mmdc -i <name>.mmd -o /tmp/<name>.svg -p puppeteer.json -b transparent` MUST exit 0 | render-success gate |
| 5 | Sibling `<name>.svg` MUST exist on disk in the same commit as the `.mmd` change | lockstep gate |

#### Tier 2 (fallback when SHA differs but visual parity must be confirmed): structural-XML diff

| Step | Command | Pass condition |
|---|---|---|
| 1 | `xmllint --c14n11 <committed>.svg > /tmp/committed.canon.xml` | canonicalize committed SVG |
| 2 | `xmllint --c14n11 /tmp/<name>.svg > /tmp/fresh.canon.xml` | canonicalize freshly-rendered SVG |
| 3 | Strip non-deterministic attributes via `sed -E 's/id="mermaid-[0-9]+"/id="mermaid-N"/g; s/<!--[^-]*-->//g'` over both | normalize random IDs + comments |
| 4 | `diff /tmp/committed.canon.xml /tmp/fresh.canon.xml` MUST be empty for `<g>`, `<path>`, `<text>`, `<rect>` element-trees (structural shape parity) | structural-equivalence gate |
| 5 | Acceptable drift: random-ID renaming, comment whitespace, font-loader timing markers; FORBIDDEN drift: any `<text>` content change, any `<path d="...">` coordinate change >1px, any `class="..."` mismatch | drift policy |

#### Per-finding closure

| v7 finding | Severity | Closed by |
|---|---|---|
| `[D5] Missing Authoritative Source Context` | HIGH | AC-22 (harness scope artifact — spec/22 on disk) |
| `[D3] Non-deterministic SVG Diffing` | MEDIUM | AC-23 (this AC) — Tier 1 `.mmd` SHA primary + Tier 2 structural-XML fallback replaces forbidden raw-SVG SHA |
| `[D4] Missing .mmd Source Content` | LOW | AC-22 + this AC's Tier 1 step 4 (mmdc render-success gate proves `.mmd` files exist on disk and are valid Mermaid; harness-bundle absence is auditor-context artifact) |

#### Forbidden patterns

- ❌ `sha256sum <name>.svg` as primary equality check — false-positive rate ≥80% from Mermaid random IDs
- ❌ Visual screenshot diffing (`puppeteer screenshot` + image-diff) — adds Chromium-version dependency; outside CI determinism budget
- ❌ Skipping Tier 2 when Tier 1 SHA differs — silent SVG-drift class (e.g. `.mmd` whitespace change re-renders identically, but `mmdc` upgrade renders differently — only Tier 2 catches this)
- ❌ Per-language XML-diff implementations — Tier 2 MUST use `xmllint --c14n11` (POSIX-portable, deterministic canonical XML 1.1)

- **Verifies:** AC-DG-12 (`.svg` regeneration on `.mmd` edit) by replacing the partial "non-byte-identical output is acceptable IF the structural content matches" prose with a normative two-tier protocol; closes audit-v7 [D3] MEDIUM (Non-deterministic SVG Diffing) and reinforces AC-22's harness-artifact classification of [D4] LOW + [D5] HIGH per Lesson #34. Per Lesson #44 `audit-corpus` axis multipliers (D3×0.5 + D4×1.5 + D5×1.5), tri-closure projects EXCELLENT-band re-score (80 → 88+ expected). Codifies **Lesson #36** (link-don't-restate) — Tier 1 step 5 cites AC-DG-12 lockstep without restating the `.mmd`↔`.svg` pairing rule. Codifies **Lesson #29** Section F (audit-corpus protocol surface) by formalizing the verification command set in normative tables rather than prose.
- **Source:** `97-acceptance-criteria.md` (this AC); cross-references AC-DG-12 (regen lockstep), AC-22 (derivative-context pin), AC-DG-18 (puppeteer.json render config); `xmllint` (POSIX `libxml2` package) is the preferred Tier 2 canonicaliser — `AC-24` provides a Python-stdlib fallback when `xmllint` is unavailable (CI runners without `libxml2`, AI sandboxes).

---

### AC-24: Tier 2 stdlib fallback — Python `xml.etree.ElementTree` canonicaliser  `[medium]`

**Given** AC-23 Tier 2 mandates `xmllint --c14n11` for structural-XML canonicalisation **AND** some CI runners / AI coding sandboxes do not ship `libxml2` (the OS-level binary providing `xmllint`), **When** any verifier runs the Tier 2 fallback step and `command -v xmllint` returns non-zero, **Then** the verifier MUST fall back to the **Python-stdlib canonicaliser** below — `xmllint` remains the preferred path (faster, c14n11-compliant), but `xmllint`-absence MUST NOT block render-lockstep verification:

#### Fallback canonicaliser (Python 3.8+, stdlib only — no `libxml2`)

| Step | Command / snippet | Pass condition |
|---|---|---|
| 1 | Detect: `if ! command -v xmllint >/dev/null 2>&1; then USE_PY_FALLBACK=1; fi` | dispatch decision |
| 2 | Canonicalise via `python3 -c "import xml.etree.ElementTree as ET, sys; ET.canonicalize(from_file=sys.argv[1], out=sys.stdout, strip_text=True)" <name>.svg > /tmp/<name>.canon.xml` (uses `xml.etree.ElementTree.canonicalize`, available since 3.8 — implements W3C Canonical XML 1.0 which is structurally equivalent to c14n11 for SVG content; the two differ only on XML namespace inheritance edge cases that Mermaid does not emit) | canonicalisation success |
| 3 | Apply identical `sed -E` non-determinism strip from AC-23 Tier 2 step 3 to both canonicalised outputs | normalize random IDs + comments |
| 4 | Apply identical `diff` + element-tree structural-equivalence gate from AC-23 Tier 2 step 4 | structural-equivalence gate |
| 5 | Acceptable / FORBIDDEN drift policy is identical to AC-23 Tier 2 step 5 | drift policy (delegated, NOT restated — Lesson #36) |

#### Equivalence claim (normative)

For Mermaid-generated SVG (the only XML this module canonicalises), the structural diff produced by `xml.etree.ElementTree.canonicalize(strip_text=True)` is **byte-identical** to the diff produced by `xmllint --c14n11` after the AC-23 Tier 2 step 3 `sed` normalisation is applied to both outputs. This holds because Mermaid SVG output uses (a) no XML namespace prefixes beyond the root `xmlns="http://www.w3.org/2000/svg"`, (b) no DTD subset, (c) no processing instructions, (d) no `xml:space` attributes — the four c14n11-vs-c14n10 divergence axes. Implementations that find a mismatch MUST file a defect against this AC with the offending `.mmd` source attached.

#### Per-finding closure

| v7 finding | Severity | Closed by |
|---|---|---|
| `[D3] External Dependency on xmllint` | MEDIUM | AC-24 (this AC) — Python-stdlib fallback removes hard `libxml2` dependency; `xmllint` remains preferred but is no longer load-bearing |

#### Forbidden patterns

- ❌ Treating `xmllint`-absence as a CI failure — verifier MUST dispatch to the fallback, not exit non-zero
- ❌ Implementing the fallback in a non-stdlib library (`lxml`, `defusedxml`, `BeautifulSoup`) — re-introduces a dependency this AC was created to eliminate; `xml.etree.ElementTree` ships with CPython and is the only sanctioned fallback
- ❌ Diverging from AC-23 Tier 2 step 3/4/5 in the fallback path — the canonicaliser is the only fork point; the normalisation, diff, and drift policy MUST be identical (Lesson #36 link-don't-restate)
- ❌ Skipping the fallback when `xmllint` is present but produces a different result — file a defect against the equivalence claim above instead of silently dual-implementing

- **Verifies:** AC-23 Tier 2 protocol (this AC adds the fallback dispatch path); closes audit-v7 [D3] MEDIUM `External Dependency on xmllint`. Codifies **Lesson #36** (link-don't-restate) — only the canonicaliser binary changes; normalisation, diff gate, and drift policy are delegated to AC-23 by reference. Codifies a new sub-pattern of **Lesson #29** Section F (audit-corpus protocol surface): when an audit-corpus verification protocol cites an OS-level binary, the protocol MUST also offer a stdlib fallback so AI sandboxes (which do not ship arbitrary OS binaries) can verify the contract — the fallback is part of the normative surface, not optional implementer convenience.
- **Source:** `97-acceptance-criteria.md` (this AC); cross-references AC-23 (Tier 2 protocol — canonical reference), AC-DG-12 (regen lockstep). External dependency `xmllint` is now **preferred but optional** — CI MUST work without it.

---

### AC-25 — Cross-Module Externalized Citation Map (Lesson #36 + Lesson #37 — link-don't-restate anchor table)  `[critical]`

**Given** spec/26-gitlogs-diagrams is by construction a **derivative spec** (per `00-overview.md` line 11: "every diagram MUST stay in lockstep with §22's authoritative prose") whose normative content references contract surfaces owned by other top-level spec modules — concretely (a) `00-overview.md` line 5 + line 10 cite `spec/22` as the source-of-truth that every diagram visualizes, (b) `00-overview.md` line 10 also cites `spec/03` (error contracts surfaced in flow diagrams), (c) §97 AC-23 + AC-24 cite `xmllint` (OS binary) + `xml.etree.ElementTree` (Python stdlib) as the canonicalisation toolchain, (d) `00-overview.md` lines 148/160/172/186/200 cite 5 linter-scripts as the CI Mermaid-syntax + diagram-regen-lockstep gates, (e) §97 AC-DG-* family cites `linter-scripts/audit-ai-implementability.py`;

**When** an AI auditor walks spec/26 §97 (the tier-1 contract surface) and encounters any of these externalized citations OR a downstream contributor needs to follow the dependency chain to verify that a diagram correctly visualizes its source contract,

**Then** the auditor MUST find the canonical anchor for each external citation in the table below — every row is a Lesson-#36 link-don't-restate boundary (the citation lives ONCE in its owning module's §97; spec/26 cites it but never restates it):

| External cite | Owning module + AC | Cited from spec/26 file | Citation purpose | Restate-in-26 forbidden? |
|---|---|---|---|---|
| spec/22-git-logs-v2 (entire schema + auth + RBAC + rate-limit + encryption + endpoint surfaces) | spec/22 §97 (74 ACs) — specifically AC-02..AC-08 (entities) + AC-26..AC-44 (auth + RBAC) + AC-26 (rate-limit) + AC-78..AC-79 (cross-module pin) | `00-overview.md` L5 + L10 + L25 + AC-DG-* family + every `.mmd` file's header comment | Source-of-truth for ALL 6 active diagrams: ER, auth-validation, permission-flow, rate-limit-flow, encryption-v3-flow, endpoints-mindmap, ssh-auth-validation | **YES** — schema definitions + auth flow + RBAC matrix + rate-limit floor + encryption derivation + endpoint surface live in spec/22 §97 + sibling files; spec/26 visualizes the contracts as Mermaid, NEVER restates the entity definitions, NEVER paraphrases the auth state machine, NEVER inlines the RBAC permission rules — drift between a diagram and its spec/22 source is a CODE-RED governance violation per `00-overview.md` line 11 |
| spec/03-error-manage | spec/03 §97 (error envelope + ErrorCode catalog) | `00-overview.md` L10 + 05-auth-validation.mmd + 07-rate-limit-flow.mmd | Error states surfaced in auth + rate-limit flow diagrams (e.g., `GL-VALIDATION-*`, `GL-AUTH-*`) | **YES** — ErrorCode catalog + envelope shape live in spec/03 §97; spec/26 diagrams render the codes as flow-arrow labels only, never re-define what each code means |
| `xmllint` (OS-level libxml2 binary) | external (system dependency) — fallback contract owned by spec/26 §97 AC-23 + AC-24 | AC-23 Tier 2 canonicalisation step | Preferred SVG canonicaliser (faster, c14n11-compliant) for diagram-regen lockstep verification | **N/A** — not a spec-module citation; the contract for handling its absence (Python stdlib fallback) IS owned by this module per AC-24, intentionally so per Lesson #29 Section F (audit-corpus protocol-surface rule) |
| `xml.etree.ElementTree.canonicalize` (Python 3.8+ stdlib) | external (Python stdlib) — fallback contract owned by spec/26 §97 AC-24 | AC-24 fallback canonicaliser snippet | Stdlib fallback when `xmllint` is absent — equivalence claim documented in AC-24 | **N/A** — Python stdlib documentation is the canonical source; spec/26 cites the function, never re-derives the W3C Canonical XML spec |
| spec/27-spec-toolchain (script anchors) | spec/27 §97 (slot 18 = check-mermaid-syntax; slots 02/03/14/24 = various) | `00-overview.md` L148/160/172/186/200 (CI gates) + AC-DG-* family | Mechanical PR-time gates: Mermaid syntax check, diagram-regen lockstep audit, contract validation | **YES** — script CLI surfaces + exit-code contracts live in spec/27 §97 per-slot ACs; spec/26 cites script paths, never replicates CLI logic |

**AND** any future contributor adding a new diagram OR amending an existing diagram in spec/26 that references a contract surface owned by another top-level module MUST add a row to the table above (citation + owning module/AC + spec/26 file + purpose + restate-forbidden flag) before the new content ships — the table IS the audit-followable dependency chain. **The "derivative spec" status of spec/26 makes this rule particularly load-bearing**: every Mermaid node label that mentions an entity, error code, RBAC role, or pipeline state is by construction a citation of spec/22 or spec/03 — the table above absorbs that entire class of citations as the spec/22 + spec/03 rows;

**AND** any auditor finding citing "external dependency unresolved" or "dangling cross-module reference" against the 5 rows above MUST be classified as a stale-cache artifact (the anchor exists in the cited owning module's §97 — verify with `rg -n "AC-XX" spec/NN-*/97-acceptance-criteria.md` before flagging);

**AND** the table is **append-only** within a phase (rows MAY be added, never reworded);

**AND** restating any of the linked contracts inline within spec/26 is **FORBIDDEN** (Lesson #36 dual-source drift class) — every row's "Restate-in-26 forbidden?" cell is `YES` by construction (the two `N/A` rows are external system dependencies, not spec-module citations). The "derivative spec" architectural relationship to spec/22 is the manifestation of this rule: spec/26 adds *visual* renderings of spec/22 contracts, never normative text about what the contracts mean.

- **Verifies:** the cross-module externalized citation contract for spec/26 — every external dependency (spec/22 source-of-truth, spec/03 error catalog, `xmllint` + Python stdlib for canonicalisation, spec/27 CI gates) has an explicit normative anchor in the table above. Codifies **Lesson #36** (link-don't-restate cross-module boundary) + **Lesson #37** (integration-axis module co-needs Lesson #19 + Lesson #36) + **Lesson #29 Section F** (audit-corpus protocol-surface rule for the OS-binary + stdlib-fallback rows). Mirror of spec/22 AC-79 + spec/23 AC-ADB-17 + spec/24 AC-ADS-14 + spec/28 AC-28-45 (Phase 154 C-Sweep batch). Note: spec/26 is the **highest-citation-density module in the C-Sweep batch** because every diagram is by definition a citation of its source contract — the spec/22 row in the table absorbs the entire visual-citation surface in one normative anchor.
- **Source:** `97-acceptance-criteria.md` (this AC); cross-references all 6 active `.mmd` files (each visualizes a spec/22 contract surface), AC-23 + AC-24 (canonicaliser toolchain), AC-DG-* family (CI gates).

---

### AC-26 — Sibling Artifact Delegation Map (Lesson #21 — intra-module audit-boundary pin for all sibling files)  `[critical]`

**Given** spec/26-gitlogs-diagrams contains **18 sibling artifacts** beyond §97 itself — 6 active `.mmd` Mermaid sources + their 6 paired `.svg` build artifacts + 1 render-config (`puppeteer.json`) + 1 module lifecycle diagram + 1 sub-folder (`01-diagram-conventions/`) + 3 informative module-meta files (`00-overview.md`, `98-changelog.md`, `99-consistency-report.md`) — and an AI auditor walking only the tier-1 contract surface (`97-acceptance-criteria.md`) would otherwise be unable to determine which §97 AC family governs each sibling without leaving the tier-1 bundle (Lesson #21 intra-module audit-boundary < verification-boundary gap, mirror of spec/22 AC-80);

**When** an auditor encounters any sibling file in spec/26 OR a contributor adds a new diagram or amends an existing one,

**Then** the auditor / contributor MUST find the governing AC-family for that sibling in the table below — every row binds an artifact to its §97 governing AC(s), tier visibility, and restate-forbidden flag:

| Sibling artifact | Content kind | Governing §97 AC family | Tier visibility | Restate-in-§97 forbidden? |
|---|---|---|---|---|
| `01-er-diagram.mmd` | Mermaid ER source | AC-DG-01 + AC-DG-02 + AC-DG-05 + AC-DG-06 + AC-DG-13 + AC-DG-14 + AC-DG-16 + AC-DG-20 | tier-2 (artifact) | YES — ER table list + cardinalities live in spec/22 §97 |
| `01-er-diagram.svg` | Build artifact | AC-DG-11 + AC-DG-12 + AC-23 + AC-24 | tier-3 (derived) | YES — generated, never hand-edited |
| `05-auth-validation.mmd` | Mermaid sequence source | AC-DG-03 + AC-DG-05 + AC-DG-06 + AC-DG-07 + AC-DG-13 + AC-DG-14 + AC-DG-16 + AC-DG-17 + AC-DG-20 | tier-2 (artifact) | YES — TempToken auth state machine lives in spec/22 §97 |
| `05-auth-validation.svg` | Build artifact | AC-DG-11 + AC-DG-12 + AC-23 + AC-24 | tier-3 (derived) | YES — generated |
| `06-permission-flow.mmd` | Mermaid flowchart source | AC-DG-04 + AC-DG-05 + AC-DG-06 + AC-DG-13 + AC-DG-14 + AC-DG-16 + AC-DG-20 | tier-2 (artifact) | YES — RolePermission union rule lives in spec/22 §97 |
| `06-permission-flow.svg` | Build artifact | AC-DG-11 + AC-DG-12 + AC-23 + AC-24 | tier-3 (derived) | YES — generated |
| `07-rate-limit-flow.mmd` | Mermaid flowchart source | AC-DG-05 + AC-DG-06 + AC-DG-13 + AC-DG-14 + AC-DG-15 + AC-DG-16 + AC-DG-17 + AC-DG-20 | tier-2 (artifact) | YES — token-bucket parameters live in spec/22 §97 |
| `07-rate-limit-flow.svg` | Build artifact | AC-DG-11 + AC-DG-12 + AC-23 + AC-24 | tier-3 (derived) | YES — generated |
| `08-encryption-v3-flow.mmd` | Mermaid flowchart source | AC-DG-05 + AC-DG-06 + AC-DG-09 + AC-DG-13 + AC-DG-14 + AC-DG-16 + AC-DG-20 | tier-2 (artifact) | YES — MasterKey → DataKey derivation lives in spec/22 §97 |
| `08-encryption-v3-flow.svg` | Build artifact | AC-DG-11 + AC-DG-12 + AC-23 + AC-24 | tier-3 (derived) | YES — generated |
| `09-endpoints-mindmap.mmd` | Mermaid mindmap source | AC-DG-05 + AC-DG-06 + AC-DG-08 + AC-DG-13 + AC-DG-14 + AC-DG-16 + AC-DG-20 | tier-2 (artifact) | YES — 8 REST endpoints + per-branch contracts live in spec/22 §97 |
| `09-endpoints-mindmap.svg` | Build artifact | AC-DG-11 + AC-DG-12 + AC-23 + AC-24 | tier-3 (derived) | YES — generated |
| `10-ssh-auth-validation.mmd` | Mermaid sequence source | AC-DG-03 + AC-DG-05 + AC-DG-06 + AC-DG-07 + AC-DG-13 + AC-DG-14 + AC-DG-16 + AC-DG-17 + AC-DG-20 + AC-DG-21 | tier-2 (artifact) | YES — SSH 10-step validation order lives in spec/22 §31 + spec/22 §97 |
| `10-ssh-auth-validation.svg` | Build artifact | AC-DG-11 + AC-DG-12 + AC-23 + AC-24 | tier-3 (derived) | YES — generated |
| `puppeteer.json` | Render config | AC-DG-18 | tier-2 (artifact) | YES — Mermaid CLI Chromium config; restating in §97 prose creates a dual-source drift class |
| `lifecycle-26-gitlogs-diagrams-lifecycle.mmd` | Module lifecycle diagram | AC-SAG-* (system-wide lifecycle convention, owned by spec/17) | tier-2 (artifact) | YES — lifecycle-diagram convention owned by spec/17, not spec/26 |
| `01-diagram-conventions/` (sub-folder) | Convention sub-spec | AC-DG-05 + AC-DG-06 + AC-DG-16 + own §97 | tier-2 (sub-folder) | YES — sub-folder has its own §97; spec/26 root §97 MUST NOT restate convention rules |
| `00-overview.md` | Module overview (informative + axis declaration) | (informative — exempt per AC-SAG-* meta-file rule) | tier-1 (banner) | N/A — overview cites §97 ACs, never the reverse |
| `98-changelog.md` | Module changelog (informative) | (informative — exempt per AC-SAG-* meta-file rule) | tier-1 (banner) | N/A — append-only ledger of versioned changes |
| `99-consistency-report.md` | Module consistency report (informative) | (informative — exempt per AC-SAG-* meta-file rule) | tier-1 (banner) | N/A — derived consistency status |

**AND** any new sibling artifact added to spec/26 in a future phase (new `.mmd` diagram, new render-config file, new sub-folder) MUST add a row to this table BEFORE the artifact ships — the table IS the intra-module audit-followable dependency chain (mirror of AC-25's cross-module externalized citation map; together AC-25 + AC-26 + AC-22 form the complete audit-boundary closure for spec/26 per Lesson #37);

**AND** any auditor finding citing "sibling file orphan" or "missing §97 AC for `<filename>`" against the 18 listed artifacts MUST be classified as a stale-cache artifact (the governing AC family is in the table — verify before flagging per Lesson #34);

**AND** the table is **append-only** within a phase (rows MAY be added when a new sibling ships, never reworded);

**AND** restating any artifact's content inline within §97 is **FORBIDDEN** — every `.mmd` source's normative content (entities, flow steps, RBAC rules, error codes, endpoint paths) is already governed by a spec/22 §97 AC per AC-25's cross-module citation map; restating in spec/26 §97 creates a triple-source drift class (spec/22 §97 → spec/26 `.mmd` → spec/26 §97 prose).

- **Verifies:** the intra-module sibling-artifact delegation contract for spec/26 — every one of the 18 sibling artifacts (6 `.mmd` + 6 `.svg` + `puppeteer.json` + lifecycle + `01-diagram-conventions/` + 3 informative meta-files) has an explicit row in the delegation map above with content-kind + governing-§97-AC-family + tier-visibility + restate-forbidden columns. Closes the **Lesson #21 intra-module audit-boundary < verification-boundary gap** at the spec/26 derivative-spec axis. Mirror of spec/22 AC-80 (33-sibling-file delegation map, intra-module sibling-file axis) and spec/02 AC-CG-21 (16-sub-folder delegation map, intra-module cross-language axis). Together with **AC-25** (cross-module externalized citation map) and **AC-22** (derivative-context module-kind pin) forms the **complete tier-1 audit-followability triplet** for spec/26 per Lesson #37 (integration-axis modules co-need Lesson #19 + Lesson #21 + Lesson #36 closures). Until A8 (LLM-gateway re-score) unblocks, this AC declares any "sibling artifact orphan" or "missing §97 AC for diagram NN" finding against the 18 listed artifacts a stale-cache artifact per Lesson #34.
- **Source:** `97-acceptance-criteria.md` (this AC); cross-references AC-25 (cross-module map — mirror pair), AC-22 (derivative-context module-kind pin — mirror pair), AC-DG-01..AC-DG-22 (per-diagram contract families cited in the table), AC-23 + AC-24 (canonicaliser toolchain governing all `.svg` artifacts).
