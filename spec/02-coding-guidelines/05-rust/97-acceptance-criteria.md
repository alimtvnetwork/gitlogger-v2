# Rust Coding Standards — Acceptance Criteria

**Version:** 4.1.0
**Last Updated:** 2026-04-29
**Scope:** `spec/02-coding-guidelines/05-rust/` — Rust 2021/2024-edition coding standards layered on the cross-language parent.

---

## Module Summary

§02/05-rust codifies Rust-specific rules: `Result<T, E>` over panics with `thiserror` for domain errors and `anyhow` for application context, `?` operator for propagation (no `unwrap()`/`expect()` outside tests/main), Tokio async with bounded MPSC channels and cancellation-safe selects, `unsafe` blocks require `// SAFETY:` justification per block, borrowing + `Arc` over `Clone` on hot paths, snake_case modules/files, PascalCase types, SCREAMING_SNAKE_CASE consts, `#[serde(rename_all = "PascalCase")]` for wire types per AC-CL-09, `clippy::pedantic` with documented allows, `cargo deny` for licenses + advisories, `#[cfg(target_os)]` + `PlatformApi` traits for cross-platform code, FFI boundaries with safety docs. Inherits ALL **AC-CL-01..AC-CL-20** per AC-CL-01.

---

## Inlined Contracts

```text
PARENT_INHERITANCE:        ../01-cross-language/97 (AC-CL-01..AC-CL-20)
MIN_RUST_VERSION:          1.75 (async-fn-in-trait stable, let-else, GATs)
                           Edition 2021 minimum; 2024 preferred when stable
EDITION:                   edition = "2021" in Cargo.toml (or "2024")
ERROR_CRATES:              thiserror = "1.x"   (domain errors with #[derive(Error)])
                           anyhow    = "1.x"   (application-layer context wrapping)
                           NEVER:    Box<dyn Error> as a domain return type
                           NEVER:    panic!() / unreachable!() / todo!() outside tests
                           NEVER:    unwrap() / expect() outside main/tests/build.rs
ERROR_PATTERN:             Library/domain layer:  Result<T, MyError> + thiserror
                           Application layer:     Result<T, anyhow::Error> + .context()
                           Conversion at boundary via #[from] or .map_err()
ASYNC_RUNTIME:             tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
                           NEVER mix async-std with tokio in the same crate
CHANNELS:                  bounded mpsc::channel(N) — never unbounded
                           oneshot for request/response
                           broadcast for fan-out
                           Drop sender → channel closes (idiom)
CANCELLATION:              tokio::select! with biased; pattern for fairness control
                           Cancellation-safe futures only inside select! arms
                           Use tokio_util::sync::CancellationToken for explicit cancel
NAMING:                    Crates:    kebab-case  (my-crate)
                           Modules:   snake_case  (mod my_module)
                           Files:     snake_case.rs (matches module)
                           Types:     PascalCase  (struct UserId, enum HttpMethod)
                           Traits:    PascalCase  (trait FromBytes)
                           Functions: snake_case  (fn parse_request)
                           Variables: snake_case  (let user_id)
                           Consts:    SCREAMING_SNAKE_CASE (const MAX_SIZE)
                           Statics:   SCREAMING_SNAKE_CASE
                           Lifetimes: 'short_snake_case ('a, 'src)
                           Generics:  Single PascalCase letter or PascalCase word
SERDE_WIRE_FORMAT:         #[serde(rename_all = "PascalCase")]  ← AC-CL-09
                           on every struct/enum that crosses the wire
                           Field-level #[serde(rename = "...")] only for legacy
UNSAFE_DISCIPLINE:         Every unsafe { ... } block MUST be preceded by:
                             // SAFETY: <invariant being upheld + why>
                           Every unsafe fn MUST document # Safety in rustdoc
                           #![forbid(unsafe_code)] in crates without FFI
LINTER:                    cargo clippy --all-targets --all-features -- -D warnings
                           clippy::pedantic enabled, with #[allow(...)] documented
                           cargo fmt --check (rustfmt enforced)
                           cargo deny check (licenses + advisories + bans)
                           cargo audit (RustSec advisory db)
INHERITED_FROM_AC_CL:      strict typing (AC-CL-04), Result over panic (AC-CL-17),
                           PascalCase wire (AC-CL-09), kebab-case files for crates
                           (AC-CL-12 — but Rust modules use snake_case, see AC-RS-07),
                           DRY rule-of-three (AC-CL-20)
```

---

## Acceptance Criteria

### AC-RS-01 — Inherits all AC-CL-01..AC-CL-20 from cross-language parent

- **Given** any `.rs` file in the codebase,
- **When** reviewed,
- **Then** it MUST satisfy every AC-CL-* rule from `../01-cross-language/97-acceptance-criteria.md`. Conflicts MUST resolve in favor of the cross-language rule per AC-CL-01, with the documented exception of AC-CL-12 file-naming (kebab-case) — Rust uses `snake_case.rs` per the language convention; see AC-RS-07. Any other waiver MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** AC-CL-01 inheritance contract.

### AC-RS-02 — Minimum Rust 1.75; edition pinned in `Cargo.toml`

- **Given** every crate's `Cargo.toml`,
- **When** parsed,
- **Then** the `[package]` table MUST include `edition = "2021"` (or `"2024"` when stable) AND the workspace `rust-version` MUST be `>= 1.75` to guarantee stable async-fn-in-trait, `let-else`, and GATs. Lower versions are FORBIDDEN. CI MUST install the exact `rust-version` from `rust-toolchain.toml` (which MUST exist at the workspace root and pin a specific stable channel).
- **Verifies:** Project Rust baseline.

### AC-RS-03 — Domain errors use `thiserror`; application errors use `anyhow` with `.context()`

- **Given** any function that can fail,
- **When** the return type is designed,
- **Then** library/domain crates MUST return `Result<T, MyError>` where `MyError` derives `thiserror::Error`. Application/binary crates MUST return `Result<T, anyhow::Error>` and MUST attach context via `.context("…")` or `.with_context(|| …)` at every error-conversion site. `Box<dyn Error>` as a domain return type is FORBIDDEN — it erases variant info and breaks pattern matching. Boundary conversions MUST use `#[from]` (preferred) or explicit `.map_err()`.
- **Verifies:** AC-CL-17 + `02-error-handling.md`.

### AC-RS-04 — `panic!`, `unwrap()`, `expect()`, `todo!()`, `unreachable!()` FORBIDDEN outside `main`/`tests`/`build.rs`

- **Given** any `.rs` file outside `src/main.rs`, `src/bin/*`, `tests/`, `benches/`, `examples/`, `build.rs`, and `#[cfg(test)]` modules,
- **When** scanned,
- **Then** zero matches MUST be found for `panic!(`, `.unwrap()`, `.expect(`, `todo!()`, `unreachable!()`, `unimplemented!()`. The `?` operator MUST be used for propagation. Lints `clippy::unwrap_used` and `clippy::expect_used` MUST be set to `deny` at the crate root (`#![deny(clippy::unwrap_used, clippy::expect_used)]`). Tests are exempt.
- **Verifies:** AC-CL-17 + Rust panic discipline.

### AC-RS-05 — `unsafe` blocks/fns require `// SAFETY:` comment + `# Safety` rustdoc

- **Given** any `unsafe { ... }` block or `unsafe fn` declaration,
- **When** the surrounding context is reviewed,
- **Then** every `unsafe` BLOCK MUST be preceded by a `// SAFETY: <invariants upheld + why this call is sound>` comment on the line(s) immediately above. Every `unsafe fn` MUST document a `# Safety` section in its rustdoc explaining the caller's obligations. Crates without FFI MUST set `#![forbid(unsafe_code)]` at the crate root. Adding `unsafe` requires a `99` waiver explaining why a safe alternative is impossible.
- **Verifies:** `04-memory-safety.md` + Rust `unsafe` discipline.

### AC-RS-06 — Tokio is the sole async runtime; mixing runtimes FORBIDDEN

- **Given** any crate with async functions,
- **When** `Cargo.toml` is parsed,
- **Then** `tokio` MUST be the runtime dependency with at least `features = ["rt-multi-thread", "macros"]`. Importing `async-std`, `smol`, or `futures-executor` (as a runtime) is FORBIDDEN — runtime mixing causes silent deadlocks. The `futures` crate is allowed for utility traits only. Crate roots that don't need a runtime SHOULD use `tokio` only via dev-dependencies for tests.
- **Verifies:** `03-async-patterns.md`.

### AC-RS-07 — Naming: crates kebab-case, modules/files/functions/vars snake_case, types/traits PascalCase, consts SCREAMING_SNAKE_CASE

- **Given** any Rust identifier,
- **When** declared,
- **Then** it MUST follow Rust API guidelines casing: crate names = kebab-case (`my-crate`); modules + filenames + functions + variables = snake_case (`mod user_service`, `user_service.rs`, `fn parse_request`, `let user_id`); types + traits + enum variants = PascalCase (`struct UserId`, `enum HttpMethod`, `trait FromBytes`); consts + statics = SCREAMING_SNAKE_CASE (`const MAX_SIZE: usize = 1024`); lifetimes = short snake_case with leading apostrophe (`'a`, `'src`). camelCase in any role is FORBIDDEN. This DOCUMENTED OVERRIDE of AC-CL-12 is the ONLY waiver granted to AC-CL inheritance.
- **Verifies:** `01-naming-conventions.md` + Rust API guidelines C-CASE.

### AC-RS-08 — Wire types use `#[serde(rename_all = "PascalCase")]` per AC-CL-09

- **Given** any struct or enum that is serialized to JSON / msgpack / wire,
- **When** the type is declared,
- **Then** it MUST carry `#[serde(rename_all = "PascalCase")]` at the type level so that snake_case Rust field names emit PascalCase wire keys (per AC-CL-09 inherited). Field-level `#[serde(rename = "Foo")]` is permitted ONLY for legacy/migration cases AND MUST be commented with the migration ticket. `#[serde(deny_unknown_fields)]` SHOULD be applied to inbound DTOs to catch wire-contract drift early.
- **Verifies:** AC-CL-09 + serde idiom.

### AC-RS-09 — Channels are bounded MPSC; unbounded channels FORBIDDEN

- **Given** any channel declaration,
- **When** parsed,
- **Then** `tokio::sync::mpsc::channel(N)` MUST be used with an explicit bound `N` (capacity reasoning documented in adjacent comment). `tokio::sync::mpsc::unbounded_channel()` is FORBIDDEN — unbounded channels mask backpressure and OOM. `oneshot` is required for request/response; `broadcast` for fan-out. The SENDER side reaching capacity MUST yield via `.send().await` (back-pressure), not `try_send` + drop.
- **Verifies:** `03-async-patterns.md`.

### AC-RS-10 — `tokio::select!` arms MUST be cancellation-safe; `biased;` documented when used

- **Given** any `tokio::select! { ... }` invocation,
- **When** the arms are reviewed,
- **Then** every future inside a select arm MUST be cancellation-safe per the Tokio docs (e.g. `mpsc::Receiver::recv`, `oneshot::Receiver`, `tokio::time::sleep`). Non-cancel-safe futures (e.g. mid-write `AsyncWriteExt::write_all` partway) MUST be wrapped in `tokio::pin!` + manual loop or held outside the select. Use of `biased;` MUST be accompanied by a comment explaining the fairness/priority decision. `tokio_util::sync::CancellationToken` SHOULD be threaded through long-running tasks for explicit cancel.
- **Verifies:** `03-async-patterns.md`.

### AC-RS-11 — Borrow over clone; `Arc<T>` for shared ownership; `Rc<T>` only single-threaded

- **Given** any function signature or shared-state design,
- **When** reviewed,
- **Then** parameters SHOULD take `&T` / `&mut T` (borrows) over `T` (move) over `T.clone()` (allocation). Shared ownership across threads MUST use `Arc<T>` (or `Arc<Mutex<T>>` / `Arc<RwLock<T>>` for shared mutability). `Rc<T>` is FORBIDDEN in code that touches Tokio (Tokio tasks are `Send`-required). Cloning large structs (>~64 bytes) on the hot path is FORBIDDEN unless benchmarked and documented in `99`.
- **Verifies:** `04-memory-safety.md`.

### AC-RS-12 — Tests follow AAA pattern; OS deps mocked via traits; integration tests in `tests/`

- **Given** any test in the project,
- **When** the test body is parsed,
- **Then** it MUST follow Arrange-Act-Assert structure with blank lines separating the three phases. OS dependencies (filesystem, network, time, env) MUST be abstracted behind a trait (`trait Clock`, `trait FileSystem`) and a fake/mock substituted in tests — direct calls to `std::fs`, `std::env`, `SystemTime::now()` in unit tests are FORBIDDEN. Integration tests MUST live in `tests/<feature>.rs`, NOT inside `#[cfg(test)] mod tests` (which is for unit tests only). Test names MUST describe BEHAVIOR per AC-CL-19.
- **Verifies:** `05-testing-standards.md` + AC-CL-19.

### AC-RS-13 — Cross-platform code uses `PlatformApi` traits + `#[cfg(target_os)]` at minimum scope

- **Given** any code that varies by OS (filesystem, process spawn, paths, signals),
- **When** the divergence point is identified,
- **Then** the OS-specific implementation MUST be hidden behind a `PlatformApi` trait with one impl per `target_os` in separate modules (`platform/linux.rs`, `platform/macos.rs`, `platform/windows.rs`). `#[cfg(target_os = "...")]` MUST scope to the smallest possible unit (preferably the entire impl module). Sprinkling `#[cfg]` inside function bodies is FORBIDDEN — it makes coverage analysis impossible.
- **Verifies:** `06-ffi-platform.md`.

### AC-RS-14 — FFI boundaries documented with `# Safety` rustdoc + `extern "C"` + `#[no_mangle]` discipline

- **Given** any FFI surface (`extern "C"` blocks, `#[no_mangle]` exports, `repr(C)` types),
- **When** declared,
- **Then** every FFI item MUST have rustdoc with `# Safety`, `# Errors`, and `# Panics` sections documenting C-side caller obligations. `#[no_mangle]` exports MUST use `extern "C"` ABI. C-bound types MUST be `#[repr(C)]` AND MUST NOT contain Rust-specific types (`String`, `Vec<T>` directly — wrap in pointer + length). Null pointer checks at FFI boundary are MANDATORY before deref.
- **Verifies:** `06-ffi-platform.md`.

### AC-RS-15 — `cargo clippy --all-targets --all-features -- -D warnings` + `clippy::pedantic` enabled

- **Given** the workspace root,
- **When** CI runs,
- **Then** `cargo clippy --workspace --all-targets --all-features -- -D warnings` MUST pass with zero warnings. `clippy::pedantic` MUST be enabled at the workspace root via `[workspace.lints.clippy] pedantic = "warn"`. Specific `#[allow(clippy::xxx)]` annotations MUST be accompanied by a comment explaining why. `cargo fmt --check` MUST pass. CI MUST also run `cargo deny check` (licenses + advisories) and `cargo audit`.
- **Verifies:** AC-CL-06 + linter contract.

### AC-RS-16 — `Cargo.lock` checked in for binaries; dependencies pinned to caret-with-patch

- **Given** the project's `Cargo.toml` files and `Cargo.lock`,
- **When** reviewed,
- **Then** `Cargo.lock` MUST be committed for binary crates and workspaces (not for libraries). Dependency versions MUST use caret with patch precision (`thiserror = "1.0.50"` not `"1"`). Git dependencies MUST be pinned to a `rev` SHA, never a branch. `[patch.crates-io]` overrides MUST be temporary AND tracked via a TODO ticket.
- **Verifies:** Dependency hygiene.

### AC-RS-17 — Logging uses `tracing` with structured fields; `println!`/`eprintln!` FORBIDDEN in non-test code

- **Given** any logging call in non-test code,
- **When** inspected,
- **Then** it MUST use the `tracing` crate with structured fields: `tracing::info!(user_id = %id, method = ?method, "user authenticated");`. `println!`, `eprintln!`, `dbg!`, `log::info!` (legacy `log` crate as a producer) are FORBIDDEN — they bypass spans, structured filtering, and async context. The application root MUST install a `tracing_subscriber` with JSON output (production) or pretty (dev). PII fields MUST be redacted via `#[derive(Debug)]` skip or custom `Display`.
- **Verifies:** Modern Rust observability.

### AC-RS-18 — Public APIs documented with rustdoc; `#![deny(missing_docs)]` on library crates

- **Given** any library crate's `lib.rs`,
- **When** parsed,
- **Then** it MUST set `#![deny(missing_docs)]` (or `#![warn(missing_docs)]` minimum) AND every `pub` item MUST have rustdoc with at least a one-sentence summary. Functions that can panic MUST document `# Panics`. Functions that return `Result` MUST document `# Errors`. `unsafe fn` MUST document `# Safety` (per AC-RS-05). Examples in rustdoc MUST compile via `cargo test --doc`.
- **Verifies:** Rust API guidelines C-DOC.

### AC-RS-19 — Lifetimes elided where the compiler accepts; explicit only when ambiguous

- **Given** any function with reference parameters or return,
- **When** the signature is reviewed,
- **Then** lifetimes MUST be elided if the compiler accepts elision (per the lifetime elision rules). Adding explicit lifetimes that the compiler would have inferred is FORBIDDEN — it adds noise. When explicit lifetimes ARE required (multiple input refs + ref return), names MUST be short snake_case (`'a`, `'src`, `'tok`) — NEVER `'long_descriptive_name`. Higher-rank trait bounds (`for<'a>`) MUST be commented when used.
- **Verifies:** Rust API guidelines C-LIFETIME.

### AC-RS-20 — Self-application: this folder's Rust examples compile + pass clippy

- **Given** every code example in `01-naming-conventions.md`, `02-error-handling.md`, `03-async-patterns.md`, `04-memory-safety.md`, `05-testing-standards.md`, `06-ffi-platform.md`,
- **When** mechanically extracted into a doctest harness and run with `cargo test --doc` + `cargo clippy --all-targets -- -D warnings`,
- **Then** every example MUST compile and pass clippy AND satisfy AC-RS-04 (no `unwrap()`/`expect()`), AC-RS-05 (`// SAFETY:` on any `unsafe`), AC-RS-08 (`#[serde(rename_all = "PascalCase")]` on wire types). Example code that violates its own ACs is a CODE-RED documentation-drift bug.
- **Verifies:** Recursive self-check + AC-SAG-18 dogfooding analogue.

---

## Legacy Index (preserved for traceability)

The following 18 stub criteria from v3.2.0 are preserved verbatim. They are NO LONGER authoritative — the GWT ACs above supersede them.

### AC-RS-LEGACY-01: Naming & Style

- [ ] PascalCase serialization uses `#[serde(rename_all = "PascalCase")]` consistently → superseded by AC-RS-08.
- [ ] Module and file naming follows Rust snake_case conventions → superseded by AC-RS-07.
- [ ] Exported types use descriptive, domain-specific names → superseded by AC-RS-07.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-RS-LEGACY-02: Error Handling

- [ ] Domain errors use `thiserror` with project error codes → superseded by AC-RS-03.
- [ ] Application logic uses `anyhow` with contextual messages → superseded by AC-RS-03.
- [ ] All error variants map to documented error codes → superseded by AC-RS-03.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-RS-LEGACY-03: Async Patterns

- [ ] Tokio async runtime is used consistently → superseded by AC-RS-06.
- [ ] Channel usage follows bounded MPSC patterns → superseded by AC-RS-09.
- [ ] Cancellation-safe patterns are applied in async code → superseded by AC-RS-10.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-RS-LEGACY-04: Memory Safety

- [ ] `unsafe` blocks include `// SAFETY:` justification comments → superseded by AC-RS-05.
- [ ] Borrowing and `Arc` are preferred over cloning → superseded by AC-RS-11.
- [ ] No unnecessary `Clone` derives on large structs → superseded by AC-RS-11.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-RS-LEGACY-05: Testing

- [ ] Unit tests follow AAA (Arrange-Act-Assert) pattern → superseded by AC-RS-12.
- [ ] OS dependencies use trait-based mocking → superseded by AC-RS-12.
- [ ] Integration tests are separated from unit tests → superseded by AC-RS-12.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
### AC-RS-LEGACY-06: Platform Abstraction

- [ ] Cross-platform code uses `PlatformApi` traits → superseded by AC-RS-13.
- [ ] Conditional compilation uses `#[cfg(target_os)]` correctly → superseded by AC-RS-13.
- [ ] FFI boundaries include safety documentation → superseded by AC-RS-14.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Cross-language parent (AC-CL-*)](../01-cross-language/97-acceptance-criteria.md)
- [Naming conventions](./01-naming-conventions.md)
- [Error handling](./02-error-handling.md)
- [Async patterns](./03-async-patterns.md)
- [Memory safety](./04-memory-safety.md)
- [Testing standards](./05-testing-standards.md)
- [FFI & platform](./06-ffi-platform.md)
- [§02 parent governance](../97-acceptance-criteria.md)
- [TypeScript sibling](../02-typescript/97-acceptance-criteria.md)
- [Golang sibling](../03-golang/97-acceptance-criteria.md)
- [PHP sibling](../04-php/97-acceptance-criteria.md)

> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29d (extension of Task #29c).
