# REST API Endpoints (v2)

**Version:** 2.9.6  
**Updated:** 2026-04-28 (Phase P4: §1.2 "Pre-parse caps & validation order" subsection added — surfaces the four `ConfigKv` enforcement caps (`RatePerMinPerProfile`, `MaxPushPayloadBytes`, `MaxLinesPerPush`, `MaxLineBytes`) + 11-step strict validation order so a blind implementer learns gate ordering without cross-walking §15/§18/§97. Closes GAP-V2-10. No DDL/AC/error-code change — purely a cross-walk-elimination doc surface. Phase P3 PreviousHasError ack contract unchanged.)
**Namespace:** `/wp-json/git-logs/v2`

---

## Common

- All write endpoints respond with a structured acknowledgement and a retrieval hint.
- All statuses/kinds/types are Enum-backed (no magic strings).
- All endpoint hits write to `AuditTrail`; no error is swallowed.

### Standard Ack Envelope

```json
{
  "Status": "Success",
  "Message": "Logs appended.",
  "TraceId": "uuid-v4",
  "PreviousHasError": false,
  "Retrieval": {
    "Logs": "/wp-json/git-logs/v2/get-logs",
    "ErrorLogs": "/wp-json/git-logs/v2/get-error-logs",
    "Pipeline": "/wp-json/git-logs/v2/get-pipeline-logs"
  }
}
```

**Field contract — `PreviousHasError`** (v2.9.5 — Phase P3, closes GAP-V2-04):

- **Type:** `boolean`
- **Required:** Yes on write endpoints #1–#4 (`/append-log`, `/fixed-log`, `/clear-log`, `/clear-log-all`); ABSENT on read endpoints #5–#10.
- **Semantics:** `true` iff the **prior** `Pipeline` row for this `(RepoVersionId, BranchName, PipelineName)` had `HasError=1` **immediately before** the current request was applied. Computed by reading `Pipeline.PreviousHasError` (set atomically per AC-75 single-statement write contract) BEFORE the current request mutates it. On a fresh `(Repo, Branch, Pipeline)` triple with no prior row, `PreviousHasError` MUST be `false` (mirrors AC-73 `first-failure` vs `still-failing` boundary).
- **On `/append-log` (#1):** lets the client decide whether to follow up with `PUT /fixed-log` automatically — if the new request resolves to `HasError=false` AND `PreviousHasError=true`, the client SHOULD chain a `/fixed-log` call (per AC-13).
- **On `/fixed-log` (#2):** echoes the state BEFORE clearing — clients use this to detect no-op fixed calls (`PreviousHasError=false` ⇒ the pipeline was already green; the call was redundant but not erroneous).
- **On `/clear-log` (#3) and `/clear-log-all` (#4):** echoes pre-clear state for audit trail correlation; the cleared row's prior state is otherwise unrecoverable.
- **Atomicity:** MUST be read in the same SQL transaction as the write (`BEGIN IMMEDIATE` … `SELECT Pipeline.PreviousHasError WHERE …` … `UPDATE Pipeline SET …`) to avoid a read-modify-write race with a concurrent `/append-log` on the same triple. Mirrors AC-75 ORM-split fallback rules.
- **Cross-refs:** §01 `Pipeline.PreviousHasError` glossary entry; §97 AC-13 (auto-fix), AC-73 (state-transition matrix), AC-74 (`Header.StateTransition` NDJSON exposure), AC-75 (atomicity); §17 `Ack` schema (lockstep — added in this phase).

### Standard Error Envelope

```json
{
  "Status": "Rejected",
  "ErrorCode": "GL-VALIDATION-001",
  "Message": "RepoUrl does not match GitProfile acceptance.",
  "TraceId": "uuid-v4"
}
```

---

## Endpoint Map

| # | Method | Path | Purpose | Auth |
|---|--------|------|---------|------|
| 1 | POST | `/append-log` | Append/stream log lines | TempToken + URL/Branch |
| 2 | PUT  | `/fixed-log` | Mark pipeline error cleared | TempToken + URL/Branch |
| 3 | POST | `/clear-log` | Clear logs for a single pipeline | TempToken + URL/Branch |
| 4 | POST | `/clear-log-all` | Clear all logs for repo+branch | TempToken + URL/Branch |
| 5 | GET  | `/get-logs` | All logs for repo at commit | App Password / Cookie |
| 6 | GET  | `/get-logs?q=…` | URL-style variant of #5 | App Password / Cookie |
| 7 | GET  | `/get-pipeline-logs` | One pipeline's logs at commit | App Password / Cookie |
| 8 | GET  | `/get-pipeline-logs?q=…` | URL-style variant of #7 | App Password / Cookie |
| 9 | GET  | `/get-error-logs` | Error logs across all pipelines | App Password / Cookie |
| 10 | GET | `/get-pipeline-error-logs` | Error logs for one pipeline | App Password / Cookie |

> **Logical-endpoint vs HTTP-path count.** This map lists **10 logical endpoints** but they collapse to **8 HTTP paths** in `17-openapi.yaml`. Rows #5/#6 share path `/get-logs` (the `?q=…` variant is a query parameter, not a separate route); same for #7/#8 sharing `/get-pipeline-logs`. AC-11 ("all 10 endpoints exist with the exact request/response field names") is satisfied by the 8-path OpenAPI document because the `q` query parameter is documented on the parent path. Implementations MUST handle both shapes (explicit `RepoUrl`+`Branch` AND shorthand `q=…`) inside the same route handler. Adding a brand-new logical endpoint requires either a new path or a new query-param shape — never silent overloading of an existing path.

---

## 1. POST /append-log

**Body**
```json
{
  "RepoUrl": "https://github.com/alimtvnetwork/macro-ahk-v23",
  "RootRepo": "https://github.com/alimtvnetwork/macro-ahk",
  "Branch": "main",
  "TempToken": "…",
  "Token": "…",
  "PipelineName": "build",
  "GitSha256": "abc123…",
  "Logs": ["line 1", "line 2"],
  "ErrorLogs": ["err 1"],
  "FilePaths": ["src/foo.ts"],
  "HasError": true
}
```
- **Streaming**: `Transfer-Encoding: chunked` accepted; lines processed incrementally.
- **Effect**: insert `LogEntry` + `ErrorLogEntry` rows; if `HasError=true`, set `Pipeline.HasError=1`. Append `History` (ActionType=`Append`) and `Action` row.
- **Response**: standard ack with `Retrieval`.

### 1.1 Streaming wire format (v2.9.4 — Phase P2)

When the client wants to stream `Logs`/`ErrorLogs` incrementally instead of buffering the full request body, it MUST opt in via a sentinel header and use NDJSON framing. This pins the byte-level contract referenced by `28-universal-ci-cli/06-log-shipping-contract.md` (AC-28-06).

| Field | Value | Notes |
|-------|-------|-------|
| Request header | `X-GL-Stream: 1` | Sentinel — without it the body MUST be a single JSON object as in §1 above |
| `Content-Type` | `application/x-ndjson; charset=utf-8` | Required iff `X-GL-Stream: 1` is present |
| `Transfer-Encoding` | `chunked` | Required iff `X-GL-Stream: 1` is present; `Content-Length` MUST be absent |
| Frame separator | exactly one `\n` (LF, U+000A) | Never CRLF; trailing LF on last frame allowed but not required |

**Frame sequence (in order):**

1. **`StreamHeader`** frame (exactly one, first):
   ```json
   {"StreamHeader":true,"RepoUrl":"…","RootRepo":"…","Branch":"main","TempToken":"…","Token":"…","PipelineName":"build","GitSha256":"abc123…","FilePaths":["src/foo.ts"]}
   ```
   Carries the same identity fields as the buffered §1 body MINUS `Logs`, `ErrorLogs`, `HasError`.
2. **`Line`** frames (zero or more):
   ```json
   {"Line":"build started","Severity":"Info"}
   {"Line":"missing dep","Severity":"Error"}
   ```
   `Severity` MUST be `"Info"` or `"Error"` (mirrors §01 `LogSeverity` enum). Server routes to `LogEntry` vs `ErrorLogEntry` accordingly.
3. **`StreamFooter`** frame (exactly one, last):
   ```json
   {"StreamFooter":true,"HasError":true}
   ```
   `HasError` is authoritative — server sets `Pipeline.HasError` from this field, NOT from any per-`Line` severity tally. This makes "stream of all-Info lines but final HasError=true" a valid, lossless representation.

**Server behavior:**

- Server MUST validate `StreamHeader` BEFORE processing any `Line` frames; if `StreamHeader` is missing, malformed, or appears after a `Line` frame, respond `400` with `GL-STREAM-NO-HEADER`.
- Server MUST close the request and respond `400` with `GL-STREAM-NO-FOOTER` if EOF arrives before a `StreamFooter` frame; partial inserts MUST be rolled back.
- Server MUST reject (`413` `GL-STREAM-TOO-MANY-LINES`) once line count exceeds `NdjsonMaxRowsPerStream` (§11.4); cap reuse is intentional — same backpressure ceiling for ingest and retrieval.
- Server MUST ignore unknown frame keys (forward-compatible) but MUST reject unknown frame discriminators (`{"Foo":true,…}` with no recognized leading key) with `GL-STREAM-UNKNOWN-FRAME`.

**Response:** standard ack envelope per §Common — buffered, NOT streamed. The `Retrieval` hint is computed after the `StreamFooter` is consumed.

### 1.2 Pre-parse caps & validation order (v2.9.6 — Phase P4)

Closes GAP-V2-10. The four enforcement caps below are seeded in `18-schema.sql` `ConfigKv` and apply to **both** the buffered §1 body and the §1.1 NDJSON streaming variant. They are listed here (rather than only in §15/§18/§97 AC-12/AC-27) so a blind implementer reading §04 top-to-bottom learns the validation gate order WITHOUT cross-walking three files.

| # | ConfigKv key | Default | Scope | When checked | Error code (§15) | HTTP |
|---|---|---|---|---|---|---|
| 1 | `RatePerMinPerProfile` | `60` | Per-Profile (token bucket; refills at 1/sec) | **BEFORE** body parse, immediately after Profile resolution from `TempToken` | `GL-RATE-LIMIT-EXCEEDED` | `429` (with `Retry-After`) |
| 2 | `MaxPushPayloadBytes` | `1048576` (1 MiB) | Per-request | Buffered: from `Content-Length` header BEFORE reading body. Streaming: incremental running counter — abort mid-stream as soon as crossed. | `GL-PAYLOAD-TOO-LARGE` | `413` |
| 3 | `MaxLinesPerPush` | `10000` | `len(Logs) + len(ErrorLogs)` (buffered) OR cumulative `Line` frame count (streaming) | Buffered: after JSON parse, BEFORE INSERT. Streaming: incremental — abort on the (10001)th `Line` frame. | `GL-LINES-TOO-MANY` | `413` |
| 4 | `MaxLineBytes` | `65536` (64 KiB) | Per-line UTF-8 byte length | Per-line, BEFORE INSERT. Oversize lines are TRUNCATED and tagged `Warn` per AC-27 — no `GL-*` error raised, the push continues. | (none — soft-truncation) | n/a |

**Strict validation order (gates fail fast, top to bottom):**

1. **TLS / transport** (Lane B SSH key signature verification per §05/§31, if `SshAuthMode != off`).
2. **Auth** — resolve `TempToken` → `Profile`; respond `401` `GL-AUTH-INVALID` if unknown/expired.
3. **Cap #1** — token bucket charge for resolved `ProfileId`; respond `429` `GL-RATE-LIMIT-EXCEEDED` if empty.
4. **Cap #2 (Content-Length pre-check)** — for buffered requests, reject `413` `GL-PAYLOAD-TOO-LARGE` BEFORE allocating any read buffer. For streaming requests (`Transfer-Encoding: chunked` + `X-GL-Stream:1`), this gate becomes the running-total cap in step 6.
5. **Body parse** — `JSON.parse()` (buffered) OR NDJSON frame loop (streaming).
6. **Cap #2 (streaming running-total)** — abort mid-stream with `413` `GL-PAYLOAD-TOO-LARGE` per AC-12 incremental contract; rollback partial inserts (the §97 AC-13 sticky-`HasError` atomicity contract makes partial-commit unsafe).
7. **Cap #3** — `len(Logs)+len(ErrorLogs)` (buffered) OR `Line` frame count (streaming) — `413` `GL-LINES-TOO-MANY`.
8. **Cap #4** — per-line — TRUNCATE + `Warn` tag (no error code per AC-27).
9. **Field validation** — `RepoUrl`/`Branch`/`PipelineName` shape per §05; reject `400` `GL-VALIDATION-*` on type/format errors.
10. **GitProfile acceptance match** — reject `400` `GL-VALIDATION-001` if `RepoUrl` does not match the resolved `Profile`'s GitProfile acceptance regex.
11. **INSERT** — atomic per AC-75 (`BEGIN IMMEDIATE` + `Pipeline.PreviousHasError` read + `UPDATE` + `INSERT LogEntry/ErrorLogEntry` + `INSERT History/Action` + `COMMIT`).

**Wall-clock cap (orthogonal):** `ConfigKv.AppendLogMaxStreamSec` (recommended default `30` s, mentioned in §97 AC-12) MUST cap total request time for streaming requests to prevent slow-loris worker exhaustion. Exceeding the cap returns `GL-INGEST-TIMEOUT` (§15). This cap does NOT apply to buffered requests under `MaxPushPayloadBytes` — `Content-Length` already bounds them.

**Cross-refs:** §18 ConfigKv seed rows (lines 426–429); §15 `Rate limiting + payload (Lane B)` table; §97 AC-12 (incremental enforcement contract), AC-27 (soft-truncation), AC-13 (atomicity), AC-75 (single-statement write); §31 (SSH lane validation order, step 0 above).

## 2. PUT /fixed-log

**Body**
```json
{ "RepoUrl": "...", "Branch": "main", "TempToken": "...", "RootRepo": "...", "Token": "...", "PipelineName": "build" }
```
- **Effect**: `Pipeline.HasError=0`. History `ActionType=Fixed`, Action row inserted.

## 3. POST /clear-log

**Body** identical to #2.
- **Effect**: delete `LogEntry`+`ErrorLogEntry` for `(Pipeline)`. History `ActionType=Clear`.

## 4. POST /clear-log-all

**Body** (no `PipelineName`)
```json
{ "RepoUrl": "...", "Branch": "...", "TempToken": "...", "RootRepo": "...", "Token": "..." }
```
- **Effect**: delete logs for all pipelines on `(RepoVersion, Branch)`. History `ActionType=ClearAll`.

---

## 5. GET /get-logs

**Body**
```json
{ "RepoUrl": "...", "GitSha256": "..." }
```
**Response**
```json
{
  "RepoUrl": "...",
  "RootRepo": "...",
  "BranchName": "main",
  "PipelineNames": ["build", "test"],
  "IsPass": false,
  "HasError": true,
  "ErrorLogs": [{ "PipelineName": "build", "LogText": "..." }],
  "Logs":      [{ "PipelineName": "build", "LogText": "..." }]
}
```

## 6. GET /get-logs?q=github.com/{org}/{repo}

Same response as #5; repo from query string, body carries only `GitSha256`.

## 7. GET /get-pipeline-logs

**Body**: `{ RepoUrl, GitSha256, PipelineName }`  
**Response**
```json
{
  "RepoUrl": "...", "RootRepo": "...", "BranchName": "main", "PipelineName": "build",
  "IsPass": false, "HasError": true,
  "ErrorLogs": ["err 1"],
  "Logs":      ["line 1", "line 2"]
}
```

## 8. GET /get-pipeline-logs?q=github.com/{org}/{repo}

Same response as #7; repo from query string; body `{ GitSha256, PipelineName }`.

## 9. GET /get-error-logs

**Body**: `{ RepoUrl, GitSha256 }`
**Response**
```json
{
  "RepoUrl": "...", "RootRepo": "...", "BranchName": "main",
  "PipelineNames": ["build", "test"],
  "IsPass": false, "HasError": true,
  "ErrorLogs": [{ "PipelineName": "build", "LogText": "..." }]
}
```

## 10. GET /get-pipeline-error-logs

**Body**: `{ RepoUrl, GitSha256, PipelineName }`
**Response**
```json
{
  "RepoUrl": "...", "RootRepo": "...", "BranchName": "main", "PipelineName": "build",
  "IsPass": false, "HasError": true,
  "ErrorLogs": ["err 1"]
}
```

---

## 11. NDJSON Streaming Retrieval (v2.9.2 — NEW in Phase 8)

### 11.1 Why streaming

Per `AC-49..AC-52` (Per-SHA Split-DB), a single `(PipelineId, Sha)` can hold **millions of log lines** in its `<Sha>.db` file. Buffering the full result into the JSON response objects defined in §5–§10 above forces the WP REST layer to materialize the entire payload in PHP memory before flushing — which OOMs on long-running CI pipelines and pegs `MaxOpenShaDbHandles` (AC-52, default `32`) for the duration of the buffer build.

NDJSON streaming lets clients (CI dashboards, log tailers, `wp git-logs tail`) consume rows incrementally as the per-SHA cursor walks them, with one open SQLite handle held for the **streaming window** only.

### 11.2 Opt-in mechanism

Streaming is **opt-in per request** via the standard HTTP content-negotiation header. Endpoints #5–#10 (the six GET endpoints) MUST honor the negotiation; endpoints #1–#4 (writes) MUST ignore it.

| Request `Accept` header | Server behavior | Response `Content-Type` |
|---|---|---|
| *(absent)* or `application/json` | Buffered JSON object as defined in §5–§10 | `application/json; charset=utf-8` |
| `application/x-ndjson` | NDJSON stream per §11.3 | `application/x-ndjson; charset=utf-8` |
| `application/x-ndjson, application/json;q=0.5` | NDJSON stream (q-value preference resolved to NDJSON) | `application/x-ndjson; charset=utf-8` |
| `application/x-ndjson` AND endpoint ∈ {#1..#4} | Header silently ignored; respond with §5–§10 ack | `application/json; charset=utf-8` |
| `application/x-ndjson` with `?stream=false` query | Streaming disabled by client override; buffered response | `application/json; charset=utf-8` |

The server MUST also set `Transfer-Encoding: chunked` and `X-Content-Type-Options: nosniff` on every NDJSON response. The server MUST NOT set `Content-Length` on streaming responses.

### 11.3 Frame schema

An NDJSON response is a sequence of JSON objects separated by exactly one `\n` (LF, U+000A) — never CRLF, never trailing LF on the last frame is required but allowed. Each object MUST carry a `Type` discriminator. Five frame types are defined:

#### 11.3.1 `Header` frame (always first, exactly one)

```json
{"Type":"Header","Schema":"git-logs-v2/ndjson@1","RepoUrl":"github.com/acme/api","RootRepo":"github.com/acme/api","BranchName":"main","Sha":"a1b2c3…","PipelineNames":["build","test"],"TotalRowsHint":42117,"StreamId":"uuid-v4","StartedAt":1745638800,"StateTransition":"first-failure"}
```

- `Schema` MUST be `"git-logs-v2/ndjson@1"` for v2.9.2 (bump on breaking change).
- `TotalRowsHint` is the `ShaRegistry.RowCount` mirror (AC-50) — **advisory only**, may drift if the per-SHA file is being written concurrently.
- `StreamId` MUST be propagated to `AuditTrail.RequestId` (AC-30) so server-side correlation works.
- `StateTransition` (added v2.9.3 Phase 12) is OPTIONAL and emitted ONLY on single-pipeline scopes (endpoints #7/#8/#9/#10 — i.e. `/get-pipeline-logs`, `/get-pipeline-error-logs`) when the request resolves to exactly one `Pipeline` row. The value is one of the four §01 glossary v3.8.10 labels — `"still-green"`, `"first-failure"`, `"still-failing"`, `"just-recovered"` — derived purely from the row's `(PreviousHasError, HasError)` tuple per §97 AC-73. On repo-scope endpoints (#5/#6 `/get-logs`, `/get-error-logs`) and on 404 / multi-pipeline resolutions, the field MUST be ABSENT entirely (never `null`, never `"unknown"`) per §97 AC-74. Clients MUST treat absence as "not-applicable" rather than as an error — older spec versions and broader-scope endpoints simply omit the field.

#### 11.3.2 `Log` frame (zero or more)

```json
{"Type":"Log","Seq":1,"PipelineName":"build","SeverityId":3,"SeverityName":"Info","LogText":"npm install starting","OccurredAt":1745638801,"LineByteLen":34}
```

- `Seq` is monotonic per-stream starting at `1` — clients use it to detect frame loss.
- `SeverityId` references the canonical `LogSeverity` lookup (denormalized into the per-SHA file per AC-51, so the value is stable even if the root DB drifts).
- `SeverityName` is included for human readability — clients SHOULD prefer `SeverityId` for any logic.
- `LineByteLen` is the byte length of `LogText` BEFORE any §10 truncation (so AC-27 truncation is observable from the stream).

For endpoint #5/#6 (`/get-logs`) the stream emits both Info-level and Error-level rows ordered by `OccurredAt ASC`. For endpoint #9/#10 (`/get-error-logs`) the stream filters to severity ≥ `Error` server-side.

#### 11.3.3 `ErrorLog` frame (zero or more — emitted by #9/#10 only)

```json
{"Type":"ErrorLog","Seq":42,"PipelineName":"build","SeverityId":5,"SeverityName":"Error","LogText":"jest: 3 tests failed","OccurredAt":1745638901,"FirstSeenAt":1745638901,"OccurrenceCount":1}
```

- `OccurrenceCount` reflects the §06 dedup-window collapse (AC-05). A re-emitted identical line within the 60s window increments this counter on the EXISTING row rather than emitting a new frame.

#### 11.3.4 `Progress` frame (zero or more, optional)

```json
{"Type":"Progress","RowsEmitted":10000,"BytesEmitted":1572864,"ElapsedMs":420}
```

- Emitted at most once per `ConfigKv.NdjsonProgressEveryRows` rows (default `10000`) OR once per `ConfigKv.NdjsonProgressEveryMs` (default `2000`), whichever fires first.
- Lets clients render a progress bar without the buffered `TotalRowsHint` going stale.

#### 11.3.5 `End` frame (always last, exactly one)

```json
{"Type":"End","Status":"Complete","RowsEmitted":42117,"BytesEmitted":6291456,"DurationMs":1340,"FinalSeq":42117}
```

- `Status ∈ { "Complete", "Truncated", "Error" }`.
- `Complete` — cursor walked the full per-SHA file successfully.
- `Truncated` — server-imposed cap (`ConfigKv.NdjsonMaxRowsPerStream`, default `1000000`) hit; client SHOULD re-request with a `?after-seq=` cursor (§11.6).
- `Error` — mid-stream failure; an `Error` frame (§11.3.6) precedes this `End` and `Status="Error"` is informational only.

#### 11.3.6 `Error` frame (zero or one — only on mid-stream failure)

```json
{"Type":"Error","Code":"GL-SHA-DB-OPEN-FAILED","Message":"per-SHA file vanished mid-stream","HttpStatus":503,"AfterSeq":15723,"Detail":{"Sha":"a1b2c3…","DbFilePath":"logs/a1/b2c3…db"}}
```

- The `Code` MUST be a §15 `GL-*` code. New codes valid in this position: `GL-SHA-DB-OPEN-FAILED` (503), `GL-SHA-DB-CHECKSUM-MISMATCH` (500), `GL-SHA-DB-QUOTA-EXCEEDED` (507), `GL-NDJSON-CLIENT-DISCONNECT` (499 informational), `GL-NDJSON-CURSOR-LOST` (500).
- `AfterSeq` tells the client which `Seq` was the last successfully emitted `Log`/`ErrorLog` frame so a resume request (§11.6) does not double-emit.
- The HTTP status code on an `Error` frame is **always 200** at the response-line level (the response already started streaming, so the status header was committed before the error was knowable). Clients MUST treat the `Error` frame body as authoritative.

### 11.4 Ordering and atomicity guarantees

1. Frames MUST appear in this order: exactly one `Header` → zero or more `Log`/`ErrorLog`/`Progress` (interleaved, but `Log`/`ErrorLog` strictly ordered by `Seq`) → optional `Error` → exactly one `End`.
2. Each frame MUST be a single line of UTF-8 JSON. The server MUST `flush()` the output buffer after each frame so clients receive frames in real-time (no Nagle batching beyond the underlying TCP layer).
3. The server MUST NOT split a JSON object across `\n`. If a single object exceeds `ConfigKv.NdjsonMaxFrameBytes` (default `262144` = 256 KiB), the `LogText` is truncated to fit and a `"Truncated":true` field is added to the frame (mirrors AC-27 `Warn` truncation semantics for ingest).
4. On client disconnect mid-stream, the server MUST detect the broken pipe within 1 flush cycle, close the per-SHA handle (returning it to the AC-52 pool), append a `GL-NDJSON-CLIENT-DISCONNECT` row to `AuditTrail` (no `Error` frame is sent — the socket is gone), and abandon the cursor.

### 11.5 New ConfigKv keys (Phase 8)

Three keys are added to govern streaming behavior. They are **defined** by this section; physical seeding into `18-schema.sql` is **deferred to a follow-up phase** to keep Phase 8 doc-only per scope discipline.

| Key | Default | Purpose | Range |
|---|---|---|---|
| `NdjsonProgressEveryRows` | `10000` | Emit `Progress` frame every N rows. `0` disables progress frames. | 0..1000000 |
| `NdjsonProgressEveryMs` | `2000` | Emit `Progress` frame every N ms (whichever fires first vs. rows). `0` disables time-based progress. | 0..60000 |
| `NdjsonMaxRowsPerStream` | `1000000` | Hard cap on rows emitted per stream; on hit, end with `Status:"Truncated"`. | 1..10000000 |
| `NdjsonMaxFrameBytes` | `262144` | Per-frame JSON byte cap; oversized `LogText` truncated with `"Truncated":true`. | 4096..1048576 |

### 11.6 Resume / cursor semantics

Streaming retrieval supports a single resume mechanism: query parameter `?after-seq=N` on endpoints #5/#6/#7/#8/#9/#10. When supplied:

- The server skips the first `N` rows of the per-SHA cursor walk and emits the `Header` frame with `StartedAt` = original stream's `StartedAt` echoed if the client also passes `?stream-id=<uuid>` (otherwise a fresh UUID is generated).
- If `N` exceeds the current `ShaRegistry.RowCount`, the server emits `Header` then `End` with `Status:"Complete"` and `RowsEmitted:0` — NOT an error.
- Resume is **best-effort, not transactional**: if the per-SHA file was pruned (AC-53) between the original stream and the resume, the response is `Header` → `Error{Code:"GL-NDJSON-CURSOR-LOST"}` → `End{Status:"Error"}`.

### 11.7 Endpoint applicability matrix

| Endpoint | NDJSON supported | Frame mix |
|---|---|---|
| #1 `/append-log` | ❌ (write) | n/a |
| #2 `/fixed-log` | ❌ (write) | n/a |
| #3 `/clear-log` | ❌ (write) | n/a |
| #4 `/clear-log-all` | ❌ (write) | n/a |
| #5 `/get-logs` | ✅ | `Header` → `Log`* + `ErrorLog`* (interleaved by `OccurredAt`) → `End` |
| #6 `/get-logs?q=…` | ✅ | same as #5 |
| #7 `/get-pipeline-logs` | ✅ | `Header` → `Log`* (one PipelineName) → `End` |
| #8 `/get-pipeline-logs?q=…` | ✅ | same as #7 |
| #9 `/get-error-logs` | ✅ | `Header` → `ErrorLog`* (severity ≥ Error) → `End` |
| #10 `/get-pipeline-error-logs` | ✅ | same as #9 (filtered to one PipelineName) |

### 11.8 Wire example (truncated)

```
HTTP/1.1 200 OK
Content-Type: application/x-ndjson; charset=utf-8
Transfer-Encoding: chunked
X-Content-Type-Options: nosniff

{"Type":"Header","Schema":"git-logs-v2/ndjson@1","RepoUrl":"github.com/acme/api","BranchName":"main","Sha":"a1b2c3","PipelineNames":["build"],"TotalRowsHint":3,"StreamId":"4f8a…","StartedAt":1745638800}
{"Type":"Log","Seq":1,"PipelineName":"build","SeverityId":3,"SeverityName":"Info","LogText":"npm install","OccurredAt":1745638801,"LineByteLen":11}
{"Type":"Log","Seq":2,"PipelineName":"build","SeverityId":3,"SeverityName":"Info","LogText":"npm test","OccurredAt":1745638850,"LineByteLen":8}
{"Type":"ErrorLog","Seq":3,"PipelineName":"build","SeverityId":5,"SeverityName":"Error","LogText":"jest failed","OccurredAt":1745638901,"FirstSeenAt":1745638901,"OccurrenceCount":1}
{"Type":"End","Status":"Complete","RowsEmitted":3,"BytesEmitted":612,"DurationMs":47,"FinalSeq":3}
```

### 11.9 Cross-references

- §10 — Limits & rate caps (AC-26 / AC-27 still apply to `LogText` truncation in stream frames).
- §15 — Error codes (`GL-SHA-DB-*`, new `GL-NDJSON-*` codes).
- §17 — OpenAPI must add `application/x-ndjson` content variants for endpoints #5–#10.
- §18 — ConfigKv defaults (4 new `Ndjson*` keys defined in §11.5; physical seeding deferred to follow-up).
- §39 — Per-SHA file is the cursor source (AC-49..AC-52).
- §97 — AC coverage for streaming behavior is **deferred to a future AC quality pass** (Phase 7 closed at AC-66 before Phase 8 doc landed).
