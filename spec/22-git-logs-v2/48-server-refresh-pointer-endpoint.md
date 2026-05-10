---
kind: future-spec
todo_audit_exempt: true
description: Server-side normative contract for `POST /wp-json/git-logs/v3/refresh-pointer` — the server-issued pointer-file refresh endpoint consumed by the J-series `riseup-git-logs` CLI when its local `.riseup-git-logs.json` is stale, missing optional fields, or has crossed `expiresAt` without a fresh upload (mirror of §41 client side per Lesson #36; bound by §97 AC-90).
content_axis: normative-contract
axis_rationale: "Server endpoint contract for J-series CLI pointer-file refresh; producer side of the §41 wire format"
---

# §48 — Server: `POST /refresh-pointer` (server-issued pointer refresh)

**Version:** 1.0.0
**Updated:** 2026-05-07 (Phase K3 — third K-series slot; producer of the §41 pointer-file wire format absent any frame upload)
**Bound by §97:** **AC-90** `[critical]`
**Mirror of:** `41-cli-pointer-file-schema.md` (wire format — link-don't-restate per Lesson #36)
**API base:** `/wp-json/git-logs/v3/` (per K1 §46 — clean separation from legacy v2)

> **Scope discipline (Lesson #36 — link-don't-restate).** This file owns the **server-side pointer-refresh production contract**. The 8-field closed wire format + 11-entry forbidden top-level fields + JSON Schema (Draft-07) for `.riseup-git-logs.json` are OWNED by `41-cli-pointer-file-schema.md` and MUST NOT be restated here — this file cites §41 by section anchor. Auth lane (Lane B) is OWNED by §31. Atomic write discipline on the CLI side is OWNED by spec/13 §97 AC-22. Error codes (`GL-PTR-*` / `GL-AUTH-*`) are OWNED by §15. Per-SHA `FixBundle` lookup + storage scoping are OWNED by §39. The `autofixDownloadUrl` field semantics (`null` ⇒ no fixable findings; absent ⇒ not yet computed) are OWNED by §41 §2 row 8.

---

## §1 Purpose & Scope

`POST /wp-json/git-logs/v3/refresh-pointer` is the **only** server-side endpoint that produces a fresh §41 pointer-file payload **without** requiring the CLI to upload frames first. It exists for three closed-set use-cases:

1. **Stale `expiresAt`** — the CLI's local `uploadUrl` has crossed `expiresAt` and the user wants to refresh BEFORE the next `git push` triggers a frame upload.
2. **First-run repair** — `riseup-git-logs init` ran but a subsequent `riseup-git-logs doctor` detected the pointer file is missing optional fields (e.g. `autofixDownloadUrl` was never populated because no fix bundle has ever been computed).
3. **Server-side pointer rotation** — the server has rotated `uploadUrl` (per K1 §46 §6 forbidden patterns: server MAY rotate paths; clients MUST tolerate via this refresh endpoint).

It is **lane-B-write-only** (writes via SSH-key auth per §31; Lane A WP-App-Password is REJECTED with `GL-AUTH-LANE-MISMATCH`). It performs **NO frame ingestion** — the request body carries identity assertions only; any frame-shaped payload is REJECTED with 400 `GL-PTR-FRAMES-FORBIDDEN`.

**In scope:**
- Accept the 4-field identity envelope per §3 below.
- Authenticate via SSH-key Lane B per §31 (full 12-step server validation order).
- Resolve `(repoIdentityHash, currentHead)` to per-SHA SQLite per §39 (READ-ONLY — no row creation).
- Emit the 8-field §41 pointer payload populated from server state.
- Refresh `uploadUrl` + `uploadedAt` + `expiresAt` (resetting TTL); leave `autofixDownloadUrl` as the latest computed value (or `null` if no bundle exists).

**Out of scope (deferred to later K-phases):**
- Unified error envelope + rate-limit policy + idempotency replay table (K4 — §49).
- Cross-link sweep §40–§49 + final 5-gate green check (K5).
- CLI test plan T-CLI-* GWT covering both client + server K-series (J15 — §45).

---

## §2 Endpoint binding

| Field | Value |
|---|---|
| Method | `POST` (NOT GET — the request carries an identity envelope; GET → 405 `GL-PTR-METHOD-FORBIDDEN`) |
| Path | `/wp-json/git-logs/v3/refresh-pointer` |
| Auth | **Lane B only** (SSH-key per §31; Lane A REJECTED 401 `GL-AUTH-LANE-MISMATCH`) |
| Request `Content-Type` | `application/json` (no NDJSON; no multipart; mismatch → 415 `GL-PTR-CONTENT-TYPE-UNSUPPORTED`) |
| Request `Idempotency-Key` | OPTIONAL UUIDv4; if present, server caches response 5 min keyed by `(profileId, repoIdentityHash, currentHead, key)`; replay with sha256-mismatched body → 409 `GL-PTR-IDEMPOTENCY-CONFLICT` |
| Response `Content-Type` | `application/json` (single §41 payload — same shape as the on-disk `.riseup-git-logs.json`) |
| Response `Cache-Control` | `private, no-store` REQUIRED (the payload carries `uploadUrl` which is per-profile; intermediary caching FORBIDDEN) |
| Max request body | 4 KiB (the identity envelope is bounded; >4 KiB → 413 `GL-PTR-BODY-TOO-LARGE` — guards a class of "smuggled frames in a refresh-pointer call" exploits) |
| Server timeout | 10s wall-clock (no streaming; the lookup is a small SQLite SELECT + URL-mint) |
| Rate limit | Token-bucket per `(profileId, repoIdentityHash)` — capacity 30, refill 1/s (intentionally lower than §46 upload — refresh is bursty-rare, NOT bursty-frequent) |

---

## §3 Request envelope (4-field closed set; mirror of §41 §2 rows 1–4)

The request body is a JSON object with **exactly four required top-level fields**. `additionalProperties: false`. Any 5th field (including any of the §41 §2 forbidden top-level field names) → 400 `GL-PTR-ENVELOPE-EXTRA-FIELD`.

| # | Field | Type | Source | Server use |
|---|---|---|---|---|
| 1 | `schemaVersion` | string (SemVer `MAJOR.MINOR.PATCH`) | The CLI's compiled-in §41 schema version | `MAJOR` mismatch → 426 `GL-PTR-SCHEMA-MAJOR-MISMATCH`; `MINOR`/`PATCH` mismatch → ACCEPTED (forward-compat per §41 §3) |
| 2 | `repoIdentityHash` | string (64 lowercase hex chars — full sha256 per §40 §3) | Local `.riseup-git-logs.json` | Used to scope the per-SHA SQLite lookup per §39 |
| 3 | `repoCanonicalRemote` | string (URL — pre-hash canonical form per §41 §2 row 3) | Local `.riseup-git-logs.json` | Recomputed server-side (lowercase + strip `.git` + strip trailing `/`) and re-hashed; mismatch with field 2 → 400 `GL-PTR-IDENTITY-DRIFT` (NOT 422 — this is a contract violation, not a data-shape issue) |
| 4 | `currentHead` | string (40 lowercase hex chars — full git SHA-1) | `git rev-parse HEAD` at request time | NOT validated against any server-known head set (the server has no view of the working tree); used to scope the §39 per-SHA SQLite SELECT for `autofixDownloadUrl` lookup |

**Forbidden request-body top-level fields** (any presence → 400 `GL-PTR-FRAMES-FORBIDDEN`): `frames`, `frame`, `payload`, `entries`, `data`, `body`, `attachments`, `files`, `patches`, `bundle` (the last six guard against "smuggle a fix-bundle through refresh-pointer" attacks; AC-89's `GL-FIX-URL-CONSTRUCTED` is the read-side mirror of this write-side guard). All §41 §2 forbidden top-level fields (`token`, `apiKey`, `secret`, `password`, `sshKey`, `privateKey`, `userId`, `userEmail`, `ownerEmail`, `env`, `platform`) are ALSO forbidden in the request body.

---

## §4 9-step strict server validation + lookup order (REORDERING FORBIDDEN)

The server MUST execute these 9 steps in this exact order. Reordering is a SPEC VIOLATION even when functionally equivalent — the order minimises information leakage about which step rejected, AND minimises wasted work on hostile traffic (cheap rejects first).

| # | Step | Reject code | Notes |
|---|---|---|---|
| 1 | Method + path match | 405 `GL-PTR-METHOD-FORBIDDEN` / 404 (no body) | Wrong method on the v3 path → 405 with `Allow: POST`; wrong path → standard 404 (no v3-specific code; do NOT leak that v3 exists to non-Lane-B callers) |
| 2 | `Content-Type: application/json` | 415 `GL-PTR-CONTENT-TYPE-UNSUPPORTED` | Charset MAY be `utf-8`; absent → assume utf-8; non-utf-8 → 415 |
| 3 | Body size ≤ 4 KiB | 413 `GL-PTR-BODY-TOO-LARGE` | Streamed read with hard cap; do NOT buffer full body before checking |
| 4 | §31 Lane B 12-step authentication | 401 `GL-AUTH-LANE-MISMATCH` (Lane A) / 401 `GL-AUTH-FAILED` (Lane B failed) | Lane A → 401 with NO `WWW-Authenticate: Basic` header (do NOT invite re-attempt); Lane B failed → 401 with `WWW-Authenticate: SshKey realm="git-logs-v3"` |
| 5 | JSON parse | 400 `GL-PTR-MALFORMED-JSON` | No JSONC; no NDJSON; no comments; trailing commas → 400 |
| 6 | Envelope schema (4 required fields, no additional, no forbidden) | 400 `GL-PTR-ENVELOPE-EXTRA-FIELD` / 400 `GL-PTR-FRAMES-FORBIDDEN` / 400 `GL-PTR-ENVELOPE-MISSING-FIELD` | Forbidden-field check fires BEFORE missing-field check (smuggle-attack signal beats incomplete-envelope signal) |
| 7 | `schemaVersion` MAJOR match | 426 `GL-PTR-SCHEMA-MAJOR-MISMATCH` | `Upgrade` header carries the server's MAJOR (e.g. `Upgrade: git-logs-pointer/1`); MINOR/PATCH skew accepted silently |
| 8 | `repoIdentityHash` recompute parity | 400 `GL-PTR-IDENTITY-DRIFT` | Recompute sha256 of canonical-form `repoCanonicalRemote` per §40 §3 step 4; mismatch → 400 (NOT 422 — contract violation, not data-shape issue) |
| 9 | Token-bucket rate-limit | 429 `GL-PTR-RATE-LIMITED` | `Retry-After` header REQUIRED in seconds; bucket key = `(profileId, repoIdentityHash)`; rejected requests do NOT consume bucket (the bucket models successful work, not attempts) |

**Successful path post-step-9:** server proceeds to §5 lookup + payload production. Authentication (step 4) precedes JSON parse (step 5) — unauthenticated callers MUST NOT be able to make the server parse a 4 KiB JSON body (CPU-amplification guard, mirror of K1 §46 §3 step ordering). Rate-limit (step 9) follows authentication so anonymous flood traffic gets 401 (cheap) instead of 429 (counted).

---

## §5 Payload production (§41 8-field shape)

The 200 OK response body is the EXACT byte-shape that the CLI writes to `.riseup-git-logs.json` per §41 §2. The CLI MUST be able to atomically replace the on-disk file with the response body verbatim (per spec/13 AC-22 atomic temp-then-rename). Field-by-field production from server state:

| §41 §2 # | Field | Production rule |
|---|---|---|
| 1 | `schemaVersion` | Echo the request body's `schemaVersion` IF the MAJOR matches step-7 server MAJOR; otherwise step 7 already rejected. The server does NOT bump MINOR/PATCH on the response — it preserves the client's value to avoid forcing CLI rewrites on every refresh. |
| 2 | `repoIdentityHash` | Echo verbatim from request (already validated at step 8). |
| 3 | `repoCanonicalRemote` | Echo verbatim from request (already validated at step 8 — the server does NOT re-canonicalise on output; the client's pre-hash form is authoritative for auditability). |
| 4 | `currentHead` | Echo verbatim from request (the server has no view of the working tree). |
| 5 | `uploadUrl` | Server-issued. MUST be HTTPS. MUST contain a per-profile path token (e.g. `/wp-json/git-logs/v3/upload-frames?token=<opaque>`). The token is opaque to the client and rotated on every refresh — the client MUST NOT extract / parse / log the token. |
| 6 | `uploadedAt` | OMITTED on this endpoint's response IF the per-SHA SQLite has no upload row for `(repoIdentityHash, currentHead)`; otherwise SET to the latest upload's RFC 3339 UTC timestamp. The server MUST NOT use the request's wall-clock time — only the latest persisted value. |
| 7 | `expiresAt` | REQUIRED iff `uploadUrl` is present (which it always is on this endpoint — see field 5). Computed as `now() + UploadUrlTtlSeconds` ConfigKv (default 86400 = 24h). Mirror of spec/13 AC-SD-23 TTL/expiry pattern per §41 §2 row 7. |
| 8 | `autofixDownloadUrl` | Three-state: `null` if a fix-bundle was computed for `(repoIdentityHash, currentHead)` AND no findings (mirror of §41 §2 row 8 "`null` means no fixable findings"); a valid HTTPS URL of the form `/wp-json/git-logs/v3/autofix/{repoIdentityHash}/{frameId}` per §47 §1 IF a bundle exists AND has not been consumed AND has not expired; OMITTED ENTIRELY if no bundle has ever been computed for this `(repoIdentityHash, currentHead)`. The server MUST NOT auto-create a bundle on this endpoint — bundle creation is owned by §46's frame-ingestion path. |

**Field ordering in the response body:** lexicographic — the same canonical key order required by §41 §3 JSON Schema. Deviation = `GL-SCHEMA-DRIFT` (the CLI MUST be able to byte-replace the on-disk file with the response body without re-serialising).

**Pointer-file write on the CLI side** is owned by §41 §1 (write discipline table) + spec/13 §97 AC-22 (atomic temp-then-rename). This server endpoint MUST NOT instruct the client on how to persist — the response body IS the new pointer file content; the CLI knows what to do with it.

---

## §6 Forbidden patterns (summary)

- Servicing the v3 path under any HTTP method other than POST (→ 405 `GL-PTR-METHOD-FORBIDDEN` with `Allow: POST`).
- Accepting Lane A (WP App Password) for any write against this endpoint (→ 401 `GL-AUTH-LANE-MISMATCH`).
- Accepting NDJSON content-type or multipart bodies (→ 415 `GL-PTR-CONTENT-TYPE-UNSUPPORTED`).
- Accepting any of the 10 forbidden body-top-level field names (`frames`/`frame`/`payload`/`entries`/`data`/`body`/`attachments`/`files`/`patches`/`bundle`) → 400 `GL-PTR-FRAMES-FORBIDDEN` (smuggle-attack guard; mirrors AC-89's `GL-FIX-URL-CONSTRUCTED` write-side equivalent).
- Accepting any of the 11 §41 §2 forbidden secret-shaped field names in the request → 400 `GL-PTR-FRAMES-FORBIDDEN` (same code; same disposition).
- Restating §41 §2 8-field shape or §41 §3 JSON Schema inline here.
- Restating §31 12-step Lane B validation inline here.
- Restating spec/13 §97 AC-22 atomic-write discipline inline here.
- Restating `GL-PTR-*` / `GL-AUTH-*` semantics inline here (cite by code name only — owned by §15).
- Auto-creating a `FixBundle` row on this endpoint (bundle creation lives in §46's frame-ingestion path; this endpoint is read-only against `FixBundle`).
- Issuing a non-HTTPS `uploadUrl` (→ SPEC VIOLATION; the CLI per §43 §2 will reject and log `GL-UPLOAD-URL-INSECURE`).
- Including a `Retry-After` header on any non-429 response (→ misleading the client into backoff that the server did not request).
- Setting `Cache-Control: public` or omitting `Cache-Control` (the response carries a per-profile rotated token in `uploadUrl`; intermediary caching = token leakage).
- Coalescing v2 + v3 paths into a single handler (v3 MUST be a separate route registration per K1 §46 §6).
- Honouring `If-None-Match` on this endpoint (the response is per-request fresh — every call MUST re-mint `uploadUrl` + reset `expiresAt`; conditional GETs make no sense; if a client sends `If-None-Match`, IGNORE silently — do NOT 304, do NOT 412).

---

## §7 Out of scope (deferred K-series slots)

- **K4 §49** — Unified error envelope + rate-limit policy + idempotency replay normative cross-cuts (AC-91).
- **K5** — Cross-link sweep across §40–§49 + final 5-gate green check.
- **J15** — §45 test plan (T-CLI-* GWT; AC-87) covering both client + server K-series surfaces.

---

## Changelog

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2026-05-07 | Phase K3 — initial ship. 7-section normative contract for `POST /wp-json/git-logs/v3/refresh-pointer`. Bound by §97 AC-90. Mirror of §41 client-side wire format per Lesson #36. v3 base + Lane B writes only + 4-field identity envelope + 9-step strict validation order + 8-field §41 payload production (server-issued `uploadUrl` + `expiresAt` reset; `autofixDownloadUrl` three-state echo from `FixBundle` lookup per §39). NO frame ingestion (10-entry forbidden body-top-level field list). |
