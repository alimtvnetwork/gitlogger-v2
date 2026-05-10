# Acceptance Criteria — 03 Error Modal Reference

**Version:** 2.1.0  
**Updated:** 2026-04-26  
**Scope:** `spec/03-error-manage/02-error-architecture/04-error-modal/03-error-modal-reference/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

This module defines the data model, capture pipeline, and UI structure for the Global Error Modal. It focuses on rendering complex 3-hop diagnostic data (React -> Go -> PHP) into a tabbed interface with automated session fetching and markdown report generation.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links. Three normative contract blocks (TypeScript / JSON Schema / React props) below are the source of truth for downstream implementations.

### Contract 1 — TypeScript: Capture & Envelope Types

```typescript
// src/components/errors/types.ts — NORMATIVE
export type ErrorLevel = 'error' | 'warn' | 'info';
export type SectionId = 'backend' | 'frontend' | 'delegated';

export const TABS_BACKEND = [
  'overview', 'log', 'execution', 'stack',
  'session', 'request', 'traversal',
] as const;
export type BackendTabId = typeof TABS_BACKEND[number];

export const TABS_FRONTEND = ['overview', 'stack', 'context', 'fixes'] as const;
export type FrontendTabId = typeof TABS_FRONTEND[number];

export interface MethodsStackFrame {
  Method: string;
  File: string;
  LineNumber: number;
}

export interface DelegatedRequestServer {
  DelegatedEndpoint: string;          // PHP URL
  Method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  StatusCode: number;                 // 100-599
  Response: unknown;
  StackTrace: string[];
  AdditionalMessages: string[];
}

export interface EnvelopeStatus {
  IsSuccess: boolean;
  Code: number;
  Message: string;
}

export interface EnvelopeAttributes {
  RequestedAt: string;                // ISO-8601 — Go entry timestamp
  RequestDelegatedAt: string;         // ISO-8601 — PHP delegation timestamp
  SessionId: string;
  HasAnyErrors: boolean;
}

export interface EnvelopeErrors {
  BackendMessage: string | null;
  DelegatedServiceErrorStack: string[]; // PHP stack lines
  Backend: string[];                    // Go error lines
  DelegatedRequestServer: DelegatedRequestServer | null;
}

export interface EnvelopeMethodsStack {
  Backend: MethodsStackFrame[];
}

export interface RawEnvelope {
  Status: EnvelopeStatus;
  Attributes: EnvelopeAttributes;
  Errors: EnvelopeErrors;
  MethodsStack: EnvelopeMethodsStack;
}

export interface CapturedError {
  id: string;                         // uuid v4
  code: string;                       // matches /^E1\d{3}$/
  level: ErrorLevel;
  message: string;
  sessionId: string;
  requestedAt: string;                // mirrors Attributes.RequestedAt
  requestDelegatedAt: string | null;  // null when no PHP hop
  envelope: RawEnvelope;
  capturedAt: string;                 // ISO-8601 — client-side capture
}

export interface ErrorQueueState {
  items: CapturedError[];
  activeIndex: number;                // 0-based; -1 when empty
}

// Badge variant helper — AC-05 source of truth
export const responseBadgeVariant = (status: number): 'destructive' | 'secondary' =>
  status >= 400 ? 'destructive' : 'secondary';
```

### Contract 2 — JSON Schema: CapturedError Wire Format

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://lovable.dev/spec/03-error-manage/captured-error.schema.json",
  "title": "CapturedError",
  "type": "object",
  "required": ["id", "code", "level", "message", "sessionId", "requestedAt", "envelope", "capturedAt"],
  "additionalProperties": false,
  "properties": {
    "id":                 { "type": "string", "format": "uuid" },
    "code":               { "type": "string", "pattern": "^E1[0-9]{3}$" },
    "level":              { "enum": ["error", "warn", "info"] },
    "message":            { "type": "string", "minLength": 1 },
    "sessionId":          { "type": "string", "minLength": 1 },
    "requestedAt":        { "type": "string", "format": "date-time" },
    "requestDelegatedAt": { "type": ["string", "null"], "format": "date-time" },
    "capturedAt":         { "type": "string", "format": "date-time" },
    "envelope": {
      "type": "object",
      "required": ["Status", "Attributes", "Errors", "MethodsStack"],
      "properties": {
        "Status": {
          "type": "object",
          "required": ["IsSuccess", "Code", "Message"],
          "properties": {
            "IsSuccess": { "type": "boolean" },
            "Code":      { "type": "integer", "minimum": 100, "maximum": 599 },
            "Message":   { "type": "string" }
          }
        },
        "Attributes": {
          "type": "object",
          "required": ["RequestedAt", "RequestDelegatedAt", "SessionId", "HasAnyErrors"],
          "properties": {
            "RequestedAt":        { "type": "string", "format": "date-time" },
            "RequestDelegatedAt": { "type": "string", "format": "date-time" },
            "SessionId":          { "type": "string" },
            "HasAnyErrors":       { "type": "boolean" }
          }
        },
        "Errors": {
          "type": "object",
          "required": ["BackendMessage", "DelegatedServiceErrorStack", "Backend", "DelegatedRequestServer"],
          "properties": {
            "BackendMessage":             { "type": ["string", "null"] },
            "DelegatedServiceErrorStack": { "type": "array", "items": { "type": "string" } },
            "Backend":                    { "type": "array", "items": { "type": "string" } },
            "DelegatedRequestServer": {
              "oneOf": [
                { "type": "null" },
                {
                  "type": "object",
                  "required": ["DelegatedEndpoint", "Method", "StatusCode", "Response", "StackTrace", "AdditionalMessages"],
                  "properties": {
                    "DelegatedEndpoint":  { "type": "string", "format": "uri" },
                    "Method":             { "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"] },
                    "StatusCode":         { "type": "integer", "minimum": 100, "maximum": 599 },
                    "Response":           {},
                    "StackTrace":         { "type": "array", "items": { "type": "string" } },
                    "AdditionalMessages": { "type": "array", "items": { "type": "string" } }
                  }
                }
              ]
            }
          }
        },
        "MethodsStack": {
          "type": "object",
          "required": ["Backend"],
          "properties": {
            "Backend": {
              "type": "array",
              "items": {
                "type": "object",
                "required": ["Method", "File", "LineNumber"],
                "properties": {
                  "Method":     { "type": "string" },
                  "File":       { "type": "string" },
                  "LineNumber": { "type": "integer", "minimum": 0 }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Contract 3 — React Component Props

```typescript
// src/components/errors/GlobalErrorModal.tsx — NORMATIVE
import type { CapturedError, ErrorQueueState, SectionId } from './types';

export interface GlobalErrorModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  queue: ErrorQueueState;
  activeSection: SectionId;
  onSectionChange: (next: SectionId) => void;
  onNavigateQueue: (delta: -1 | 1) => void;
  onCopyCompactReport: (err: CapturedError) => Promise<void>;
}

export interface BackendSectionProps {
  error: CapturedError;
  // Auto-fetch trigger — AC-03
  enableSessionDiagnostics?: boolean;
}

export interface UseSessionDiagnosticsResult {
  logsUrl: string;            // `/api/v1/sessions/${sessionId}/logs`
  diagnosticsUrl: string;     // `/api/v1/sessions/${sessionId}/diagnostics`
  loading: boolean;
  error: Error | null;
}

export type UseSessionDiagnostics =
  (sessionId: string) => UseSessionDiagnosticsResult;
```

---

## Acceptance Criteria

### AC-01: Conditional Delegated Logs Section Visibility  `[critical]`
- **Given** A `CapturedError` object populated after a failed API call where `envelopeErrors.DelegatedRequestServer` is present.
- **When** The `GlobalErrorModal` is opened.
- **Then** The modal must render the 'Delegated Logs' pill-style button in the Section Toggle with a green globe icon.
- **Verifies:** 04-modal-structure.md

### AC-02: Backend Message Banner Mapping  `[high]`
- **Given** A backend error response containing `envelopeErrors.BackendMessage`.
- **When** The user selects the 'Backend' section and 'Overview' tab.
- **Then** The 'Overview' tab in the Backend section must display a red-themed banner containing that specific message.
- **Verifies:** 05-backend-tabs.md

### AC-03: Session Diagnostics Auto-fetch Trigger  `[medium]`
- **Given** A captured error with a valid `sessionId` and an active `BackendSection`.
- **When** The backend section is rendered.
- **Then** The `useSessionDiagnostics` hook must trigger a fetch to `/api/v1/sessions/{id}/logs` and `/api/v1/sessions/{id}/diagnostics` and display the 'Session' tab.
- **Verifies:** 09-session-diagnostics.md

### AC-04: Go Call Chain Table Rendering  `[medium]`
- **Given** The modal is open with an error containing `envelopeMethodsStack.Backend` data.
- **When** The user navigates to Backend -> Execution.
- **Then** The 'Execution' tab must render a sortable table with columns: '#', 'Method', 'File', and 'Line'.
- **Verifies:** 03-envelope-parsing.md

### AC-05: 3-Hop Request Chain Visualization  `[high]`
- **Given** The 'Request' tab in the Backend section is active.
- **When** The error contains both `requestedAt` and `requestDelegatedAt`.
- **Then** A 3-node visualization must appear showing 'React -> Go', 'Go -> Delegated', and 'Delegated Response' with their respective HTTP status badges and URLs.
- **Verifies:** 07-request-chain.md

### AC-06: Compact Report Scrubbing Rules  `[medium]`
- **Given** The 'Compact Report' copy action is triggered.
- **When** The user clicks the primary 'Copy' split-button.
- **Then** The generated markdown must strip timestamps and base API URLs from the execution chain while retaining the relative paths.
- **Verifies:** 10-report-generation.md

### AC-07: Multi-Error Queue Navigation UI  `[medium]`
- **Given** An error in the queue is currently displayed in the modal.
- **When** `errorQueue.length` is greater than 1.
- **Then** The header must show a badge with the index (e.g., '1/3') and Chevron buttons that invoke `navigateQueue`.
- **Verifies:** 11-queue-navigation.md

### AC-08: PHP Error Stack Theming in Traversal  `[low]`
- **Given** The Traversal tab is active and `envelopeErrors.DelegatedServiceErrorStack` contains data.
- **When** Rendering Traversal details.
- **Then** The output must be rendered in an orange-themed `ScrollArea` labeled as PHP error lines.
- **Verifies:** 08-traversal-details.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)