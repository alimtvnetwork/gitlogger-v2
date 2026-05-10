# Endpoint Examples (v2)

**Version:** 2.2.0  
**Updated:** 2026-04-25

Concrete request/response samples for all 10 endpoints under `/wp-json/git-logs/v2/`. All bodies are PascalCase JSON. Times are unix seconds. Replace `https://wp.example.com` with your site root.

---

## Lane B — Write (CI/CD, TempToken in body)

### 1. POST `/append-log`

```bash
curl -sS -X POST https://wp.example.com/wp-json/git-logs/v2/append-log \
  -H 'Content-Type: application/json' \
  --data @- <<'JSON'
{
  "TempToken": "tt_b8f3a1e9d4c7…",
  "Token": "tk_4f2c9a1b6e8d…",
  "RepoUrl": "https://github.com/acme/widget-v2",
  "Branch": "main",
  "AppSlug": "widget-ci",
  "Pipeline": "build-and-test",
  "HasError": false,
  "Logs": [
    { "Severity": "Info", "Message": "Build started", "OccurredAt": 1745568000 },
    { "Severity": "Info", "Message": "Tests: 142 passed", "OccurredAt": 1745568042 }
  ],
  "ErrorLogs": []
}
JSON
```

**200 OK**:
```json
{
  "Status": "Ack",
  "PipelineId": 8821,
  "AcceptedLogCount": 2,
  "AcceptedErrorCount": 0,
  "Retrieval": {
    "GetLogs": "/wp-json/git-logs/v2/get-pipeline-logs?PipelineId=8821",
    "GetErrors": "/wp-json/git-logs/v2/get-pipeline-error-logs?PipelineId=8821"
  }
}
```

Streaming variant: same body sent with `Transfer-Encoding: chunked`. Server consumes line-by-line; cap is `MaxPushPayloadBytes` total.

### 2. POST `/fixed-log`

Use after a previous `HasError=true` push to mark the pipeline clean.

```bash
curl -sS -X POST https://wp.example.com/wp-json/git-logs/v2/fixed-log \
  -H 'Content-Type: application/json' \
  -d '{
    "TempToken": "tt_…", "Token": "tk_…",
    "RepoUrl": "https://github.com/acme/widget-v2",
    "Branch": "main", "Pipeline": "build-and-test"
  }'
```

**200 OK**: `{ "Status": "Ack", "PipelineId": 8821, "HasError": false }`

### 3. POST `/clear-log`

Truncates `LogEntry` + `ErrorLogEntry` for one Pipeline. Audited.

```bash
curl -sS -X POST .../clear-log \
  -d '{"TempToken":"…","Token":"…","RepoUrl":"…","Branch":"main","Pipeline":"build-and-test"}'
```

### 4. POST `/clear-log-all`

Truncates every Pipeline under one RepoVersion. Audited as a single bulk action.

```bash
curl -sS -X POST .../clear-log-all \
  -d '{"TempToken":"…","Token":"…","RepoUrl":"https://github.com/acme/widget-v2","Branch":"main"}'
```

---

## Lane A — Read (WP App Password / cookie)

Authenticate with a WordPress Application Password:

```bash
curl -sS -u 'admin:xxxx xxxx xxxx xxxx xxxx xxxx' \
  'https://wp.example.com/wp-json/git-logs/v2/get-logs?RepoUrl=https://github.com/acme/widget-v2&Branch=main&Limit=50'
```

### 5. GET `/get-logs`

Query params: `RepoUrl`, `Branch`, `Limit` (default 100, max 1000), `Cursor` (opaque), `Severity` (optional filter).

**200 OK**:
```json
{
  "Items": [
    { "LogEntryId": 91201, "PipelineId": 8821, "Severity": "Info",
      "Message": "Build started", "OccurredAt": 1745568000 }
  ],
  "NextCursor": "eyJJZCI6OTEyMDF9",
  "TotalReturned": 1
}
```

### 6. GET `/get-logs?q=…`

URL-style shorthand: `?q=<RepoUrl>@<Branch>` collapses the two params.

```
GET /wp-json/git-logs/v2/get-logs?q=https://github.com/acme/widget-v2@main&Limit=50
```

### 7. GET `/get-pipeline-logs`

Same shape as `/get-logs` but scoped to a single `PipelineId`.

```
GET /wp-json/git-logs/v2/get-pipeline-logs?PipelineId=8821
```

### 8. GET `/get-pipeline-logs?q=…`

Shorthand: `?q=<PipelineId>`.

### 9. GET `/get-error-logs`

Returns only `ErrorLogEntry` rows. Same params as `/get-logs`.

```json
{
  "Items": [
    { "ErrorLogEntryId": 4412, "PipelineId": 8830, "Severity": "Error",
      "Message": "Test failed: auth.spec.ts:42", "OccurredAt": 1745571200 }
  ],
  "NextCursor": null,
  "TotalReturned": 1
}
```

### 10. GET `/get-pipeline-error-logs`

Per-Pipeline error rows. Param: `PipelineId`.

---

## Common error envelope

Every reject (Lane A or B) returns:

```json
{
  "Status": "Error",
  "Code": "GL-AUTH-TEMPTOKEN-INVALID",
  "Message": "Token validation failed",
  "RequestId": "req_01HXY…",
  "HttpStatus": 401
}
```

See [`15-error-codes.md`](./15-error-codes.md) for the full code catalog.

---

## Headers always returned

| Header | Purpose |
|--------|---------|
| `X-GitLogs-Request-Id` | Echo for correlation with `AuditTrail.RequestId` |
| `X-GitLogs-Plugin-Version` | From `ConfigKv.PluginVersion` |
| `Retry-After` | Only on `429` / rate-limit reject |
