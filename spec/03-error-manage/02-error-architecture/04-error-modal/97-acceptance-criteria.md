# Acceptance Criteria — 04 Error Modal

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/03-error-manage/02-error-architecture/04-error-modal/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

This module specifies the architecture and implementation of the Global Error Modal, including its React component structure, Zustand state management, color-themed diagnostic tabs (React/Go/PHP), error history persistence (API sync), and standardized markdown/JSON export formats.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

// LogLevel Enum
enum LogLevel {
  Error = 'error',
  Warn = 'warn',
  Info = 'info'
}

// Error History Input
interface ErrorHistoryInput {
  error: CapturedError;
  context: Record<string, any>;
}

// React Query Meta Extension
interface QueryMeta {
  suppressGlobalError?: boolean;
}

// API Endpoints Referenced
// GET /api/v1/error-history (List)
// POST /api/v1/error-history (Save)
// DELETE /api/v1/error-history/:id (Delete)
// POST /api/v1/error-history/bulk (Export)
// GET /api/v1/logs/error (Raw Error Log)

// Error Codes
// E9005: Critical system error requiring immediate modal attention.

---

## Acceptance Criteria

### AC-01: Primary Error Icon Color Mapping  `[high]`
- **Given** The `GlobalErrorModal` React component is rendering an error with `selectedError.level` set to `LogLevel.Error`
- **When** The modal header is evaluated for visual compliance.
- **Then** The header icon must render the `AlertCircle` icon with the `text-destructive` Tailwind class as defined in `04-color-themes.md` section 2.
- **Verifies:** 04-color-themes.md

### AC-02: Global Error Suppression Pattern  `[critical]`
- **Given** Any React `useQuery` or `useMutation` that provides its own local error UI or toasts
- **When** A network error occurs during the execution of that query or mutation.
- **Then** The query/mutation configuration must include `meta: { suppressGlobalError: true }` to prevent double-notification in the `QueryCache` and `MutationCache` handlers.
- **Verifies:** 06-suppress-global-error.md

### AC-03: Delegated Server Color Tier Enforcement  `[medium]`
- **Given** A PHP or Delegated Server error frame being rendered in the `BackendSection` tabs
- **When** Rendering PHP stack frames or delegated service errors.
- **Then** The UI must use the 'orange' theme (e.g., `text-orange-500`, `bg-orange-500/5`) and NEVER use purple, as per the 'Two-Tier Color System' in `04-color-themes.md`.
- **Verifies:** 04-color-themes.md

### AC-04: Error History Persistence Flow  `[high]`
- **Given** The `useErrorHistory` hook is invoked to persist a captured error to the backend database
- **When** `saveMutation.mutate()` is called.
- **Then** It must perform a `POST /api/v1/error-history` request and invalidate the `['error-history']` query key upon success.
- **Verifies:** 05-error-history-persistence.md

### AC-05: Immediate Modal Trigger for E9005  `[critical]`
- **Given** The `GlobalErrorModal` renders an error response with HTTP status code E9005
- **When** An `ApiClientError` with code `E9005` is caught by the global handler.
- **Then** The `showGlobalError` function in `App.tsx` must trigger `openErrorModal()` immediately instead of just showing a toast with a "View Details" button.
- **Verifies:** 06-suppress-global-error.md

### AC-06: Default Compact Report Generation  `[medium]`
- **Given** The user clicks the 'Copy' button in the `GlobalErrorModal` for an instant report
- **When** The primary copy action is triggered.
- **Then** The system must generate the 'Compact Report' (Markdown) which includes delegated server info from `CapturedError` without making additional API calls.
- **Verifies:** 01-copy-formats/01-compact-report.md

### AC-07: Backend Tab Completeness  `[medium]`
- **Given** The `GlobalErrorModal` is active and the `BackendSection` is visible
- **When** The modal structure is inspected.
- **Then** The component must render exactly seven tabs: Overview, Log, Execution, Stack, Session, Request, and Traversal, as defined in the `02-react-components` hierarchy.
- **Verifies:** 02-react-components/00-overview.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)