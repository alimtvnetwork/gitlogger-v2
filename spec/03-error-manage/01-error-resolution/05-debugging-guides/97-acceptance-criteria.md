# Acceptance Criteria — 05 Debugging Guides

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/03-error-manage/01-error-resolution/05-debugging-guides/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

Specifies debugging protocols, initialization sequences, and logging patterns for PHP (WordPress), Go (CLI/Backend), and TypeScript (React) environments. It defines mandatory error envelopes and diagnostic procedures for cross-stack troubleshooting.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

### PHP Constants
- `PLUGIN_DEBUG_LOGGING`: bool (Toggle debug.log)
- `PLUGIN_ERROR_LOGGING`: bool (Toggle error.log)

### PHP Helper Functions
- `ensure_directories_exist()`: Required before DB init.
- `ensure_database_ready()`: Requires directories to exist.

### PHP Log Paths
- `wp-content/uploads/{plugin-slug}/logs/debug.log`
- `wp-content/uploads/{plugin-slug}/logs/error.log`

### Go Error Envelope (JSON)
```go
type Response[T any] struct {
    Success bool       `json:"success"`
    Data    T          `json:"data,omitempty"`
    Error   *ErrorInfo `json:"error,omitempty"`
}

type ErrorInfo struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
    Details string `json:"details,omitempty"`
}
```

### TypeScript API Envelope
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: number;
    message: string;
    details?: string;
  };
}
```

### Logs Levels (Go)
- `Trace`, `Debug`, `Info`, `Warn`, `Error`, `Fatal`

### Health Check Endpoint
- Path: `/api/v1/health`
- Timeout: 5000ms


---

## Acceptance Criteria

### AC-01: Strict PHP Initialization Sequence Enforcement  `[critical]`
- **Given** A WordPress plugin environment requiring PHP debugging initialization to be checked
- **When** The plugin's activation sequence is triggered.
- **Then** The `ensure_directories_exist()` function must be called and succeed before `ensure_database_ready()` is executed per the STEP 1/STEP 2 protocol in 01-debugging-php.md.
- **Verifies:** 01-debugging-php.md#initialization-order-critical

### AC-02: Log Content and Location Verification  `[high]`
- **Given** The PHP constants `PLUGIN_DEBUG_LOGGING` and `PLUGIN_ERROR_LOGGING` are defined in `includes/constants.php`
- **When** A component-level exception or success event occurs during execution.
- **Then** Success/failure for component initialization must appear in `wp-content/uploads/{plugin-slug}/logs/debug.log` while stack traces for exceptions must appear in `error.log`.
- **Verifies:** 01-debugging-php.md#log-files-location

### AC-03: Go Service Initialization Order Compliance  `[critical]`
- **Given** A Go CLI service utilizing the standard main function structure from 02-debugging-go.md
- **When** The Go executable is launched.
- **Then** The application must load config (Step 1), ensure directories (Step 2), and connect to the DB (Step 3) before `api.NewServer` (Step 5) is invoked.
- **Verifies:** 02-debugging-go.md#initialization-order-critical

### AC-04: Go Structured Logging Format and Level Handling  `[medium]`
- **Given** The structured logging setup using `zerolog` in a Go backend
- **When** The `logger.Init(debug)` method is called during startup.
- **Then** If `debug` is true, logs must be output via `zerolog.ConsoleWriter` with `time.RFC3339`; otherwise, they must use JSON format with `zerolog.TimeFormatUnix`.
- **Verifies:** 02-debugging-go.md#structured-logging-with-zerolog

### AC-05: Go Standard Error Envelope Compliance  `[high]`
- **Given** A Go HTTP handler responding to a client request with an error
- **When** The `respondError` helper is executed.
- **Then** The response body must match the `Response[T]` envelope containing `Success: false`, a numeric `Code`, a `Message`, and an optional `Details` string.
- **Verifies:** 02-debugging-go.md#error-handling-pattern

### AC-06: TypeScript API Response Validation Priority  `[high]`
- **Given** A TypeScript/React application communicating with a backend API
- **When** An API call is received by the frontend client.
- **Then** The `fetchWithValidation` logic must prioritize `!response.ok` (HTTP status) as the primary indicator before checking the `body.success` field from the standard envelope.
- **Verifies:** 03-debugging-typescript.md#response-format-verification

### AC-07: Health Check Diagnostic Precision  `[medium]`
- **Given** The TypeScript `checkHealth` function implementation in a React frontend
- **When** A connection status detection event is triggered in the UI.
- **Then** The health check must target `{baseUrl}/api/v1/health`, utilize a 5000ms `AbortSignal.timeout`, and return the `latency` calculated as the difference between sample times.
- **Verifies:** 03-debugging-typescript.md#connection-status-detection

### AC-08: Environment Variable Diagnostic Transparency  `[low]`
- **Given** An error modal triggered by an environment variable mismatch in React
- **When** Users trigger the 'Show Diagnostics' collapsible in the ErrorModal.
- **Then** The diagnostics must display both `raw` values (e.g., `import.meta.env.VITE_API_BASE_URL`) and `resolved` values (e.g., from `getApiBaseUrl()`) to help isolate configuration issues.
- **Verifies:** 03-debugging-typescript.md#environment-variable-diagnostics

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)