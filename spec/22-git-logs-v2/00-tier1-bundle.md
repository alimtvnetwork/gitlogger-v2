---
kind: bundle-manifest
todo_audit_exempt: true
description: Tier-1 essential bundle — the minimum subset of §22 source files an LLM must read to implement the Git Logs WordPress backend end-to-end. Targets the Raw-LLM persona (single context window, no file-tool access). All other §22 files are tier-2 (recommended) or tier-3 (specialised surfaces). Out-of-bundle files MUST NOT introduce contracts not pinned by tier-1 — drift = §22 §97 AC-22-CE2 breach.
content_axis: navigation-aid
axis_rationale: "Single-page read-order anchor for the §22 spec set"
---

# Git Logs v2 — Tier-1 Essential Bundle

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-67 B-1 — initial tier-1 / tier-2 / tier-3 partition; introduced to lift §22 Raw-LLM persona score by carving a ≤2.2K-line implementable subset out of the 10,282-line full §22 corpus.)
**Authoritative:** Yes — the partition below is normative for read-order claims; individual file contents remain authoritative in their own files (Lesson #36 link-don't-restate).

> 🤖 **Raw-LLM Reader Pin.** If your context window cannot fit all of §22 (10,282 lines across 57 files), read **only the tier-1 files below** in the listed order. The 9 tier-1 files (~2,140 lines) are sufficient to implement the §22 WordPress backend end-to-end — REST endpoints, auth, DB schema, seed data, error catalogue, and permission matrix. Tier-2 files refine specialised surfaces (logger internals, SSH key auth, split-DB log storage). Tier-3 files are operational, retrospective, AC-detail, or test-skeleton surfaces — they are *required reading* only when the corresponding feature is being built.

---

## Tier-1 — Implementable minimum (read in order)

| # | File | Lines | Role | Why tier-1 |
|---|---|---|---|---|
| 1 | [`00-overview.md`](./00-overview.md) | 273 | Module pin + Raw-LLM auditor pin + cross-cohort gate map | Fixes vocabulary (`profile`, `applink`, `pipeline`, `repo`, `app`) and the locked-7 perimeter. |
| 2 | [`01-glossary-and-enums.md`](./01-glossary-and-enums.md) | 313 | Closed enum catalogue (12 enum types, 11 active + 1 forbidden) | Every status / kind / role token an implementer emits MUST be drawn from this file. Forbids free-text. |
| 3 | [`19-permission-matrix.md`](./19-permission-matrix.md) | 73 | Role × endpoint × verb permission matrix | Tiny, but every endpoint handler depends on it. Read before §17/§18. |
| 4 | [`18-schema.sql`](./18-schema.sql) | 485 | Authoritative SQLite DDL (CREATE TABLE × N + indexes + triggers + seed-id locks) | Machine-readable single source of truth for the database surface. Supersedes prose in `02-database-schema.md` per Lesson #36. |
| 5 | [`16-seed-data.md`](./16-seed-data.md) | 235 | Locked seed rows (AppLinkType id=1/2, RolePermission grid, MigrationState bootstrap) | Required to bring the schema in §18 into a working initial state. |
| 6 | [`17-openapi.yaml`](./17-openapi.yaml) | 562 | Authoritative OpenAPI 3.1 spec for all 8 REST endpoints + request/response schemas | Machine-readable single source of truth for the REST surface. Supersedes prose in `04-rest-api-endpoints.md` per Lesson #36. |
| 7 | [`05-auth-and-validation.md`](./05-auth-and-validation.md) | 124 | Auth pipeline ordering (parse → GitProfile → Acceptance → Branch → TempToken → Token → Profile → App) + GL-* reject codes | Every endpoint runs this pipeline before its handler. Read after §17. |
| 8 | [`14-endpoint-examples.md`](./14-endpoint-examples.md) | 177 | Concrete request + response transcripts per endpoint | Disambiguates §17 schema choices the OpenAPI cannot encode (header casing, body framing). |
| 9 | [`15-error-codes.md`](./15-error-codes.md) | 142 | Closed GL-* error code catalogue with HTTP-status, retryability, audit category | Required for every endpoint reject branch + §22 observability surface. |
| **Σ** | **9 files** | **~2,384** | **Tier-1 footprint** | Below the 8K-token "single context window" comfort threshold for most LLMs at default prompt budgets. |

**Read-order rationale:** vocabulary (1, 2) → access control (3) → state shape (4, 5) → API surface (6, 7, 8) → failure surface (9). An implementer who follows this order can author every endpoint handler, every storage call, and every error path without needing tier-2 or tier-3.

---

## Tier-2 — Recommended adjuncts (read when implementing the named surface)

| File | Lines | Surface it refines | When to add to context |
|---|---|---|---|
| [`02-database-schema.md`](./02-database-schema.md) | 507 | Prose narrative + ER intent for §18 SQL | Only if the implementer needs ER relationships in prose form (e.g. building admin UI). Tier-1 §18 + §26 §01 ER diagram normally suffice. |
| [`04-rest-api-endpoints.md`](./04-rest-api-endpoints.md) | 406 | Prose narrative + endpoint-by-endpoint design rationale | Only when §17 OpenAPI alone is ambiguous on intent (e.g. polymorphic AppLink target resolution). |
| [`06-migrations-and-logger.md`](./06-migrations-and-logger.md) | 60 | Logger internals + migration runner | Required for §22 §39 split-DB log storage and any AC that mentions `MigrationState`. |
| [`07-app-entity.md`](./07-app-entity.md) | 63 | App entity lifecycle (create → activate → archive) | Required when implementing §22 App-write surface (POST /apps + status transitions). |
| [`08-history-and-action.md`](./08-history-and-action.md) | 56 | History + PipelineAction tables semantics | Required for the audit-trail and admin pipeline-action UI. |
| [`31-ssh-key-auth.md`](./31-ssh-key-auth.md) | 205 | SSH key auth lane (alternative to header-token auth) | Required when implementing the headless SSH auth flow (mutually exclusive with WP-auth lane per §05). |
| [`39-split-db-log-storage.md`](./39-split-db-log-storage.md) | 186 | Per-app log SQLite file partitioning | Required for high-volume deployments; tier-1 schema in §18 references the join points. |
| **Σ** | **~1,483** | **Tier-2 footprint** | When combined with tier-1 (~3,867 lines total) covers ≥95% of the buildable surface. |

---

## Tier-3 — Specialised surfaces (read only for the named feature)

Grouped by reason for tier-3 status. None are required for a working baseline backend.

### Operational + deployment (read for ops/SRE work)
- [`20-observability.md`](./20-observability.md) (110) — metrics/log shipping
- [`22-retention-and-pruning.md`](./22-retention-and-pruning.md) (158) — log retention policy
- [`23-backup-restore.md`](./23-backup-restore.md) (183) — DB backup procedure
- [`24-multisite.md`](./24-multisite.md) (85) — WP multisite caveats
- [`26-readme-and-screenshots.md`](./26-readme-and-screenshots.md) (168) — plugin README
- [`27-wp-cli-reference.md`](./27-wp-cli-reference.md) (178) — WP-CLI command set
- [`29-uninstall-policy.md`](./29-uninstall-policy.md) (123) — uninstall hook contract
- [`30-threat-model.md`](./30-threat-model.md) (122) — STRIDE summary

### CI + tests (read when authoring or wiring tests)
- [`28-example-github-actions.md`](./28-example-github-actions.md) (331)
- [`32-cli-test-plan.md`](./32-cli-test-plan.md) (234)
- [`33-bats-test-skeleton.md`](./33-bats-test-skeleton.md) (324)
- [`34-phpunit-test-skeleton.md`](./34-phpunit-test-skeleton.md) (469)
- [`35-reference-ci-yml.md`](./35-reference-ci-yml.md) (167)
- [`45-cli-test-plan.md`](./45-cli-test-plan.md) (181)

### CLI surface (read for §22 CLI client implementation — distinct from §28 universal CLI)
- [`03-admin-ui.md`](./03-admin-ui.md) (93)
- [`25-headless-auth-notes.md`](./25-headless-auth-notes.md) (96)
- [`40-cli-overview.md`](./40-cli-overview.md) (100)
- [`41-cli-pointer-file-schema.md`](./41-cli-pointer-file-schema.md) (259)
- [`42-cli-classifier-rules.md`](./42-cli-classifier-rules.md) (238)
- [`43-cli-upload-protocol.md`](./43-cli-upload-protocol.md) (214)
- [`44-cli-autofix-protocol.md`](./44-cli-autofix-protocol.md) (260)
- [`46-server-upload-frames-endpoint.md`](./46-server-upload-frames-endpoint.md) (237)
- [`47-server-autofix-endpoint.md`](./47-server-autofix-endpoint.md) (153)
- [`48-server-refresh-pointer-endpoint.md`](./48-server-refresh-pointer-endpoint.md) (150)

### AC sub-detail files (delegations from §97 — read only when the parent AC is unclear)
- [`49-ac-section-a-detail.md`](./49-ac-section-a-detail.md) (146)
- [`50-ac-delegation-maps-detail.md`](./50-ac-delegation-maps-detail.md) (121)
- [`51-ac-enum-catalog-detail.md`](./51-ac-enum-catalog-detail.md) (44)
- [`52-ac-k-series-server-detail.md`](./52-ac-k-series-server-detail.md) (96)
- [`53-ac-section-e-detail.md`](./53-ac-section-e-detail.md) (40)
- [`54-ac-j-series-cli-detail.md`](./54-ac-j-series-cli-detail.md) (158)
- [`55-ac-section-d-detail.md`](./55-ac-section-d-detail.md) (39)
- [`56-ac-section-d-constraints-detail.md`](./56-ac-section-d-constraints-detail.md) (44)
- [`57-ac-section-d-endpoints-detail.md`](./57-ac-section-d-endpoints-detail.md) (97)
- [`58-ac-section-e-multisite-detail.md`](./58-ac-section-e-multisite-detail.md) (86)
- [`59-ac-section-e-logger-detail.md`](./59-ac-section-e-logger-detail.md) (83)
- [`60-app-cohort-integration.md`](./60-app-cohort-integration.md) (229)

### Retrospective / superseded (read only for spec-history archaeology)
- [`36-why-v1-archived.md`](./36-why-v1-archived.md) (80)
- [`37-blind-ai-gap-analysis.md`](./37-blind-ai-gap-analysis.md) (192)
- [`38-test-plan-superseded.md`](./38-test-plan-superseded.md) (25)

### Ledgers (always last; read for version/changelog context only)
- [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) (686) — 84 ACs (consult on demand per AC-id; do NOT linearise)
- [`98-changelog.md`](./98-changelog.md) (52)
- [`99-consistency-report.md`](./99-consistency-report.md) (160)

---

## Implementer pre-flight checklist (per persona)

| Persona | Read order | Stop reading after | Implementation guarantee |
|---|---|---|---|
| **Raw-LLM** (single context window) | Tier-1 only | After file 9 (`15-error-codes.md`) | High for endpoint handlers + DB + auth + errors. Tier-2/3 deferred to follow-up turns with focused excerpts. |
| **Cursor / Claude-Code** (file access + shell) | Tier-1 in order, then load tier-2 on demand | When the surface under construction is covered | Very high; gate-set in §27 will catch drift. |
| **Lovable** (full agent + Cloud + UI preview) | Tier-1 as primer, then jump to whichever tier-2/3 the current sub-task names | n/a — agent re-loads files on demand | Very high; same as Cursor + Cloud-side schema preview. |

---

## Drift contract (Lesson #36 + Lesson #15 reflexivity)

- **Add or remove a §22 file** → update both the relevant tier table here AND the totals row in the same commit. Failure to do so MUST be flagged by §22 §99 next consistency report.
- **Promote a tier-3 file to tier-2** (or tier-2 → tier-1) → MUST cite the AC family that newly depends on it, and re-tally the "Σ" line. Tier-1 footprint MUST stay ≤ 2,500 lines (the soft Raw-LLM ceiling); breach triggers a tier-1 candidate-removal review in the same commit.
- **Forbidden:** introducing a new normative contract in any tier-2 / tier-3 file that is not also surfaced (by reference) in tier-1. This file pins the read-order; new contracts must enter through tier-1 first.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [§26 ER diagram](../26-gitlogs-diagrams/01-er-diagram.mmd) — visualises tier-1 file 4 (`18-schema.sql`)
- [§26 endpoints mindmap](../26-gitlogs-diagrams/09-endpoints-mindmap.mmd) — visualises tier-1 file 6 (`17-openapi.yaml`)
- [§23 R-1 endpoint matrix](../23-app-database/00-overview.md) — downstream consumer of tier-1 file 6
