# Golang Standards — Acceptance Criteria

**Version:** 4.1.0
**Last Updated:** 2026-04-29
**Scope:** `spec/02-coding-guidelines/03-golang/` — Go-specific coding standards layered on the cross-language parent.

---

## Module Summary

§02/03-golang codifies Go-specific rules: `apperror.Result[T]` over panics, `(T, error)` idiom for stdlib boundaries, exported `MixedCaps` / unexported `mixedCaps`, acronym casing (`URL`/`ID`/`HTTP` always all-caps), `defer` placement rules, no `panic` outside `main`, generics over `interface{}`, `golangci-lint` enforcement, `errors.Is`/`As` for matching, context propagation, single-flight on hot paths. Inherits ALL **AC-CL-01..AC-CL-20** per AC-CL-01.

---

## Inlined Contracts

```text
PARENT_INHERITANCE:        ../01-cross-language/97 (AC-CL-01..AC-CL-20)
MIN_GO_VERSION:            1.22 (generics + range-over-int + slog)
ERROR_PATTERN:             apperror.Result[T] for project APIs
                           (T, error) for stdlib/library boundaries
                           NEVER panic outside main() / init() / tests
ENUM_PATTERN:              type X string + const block + Validate() method
                           (NOT iota for stable wire types)
NAMING:                    Exported: MixedCaps (UserID, HTTPClient)
                           Unexported: mixedCaps (userID, httpClient)
                           Acronyms: ALL CAPS (URL, ID, API, HTTP, JSON, SQL)
                           NEVER: Url, Id, Http, Api, Json, Sql
DEFER_RULES:               defer immediately after acquiring resource
                           NEVER defer inside loops without scope-bounding
                           defer ordering: LIFO (last-deferred runs first)
LINTER:                    golangci-lint with .golangci.yml
                           required: govet, errcheck, staticcheck,
                                     ineffassign, gosec, unparam, gosimple,
                                     unconvert, misspell, gocyclo (≤10),
                                     revive (replaces golint)
CONCURRENCY:               context.Context as first parameter
                           goroutines MUST have explicit cancellation
                           channels typed; sender owns the close
                           sync.WaitGroup for fan-out, errgroup for fan-out-with-error
GENERICS:                  prefer generic constraints over interface{} (Go 1.18+)
                           constraints package + custom interfaces
INHERITED_FROM_AC_CL:      strict typing (AC-CL-04), null safety/(T,error) (AC-CL-13),
                           Result over panic (AC-CL-17), kebab-case files (AC-CL-12),
                           DRY rule-of-three (AC-CL-20)
```

---

## Acceptance Criteria

### AC-GO-01 — Inherits all AC-CL-01..AC-CL-20 from cross-language parent

- **Given** any `.go` file in the codebase,
- **When** reviewed,
- **Then** it MUST satisfy every AC-CL-* rule from `../01-cross-language/97-acceptance-criteria.md`. Conflicts MUST resolve in favor of the cross-language rule per AC-CL-01. Go-specific ACs below LAYER on top of cross-language ACs and MUST NOT contradict them. Any waiver MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** AC-CL-01 inheritance contract.

### AC-GO-02 — Minimum Go version 1.22; toolchain pinned in `go.mod`

- **Given** the project's `go.mod`,
- **When** parsed,
- **Then** the `go` directive MUST be `>= 1.22` AND a `toolchain` directive MUST pin a specific 1.22.x release (e.g. `toolchain go1.22.5`). Lower versions are FORBIDDEN — they lack generics-over-int range, `slog`, `errors.Join`, and the v2 `math/rand` semantics this project assumes. CI MUST run on the pinned toolchain version.
- **Verifies:** Project Go version baseline.

### AC-GO-03 — Acronyms in identifiers are ALL-CAPS

- **Given** any exported or unexported identifier containing an acronym,
- **When** the identifier is parsed,
- **Then** acronyms MUST be ALL-CAPS: `URL`, `ID`, `API`, `HTTP`, `JSON`, `SQL`, `HTTPS`, `URI`, `UUID`, `XML`, `IO`, `OS`, `RPC`. Forms `Url`, `Id`, `Http`, `Api`, `Json` are FORBIDDEN. The exception: when at the start of an UNexported identifier, lowercase the entire acronym (`urlParser` not `URLParser`; `idGen` not `IDGen`). `revive` rule `var-naming` MUST enforce this.
- **Verifies:** Effective Go naming + `golang.org/wiki/CodeReviewComments#initialisms`.

### AC-GO-04 — `apperror.Result[T]` for project APIs; `(T, error)` for stdlib boundaries

- **Given** any function that can fail,
- **When** the signature is designed,
- **Then** project-internal APIs MUST return `apperror.Result[T]` (per AC-CL-17 inherited). Functions implementing stdlib interfaces (e.g. `io.Reader.Read`, `json.Marshaler.MarshalJSON`) or interacting with third-party libs MUST use the idiomatic `(T, error)` form. Mixing the two within one package is allowed; mixing within one call chain is FORBIDDEN — convert at the boundary.
- **Verifies:** AC-CL-17 + project AppError contract.

### AC-GO-05 — `panic` is forbidden outside `main()`, `init()`, and `_test.go`

- **Given** any `.go` source file (excluding `*_test.go`),
- **When** scanned for `panic(` calls,
- **Then** zero matches MUST be found unless the file is `main.go` (top-level fatal init) or contains an `init()` function with the panic. All other failures MUST return errors via `apperror.Result[T]` or `(T, error)`. `must*()` helper functions that panic are allowed ONLY in `_test.go`. `golangci-lint` rule `revive: deep-exit` MUST flag violations.
- **Verifies:** AC-CL-17 + Go panic discipline.

### AC-GO-06 — Errors compared via `errors.Is` / `errors.As`, never `==` or string match

- **Given** any error comparison,
- **When** the comparison is parsed,
- **Then** sentinel errors MUST be matched via `errors.Is(err, ErrFoo)`; typed errors MUST be matched via `errors.As(err, &target)`. Direct `err == ErrFoo` is FORBIDDEN (breaks wrapping). String matching (`strings.Contains(err.Error(), "...")`) is FORBIDDEN — it's brittle and fails on translation. Sentinel errors MUST be declared as exported package-level vars: `var ErrNotFound = errors.New("not found")`.
- **Verifies:** Go 1.13+ error wrapping idiom.

### AC-GO-07 — `context.Context` is the first parameter on every cancellable function

- **Given** any function that performs I/O, blocks, or spawns goroutines,
- **When** the signature is parsed,
- **Then** `ctx context.Context` MUST be the FIRST parameter (before `self`/receiver — receiver is implicit, so first non-receiver). Storing `context.Context` in a struct field is FORBIDDEN — it leaks request scope. Passing `context.TODO()` outside test/scaffold code is FORBIDDEN. `context.Background()` is allowed only at process roots (`main`, top-level handlers).
- **Verifies:** Go context idiom + `context-as-input-parameter` revive rule.

### AC-GO-08 — `defer` placed immediately after resource acquisition; never inside unbounded loops

- **Given** any resource acquisition (`os.Open`, `sql.DB.Conn`, `Mutex.Lock`, response body),
- **When** the code is reviewed,
- **Then** `defer cleanup()` MUST appear on the line IMMEDIATELY following the acquisition. Defer inside an unbounded loop is FORBIDDEN — defers stack until function return, causing leaks. To loop-defer, MUST extract the body into a function so each iteration's defer fires at iteration end. The 5 defer rules in `05-defer-rules.md` are binding.
- **Verifies:** `05-defer-rules.md` + memory-leak prevention.

### AC-GO-09 — Enums use `type X string` + const block + `Validate()` method (NOT iota)

- **Given** any enum-like type for a value that crosses the wire (DB, JSON, HTTP),
- **When** declared,
- **Then** it MUST follow the `type X string` pattern with a const block and a `Validate() error` method. Example: `type HttpMethod string; const ( HttpMethodGET HttpMethod = "GET"; HttpMethodPOST HttpMethod = "POST" ); func (m HttpMethod) Validate() error { ... }`. The `iota` integer pattern is FORBIDDEN for wire types — int values are unstable across reorders. `iota` is allowed for purely internal flags / bit masks.
- **Verifies:** `01-enum-specification/` + `03-httpmethod-enum.md`.

### AC-GO-10 — Generics preferred over `interface{}` / `any` for typed containers

- **Given** any container or utility function that should accept multiple types,
- **When** the signature is designed,
- **Then** Go generics (`func Foo[T comparable](x T) T`) MUST be used. `interface{}` / `any` parameters are FORBIDDEN unless the function genuinely accepts heterogeneous types (e.g. `fmt.Println`-like). Type assertions on `any` (`x.(string)`) outside FFI/reflection boundaries MUST be replaced with generic constraints. The `constraints` package + custom interface constraints are the standard tools.
- **Verifies:** AC-CL-04 + Go 1.18+ generics idiom.

### AC-GO-11 — Goroutines MUST have explicit cancellation; no fire-and-forget

- **Given** any `go func() { ... }()` invocation,
- **When** the goroutine is reviewed,
- **Then** the goroutine MUST have an explicit cancellation path — either (a) the goroutine reads from a `<-ctx.Done()` case, (b) the goroutine receives from a quit channel, (c) the goroutine joins via `sync.WaitGroup` / `errgroup.Group.Wait()`. Fire-and-forget goroutines (no way to stop or join) are FORBIDDEN — they leak on shutdown and hide errors. `errgroup` is preferred for fan-out-with-error.
- **Verifies:** Goroutine lifecycle discipline.

### AC-GO-12 — Channels: receiver-only / sender-only direction in signatures; sender closes

- **Given** any function that takes or returns a channel,
- **When** the signature is parsed,
- **Then** the channel MUST be declared with explicit direction: `<-chan T` (receive-only) for consumers, `chan<- T` (send-only) for producers. Bidirectional `chan T` in signatures is FORBIDDEN — it leaks responsibility. The SENDER (and only the sender) MUST close the channel. Closing a receive-end channel is a runtime panic.
- **Verifies:** Channel direction + ownership.

### AC-GO-13 — `golangci-lint` config enables 10 required linters; CI fails on any warning

- **Given** the project's `.golangci.yml`,
- **When** parsed,
- **Then** `linters.enable` MUST include: `govet`, `errcheck`, `staticcheck`, `ineffassign`, `gosec`, `unparam`, `gosimple`, `unconvert`, `misspell`, `gocyclo` (with `min-complexity: 10` per AC-CL-06), `revive`. CI MUST run `golangci-lint run --max-issues-per-linter=0 --max-same-issues=0` and fail on ANY issue. Disabling a linter requires `99-consistency-report.md` waiver row.
- **Verifies:** `04-golang-standards-reference.md` linter section + AC-CL-06.

### AC-GO-14 — Naming: receiver names are 1-3 letter abbreviations of the type

- **Given** any method receiver,
- **When** the receiver name is inspected,
- **Then** it MUST be a 1-3 letter abbreviation of the type (`func (u *User) ...`, `func (db *DB) ...`, `func (cfg *Config) ...`). `self`, `this`, `me`, the full type name (`func (user *User)`), or single-letter pure-pronoun (`s` for `Server`) are FORBIDDEN unless they're the type abbreviation. Receivers MUST be consistent across all methods of one type — mixing `func (u *User)` and `func (usr *User)` is FORBIDDEN.
- **Verifies:** Effective Go receiver-name rule.

### AC-GO-15 — Pointer vs value receivers: documented choice per type, no mixing

- **Given** any struct type with methods,
- **When** the methods are inspected,
- **Then** ALL methods MUST use the SAME receiver style (all pointer `*T` OR all value `T`). Mixing is FORBIDDEN — it breaks interface satisfaction unpredictably. The choice MUST be: pointer receivers for types that mutate state, hold sync primitives, are large (>~64 bytes), or implement an interface where any implementor uses pointer; value receivers for small immutable value types (`time.Time`-like).
- **Verifies:** `golang.org/wiki/CodeReviewComments#receiver-type`.

### AC-GO-16 — Struct tags include explicit JSON tag with PascalCase wire name (per AC-CL-09)

- **Given** any struct field that is serialized to JSON,
- **When** the tag is inspected,
- **Then** the field MUST carry a `json:"PascalCaseName"` tag (per AC-CL-09 inherited PascalCase wire format). Untagged exported fields would emit Go's `MixedCaps` to JSON, violating the wire contract. Optional fields MUST add `,omitempty` only when zero-value semantically means absent. Sensitive fields MUST use `json:"-"` AND include a comment explaining the redaction.
- **Verifies:** AC-CL-09 + Go json idiom.

### AC-GO-17 — Tests use table-driven pattern + `t.Run(name, ...)` subtests

- **Given** any `_test.go` file with multiple test cases,
- **When** parsed,
- **Then** test cases MUST be expressed as a table (`tests := []struct{ name string; input ...; want ... }{...}`) iterated with `t.Run(tt.name, func(t *testing.T) { ... })`. Multiple sequential top-level `func TestX_*` for variants of the same behavior are FORBIDDEN. `t.Parallel()` SHOULD be called in subtests where safe. Test names MUST describe BEHAVIOR per AC-CL-19 inherited.
- **Verifies:** AC-CL-19 + Go table-driven idiom.

### AC-GO-18 — `go.mod` dependencies are minimal; vendored deps prohibited unless air-gapped

- **Given** the project's `go.mod` + `go.sum`,
- **When** reviewed,
- **Then** dependencies MUST be the minimum needed; transitive `require` blocks MUST be regularly pruned via `go mod tidy`. Vendored `vendor/` directories are FORBIDDEN unless the project explicitly targets air-gapped builds (waiver in `99` required). Indirect dependencies that exceed direct dep count by 10x SHOULD trigger a dependency review.
- **Verifies:** Dependency hygiene.

### AC-GO-19 — Logging uses `log/slog` with structured key-value pairs; no `fmt.Println`

- **Given** any logging call in non-test code,
- **When** inspected,
- **Then** it MUST use `log/slog` (Go 1.21+) with structured K/V: `slog.Info("user authenticated", "user_id", id, "method", method)`. `fmt.Println` / `fmt.Printf` for logging is FORBIDDEN — it has no level, no structure, no destination control. `log.Printf` (stdlib old) is FORBIDDEN — superseded by `slog`. PII in log keys/values MUST be redacted before emit.
- **Verifies:** Modern Go logging idiom + observability.

### AC-GO-20 — Self-application: this folder's Go examples + enum patterns satisfy AC-GO-01..AC-GO-19

- **Given** every code example in `02-boolean-standards.md`, `03-httpmethod-enum.md`, `04-golang-standards-reference.md`, `05-defer-rules.md`, `06-string-slice-internals.md`, `08-pathutil-fileutil-spec.md`, and the `01-enum-specification/` subfolder,
- **When** mechanically extracted and compiled with `go vet ./... && golangci-lint run`,
- **Then** every example MUST pass without errors AND satisfy AC-GO-09 (`type X string` enums NOT iota for wire types) AND satisfy AC-GO-08 (defer placement). Example code that violates its own ACs is a CODE-RED documentation-drift bug.
- **Verifies:** Recursive self-check + AC-SAG-18 dogfooding analogue.

---

## Legacy Index (preserved for traceability)

The following stub criteria from v3.2.0 are preserved verbatim. They are NO LONGER authoritative — the GWT ACs above supersede them.

### AC-GO-LEGACY: Code Standards

- [ ] AC-GO-LEGACY-01-A — Boolean standards define naming (`isX`, `hasX`, `canX`) and evaluation patterns
- [ ] AC-GO-LEGACY-01-B — Error handling uses `apperror.Result[T]` pattern consistently
- [ ] AC-GO-LEGACY-01-C — Naming conventions follow Go idioms (exported/unexported, acronym casing)


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-GO-LEGACY: Architecture

- [ ] AC-GO-LEGACY-02-A — Service layer follows interface-based dependency injection
- [ ] AC-GO-LEGACY-02-B — HTTP handlers use typed request/response structs
- [ ] AC-GO-LEGACY-02-C — Database access uses repository pattern with prepared statements

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Cross-language parent (AC-CL-*)](../01-cross-language/97-acceptance-criteria.md)
- [Golang standards reference](./04-golang-standards-reference.md)
- [Defer rules](./05-defer-rules.md)
- [HTTP method enum pattern](./03-httpmethod-enum.md)
- [Enum specification subfolder](./01-enum-specification/)
- [Boolean standards](./02-boolean-standards.md)
- [§02 parent governance](../97-acceptance-criteria.md)
- [TypeScript sibling](../02-typescript/97-acceptance-criteria.md)

> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
