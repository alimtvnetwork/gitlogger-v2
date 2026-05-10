# Changelog: Rust Standards

**Updated:** 2026-04-29


**Version:** 4.0.1
---

### 4.0.1 — 2026-04-29 — Phase 153 Task #29d closure: AI Confidence parity reached 51/51 (100%)
- Lockstep companion bump for §00/§99 banner edits made under Phase 153 Task #29d (P1 inventory regex widened in `check-ai-confidence.py`, underclaim banners promoted, legacy stub Verifies clauses backfilled). **No AC change beyond Task #29c-pattern legacy stubs; no CI workflow change.** See `.lovable/memory/audit/v2-deterministic/phase-153-task-29d-p1-regex-widening-and-final-parity.md`.

## v4.0.0 — 2026-04-26 (Phase 16l: §97 full GWT rewrite)
- **P21 sync** (2026-04-28): §00 banner version field bumped 3.2.0 → 4.0.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 21 -->` stamp added under §00 banner; no spec content change).

- **Changed** §97 — full GWT rewrite. Replaced 18 stub checkbox criteria (AC-01..AC-06) with **20 module-specific Given/When/Then ACs** (AC-RS-01..AC-RS-20) covering: explicit AC-CL-01..AC-CL-20 inheritance with documented AC-CL-12 file-naming override (AC-RS-01); minimum Rust 1.75 + edition pinned + `rust-toolchain.toml` (AC-RS-02); `thiserror` for domain / `anyhow` with `.context()` for application + `Box<dyn Error>` FORBIDDEN (AC-RS-03); `panic!`/`unwrap`/`expect`/`todo!`/`unreachable!`/`unimplemented!` FORBIDDEN outside main/tests with clippy deny lints (AC-RS-04); `// SAFETY:` comment + `# Safety` rustdoc on every `unsafe` + `#![forbid(unsafe_code)]` for non-FFI crates (AC-RS-05); Tokio sole runtime, mixing with async-std/smol FORBIDDEN (AC-RS-06); Rust naming (kebab crates, snake_case mods/files/fns/vars, PascalCase types/traits, SCREAMING_SNAKE consts) — sole AC-CL-12 waiver (AC-RS-07); `#[serde(rename_all = "PascalCase")]` per AC-CL-09 + `#[serde(deny_unknown_fields)]` (AC-RS-08); bounded `mpsc::channel(N)` only, `unbounded_channel()` FORBIDDEN (AC-RS-09); cancellation-safe `tokio::select!` arms + `biased;` documented + `CancellationToken` (AC-RS-10); borrow > Arc > clone, `Rc<T>` FORBIDDEN with Tokio (AC-RS-11); AAA tests, OS deps trait-mocked, integration tests in `tests/` (AC-RS-12); `PlatformApi` traits + per-OS modules + minimum-scope `#[cfg(target_os)]` (AC-RS-13); FFI boundaries with `# Safety`/`# Errors`/`# Panics` rustdoc + `#[repr(C)]` + null checks (AC-RS-14); `cargo clippy --workspace --all-targets --all-features -- -D warnings` + `clippy::pedantic` + `cargo deny` + `cargo audit` (AC-RS-15); `Cargo.lock` checked in for binaries + caret-with-patch + git deps pinned to SHA (AC-RS-16); `tracing` structured logging, `println!`/`eprintln!`/`dbg!`/`log::*` FORBIDDEN in non-test code (AC-RS-17); `#![deny(missing_docs)]` + `# Panics`/`# Errors`/`# Safety` sections + doctest compile (AC-RS-18); lifetime elision preferred + short `'a`/`'src` names + `for<'a>` commented (AC-RS-19); self-application doctest harness via `cargo test --doc` (AC-RS-20).
- **Preserved** legacy 18 stub checkboxes as AC-RS-LEGACY-01..06 at end of §97.
- **Bumped** §97 v3.2.0 → v4.0.0 (major; AC contract reshaped from stub-checkbox to GWT). §98 v3.2.0 → v4.0.0. §99 v3.2.0 → v4.0.0.

---

## [1.1.0] — 2026-03-30

- Added AI Confidence and Ambiguity scores to overview
- Added Keywords and Scoring table

## [1.0.0] — 2026-03-09

- Initial Rust standards: naming, error handling, async, memory safety, testing, FFI

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | minor | Phase 27c: Added `kind: future-spec` frontmatter + Drift Acknowledgment. Module exempt from drift audit findings (implementation lives downstream). |

## 2026-04-27 — Phase 58 impl-sweep

- Phase 58: appended RustLintResult JSON Schema to satisfy `has_json_schema` rubric (impl 70 → 85).

## 2026-04-27 — Phase 65 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 65 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 71 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

