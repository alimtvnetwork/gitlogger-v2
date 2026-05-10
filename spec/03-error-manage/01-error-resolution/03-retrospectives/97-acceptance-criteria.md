# Acceptance Criteria — 03 Retrospectives

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/03-error-manage/01-error-resolution/03-retrospectives/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

Documents retrospectives and technical fixes for critical system failures including health check mismatches, race conditions in ZIP finalization, and redundant API retries.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

// Error Codes
E9005: Backend connection failure

// Standard API Envelope
type StandardResponse struct {
    Success bool        `json:"success"`
    Data    interface{} `json:"data"`
    Error   string      `json:"error,omitempty"`
}

// Health Response (Nested in Data)
type HealthData struct {
    Status    string `json:"status"` // Expected: "ok"
    Timestamp string `json:"timestamp"`
}

// WP Uploader PHP Registered Slugs (Riseup Asia)
// /status
// /upload (Accepts: activate: true)
// /plugins
// /export-self

// Backend Configuration (App.tsx)
// staleTime: 300000 (5 mins)
// retry: false
// refetchOnWindowFocus: false

// Publish Cooldown
// COOLDOWN_MS: 30000 (30 seconds)

---

## Acceptance Criteria

### AC-01: Standardized Health Response Format  `[critical]`
- **Given** Backend `Health` handler in `backend/internal/api/handlers/handlers.go`
- **When** A GET request is made to `/api/v1/health`
- **Then** The response MUST follow the standard envelope pattern: `{"success":true,"data":{"status":"ok","timestamp":"..."}}` with HTTP status 200.
- **Verifies:** 01-health-endpoint-mismatch.md

### AC-02: Resilient Connection Detection Logic  `[high]`
- **Given** The frontend `BackendStatus.tsx` component
- **When** Evaluating backend availability from the frontend UI
- **Then** Connectivity MUST be determined strictly by `response.ok` (any 2xx status) rather than matching specific string values like 'healthy' or 'ok' in the payload.
- **Verifies:** 01-health-endpoint-mismatch.md

### AC-03: Disable Automatic Retry Storms  `[high]`
- **Given** The `queryClient` configuration in `src/App.tsx`
- **When** An API query fails or the browser window regains focus
- **Then** The global settings MUST include `retry: false` and `refetchOnWindowFocus: false` to prevent redundant network requests and duplicate error notifications.
- **Verifies:** 02-retry-debounce-dedup-fixes.md

### AC-04: Publishing Request Deduplication  `[critical]`
- **Given** The `publishPlugin` function in `src/lib/api/methods.ts`
- **When** A user double-clicks the publish button or triggers overlapping publish actions
- **Then** Multiple concurrent calls for the same `pluginId:siteId` MUST be blocked using an internal `inFlight` Set, and a 30s cooldown MUST be enforced after success.
- **Verifies:** 02-retry-debounce-dedup-fixes.md

### AC-05: Synchronous ZIP Finalization  `[critical]`
- **Given** Go ZIP creation functions `createFullZip` or `createSelectiveZip`
- **When** Generating a plugin archive for immediate upload
- **Then** The `zip.Writer.Close()` and `os.File.Close()` MUST be called explicitly in that order before the function returns, without using `defer` for the critical finalization steps.
- **Verifies:** 03-zip-finalization-before-return.md

### AC-06: Preserve ZIP on Failure  `[medium]`
- **Given** The publishing cleanup logic in `backend/internal/services/publish/service.go`
- **When** A publishing operation fails for any reason
- **Then** The temporary ZIP file MUST NOT be deleted if `publishFailed` is true, ensuring it remains available for manual debugging.
- **Verifies:** 03-zip-finalization-before-return.md

### AC-07: Skip Redundant Plugin Activation  `[high]`
- **Given** The activation workflow in `backend/internal/wordpress/uploader.go`
- **When** The WP Uploader plugin has already handled activation during the upload phase
- **Then** If the `/upload` response indicates `activated: true`, the system MUST skip any subsequent calls to specific activation endpoints (e.g., `/enable`).
- **Verifies:** 04-activation-endpoint-mismatch.md

### AC-08: Enhanced Environment Diagnostics  `[low]`
- **Given** Diagnostics logic in `GlobalErrorModal.tsx` and `src/lib/diagnostics.ts`
- **When** Viewing the error modal after a connection failure
- **Then** The UI MUST display both the raw `VITE_API_URL` environment variable and the actual `Resolved API Origin` to troubleshoot configuration mismatches.
- **Verifies:** 01-health-endpoint-mismatch.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)