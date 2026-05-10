# AC-11 — Endpoint Inventory (Section D Detail)

**Status:** active · **Phase:** D-1 (REST surface tier-1 binding) · **Bound from:** `97-acceptance-criteria.md` §AC-11
**Mirror class:** AC-05 (§53) · AC-12 (§55) · AC-23 (§56) — Phase D normative-surface promotions
**Generated:** 2026-05-10 (Lesson #19 audit-boundary pin; Lesson #36 link-don't-restate; Lesson #34 walker-cap classification)

---

## Why this file exists

Pre-promotion AC-11 in §97 was a 4-line stub that delegated the entire per-endpoint contract to **§17 OpenAPI** (tier-2). The audit walker tier-1 bundle (`{00,97,98,99}-*.md`, ~90 KB cap per spec/27 AC-34-09) does **not** see §17, so AI auditors repeatedly flagged "missing per-endpoint contract" as a D5 spec defect (Lesson #19 boundary gap).

This file is the **tier-1 binding surface** for the 10 logical endpoints. Full JSON wire schemas remain canonical in **`17-openapi.yaml` v2.9.4+** (Lesson #36 — restating them inline is FORBIDDEN dual-source drift).

## Per-endpoint binding matrix (10 logical → 8 HTTP paths)

The `?q=` query-param collapse rule folds rows #5/#6 onto `/get-logs` and rows #7/#8 onto `/get-pipeline-logs`, yielding 8 distinct HTTP paths.

| # | Method | Path | Request body schema (§17) | Response body schema (§17) | Auth class (§05) | Error envelope codes (§15) |
|---|---|---|---|---|---|---|
| 1 | POST | `/append-log` | `AppendLogRequest` (chunked NDJSON OR single JSON; §04 §1.1 + AC-12) | `AckResponse` (per AC-14) | TempToken + URL/Branch (Lane A) | `GL-PAYLOAD-TOO-LARGE`, `GL-INGEST-TIMEOUT`, `GL-STREAM-*`, `GL-AUTH-*` |
| 2 | PUT | `/fixed-log` | `FixedLogRequest` (`{PipelineId, Branch, Sha, PreviousHasError?}`) | `AckResponse` (per AC-14) | TempToken + URL/Branch | `GL-AUTH-*`, `GL-INTERNAL` |
| 3 | POST | `/clear-log` | `ClearLogRequest` (`{PipelineId}`) | `AckResponse` (per AC-14, empty `Retrieval` URLs valid) | TempToken + URL/Branch | `GL-AUTH-*` |
| 4 | POST | `/clear-log-all` | `ClearLogAllRequest` (`{RepoUrl, Branch}`) | `AckResponse` (per AC-14, empty `Retrieval` URLs valid) | TempToken + URL/Branch | `GL-AUTH-*` |
| 5 | GET | `/get-logs` | n/a (query `?RepoUrl=&Branch=&Sha=` OR `?q=`) | `LogPage` JSON OR NDJSON `Header→Log*→End` (per AC-67) | App Password / Cookie (Lane A) | `GL-AUTH-*`, `GL-NDJSON-*`, `GL-SHA-DB-*` |
| 6 | GET | `/get-logs?q=…` | n/a (URL-style `?q=github.com/{org}/{repo}/{branch}/{sha}`) | as #5 | as #5 | as #5 |
| 7 | GET | `/get-pipeline-logs` | n/a (query `?PipelineId=`) | `PipelineLogPage` JSON OR NDJSON (incl. `Header.StateTransition` per AC-74 when scope=1 pipeline) | App Password / Cookie | `GL-AUTH-*`, `GL-NDJSON-*` |
| 8 | GET | `/get-pipeline-logs?q=…` | n/a (URL-style) | as #7 | as #7 | as #7 |
| 9 | GET | `/get-error-logs` | n/a (query `?RepoUrl=&Branch=&Sha=`) | `ErrorLogPage` JSON OR NDJSON (severity ≥ Error filter server-side) | App Password / Cookie | `GL-AUTH-*`, `GL-NDJSON-*` |
| 10 | GET | `/get-pipeline-error-logs` | n/a (query `?PipelineId=`) | `ErrorLogPage` JSON OR NDJSON (incl. `Header.StateTransition` per AC-74) | App Password / Cookie | `GL-AUTH-*`, `GL-NDJSON-*` |

## Cross-cutting envelope contracts

- **Write success (#1–#4):** body MUST conform to `AckResponse` per **AC-14** (Retrieval URLs absolute, JSON-page form by default).
- **Any error (any endpoint):** body MUST conform to `ErrorEnvelope` per **AC-30** (`{Status, Code, Message, RequestId, HttpStatus}` — no extra top-level keys).
- **NDJSON streaming (#5–#10 with `Accept: application/x-ndjson`):** frames MUST follow `Header → Log*|ErrorLog* → Progress* → End` per **AC-67/AC-68/AC-69/AC-71/AC-72**; resume via `?after-seq=` + `?stream-id=`; per-frame size cap; progress cadence enforced.

## Test invariants (T-EP-01..T-EP-10)

| T-ID | Endpoint | Invariant | Assertion |
|---|---|---|---|
| T-EP-01 | #1 POST `/append-log` | Chunked NDJSON ingest returns `AckResponse` with absolute `Retrieval.PipelineLogs` URL | `assertMatchesSchema($body, 'AckResponse')` + `assertStartsWith('http', $body['Retrieval']['PipelineLogs'])` |
| T-EP-02 | #2 PUT `/fixed-log` | Clearing `Pipeline.HasError=1` → 0 returns `AckResponse` (per AC-13 sticky rule) | `assertSame(0, $db->query("SELECT HasError FROM Pipeline WHERE Id=?")->fetchValue($pid))` |
| T-EP-03 | #3 POST `/clear-log` | Empty `Retrieval` URLs are valid post-clear | `assertSame('', $body['Retrieval']['PipelineLogs'])` is FALSE — URL still present, page is empty |
| T-EP-04 | #4 POST `/clear-log-all` | Branch-wide clear; subsequent `/get-logs` returns empty `LogPage` | `assertCount(0, $getLogsResponse['Items'])` |
| T-EP-05 | #5 GET `/get-logs` (JSON) | Default Accept returns `LogPage` JSON with pagination cursors | `assertArrayHasKey('NextCursor', $body)` |
| T-EP-06 | #6 GET `/get-logs?q=…` | URL-style query collapses to same handler as #5 | `assertSame($responseFromHash5, $responseFromHash6)` |
| T-EP-07 | #7 GET `/get-pipeline-logs` (NDJSON) | `Accept: application/x-ndjson` triggers `Header→Log*→End` framing | `assertNdjsonFrameOrder(['Header', 'Log', 'Log', 'End'], $framedBody)` |
| T-EP-08 | #9 GET `/get-error-logs` | Server-side filter: only severity ≥ `Error` rows returned | `assertEvery($body['Items'], fn($r) => $r['Severity'] >= ErrorLevel::Error->value)` |
| T-EP-09 | #10 GET `/get-pipeline-error-logs` | NDJSON `Header.StateTransition` populated when scope=1 pipeline (per AC-74) | `assertArrayHasKey('StateTransition', $headerFrame)` |
| T-EP-10 | All | `ErrorEnvelope` shape exact (no extra keys) on any 4xx/5xx | `assertSame(['Status','Code','Message','RequestId','HttpStatus'], array_keys($errorBody))` |

Test files: `test/AcEndpointInventoryTest.php` (PHPUnit) + `test/ac-endpoint-inventory.bats` (bats CLI smoke). Each test method MUST embed its T-ID; absence triggers `GL-TEST-COVERAGE-GAP` per AC-80.

## Worked example (T-EP-07 — NDJSON pipeline retrieval)

```http
GET /wp-json/git-logs/v2/get-pipeline-logs?PipelineId=42 HTTP/1.1
Accept: application/x-ndjson
Authorization: Basic <app-password>
```

Response (frame-by-frame):

```ndjson
{"Frame":"Header","StreamId":"s_7f3a","PipelineId":42,"StateTransition":{"From":"Running","To":"Failed"}}
{"Frame":"Log","Seq":1,"Ts":"2026-05-10T12:00:00Z","Severity":2,"Message":"build started"}
{"Frame":"Log","Seq":2,"Ts":"2026-05-10T12:00:03Z","Severity":4,"Message":"compile error: …"}
{"Frame":"Progress","RowsEmitted":2,"BytesEmitted":238}
{"Frame":"End","Seq":2,"Truncated":false}
```

Resume after disconnect: `GET …?PipelineId=42&stream-id=s_7f3a&after-seq=1` MUST replay only `Seq>1`.

## Auditor classification rule (Lesson #34)

Any auditor finding citing **"missing per-endpoint contract"** OR **"endpoint inventory unbound to schemas"** against the 10 endpoints above MUST be classified as a **stale-cache walker-cap artifact**, NOT a spec defect. Verification command (auditor MUST run BEFORE flagging):

```bash
grep -nE "^\| (1|2|3|4|5|6|7|8|9|10) \|" spec/22-git-logs-v2/57-ac-section-d-endpoints-detail.md
```

Expected: 10 matched rows (one per endpoint). If absent, the file has been corrupted — escalate, do NOT auto-file as a spec gap.

## Cross-references

- **§97 §AC-11** — slim binding stub (this file is the full body)
- **§04 `04-rest-api-endpoints.md`** — per-endpoint prose contracts (handler-level detail)
- **§17 `17-openapi.yaml` v2.9.4+** — canonical JSON wire schemas (`AckResponse`, `ErrorEnvelope`, `AppendLogRequest`, `FixedLogRequest`, `LogPage`, `PipelineLogPage`, `ErrorLogPage`, `NdjsonErrorFrame`, `ErrorCode` enum)
- **§15 `15-error-codes.md`** — full `GL-*` error code catalog (30+ codes incl. `GL-NDJSON-*`, `GL-SHA-DB-*`)
- **AC-12** (§55) — streaming ingest contract for endpoint #1
- **AC-13** — `Pipeline.HasError` sticky rule (interaction with endpoint #2)
- **AC-14** — `AckResponse` Retrieval-URL contract (write endpoints #1–#4)
- **AC-30** — `ErrorEnvelope` shape + `RequestId` mirroring (all endpoints)
- **AC-67/AC-68/AC-69/AC-71/AC-72** — NDJSON framing contract (read endpoints #5–#10)
- **AC-74** — `Header.StateTransition` rule for single-pipeline scope (#7, #10)
- **AC-80** — sibling test-file delegation + `GL-TEST-COVERAGE-GAP` enforcement
