---
kind: interface-contract
content_axis: normative-cli-upload-wire-protocol
axis_rationale: "riseup-git-logs CLI → server NDJSON streaming wire protocol; tier-1 transport contract for the J-series CLI subsystem"
---

# `riseup-git-logs` CLI — Upload Protocol

**Version:** 1.1.0
**Updated:** 2026-05-08 (Phase L1 — §8 Worked Example added; transcript per Lesson #29 `kind: example`; normative contract unchanged)
<!-- verified-phase: 158 -->

> **Status:** Normative tier-1 (governing AC: §97 AC-85). Fourth of the J-series CLI subsystem (§40–§45).
> Per **Lesson #36** (link-don't-restate): the REST endpoint surface is owned by **spec/22 §04** (`04-rest-api-endpoints.md`); the split-DB log-storage scoping is owned by **spec/22 §39** (`39-split-db-log-storage.md`); the SSH-key Lane B auth contract is owned by **spec/22 §31** (`31-ssh-key-auth.md`); rate-limit + payload caps are owned by **spec/22 §05** (`05-auth-and-validation.md`). This file binds the wire shape that consumes those surfaces and **does not restate any of their bodies**.
> Per **Lesson #21** (intra-module sibling-file delegation): bound from §97 AC-85 by name; row 37 of AC-80 Sibling File Delegation Map.
> Per **Lesson #19** (audit-boundary pin): the 6-section wire-format contract is enumerated as a normative tier-1 surface here; restating any of it in §40, §41, §42, §44, or §45 is FORBIDDEN.

---

## 1. Purpose & Scope

The upload protocol is the **deterministic wire format** by which the `riseup-git-logs` CLI streams classified frames (per §42 outcome set) to the spec/22 WordPress plugin's REST endpoint. The protocol is **NDJSON-over-HTTPS** with explicit idempotency, retry/backoff, and partial-progress resumption.

**In scope:** request shape (method/path/headers/body grammar), per-frame envelope, idempotency key derivation, retry+backoff schedule, partial-progress resumption, server response contract.

**Out of scope:** REST endpoint catalog (§04); split-DB log storage (§39); auth lane (§31); rate-limit values (§05); classifier rules (§42); pointer-file shape (§41); auto-fix protocol (§44).

## 2. Transport (Normative)

| Concern | Value |
|---|---|
| Method | `POST` |
| Path | `/wp-json/git-logs/v1/upload` (canonical; per spec/22 §04) |
| Scheme | `https` only — `http` FORBIDDEN |
| Auth lane | SSH-key Lane B per spec/22 §31 (Authorization header derivation owned by §31; CLI MUST NOT invent a new lane) |
| Request body | `application/x-ndjson` — one JSON object per line, LF-terminated |
| Request encoding | `Content-Encoding: gzip` REQUIRED for any body >4 KiB; OPTIONAL otherwise |
| Response body | `application/json` — single JSON object per §6 contract |

**Forbidden:** `multipart/form-data`; chunked-transfer without `Content-Length` AND without `Transfer-Encoding: chunked` (the two are mutually exclusive per RFC 7230); `application/json` body with a top-level array (use NDJSON for streamability).

## 3. Per-Frame Envelope (Normative — Closed Set of 9 Fields)

Every NDJSON line MUST be a JSON object with `additionalProperties: false` carrying exactly these 9 fields:

| Field | Type | Required | Notes |
|---|---|---|---|
| `frameId` | string (uuid v4) | YES | Per-frame unique id; derived client-side; idempotency key per §4. |
| `repoIdentityHash` | string (64-hex sha256, lowercase) | YES | Per §40 §3 step 4; binds the frame to a repo. |
| `currentHead` | string (40-hex git SHA, lowercase) | YES | Per §40 §3 step 3; pinned at upload start, not per-frame. |
| `subcommand` | string enum {`log`,`status`,`diff`,`show`} | YES | The wrapped subcommand that produced the frame (per §40 §2 closed set). |
| `outcome` | string enum {`NORMAL`,`WARN`,`ERROR`,`INTERNAL`} | YES | Per §42 §2 closed set. |
| `classifierVersion` | string (SemVer) | YES | Banner version of `42-cli-classifier-rules.md` per §42 §6. |
| `payload` | string OR null | YES | Raw subcommand output for the frame; `null` when `outcome=INTERNAL` AND `redact: true` per §42 §2; `null` for binary diff frames per §42 DIFF-W1. |
| `emittedAt` | string (RFC 3339 UTC) | YES | CLI-side wall clock at frame emission; server MUST NOT trust for ordering — use `frameId` UUIDv4 timestamp prefix instead per §6. |
| `redact` | boolean | YES | `true` iff `outcome=INTERNAL`; `false` otherwise. Server MAY apply additional redaction policy on top. |

**Forbidden fields (any presence = `400 Bad Request` + `GL-UPLOAD-FORBIDDEN-FIELD`):** every entry from `41-cli-pointer-file-schema.md` §2 forbidden-field list (`token`/`apiKey`/`secret`/`password`/`sshKey`/`privateKey`/`userId`/`userEmail`/`ownerEmail`/`env`/`platform`) PLUS `clientIp`, `hostname`, `cwd`, `username`, `homeDir` (no host-fingerprinting under any circumstance).

## 4. Idempotency (Normative)

The CLI MUST set `Idempotency-Key: <batchId>` on every request, where `<batchId>` is a UUIDv4 generated once per CLI invocation (NOT per frame; one key per batch).

**Server contract** (delegated to spec/22 §04 — link-don't-restate):

- First request with a given `Idempotency-Key` → process normally, return `200 OK` + body per §6.
- Repeat request with the same `Idempotency-Key` AND identical body sha256 → return the **cached response** from the first request (no duplicate persistence; idempotent).
- Repeat request with the same `Idempotency-Key` BUT different body sha256 → `409 Conflict` + `GL-UPLOAD-IDEMPOTENCY-CONFLICT`.
- `Idempotency-Key` retention window: 24 hours server-side; after expiry, the same key MAY be reused.

**Frame-level idempotency:** the server MUST treat any duplicate `frameId` within a `repoIdentityHash` as already-persisted (no-op insert). This belt-and-braces guarantee covers partial-progress resumption per §5.

## 5. Retry & Backoff (Normative)

The CLI MUST NOT retry on `4xx` responses (those are contract violations — surface to the user). For `5xx` and network errors (DNS/TCP/TLS), the CLI MUST use **exponential backoff with full jitter**:

| Attempt | Base delay | Max delay (with jitter cap) | Notes |
|---|---|---|---|
| 1 | — | — | Initial request. |
| 2 | 1 s | 1.5 s | retry after first 5xx/network error. |
| 3 | 2 s | 3 s | |
| 4 | 4 s | 6 s | |
| 5 | 8 s | 12 s | |
| 6 | 16 s | 24 s | Final retry. |
| 7+ | — | — | Give up; emit `INTERNAL` to local stderr; pointer file's `uploadedAt`/`uploadUrl`/`autofixDownloadUrl` left untouched per §41. |

**Jitter formula:** `delay = base_delay * (0.5 + random()) ` clamped to the per-row max. Random source: cryptographically-random PRNG (Go `crypto/rand`, Rust `rand::rngs::OsRng`, etc.); `math/rand` FORBIDDEN.

**Resumption discipline:** on retry, the CLI MUST resend the **identical body** with the **identical `Idempotency-Key`** (§4 above guarantees no duplicate persistence). Re-deriving frames between attempts is FORBIDDEN — this would break the `Idempotency-Key`+sha256 contract.

**Forbidden:** linear backoff; exponential without jitter (causes thundering-herd); honoring `Retry-After` >24 s (server SHOULD NOT request waits longer than the final-retry max — if it does, give up + `INTERNAL`); retry on `400`/`401`/`403`/`409`/`410`/`422`.

## 6. Server Response Contract (Normative)

`200 OK` body (single JSON object, `additionalProperties: false`):

| Field | Type | Required | Notes |
|---|---|---|---|
| `batchId` | string (uuid v4) | YES | Echoes `Idempotency-Key`. |
| `framesReceived` | integer ≥0 | YES | Count of frames the server persisted (deduplicated). |
| `framesDeduplicated` | integer ≥0 | YES | Count of frames the server discarded as duplicate `frameId`. |
| `uploadedAt` | string (RFC 3339 UTC) | YES | Server-authoritative timestamp the CLI MUST write into pointer-file `uploadedAt` per §41. |
| `expiresAt` | string (RFC 3339 UTC) | YES | Server-authoritative log-retention horizon; CLI writes into pointer-file `expiresAt` per §41 (mirrors spec/05 AC-SD-23 TTL precedent). |
| `autofixDownloadUrl` | string (https URL) OR null | YES | Server-side per-batch fix URL; CLI writes into pointer-file `autofixDownloadUrl` per §41; `null` iff the batch contained 0 `ERROR` outcomes per §42. |

**Error responses** (single JSON object with `code` + `message` per spec/22 §15 envelope — link-don't-restate):

| Status | Code | Cause |
|---|---|---|
| `400` | `GL-UPLOAD-MALFORMED-NDJSON` | Non-NDJSON body OR a line failed §3 schema validation. |
| `400` | `GL-UPLOAD-FORBIDDEN-FIELD` | Per §3 forbidden-field list. |
| `401` | `GL-UPLOAD-AUTH-INVALID` | Per spec/22 §31 SSH-key Lane B contract. |
| `409` | `GL-UPLOAD-IDEMPOTENCY-CONFLICT` | Per §4. |
| `413` | `GL-UPLOAD-PAYLOAD-TOO-LARGE` | Per spec/22 §05 caps (link-don't-restate concrete byte values). |
| `429` | `GL-UPLOAD-RATE-LIMITED` | Per spec/22 §05 rate-limit contract; honor `Retry-After` up to §5 cap. |
| `5xx` | `GL-UPLOAD-SERVER-ERROR` | Triggers retry per §5. |

## 7. Forbidden Patterns

- Buffering the entire batch in memory before transmission (NDJSON is streamable — flush per frame OR per ≤256 KiB chunk).
- Re-deriving frames between retry attempts (breaks idempotency).
- Trusting CLI-side `emittedAt` for server-side ordering (use `frameId` UUIDv4 v7-style timestamp prefix when available; else server insertion order).
- Sending pointer-file fields (`uploadUrl`/`uploadedAt`/`expiresAt`/`autofixDownloadUrl`) in the request body — those are server-authoritative response fields, never client-supplied.
- Restating spec/22 §04 endpoint catalog, §05 rate-limit values, §15 error-envelope shape, §31 auth derivation, or §39 split-DB scoping inside this file (Lesson #36 violation).

---

## 8. Worked Example (Non-normative, `kind: example`)

> **Status:** Illustrative transcript per **Lesson #29** module-kind pin — examples are auditor-quoted evidence, NOT normative contract. The normative wire shape lives in §2–§7 above and §97 AC-85; restating it here in transcript form is FORBIDDEN. Any drift between this transcript and §2–§7 is resolved IN FAVOUR OF §2–§7 + AC-85.

### 8.1 Setup (givens)

- CLI: `riseup-git-logs v0.4.2`, classifier `42-cli-classifier-rules.md` v2.1.0
- Repo: `git@github.com:acme/widgets.git`, `currentHead = a1b2c3d4e5f60718293a4b5c6d7e8f9012345678`
- `repoIdentityHash = 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08` (per §40 §3)
- Lane B SSH key fingerprint: `SHA256:LP3...` (Authorization header derivation owned by §31)
- Batch: 3 frames — 1 `NORMAL` (`git log -3`), 1 `WARN` (`git status` with untracked file), 1 `ERROR` (`git diff` exit 128)
- Generated `Idempotency-Key = 5e1f4a2b-7c8d-4a3b-9e1f-2c3d4a5b6c7d` (UUIDv4, one per CLI invocation per §4)

### 8.2 First request (success path)

```http
POST /wp-json/git-logs/v1/upload HTTP/1.1
Host: logs.acme.example
Authorization: <derived per spec/22 §31 — link-don't-restate>
Content-Type: application/x-ndjson
Content-Encoding: gzip
Idempotency-Key: 5e1f4a2b-7c8d-4a3b-9e1f-2c3d4a5b6c7d
Content-Length: 4127

<gzip stream of 3 NDJSON lines, decompressed below for clarity:>
{"frameId":"01HZ8K9V3Q7M5N2P4R6T8X0Y1A","repoIdentityHash":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08","currentHead":"a1b2c3d4e5f60718293a4b5c6d7e8f9012345678","subcommand":"log","outcome":"NORMAL","classifierVersion":"2.1.0","payload":"commit a1b2c3d…\nAuthor: Alice <alice@acme.example>\nDate: 2026-05-08T10:14:22Z\n\n    feat: ship widget v3\n","emittedAt":"2026-05-08T10:15:00.142Z","redact":false}
{"frameId":"01HZ8K9V3Q7M5N2P4R6T8X0Y1B","repoIdentityHash":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08","currentHead":"a1b2c3d4e5f60718293a4b5c6d7e8f9012345678","subcommand":"status","outcome":"WARN","classifierVersion":"2.1.0","payload":"On branch main\nUntracked files:\n  scratch.txt\n","emittedAt":"2026-05-08T10:15:00.218Z","redact":false}
{"frameId":"01HZ8K9V3Q7M5N2P4R6T8X0Y1C","repoIdentityHash":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08","currentHead":"a1b2c3d4e5f60718293a4b5c6d7e8f9012345678","subcommand":"diff","outcome":"ERROR","classifierVersion":"2.1.0","payload":"fatal: bad revision 'HEAD~99'\n","emittedAt":"2026-05-08T10:15:00.301Z","redact":false}
```

Server replies (per §6):

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"batchId":"5e1f4a2b-7c8d-4a3b-9e1f-2c3d4a5b6c7d","framesReceived":3,"framesDeduplicated":0,"uploadedAt":"2026-05-08T10:15:01.044Z","expiresAt":"2026-06-07T10:15:01.044Z","autofixDownloadUrl":"https://logs.acme.example/wp-json/git-logs/v3/autofix/9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08/01HZ8K9V3Q7M5N2P4R6T8X0Y1C"}
```

CLI then writes `uploadedAt` / `expiresAt` / `autofixDownloadUrl` into the pointer file per §41 (link-don't-restate). `autofixDownloadUrl` is non-null because the batch contained ≥1 `ERROR` outcome.

### 8.3 Retry path (network blip on attempt 1)

Suppose attempt 1 fails with `ETIMEDOUT` after 5 s. CLI computes attempt-2 delay per §5: `base=1s, jitter ∈ [0.5, 1.5]s` ⇒ sleeps e.g. 1.27 s, then **resends the byte-identical body with the same `Idempotency-Key`**. If the original request had landed server-side (response lost in transit), the server returns the cached `200 OK` body from §8.2 with `framesDeduplicated: 0` (idempotency-cache hit per §4). If the original never landed, the server processes it normally and returns identical fields. Either outcome is indistinguishable to the CLI — that is the point.

### 8.4 Forbidden-field rejection (negative path)

A buggy CLI build that accidentally includes `hostname` in each frame triggers:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{"code":"GL-UPLOAD-FORBIDDEN-FIELD","message":"frame[0]: field 'hostname' is forbidden per §3 forbidden-field list","details":{"frameIndex":0,"field":"hostname"}}
```

Per §5, `400` MUST NOT trigger retry — the CLI surfaces the error to the user (exit code per spec/13 AC-21 typed `ExitCode` enum, link-don't-restate) and leaves the pointer file untouched (`uploadedAt`/`expiresAt`/`autofixDownloadUrl` per §41 stay at their pre-attempt values).

### 8.5 Idempotency-conflict rejection

If the CLI mistakenly mutates frames between retry attempts (FORBIDDEN per §5 + §7), the server responds:

```http
HTTP/1.1 409 Conflict

{"code":"GL-UPLOAD-IDEMPOTENCY-CONFLICT","message":"Idempotency-Key 5e1f4a2b-7c8d-4a3b-9e1f-2c3d4a5b6c7d already seen with different body sha256"}
```

Treated as a 4xx contract violation — no retry, surface to user, pointer file untouched.

### 8.6 What this transcript IS NOT

This §8 is illustrative evidence per `kind: example`. It does not extend, narrow, or supersede any rule in §2–§7. If a future contributor needs to change the wire shape, the edit lands in §2–§7 + §97 AC-85 (with full lockstep); §8 is then refreshed to mirror — never the inverse. Lesson #29 module-kind pin applies (this file's front-matter `kind: interface-contract`; the §8 sub-section is `kind: example` by Lesson #29's quoted-evidence rule).

## Cross-link

- §97 AC-85 binds this file (governing AC for slot §43)
- §97 AC-80 Sibling File Delegation Map row 37 (`43-cli-upload-protocol.md` → AC-85)
- §40 §2 (closed wrap-set source for `subcommand` field) + §40 §3 (identity discovery for `repoIdentityHash`/`currentHead` fields)
- §41 (pointer-file fields written from §6 response — `uploadedAt`/`expiresAt`/`autofixDownloadUrl`)
- §42 (classifier outcomes consumed in `outcome`/`classifierVersion`/`redact` fields)
- §44 (auto-fix protocol consumes `autofixDownloadUrl` from §6 response)
- spec/22 §04 (REST endpoint catalog — link-don't-restate)
- spec/22 §05 (payload caps + rate-limit contract — link-don't-restate)
- spec/22 §15 (`GL-UPLOAD-*` error code surface — owning module)
- spec/22 §31 (SSH-key Lane B auth — link-don't-restate)
- spec/22 §39 (split-DB log storage scoping — link-don't-restate)
