---
kind: ac-detail
content_axis: normative-ac-detail-section-d-streaming-ingest
axis_rationale: "Detailed normative body for AC-12 (streaming ingestion) promoted out of 97-acceptance-criteria.md per Lesson #65 (structural surgery) + Lesson #36 (link-don't-restate). Slot 55 = sibling (01–96), not tier-1 — keeps §97 within walker cap."
---

# §97 AC — Section D Detail (AC-12 Streaming Ingestion)

**Version:** 1.0.0
**Updated:** 2026-05-10
**Slot type:** sibling (non-tier1) — bound from `97-acceptance-criteria.md` AC-12
**Promotion rationale:** AC-12's full normative body (single 5.7 KB block: Given/When/Then prose + 11-row T-INGEST-* testable scenario matrix) is promoted per **Lesson #65 — structural surgery > pure-promotion**; §97 retains a slim binding stub. Same pattern as `49-ac-section-a-detail.md`, `50-ac-delegation-maps-detail.md`, `52-ac-k-series-server-detail.md`, `53-ac-section-e-detail.md`, `54-ac-j-series-cli-detail.md`.

> **Status:** Normative tier-2 (sibling). The detail block below is the authoritative normative source for AC-12. Restating it in §97 or any other sibling is FORBIDDEN per **Lesson #19** (audit-boundary pin) and **Lesson #36** (link-don't-restate). The §97 entry MUST link here by anchor.

---

### AC-12 — Streaming ingestion (Lesson #19 + Lesson #36)  `[active]`

- **Given** a client sends a request to `/append-log` (endpoint #1 per §04) carrying `Transfer-Encoding: chunked` (no `Content-Length` header) — typically used by CI runners forwarding live `tail -f` output
- **When** the server begins parsing the request body
- **Then** the server MUST consume the body as a stream — reading and parsing one JSON value (or one NDJSON line, if §04 §11 ingestion-side streaming is later adopted) at a time — and MUST NOT buffer the entire body into memory before validation begins; AND the §10 size caps (`ConfigKv.MaxPushPayloadBytes` default 1 MiB, `MaxLinesPerPush` default 10 000, `MaxLineBytes` default 64 KiB) MUST be enforced INCREMENTALLY against running counters: as soon as any threshold is crossed mid-stream, the server MUST abort by returning `GL-PAYLOAD-TOO-LARGE` (HTTP 413) per §15 with a partial-ingest indicator in the error envelope's `Message` (e.g. `"aborted at line 8217 of …"`); AND chunks already accepted before the abort MUST be rolled back (the entire `/append-log` request is atomic per AC-13's sticky-`HasError` contract — a partial commit would corrupt the per-SHA cursor); AND the server MUST set a hard wall-clock cap of `ConfigKv.AppendLogMaxStreamSec` (recommended default 30 s) to prevent slow-loris ingest exhausting the PHP-FPM worker pool — exceeding the cap MUST return `GL-INGEST-TIMEOUT` per §15; AND when the request omits `Transfer-Encoding: chunked` and instead sends `Content-Length: N`, the server MAY (but is not required to) enable streaming — buffered ingest is acceptable for known-bounded payloads under the size caps.
- **AND (Phase E2 — testable scenario matrix per Lesson #19 audit-boundary pin):** the 11-row scenario matrix below is the **normative tier-1 testable surface** for AC-12. Every row maps to a discrete PHPUnit/bats test case implementers can author 1:1. Test fixture skeletons SHOULD live under `34-phpunit-test-skeleton.md` per AC-80 sibling delegation; restating the matrix in any other spec/22 file is FORBIDDEN per Lesson #36.

  | T-ID | Scenario | Input | Expected outcome | Verifies clause |
  |---|---|---|---|---|
  | T-INGEST-01 | Chunked happy path under all caps | `Transfer-Encoding: chunked`, 100 lines × 1 KiB each, total 100 KiB, wall-clock 2 s | HTTP 200, `AckResponse.WrittenCount=100`, all rows committed atomically | streaming consume + AC-14 ack |
  | T-INGEST-02 | Buffered (Content-Length) happy path | `Content-Length: 50000`, 50 lines × 1 KiB, no chunked header | HTTP 200, `WrittenCount=50` (server MAY buffer; both paths legal) | "buffered ingest is acceptable for known-bounded payloads" |
  | T-INGEST-03 | Mid-stream `MaxLineBytes` (64 KiB) breach | chunked stream, line 17 = 70 KiB | HTTP 413 `GL-PAYLOAD-TOO-LARGE`, `Message` contains `"aborted at line 17"`, lines 1..16 ROLLED BACK (DB row count unchanged from pre-request) | INCREMENTAL line-byte enforcement + atomic rollback |
  | T-INGEST-04 | Mid-stream `MaxLinesPerPush` (10 000) breach | chunked stream, 10 001 lines × 100 B each | HTTP 413 `GL-PAYLOAD-TOO-LARGE`, `Message` contains `"aborted at line 10001"`, full rollback | INCREMENTAL line-count enforcement |
  | T-INGEST-05 | Mid-stream `MaxPushPayloadBytes` (1 MiB) breach | chunked stream, cumulative bytes cross 1 MiB at line 1043 | HTTP 413 `GL-PAYLOAD-TOO-LARGE`, `Message` contains `"aborted at line 1043"`, full rollback | INCREMENTAL byte-total enforcement |
  | T-INGEST-06 | Slow-loris timeout | chunked stream, sender pauses 31 s mid-stream (>`AppendLogMaxStreamSec=30`) | HTTP 408 (or per-§15 status) `GL-INGEST-TIMEOUT`, full rollback, FPM worker released within 1 s of abort | wall-clock cap + worker-pool protection |
  | T-INGEST-07 | Memory bound under streaming | chunked stream, 9 999 lines × 50 KiB ≈ 500 MiB total raw bytes | EITHER full success (if under all caps) OR a cap breach per T-INGEST-03/04/05; peak PHP heap MUST stay <64 MiB (proves NO whole-body buffering — see §10) | "MUST NOT buffer the entire body into memory" |
  | T-INGEST-08 | Atomic rollback on validation failure | chunked stream, line 200 fails JSON-schema validation per §04 | HTTP 422, `Code=GL-VALIDATION-FAILED`, lines 1..199 ROLLED BACK | atomicity binding to AC-13 sticky-HasError |
  | T-INGEST-09 | Logger gating during ingest | chunked stream firing 1000 `Logger::debug()` calls with `LogLevelMin=Info` | NO debug lines reach any sink, ingest latency unchanged ±5% vs T-INGEST-01 baseline | AC-04 constant-time gate applies inside ingest path |
  | T-INGEST-10 | Clock-injection determinism | T-INGEST-06 replayed under `ClockInterface::advance(31s)` (per AC-29 §5 clock-injection subsection) | same `GL-INGEST-TIMEOUT` outcome WITHOUT a real 31 s wait; test suite wall-time <500 ms | AC-29 §5 binding |
  | T-INGEST-11 | Cross-request idempotency boundary | two concurrent `/append-log` for SAME `{PipelineId, Sha}` | both succeed if non-overlapping seq ranges; one returns `GL-CURSOR-CONFLICT` if overlapping; NEVER a half-commit from one losing | per-SHA cursor isolation + atomicity |

- **Verifies:** brief §Endpoints.2.b (chunked ingest), §04 (endpoint #1 contract), §10 (size cap matrix), §15 (`GL-PAYLOAD-TOO-LARGE`, `GL-INGEST-TIMEOUT`, `GL-VALIDATION-FAILED`, `GL-CURSOR-CONFLICT`), AC-13 (atomicity coupling), AC-29 §5 (clock injection — deterministic timeout testing). For the test matrix: closes the **Lesson #19 audit-boundary < verification-boundary gap** for streaming-ingest semantics. Mirror of AC-05's T-DEDUP-* matrix (Phase E1) on the second testable-scenario axis (ingest path); two Phase E-series tier-1 promotions on the testable-scenario axis.
