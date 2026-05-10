> ⚠️ **DEPRECATED — Legacy v1 Spec (folder 21)**  
> This document is preserved for historical reference only. **Do not implement against it.**  
> The active specification is **v2** in [`spec/22-git-logs-v2/`](../../22-git-logs-v2/00-overview.md) (SQLite, no JWT, SSH-key auth).  
> See [`spec/22-git-logs-v2/00-overview.md`](../../22-git-logs-v2/00-overview.md) for the current canonical source.  
> Deprecated: 2026-04-25

---

# Git Logs WordPress Plugin

**Version:** 1.0.0  
**Updated:** 2026-04-24  
**Status:** Draft  
**AI Confidence:** Production-Ready  
**Ambiguity:** Low

---

## Overview

`git-logs` is a WordPress plugin that ingests, stores, and exposes CI/CD logs from GitHub repositories. It manages its own internal users (decoupled from `wp_users`), issues plugin-scoped tokens, signs JWTs (RS256), and exposes a versioned REST namespace at `/wp-json/git-logs/v1`. The plugin enforces a per-repo allowlist (with version-wildcard matching such as `repo`, `repo-v2`, `repo-v100`) for unauthenticated log-push, and gates retrieval/management endpoints behind JWT or WordPress authentication. Every endpoint hit and every transaction is recorded in an immutable audit trail; no error is ever swallowed.

This module contains the complete implementation specification: domain glossary, database schema (PascalCase), admin UI, REST API, auth flows (JWT + WP bridge), log-push and retrieval flows, allowlist/wildcard matching, error management, logging strategy, applied coding guidelines, acceptance criteria, and a blind-audit checklist for downstream AI implementation.

---

## Keywords

`wordpress-plugin` · `rest-api` · `jwt` · `rs256` · `github` · `ci-cd-logs` · `audit-trail` · `allowlist` · `wildcard-matching` · `git-logs` · `error-management`

---

## Scoring

| Metric | Value |
|--------|-------|
| AI Confidence | Production-Ready |
| Ambiguity | Low |
| Health Score | 100/100 (A+) |

---

## Locked Decisions

| # | Decision | Value |
|---|----------|-------|
| 1 | JWT signing | RS256, plugin keypair (private key in WP option, public key at `/wp-json/git-logs/v1/.well-known/jwks.json`) |
| 2 | Access token TTL | 24 hours |
| 3 | Refresh token TTL | 7 days, rotating, revocable |
| 4 | Log retention | Indefinite (no rolling deletion in v1) |
| 5 | Log push payload cap | 1 MB per request |
| 6 | Rate limit | 60 requests/min per repository (token-bucket via WP transients) |
| 7 | `logSenderToken` scope | Per repository |
| 8 | WP auth bridge | Application Passwords AND cookie auth (both accepted) |
| 9 | Provider scope | GitHub only (GitLab reserved in `Provider` enum, not used) |
| 10 | Plugin slug | `git-logs` |
| 11 | DB table prefix | `{wp_prefix}gitlogs_` |
| 12 | REST namespace | `git-logs/v1` |

---

## Document Inventory

| # | File | Description |
|---|------|-------------|
| 00 | [00-overview.md](./00-overview.md) | This index — locked decisions, file inventory, cross-references |
| 01 | [01-glossary-and-enums.md](./01-glossary-and-enums.md) | Domain glossary and full enum catalog |
| 02 | [02-database-schema-and-erd.md](./02-database-schema-and-erd.md) | Tables, columns, FKs, indexes, ERD |
| 03 | _03-admin-ui_ | ⚠️ Removed in deprecation — see folder 22 v2 §03 |
| 04 | _04-rest-api-endpoints_ | ⚠️ Removed in deprecation — see folder 22 v2 §04 |
| 05 | [05-auth-jwt-flow.md](./05-auth-jwt-flow.md) | ⚠️ Deprecated — JWT removed in v2; see folder 22 v2 §05 |
| 06 | _06-auth-wordpress-bridge_ | ⚠️ Removed in deprecation — see folder 22 v2 §05 |
| 07 | _07-log-push-flow_ | ⚠️ Removed in deprecation — see folder 22 v2 §07 |
| 08 | [08-allowlist-and-wildcard-matching.md](./08-allowlist-and-wildcard-matching.md) | Allowlist resolver (v1) |
| 09 | _09-log-retrieval-flow_ | ⚠️ Removed in deprecation — see folder 22 v2 §04 |
| 10 | _10-audit-trail_ | ⚠️ Removed in deprecation — see folder 22 v2 §08 + §15 |
| 11 | [11-error-management.md](./11-error-management.md) | ⚠️ Deprecated — see folder 22 v2 §15 |
| 12 | [12-logging-strategy.md](./12-logging-strategy.md) | ⚠️ Deprecated — see folder 22 v2 §06 |
| 13 | _13-coding-guidelines-applied_ | ⚠️ Removed in deprecation |
| 14 | _14-acceptance-criteria_ | ⚠️ Removed in deprecation — see §97 |
| 15 | _15-blind-audit-checklist_ | ⚠️ Removed in deprecation |
| 16 | [16-jwt-onboarding-and-token-usage.md](./16-jwt-onboarding-and-token-usage.md) | ⚠️ Deprecated — JWT removed in v2 |
| 17 | [17-spec-consistency-checklist.md](./17-spec-consistency-checklist.md) | Spec consistency checklist (v1) |
| 97 | [97-acceptance-criteria.md](./97-acceptance-criteria.md) | Canonical AC index (v1) |
| 98 | _98-changelog_ | ⚠️ Never authored — folder frozen at v1 |
| 99 | [99-consistency-report.md](./99-consistency-report.md) | Structural health report (deprecated stub) |

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Spec authoring guide | [../../01-spec-authoring-guide/00-overview.md](../../01-spec-authoring-guide/00-overview.md) |
| Master coding guidelines | [../../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/00-overview.md](../../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/00-overview.md) |
| PHP standards reference | [../../02-coding-guidelines/04-php/07-php-standards-reference/00-overview.md](../../02-coding-guidelines/04-php/07-php-standards-reference/00-overview.md) |
| Error management | [../../03-error-manage/00-overview.md](../../03-error-manage/00-overview.md) |
| Database conventions | [../../04-database-conventions/00-overview.md](../../04-database-conventions/00-overview.md) |
| WP plugin how-to | [../../18-wp-plugin-how-to/00-overview.md](../../18-wp-plugin-how-to/00-overview.md) |

---

## Continuation Marker

If you have any questions or confusion, feel free to ask. If you are creating multiple tasks — especially bigger ones — do it in a way so that when we say `next`, you continue with the remaining tasks.
