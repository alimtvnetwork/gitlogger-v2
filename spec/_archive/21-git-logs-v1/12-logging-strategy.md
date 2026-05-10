> ⚠️ **DEPRECATED — Legacy v1 Spec (folder 21)**  
> This document is preserved for historical reference only. **Do not implement against it.**  
> The active specification is **v2** in [`spec/22-git-logs-v2/`](../../22-git-logs-v2/00-overview.md) (SQLite, no JWT, SSH-key auth).  
> See [`spec/22-git-logs-v2/00-overview.md`](../../22-git-logs-v2/00-overview.md) for the current canonical source.  
> Deprecated: 2026-04-25

---

# Logging Strategy

**Version:** 1.2.0  
**Updated:** 2026-04-25  
**Status:** Active  
**AI Confidence:** High  
**Ambiguity:** Low

---

## Overview

This document defines the **structured logging contract** for the `git-logs` WordPress plugin. Every endpoint hit, every authentication attempt, every approval/policy decision, and every CI/CD log ingestion event MUST be recorded. **No error is ever swallowed.**

Two distinct log streams exist and MUST NOT be conflated:

| Stream | Purpose | Storage | Retention |
|--------|---------|---------|-----------|
| **CI/CD log stream** | User-submitted CI logs from GitHub | `LogEntry` table | Indefinite (v1) |
| **Internal diagnostic stream** | Plugin's own structured runtime logs | `AuditTrail` table + PHP `error_log` mirror | `AuditTrail` indefinite; `error_log` per WP host policy |

This document covers the **internal diagnostic stream**. CI/CD log ingestion is covered in `07-log-push-flow.md`.

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Audit trail schema | [./02-database-schema-and-erd.md](./02-database-schema-and-erd.md) §3.6 |
| Audit trail behavior | ./10-audit-trail.md (`10-audit-trail` — removed in v1 deprecation) *(planned)* |
| Error management | [./11-error-management.md](./11-error-management.md) *(planned)* |
| Foundational error mgmt | [../../03-error-manage/00-overview.md](../../03-error-manage/00-overview.md) |
| Glossary & enums | [./01-glossary-and-enums.md](./01-glossary-and-enums.md) |

---

## 1. Logging Principles (Hard Rules)

| # | Rule | Rationale |
|---|------|-----------|
| 1 | **No swallowed errors.** Every `catch` MUST either re-throw or log with full context (message, code, stack, request id). | User explicit requirement. |
| 2 | **Every endpoint call writes exactly one `AuditTrail` row** before returning, including 4xx and 5xx. | Single source of truth for "did the request happen". |
| 3 | **Every transaction writes exactly one `AuditTrail` row** with the matching `AuditActionType`. | Token issue, repo CRUD, log push, log query, auth success/fail. |
| 4 | **Logs are structured (JSON), not free text.** Free text only goes inside the `Message`/`Notes` field. | Greppable, parseable, ML-friendly. |
| 5 | **PII and secrets are redacted before logging.** Tokens, passwords, JWTs, refresh tokens, `Authorization` header values. | Security baseline. |
| 6 | **`TraceId` propagates across every log line of a single request.** | End-to-end debuggability. |
| 7 | **Log writes MUST NOT block the response on failure.** If `AuditTrail` insert fails, mirror the entry to PHP `error_log` and continue. | Availability > observability. |
| 8 | **All severity comparisons use the `LogSeverity.NumericLevel` numeric column,** never the `Name`. | Avoids string comparison bugs. |

---

## 2. Trace Context

Every request MUST carry a `TraceId`. The same value flows through HTTP headers, the response envelope (as `Attributes.SessionId`), every structured log line, and the terminal `AuditTrail` row.

### 2.1 Resolution order

1. Inbound `X-Request-Id` header (validated as UUIDv4 or `^[A-Za-z0-9._-]{8,128}$`).
2. Inbound `Traceparent` header (W3C Trace Context — extract `trace-id`).
3. Generated `wp_generate_uuid4()` if neither header is present (or the inbound value fails validation).

### 2.2 Propagation

- Echoed back as `X-Request-Id` response header.
- Surfaced as `Attributes.SessionId` in the response envelope (per `11-error-management.md` §3).
- Stored in `AuditTrail.DetailsJson.traceId`.
- Included in every internal `error_log` mirror line.
- Forwarded to GitHub callbacks (where applicable) as `X-Request-Id`.

### 2.3 Lifecycle Phases

A `TraceId` lives through **six phases**. Each phase has at least one structured log event in §4 and produces evidence on a different surface.

| # | Phase | Surface | Owner |
|---|-------|---------|-------|
| 1 | **Resolve** | `TraceMiddleware` reads/generates the value. | `TraceMiddleware` (outermost). |
| 2 | **Propagate (request-side)** | Set as the request-scoped context value. Every `logEvent()` call reads it. | `TraceMiddleware`. |
| 3 | **Annotate** | Each subsystem (`Auth`, `Approval`, `Ingestion`) emits structured log lines carrying the same `traceId`. | Per-subsystem services. |
| 4 | **Persist** | Final `AuditTrail` row writes `DetailsJson.traceId = <value>`. | `AuditMiddleware`. |
| 5 | **Surface (response-side)** | Echoed as `X-Request-Id` response header AND `Attributes.SessionId` envelope field. | `ErrorEnvelopeMapper` / response post-processor. |
| 6 | **Forward** | When the plugin calls back to GitHub, the same value is sent as `X-Request-Id` on the outbound request. | Outbound HTTP client. |

> **Invariant.** The `TraceId` value is set exactly once in phase 1 and is **immutable** for the rest of the request. Phase 1 is also the only phase allowed to fail; if it does, the request is rejected at the edge with a server-generated id and a `Warn` log line. See `11-error-management.md` rule R2.

### 2.4 Example HTTP Headers

#### 2.4.1 Inbound — caller supplies a valid `X-Request-Id`

```http
POST /wp-json/git-logs/v1/logs/push HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...   ; envelope JWT (HS256, per-repo LogSenderToken)
Content-Type: application/json
Content-Encoding: gzip
X-Request-Id: 5b3e0fd2-9b4a-4a18-b2b6-cb2c2c8cd571
Traceparent: 00-5b3e0fd29b4a4a18b2b6cb2c2c8cd571-00f067aa0ba902b7-01
User-Agent: github-actions-runner/2.317.0
Content-Length: 18432
```

The plugin accepts `5b3e0fd2-9b4a-4a18-b2b6-cb2c2c8cd571` (UUIDv4 ✓ and matches the `Traceparent` `trace-id`) and uses it as the `TraceId`.

#### 2.4.2 Inbound — caller omits the header

```http
POST /wp-json/git-logs/v1/logs/push HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
User-Agent: github-actions-runner/2.317.0
```

`TraceMiddleware` generates `wp_generate_uuid4()` → `f2c11b5e-4406-49c9-bff1-3a5a6d9b7044`.

#### 2.4.3 Inbound — caller supplies a malformed value

```http
X-Request-Id: <script>alert(1)</script>
```

The value fails the `^[A-Za-z0-9._-]{8,128}$` whitelist. `TraceMiddleware`:

1. Discards the inbound value.
2. Generates a fresh server-side UUIDv4.
3. Emits a `Warn` log line `TraceIdRejected_Malformed` with the rejected value (truncated to 64 chars) in `details.rejectedTraceId`.

#### 2.4.4 Outbound — success response

```http
HTTP/1.1 202 Accepted
Content-Type: application/json
X-Request-Id: 5b3e0fd2-9b4a-4a18-b2b6-cb2c2c8cd571
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 47
X-RateLimit-Reset: 1714032720
```

```json
{
  "Status": { "IsSuccess": true, "IsFailed": false, "Code": 202, "Message": "OK", "Timestamp": "2026-04-25T08:11:42.117Z" },
  "Attributes": {
    "RequestedAt": "https://example.com/wp-json/git-logs/v1/logs/push",
    "SessionId": "5b3e0fd2-9b4a-4a18-b2b6-cb2c2c8cd571",
    "HasAnyErrors": false, "IsSingle": false, "IsMultiple": true, "IsEmpty": false,
    "TotalRecords": 12, "PerPage": 0, "TotalPages": 0, "CurrentPage": 0
  },
  "Results": [{ "PersistedCount": 12, "PipelineId": 88 }]
}
```

The `X-Request-Id` response header value is **byte-identical** to `Attributes.SessionId`.

#### 2.4.5 Outbound — error response (envelope rejected by allowlist)

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json
X-Request-Id: 5b3e0fd2-9b4a-4a18-b2b6-cb2c2c8cd571
```

```json
{
  "Status": { "IsSuccess": false, "IsFailed": true, "Code": 403, "Message": "[GL-PUSH-001] Repository is not in the allowlist.", "Timestamp": "2026-04-25T08:11:42.220Z" },
  "Attributes": { "SessionId": "5b3e0fd2-9b4a-4a18-b2b6-cb2c2c8cd571", "RequestedAt": "https://example.com/wp-json/git-logs/v1/logs/push", "HasAnyErrors": true, "IsEmpty": true, "TotalRecords": 0 },
  "Results": [],
  "Errors": { "BackendMessage": "[GL-PUSH-001] Repository is not in the allowlist.", "ValidationErrors": [] }
}
```

### 2.5 End-to-End Timeline — JWT validation → CI/CD log ingestion

A worked example for `POST /wp-json/git-logs/v1/logs/push`. The same `traceId = 5b3e0fd2-9b4a-4a18-b2b6-cb2c2c8cd571` appears on every line. Times are relative to `t0`.

```
t0    + 0.00 ms  ── HTTP request hits PHP-FPM
                   ┌─────────────────────────────────────────────────────────────────────┐
                   │ 1. TraceMiddleware                                                  │
                   │    - Reads X-Request-Id header → validates → adopts.                │
                   │    - Sets request-scoped context: traceId=5b3e0fd2-…                │
                   └─────────────────────────────────────────────────────────────────────┘

t0    + 0.40 ms  LOG  EndpointReceived           [Info]   traceId=5b3e0fd2-…
                                                          httpMethod=POST endpointPath=/wp-json/git-logs/v1/logs/push
                                                          requestIp=140.82.121.4 userAgent="github-actions-runner/2.317.0"

t0    + 0.85 ms  LOG  EndpointResolved           [Debug]  traceId=5b3e0fd2-…  controller=LogPushController

                   ┌─────────────────────────────────────────────────────────────────────┐
                   │ 2. AuthMiddleware (envelope JWT path — HS256, per-repo)             │
                   └─────────────────────────────────────────────────────────────────────┘
t0    + 1.10 ms  LOG  JwtValidationStarted       [Debug]  traceId=5b3e0fd2-…  alg=HS256 kid=lst_42_…
t0    + 1.95 ms  LOG  EnvelopeJwtVerified        [Info]   traceId=5b3e0fd2-…  repositoryId=42
                                                          (HMAC ok · exp ok · ttl ok · jti not in nonce table)
                  AUDIT  (no row yet — terminal write happens at EndpointCompleted)

                   ┌─────────────────────────────────────────────────────────────────────┐
                   │ 3. ApprovalMiddleware — allowlist + RBAC + rate limit               │
                   └─────────────────────────────────────────────────────────────────────┘
t0    + 2.30 ms  LOG  AllowlistMatched_Exact     [Info]   traceId=5b3e0fd2-…  repositoryId=42
                                                          matchMode=Exact  acceptanceMode=RepoUrl
t0    + 2.55 ms  LOG  RoleCheckPassed            [Debug]  traceId=5b3e0fd2-…  role=LogSender(envelope)
t0    + 2.80 ms  LOG  RateLimitPassed            [Debug]  traceId=5b3e0fd2-…  bucket=repo:42  remaining=47/60

                   ┌─────────────────────────────────────────────────────────────────────┐
                   │ 4. ValidationMiddleware — body schema                               │
                   └─────────────────────────────────────────────────────────────────────┘
t0    + 3.40 ms  LOG  PayloadCapPassed           [Debug]  traceId=5b3e0fd2-…  rawBytes=18432  decompressedBytes=87104

                   ┌─────────────────────────────────────────────────────────────────────┐
                   │ 5. LogPushController → IngestionService                             │
                   └─────────────────────────────────────────────────────────────────────┘
t0    + 3.90 ms  LOG  IngestionStarted           [Debug]  traceId=5b3e0fd2-…  entryCount=12
t0    + 4.25 ms  LOG  PipelineAutoCreated        [Info]   traceId=5b3e0fd2-…  pipelineId=88 branch=main pipeline=ci-build
t0    + 9.60 ms  LOG  LogEntriesPersisted        [Info]   traceId=5b3e0fd2-…  pipelineId=88 persisted=12 failed=0

                   ┌─────────────────────────────────────────────────────────────────────┐
                   │ 6. ErrorEnvelopeMiddleware — wraps response                         │
                   └─────────────────────────────────────────────────────────────────────┘
t0    + 9.85 ms                                  Builds 202 envelope; SessionId = traceId.

                   ┌─────────────────────────────────────────────────────────────────────┐
                   │ 7. AuditMiddleware — single terminal AuditTrail row                 │
                   └─────────────────────────────────────────────────────────────────────┘
t0    +10.10 ms  AUDIT INSERT INTO AuditTrail  (one row)
                   AuditActionTypeName = 'LogPush'
                   AuditOutcomeName    = 'Success'
                   IsSuccessful        = 1
                   HttpMethod          = 'POST'
                   HttpStatus          = 202
                   EndpointPath        = '/wp-json/git-logs/v1/logs/push'
                   RequestIp           = '140.82.121.4'
                   DetailsJson         = { "traceId":"5b3e0fd2-…", "repositoryId":42,
                                           "pipelineId":88, "persisted":12, "latencyMs":10 }

                   ┌─────────────────────────────────────────────────────────────────────┐
                   │ 8. LoggingMiddleware (exit)                                         │
                   └─────────────────────────────────────────────────────────────────────┘
t0    +10.35 ms  LOG  EndpointCompleted          [Info]   traceId=5b3e0fd2-…
                                                          httpStatus=202  latencyMs=10
                                                          auditActionTypeName=LogPush  auditOutcomeName=Success

t0    +10.50 ms  ── HTTP response flushed
                   X-Request-Id: 5b3e0fd2-9b4a-4a18-b2b6-cb2c2c8cd571
                   Body: { "Attributes": { "SessionId": "5b3e0fd2-…" }, … }
```

#### 2.5.1 Failure variant — JWT signature invalid

If step 2 fails, the timeline diverges and the same `traceId` still appears everywhere:

```
t0    + 1.10 ms  LOG  JwtValidationStarted             [Debug]  traceId=5b3e0fd2-…
t0    + 1.85 ms  LOG  JwtValidationFailed_BadSignature [Warn]   traceId=5b3e0fd2-…
                                                                errorCode=GL-AUTH-008  (internal sub-code)
                                                                publicErrorCode=GL-AUTH-002
t0    + 2.00 ms                                        ErrorEnvelopeMapper builds 401 envelope with
                                                       BackendMessage="[GL-AUTH-002] Access JWT is invalid or expired."
t0    + 2.20 ms  AUDIT INSERT (Outcome=Rejected, errorCode=GL-AUTH-008 in DetailsJson)
t0    + 2.35 ms  LOG  EndpointCompleted                [Info]   traceId=5b3e0fd2-…  httpStatus=401  latencyMs=2
t0    + 2.50 ms  ── HTTP 401 flushed; X-Request-Id: 5b3e0fd2-…
```

> **Note:** the public `BackendMessage` carries `GL-AUTH-002` (generic), while the audit row and log lines carry the precise sub-code `GL-AUTH-008` — preventing the response from acting as an oracle while preserving full diagnostics. See `11-error-management.md` §6.1.

#### 2.5.2 Operational query — reconstruct the timeline

```sql
-- Single-trace timeline (audit rows for one request)
SELECT CreatedAt, AuditActionTypeName, AuditOutcomeName, HttpStatus,
       JSON_EXTRACT(DetailsJson, '$.errorCode') AS errorCode
FROM   VwAuditTrailDetail
WHERE  JSON_EXTRACT(DetailsJson, '$.traceId') = '5b3e0fd2-9b4a-4a18-b2b6-cb2c2c8cd571'
ORDER  BY CreatedAt ASC;
```

For the structured log lines (mirrored to `error_log` when severity ≥ Warn), grep on `"traceId":"5b3e0fd2-…"`.

---

## 3. Log Event Schema (Structured)

Every internal log line is a JSON object with this shape:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `traceId` | string | yes | See §2 |
| `timestamp` | ISO 8601 with `µs` | yes | Server clock, UTC |
| `severityName` | string | yes | One of `LogSeverity.Name` |
| `severityNumeric` | int | yes | `LogSeverity.NumericLevel` |
| `eventCategory` | string | yes | `Endpoint` \| `Auth` \| `Approval` \| `Ingestion` \| `Background` \| `Security` |
| `eventName` | string | yes | PascalCase, e.g. `JwtValidationFailed`, `LogPushAccepted` |
| `actorUserId` | int \| null | yes | `User.UserId` if known |
| `actorWordPressUserId` | bigint \| null | yes | `wp_users.ID` if WP-bridge |
| `repositoryId` | int \| null | yes | When repo-scoped |
| `auditActionTypeName` | string | conditional | Required when transaction; matches `AuditActionType.Name` |
| `auditOutcomeName` | string | conditional | Required when transaction; matches `AuditOutcome.Name` |
| `httpMethod` | string | yes (endpoint) | Uppercase |
| `httpStatus` | int | yes (endpoint) | Final status returned |
| `endpointPath` | string | yes (endpoint) | Without query string |
| `requestIp` | string | yes | After proxy resolution (see §6) |
| `userAgent` | string | yes | Truncated to 512 |
| `latencyMs` | int | yes (endpoint) | Wall-clock between request start and response flush |
| `errorCode` | string | conditional | Required on failure; from error registry |
| `errorMessage` | string | conditional | Human-readable, redacted |
| `errorStack` | string | conditional | Required when `severityNumeric >= 50` |
| `details` | object | optional | Free-form, must be redacted |

This object is what gets stored in `AuditTrail.DetailsJson` and what gets serialized to `error_log` (single line, JSON).

---

## 4. Required Log Events (Catalog)

Every event below MUST emit exactly one structured log line and one `AuditTrail` row.

### 4.1 Endpoint Lifecycle (every REST call)

| Event | When | Severity | `AuditActionType` |
|-------|------|----------|-------------------|
| `EndpointReceived` | Before any auth check | `Info` | — (entry log only) |
| `EndpointResolved` | After routing | `Debug` | — |
| `EndpointCompleted` | After response is built | `Info` | matches transaction type if any |

> Implementation note: `EndpointReceived` and `EndpointCompleted` MUST share the same `traceId`. `EndpointCompleted` is the row that gets the final `HttpStatus`, `LatencyMs`, and outcome.

### 4.2 Authentication & JWT Validation

| Event | Severity | `AuditActionType` | `AuditOutcome` |
|-------|----------|-------------------|----------------|
| `JwtValidationStarted` | `Debug` | — | — |
| `JwtValidationSucceeded` | `Info` | `AuthSuccess` | `Success` |
| `JwtValidationFailed_BadSignature` | `Warn` | `AuthFail` | `Rejected` |
| `JwtValidationFailed_Expired` | `Info` | `AuthFail` | `Rejected` |
| `JwtValidationFailed_BadIssuer` | `Warn` | `AuthFail` | `Rejected` |
| `JwtValidationFailed_BadAudience` | `Warn` | `AuthFail` | `Rejected` |
| `JwtValidationFailed_RevokedJti` | `Warn` | `AuthFail` | `Rejected` |
| `RefreshTokenRotated` | `Info` | `TokenIssue` | `Success` |
| `RefreshTokenReuseDetected` | `Error` | `AuthFail` | `Rejected` |
| `WpBridgeAuthSucceeded` | `Info` | `AuthSuccess` | `Success` |
| `WpBridgeAuthFailed` | `Warn` | `AuthFail` | `Rejected` |
| `TokenIssued` | `Info` | `TokenIssue` | `Success` |
| `TokenRevoked` | `Info` | `TokenRevoke` | `Success` |

> `RefreshTokenReuseDetected` MUST also revoke the entire token chain (set `IsRevoked = 1` on every descendant) and emit a separate `Security` event.

### 4.3 Approval & Policy Decisions

Every authorization or policy decision (allowlist match, role check, rate-limit check) MUST log its decision — both pass and fail.

| Event | Severity | `AuditActionType` | `AuditOutcome` |
|-------|----------|-------------------|----------------|
| `AllowlistMatched_Exact` | `Info` | `LogPush` | `Success` (continues) |
| `AllowlistMatched_VersionWildcard` | `Info` | `LogPush` | `Success` (continues) |
| `AllowlistMatched_OwnerWildcard` | `Info` | `LogPush` | `Success` (continues) |
| `AllowlistRejected_NotRegistered` | `Warn` | `LogPush` | `Rejected` |
| `AllowlistRejected_Disabled` | `Warn` | `LogPush` | `Rejected` |
| `RoleCheckPassed` | `Debug` | — | — |
| `RoleCheckFailed` | `Warn` | varies | `Rejected` |
| `RateLimitPassed` | `Debug` | — | — |
| `RateLimitExceeded` | `Warn` | `LogPush` or `LogQuery` | `Rejected` |
| `EnvelopeJwtVerified` | `Info` | `LogPush` | `Success` (continues) |
| `EnvelopeJwtRejected_BadHmac` | `Warn` | `LogPush` | `Rejected` |
| `EnvelopeJwtRejected_Expired` | `Info` | `LogPush` | `Rejected` |
| `PayloadCapExceeded` | `Warn` | `LogPush` | `Rejected` |

> Each "continues" event is informational; the transaction's terminal outcome is logged separately at `EndpointCompleted` time so each `AuditTrail` row maps to one final state.

### 4.4 CI/CD Log Ingestion (`POST /logs/push`)

| Event | Severity | `AuditActionType` | `AuditOutcome` |
|-------|----------|-------------------|----------------|
| `IngestionStarted` | `Debug` | — | — |
| `PipelineAutoCreated` | `Info` | — | — |
| `LogEntriesPersisted` | `Info` | `LogPush` | `Success` |
| `IngestionPartial` | `Warn` | `LogPush` | `Rejected` |
| `IngestionFailed_DbError` | `Error` | `LogPush` | `Error` |
| `IngestionFailed_ValidationError` | `Warn` | `LogPush` | `Rejected` |

> `IngestionPartial` MUST list the rejected entries' indices in `details.rejectedIndices` and the reason per index.

### 4.5 Background & Maintenance

| Event | Severity | `AuditActionType` | `AuditOutcome` |
|-------|----------|-------------------|----------------|
| `RefreshTokenSweepStarted` | `Debug` | — | — |
| `RefreshTokenSweepCompleted` | `Info` | — | `Success` |
| `RefreshTokenSweepFailed` | `Error` | — | `Error` |
| `JwksKeyRotationStarted` | `Info` | — | — |
| `JwksKeyRotationCompleted` | `Info` | — | `Success` |

### 4.6 Security Events

| Event | Severity |
|-------|----------|
| `SuspectedReplayAttack` | `Error` |
| `SuspectedBruteForce` | `Warn` |
| `SuspectedAllowlistProbe` | `Warn` |
| `IntegrityCheckFailed` | `Fatal` |

---

## 5. Error Handling — No-Swallow Rules

### 5.1 PHP `try`/`catch` template

```php
try {
    $result = $this->doWork($input);
    $this->logger->logEvent('OperationSucceeded', LogSeverity::Info, [
        'auditActionTypeName' => 'RepoCreate',
        'auditOutcomeName'    => 'Success',
        'details'             => ['repoId' => $result->repoId],
    ]);
    return $result;
} catch (DomainException $e) {
    // Expected, recoverable — log at Warn, return error envelope, do not re-throw.
    $this->logger->logEvent('OperationRejected', LogSeverity::Warn, [
        'auditActionTypeName' => 'RepoCreate',
        'auditOutcomeName'    => 'Rejected',
        'errorCode'           => $e->getCode(),
        'errorMessage'        => $e->getMessage(),
    ]);
    throw $e; // re-throw so the controller maps to HTTP error envelope
} catch (\Throwable $e) {
    // Unexpected — log at Error with stack, then re-throw.
    $this->logger->logEvent('OperationFailed', LogSeverity::Error, [
        'auditActionTypeName' => 'RepoCreate',
        'auditOutcomeName'    => 'Error',
        'errorCode'           => 'INTERNAL_ERROR',
        'errorMessage'        => $e->getMessage(),
        'errorStack'          => $e->getTraceAsString(),
    ]);
    throw $e;
}
```

### 5.2 Forbidden patterns

- `catch (\Throwable $e) {}` — empty catch.
- `catch (\Throwable $e) { return null; }` — silent fallback.
- `@function_call(...)` — error suppression operator.
- `set_error_handler(function() { return true; })` — global swallow.
- Logging without `traceId`.
- Logging the raw `Authorization` header, raw token, raw JWT, raw refresh token, raw password, or raw `LogSenderToken`.

### 5.3 Mandatory finally

Every endpoint controller MUST wrap its body in `try`/`catch`/`finally` so the `EndpointCompleted` log line and the matching `AuditTrail` row are written **even on uncaught exceptions**.

---

## 6. Redaction & PII Rules

### 6.1 Always redacted

| Source | Replacement |
|--------|-------------|
| `Authorization` header | `Bearer <redacted:len=NN>` |
| Plugin token (raw) | `<redacted:token>` |
| Refresh token (raw) | `<redacted:refresh>` |
| `LogSenderToken` (raw) | `<redacted:senderToken>` |
| JWT (raw) | `<redacted:jwt:kid=KID>` (preserve `kid` only) |
| Password fields | `<redacted:password>` |
| Email (in `details`) | mask local part: `j***@example.com` |

### 6.2 IP resolution (audit-truthful)

Trust chain MUST be configurable. Default order, evaluated only when the immediate peer matches a configured trusted-proxy CIDR list:

1. `CF-Connecting-IP`
2. `True-Client-IP`
3. `X-Forwarded-For` (first public, left-most)
4. `REMOTE_ADDR` (always logged as `details.remoteAddr` regardless)

If the immediate peer is **not** in the trusted-proxy list, only `REMOTE_ADDR` is used and proxy headers are logged as `details.untrustedProxyHeaders` for audit.

---

## 7. Storage & Mirroring

### 7.1 Primary store — `AuditTrail`

Every event in §4 produces one row. The structured JSON object from §3 is stored in `AuditTrail.DetailsJson`. Endpoint columns (`HttpMethod`, `HttpStatus`, `EndpointPath`, `RequestIp`, `UserAgent`, `IsSuccessful`) are denormalized for fast filtering.

### 7.2 Mirror — PHP `error_log`

The same JSON line is mirrored to PHP `error_log` when:

- `severityNumeric >= 40` (`Warn`, `Error`, `Fatal`), OR
- the `AuditTrail` insert itself failed.

Mirror format (single line):

```
[git-logs] {jsonObject}
```

This guarantees that even if the database is unavailable, no error is lost.

### 7.3 Insert failure handling

If `AuditTrail` insert fails:

1. Emit `IntegrityCheckFailed` to `error_log` with the original event's JSON and the DB error.
2. Do NOT retry inline (would block the response).
3. Schedule a `wp-cron` retry job to re-attempt the write from a small in-memory ring buffer (best-effort).
4. Increment a `gitlogs_audit_write_failures` WP transient counter for monitoring.

---

## 8. Performance Constraints

| Constraint | Value |
|------------|-------|
| Max synchronous log overhead per request | ≤ 5 ms (P95) |
| Max `DetailsJson` size | 8 KB (truncate `details` to fit; never truncate required fields) |
| Bulk ingestion log batching | One `AuditTrail` row per `LogPush` request — NOT one per `LogEntry` |
| Background log flush | Disabled in v1 (synchronous writes only) |

---

## 9. Querying Logs (Operational)

Use the views defined in `02-database-schema-and-erd.md` §6:

- `VwAuditTrailDetail` — flattened audit trail with action/outcome names.

Common operational queries:

```sql
-- All failures in the last hour
SELECT * FROM VwAuditTrailDetail
WHERE IsSuccessful = 0
  AND CreatedAt >= NOW() - INTERVAL 1 HOUR
ORDER BY CreatedAt DESC;

-- Single-trace timeline
SELECT * FROM VwAuditTrailDetail
WHERE JSON_EXTRACT(DetailsJson, '$.traceId') = '<traceId>'
ORDER BY CreatedAt ASC;

-- Top rejection reasons (last 24h)
SELECT JSON_EXTRACT(DetailsJson, '$.errorCode') AS code, COUNT(*) AS n
FROM VwAuditTrailDetail
WHERE AuditOutcomeName = 'Rejected'
  AND CreatedAt >= NOW() - INTERVAL 24 HOUR
GROUP BY code
ORDER BY n DESC;
```

---

## 10. Acceptance Criteria

| # | Criterion |
|---|-----------|
| AC-LOG-01 | Every REST endpoint produces exactly one terminal `AuditTrail` row, including 4xx and 5xx. |
| AC-LOG-02 | Every JWT validation outcome (success and every failure mode in §4.2) emits a structured log with `traceId`. |
| AC-LOG-03 | Every allowlist decision logs the matched mode (`Exact` / `VersionWildcard` / `OwnerWildcard`) or the rejection reason. |
| AC-LOG-04 | Every CI/CD log push produces exactly one `LogPush` `AuditTrail` row, regardless of how many `LogEntry` rows it persisted. |
| AC-LOG-05 | No `catch` block in the codebase is empty or returns silently — verified by static lint rule. |
| AC-LOG-06 | `Authorization`, JWT, plugin token, refresh token, `LogSenderToken`, and password values never appear in any `AuditTrail.DetailsJson` or `error_log` line. |
| AC-LOG-07 | When the `AuditTrail` insert fails, the same JSON line appears in `error_log` and the request still completes with the correct HTTP status. |
| AC-LOG-08 | `traceId` is present on every internal log line and echoed in the `X-Request-Id` response header. |
| AC-LOG-09 | Refresh-token reuse triggers `RefreshTokenReuseDetected`, revokes the entire chain, and emits a `Security` event. |
| AC-LOG-10 | `RateLimitExceeded` logs the limit, the window, and the current count in `details`. |

---

## 11. Open Items (require resolution before implementation)

| # | Item | Notes |
|---|------|-------|
| OI-LOG-01 | Final error-code registry | Depends on `11-error-management.md` (not yet authored). |
| OI-LOG-02 | Trusted-proxy CIDR list source | WP option vs. constant in `wp-config.php`? |
| OI-LOG-03 | `wp-cron` retry job for failed audit inserts | Needs a small persistence mechanism; `wp_options` ring buffer is one candidate. |
| OI-LOG-04 | Whether `EndpointReceived` should also persist to `AuditTrail` or only to `error_log` at `Debug` | Cost/benefit — doubles row volume. |

---

## Continuation Marker (intentionally omitted per project preference)
