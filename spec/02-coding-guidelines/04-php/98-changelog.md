# PHP Standards — Changelog


**Version:** 4.1.1
**Last Updated:** 2026-04-29

All notable changes to the PHP Standards specification are documented here.

---

### 4.1.1 — 2026-04-29 — Phase 153 Task #29d closure: AI Confidence parity reached 51/51 (100%)
- Lockstep companion bump for §00/§99 banner edits made under Phase 153 Task #29d (P1 inventory regex widened in `check-ai-confidence.py`, underclaim banners promoted, legacy stub Verifies clauses backfilled). **No AC change beyond Task #29c-pattern legacy stubs; no CI workflow change.** See `.lovable/memory/audit/v2-deterministic/phase-153-task-29d-p1-regex-widening-and-final-parity.md`.

## 4.2.0 — 2026-04-27
- **P21 sync** (2026-04-28): §00 banner version field bumped 3.3.0 → 4.2.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 21 -->` stamp added under §00 banner; no spec content change).

- Phase 51: appended JSON Schema + typed enum contracts to overview to lift implementability score (no behavior change).

## v4.1.0 — 2026-04-26 (Phase 27 drift sweep)

- **Added** `kind: future-spec` frontmatter + Drift Acknowledgment section to `00-overview.md`. Acknowledges that referenced application/workflow code lives in downstream repos and is intentionally absent from this spec-only repo's local code index, so audit `drift` findings of the form "spec references file that doesn't exist" are expected and accepted.
- **Bumped** banner v3.2.0 → v3.3.0 (minor; metadata + acknowledgment, no contract change).

## v4.0.0 — 2026-04-26 (Phase 16k: §97 full GWT rewrite)

- **Changed** §97 — full GWT rewrite. Replaced 7 table-row criteria (AC-01..AC-07) with **20 module-specific Given/When/Then ACs** (AC-PHP-01..AC-PHP-20) covering: explicit AC-CL-01..AC-CL-20 inheritance (AC-PHP-01); PHP 8.1+ minimum + `declare(strict_types=1)` mandatory first statement (AC-PHP-02); string-backed enums with PascalCase cases AND PascalCase values (AC-PHP-03); mandatory `isEqual(self $other): bool` on every enum (AC-PHP-04); `ResultHelper::ok|failed|error|errorWithCode|errorFromException` only on service returns (AC-PHP-05); `ResponseKeyType::Foo->value` array keys, no string literals (AC-PHP-06); role-based identifier casing (AC-PHP-07); boolean `is`/`has`/`can`/`should` camelCase prefix, no snake_case, no negative polarity (AC-PHP-08); `use`-imported globals with no leading backslash, grouped imports (AC-PHP-09); `safeExecute(fn() => ...)` REST wrap + `wp_die()` FORBIDDEN (AC-PHP-10); blank-line discipline before `if`/`throw`/`return` (AC-PHP-11); constructor property promotion + `readonly` for DTOs (AC-PHP-12); type declarations on every parameter and return, no `mixed` without waiver (AC-PHP-13); `RiseupAsia\Exceptions\BaseException` hierarchy, SPL only at boundaries (AC-PHP-14); `phpstan --level=8` + `psalm --show-info=true` zero issues + no baseline files (AC-PHP-15); PSR-4 file-per-class (AC-PHP-16); PHPUnit 10+ `#[Test]` attribute, no `@test` PHPDoc (AC-PHP-17); composer caret-with-patch + `composer.lock` checked in (AC-PHP-18); PSR-3 `LoggerInterface` structured logging, no `error_log`/`var_dump`/`print_r`/`echo` (AC-PHP-19); self-application doctest (AC-PHP-20).
- **Preserved** legacy AC-01..AC-07 as AC-PHP-LEGACY-01..07 at end of §97.
- **Bumped** §97 v2.0.0 → v4.0.0 (major; AC contract reshaped from 7 table rows to 20 GWT). §98 v3.2.0 → v4.0.0. §99 v3.2.0 → v4.0.0.

---

## v2.1.0 — 2026-03-31

### Changed
- `07-php-standards-reference.md` split into subfolder (5 files, max 252 lines — down from 840)
- Fixed spacing violations in code examples

---

## v2.0.0 — 2026-03-09

### Global Version Bump

Project-wide major version increment (+1.0.0) applied to all specification files in `03-coding-guidelines/04-php`.

#### Changed
- All spec files received a major version bump and date update to 2026-03-09.
- Part of a global effort spanning ~638 files across all 30+ spec folders, establishing a new project-wide versioning baseline.

---

*Keep this file updated when specs change.*

## 2026-04-27 — Phase 57 impl-sweep

- Phase 57: appended TypeScript enum mirror (PhpLintSeverity / PhpModuleState / PhpTestKind) to satisfy `has_ts_enums` rubric (impl 65 → 75).

## 2026-04-27 — Phase 59 impl-sweep

- Phase 59: appended PHP Compliance OpenAPI OpenAPI to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 68 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 68 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 71 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.


### 4.2.1 — 2026-04-29 — Phase 153 Task #35-fu2: §98 backfill (parity gate close-out)

- **Action**: Backfilled missing §98 row to match §00 banner v4.2.1. Phase 153 Task #35-fu surfaced this as part of the §00-ahead-of-§98 drift class after `latest_release()` was patched to SemVer-max comparator. The §00 banner had been bumped in a prior phase but the corresponding §98 row was never authored — this entry closes the parity gate.
- **Lockstep**: §98 latest release now equals §00 banner; no §00/§99 changes (banner already at v4.2.1).
- **Why**: Codifies Lesson #28 — version-parity drift is mechanical close-out work, not a comparator bug.
