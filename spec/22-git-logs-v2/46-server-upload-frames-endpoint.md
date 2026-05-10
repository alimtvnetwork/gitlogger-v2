---
kind: future-spec
todo_audit_exempt: true
description: Server-side normative contract for `POST /wp-json/git-logs/v3/upload-frames` — the receiver endpoint for the J-series `riseup-git-logs` CLI's NDJSON-over-HTTPS streaming upload (mirror of §43 client side per Lesson #36; bound by §97 AC-88).
content_axis: normative-contract
axis_rationale: "Server endpoint contract for J-series CLI upload protocol; receiver side of §43"
---

# §46 — Server: `POST /upload-frames` (NDJSON receiver)

**Version:** 1.1.0
**Updated:** 2026-05-10 (Phase L5 — non-normative §8 Worked Server Transcript added; pattern from L1/L2/L3/L4)
**Bound by §97:** **AC-88** `[critical]`
**Mirror of:** `43-cli-upload-protocol.md` (client side — link-don't-restate per Lesson #36)
**API base:** `/wp-json/git-logs/v3/` (NEW v3 base — clean separation from legacy v2 endpoints in §04 per archive precedent v1→v2; v2 endpoints remain unchanged and continue serving the legacy CI/CD callers)

> **Scope discipline (Lesson #36 — link-don't-restate).** This file owns the **server-side accept/reject contract**. The wire shape (frame envelope, idempotency-key shape, retry semantics) is OWNED by `43-cli-upload-protocol.md` and MUST NOT be restated here — this file cites §43 by section anchor. The auth lane (SSH-key Lane B) is OWNED by §31 — this file cites §31. Error codes are OWNED by §15 — this file cites code names only.

---

## §1 Purpose & Scope

`POST /wp-json/git-logs/v3/upload-frames` is the **only** server-side endpoint that accepts the J-series CLI's classified frames. It is **lane-B-write-only** (writes via SSH-key auth per §31; Lane A WP-App-Password is REJECTED with `GL-AUTH-LANE-MISMATCH`). It does NOT serve reads — read endpoints land in a future K-phase (out of scope here).

**In scope:**
- Accept the NDJSON envelope shape defined in §43 §3.
- Authenticate via SSH-key Lane B per §31 (full 12-step server validation order).
- Enforce idempotency-key contract per §43 §4 (24h server retention; sha256-mismatch → 409).
- Map each accepted frame to per-SHA SQLite storage per §39 (split-DB scoping).
- Return the 6-field response envelope per §43 §6.

**Out of scope (deferred to later K-phases):**
- `GET /autofix/{repoIdentityHash}/{frameId}` (K2 — §47).
- `POST /refresh-pointer` (K3 — §48).
- Unified error envelope + rate-limit + idempotency replay (K4 — §49).

---

## §2 Endpoint binding

| Field | Value |
|---|---|
| Method | `POST` |
| Path | `/wp-json/git-logs/v3/upload-frames` |
| Auth | **Lane B only** (SSH-key per §31; Lane A REJECTED 401 `GL-AUTH-LANE-MISMATCH`) |
| Request `Content-Type` | `application/x-ndjson` (LF-terminated; non-LF → 400 `GL-UPLOAD-FRAME-MALFORMED`) |
| Request `Content-Encoding` | `gzip` MAY be present (per §43 §2 >4 KiB rule); other encodings → 415 `GL-UPLOAD-ENCODING-UNSUPPORTED` |
| Request `Idempotency-Key` | REQUIRED UUIDv4 per §43 §4; absent → 400 `GL-UPLOAD-IDEMPOTENCY-MISSING` |
| Response `Content-Type` | `application/json` (single envelope per §43 §6 — NOT NDJSON) |
| Max request body | 16 MiB compressed / 64 MiB decompressed (decompressed cap > §43 §2 to permit server-side header overhead) |
| Max frames per request | `NdjsonMaxRowsPerStream` ConfigKv (default 10 000); exceeded → 413 `GL-UPLOAD-TOO-MANY-FRAMES` |
| Connect / body timeout | 30s connect / 60s body (mirror §43 §2; client-side advisory) |

**FORBIDDEN:** servicing this path under any other HTTP method (GET/PUT/DELETE → 405 `GL-METHOD-NOT-ALLOWED`); accepting any `X-GL-Auth-Mode` value other than `ssh`; serving from any base other than `/wp-json/git-logs/v3/`.

---

## §3 Server validation order (strict 10-step)

The server MUST execute these checks in this exact order. First failure short-circuits with the matching `GL-*` code from §15 and an error envelope per §43 §7.

| # | Check | Reject code (HTTP) |
|---|---|---|
| 1 | Method is `POST`; path matches `/wp-json/git-logs/v3/upload-frames` exactly | `GL-METHOD-NOT-ALLOWED` (405) |
| 2 | `Content-Type: application/x-ndjson` (case-insensitive; charset MAY be `utf-8`, MUST NOT be other) | `GL-UPLOAD-CONTENT-TYPE-INVALID` (415) |
| 3 | `Idempotency-Key` header present + UUIDv4 shape | `GL-UPLOAD-IDEMPOTENCY-MISSING` (400) |
| 4 | Lane B auth per §31 12-step order (headers complete → timestamp skew ≤300s → `SshKey` row found + `IsActive=1` → repo bind → acceptance + branch → nonce fresh → signature verify → profile active → app gate) | per §31 (401/403) |
| 5 | Body size ≤ 16 MiB compressed; decompressed ≤ 64 MiB; gzip-bomb guard (decompressed/compressed ratio ≤ 100×) | `GL-UPLOAD-PAYLOAD-TOO-LARGE` (413) |
| 6 | NDJSON parse: every line is valid JSON; LF-terminated; no trailing partial frame | `GL-UPLOAD-FRAME-MALFORMED` (400) |
| 7 | Per-frame schema validation against §43 §3 9-field closed set + 16-entry forbidden-field list (`additionalProperties: false`) | `GL-UPLOAD-FRAME-MALFORMED` (400) |
| 8 | Frame count ≤ `NdjsonMaxRowsPerStream` ConfigKv | `GL-UPLOAD-TOO-MANY-FRAMES` (413) |
| 9 | Idempotency replay: lookup `IdempotencyKey` in `UploadIdempotency` table — if present + body sha256 matches → return cached response (200); if present + sha256 differs → 409 | `GL-UPLOAD-IDEMPOTENCY-CONFLICT` (409) |
| 10 | Token-bucket rate-limit per `OwnedByProfileId` (defer to existing §05 §3 logic; Retry-After header on rejection) | `GL-RATE-LIMIT-EXCEEDED` (429) |

**Reordering FORBIDDEN.** Auth (step 4) MUST precede body-size + parse (steps 5–8) so unauthenticated payloads cannot consume parse cycles.

---

## §4 Frame → storage mapping

For each accepted frame:

1. Resolve `(repoIdentityHash, currentHead)` to a per-SHA SQLite file per §39 (`<dataDir>/<ShaLogsRoot>/<currentHead[0:2]>/<currentHead>.db`); create the row in root `ShaRegistry` if missing (atomic `INSERT OR IGNORE`).
2. INSERT a row into the per-SHA file's `LogEntry` (or `ErrorLogEntry` if `outcome ∈ {ERROR, INTERNAL}`) table per spec/04 conventions.
3. Frame-level dedup (belt-and-braces per §43 §4): `(currentHead, subcommand, frameId)` UNIQUE constraint; duplicate INSERT → counted in `framesDeduplicated`, NOT an error.
4. `outcome=ERROR` or `outcome=INTERNAL` → set `Pipeline.HasError = 1` for the matching `(repoIdentityHash, currentHead, subcommand)` tuple per §08 history rules.

**FORBIDDEN:** writing into the legacy v2 `LogEntry` tables described in §02 §03 — v3 frames land **only** in the v3.8.0+ split-DB layout per §39. The two storage paths share the per-SHA SQLite files (no schema drift), but the v3 endpoint MUST NOT touch the root v2 `LogEntry` table.

---

## §5 Response envelope

On success, return HTTP 200 with the 6-field response per §43 §6:

```json
{
  "batchId": "<UUIDv4 — server-assigned, equals Idempotency-Key by default>",
  "framesReceived": <int>,
  "framesDeduplicated": <int>,
  "uploadedAt": "<RFC 3339 UTC>",
  "expiresAt": "<RFC 3339 UTC — server retention horizon>",
  "autofixDownloadUrl": "<https URL or null>"
}
```

`autofixDownloadUrl` is **non-null only** when the server has prepared a fix bundle per §44 (auto-fix protocol); otherwise `null`. The URL points at K2's `GET /autofix/{repoIdentityHash}/{frameId}` endpoint (out of scope here — link only).

**FORBIDDEN:** returning NDJSON; returning multiple envelopes; embedding frame echoes; returning any field outside the 6-field set.

---

## §6 Forbidden patterns

- Accepting any `X-GL-Auth-Mode` value other than `ssh` (Lane A REJECTED).
- Restating the frame-envelope shape, idempotency-key contract, or retry semantics inline (those are OWNED by §43 — cite by section anchor).
- Restating the SSH-key Lane B 12-step server validation order inline (OWNED by §31 — cite by section anchor).
- Restating per-SHA SQLite scoping rules inline (OWNED by §39 — cite by section anchor).
- Restating `GL-UPLOAD-*` / `GL-FIX-*` / `GL-AUTH-*` error code semantics inline (OWNED by §15 — cite by code name only).
- Coalescing v2 + v3 endpoint paths into a single handler that branches internally — v3 MUST be a separate route registration with separate rate-limit, idempotency, and storage policies.
- Auto-promoting a v2 caller to v3 (no implicit lane upgrade; clients MUST opt-in by calling the v3 path).

---

## §7 Out of scope (next K-phases)

| Phase | Endpoint | Bound AC |
|---|---|---|
| K2 | `GET /autofix/{repoIdentityHash}/{frameId}` (fix bundle download — §47) | AC-89 (planned) |
| K3 | `POST /refresh-pointer` (server-issued pointer-file refresh — §48) | AC-90 (planned) |
| K4 | Unified error envelope + rate-limit policy + idempotency replay (§49) | AC-91 (planned) |
| K5 | Cross-link sweep + final 5-gate green check + Lesson #41 follow-up | — |

---

## §8 Worked Server Transcript (Non-Normative)

> **Status:** `kind: example` — non-normative illustration per **Lesson #29**. Walks the server-side `POST /upload-frames` accept path end-to-end (auth → idempotency → frame parse → per-SHA storage → response envelope), then exercises three rejection paths covering the §3 strict-step guarantees. Mirror of §43 §8 client-side transcript — the two halves form a **complete request/response pair** for the J-series upload protocol. Fixtures only; do not treat as test vectors. Normative shape lives in §3/§4/§5.

### §8.1 Setup givens

- Endpoint: `POST https://logs.example.com/wp-json/git-logs/v3/upload-frames`
- Auth lane: SSH-key Lane B per §31 (Lane A REJECTED at §3 step 5)
- Caller: `riseup-git-logs` v1.0.0 with classifier v1.1.0 (per §42 §6)
- Body: 3-frame NDJSON batch matching §43 §8.2 (one each NORMAL/WARN/ERROR)

### §8.2 Accept-path transcript (200 OK)

**Request line + headers** (cited verbatim from §43 §8.2 — link-don't-restate):
```
POST /wp-json/git-logs/v3/upload-frames HTTP/1.1
Host: logs.example.com
Content-Type: application/x-ndjson
X-GL-Auth-Mode: ssh
X-GL-SSH-Key-Fingerprint: SHA256:xxxx...
X-GL-SSH-Signature: <base64 ed25519 sig over canonical request bytes>
Idempotency-Key: 7f3a-4b2c-...
Content-Length: 1842
```

**Server §3 strict 10-step walk** (each step name OWNED by §3 — link-don't-restate):
1. Method = POST ✓
2. Path = `/wp-json/git-logs/v3/upload-frames` ✓
3. `Content-Type` = `application/x-ndjson` ✓
4. `X-GL-Auth-Mode` = `ssh` ✓ (Lane A would reject here per §6 forbidden #1)
5. §31 Lane B 12-step SSH validation invoked → PASS (key present in `AuthorizedKey` table, signature verifies over canonical bytes per §31)
6. `Idempotency-Key` lookup in 5-min cache → MISS → proceed (HIT path covered in §8.4)
7. Body size ≤ §3 step 7 cap ✓
8. Per-line NDJSON parse → 3 frames, all valid against §43 §3 envelope shape (per-frame `outcome` ∈ §42 §2 closed set)
9. §39 per-SHA SQLite scoping → routes all 3 frames to `repoIdentityHash=3f2a8b1c...` shard
10. Token-bucket rate-limit → within budget → ACCEPT

**Storage write per §4 mapping:**
- Each NDJSON frame → one `Frame` row in the per-SHA SQLite (atomic transaction with `BEGIN IMMEDIATE` per spec/13 AC-22 link-don't-restate)
- One `Batch` row created with `batchId = uuid v4`, `frameCount = 3`, `acceptedAt = 2026-05-10T09:15:42Z`
- `Idempotency-Key` cached for 5 min mapped to the response body for byte-identical replay

**Response per §5 (6-field closed envelope):**
```http
HTTP/1.1 200 OK
Content-Type: application/json
ETag: "9c4e1a2b8d3f"

{
  "batchId": "f1a2b3c4-d5e6-7890-abcd-ef0123456789",
  "frameCount": 3,
  "acceptedAt": "2026-05-10T09:15:42Z",
  "uploadUrl": "https://logs.example.com/u/3f2a8b1c",
  "expiresAt": "2026-08-08T09:15:42Z",
  "autofixDownloadUrl": "https://logs.example.com/fix/3f2a8b1c/b2c3d4d4.patch"
}
```

The `autofixDownloadUrl` is server-issued (URL-construction by clients FORBIDDEN per §47 §1) and consumed by §44 client-side auto-fix flow.

### §8.3 Negative path A — Lane A rejection (§3 step 4)

**Request:** identical to §8.2 but with `X-GL-Auth-Mode: bearer`.

**Server walk:**
1–3 ✓; step 4 detects `bearer` ≠ `ssh` → REJECT immediately
- §3 step 5 (SSH-key validation) NOT invoked (auth-mode gate precedes lane validation)
- Response: `401 Unauthorized` with `GL-AUTH-LANE-A-FORBIDDEN` (code OWNED by §15)
- No `Frame` rows written; `Idempotency-Key` NOT cached (failed requests do not occupy cache slots)

### §8.4 Negative path B — Idempotency-Key replay with mutated body (§3 step 6)

**Request:** identical headers to §8.2 (same `Idempotency-Key`) but body has 4 frames instead of 3.

**Server walk:**
1–5 ✓; step 6 finds cached entry for the key → compares request body sha256 against cached sha256 → **MISMATCH**
- Per §43 §5 + this file's §3 step 6, mutated body with same idempotency key is FORBIDDEN
- Response: `409 Conflict` with `GL-UPLOAD-IDEMPOTENCY-MUTATED` (code OWNED by §15)
- The original cached response is NOT returned (replay-with-mutation is a security signal, not an honest retry)
- No new `Frame` rows written

### §8.5 Negative path C — Per-SHA shard rate-limit exceeded (§3 step 10)

**Request:** identical to §8.2, but caller has already burned the per-shard token bucket within the current window.

**Server walk:**
1–9 ✓ (frames are valid; SHA scoping resolves correctly); step 10 token-bucket check → DENY
- Response: `429 Too Many Requests` with `Retry-After: 30` and `GL-UPLOAD-RATE-LIMIT-PER-SHA` (code OWNED by §15)
- No `Frame` rows written
- Client retry behaviour OWNED by §43 §5 backoff math (link-don't-restate)

### §8.6 Coverage summary

This transcript exercises:
- All 10 §3 strict steps on the accept path (§8.2)
- The Lane-A forbidden enforcement gate (§8.3 — §3 step 4)
- The idempotency-mutation guard (§8.4 — §3 step 6)
- The per-SHA token-bucket gate (§8.5 — §3 step 10)
- §4 frame→storage mapping (§8.2 storage write block)
- §5 6-field closed response envelope shape (§8.2 response block)

Auth Lane B 12-step validation (§31), per-SHA SQLite scoping (§39), `GL-*` error code semantics (§15), and frame-envelope shape (§43) are cited by anchor and not restated, per §6 forbidden patterns + Lesson #36.
