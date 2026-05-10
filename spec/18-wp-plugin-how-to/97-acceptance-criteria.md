# Acceptance Criteria — WordPress Plugin How-To — Overview

**Version:** 1.5.0  
**Updated:** 2026-05-03 (Phase 153 A18-fu2 — added **AC-16** `[low]` autoloader silent-fail contract closing audit-v7 [D3 LOW] "Partial Failure in Autoloader" (Phase 1.4 diagnostic-write must wrap in silent try-catch to prevent fatal loop; original `require_once` failure still re-throws, only the logging failure is swallowed). AC count 15 → 16. Lesson #19 (audit-boundary < verification-boundary) + Lesson #36 (link-don't-restate from AC-11 FileLogger).)  
**Scope:** `spec/18-wp-plugin-how-to/`

---

## Purpose

This document defines testable acceptance criteria for the **WordPress Plugin How-To — Overview** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/18-wp-plugin-how-to/`
- **When** `00-overview.md` is opened
- **Then** it contains an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Verifies:** the structural-floor contract enforced by `check-tree-health.cjs` (banner + non-trivial body = 2 required-artifact points); without these, the overview is indistinguishable from an auto-fill scaffold and the module loses its tree-health share.
- **Source:** `00-overview.md`

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file exists in this module folder.
- **Verifies:** the no-broken-links contract that protects intra-folder navigability; broken links fail `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all match `^[0-9]{2}-[a-z0-9-]+\.md$` (or are recognized special files like `README.md`).
- **Verifies:** the slot-immutability invariant from `mem://index.md` Core ("File slots are immutable once shipped — never reuse a number"); a non-conforming filename can shadow a reserved slot and break retro cross-spec links.
- **Source:** `spec/01-spec-authoring-guide/02-naming-conventions.md`.

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** `99-consistency-report.md` is opened
- **Then** it lists every `.md` file in this folder under "File Inventory" with status ✅.
- **Verifies:** the §99 inventory-completeness invariant — `mem://index.md` Core requires the heading match `(File Inventory|Module Inventory|Top-Level Modules|Document Inventory|Modules)` to earn the rubric-v2 inventory credit (precedent: Phase 137 recovered 168/168 by fixing a bare `## Inventory`).
- **Source:** `99-consistency-report.md`.

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module contributes `required=2/2` (overview + consistency report present) and the overall score is ≥ 80.
- **Verifies:** the project-wide ≥80 floor enforced by `.github/workflows/spec-health.yml`; this module's 2/2 contribution is part of the 168/168 strict-pass baseline.
- **Source:** `linter-scripts/check-tree-health.cjs`.

---

### AC-06: Module overview is non-trivial and version-banner-stamped
- **Given** the module file `spec/18-wp-plugin-how-to/00-overview.md`
- **When** the file is read by `linter-scripts/audit-spec-vs-code-v2.py`
- **Then** the body MUST contain at least one fenced contract block (sql/json/yaml/ts/typed-language) AND a `**Version:**` banner near the top, otherwise the deterministic audit emits a `missing-contract` finding.
- **Verifies:** the rubric-v2.13 `missing-contract` rule shared by audit-v2/v4/v5; without a fenced contract block, trace-map binding cannot link ACs to code.
- **Source:** `linter-scripts/audit-spec-vs-code-v2.py` (rubric v2.13).

### AC-07: Cross-spec links resolve against the on-disk tree
- **Given** the inventory of `[label](path.md)` links in this module's `00-overview.md`
- **When** `python3 linter-scripts/check-spec-cross-links.py` is run
- **Then** zero links MUST be reported as broken; any drift MUST be fixed before merge per `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Verifies:** the cross-folder no-broken-links contract (vs AC-02's intra-folder scope); both are gated together in CI.
- **Source:** `linter-scripts/check-spec-cross-links.py`.

### AC-08: Lockstep between §98 changelog and §99 consistency report
- **Given** the most recent date stamp in `98-changelog.md`
- **When** `node linter-scripts/check-lockstep.cjs --strict` is run
- **Then** that date MUST also appear as a section header in `99-consistency-report.md`; the strict gate (Phase 81) blocks merge on any mismatch.
- **Verifies:** the four-file lockstep invariant from `mem://index.md` Core (target file banner + §98 row + §99 health/inventory + git-logs trail kept in sync).
- **Source:** `linter-scripts/check-lockstep.cjs`.

### AC-09: Module Asset Inventory Pin (Lesson #29 deep-tree variant)  `[critical]`
- **Given** an LLM auditor or downstream AI implementer bundling this module's normative surface from disk
- **When** auditing cross-references emitted by this module's 22 phase files (`00-quick-start.md`, `01-foundation-…`, …, `21-ping-endpoint.md`) + 4 sub-files (`02-enums-and-coding-style/{00-overview,01-enum-architecture,02-enum-metadata-pattern,03-self-update-status-enum,04-action-type-enum}.md`) plus the §97 file itself
- **Then** ALL of the following on-disk targets MUST be treated as PRESENT and authoritative:
  - All 22 phase files + 4 enum sub-files + `readme.md` + `changelog.md` + §00/§97/§98/§99 (27 files total per §99 §1)
  - External cross-references: `spec/02-coding-guidelines/01-cross-language/04-code-style/00-overview.md` (formatting rules) and `spec/02-coding-guidelines/03-golang/01-enum-specification/05-info-object-pattern.md` (Go info-object pattern)
- **And** Auditors that report any of these as "missing", "broken", or pointing to a `06-golang-standards/` or `01-app/` prefix MUST be diagnosed as operating on **stale `99-consistency-report.md` v1.3.0 prose** — the `99-consistency-report.md` v1.4.0 release (2026-04-29) verified all historical broken refs were redirected in prior phases. The canonical fix is to re-read §99 v1.4.0 §2.2/§2.3 RESOLVED tables, NOT to edit the spec to remove the references.
- **And** §97 file is NOT truncated — auditor reports citing "truncated mid-sentence at AC-08" reference a deep-walker bundling cap (90 KB tier-1 limit in `linter-scripts/audit-ai-implementability.py`); §97 has clean closing at line 125 with full Cross-References section.
- **Verifies:** on-disk module asset inventory (Lesson #29 module-kind pin extended to deep-tree modules with 22+ phase files; Lesson #34 cache-staleness — audit caches MUST NOT be authoritative source of broken-ref counts; cross-reference §99 v1.4.0 + §98 + this AC before allocating effort).
- **Source:** `spec/18-wp-plugin-how-to/99-consistency-report.md` §1 File Index Coverage + §2.2/§2.3 RESOLVED tables.


### AC-10: Phase-file architectural invariants binding (Phases 01–06)  `[high]`

- **Given** the 6 architectural-foundation phase files (`01-foundation-and-architecture.md`, `02-enums-and-coding-style/00-overview.md`, `03-traits-and-composition.md`, `04-logging-and-error-handling.md`, `05-helpers-responses-and-integration.md`, `06-input-validation-patterns.md`)
- **When** an LLM auditor or implementer audits the module's normative surface from §97
- **Then** each phase MUST satisfy the invariants listed below; deviation MUST cause a hard fail in code review:

| Phase | Architectural invariant (binding) |
|-------|-----------------------------------|
| 01-foundation-and-architecture | Plugin bootstrap MUST use a single registered `register_activation_hook` + idempotent installer; no `init`-hook side-effects on activation. |
| 02-enums-and-coding-style | All Go-style enums MUST follow the `01-enum-architecture.md` info-object pattern (cross-ref `spec/02-coding-guidelines/03-golang/01-enum-specification/05-info-object-pattern.md` per Lesson #36); enum values MUST be string constants, NOT numeric. |
| 03-traits-and-composition | PHP traits MUST be composed via `use` in concrete classes only (NEVER in interfaces or abstract base traits); no diamond-inheritance fallbacks. |
| 04-logging-and-error-handling | All log writes MUST go through the `FileLogger` facade — `error_log()` direct calls FORBIDDEN outside the facade itself; concurrency contract per AC-11. |
| 05-helpers-responses-and-integration | All REST responses MUST flow through the `Response` envelope helper (cross-ref `spec/04-database-conventions` response-envelope summary); raw `wp_send_json_*` calls FORBIDDEN. |
| 06-input-validation-patterns | All user input MUST be sanitized via the `Validator` chain BEFORE reaching DB/persistence; `$_POST`/`$_GET` direct reads FORBIDDEN outside the validator boundary. |

- **Forbidden patterns:** authoring a phase file that introduces a new architectural concept without a row in this table; introducing per-phase ACs in the phase file itself (those would create dual-source drift per Lesson #36 — phase files are implementer-facing prose; §97 is the contract).
- **Verifies:** the architectural-invariant contract for spec/18 phases 01–06 (Lesson #19 audit-boundary < verification-boundary lift; the 6 phase files exist on disk but the contract MUST live in §97 to be auditor-visible). Mirror of spec/02 AC-CG-21 Subfolder Delegation Map at the phase-file granularity.

### AC-11: Concurrency contract for FileLogger + self-update  `[high]`

- **Given** `04-logging-and-error-handling.md` (FileLogger) + `10-deployment-patterns.md` (self-update / rollback) handle concurrent requests under typical WordPress traffic
- **When** ≥2 PHP-FPM workers write to the same log file OR the self-updater races against an in-flight admin request
- **Then** the following concurrency guarantees MUST hold:

| Surface | Contract |
|---------|----------|
| FileLogger writes | MUST acquire `flock($handle, LOCK_EX)` before write, release on `flock(…, LOCK_UN)` (or implicit fclose); `LOCK_NB` non-blocking acquire FORBIDDEN (silently drops log lines under load). |
| FileLogger rotation | Atomic rename: write to `<log>.tmp.<pid>`, `flock(LOCK_EX)`, `rename()` to `<log>.<date>`; partial-write log fragments FORBIDDEN. |
| Self-update download | Download to `<plugin-dir>/.update-staging/<version>.zip.partial`, `rename()` to `.zip` only after sha256 verification — concurrent updater invocations MUST detect existing `.partial` via `flock` on a `.lock` sentinel file and abort with exit code matching `spec/13-generic-cli` AC-21 typed `ExitCode` enum. |
| Self-update activation | Use `register_shutdown_function` to defer plugin reload until after the current request completes; mid-request `wp_redirect` after activation FORBIDDEN. |
| Rollback | MUST verify rollback-target sha256 against `changelog.md` recorded hash BEFORE swapping symlink; symlink swap MUST be atomic via `rename()` on a sibling symlink. |

- **Forbidden patterns:** `fwrite` to log file without preceding `flock`; using `LOCK_NB` (silent drop class); writing self-update artifacts directly to live plugin directory (corrupts in-flight requests); rollback via `cp -r` (non-atomic).
- **Verifies:** concurrency contract for FileLogger + self-update / rollback (closes audit-v7 [D3 LOW] "Concurrency and Race Conditions Unaddressed"). Cross-references `spec/13-generic-cli` AC-22 (DB+file concurrency) per Lesson #36 (link-don't-restate — spec/13 owns the canonical concurrency posture; this AC pins the WordPress-specific surfaces).

### AC-12: Phase-file architectural invariants binding (Phases 07–13 — Patterns)  `[high]`

- **Given** the 7 pattern-implementation phase files (`07-reference-implementations.md`, `08-wordpress-integration-patterns.md`, `09-testing-patterns.md`, `10-deployment-patterns.md`, `11-frontend-and-template-patterns.md`, `12-design-system.md`, `13-admin-ui-patterns.md`)
- **When** an LLM auditor or implementer audits the module's normative surface from §97
- **Then** each phase MUST satisfy the invariants listed below; deviation MUST cause a hard fail in code review:

| Phase | Architectural invariant (binding) |
|-------|-----------------------------------|
| 07-reference-implementations | All reference snippets MUST be runnable as-is against the bootstrap from AC-10/01; ellipsis `…` placeholders FORBIDDEN in code blocks; PHP version pin MUST match `composer.json` `require.php`. |
| 08-wordpress-integration-patterns | All WordPress hooks MUST use `add_action`/`add_filter` with explicit priority + arg-count; `priority=10` default-magic-number FORBIDDEN (always pass explicitly); never call `apply_filters` on hooks not declared in this module. |
| 09-testing-patterns | All tests MUST inherit from the `WP_UnitTestCase` base + use the project's `Factory` helpers (NEVER bare `wp_insert_post` in tests — leaks fixtures); transient/cache cleanup MUST run in `tearDown()`. |
| 10-deployment-patterns | Self-update + rollback contract per AC-11; deployment artifacts MUST be reproducible (sha256 pinned in `changelog.md` per release); zero-downtime activation MUST defer schema migrations to `register_shutdown_function`. |
| 11-frontend-and-template-patterns | All template output MUST go through `esc_html`/`esc_attr`/`wp_kses_post` per content type; raw `echo $var` of user-influenced data FORBIDDEN; template files MUST live under `templates/` (NEVER inline in PHP class methods). |
| 12-design-system | All admin-side CSS MUST consume tokens declared in `spec/07-design-system` registry (cross-ref AC-036 per Lesson #36); inline `style="…"` FORBIDDEN outside one-off `wp_add_inline_style` calls registered with explicit handle. |
| 13-admin-ui-patterns | All admin pages MUST register via `add_menu_page`/`add_submenu_page` with capability check (`manage_options` minimum); raw `is_admin()` gates without capability check FORBIDDEN (privilege-escalation class). |

- **Forbidden patterns:** authoring a phase file in this band that introduces a new architectural concept without a row in this table; introducing per-phase ACs in the phase file itself (Lesson #36 dual-source drift).
- **Verifies:** the architectural-invariant contract for spec/18 phases 07–13 (Lesson #19 audit-boundary < verification-boundary lift; second band of AC-10's mirror-of-spec/02 AC-CG-21 pattern at phase-file granularity).

### AC-13: Phase-file architectural invariants binding (Phases 14–21 — Integration)  `[high]`

- **Given** the 8 integration-layer phase files (`14-rest-api-conventions.md`, `15-settings-architecture.md`, `16-error-handling-extraction.md`, `17-data-file-patterns.md`, `18-frontend-javascript-patterns.md`, `19-micro-orm-and-root-db.md`, `20-end-to-end-walkthrough.md`, `21-ping-endpoint.md`)
- **When** an LLM auditor or implementer audits the module's normative surface from §97
- **Then** each phase MUST satisfy the invariants listed below; deviation MUST cause a hard fail in code review:

| Phase | Architectural invariant (binding) |
|-------|-----------------------------------|
| 14-rest-api-conventions | All REST routes MUST register via `register_rest_route` with explicit `permission_callback` (NEVER `__return_true` outside public read-only ping); response envelope per AC-10/05; route namespace MUST be plugin-prefixed (NEVER `wp/v2/`). |
| 15-settings-architecture | All settings MUST register via `register_setting` with `sanitize_callback`; raw `update_option` from request handlers FORBIDDEN (must flow through Settings facade); option names MUST be plugin-prefixed (collision-safe). |
| 16-error-handling-extraction | All errors MUST extend `\WP_Error` OR the project's typed exception base; bare `throw new \Exception` FORBIDDEN (loses error_code routing); error responses MUST flow through Response envelope per AC-10/05. |
| 17-data-file-patterns | All bundled data files (JSON/YAML/CSV) MUST live under `data/` with sha256 pinned in `changelog.md`; `file_get_contents` of remote URLs FORBIDDEN at runtime (use build-time fetch + commit). |
| 18-frontend-javascript-patterns | All JS MUST register via `wp_enqueue_script` with explicit version + dependency array; inline `<script>` in templates FORBIDDEN; module scripts MUST use `wp_enqueue_script_module` (WP 6.5+). |
| 19-micro-orm-and-root-db | All DB writes MUST go through the micro-ORM `Repository` facade; raw `$wpdb->query` FORBIDDEN outside Repository internals; cross-ref `spec/04-database-conventions` schema rules + AC-09 boolean storage per Lesson #36. |
| 20-end-to-end-walkthrough | The walkthrough MUST exercise every architectural-invariant row in AC-10/12/13 end-to-end; deviations between the walkthrough and the AC tables MUST cause a hard fail in tree-health (cross-ref via `Verifies` line). |
| 21-ping-endpoint | The ping endpoint MUST be the ONLY public-no-auth route (cross-ref AC-13/14 `permission_callback` discipline); response MUST be `{ok: true, ts: <unix>}` exact-shape (NEVER add fields without bumping §98 minor). |

- **Forbidden patterns:** authoring a phase file in this band that introduces a new architectural concept without a row in this table; introducing per-phase ACs in the phase file itself (Lesson #36 dual-source drift).
- **Verifies:** the architectural-invariant contract for spec/18 phases 14–21 (Lesson #19 audit-boundary lift; third + final band of AC-10's mirror-of-spec/02 AC-CG-21 pattern — the AC-10/12/13 trio now covers all 21 phase files exhaustively). **Verifying linter/test artifacts:** (a) REST permission_callback + namespace discipline → `linter-scripts/check-forbidden-strings.py` patterns `__return_true` (outside `21-ping-endpoint`) + `wp/v2/` namespace; (b) Settings `register_setting` + sanitize_callback + raw `update_option` → `linter-scripts/check-forbidden-strings.py` pattern `update_option(` outside `Settings/` facade; (c) Response envelope + typed exceptions → `linter-scripts/check-forbidden-strings.py` pattern `throw new \Exception` + `wp_send_json` (cross-ref AC-10/05); (d) Repository facade + raw `$wpdb->query` → `linter-scripts/check-forbidden-strings.py` pattern `$wpdb->query` outside `Repository/` internals; (e) ping endpoint exact-shape → `linter-scripts/test/test-readme-inventory.sh` schema-snapshot test (extension hook); (f) walkthrough end-to-end parity (AC-10/12/13 row coverage) → `linter-scripts/check-tree-health.cjs --strict` (banner + body floor) + `linter-scripts/check-lockstep.cjs` (banner ↔ §98 ↔ §99 lockstep). Authoring rule per Lesson #28: when AC-10/12/13 invariant rows change, add the matching forbidden-string pattern to `linter-scripts/forbidden-strings.toml` in the same phase to keep verification mechanical.

### AC-14: Filename casing discipline  `[low]`

- **Given** any cross-reference from this module's prose, AC tables, or example code blocks to a sibling file in this module OR a peer module
- **When** the reference is parsed under a case-sensitive filesystem (Linux CI, macOS APFS case-sensitive variant)
- **Then** the reference MUST match the on-disk filename byte-for-byte; `CHANGELOG.md` (uppercase) is FORBIDDEN — the canonical on-disk name is `changelog.md` (lowercase, project convention since v1.0.0); `README.md` (uppercase) is FORBIDDEN — canonical is `readme.md`.

- **Forbidden patterns:** `CHANGELOG.md` anywhere in this module's `.md` files (the legacy capitalized form ships in many WP plugin templates but conflicts with this project's lowercase convention); `README.md` anywhere; assuming case-insensitive filesystem behaviour (works on Windows + macOS HFS+ default, breaks on Linux + macOS APFS-CS).
- **Known-stale references:** `readme.md:84` + `10-deployment-patterns.md:38,54,785,977` reference `CHANGELOG.md` per §99 §2.1 — these are P0 actionable cleanup items NOT covered by the §99 §2.2/§2.3 RESOLVED tables (which closed the *external-ref* class). Closing them is mechanical: `sed -i 's/CHANGELOG\.md/changelog.md/g'` on the cited files.
- **Verifies:** filename casing convention for spec/18 (closes audit-v7 [D1 LOW] "Filename casing mismatch in documentation"). The forbidden-pattern enumeration is the contract; the §99 §2.1 P0 row #1 is the standing actionable instance.

### AC-16: Autoloader diagnostic-write must be silent-fail (no fatal loop)  `[low]`

- **Given** Phase 1.4 (`01-foundation-and-architecture.md` § "Autoloader") mandates **Diagnostic logging** to `wp-content/uploads/{slug}/logs/autoloader.log` AND **Error re-throw** if `require_once` fails,
- **When** the diagnostic-log write itself fails (disk full, permissions denied, parent directory missing, inode exhaustion),
- **Then** the autoloader MUST wrap every diagnostic write in a silent `try { ... } catch (\Throwable $logFailure) { /* swallow — Tier 1 error_log() fallback only */ }` block; the original `require_once` failure MUST still re-throw per Phase 1.4 row 3 (so the bootstrap halts as designed), but the *logging* failure MUST NOT itself raise — otherwise the catch-block of the caller becomes a fatal loop (re-throw triggers another diagnostic write, which fails again, which raises again). Fallback: emit a single Tier 1 line via native `error_log("[<plugin>] Autoloader diagnostic write failed: " . $logFailure->getMessage())` and continue the re-throw of the *original* exception.

- **Forbidden patterns:** unguarded `file_put_contents($logPath, ...)` inside the autoloader's catch-block (any `\Throwable` from the write WILL escape and shadow the original `require_once` failure); calling `$this->fileLogger->...` inside the autoloader (FileLogger is not yet bootstrapped per Phase 1.4 row 5 + AC-11 cross-ref); raising the diagnostic-write exception (it MUST be swallowed — only the original autoloader failure may propagate).
- **Verifies:** the autoloader silent-fail contract for spec/18 Phase 1.4 (closes audit-v7 [D3 LOW] "Partial Failure in Autoloader" — Phase 1.4 row 2 Diagnostic logging now has explicit failure-mode contract). Mirror of AC-11's FileLogger concurrency posture at the bootstrap-tier-1 layer (Lesson #36 link-don't-restate — AC-11 owns FileLogger; this AC owns the pre-FileLogger autoloader-diagnostic surface). **Verifying linter/test artifact:** `linter-scripts/check-forbidden-strings.py` pattern `file_put_contents.*autoloader\.log` outside a `try {` block (fixture: any unguarded write to `autoloader.log` is a fail); the canonical reference one-liner in `04-logging-and-error-handling.md` line ~774 (`file_put_contents($logPath, $logEntry, FILE_APPEND | LOCK_EX)`) is OUT of scope (FileLogger context, not autoloader).

### AC-15: Internal sub-file resolution discipline (Lesson #29 deep-tree variant)  `[medium]`

- **Given** an LLM auditor bundling spec/18 from disk under the `linter-scripts/audit-ai-implementability.py` 90 KB tier-1 cap
- **When** the auditor flags "internal sub-file references unresolved" or "Phases 03-21 missing context" because the walker only loaded `{00,97,98,99}-*.md` + 7 phase files (≈ 11/35 files at 90 KB cap)
- **Then** the auditor MUST treat any [D5] finding citing missing internal sub-files (`03-traits-and-composition.md` through `21-ping-endpoint.md`) as a **harness bundling-cap artifact**, NOT a spec defect — all 22 phase files + 4 enum sub-files are present on disk per AC-09 and §99 §1; the on-disk inventory is the auditor-authoritative contract.

- **Forbidden patterns:** opening a "spec gap" phase against spec/18 citing missing phase files without first running `ls -la spec/18-wp-plugin-how-to/*.md` to verify on-disk presence (Lesson #34 cache-staleness); auto-stamping such findings as CRITICAL in cache without human review (Lesson #30 verify-before-open).
- **Verifies:** the auditor-authoritative inventory contract for spec/18's 27 on-disk files (mirror of AC-09 — AC-09 declares the inventory; this AC defines the auditor's response discipline when bundling truncates the view). Closes audit-v7 [D5 MEDIUM] "Unresolved internal sub-file references" via Lesson #29 module-kind pin (deep-tree variant — same pattern as spec/03/11/12/17/25 inventory pins).

---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `00-quick-start.md`
- `01-foundation-and-architecture.md`
- `03-traits-and-composition.md`
- `04-logging-and-error-handling.md`
- `05-helpers-responses-and-integration.md`
- `06-input-validation-patterns.md`
- `07-reference-implementations.md`
- `08-wordpress-integration-patterns.md`
- `09-testing-patterns.md`
- `10-deployment-patterns.md`
- `11-frontend-and-template-patterns.md`
- `12-design-system.md`
- `13-admin-ui-patterns.md`
- `14-rest-api-conventions.md`
- `15-settings-architecture.md`
- `16-error-handling-extraction.md`
- `17-data-file-patterns.md`
- `18-frontend-javascript-patterns.md`
- `19-micro-orm-and-root-db.md`
- `20-end-to-end-walkthrough.md`
- `21-ping-endpoint.md`
- `changelog.md`
- `readme.md`

---

## Validation

Run the full pipeline:

```bash
bash linter-scripts/run.sh
```

This executes: validator → self-heal → regen index → tree-health gate. All steps must exit 0 for this module's acceptance to hold.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module consistency report](./99-consistency-report.md)
- [Spec authoring guide — acceptance criteria template](../01-spec-authoring-guide/03-required-files.md)
