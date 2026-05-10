# Acceptance Criteria — 05 Response Envelope

**Version:** 2.1.0  
**Updated:** 2026-04-26 (Phase 20 contract-inlining sweep: §97 "Inlined Contracts" replaced flat-prose summary with FOUR machine-parseable normative blocks — `text` human-readable summary, `ts` block (ResponseEnvelope<T> + EnvelopeStatus + EnvelopeAttributes + EnvelopeNavigation + DelegatedRequestServer + EnvelopeErrors + MethodsStackEntry + RESPONSE_DEBUG_CONFIG_KEYS const), `go` block (Envelope + Status + Attributes + Navigation + Errors + DelegatedRequestServer + MethodsStackEntry structs with explicit json tags + omitempty), and `json` JSON-Schema 2020-12 wire-format validator. Auditor contract count for this module 1/3 → 2/3 (now ts + json; sql N/A). Module weighted overall projected 51 (F) → 70+ (C/B). The pre-existing AC-01..AC-06 GWT criteria are unchanged.)  
**Scope:** `spec/03-error-manage/02-error-architecture/05-response-envelope/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`; Phase 20 normative contracts hand-authored.

---

## Module Summary

Defines a universal API response envelope used across Go, PHP, and React. It standardizes PascalCase keys, mandates that results are always returned as arrays, and provides structured error/delegation metadata.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links. Three normative machine-parseable contract blocks (TypeScript, Go, JSON Schema) follow the human-readable summary.

### Human-readable summary

```text
KEY_CONVENTION:   PascalCase (mandated; AC-01)
RESULTS_RULE:     Always an array, even for single-item responses (AC-02)
CONFIG_KEYS:
  pagination.defaultPerPage
  responseDebug.includeErrors
  responseDebug.includeStackTrace
  responseDebug.includeDelegatedServerInfo
  responseDebug.includeMethodsStack
TOP_LEVEL_FIELDS:
  Status        Object   Required
  Attributes    Object   Required
  Results       Array    Required (always array; never bare object)
  Navigation    Object   Optional (pointer; omitempty)
  Errors        Object   Optional (pointer; omitempty)
  MethodsStack  Object   Optional (pointer; omitempty)
STATUS_OBJECT:
  IsSuccess  bool
  IsFailed   bool
  Code       int      (HTTP status)
  Message    string
  Timestamp  string   (ISO-8601)
DELEGATED_REQUEST_SERVER:
  DelegatedEndpoint    string
  Method               string
  StatusCode           int
  RequestBody          object | null
  Response             object | null
  StackTrace           string[]
  AdditionalMessages   string
```

### Normative TypeScript contract (frontend + cross-language source of truth)

```ts
// Authoritative type-level contract for the Universal Response Envelope.
// Consumed by: React frontend (src/api/types/envelope.ts), Go backend (pkg/response),
// PHP WordPress companion plugin (src/Response/Envelope.php). All three implementations
// MUST conform to this shape — diverging keys/casings constitute a contract violation
// caught by `linter-scripts/audit-spec-vs-code-v2.py` and AC-01..AC-06 of this module.

/** ISO-8601 timestamp string, e.g. "2026-04-26T12:34:56.789Z". */
export type Iso8601 = string;

/** Status block — always present at top level. */
export interface EnvelopeStatus {
  readonly IsSuccess: boolean;
  readonly IsFailed: boolean;
  readonly Code: number;        // HTTP status, e.g. 200, 404, 500
  readonly Message: string;
  readonly Timestamp: Iso8601;
}

/** Attributes block — always present; describes shape of Results array. */
export interface EnvelopeAttributes {
  readonly IsSingle: boolean;       // Results.length === 1 AND request was for one resource
  readonly IsMultiple: boolean;     // Results.length > 1 OR pagination active
  readonly IsEmpty: boolean;        // Results.length === 0
  readonly HasAnyErrors: boolean;   // Errors block present and non-empty
  readonly TotalRecords: number;
  readonly TotalPages: number;
}

/** Pagination/navigation block — optional; omitted when TotalPages <= 1. */
export interface EnvelopeNavigation {
  readonly CurrentPage: number;
  readonly TotalPages: number;
  readonly PerPage: number;
  readonly NextPage: string | null;     // absolute URL, e.g. "http://host/api/v1/x?page=2"
  readonly PrevPage: string | null;     // absolute URL or null on first page
  readonly FirstPage: string;
  readonly LastPage: string;
}

/** Delegated-server diagnostics — populated when Go backend proxies to PHP/WP. */
export interface DelegatedRequestServer {
  readonly DelegatedEndpoint: string;
  readonly Method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE" | "HEAD" | "OPTIONS";
  readonly StatusCode: number;
  readonly RequestBody: Record<string, unknown> | null;
  readonly Response: Record<string, unknown> | null;
  readonly StackTrace: readonly string[];
  readonly AdditionalMessages: string;
}

/** Errors block — optional; omitted entirely when responseDebug.includeErrors=false (AC-03). */
export interface EnvelopeErrors {
  readonly Code?: string;                                    // app-specific error code
  readonly Type?: string;                                    // category, e.g. "validation", "delegation"
  readonly Details?: readonly Record<string, unknown>[];
  readonly StackTrace?: readonly string[];                   // included only when responseDebug.includeStackTrace=true
  readonly DelegatedRequestServer?: DelegatedRequestServer;  // populated per AC-04
}

/** Methods-stack diagnostics — optional; included only when responseDebug.includeMethodsStack=true. */
export interface MethodsStackEntry {
  readonly Method: string;
  readonly DurationMs: number;
  readonly StartedAt: Iso8601;
}

/** The universal envelope. Generic over the row type T contained in Results. */
export interface ResponseEnvelope<T = Record<string, unknown>> {
  readonly Status: EnvelopeStatus;
  readonly Attributes: EnvelopeAttributes;
  readonly Results: readonly T[];                              // ALWAYS array (AC-02), even for single-resource responses
  readonly Navigation?: EnvelopeNavigation;                    // omitempty
  readonly Errors?: EnvelopeErrors;                            // omitempty (AC-03)
  readonly MethodsStack?: readonly MethodsStackEntry[];        // omitempty
}

/** Configuration keys that gate optional envelope sections (read by backend at marshal time). */
export const RESPONSE_DEBUG_CONFIG_KEYS = [
  "pagination.defaultPerPage",
  "responseDebug.includeErrors",
  "responseDebug.includeStackTrace",
  "responseDebug.includeDelegatedServerInfo",
  "responseDebug.includeMethodsStack",
] as const;
export type ResponseDebugConfigKey = typeof RESPONSE_DEBUG_CONFIG_KEYS[number];
```

### Normative Go contract (backend marshalling source of truth)

```go
// Package response defines the Universal Response Envelope for all Go HTTP handlers.
// MUST mirror the TypeScript ResponseEnvelope<T> contract above and the JSON Schema below.
// Default JSON marshalling MUST produce PascalCase keys — DO NOT add `json:"camelCase"` tags
// (AC-01). All optional fields use pointer types so `omitempty` removes them entirely (AC-03).
package response

import "time"

// Envelope is the universal API response wrapper. Generic in spirit; in practice
// handlers populate Results as []any and let json.Marshal do the work.
type Envelope struct {
    Status       Status                  `json:"Status"`
    Attributes   Attributes              `json:"Attributes"`
    Results      []any                   `json:"Results"`                // ALWAYS array (AC-02)
    Navigation   *Navigation             `json:"Navigation,omitempty"`
    Errors       *Errors                 `json:"Errors,omitempty"`       // AC-03
    MethodsStack []MethodsStackEntry     `json:"MethodsStack,omitempty"`
}

type Status struct {
    IsSuccess bool      `json:"IsSuccess"`
    IsFailed  bool      `json:"IsFailed"`
    Code      int       `json:"Code"`        // HTTP status
    Message   string    `json:"Message"`
    Timestamp time.Time `json:"Timestamp"`   // marshals as RFC3339 (ISO-8601 compatible)
}

type Attributes struct {
    IsSingle     bool `json:"IsSingle"`
    IsMultiple   bool `json:"IsMultiple"`
    IsEmpty      bool `json:"IsEmpty"`
    HasAnyErrors bool `json:"HasAnyErrors"`
    TotalRecords int  `json:"TotalRecords"`
    TotalPages   int  `json:"TotalPages"`
}

type Navigation struct {
    CurrentPage int     `json:"CurrentPage"`
    TotalPages  int     `json:"TotalPages"`
    PerPage     int     `json:"PerPage"`
    NextPage    *string `json:"NextPage"`     // absolute URL or null (AC-05)
    PrevPage    *string `json:"PrevPage"`
    FirstPage   string  `json:"FirstPage"`
    LastPage    string  `json:"LastPage"`
}

type DelegatedRequestServer struct {
    DelegatedEndpoint  string         `json:"DelegatedEndpoint"`
    Method             string         `json:"Method"`
    StatusCode         int            `json:"StatusCode"`
    RequestBody        map[string]any `json:"RequestBody"`
    Response           map[string]any `json:"Response"`
    StackTrace         []string       `json:"StackTrace"`
    AdditionalMessages string         `json:"AdditionalMessages"`
}

type Errors struct {
    Code                   string                  `json:"Code,omitempty"`
    Type                   string                  `json:"Type,omitempty"`
    Details                []map[string]any        `json:"Details,omitempty"`
    StackTrace             []string                `json:"StackTrace,omitempty"`
    DelegatedRequestServer *DelegatedRequestServer `json:"DelegatedRequestServer,omitempty"` // AC-04
}

type MethodsStackEntry struct {
    Method     string    `json:"Method"`
    DurationMs int64     `json:"DurationMs"`
    StartedAt  time.Time `json:"StartedAt"`
}
```

### Normative JSON Schema (wire-format validator)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://lovable.spec/03-error-manage/05-response-envelope/envelope.schema.json",
  "title": "ResponseEnvelope",
  "description": "Universal API response envelope. All Go, PHP, and React implementations MUST produce JSON conforming to this schema. Verifies AC-01..AC-06.",
  "type": "object",
  "required": ["Status", "Attributes", "Results"],
  "additionalProperties": false,
  "properties": {
    "Status": {
      "type": "object",
      "required": ["IsSuccess", "IsFailed", "Code", "Message", "Timestamp"],
      "properties": {
        "IsSuccess": { "type": "boolean" },
        "IsFailed":  { "type": "boolean" },
        "Code":      { "type": "integer", "minimum": 100, "maximum": 599 },
        "Message":   { "type": "string" },
        "Timestamp": { "type": "string", "format": "date-time" }
      }
    },
    "Attributes": {
      "type": "object",
      "required": ["IsSingle", "IsMultiple", "IsEmpty", "HasAnyErrors", "TotalRecords", "TotalPages"],
      "properties": {
        "IsSingle":     { "type": "boolean" },
        "IsMultiple":   { "type": "boolean" },
        "IsEmpty":      { "type": "boolean" },
        "HasAnyErrors": { "type": "boolean" },
        "TotalRecords": { "type": "integer", "minimum": 0 },
        "TotalPages":   { "type": "integer", "minimum": 0 }
      }
    },
    "Results": {
      "type": "array",
      "description": "ALWAYS an array (AC-02), even when the response represents a single resource.",
      "items": { "type": "object" }
    },
    "Navigation": {
      "type": "object",
      "required": ["CurrentPage", "TotalPages", "PerPage", "NextPage", "PrevPage", "FirstPage", "LastPage"],
      "properties": {
        "CurrentPage": { "type": "integer", "minimum": 1 },
        "TotalPages":  { "type": "integer", "minimum": 1 },
        "PerPage":     { "type": "integer", "minimum": 1 },
        "NextPage":    { "type": ["string", "null"], "format": "uri", "description": "Absolute URL (AC-05) or null on last page." },
        "PrevPage":    { "type": ["string", "null"], "format": "uri" },
        "FirstPage":   { "type": "string", "format": "uri" },
        "LastPage":    { "type": "string", "format": "uri" }
      }
    },
    "Errors": {
      "type": "object",
      "description": "Omitted entirely when responseDebug.includeErrors=false (AC-03).",
      "properties": {
        "Code":       { "type": "string" },
        "Type":       { "type": "string" },
        "Details":    { "type": "array", "items": { "type": "object" } },
        "StackTrace": { "type": "array", "items": { "type": "string" } },
        "DelegatedRequestServer": {
          "type": "object",
          "required": ["DelegatedEndpoint", "Method", "StatusCode"],
          "properties": {
            "DelegatedEndpoint":  { "type": "string" },
            "Method":             { "enum": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"] },
            "StatusCode":         { "type": "integer", "minimum": 100, "maximum": 599 },
            "RequestBody":        { "type": ["object", "null"] },
            "Response":           { "type": ["object", "null"] },
            "StackTrace":         { "type": "array", "items": { "type": "string" } },
            "AdditionalMessages": { "type": "string" }
          }
        }
      }
    },
    "MethodsStack": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["Method", "DurationMs", "StartedAt"],
        "properties": {
          "Method":     { "type": "string" },
          "DurationMs": { "type": "integer", "minimum": 0 },
          "StartedAt":  { "type": "string", "format": "date-time" }
        }
      }
    }
  }
}
```

---


## Acceptance Criteria

### AC-01: Enforce PascalCase Key Convention  `[critical]`
- **Given** The PascalCase key convention is mandated by ADR 01-adr.md and the JSON schema referenced in 02-changelog.md
- **When** Any backend (Go or PHP) marshals a response envelope to JSON.
- **Then** The API must return JSON keys in PascalCase (e.g., 'IsSuccess', 'TotalRecords') and the Go implementation must utilize default marshaling without camelCase struct tags.
- **Verifies:** spec/03-error-manage/02-error-architecture/05-response-envelope/01-adr.md

### AC-02: Results Field Consistency as Array  `[high]`
- **Given** A request for a single resource (e.g., a specific user) is made.
- **When** The API processes a single-item response.
- **Then** The 'Results' field must still be returned as an array containing exactly one object ('Results': [ {...} ]) as per the ADR and reference docs.
- **Verifies:** spec/03-error-manage/02-error-architecture/05-response-envelope/04-response-envelope-reference.md

### AC-03: Conditional Errors Block Omission  `[medium]`
- **Given** The backend configuration has 'responseDebug.includeErrors' set to false.
- **When** A request fails but error reporting is disabled in config.json.
- **Then** The 'Errors' top-level key must be omitted entirely from the JSON response using Go's 'omitempty' pointer behavior.
- **Verifies:** spec/03-error-manage/02-error-architecture/05-response-envelope/03-configurability.md

### AC-04: Structured Delegated Error Capture  `[high]`
- **Given** The Go backend proxies a request to a WordPress/PHP companion plugin.
- **When** The delegated request returns an HTTP status code >= 400.
- **Then** The 'Errors.DelegatedRequestServer' object must contain 'DelegatedEndpoint', 'Method', 'StatusCode', 'RequestBody', and 'Response' from the downstream call.
- **Verifies:** spec/03-error-manage/02-error-architecture/05-response-envelope/03-configurability.md

### AC-05: Absolute URL Pagination Links  `[medium]`
- **Given** A list response contains enough items to span multiple pages (TotalPages > 1).
- **When** The 'Navigation' block is present in the response.
- **Then** The 'Navigation.NextPage' and 'Navigation.PrevPage' fields must contain fully qualified, absolute URL strings (e.g., 'http://localhost:8080/api/v1/plugins?page=2').
- **Verifies:** spec/03-error-manage/02-error-architecture/05-response-envelope/01-adr.md

### AC-06: Attribute Descriptor Correctness  `[low]`
- **Given** A response contains a successful single-item payload.
- **When** The response envelope is generated.
- **Then** In 'Attributes', 'IsSingle' must be true, 'IsMultiple' must be false, 'IsEmpty' must be false, and 'HasAnyErrors' must be false.
- **Verifies:** spec/03-error-manage/02-error-architecture/05-response-envelope/04-response-envelope-reference.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)