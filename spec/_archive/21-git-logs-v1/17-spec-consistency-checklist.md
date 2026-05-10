> ⚠️ **DEPRECATED — Legacy v1 Spec (folder 21)**  
> This document is preserved for historical reference only. **Do not implement against it.**  
> The active specification is **v2** in [`spec/22-git-logs-v2/`](../../22-git-logs-v2/00-overview.md) (SQLite, no JWT, SSH-key auth).  
> See [`spec/22-git-logs-v2/00-overview.md`](../../22-git-logs-v2/00-overview.md) for the current canonical source.  
> Deprecated: 2026-04-25

---

# Spec Consistency Checklist — App vs Coding Guidelines, Naming, Booleans/Enums, Split-DB, Seedable Config

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Status:** Active  
**AI Confidence:** Production-Ready  
**Ambiguity:** Low  
**Scope:** All spec files under `spec/21-git-logs/` (the `git-logs` App)

---

## Purpose

This checklist verifies that every App spec file in `spec/21-git-logs/` complies with the four binding guideline domains:

1. **Master Coding Guidelines** — `spec/02-coding-guidelines/01-cross-language/15-master-coding-guidelines/`
2. **Naming Conventions (Zero-Underscore Policy)** — `01-naming-and-database.md` §1.4 and `spec/04-database-conventions/01-naming-conventions.md`
3. **Boolean & Enum Patterns** — `02-boolean-and-enum.md`
4. **Split-Database Architecture** — `spec/05-split-db-architecture/`
5. **Seedable Config Architecture (CW Config)** — `spec/06-seedable-config-architecture/`

A spec passes only when every applicable check returns **PASS**. `N/A` is allowed only with a one-line written justification immediately under the row. `FAIL` blocks merge.

---

## How to Run This Checklist

1. Open the spec file under audit (e.g., `02-database-schema-and-erd.md`).
2. Walk through every section below in order. Do not skip — record `PASS`, `FAIL`, or `N/A` for each row.
3. For every `FAIL`, capture the offending excerpt (≤ 120 chars) and the corrective action in the **Findings Log** at the bottom of the audited file (or in a sibling issue file under `spec/25-app-issues/`).
4. Run the cross-link verifier:
   ```bash
   python3 linter-scripts/check-spec-cross-links.py --root spec --repo-root .
   ```
5. Stamp the file: `_Consistency check passed: {YYYY-MM-DD} by {auditor-id}_`.

---

## Section A — Master Coding Guidelines Compliance

| # | Check | Source | Pass Criterion |
|---|-------|--------|----------------|
| A1 | Spec references the master guidelines exactly once in its **Cross-References** table | `15-master-coding-guidelines/00-overview.md` | Link present and resolves |
| A2 | All PHP code samples use **PSR-12 + WP coding standards subset** as declared in the applied-guidelines doc | `13-coding-guidelines-applied.md` | No tab/space mixing; braces on same line for control flow |
| A3 | No empty `catch` blocks, no `@` suppression operator, no raw `WP_Error` returns | `11-error-management.md` §No-Swallow | Every `catch` logs full context AND re-throws or returns standard envelope |
| A4 | Every public function has explicit return type and parameter type declarations | Master §Type Safety | `function foo(): SomeType` form everywhere |
| A5 | No magic strings — every literal status, role, capability, hook name routed through a constant or enum | Master §Magic Strings | Search for raw `'admin'`, `'success'` in code samples returns zero hits |
| A6 | Errors carry stable codes from the `GL-*` namespace defined in `11-error-management.md` | `11-error-management.md` | Every error path names a `GL-{NAMESPACE}-{REASON}` code |
| A7 | Files defining a single primary type use **PascalCase filenames** in code samples | Master §1.3 | `SnapshotManager.php`, never `snapshot-manager.php` |
| A8 | Spec files (this folder) use lowercase kebab-case with numeric prefix | Master §1.3 exemption | `NN-name.md` form |
| A9 | All function/method names in samples are camelCase (PHP/TS) or PascalCase (Go) | Master §1.1 | Conforms to language column |
| A10 | Abbreviations follow first-letter-cap rule: `Id`, `Url`, `Json`, `Jwt`, `Ip`, `Db` (never `ID`, `URL`, `JSON`, `JWT`, `IP`, `DB`) | Master §1.2 | Search for `\b(ID|URL|JSON|JWT|IP|DB|API|HTTP|HTML|SQL|MD5)\b` in code samples returns zero hits |

---

## Section B — Zero-Underscore / Naming Conventions

| # | Check | Source | Pass Criterion |
|---|-------|--------|----------------|
| B1 | No underscores in PHP variable names in code samples | Master §1.4 | `$is_active` → FAIL; `$isActive` → PASS |
| B2 | No underscores in PHP method/property names | Master §1.4 | `process_upload()` → FAIL; `processUpload()` → PASS |
| B3 | No underscores in array keys used in application logic (log context, response payloads, internal maps) | Master §1.4 | `'post_id'` → FAIL; `'postId'` (logic) or `'PostId'` (REST/DB) → PASS |
| B4 | REST request/response field names are **PascalCase** (e.g., `RepoUrl`, `TraceId`) | `spec/04-database-conventions/06-rest-api-format.md` + Master §1.1 | Lowercase or snake_case in JSON examples → FAIL |
| B5 | Database table names are **PascalCase** singular-or-plural per existing convention (e.g., `Repository`, `AuditTrail`, `RevokedJti`) | `04-database-conventions/01-naming-conventions.md` + `05-split-db-architecture` Critical Naming | snake_case → FAIL |
| B6 | Database column names are PascalCase | Same as B5 | snake_case column → FAIL |
| B7 | Index names use `Idx` prefix + PascalCase (e.g., `IdxAuditTrail_TraceId`) | Master §2 | Other forms → FAIL |
| B8 | Allowed underscore exemptions are explicitly tagged when used (WP hooks, capabilities, option keys, `wp_*` core tables, HTTP headers, env vars, WP-Cron args) | Master §1.4 Exemptions | Inline note like `// WP option key — exempt` is required |
| B9 | WordPress option keys for this plugin use the `gitlogs_` prefix (e.g., `gitlogs_trusted_proxies`, `gitlogs_allowed_origins`) — exempt from PascalCase but must carry the prefix | `00-overview.md` decision #11 | Missing prefix → FAIL |
| B10 | REST namespace and route segments use lowercase kebab-case (`/wp-json/git-logs/v1/...`) — REST URL exemption | `00-overview.md` decision #12 | Other forms → FAIL |
| B11 | File names inside `spec/21-git-logs/` use `NN-kebab-name.md` | `01-spec-authoring-guide/02-naming-conventions.md` | Other forms → FAIL |
| B12 | No abbreviation collisions — `Jwt` not mixed with `JWT` within the same spec | Master §1.2 | Mixed case → FAIL |

---

## Section C — Boolean & Enum Patterns

### C.1 Booleans (positive-logic, no negatives)

| # | Check | Source | Pass Criterion |
|---|-------|--------|----------------|
| C1 | Every boolean in code samples starts with `is`, `has`, or `should` (rare) — never `can`, `was`, `will` | `02-boolean-and-enum.md` P1 | `$loaded` → FAIL; `$isLoaded` → PASS |
| C2 | No negative words inside boolean names: `not`, `no`, `non` | P2 | `$isNotReady` → FAIL; `$isPending` → PASS |
| C3 | No raw `!` applied to function calls — use the semantic inverse | P3 | `if (!$order->isValid())` → FAIL; `if ($order->isInvalid())` → PASS |
| C4 | Compound expressions with 2+ operators extracted to a named boolean | P4 | `if ($a && $b && !$c)` inline → FAIL |
| C5 | No boolean function parameters (use named methods or options arrays) | P5 | `process(true)` → FAIL |
| C6 | No mixed polarity (`isX && !isY`) — extract to single-intent name | P6 | Mixed polarity inline → FAIL |
| C7 | Existence guards use `isDefined()` / `isDefinedAndValid()` / `isEmpty()` instead of `!== null` chains | §3.1 | `if ($x !== null && $x->isValid())` → FAIL |
| C8 | Result wrappers expose `isDefined()`, `isSafe()`, `isEmpty()`, `hasError()` | §3.1 Result Wrappers | Custom variants forbidden |

### C.2 Enums

| # | Check | Source | Pass Criterion |
|---|-------|--------|----------------|
| C9 | Every domain category uses an enum (no magic strings): `Provider`, `ActorType`, `Outcome`, `TokenScope`, `MatchKind`, `MatchPattern`, `JwtAlg`, `RateLimitClass` | `01-glossary-and-enums.md` + Master §4 | Inline string literal → FAIL |
| C10 | Enum type names are PascalCase, optionally with `Type` suffix when ambiguous | Master §1.1 | other forms → FAIL |
| C11 | Enum cases are PascalCase | Master §4 | snake_case / SCREAMING_SNAKE → FAIL |
| C12 | Every `switch`/`match` over an enum has an exhaustive `default` branch that throws / returns standard error | Master §4 | Missing `default` → FAIL |
| C13 | Reserved-but-disabled enum values (e.g., `Provider::GitLab`) carry an explicit reject rule and a `GL-VAL-*` code | Audit issue P2-GL-20 | Missing reject rule → FAIL |
| C14 | Enum comparison uses `isEqual()` (PHP) / `=== EnumType.Member` (TS) / `Is{Value}()` (Go) — never `==` on enum-cased strings | Master §4 | Raw `==` on enum → FAIL |

---

## Section D — Split-Database Architecture Compliance

| # | Check | Source | Pass Criterion |
|---|-------|--------|----------------|
| D1 | If the App stores per-repository or per-pipeline data that may grow unbounded, it documents whether it follows the **Root DB → Item DB** split or stays within the WP DB; if split, schema doc names the Root DB and Item DB tables | `05-split-db-architecture/01-fundamentals.md` | Missing decision → FAIL |
| D2 | All custom tables use **PascalCase** field names (no underscores) | Split-DB Critical Naming | `created_at` → FAIL; `CreatedAt` → PASS |
| D3 | Every DB connection path (Root DB or Item DB) uses **WAL mode** for SQLite engines, or matches existing WP MySQL conventions | Split-DB §Connection Pooling | Missing WAL pragma for SQLite → FAIL |
| D4 | Each table has explicit indexes on every foreign key and on every column appearing in `WHERE` of the documented queries (e.g., `IdxAuditTrail_TraceId`, `IdxAuditTrail_RepositoryId_CreatedAt`) | `04-database-conventions/02-schema-design.md` | Missing index → FAIL |
| D5 | Backup / export hooks are addressed: spec states whether the table participates in standard WP export or exposes a dedicated backup endpoint | Split-DB §Backup | Missing statement → FAIL |
| D6 | If the spec defines a child-DB lifecycle (create/destroy), it follows the **2-step reset API standard (5-min TTL)** from Split-DB features | `05-split-db-architecture/02-features/02-reset-api-standard.md` | Single-step destructive endpoint → FAIL |
| D7 | RBAC for cross-DB access is documented (Casbin or capability mapping) | `05-split-db-architecture/02-features/04-rbac-casbin.md` | Missing role matrix → FAIL or N/A with justification |
| D8 | User-scoped isolation rules are stated when the table holds per-user rows (`UserId` FK) | `02-features/05-user-scoped-isolation.md` | Missing isolation rule → FAIL |

---

## Section E — Seedable Config Architecture (CW Config) Compliance

| # | Check | Source | Pass Criterion |
|---|-------|--------|----------------|
| E1 | Any first-run configuration (default rate-limit, default trusted-proxy CIDRs, default allowed-origins, JWT keypair bootstrap) is sourced from a **`config.seed.json`** equivalent (a `gitlogs.seed.json` or a constants file) | `06-seedable-config-architecture/01-fundamentals.md` | Hard-coded defaults inline → FAIL |
| E2 | Configuration carries a **semver `Version`** field; spec names the exact location | CW Config §Version Flow | Missing version field → FAIL |
| E3 | Every change to defaults bumps the `Version` and writes a row to `98-changelog.md` (and `CHANGELOG.md` at runtime) | CW Config §Changelog | Silent default change → FAIL |
| E4 | Subsequent runs check the stored version before re-seeding (no duplicate seeds) | CW Config §Subsequent Runs | Idempotency unspecified → FAIL |
| E5 | Merge strategy on upgrade is named: **replace**, **merge-shallow**, or **merge-deep** — and applied per-key | CW Config §Merge Strategies | Unstated → FAIL |
| E6 | Validation helpers are specified for every seeded config key (e.g., CIDR validator for `gitlogs_trusted_proxies`) | `02-features/02-rag-validation-helpers.md` (pattern) | Missing validator → FAIL |
| E7 | Seeded data lands in the **Root DB** (or WP options) per the seeding pattern in `02-features/05-validation-data-seeding.md` | CW Config §Seeding | Wrong destination → FAIL |
| E8 | Update-check / version-probe keys (e.g., `Update.LastCheckedAt`, `Storage.Backend`) follow the convention in `02-features/06-update-check-keys.md` | CW Config §Update Keys | Other key naming → FAIL |

---

## Section F — Cross-Cutting (applies to every file)

| # | Check | Pass Criterion |
|---|-------|----------------|
| F1 | File starts with the standard header (Title, **Version:** X.Y.Z, **Updated:** YYYY-MM-DD, optional Status / AI Confidence / Ambiguity) | Conforms to `01-spec-authoring-guide/02-naming-conventions.md` |
| F2 | File ends with a **Cross-References** table linking to every guideline domain it depends on | Present and resolves |
| F3 | All `AC-*` IDs in the file are unique and listed in `97-acceptance-criteria.md` | Linter pass |
| F4 | All `OI-*` (open items) and `TBD` markers are tracked in the parent `98-changelog.md` or in a `spec/25-app-issues/` entry | Untracked open item → FAIL |
| F5 | No prose contradicts a row in `00-overview.md` **Locked Decisions** | Inconsistency → FAIL |

---

## Per-File Application Matrix

This matrix shows which sections apply to which existing App spec file. Use it to decide where each check is binding.

| Spec File | A | B | C | D | E | F |
|-----------|:-:|:-:|:-:|:-:|:-:|:-:|
| `00-overview.md` | ✅ | ✅ | — | — | — | ✅ |
| `01-glossary-and-enums.md` | ✅ | ✅ | ✅ | — | — | ✅ |
| `02-database-schema-and-erd.md` | ✅ | ✅ | C9–C14 | ✅ | E2 | ✅ |
| `08-allowlist-and-wildcard-matching.md` | ✅ | ✅ | ✅ | D2, D4 | E1, E5 | ✅ |
| `11-error-management.md` | ✅ | ✅ | C9–C14 | — | — | ✅ |
| `12-logging-strategy.md` | ✅ | ✅ | ✅ | D4 | E1 | ✅ |
| `16-jwt-onboarding-and-token-usage.md` | ✅ | ✅ | ✅ | D4 | E1, E2 | ✅ |
| _Future_ `03-admin-ui.md` | A1, A5 | ✅ | ✅ | — | E1–E8 | ✅ |
| _Future_ `04-rest-api-endpoints.md` | ✅ | ✅ | C9–C14 | — | — | ✅ |
| _Future_ `05-auth-jwt-flow.md` | ✅ | ✅ | ✅ | D4 | E1–E5 | ✅ |
| _Future_ `06-auth-wordpress-bridge.md` | ✅ | ✅ | C1–C8 | — | — | ✅ |
| _Future_ `07-log-push-flow.md` | ✅ | ✅ | ✅ | D4 | E1 | ✅ |
| _Future_ `09-log-retrieval-flow.md` | ✅ | ✅ | ✅ | D4 | — | ✅ |
| _Future_ `10-audit-trail.md` | ✅ | ✅ | C9–C14 | ✅ | — | ✅ |
| _Future_ `13-coding-guidelines-applied.md` | ✅ | ✅ | ✅ | D2, D4 | E1 | ✅ |

---

## Findings Log Template

Append to the audited spec under a `## Consistency Findings` heading.

```
| Check | Status | Excerpt | Corrective Action | Issue Ref |
|-------|--------|---------|-------------------|-----------|
| B1 | FAIL | `$is_active = true;` | Rename to `$isActive` | P2-GL-XX |
| C7 | PASS | — | — | — |
| D4 | FAIL | No index on `AuditTrail.TraceId` | Add `IdxAuditTrail_TraceId` | P2-GL-XX |
```

---

## Acceptance Criteria

| # | ID | Given | When | Then |
|---|-----|-------|------|------|
| 1 | `AC-CHK-01` | Any spec file in `spec/21-git-logs/` | The auditor walks Sections A–F | Every applicable row records PASS / FAIL / N/A — no row left blank |
| 2 | `AC-CHK-02` | A spec sample contains `$user_id` | Section B is run | Row B1 records FAIL with the excerpt |
| 3 | `AC-CHK-03` | A spec sample contains `if (!$order->isValid())` | Section C is run | Row C3 records FAIL |
| 4 | `AC-CHK-04` | A spec defines a custom table with column `created_at` | Section D is run | Row D2 records FAIL |
| 5 | `AC-CHK-05` | A spec introduces a default value without a `Version` bump | Section E is run | Rows E2 + E3 record FAIL |
| 6 | `AC-CHK-06` | All checks pass on a file | Cross-link verifier runs | Exit code 0 and the file is stamped `_Consistency check passed_` |
| 7 | `AC-CHK-07` | A `default` branch is missing on a `match` over `Provider` | Section C is run | Row C12 records FAIL |
| 8 | `AC-CHK-08` | A reserved enum value (e.g., `Provider::GitLab`) lacks a reject rule | Section C is run | Row C13 records FAIL |

---

## Verification

```bash
python3 linter-scripts/check-spec-cross-links.py --root spec --repo-root .
```

**Expected:** exit 0. Any non-zero exit blocks merge.

Optional grep-based pre-checks (run from repo root):

```bash
# B1/B2: underscore identifiers in PHP samples (excluding allowed exemptions)
rg -n '\$[a-z][a-zA-Z0-9]*_[a-zA-Z0-9_]+' spec/21-git-logs

# A10: forbidden uppercase abbreviations
rg -n '\b(ID|URL|JSON|JWT|IP|DB|API|HTTP|HTML|SQL|MD5)\b' spec/21-git-logs

# C2: negative boolean names
rg -n '\$is(Not|No|Non)[A-Z]' spec/21-git-logs

# C3: raw negation on method calls
rg -n 'if \(!\$[a-zA-Z0-9_>-]+\(' spec/21-git-logs
```

Each grep returning zero hits (after subtracting documented exemptions) is a positive signal but not a substitute for the section-by-section walk-through.

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Master Coding Guidelines | [../../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/00-overview.md](../../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/00-overview.md) |
| Naming + Database (master) | [../../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/01-naming-and-database.md](../../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/01-naming-and-database.md) |
| Boolean + Enum (master) | [../../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/02-boolean-and-enum.md](../../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/02-boolean-and-enum.md) |
| Database Naming Conventions | [../../04-database-conventions/01-naming-conventions.md](../../04-database-conventions/01-naming-conventions.md) |
| REST API Format (PascalCase JSON) | [../../04-database-conventions/06-rest-api-format.md](../../04-database-conventions/06-rest-api-format.md) |
| Split-DB Architecture | [../../05-split-db-architecture/00-overview.md](../../05-split-db-architecture/00-overview.md) |
| Seedable Config (CW Config) | [../../06-seedable-config-architecture/00-overview.md](../../06-seedable-config-architecture/00-overview.md) |
| App Spec Index | [./00-overview.md](./00-overview.md) |
| Phase-2 Audit Findings | [../../25-app-issues/01-phase-2-git-logs-audit/00-overview.md](../../25-app-issues/01-phase-2-git-logs-audit/00-overview.md) |
| Triage Format | [../../25-app-issues/00-overview.md](../../25-app-issues/00-overview.md) |

---

## Status

Checklist active. Apply to every existing and future spec file in `spec/21-git-logs/` before marking the file production-ready.
