# Acceptance Criteria — 07 Logging And Diagnostics

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/03-error-manage/02-error-architecture/07-logging-and-diagnostics/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

Specifies the React frontend execution tracking and the backend session-based logging architecture. This includes component render tracing with parent-child relationships and 3-hop delegated request traceability for proxied API calls.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

// Execution Logger Structures (Frontend)
interface ExecutionLogEntry {
  type: 'render' | 'effect' | 'handler' | 'api';
  id: string;
  parentId?: string;
  name: string;
  data: any; // Props, Deps, Args
  timestamp: number;
}

// Session Logging (Backend)
enum LogRedactionKeys {
  AUTHORIZATION = "Authorization",
  COOKIE = "Cookie",
  SET_COOKIE = "Set-Cookie"
}

interface DelegatedRequestServer {
  endpoint: string;
  method: string;
  status: number;
  stacktrace: string;
  requestBody: string;
  responseBody: string;
  messages: string[];
}

interface ErrorEnvelope {
  Attributes: {
    SessionId: string;
  };
  executionChain: ExecutionLogEntry[];
}

// Limits
const MAX_LOG_ENTRIES = 100;
const MAX_BODY_SIZE = 51200; // 50KB

---

## Acceptance Criteria

### AC-01: Execution Log Retention Limit  `[high]`
- **Given** An active React execution environment with `useExecutionLogger` enabled
- **When** A component tree undergoes more than 100 state changes or render cycles.
- **Then** The Zustand store must maintain a queue of exactly the last 100 entries as per NF4, containing component renders, props, and effect dependencies.
- **Verifies:** 01-react-execution-logger.md/3.2 Non-Functional Requirements

### AC-02: Logger Performance Overhead  `[medium]`
- **Given** A React component using `useExecutionLogger`
- **When** The `logComp` or `logEffect` functions are invoked during a standard render cycle.
- **Then** The `CPU overhead per log` measured during a render or effect trigger must remain below 0.1ms.
- **Verifies:** 01-react-execution-logger.md/3.2 Non-Functional Requirements

### AC-03: Zero Overhead Production Mode  `[high]`
- **Given** A React application in a production environment with debug mode disabled (F8)
- **When** Diagnostic tools are queried for current memory usage.
- **Then** The memory overhead attributable to the `ExecutionLogEntry` array in the Zustand store must be 0MB.
- **Verifies:** 01-react-execution-logger.md/3.1 Functional Requirements

### AC-04: Error Capture Integration  `[critical]`
- **Given** A failed frontend operation that triggers `captureError()`
- **When** The global error handler intercepts an unhandled exception or explicit error report.
- **Then** The resulting error payload must include an `executionChain` property containing the full sequence of parent-child function relationships from the logger.
- **Verifies:** 01-react-execution-logger.md/4.1 Component Diagram

### AC-05: Interaction Traceability  `[high]`
- **Given** The React execution logger active during a user interaction
- **When** A user clicks a button or triggers a tracked event handler.
- **Then** The log must capture the handler name, the arguments passed to the handler, and the component context where it was invoked.
- **Verifies:** 01-react-execution-logger.md/3.1 Functional Requirements

### AC-06: Session ID Traceability  `[critical]`
- **Given** An incoming API request to the backend service
- **When** The Session Logging Middleware processes the request.
- **Then** The service must generate a unique session ID and populate the error envelope `Attributes.SessionId` with this exact value if an error occurs.
- **Verifies:** 02-session-based-logging.md/2.1 Functional Requirements

### AC-07: Sensitive Data Redaction  `[high]`
- **Given** An API request containing sensitive header keys (e.g., 'Authorization', 'Cookie')
- **When** The request metadata is persisted to the Session Store.
- **Then** The session store must contain redacted values (e.g., '[REDACTED]') for these specific keys instead of the raw tokens.
- **Verifies:** 02-session-based-logging.md/2.1 Functional Requirements

### AC-08: 3-Hop Delegated Traceability  `[high]`
- **Given** A Go backend request that proxies to WordPress PHP or a Chrome extension
- **When** The Request Handler executes a delegated request.
- **Then** The session log must contain a `DelegatedRequestServer` object including the external endpoint, method, status, and external stack trace.
- **Verifies:** 02-session-based-logging.md/3.1 Component Diagram

### AC-09: Maximum Body Capture Enforcement  `[medium]`
- **Given** An API request with a body larger than 50KB
- **When** The middleware captures the 'Request Body' for storage.
- **Then** The session store must truncate the captured body at exactly 50KB to maintain storage efficiency.
- **Verifies:** 02-session-based-logging.md/2.2 Non-Functional Requirements

### AC-10: Health Check Exclusion  `[low]`
- **Given** A system-level health check ping (e.g., `/healthz` or `/status`)
- **When** The request path matches the excluded endpoints.
- **Then** No entry should be created in the Request Session Store for this specific request.
- **Verifies:** 02-session-based-logging.md/2.1 Functional Requirements

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)