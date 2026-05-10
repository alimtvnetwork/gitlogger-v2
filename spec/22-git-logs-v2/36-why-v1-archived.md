# Why folder 21 is in `_archive/`

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Status:** Reference  
**Audience:** Anyone landing in v2 looking for v1

---

## TL;DR

`spec/21-git-logs-v1/` was moved to **`spec/_archive/21-git-logs-v1/`** on 2026-04-25 because the v1 design was superseded by a structurally incompatible v2:

| Aspect | v1 (folder 21) | v2 (folder 22) |
|--------|----------------|----------------|
| Database | MySQL via `wpdb`, `{wp_prefix}gitlogs_*` tables | **SQLite root DB**, single file owned by plugin |
| Auth (CI/CD) | Allowlist gate + plugin **JWT (RS256)** + JWKS endpoint | **TempToken + GitHub URL + branch validation** (JWT *dropped*); SSH-key sub-mode preferred from v2.7.0 |
| Roles | Mapped to WP roles | Plugin-internal SQLite Admin/Editor; **Permission**-based authz, never role-name |
| REST namespace | `git-logs/v1` (paths like `/logs/push`, `/logs/{id}`) | `git-logs/v2` (10 logical endpoints: `/append-log`, `/fixed-log`, …) |
| Audit model | Single audit table | Three-table split: `AuditTrail` (system) + `History` (per RepoVersion) + `Action` (enum log) |
| App entity | _(not modeled)_ | First-class `App` + polymorphic `AppLink` |
| Naming | snake_case | **PascalCase** tables/columns/JSON keys/values |
| Acceptance modes | Allowlist + version-wildcard regex | `AcceptAllRepos` / `AcceptSelectedRepoOnly` / `AcceptSelectedRepoInAllVersions` enum |

The two designs share the *problem domain* (ingest CI/CD logs into a WP-hosted store) but **disagree on every major contract**: schema, auth, namespace, audit shape, and identifier conventions. A unified file tree would have made every cross-link ambiguous (`logs/push` vs `append-log`?), so the historical record was preserved separately.

---

## Why archived (not deleted)

1. **Provenance.** v2 was derived from a verbatim brief that lived in v1's `reference/` directory. Deleting v1 would orphan that source-of-truth document.
2. **Migration audits.** Anyone running v1 in production needs the v1 schema+API to plan a cut-over. The v2 changelog references v1 fields by name.
3. **Locked-decision evidence.** v2 §05 ("Why no JWT in v2") cites v1's RS256/JWKS infrastructure as the thing being rolled back. That citation needs a target.
4. **Audit traceability.** The deterministic audit (`linter-scripts/audit-spec-vs-code-v2.py`) reads `_archive/` so historical scores are reproducible.

A deprecation banner was prepended to every file under `_archive/21-git-logs-v1/` on 2026-04-25 redirecting readers to v2.

---

## Where v1 features live now

| v1 file | v2 equivalent | Notes |
|---------|---------------|-------|
| `00-overview.md` | `22/00-overview.md` | Locked decisions table replaces v1 prose |
| `01-glossary-and-enums.md` | `22/01-glossary-and-enums.md` | Renamed/expanded enums (added `Acceptance`, `AppStatus`, `LogSeverity`) |
| `02-database-schema-and-erd.md` | `22/02-database-schema.md` + `22/18-schema.sql` | DDL extracted to `.sql`; ERD moved to `26-gitlogs-diagrams/` |
| `05-auth-jwt-flow.md` | `22/05-auth-and-validation.md` + `22/31-ssh-key-auth.md` | **JWT removed.** Replaced by TempToken validation + optional SSH lane |
| `08-allowlist-and-wildcard-matching.md` | `22/05` (acceptance modes) + `22/01` (`Acceptance` enum) | Regex wildcard replaced by enum-based acceptance + canonical RepoUrl parsing |
| `11-error-management.md` | `22/15-error-codes.md` | All `GL-*` codes consolidated; v1 had per-feature scattering |
| `12-logging-strategy.md` | `22/06-migrations-and-logger.md` + `22/20-observability.md` | Logger spec + Site Health card |
| `16-jwt-onboarding-and-token-usage.md` | _(removed)_ | No JWT in v2 |
| `17-spec-consistency-checklist.md` | `22/99-consistency-report.md` | Audit checklist replaced by automated linter (`linter-scripts/audit-spec-vs-code-v2.py`) |
| `97-acceptance-criteria.md` | `22/97-acceptance-criteria.md` | Format kept (Given/When/Then in v1); **content rewritten** because endpoints changed |
| `99-consistency-report.md` | `22/99-consistency-report.md` | Same role |
| `reference/00-verbatim-brief.md` | _(unchanged path)_ | Authoritative source for both versions; kept where it is |
| `error-codes.json` | `22/15-error-codes.md` (markdown table) | Format change: JSON → reviewable Markdown |

---

## Should I read v1 ever?

Only if:

- You are migrating a v1-deployed site and need the v1 schema to write a SQL exporter.
- You are reviewing why a specific decision was reversed (the verbatim brief in `reference/00-verbatim-brief.md` is the primary source — v1 just *interpreted* it).
- You are auditing the trail.

For new implementations, **always start at [`spec/22-git-logs-v2/00-overview.md`](./00-overview.md)**.

---

## Can v1 be deleted in a future cycle?

Yes — when:

1. No production deployment of v1 remains (tracked in `mem://specs/git-logs.md`).
2. The verbatim brief at `reference/00-verbatim-brief.md` is moved into v2 (e.g. `22/_brief/00-verbatim-brief.md`).
3. The deterministic audit's blast-radius for `21-git-logs-v1` drops to 0.

Until then, leave `_archive/` alone.
