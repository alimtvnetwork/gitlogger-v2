# Acceptance Criteria — 04 Verification Patterns

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/03-error-manage/01-error-resolution/04-verification-patterns/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

Defines mandatory patterns for verifying frontend-backend synchronization, including standardized JSON envelopes, environment variable diagnostics, and WebSocket connectivity checks.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

### API Response Envelopes

**Success Envelope:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error Envelope:**
```json
{
  "success": false,
  "error": {
    "code": "string (e.g., ERR_NOT_FOUND)",
    "message": "string"
  }
}
```

### Environment Variables
- `VITE_API_URL`: The base URL for the backend API.

### Required HTTP Headers
- `Content-Type`: `application/json`
- `Access-Control-Allow-Origin`: Required for cross-origin frontend-backend communication.

### WebSocket Events
- `onopen`: Connection established.
- `onmessage`: Data received.
- `onerror`: Connection failure.
- `onclose`: Code and Reason provided.

---

## Acceptance Criteria

### AC-01: Standard Success Response Envelope Verification  `[critical]`
- **Given** An API endpoint at /api/v1/health
- **When** Performing Step 1: Backend Verification using curl.
- **Then** The response MUST utilize the standard envelope format {success: true, data: {...}} and return HTTP 200 with Content-Type: application/json.
- **Verifies:** 01-frontend-backend-sync.md

### AC-02: Standard Error Response Format  `[high]`
- **Given** An invalid resource request to /api/v1/resource/invalid
- **When** The backend encounters a missing or invalid resource.
- **Then** The response MUST return {success: false, error: {code: string, message: string}}.
- **Verifies:** 01-frontend-backend-sync.md

### AC-03: Frontend Response Handling Logic  `[high]`
- **Given** Frontend component BackendStatus.tsx or similar detection logic
- **When** Verifying Step 2: Frontend Verification via source inspection.
- **Then** The code MUST use HTTP 2xx status codes as the primary indicator and correctly parse the {success, data} envelope.
- **Verifies:** 01-frontend-backend-sync.md

### AC-04: Environment Variable Transparency  `[medium]`
- **Given** A frontend environment configuration using Vite
- **When** Debugging connection issues between frontend and backend.
- **Then** Diagnostic code MUST log both the raw value of import.meta.env.VITE_API_URL and the value returned by getResolvedApiUrl().
- **Verifies:** 01-frontend-backend-sync.md

### AC-05: WebSocket Connection Lifecycle Verification  `[high]`
- **Given** A WebSocket endpoint at /ws
- **When** Implementing Step 3: Integration Verification for real-time features.
- **Then** The connection test MUST verify that onopen fires, messages match the expected format, and onclose provides the numeric exit code and reason string.
- **Verifies:** 01-frontend-backend-sync.md

### AC-06: Endpoint Readiness Checklist Compliance  `[medium]`
- **Given** A new API endpoint implementation task
- **When** Moving from backend development to frontend integration.
- **Then** The developer MUST verify the route is in the router file, the handler is in the handlers file, and the endpoint is documented in openapi.yaml.
- **Verifies:** 01-frontend-backend-sync.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)