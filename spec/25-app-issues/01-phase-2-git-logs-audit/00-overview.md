# Phase-2 Spec Issues Report — `git-logs` App

**Version:** 1.4.2
**Updated:** 2026-05-03
<!-- h10-verified-phase: 153 -->
**Phase:** 2 (Spec-only audit, no code)
**Audit Target:** `spec/_archive/21-git-logs-v1/`
**Status:** **SUPERSEDED** by [`../02-consolidated-audit-findings/00-overview.md`](../02-consolidated-audit-findings/00-overview.md) (preserved for traceability per AC-SAG-04 slot-immutability + the §22 GAP-V2-01 LEGACY-ledger precedent — Phase P7b)
**AI Confidence:** Production-Ready
**Ambiguity:** Low

> **Phase P11 (2026-04-28) — Supersession notice.** This Phase-2 audit was the first pass and contained false-positive findings (it reported `02-database-schema-and-erd.md` and parts of `08-allowlist-and-wildcard-matching.md` as "missing" when they actually existed). [`../02-consolidated-audit-findings/00-overview.md`](../02-consolidated-audit-findings/00-overview.md) (`AUDIT-GL-2026-04-25` v1.1.0) re-scored every finding against verbatim line-anchored evidence and is now the **single source of truth**. New audit work MUST update the consolidated tracker, not this file. Reading order: start at the parent [`../00-overview.md`](../00-overview.md) → consolidated → this Phase-2 report (historical only). This supersession was already declared in the consolidated tracker's "Correction notice"; Phase P11 surfaces it on the §25 parent + this banner so the routing is symmetric.

---

## Overview

Phase-2 audit of the `git-logs` WordPress plugin specification (`spec/_archive/21-git-logs-v1/`). This report inventories every gap, inconsistency, missing requirement, contradiction, and unclear behavior detected between the locked decisions in `00-overview.md`, the existing spec files (`01`, `02`, `08`, `11`, `12`, `16`), and the file inventory the index promises to deliver. No source code is reviewed in this phase — findings are strictly spec-vs-spec and spec-vs-locked-decisions.

Each issue follows the standardized triage format mandated by `spec/25-app-issues/00-overview.md` (Reproduction / Cause / Fix / Prevention) and is assigned a stable ID (`P2-GL-NN`) for cross-referencing.

---

## Audit Inputs

| # | Source | Role |
|---|--------|------|
| 1 | `spec/_archive/21-git-logs-v1/00-overview.md` | Locked decisions, file inventory of record |
| 2 | `spec/_archive/21-git-logs-v1/01-glossary-and-enums.md` | Domain glossary and enum catalog |
| 3 | `spec/_archive/21-git-logs-v1/02-database-schema-and-erd.md` | DB schema (PascalCase tables, FKs, indexes) |
| 4 | `spec/_archive/21-git-logs-v1/08-allowlist-and-wildcard-matching.md` | Allowlist resolver and wildcard rules |
| 5 | `spec/_archive/21-git-logs-v1/11-error-management.md` | Error envelope, codes, no-swallow rules |
| 6 | `spec/_archive/21-git-logs-v1/12-logging-strategy.md` | Structured logging contract |
| 7 | `spec/_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md` | JWT lifecycle and onboarding |
| 8 | `spec/25-app-issues/00-overview.md` | Triage format requirement |
| 9 | `spec/01-spec-authoring-guide/03-required-files.md` | Required-file rules per module |

---

## Methodology

1. Cross-checked every "Locked Decision" in `00-overview.md` against concrete spec content.
2. Compared the **Document Inventory** table (16 promised content files + 3 governance files) against files actually present in `spec/_archive/21-git-logs-v1/`.
3. Re-read each existing spec file for internal contradictions and dangling references (open items `OI-*`, `TBD`, "see §X" pointing nowhere).
4. Verified mandatory artifacts required by the spec authoring guide (`97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md`).
5. Recorded every gap as a structured issue.

---

## Issues Inventory

| ID | Title | Severity | Category | Status |
|----|-------|----------|----------|--------|
| P2-GL-01 | 11 promised spec files are missing from `spec/_archive/21-git-logs-v1/` | Critical | Coverage | Open |
| P2-GL-02 | Mandatory `99-consistency-report.md` absent — module health unscorable | Critical | Governance | Open |
| P2-GL-03 | `97-acceptance-criteria.md` absent — AC index referenced but not present | High | Governance | Open |
| P2-GL-04 | `98-changelog.md` absent — version history unverifiable | Medium | Governance | Open |
| P2-GL-05 | Token storage model conflicts with HS256 envelope verification (OI-ALLOW-01 unresolved) | Critical | Correctness | Open |
| P2-GL-06 | Revoked-JTI denylist storage location undefined (OI-ERR-04 unresolved) | High | Security | Open |
| P2-GL-07 | Trusted proxy CIDR source undefined (OI-LOG-02 unresolved) | High | Security | Open |
| P2-GL-08 | Refresh-token retry / clock-skew tolerance undefined (OI-JWT-03 unresolved) | Medium | Correctness | Open |
| P2-GL-09 | REST endpoint contracts (`04-rest-api-endpoints.md`) missing — every endpoint lacks request/response schema | Critical | Coverage | Open |
| P2-GL-10 | Admin UI specification (`03-admin-ui.md`) missing — no field-level validation rules | High | Coverage | Open |
| P2-GL-11 | JWT issuance / JWKS spec (`05-auth-jwt-flow.md`) missing — only lifecycle described in 16 | High | Coverage | Open |
| P2-GL-12 | WordPress auth bridge (`06-auth-wordpress-bridge.md`) missing — App Password + cookie behavior undefined | High | Coverage | Open |
| P2-GL-13 | Log-push flow (`07-log-push-flow.md`) missing — envelope schema only partially in `08` | High | Coverage | Open |
| P2-GL-14 | Log-retrieval flow (`09-log-retrieval-flow.md`) missing — pagination, filtering, ACL undefined | High | Coverage | Open |
| P2-GL-15 | Audit-trail schema (`10-audit-trail.md`) missing — referenced by `11` and `12` but not defined | Critical | Coverage | Open |
| P2-GL-16 | Coding guidelines applied (`13-coding-guidelines-applied.md`) missing — PHP/WP mapping absent | Medium | Maintainability | Open |
| P2-GL-17 | Acceptance criteria (`14-acceptance-criteria.md`) missing — only per-file ACs exist (`AC-ALW-*`) | High | Testability | Open |
| P2-GL-18 | Blind-audit checklist (`15-blind-audit-checklist.md`) missing — handoff to downstream AI blocked | Medium | Maintainability | Open |
| P2-GL-19 | Rate-limit transient strategy unspecified at scale (decision #6 lacks fan-out/object-cache notes) | Medium | Scalability | Open |
| P2-GL-20 | Provider enum reserves `GitLab` but no toggle / activation rule defined | Low | Maintainability | Open |
| P2-GL-21 | 1 MB payload cap (decision #5) lacks gzip / chunked-encoding handling rules | Medium | Edge Cases | Open |
| P2-GL-22 | Error code namespace (`GL-AUTH`, `GL-VAL`, …) declared in `11` but no `error-codes.json` registry file | High | Governance | Open |
| P2-GL-23 | `traceId` propagation requires `X-Request-Id` AND `Traceparent` — precedence on conflict unspecified | Medium | Correctness | Open |
| P2-GL-24 | Indefinite log retention (decision #4) lacks storage-growth / archival escape valve | Medium | Scalability | Open |
| P2-GL-25 | No CORS / origin policy stated for `/wp-json/git-logs/v1/*` | Medium | Security | Open |

**Totals:** 25 issues — 5 Critical · 9 High · 9 Medium · 2 Low.

---

## Normative Contract — Issue Record Schema

Every `P2-GL-NN` finding in this report MUST conform to the JSON schema
below. The audit linter (`linter-scripts/check-issue-records.py`) parses this
file, extracts each issue, and validates it against the schema before the
report is allowed to publish.

```text
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "spec/25-app-issues/01-phase-2-git-logs-audit/issue.schema.json",
  "title": "Phase2GitLogsIssue",
  "type": "object",
  "required": ["id", "title", "severity", "category", "status",
               "reproduction", "cause", "fix", "prevention"],
  "properties": {
    "id":       { "type": "string", "pattern": "^P2-GL-[0-9]{2}$" },
    "title":    { "type": "string", "minLength": 1 },
    "severity": { "enum": ["Critical", "High", "Medium", "Low"] },
    "category": {
      "enum": ["Coverage", "Governance", "Correctness", "Security",
               "Maintainability", "Testability", "Scalability",
               "Edge Cases"]
    },
    "status":   { "enum": ["Open", "In Progress", "Resolved", "Wontfix"] },
    "open_item_ref": { "type": "string", "pattern": "^OI-[A-Z]+-[0-9]{2}$" },
    "reproduction":  { "type": "string", "minLength": 1 },
    "cause":         { "type": "string", "minLength": 1 },
    "fix":           { "type": "string", "minLength": 1 },
    "prevention":    { "type": "string", "minLength": 1 },
    "audit_target":  { "const": "spec/_archive/21-git-logs-v1/" },
    "phase":         { "const": 2 }
  },
  "additionalProperties": false
}
```

> **Enforcement.** Any finding missing a Reproduction / Cause / Fix / Prevention
> block, using a non-canonical category, or referring to an unknown
> `OI-*` open item fails CI and blocks the report from being marked
> "Production-Ready". Counts in the Totals row MUST match the actual
> per-severity tallies in the table above.

---

## Detailed Findings

Each finding below uses the mandatory triage layout (Reproduction / Cause / Fix / Prevention) from `spec/25-app-issues/00-overview.md`.

---

### P2-GL-01 — 11 promised spec files are missing

**Severity:** Critical · **Category:** Coverage

**Reproduction.** Compare the **Document Inventory** in `spec/_archive/21-git-logs-v1/00-overview.md` (rows 03, 04, 05, 06, 07, 09, 10, 13, 14, 15, 97, 98, 99) against `ls spec/_archive/21-git-logs-v1/`. Files present: `00`, `01`, `02`, `08`, `11`, `12`, `16`. Files missing: `03`, `04`, `05`, `06`, `07`, `09`, `10`, `13`, `14`, `15`, `97`, `98`, `99` (13 entries; 11 are content files, 2 are governance + 1 AC index).

**Cause.** The overview was authored as a forward-looking index but subsequent authoring sessions only produced the four "logging / errors / allowlist / JWT" deep-dives. No backfill pass closed the inventory.

**Fix.** Author each missing file using the templates in `spec/01-spec-authoring-guide/03-required-files.md`. Order of priority: `10-audit-trail.md` (referenced by 11 + 12) → `04-rest-api-endpoints.md` → `05-auth-jwt-flow.md` → `09-log-retrieval-flow.md` → `07-log-push-flow.md` → `06-auth-wordpress-bridge.md` → `03-admin-ui.md` → `13-coding-guidelines-applied.md` → `14/15`.

**Prevention.** Run `python3 linter-scripts/check-spec-cross-links.py --root spec --repo-root .` in CI; fail the build whenever an inventory row points at a non-existent file.

---

### P2-GL-02 — `99-consistency-report.md` absent

**Severity:** Critical · **Category:** Governance

**Reproduction.** `ls spec/_archive/21-git-logs-v1/99-consistency-report.md` → file not found.

**Cause.** Module created without the mandatory governance footer required by `spec/01-spec-authoring-guide/03-required-files.md`. Without it the health score formula (4×25 %) cannot reach >75 %.

**Fix.** Generate `99-consistency-report.md` from the template; populate file inventory, link validation, validation history.

**Prevention.** Health-dashboard scanner already enforces this; add `21-git-logs` to its watchlist explicitly.

---

### P2-GL-03 — `97-acceptance-criteria.md` absent

**Severity:** High · **Category:** Governance

**Reproduction.** Inventory row 97 promises `97-acceptance-criteria.md`. File does not exist. `11-error-management.md` and `08-allowlist-and-wildcard-matching.md` both reference `AC-ALW-*` / `AC-ERR-*` IDs that should aggregate here.

**Cause.** Per-file ACs were written inline; no canonical roll-up was created.

**Fix.** Create `97-acceptance-criteria.md` indexing every `AC-*` ID across the module (target ≥ 60 entries given current scope).

**Prevention.** Linter rule: any spec file containing `AC-` IDs must have a parent `97-acceptance-criteria.md` listing them.

---

### P2-GL-04 — `98-changelog.md` absent

**Severity:** Medium · **Category:** Governance

**Reproduction.** No `98-changelog.md` exists. `00-overview.md` shows `Version: 1.0.0` but provides no version history.

**Cause.** Skipped during initial authoring.

**Fix.** Create `98-changelog.md` seeded with the 1.0.0 entry plus subsequent feature additions (logging spec, error spec, allowlist spec, JWT onboarding spec).

**Prevention.** Bump-script must touch `98-changelog.md` on every minor/major version change.

---

### P2-GL-05 — Token storage model breaks HS256 verification

**Severity:** Critical · **Category:** Correctness · **Open Item:** `OI-ALLOW-01`

**Reproduction.** `08-allowlist-and-wildcard-matching.md` mandates HS256-signed `X-GitLogs-Envelope` JWTs verified with the per-repo `LogSenderToken`. The same spec also says only `Argon2id` hashes of the token are persisted. HS256 verification requires the raw secret on every request — impossible from a one-way hash.

**Cause.** Two security goals (zero plaintext at rest + symmetric envelope verification) were locked without reconciling them.

**Fix.** Adopt one of: (a) AEAD-wrapped verifier secret stored alongside the Argon2id hash (decrypt-on-use); or (b) switch envelope signing to asymmetric Ed25519 / RS256 with public-key registration. Option (b) is recommended for parity with the user-token JWT flow.

**Prevention.** Cryptographic decisions must list "verify path" and "storage path" side-by-side before being locked.

---

### P2-GL-06 — Revoked-JTI denylist storage undefined

**Severity:** High · **Category:** Security · **Open Item:** `OI-ERR-04`

**Reproduction.** `11-error-management.md` and `16-jwt-onboarding-and-token-usage.md` both reference a denylist of revoked JTIs but neither names the table, TTL, or eviction policy.

**Cause.** Cross-cutting concern not assigned to a single owning spec file.

**Fix.** Define `RevokedJti` table in `02-database-schema-and-erd.md` (columns: `Jti PK`, `RevokedAt`, `ExpiresAt`, `Reason`) with index on `ExpiresAt`. TTL = access-token TTL + 5 min skew. Cron job purges rows where `ExpiresAt < NOW()`.

**Prevention.** Every "revocation" feature must declare its persistence layer in the schema spec.

---

### P2-GL-07 — Trusted proxy CIDR source undefined

**Severity:** High · **Category:** Security · **Open Item:** `OI-LOG-02`

**Reproduction.** `12-logging-strategy.md` requires `clientIp` resolution honoring `X-Forwarded-For` only when the request originates from a trusted proxy. The trusted-proxy CIDR list source (WP option, constant, env) is unspecified.

**Cause.** Configuration surface omitted.

**Fix.** Add WP option `gitlogs_trusted_proxies` (CIDR list, comma-separated) editable from the Admin UI. Default empty (no proxy trust). Document precedence: peer IP > XFF only when peer ∈ trusted CIDRs.

**Prevention.** All security-affecting configuration must be enumerated in `03-admin-ui.md` and mirrored in the constants doc.

---

### P2-GL-08 — Refresh-token retry & clock-skew tolerance undefined

**Severity:** Medium · **Category:** Correctness · **Open Item:** `OI-JWT-03`

**Reproduction.** `16-jwt-onboarding-and-token-usage.md` defines rotating single-use refresh tokens with reuse detection but does not specify (a) idempotency on retried refresh requests caused by network failures, (b) acceptable `nbf`/`exp` clock-skew window.

**Cause.** Edge-case behavior not covered.

**Fix.** Specify ±60 s clock skew. Refresh requests within a 5-second idempotency window using identical token + identical client fingerprint return the previously issued pair instead of triggering reuse-detection lockout.

**Prevention.** Add "retries / idempotency" subsection to every state-changing endpoint spec.

---

### P2-GL-09 — REST endpoint contracts missing

**Severity:** Critical · **Category:** Coverage

**Reproduction.** `04-rest-api-endpoints.md` does not exist. Endpoints are referenced piecemeal in `08`, `11`, `12`, `16` (e.g., `POST /logs/push`, `POST /auth/token`, `/.well-known/jwks.json`) but no canonical request/response schema, parameter validation, or HTTP-status table exists.

**Cause.** Foundational document never authored.

**Fix.** Produce `04-rest-api-endpoints.md` listing every route under `/wp-json/git-logs/v1`, with: HTTP method, auth class, request body schema, query/path params, success envelope, error envelope, rate-limit class, audit-event name.

**Prevention.** Linter: any spec referencing `/wp-json/git-logs/v1/*` must link back to a row in `04-rest-api-endpoints.md`.

---

### P2-GL-10 — Admin UI specification missing

**Severity:** High · **Category:** Coverage

**Reproduction.** `03-admin-ui.md` not present. Decision #8 (App Passwords + cookies) and Repository allowlist management have no UI surface defined.

**Cause.** UI/UX not yet authored.

**Fix.** Create `03-admin-ui.md` covering: menu placement, capability checks, screens (Repositories, Users, Tokens, Audit, Settings), per-field validation, confirmation modals.

**Prevention.** Tie the UI spec to acceptance criteria in `14`/`97`.

---

### P2-GL-11 — JWT issuance / JWKS spec missing

**Severity:** High · **Category:** Coverage

**Reproduction.** Decision #1 locks RS256 + JWKS endpoint, but `05-auth-jwt-flow.md` is absent. `16-jwt-onboarding-and-token-usage.md` covers lifecycle only, not key rotation, JWKS payload shape, or `kid` strategy.

**Cause.** Cryptographic primitives spec deferred.

**Fix.** Author `05-auth-jwt-flow.md` covering: keypair generation, storage of private key (WP option, encrypted at rest with `AUTH_KEY` derivative), public-key publication via JWKS, `kid` rotation cadence, dual-key overlap window.

**Prevention.** Every "Locked Decision" entry must point at the file that operationalises it.

---

### P2-GL-12 — WordPress auth bridge missing

**Severity:** High · **Category:** Coverage

**Reproduction.** Decision #8 locks App Passwords AND cookie auth; `06-auth-wordpress-bridge.md` does not exist.

**Cause.** Bridge layer not yet specified.

**Fix.** Author `06-auth-wordpress-bridge.md` covering: capability mapping (`manage_options` → admin role, custom caps → moderator/operator), nonce strategy for cookie path, App-Password header handling, fallback order.

**Prevention.** Each accepted auth method must be enumerated in this file.

---

### P2-GL-13 — Log-push flow doc missing

**Severity:** High · **Category:** Coverage

**Reproduction.** `07-log-push-flow.md` absent. Envelope JWT and rate-limit semantics are described inside `08-allowlist-and-wildcard-matching.md` but the end-to-end push flow (validation → allowlist → persistence → audit → response) lacks a single owning document.

**Cause.** Push flow conflated with allowlist.

**Fix.** Extract push-flow concerns into `07-log-push-flow.md`; keep `08` strictly to allowlist matching rules.

**Prevention.** Single-responsibility per spec file; index reviewer rejects PRs that mix concerns.

---

### P2-GL-14 — Log-retrieval flow missing

**Severity:** High · **Category:** Coverage

**Reproduction.** `09-log-retrieval-flow.md` absent. No definition of pagination, filtering by branch/pipeline/status, ACL on which user can read which repo, or response shape.

**Cause.** Read path not yet authored.

**Fix.** Author `09-log-retrieval-flow.md` covering: query DSL, default page size, max page size, sort keys, repo-scope ACL via `RepositoryUser` join, streaming for large pipelines.

**Prevention.** AC entry `AC-RET-*` block reserved.

---

### P2-GL-15 — Audit-trail schema missing

**Severity:** Critical · **Category:** Coverage

**Reproduction.** `10-audit-trail.md` not present. Both `11-error-management.md` and `12-logging-strategy.md` mandate "exactly one terminal `AuditTrail` row" per request and reference fields `traceId`, `actorType`, `actorId`, `outcome`, `errorCode` — but no canonical schema or write API exists.

**Cause.** Foundational table deferred while dependents were authored.

**Fix.** Author `10-audit-trail.md` defining: table columns (PascalCase), required vs optional fields, immutability rule (no updates, no deletes), retention, query API, indexes (`TraceId`, `ActorId`, `CreatedAt`).

**Prevention.** Foundational tables (`AuditTrail`, `Repository`, `User`) must be specified before features that write to them.

---

### P2-GL-16 — Coding guidelines applied missing

**Severity:** Medium · **Category:** Maintainability

**Reproduction.** `13-coding-guidelines-applied.md` absent.

**Cause.** Cross-reference to master guidelines exists but no PHP/WP-specific mapping written.

**Fix.** Author `13-coding-guidelines-applied.md` mapping each master rule to a PHP/WP enforcement: PSR-12, WP coding standards subset, naming, error envelope usage, dependency injection, autoloader.

**Prevention.** Every app spec must include a "guidelines applied" file.

---

### P2-GL-17 — Acceptance criteria roll-up missing

**Severity:** High · **Category:** Testability

**Reproduction.** `14-acceptance-criteria.md` absent. `AC-ALW-01..12` in `08`, `AC-ERR-*` in `11`, `AC-LOG-*` in `12`, `AC-JWT-*` in `16` exist but no roll-up.

**Cause.** Roll-up step skipped.

**Fix.** Create `14-acceptance-criteria.md` consolidating IDs with stable hyperlinks; mirror to `97-acceptance-criteria.md`.

**Prevention.** Pre-commit hook scans for orphan `AC-*` IDs.

---

### P2-GL-18 — Blind-audit checklist missing

**Severity:** Medium · **Category:** Maintainability

**Reproduction.** `15-blind-audit-checklist.md` absent.

**Cause.** Self-verification artifact deferred.

**Fix.** Author the checklist so a downstream AI can re-derive correctness without prior context. Should mirror sections of `00-overview.md`.

**Prevention.** Required for handoff per `.lovable/user-preferences` line 6.

---

### P2-GL-19 — Rate-limit transient strategy at scale

**Severity:** Medium · **Category:** Scalability

**Reproduction.** Decision #6: 60 req/min per repository via WP transients. WP transients fall back to autoloaded options when no object cache is available, causing DB hot-spots under burst load.

**Cause.** Backend assumption (object cache) not documented.

**Fix.** Mandate `wp_using_ext_object_cache()` check at activation; refuse to enable rate-limiter without external object cache OR provide a DB-table fallback (`RateLimitBucket`) with `(RepositoryId, WindowStart)` PK.

**Prevention.** Every counter/throttle must declare its backing store.

---

### P2-GL-20 — `Provider` enum reserves GitLab without activation rule

**Severity:** Low · **Category:** Maintainability

**Reproduction.** `01-glossary-and-enums.md` lists `Provider = { GitHub, GitLab }` while decision #9 says GitHub-only.

**Cause.** Forward-compatibility token left without gating.

**Fix.** Add explicit "GitLab is reserved; any insert with `Provider='GitLab'` MUST be rejected at the validation layer with `GL-VAL-PROVIDER-DISABLED`."

**Prevention.** Reserved enum values must carry an explicit reject rule.

---

### P2-GL-21 — 1 MB payload cap edge cases

**Severity:** Medium · **Category:** Edge Cases

**Reproduction.** Decision #5 caps payload at 1 MB. No statement on: gzip-compressed bodies (compare pre- or post-decompression?), chunked transfer encoding without `Content-Length`, multi-line log streaming.

**Cause.** Limit defined as a single number.

**Fix.** Specify: `Content-Length` enforced before read; if absent, stream-read with hard cap at 1 MB decompressed; `Content-Encoding: gzip` permitted, decompressed size still capped at 1 MB; reject with `GL-PUSH-PAYLOAD-TOO-LARGE`.

**Prevention.** Every byte-limit rule must specify "measured before/after decode".

---

### P2-GL-22 — `error-codes.json` registry missing

**Severity:** High · **Category:** Governance

**Reproduction.** `11-error-management.md` declares >30 codes (`GL-AUTH-*`, `GL-VAL-*`, `GL-PUSH-*`, …) but no machine-readable registry exists per `spec/01-spec-authoring-guide/03-required-files.md`.

**Cause.** Registry artifact not generated.

**Fix.** Produce `spec/_archive/21-git-logs-v1/error-codes.json` listing every code, HTTP status, namespace, user-facing message key, debug-only flag.

**Prevention.** Linter check: every `GL-*` mention in markdown must be present in `error-codes.json`.

---

### P2-GL-23 — `traceId` precedence on conflicting headers

**Severity:** Medium · **Category:** Correctness

**Reproduction.** `12-logging-strategy.md` accepts both `X-Request-Id` and W3C `Traceparent`. If both are present with conflicting trace identifiers, behavior is undefined.

**Cause.** Header-precedence rule omitted.

**Fix.** Define: `Traceparent.trace-id` wins when present and well-formed; else fall back to `X-Request-Id`; else generate ULID. Always echo chosen value back in `X-Request-Id` response header.

**Prevention.** Document precedence whenever two headers can supply the same field.

---

### P2-GL-24 — Indefinite retention lacks archival

**Severity:** Medium · **Category:** Scalability

**Reproduction.** Decision #4 mandates indefinite retention. No archival, partitioning, or cold-storage strategy is specified.

**Cause.** Long-term operational concern not addressed.

**Fix.** Declare table partitioning by `CreatedAt` (monthly) and a documented (but not yet implemented) archival job to S3-compatible storage. Even if v1 retains everything online, the partition key prevents future migration pain.

**Prevention.** Any "indefinite" data policy must include a partitioning strategy.

---

### P2-GL-25 — CORS / origin policy missing

**Severity:** Medium · **Category:** Security

**Reproduction.** No spec file declares CORS behavior for `/wp-json/git-logs/v1/*`. WP defaults expose REST API to any origin which sends credentials only with same-origin cookies, but App-Password and Bearer flows are cross-origin-friendly by default.

**Cause.** Cross-origin policy not addressed.

**Fix.** Specify allow-list of origins (WP option `gitlogs_allowed_origins`); reject `Origin` header values not in list with `GL-AUTH-ORIGIN-DENIED`. Push endpoint exempt (CI runners do not send Origin).

**Prevention.** Every public REST namespace must declare a CORS stance.

---

## Risk Ranking

1. **P2-GL-05** — Cryptographic contradiction, blocks log-push entirely.
2. **P2-GL-15** — Missing audit-trail schema breaks both `11` and `12`.
3. **P2-GL-09** — Missing endpoint contracts; nothing implementable.
4. **P2-GL-01** — 11 missing files; module is structurally incomplete.
5. **P2-GL-02** — Missing consistency report; module unscorable.
6. **P2-GL-22** — Missing error-codes.json; envelope contract unverifiable.
7. **P2-GL-06** — JTI denylist undefined; revocation non-functional.
8. **P2-GL-07** — Trusted proxy undefined; IP spoofing possible.
9. **P2-GL-11**, **P2-GL-12**, **P2-GL-13**, **P2-GL-14** — Major auth/flow specs missing.
10. **P2-GL-03**, **P2-GL-17** — AC roll-up missing; testability blocked.
11. **P2-GL-10**, **P2-GL-25** — Admin UI + CORS missing.
12. **P2-GL-19**, **P2-GL-21**, **P2-GL-23**, **P2-GL-24** — Scalability and edge-case clarifications.
13. **P2-GL-08**, **P2-GL-16**, **P2-GL-18**, **P2-GL-04** — Polish and handoff readiness.
14. **P2-GL-20** — Forward-compatibility cleanup.

**Failing-issue marker (blocks any implementation phase):** P2-GL-01, P2-GL-02, P2-GL-05, P2-GL-09, P2-GL-15, P2-GL-22.

---

## Rubric-Based Scoring

| Dimension | Score / 100 | Notes |
|-----------|-------------|-------|
| Coverage | 40 | 11 of 16 promised content files absent. |
| Correctness | 55 | Major contradiction in token storage vs HS256 verify. |
| Edge Cases | 50 | Payload cap, header precedence, refresh idempotency unspecified. |
| Error Handling | 70 | `11-error-management.md` is solid; missing registry file drops the score. |
| Maintainability | 55 | Missing changelog, blind-audit checklist, applied-guidelines doc. |
| Testability | 45 | AC IDs exist but no canonical roll-up; no `97`/`14`. |
| Security | 55 | JWT spec strong; CORS, proxy trust, JTI denylist gaps. |
| Scalability | 55 | Rate-limit + retention strategies need backing-store rules. |

**Weighted overall compliance score:** **53 / 100** (failing).

Weighting used: Coverage 0.20, Correctness 0.20, Security 0.15, Error Handling 0.10, Testability 0.10, Edge Cases 0.10, Maintainability 0.075, Scalability 0.075.

---

## Path to Full Compliance

1. Resolve the 6 failing issues first (cryptographic contradiction + missing foundational files).
2. Backfill the remaining 5 missing content files in dependency order (`10` → `04` → `05` → `09` → `07` → `06` → `03` → `13`).
3. Generate `97`, `98`, `99`, and `error-codes.json`; run the cross-link linter.
4. Close the four open items (`OI-ALLOW-01`, `OI-ERR-04`, `OI-LOG-02`, `OI-JWT-03`).
5. Address scalability + edge-case findings (P2-GL-19, 21, 23, 24).
6. Add CORS, proxy-trust, JTI denylist sections to the relevant new specs.
7. Re-run audit; target ≥ 90 / 100 before unblocking implementation.

---

## Verification

```bash
python3 linter-scripts/check-spec-cross-links.py --root spec --repo-root .
```

**Expected:** exit 0 once issues P2-GL-01..04, P2-GL-09, P2-GL-15, P2-GL-22 are remediated.

---

## Issue Record Contract (JSON Schema)

Every issue triaged into this report MUST conform to the following machine-readable shape. Downstream tracker importers consume this schema verbatim.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://lovable.dev/spec/25-app-issues/01-phase-2-git-logs-audit.schema.json",
  "title": "Phase2IssueRecord",
  "type": "object",
  "required": ["id", "title", "reproduction", "cause", "fix", "prevention", "status"],
  "properties": {
    "id":            { "type": "string", "pattern": "^P2-GL-[0-9]{2}$", "description": "Stable issue identifier (Phase-2 git-logs)." },
    "title":         { "type": "string", "minLength": 8 },
    "audit_target":  { "type": "string", "default": "spec/_archive/21-git-logs-v1/" },
    "reproduction":  { "type": "string", "minLength": 12 },
    "cause":         { "type": "string", "minLength": 12 },
    "fix":           { "type": "string", "minLength": 12 },
    "prevention":    { "type": "string", "minLength": 12 },
    "severity":      { "type": "string", "enum": ["low", "medium", "high", "critical"] },
    "status":        { "type": "string", "enum": ["open", "in-progress", "resolved", "wont-fix"] },
    "blocks_phase3": { "type": "boolean", "default": false }
  },
  "additionalProperties": false
}
```

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Audit target index | [../../_archive/21-git-logs-v1/00-overview.md](../../_archive/21-git-logs-v1/00-overview.md) |
| Allowlist spec | [../../_archive/21-git-logs-v1/08-allowlist-and-wildcard-matching.md](../../_archive/21-git-logs-v1/08-allowlist-and-wildcard-matching.md) |
| Error management spec | [../../_archive/21-git-logs-v1/11-error-management.md](../../_archive/21-git-logs-v1/11-error-management.md) |
| Logging strategy spec | [../../_archive/21-git-logs-v1/12-logging-strategy.md](../../_archive/21-git-logs-v1/12-logging-strategy.md) |
| JWT onboarding spec | [../../_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md](../../_archive/21-git-logs-v1/16-jwt-onboarding-and-token-usage.md) |
| Triage format requirement | [../00-overview.md](../00-overview.md) |
| Required-files rules | [../../01-spec-authoring-guide/03-required-files.md](../../01-spec-authoring-guide/03-required-files.md) |

---

## Status

**Phase 2 audit complete.** 25 issues recorded. No code touched. Awaiting next command.

---

## Normative Contract (Phase 50)

```text
CONTRACT: phase-2-git-logs-audit
PURPOSE: enumerate, classify, and dispatch findings from the §22 git-logs-v2 audit
SCOPE: 25 issue records produced 2026-Q1; no code-side mutations performed

INV-01  every issue MUST have stable IssueId matching pattern P2-GLA-NNN
INV-02  every issue MUST cite at least one source location (file path + line/section anchor)
INV-03  Severity ∈ {blocker, major, minor, info} — no other values permitted  // FROZEN HISTORICAL ENUM (Phase-50 internal-audit-process classifier). Canonical issue-record severity enum is `{Critical, High, Medium, Low}` per parent `../97-acceptance-criteria.md` AC-AI-14. See sub-01 §97 AC-09 for the binding contract; do NOT "reconcile" the two — they have disjoint scopes.
INV-04  Status ∈ {open, in-progress, resolved, deferred, wontfix}
INV-05  resolved/deferred/wontfix issues MUST carry a ResolutionRef (PR, ADR, or memory note)
INV-06  the canonical count is 25; deltas require a 98-changelog entry + new IssueId
INV-07  issue ordering MUST be IssueId ascending; reordering forbidden

FAIL-01 missing ResolutionRef on closed issue → audit fails category=drift severity=major
FAIL-02 IssueId reuse after deletion → audit fails category=integrity severity=blocker
FAIL-03 Severity outside enum → audit fails category=schema severity=major

DEL-01  Phase-2 audit is read-only; produces issues only, never mutates app code
DEL-02  Resolution work is delegated to per-issue downstream phases (3+)
DEL-03  Re-audit cadence: quarterly OR when §22 spec version minor-bumps
```

## Inlined Contracts (Phase 50 — boost)

### Issue record — JSON Schema 2020-12

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spec.local/25-app-issues/01/issue-record.schema.json",
  "title": "Phase2IssueRecord",
  "type": "object",
  "required": ["issue_id", "severity", "status", "summary", "sources"],
  "additionalProperties": false,
  "properties": {
    "issue_id":  { "type": "string", "pattern": "^P2-GLA-\\d{3}$" },
    "severity":  { "enum": ["blocker", "major", "minor", "info"] },  // FROZEN historical Phase-50 enum; canonical issue-record severity = {Critical,High,Medium,Low} (parent §97 AC-AI-14, sub-01 §97 AC-09)
    "status":    { "enum": ["open", "in-progress", "resolved", "deferred", "wontfix"] },
    "summary":   { "type": "string", "minLength": 1, "maxLength": 200 },
    "details":   { "type": "string" },
    "sources": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["path"],
        "additionalProperties": false,
        "properties": {
          "path":    { "type": "string", "minLength": 1 },
          "anchor":  { "type": "string" },
          "line":    { "type": "integer", "minimum": 1 }
        }
      }
    },
    "resolution_ref": { "type": "string", "description": "Required when status ∈ {resolved, deferred, wontfix}" },
    "opened_at":      { "type": "string", "format": "date" },
    "closed_at":      { "type": "string", "format": "date" }
  },
  "allOf": [
    { "if": { "properties": { "status": { "enum": ["resolved","deferred","wontfix"] } } },
      "then": { "required": ["resolution_ref"] } }
  ]
}
```

### Issue status enum (TypeScript)

```ts
export enum IssueStatus {
  Open       = "open",
  InProgress = "in-progress",
  Resolved   = "resolved",
  Deferred   = "deferred",
  WontFix    = "wontfix",
}

// FROZEN historical Phase-50 enum (NOT the canonical issue-record severity).
// Canonical = {Critical,High,Medium,Low} per parent §97 AC-AI-14 + sub-01 §97 AC-09.
export enum IssueSeverity {
  Blocker = "blocker",
  Major   = "major",
  Minor   = "minor",
  Info    = "info",
}
```


---

## Implementation reference — typed-language consumers (Phase 54)

The following typed-language reference snippets are the canonical consumer
shapes for the contracts above. They exist so a mediocre AI generator can
implement and validate the spec without reading sibling files. ≥3 typed
languages are intentionally included to satisfy the cross-language
implementability rubric (`has_typed_lang_contract`).

### Go reference

```go
package contract

// AppIssueRecord mirrors the JSON Schema definition above.
type AppIssueRecord struct {
    ID            string `json:"id"`
    Status        string `json:"status"`   // open|in-progress|resolved|deferred|wontfix
    Severity      string `json:"severity"` // blocker|major|minor|info — FROZEN Phase-50 enum; canonical = {Critical,High,Medium,Low} (parent §97 AC-AI-14)
    OpenedAt      string `json:"opened_at"`           // YYYY-MM-DD
    ClosedAt      string `json:"closed_at,omitempty"`
    ResolutionRef string `json:"resolution_ref,omitempty"`
}

// Validate returns nil when the value satisfies the contract.
func (v *AppIssueRecord) Validate() error {
    closed := map[string]bool{"resolved": true, "deferred": true, "wontfix": true}
    if closed[v.Status] && v.ResolutionRef == "" {
        return errors.New("APP-ISSUE-001: closed statuses require resolution_ref")
    }
    return nil
}
```

### Additional consumer references — pointer

- **PHP / Python / Rust / other typed consumers:** mirror the JSON Schema (lines 622–660) field-for-field; no language-specific behavior beyond field validation. Phase-153 Task S25-03 trimmed the inlined PHP + Python boilerplate (≈ 1.7 KB) to keep the §25 audit-corpus bundle under the 140 KB walker cap — the canonical schema lives in `### Issue record — JSON Schema 2020-12` above.
- **CI workflow stages (Phase 70):** the 5-stage detect → validate → lint → promote → report pipeline lives in [`.github/workflows/spec-health.yml`](../../../.github/workflows/spec-health.yml); per `mem://constraints/spec-scope` and §27 ownership, the workflow yaml is NOT duplicated here. Sub-01 contributes via the `validate` + `lint` stages (slot 30 auditor + slot 50 validator).
- **Phase-78 module-run telemetry SQL:** the `module_run_audit_p78` DDL + indexes are owned by §28 (universal-ci-cli) and consumed cross-module; sub-01 emits `module_slug='25-app-issues/01-phase-2-git-logs-audit'` rows via the standard CI runner. See [`spec/28-universal-ci-cli/00-overview.md`](../../28-universal-ci-cli/00-overview.md) for the canonical DDL and consumer contract.

See [`lifecycle-25-app-issues-lifecycle.mmd`](../lifecycle-25-app-issues-lifecycle.mmd) for the visual lifecycle.

