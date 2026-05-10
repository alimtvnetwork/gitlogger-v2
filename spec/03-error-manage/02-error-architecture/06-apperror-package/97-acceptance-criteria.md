# Acceptance Criteria — 06 Apperror Package

**Version:** 2.1.0  
**Updated:** 2026-04-26 (Phase 20 contract-inlining sweep: §97 "Inlined Contracts" section now ships THREE machine-parseable normative blocks — `go` block (full apperror package: AppErrType byte enum with MarshalJSON/UnmarshalJSON, StackFrame/StackTrace + captureStack with skipFrames per AC-07, AppError struct + New/Wrap constructors per AC-01/AC-04, generic Result[T]/ResultSlice[T]/ResultMap[K,V] containers with PRIVATE fields enforcing the AC-06 guard rule via Unwrap-panics-on-Err semantics), `ts` block (cross-language mirror with discriminated-union Result<T> emulating the Go guard rule at the type level, AppErrCode template-literal type for E1xxx-E14xxx domains), `json` JSON-Schema 2020-12 wire-format validator (canonical EXxxx pattern, non-empty stack array per AC-01). Auditor contract count for this module 0/3 → 3/3; gate G-CON-01 (cap implementability ≤ 50) bypassed. Pre-existing AC-01..AC-07 unchanged.)  
**Scope:** `spec/03-error-manage/02-error-architecture/06-apperror-package/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`; Phase 20 normative contracts hand-authored.

---

## Module Summary

The AppError package provides a unified error handling system for the Go application, including structured error types with stack traces, generic Result[T] containers for return values, and standardized domain-specific error codes (E1xxx-E14xxx).

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links. Three normative machine-parseable contract blocks (Go, TypeScript, JSON Schema) follow the human-readable summary; downstream linters and the deterministic spec auditor parse the fenced blocks by language tag.

### Human-readable summary

```text
ERROR_CODE_DOMAINS:
  E1xxx   System / Internal
  E2xxx   Validation / Request
  E3xxx   Authentication
  E4xxx   Authorization
  E5xxx   Resource / NotFound
  E6xxx   Conflict / State
  E7xxx   RateLimit / Quota
  E8xxx   ExternalService / Delegation
  E9xxx   Database / Persistence
  E10xxx  FileSystem / IO
  E11xxx  Network / Transport
  E12xxx  Configuration
  E13xxx  Scheduler / Job
  E14xxx  Domain-Specific (per-feature)
RESULT_GUARD_RULE:
  Result[T].Value MUST NOT be accessed when Result[T].Error != nil (AC-06).
  Enforced via private fields + IsOk() / IsErr() / Unwrap() / UnwrapErr() methods.
ENUM_PATTERN:
  AppErrType uses byte-based enums with custom MarshalJSON/UnmarshalJSON
  (mirrors spec/02-coding-guidelines/03-golang/01-enum-specification).
STACK_TRACE_RULE:
  Stack capture MUST skip internal apperror frames so caller is frame[0] (AC-07).
```

### Normative Go contract (authoritative apperror package source-of-truth)

```go
// Package apperror provides the unified error-handling system for the Go application.
// This block is the SOURCE OF TRUTH for AC-01..AC-07; any code under pkg/apperror/
// MUST conform to these signatures. The auditor `audit-spec-vs-code-v2.py` parses
// this fenced `go` block to satisfy gate G-CON-01 (contract presence).
package apperror

import (
    "encoding/json"
    "runtime"
)

// ---------- AppErrType: byte-based enum with custom JSON marshalling ----------

// AppErrType is a byte-sized enum identifying the error domain (E1xxx..E14xxx).
// Stored as byte for memory efficiency; serialized as the canonical "EXxxx" string.
type AppErrType byte

const (
    // E1xxx — System / Internal
    ErrSystemUnknown    AppErrType = 0x10
    ErrSystemPanic      AppErrType = 0x11
    // E2xxx — Validation / Request
    ErrValidationFailed AppErrType = 0x20
    ErrInvalidArgument  AppErrType = 0x21
    // E3xxx — Authentication
    ErrAuthRequired     AppErrType = 0x30
    ErrAuthInvalid      AppErrType = 0x31
    // E4xxx — Authorization
    ErrForbidden        AppErrType = 0x40
    // E5xxx — Resource / NotFound
    ErrNotFound         AppErrType = 0x50
    // E6xxx — Conflict / State
    ErrConflict         AppErrType = 0x60
    // E7xxx — RateLimit / Quota
    ErrRateLimited      AppErrType = 0x70
    // E8xxx — ExternalService / Delegation
    ErrExternalService  AppErrType = 0x80
    // E9xxx — Database / Persistence
    ErrDatabase         AppErrType = 0x90
    // E10xxx — FileSystem / IO
    ErrFilesystem       AppErrType = 0xA0
    // E11xxx — Network / Transport
    ErrNetwork          AppErrType = 0xB0
    // E12xxx — Configuration
    ErrConfig           AppErrType = 0xC0
    // E13xxx — Scheduler / Job
    ErrScheduler        AppErrType = 0xD0
    // E14xxx — Domain-Specific (per-feature; subdivided by app)
    ErrDomain           AppErrType = 0xE0
)

// String returns the canonical "EXxxx" code for this type (AC-03, AC-05).
func (t AppErrType) String() string { return appErrTypeCanonical[t] }

// MarshalJSON serialises AppErrType as its canonical "EXxxx" string (AC-05).
func (t AppErrType) MarshalJSON() ([]byte, error) { return json.Marshal(t.String()) }

// UnmarshalJSON parses the canonical "EXxxx" string back into the byte enum.
func (t *AppErrType) UnmarshalJSON(b []byte) error {
    var s string
    if err := json.Unmarshal(b, &s); err != nil {
        return err
    }
    v, ok := appErrTypeFromCanonical[s]
    if !ok {
        return ErrInvalidArgument.New("unknown AppErrType: " + s).Err()
    }
    *t = v
    return nil
}

var appErrTypeCanonical = map[AppErrType]string{ /* populated at init time */ }
var appErrTypeFromCanonical = map[string]AppErrType{ /* inverse populated at init time */ }

// ---------- StackTrace ----------

// StackFrame is one captured runtime frame.
type StackFrame struct {
    File     string `json:"file"`
    Line     int    `json:"line"`
    Function string `json:"function"`
}

// StackTrace is an ordered list of frames; frame[0] is the caller of the constructor (AC-07).
type StackTrace []StackFrame

// captureStack walks runtime.Callers, skipping the requested number of internal apperror frames.
// AC-07: skipFrames MUST be tuned so the apperror package itself never appears at frame[0].
func captureStack(skipFrames int) StackTrace {
    pcs := make([]uintptr, 32)
    n := runtime.Callers(skipFrames+2, pcs)
    frames := runtime.CallersFrames(pcs[:n])
    out := make(StackTrace, 0, n)
    for {
        f, more := frames.Next()
        out = append(out, StackFrame{File: f.File, Line: f.Line, Function: f.Function})
        if !more {
            break
        }
    }
    return out
}

// ---------- AppError ----------

// AppError is the unified error type for the application.
// JSON-serialisable (AC-05); always carries a stack trace (AC-01) and a trace ref.
type AppError struct {
    Code    AppErrType `json:"code"`
    Message string     `json:"message"`
    Stack   StackTrace `json:"stack"`
    Ref     string     `json:"ref"` // trace ID or correlation ID
    inner   error      // wrapped underlying error (not serialised)
}

// New constructs an AppError with the caller's stack as frame[0] (AC-01, AC-07).
func (t AppErrType) New(msg string) *AppError {
    return &AppError{Code: t, Message: msg, Stack: captureStack(1)}
}

// Wrap wraps an existing error into a new AppError (AC-04 — adapter pattern).
func (t AppErrType) Wrap(err error, msg string) *AppError {
    if err == nil {
        return nil
    }
    if ae, ok := err.(*AppError); ok {
        // Re-wrap an existing AppError, preserving original stack.
        return &AppError{Code: t, Message: msg, Stack: ae.Stack, Ref: ae.Ref, inner: ae}
    }
    return &AppError{Code: t, Message: msg, Stack: captureStack(1), inner: err}
}

func (e *AppError) Error() string  { return e.Message }
func (e *AppError) Unwrap() error  { return e.inner }
func (e *AppError) Err() *AppError { return e }

// ---------- Result[T] — generic guarded container (AC-02, AC-06) ----------

// Result wraps either a value of type T or an AppError. Fields are PRIVATE
// to enforce AC-06: the caller MUST go through IsOk/IsErr/Unwrap.
type Result[T any] struct {
    value T
    err   *AppError
}

func Ok[T any](v T) Result[T]            { return Result[T]{value: v} }
func Err[T any](e *AppError) Result[T]   { return Result[T]{err: e} }

func (r Result[T]) IsOk() bool           { return r.err == nil }
func (r Result[T]) IsErr() bool          { return r.err != nil }

// Unwrap PANICS if r.IsErr() (AC-06 guard rule).
func (r Result[T]) Unwrap() T {
    if r.err != nil {
        panic("apperror: Result.Unwrap on Err: " + r.err.Message)
    }
    return r.value
}

// UnwrapErr PANICS if r.IsOk().
func (r Result[T]) UnwrapErr() *AppError {
    if r.err == nil {
        panic("apperror: Result.UnwrapErr on Ok")
    }
    return r.err
}

// ResultSlice is the slice variant; same guard rules apply.
type ResultSlice[T any] struct {
    items []T
    err   *AppError
}

func OkSlice[T any](items []T) ResultSlice[T]      { return ResultSlice[T]{items: items} }
func ErrSlice[T any](e *AppError) ResultSlice[T]   { return ResultSlice[T]{err: e} }
func (r ResultSlice[T]) IsOk() bool                { return r.err == nil }
func (r ResultSlice[T]) Items() []T                {
    if r.err != nil { panic("apperror: ResultSlice.Items on Err") }
    return r.items
}

// ResultMap is the map variant.
type ResultMap[K comparable, V any] struct {
    data map[K]V
    err  *AppError
}

func OkMap[K comparable, V any](data map[K]V) ResultMap[K, V]     { return ResultMap[K, V]{data: data} }
func ErrMap[K comparable, V any](e *AppError) ResultMap[K, V]     { return ResultMap[K, V]{err: e} }
func (r ResultMap[K, V]) IsOk() bool                              { return r.err == nil }
func (r ResultMap[K, V]) Data() map[K]V {
    if r.err != nil { panic("apperror: ResultMap.Data on Err") }
    return r.data
}
```

### Normative TypeScript mirror (frontend / cross-language clients)

```ts
// Cross-language mirror of the Go apperror contract. Frontend consumers receive AppError
// JSON over the wire; this type exposes the same shape using a discriminated union to
// emulate the Go Result[T] guard rule (AC-06) at the type level.

/** Canonical EXxxx error-code domain string. */
export type AppErrCode =
  | `E1${number}`  | `E2${number}`  | `E3${number}`  | `E4${number}`
  | `E5${number}`  | `E6${number}`  | `E7${number}`  | `E8${number}`
  | `E9${number}`  | `E10${number}` | `E11${number}` | `E12${number}`
  | `E13${number}` | `E14${number}`;

export interface StackFrame {
  readonly file: string;
  readonly line: number;
  readonly function: string;
}

export interface AppError {
  readonly code: AppErrCode;
  readonly message: string;
  readonly stack: readonly StackFrame[];
  readonly ref: string;
}

/** Discriminated union enforcing AC-06 at the type level. */
export type Result<T> =
  | { readonly ok: true;  readonly value: T }
  | { readonly ok: false; readonly error: AppError };

export const Ok  = <T>(value: T): Result<T> => ({ ok: true, value });
export const Err = <T>(error: AppError): Result<T> => ({ ok: false, error });

/** Type-narrowing helpers. */
export const isOk  = <T>(r: Result<T>): r is { ok: true;  value: T }     => r.ok;
export const isErr = <T>(r: Result<T>): r is { ok: false; error: AppError } => !r.ok;
```

### Normative JSON Schema (wire format for AppError)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://lovable.spec/03-error-manage/06-apperror-package/apperror.schema.json",
  "title": "AppError",
  "description": "Wire format for the apperror.AppError struct. Verifies AC-01 (stack present), AC-03 (code domain), AC-05 (canonical code string).",
  "type": "object",
  "required": ["code", "message", "stack", "ref"],
  "additionalProperties": false,
  "properties": {
    "code": {
      "type": "string",
      "pattern": "^E(1[0-4]|[1-9])[0-9]{1,3}$",
      "description": "Canonical EXxxx error code; X in 1..14 per ERROR_CODE_DOMAINS."
    },
    "message": { "type": "string", "minLength": 1 },
    "stack": {
      "type": "array",
      "minItems": 1,
      "description": "AC-01: every AppError MUST carry a non-empty stack. AC-07: frame[0] is the caller, never the apperror package itself.",
      "items": {
        "type": "object",
        "required": ["file", "line", "function"],
        "properties": {
          "file":     { "type": "string" },
          "line":     { "type": "integer", "minimum": 1 },
          "function": { "type": "string" }
        }
      }
    },
    "ref": {
      "type": "string",
      "description": "Trace / correlation ID (e.g. UUID, OpenTelemetry trace-id). MUST be non-empty for cross-service propagation."
    }
  }
}
```

---


## Acceptance Criteria

### AC-01: StackTrace Injection in AppError Constructors  `[critical]`
- **Given** A call to a constructor in 02-apperror-struct.md to create an AppError
- **When** An AppError instance is instantiated using the package's factory methods.
- **Then** The returned object must contain a StackTrace as defined in 01-overview-and-stack.md with accurate file and line information.
- **Verifies:** 01-overview-and-stack.md, 02-apperror-struct.md

### AC-02: Generic Result Type Container Integrity  `[critical]`
- **Given** A generic type T and the Result[T] definition in 03-result-types.md
- **When** A function returns a Result[T] to encapsulate failure or success.
- **Then** The Result type must provide access to either the value of type T or an AppError, but never both in a valid 'success' state.
- **Verifies:** 03-result-types.md

### AC-03: Domain-Specific Error Code Mapping  `[high]`
- **Given** The error code conventions in 04-codes-and-policy.md
- **When** An AppErrType enum value is assigned to an AppError.
- **Then** The error code must follow the E1xxx–E14xxx domain mapping defined in 05-apperrtype-enums.md.
- **Verifies:** 04-codes-and-policy.md, 05-apperrtype-enums.md

### AC-04: Adapter Pattern Error Conversion  `[medium]`
- **Given** The service adapter unwrap pattern from 05-usage-and-adapters.md
- **When** An external service error is processed by the AppError adapter.
- **Then** The adapter must correctly extract the inner error or convert a standard Go 'error' into an AppError before returning.
- **Verifies:** 05-usage-and-adapters.md

### AC-05: AppError JSON Serialization Masking  `[high]`
- **Given** The JSON serialization requirements in 06-serialization-and-guards.md and the Enum Specification cross-reference
- **When** The AppError is marshaled for delivery over an API boundary.
- **Then** The AppError and its internal AppErrType must be serialized to JSON using the byte-based enum pattern with mandatory JSON marshaling.
- **Verifies:** 06-serialization-and-guards.md, 05-apperrtype-enums.md

### AC-06: Result Guard Rule Enforcement  `[medium]`
- **Given** The Result guard rule in 06-serialization-and-guards.md
- **When** A programmer attempts to access Result[T].Value when Result[T].Error is present.
- **Then** The Result object must prevent access to the data payload if the internal AppError is non-nil/contains a failure code.
- **Verifies:** 06-serialization-and-guards.md

### AC-07: StackTrace Frame Skipping Logic  `[low]`
- **Given** The stack trace skip rules in 04-codes-and-policy.md
- **When** The runtime stack is captured during AppError creation.
- **Then** The StackTrace must correctly skip the internal apperror package frames so the caller's location is the head of the trace.
- **Verifies:** 04-codes-and-policy.md, 01-overview-and-stack.md

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)