---
kind: future-spec
todo_audit_exempt: true
description: Server-side normative contract for `GET /wp-json/git-logs/v3/autofix/{repoIdentityHash}/{frameId}` — the fix-bundle download endpoint consumed by the J-series `riseup-git-logs` CLI's auto-fix protocol (mirror of §44 client side per Lesson #36; bound by §97 AC-89).
content_axis: normative-contract
axis_rationale: "Server endpoint contract for J-series CLI auto-fix bundle download; producer side of §44"
---

# §47 — Server: `GET /autofix/{repoIdentityHash}/{frameId}` (fix-bundle producer)

**Version:** 1.0.0
**Updated:** 2026-05-07 (Phase K2 — second K-series slot; producer of §44 fix-bundle envelope)
**Bound by §97:** **AC-89** `[critical]`
**Mirror of:** `44-cli-autofix-protocol.md` (client side — link-don't-restate per Lesson #36)
**API base:** `/wp-json/git-logs/v3/` (per K1 §46 — clean separation from legacy v2)

> **Scope discipline (Lesson #36 — link-don't-restate).** This file owns the **server-side fix-bundle producer contract**. The bundle envelope shape (7-field closed set + 17-entry forbidden list), 4-state outcome semantics, preflight discipline, atomic apply, and post-apply pointer-file refresh are OWNED by `44-cli-autofix-protocol.md` and MUST NOT be restated here — this file cites §44 by section anchor. Auth lane (Lane B) is OWNED by §31. Error codes (`GL-FIX-*` / `GL-AUTH-*`) are OWNED by §15. The download URL is server-issued via §43 §6 `autofixDownloadUrl` field (OWNED by §43).

---

## §1 Purpose & Scope

`GET /wp-json/git-logs/v3/autofix/{repoIdentityHash}/{frameId}` is the **only** server-side endpoint that produces a J-series fix-bundle envelope. It is **lane-B-read-only** (reads via SSH-key auth per §31). The URL is **server-issued** in the §43 §6 `autofixDownloadUrl` response field — clients MUST NOT construct this URL by hand (path discovery via construction = `GL-FIX-URL-CONSTRUCTED`, 403).

**In scope:**
- Resolve `(repoIdentityHash, frameId)` to a server-prepared fix bundle (or 404 / 410 / 409 per §3).
- Authenticate via SSH-key Lane B per §31 (full 12-step server validation order).
- Emit the 7-field bundle envelope per §44 §3 with `additionalProperties: false`.
- Honour `If-None-Match` / etag for unchanged bundles (304).
- Enforce single-consumption + expiry semantics (410 after consume; 410 after `expiresAt`).

**Out of scope (deferred to later K-phases):**
- `POST /refresh-pointer` (K3 — §48).
- Unified error envelope + rate-limit + idempotency replay (K4 — §49).
- Multi-bundle queueing / partial-bundle resumption (FORBIDDEN by §44 §10 — server MUST NOT expose).

---

## §2 Endpoint binding

| Field | Value |
|---|---|
| Method | `GET` |
| Path | `/wp-json/git-logs/v3/autofix/{repoIdentityHash}/{frameId}` |
| `{repoIdentityHash}` | 32-hex (per §40 §3 identity-discovery step d); non-32-hex → 400 `GL-FIX-PATH-MALFORMED` |
| `{frameId}` | UUIDv4 (per §43 §3 frame envelope); non-UUIDv4 → 400 `GL-FIX-PATH-MALFORMED` |
| Auth | **Lane B only** (SSH-key per §31; Lane A → 401 `GL-AUTH-LANE-MISMATCH`) |
| Request `Accept` | `application/vnd.riseup.git-logs.fix+json; v=1` REQUIRED; absent or other → 406 `GL-FIX-ACCEPT-INVALID` |
| Request `If-None-Match` | OPTIONAL; matches current bundle etag → 304 (no body) |
| Request `Idempotency-Key` | FORBIDDEN on GET — present → 400 `GL-FIX-IDEMPOTENCY-FORBIDDEN` (idempotency-key contract per §43 §4 is for POST writes only; reusing a GET key risks cache-poisoning) |
| Response `Content-Type` | `application/vnd.riseup.git-logs.fix+json; v=1` (NOT plain `application/json`) |
| Response `Content-Encoding` | `gzip` MAY be applied when `Accept-Encoding: gzip` present |
| Response `ETag` | strong etag = `"sha256(bundleId + targetHead + sha256-of-canonical-bundle-bytes)[0:16]"` (16-hex; double-quoted) |
| Response `Cache-Control` | `private, no-store` (bundles are single-consumption per §3 step 9; CDN caching FORBIDDEN) |
| Max response body | 4 MiB compressed / 16 MiB decompressed (mirrors §44 §2 client cap) |
| Connect / body timeout | 30s connect / 60s body (advisory) |

**FORBIDDEN:** servicing this path under any HTTP method other than GET (POST/PUT/DELETE → 405 `GL-METHOD-NOT-ALLOWED`); accepting any `X-GL-Auth-Mode` value other than `ssh`; serving from any base other than `/wp-json/git-logs/v3/`; honouring `Idempotency-Key` on this endpoint; setting `Cache-Control: public` or any value permitting intermediary caching; responding without an `ETag` header.

---

## §3 Server validation + lookup order (strict 11-step)

The server MUST execute these checks in this exact order. First failure short-circuits with the matching `GL-*` code from §15 and an error envelope per §44 §9.

| # | Check | Reject code (HTTP) |
|---|---|---|
| 1 | Method is `GET`; path matches `/wp-json/git-logs/v3/autofix/{repoIdentityHash}/{frameId}` exactly | `GL-METHOD-NOT-ALLOWED` (405) |
| 2 | `{repoIdentityHash}` is 32-hex; `{frameId}` is UUIDv4 | `GL-FIX-PATH-MALFORMED` (400) |
| 3 | `Accept: application/vnd.riseup.git-logs.fix+json; v=1` exact match (case-insensitive on header name; charset MAY be `utf-8`) | `GL-FIX-ACCEPT-INVALID` (406) |
| 4 | `Idempotency-Key` header ABSENT | `GL-FIX-IDEMPOTENCY-FORBIDDEN` (400) |
| 5 | Lane B auth per §31 12-step order (full sequence; reordering FORBIDDEN) | per §31 (401/403) |
| 6 | `(repoIdentityHash)` resolves to a `Repo` row visible to the authenticated `Profile` (per §05 acceptance + §08 `Pipeline.HasError` scoping); else "not your repo" → 404 (NOT 403, to avoid existence-leak) | `GL-FIX-NOT-FOUND` (404) |
| 7 | `(repoIdentityHash, frameId)` row exists in `FixBundle` table; else | `GL-FIX-NOT-FOUND` (404) |
| 8 | `FixBundle.expiresAt > now()`; else | `GL-FIX-EXPIRED` (410) |
| 9 | `FixBundle.consumedAt IS NULL`; else (single-consumption invariant per §44 §10) | `GL-FIX-CONSUMED` (410) |
| 10 | `If-None-Match` header (if present) does NOT match current etag | `304 Not Modified` (no body, no error code) |
| 11 | Token-bucket rate-limit per `OwnedByProfileId` (defer to existing §05 §3 logic; Retry-After header on rejection) | `GL-RATE-LIMIT-EXCEEDED` (429) |

**Reordering FORBIDDEN.** Auth (step 5) MUST precede ownership lookup (step 6) so unauthenticated callers cannot probe `(repoIdentityHash, frameId)` existence. Ownership check (step 6) MUST precede bundle existence check (step 7) so cross-tenant probes return identical 404 regardless of bundle presence. Expiry (step 8) MUST precede consume check (step 9) so an expired-but-already-consumed bundle returns `GL-FIX-EXPIRED` (more actionable for the client per §44 §9).

**Note on 304:** A 304 response does NOT count as "consumption" — the `consumedAt` column is set only on a successful 200 response (step 11 passes + body emitted). This permits clients to revalidate without burning the bundle.

---

## §4 Bundle envelope production

When all validation passes, the server MUST produce the bundle envelope per `44-cli-autofix-protocol.md` §3 (canonical 7-field closed set + 17-entry forbidden field list):

| Field | Source |
|---|---|
| `bundleId` | `FixBundle.bundleId` (UUIDv4 server-assigned at bundle creation per §44 §3) |
| `batchId` | `FixBundle.batchId` (UUIDv4; equals the §43 batch that triggered fix preparation) |
| `repoIdentityHash` | `{repoIdentityHash}` URL parameter (echoed verbatim) |
| `targetHead` | `FixBundle.targetHead` (40-hex; the HEAD the patches were computed against) |
| `schemaBump` | `FixBundle.schemaBump` (enum `{patch, minor, major}` per §44 §3) |
| `patches` | array of `{path, mode, beforeSha256, afterSha256, unifiedDiff}` per §44 §3 (`additionalProperties: false`) |
| `expiresAt` | `FixBundle.expiresAt` (RFC 3339; identical to the value used in step 8) |

**Field ordering** in the JSON response MUST match the canonical order above (lexicographic field-stable serialisation per spec/04 conventions). Deviation = `GL-SCHEMA-DRIFT`.

**FORBIDDEN bundle production patterns:** including any field outside the 7-field closed set (e.g. `executablePath`, `serverHostname`, `wordpressVersion` — full 17-entry forbidden list owned by §44 §3); restating §44 §3 forbidden list inline here; mutating `patches[].unifiedDiff` between bundle creation and download (bundles are immutable once written; re-derivation = new `bundleId`); serialising with non-canonical key order; emitting NDJSON.

---

## §5 Single-consumption + expiry semantics

After a successful 200 response (body emitted), the server MUST atomically (per spec/13 §97 AC-22 link-don't-restate):

1. Set `FixBundle.consumedAt = now()` (UTC, RFC 3339).
2. Set `FixBundle.consumedByProfileId = <authenticated profile id>`.
3. Append a `SystemEvent` row with type `FixBundleConsumed` per §20 (event payload: `{bundleId, batchId, repoIdentityHash, targetHead, consumedAt, consumedByProfileId}`).

These three writes MUST occur in a single SQLite transaction (`BEGIN IMMEDIATE` per spec/13 AC-22). Partial writes = `GL-SCHEMA-DRIFT` and the bundle MUST be considered consumed (do not retry — the client already received the body; retrying could produce double-consumption races on concurrent GETs).

**Expiry:** `FixBundle.expiresAt` is set at bundle creation (server-side, NOT here). Default TTL is `FixBundleDefaultTtlSeconds` ConfigKv (default 86400 = 24h). Bundles past `expiresAt` MUST return 410 `GL-FIX-EXPIRED` (step 8 above) — do NOT auto-extend, do NOT regenerate inline. The client per §44 §5 step 1 will fall back to fresh upload to obtain a new `autofixDownloadUrl`.

**Concurrent-GET race resolution:** if two authenticated GETs land within the same window before `consumedAt` is set, the SECOND one MUST see `consumedAt IS NOT NULL` (step 9) and return 410 `GL-FIX-CONSUMED`. The implementation MUST use `SELECT ... FOR UPDATE` semantics (or SQLite `BEGIN IMMEDIATE` with `WHERE consumedAt IS NULL` UPDATE-and-check-rowcount pattern) — application-level mutex / advisory lock FORBIDDEN (does not survive server restart).

---

## §6 Forbidden patterns (summary)

- Servicing the v3 path under any HTTP method other than GET (→ 405).
- Accepting Lane A (WP App Password) for any read against this endpoint (→ 401 `GL-AUTH-LANE-MISMATCH`).
- Allowing client-constructed URLs that bypass the server-issued `autofixDownloadUrl` from §43 §6 (the URL MUST flow through the §43 response — direct construction = `GL-FIX-URL-CONSTRUCTED`, 403).
- Restating §44 §3 7-field bundle envelope or 17-entry forbidden list inline here.
- Restating §44 §4 4-state outcome set inline here (the outcome is computed CLIENT-side after applying the bundle — server has no opinion on outcome).
- Restating §31 12-step Lane B validation inline here.
- Restating §43 frame-envelope shape or idempotency-key contract inline here.
- Restating `GL-FIX-*` / `GL-AUTH-*` semantics inline here (cite by code name only — owned by §15).
- Honouring `Idempotency-Key` on this GET endpoint (→ 400 `GL-FIX-IDEMPOTENCY-FORBIDDEN`).
- Setting `Cache-Control: public` or omitting `Cache-Control` (private, no-store REQUIRED — bundles are single-consumption secrets).
- Auto-regenerating an expired bundle inline (→ 410, force client fallback to fresh upload).
- Coalescing v2 + v3 paths into a single handler (v3 MUST be a separate route registration per K1 §46 §6).
- Servicing partial-bundle resumption (e.g. byte-range reads) — bundles are atomic-or-nothing; range requests → 416 `GL-FIX-RANGE-UNSUPPORTED`.

---

## §7 Out of scope (deferred K-series slots)

- **K3 §48** — `POST /wp-json/git-logs/v3/refresh-pointer` (server-issued pointer-file refresh; AC-90).
- **K4 §49** — Unified error envelope + rate-limit + idempotency replay normative cross-cuts (AC-91).
- **K5** — Cross-link sweep across §40–§49 + final 5-gate green check.
- **J15** — §45 test plan (T-CLI-* GWT; AC-87) covering both client + server K-series surfaces.

---

## Changelog

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2026-05-07 | Phase K2 — initial ship. 7-section normative contract for `GET /wp-json/git-logs/v3/autofix/{repoIdentityHash}/{frameId}`. Bound by §97 AC-89. Mirror of §44 client side per Lesson #36. v3 base + Lane B reads only + server-issued URL discipline. |
