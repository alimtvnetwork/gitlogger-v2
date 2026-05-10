# Acceptance Criteria — PowerShell Integration for Project Runner

**Version:** 1.5.0  
**Updated:** 2026-05-07 (Phase J2 — added **AC-14** `[critical]` Sibling File Delegation Map (Lesson #21 + Lesson #39 fifth instance, intra-module sibling-file axis); 13-row delegation table covering all sibling files; mirror of spec/22 AC-80 + spec/13 AC-27 + spec/04 AC-18 + spec/02 AC-CG-21. AC count 13 → 14.)  
**Scope:** `spec/11-powershell-integration/`

---

## Purpose

This document defines testable acceptance criteria for the **PowerShell Integration for Project Runner** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/11-powershell-integration/`
- **When** `00-overview.md` is opened
- **Then** it contains an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Source:** `00-overview.md`
- **Verifies:** §00 Module overview baseline (H1 + Version + Updated banner)

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file exists in this module folder.
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.
- **Verifies:** §00 cross-reference inventory; `linter-scripts/check-spec-cross-links.py`

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all match `^[0-9]{2}-[a-z0-9-]+\.md$` (or are recognized special files like `README.md`).
- **Source:** `spec/01-spec-authoring-guide/02-naming-conventions.md`.
- **Verifies:** `spec/01-spec-authoring-guide/02-naming-conventions.md` §Filename pattern

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** `99-consistency-report.md` is opened
- **Then** it lists every `.md` file in this folder under "File Inventory" with status ✅.
- **Source:** `99-consistency-report.md`.
- **Verifies:** §99 File Inventory rubric

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module contributes `required=2/2` (overview + consistency report present) and the overall score is ≥ 80.
- **Source:** `linter-scripts/check-tree-health.cjs`.
- **Verifies:** `linter-scripts/check-tree-health.cjs` §required=2/2 contribution

---

### AC-06: Module overview is non-trivial and version-banner-stamped
- **Given** the module file `spec/11-powershell-integration/00-overview.md`
- **When** the file is read by `linter-scripts/audit-spec-vs-code-v2.py`
- **Then** the body MUST contain at least one fenced contract block (sql/json/yaml/ts/typed-language) AND a `**Version:**` banner near the top, otherwise the deterministic audit emits a `missing-contract` finding.
- **Source:** `linter-scripts/audit-spec-vs-code-v2.py` (rubric v2.13).
- **Verifies:** `linter-scripts/audit-spec-vs-code-v2.py` rubric v2.13 (G-CON-01 contract gate)

### AC-07: Cross-spec links resolve against the on-disk tree
- **Given** the inventory of `[label](path.md)` links in this module's `00-overview.md`
- **When** `python3 linter-scripts/check-spec-cross-links.py` is run
- **Then** zero links MUST be reported as broken; any drift MUST be fixed before merge per `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Source:** `linter-scripts/check-spec-cross-links.py`.
- **Verifies:** `linter-scripts/check-spec-cross-links.py` §Phase 81 strict gate

### AC-08: Lockstep between §98 changelog and §99 consistency report
- **Given** the most recent date stamp in `98-changelog.md`
- **When** `node linter-scripts/check-lockstep.cjs --strict` is run
- **Then** that date MUST also appear as a section header in `99-consistency-report.md`; the strict gate (Phase 81) blocks merge on any mismatch.
- **Source:** `linter-scripts/check-lockstep.cjs`.
- **Verifies:** `linter-scripts/check-lockstep.cjs` §strict date+phase parity

### AC-09: Per-step pipeline contract with closed exit-code enumeration (Phase 153 P48-4)  `[critical]`
- **Given** the 5-stage pipeline declared in `00-overview.md` § "Pipeline Steps" (1 Git Pull → 2 Prerequisites → 3 pnpm Install → 4 Frontend Build → 5 Copy & Run) AND the existing `04-error-codes.md` top-level exit codes (`0..10`) and detailed `9500..9599` codes AND the pinned dependency toolchain in `07-runner-interface.md`,
- **When** any implementer authors or audits the PowerShell runner (`run.ps1`),
- **Then** the implementer MUST follow the **Per-Step Contract (Normative)** subsection in `00-overview.md` § "Pipeline Steps" — every step has an explicit (a) inputs row drawn from `powershell.json` + `Param()` flags, (b) outputs / side effects row, (c) success criteria row, (d) **disjoint** top exit-code subset from `{1..10}`, (e) cross-walk to the detailed `9500..9599` codes that map under that top code. Pre-flight (configuration) exit codes `{5, 6, 7}` apply BEFORE Step 1 and are NOT step-attributed. The runner MUST exit on the FIRST failing step (fail-fast — later steps MUST NOT execute). The runner MUST NOT (1) continue to step `N+1` after step `N` returned non-zero, (2) emit a top exit code outside `{0, 1..10}` without first extending the per-step contract table + shipping a §98 release row, (3) emit a detailed `9500..9599` code without ALSO setting the paired top exit code, (4) map a single top exit code to multiple steps (disjointness is load-bearing for unambiguous attribution from exit code alone), (5) treat `-SkipPull` / `-SkipBuild` / `-BuildOnly` as success without satisfying the additional success criteria for that step (e.g. `-BuildOnly` still requires copy success). This codifies the **Phase 153 P47-fu1 critical finding** "Pipeline Steps (1. Git Pull → 2. Prerequisites → 3. pnpm Install → 4. Build → 5. Run) — overview lists pipeline steps but provides no detailed contract for each step's expected behavior, inputs, outputs, or error handling". Mirrors `spec/02 AC-CG-21` Subfolder Delegation Map / `spec/23 AC-ADB-14` Polymorphic AppLink Resolution / `spec/27 AC-T-29` per-artifact AC delegation (Lessons #19/#21/#26/#33): when a contract surface lives implicitly across multiple sibling files, it is invisible to context-window-bounded auditors and to fresh implementers — the contract MUST be lifted into a single normative table on the entry-point document with closed-enumeration codes and forbidden patterns.
- **Source:** `00-overview.md` § "Pipeline Steps" → "Per-Step Contract (Normative)" (table + pre-flight codes + forbidden runtime patterns subsections).
- **Verifies:** `00-overview.md` § "Pipeline Steps" → "Per-Step Contract (Normative)" (5 step rows × 5 columns + 3 pre-flight rows + 5 forbidden patterns); `04-error-codes.md` § "Exit Codes" (top `0..10` band — paired with per-step rows); `04-error-codes.md` § "Detailed Error Codes" (`9500..9599` bands — paired with per-step rows); `07-runner-interface.md` (CLI `Param()` block + minimum dependency versions Go 1.22 / Node 20.11 / pnpm 9 referenced from Step 2 success criteria). Codifies **Lesson #34** "Multi-step pipeline contracts MUST lift the per-step inputs/outputs/success/exit-code contract to a single normative table on the entry-point document — fragmenting the contract across sibling files (steps in §00, exit codes in §04, deps in §07) is invisible to LLM auditors and fresh implementers; closed-enumeration top exit codes with disjoint per-step ownership is the canonical fix".

### AC-10: On-disk asset inventory pin (Phase 153 audit-v6 close-out)  `[critical]`
- **Given** this module ships **two non-`.md` normative assets** required by every implementer — (a) `templates/run.ps1` (855 lines, the canonical reference PowerShell runner that every consumer copies + adapts per `00-overview.md` § "Template vs. Project" and `01-template-vs-project-differences.md`); (b) `schemas/powershell.schema.json` (268 lines, the JSON Schema draft-07 contract for `powershell.json` referenced from `01-configuration-schema.md`),
- **When** any LLM auditor or fresh implementer reads this module via tier-1 contract files (`{00,97,98,99}-*.md`, 90 KB cap per `linter-scripts/audit-ai-implementability.py` walker contract — slot 34 v1.1.0 AC-34-09),
- **Then** the auditor MUST treat these two paths as **PRESENT on-disk acceptance surface** — NOT as missing-file findings. The deep-walker's tier-1 cap legitimately stops before reaching `templates/` and `schemas/` subfolders, so any `[D5] missing-file` or `[D5] broken-reference` finding citing `templates/run.ps1` or `schemas/powershell.schema.json` is a **harness false-positive** (auditor cannot see ≠ file does not exist). The implementer MUST verify presence via `ls spec/11-powershell-integration/templates/run.ps1 spec/11-powershell-integration/schemas/powershell.schema.json` (both exit 0 with non-zero byte-count). The implementer MUST NOT (1) re-author either asset from scratch — both are the canonical normative source; (2) treat their absence from `97-acceptance-criteria.md` § "Module-Specific Files" as a contract gap (that section enumerates `.md` acceptance surface only — non-`.md` assets are pinned HERE in AC-10); (3) cite either path as "aspirational" or "future-spec" (they are shipped, line-counted, and have been the implementation target since Phase 1). Mirrors `spec/25 AC-AI-09/10/11` audit-corpus pattern (Lesson #29): when a module's normative surface lives outside the LLM auditor's tier-1 reach, the entry-point contract MUST declare the asset inventory with line-anchored citations so harness misreadings are pre-emptively closed.
- **Source:** `00-overview.md` § "Template vs. Project"; `01-template-vs-project-differences.md`; `01-configuration-schema.md` (references `schemas/powershell.schema.json` `$schema` URI).
- **Verifies:** `templates/run.ps1` (855 lines, present 2026-04-29); `schemas/powershell.schema.json` (268 lines, present 2026-04-29); `templates/powershell.json` (canonical config exemplar, references the schema via `"$schema": "../schemas/powershell.schema.json"`). Codifies **Lesson #29** "Audit-corpus / asset-inventory misclassification — when a module's normative surface lives outside the LLM auditor's tier-1 contract-file reach (templates/, schemas/, fixtures/, archived corpora), §97 MUST carry an explicit asset-inventory pin with on-disk path + line-count + auditor-treats-as-present declaration; mirror of AC-AI-09/10/11 for the asset-vs-prose axis".


---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `01-configuration-schema.md`
- `01-template-vs-project-differences.md`
- `02-script-reference.md`
- `03-integration-guide.md`
- `04-error-codes.md`
- `05-firewall-rules.md`
- `06-php-known-issues.md`
- `25-multi-site-deployment.md`
- `changelog.md`
- `parallel-work-sync-output.md`
- `readme.md`

---

## Validation

Run the full pipeline:

```bash
bash linter-scripts/run.sh
```

This executes: validator → self-heal → regen index → tree-health gate. All steps must exit 0 for this module's acceptance to hold.

---

### AC-11: Shared pnpm store concurrency contract (Phase 153 A18-fu1 #3)  `[high]`
- **Given** multiple `run.ps1` instances may execute concurrently on the same workstation (parallel CI runners, developer multi-project workflow, `-uas` multi-site deployment) AND `pnpm` resolves to a single shared content-addressable store at `$env:PNPM_HOME\store` (or `$HOME\.local\share\pnpm\store` on POSIX-mode pwsh) by default,
- **When** Step 3 ("pnpm Install") runs OR any maintenance flag triggers `pnpm store prune` / `Remove-Item -Recurse -Force` against the shared store path,
- **Then** the runner MUST observe the following concurrency contract: (a) **Read/install paths are safe by design** — pnpm's content-addressable store uses atomic hardlink writes keyed by content hash; concurrent `pnpm install` from N runners is supported and MUST NOT be serialized via external locks (doing so deadlocks against pnpm's internal store-lock). (b) **Destructive operations are NOT safe and MUST be gated** — before invoking `pnpm store prune`, `pnpm store path | Remove-Item -Recurse`, or any `-Force` clean of the store, the runner MUST (i) acquire an advisory lock at `$env:TEMP\pnpm-store-prune.lock` via `[System.IO.File]::Open($lockPath, 'CreateNew', 'Write', 'None')` (fails fast with `IOException` if another runner holds it); (ii) enumerate sibling `run.ps1` / `pnpm` processes via `Get-Process -Name pwsh,powershell,node | Where-Object { $_.Id -ne $PID -and $_.CommandLine -match 'run\.ps1|pnpm' }`; (iii) if ANY sibling is detected, SKIP the prune (emit warning, exit step with code 0 — non-fatal) rather than corrupt an in-flight install; (iv) on lock acquisition success + zero siblings, perform the prune, then `$lock.Dispose()` + `Remove-Item $lockPath`. (c) **Lock file lifetime is the prune operation only** — the runner MUST NOT hold the lock across `pnpm install` (it is needed only during destructive ops). (d) **Lock path is workstation-scoped, NOT repo-scoped** — the shared store is per-user, so the lock MUST live at `$env:TEMP` (or `/tmp` on POSIX), never inside any project tree. The runner MUST NOT (1) wrap `pnpm install` in any external mutex/flock (deadlocks pnpm's internal locking); (2) silently overwrite the lock file (use `CreateNew` mode, fail on collision); (3) leave a stale lock on `Ctrl+C` — wire `try { … } finally { $lock?.Dispose(); Remove-Item $lockPath -ErrorAction SilentlyContinue }`; (4) treat lock-acquisition failure as a hard error (it means a peer is doing maintenance — skip is correct); (5) prune the store from inside Step 3 of the canonical pipeline (prune is a maintenance command, not a build step — invoke from a separate `-MaintenanceMode` flag never bound to default `run.ps1` execution). Mirror of `spec/13 AC-22` (SQLite `busy_timeout`+retry+`update.lock`) and `spec/27 AC-T-28 R3` (atomic temp-then-rename + lock discipline) per Lesson #36 (link-don't-restate the cross-engine concurrency primitives, but lift the pnpm-specific surface here because PowerShell + pnpm + content-addressable-store is a distinct invariant set not covered by the SQLite contracts).
- **Source:** `00-overview.md` § "Pipeline Steps" Step 3; `02-script-reference.md` § "Maintenance Flags" (forthcoming `-MaintenanceMode` row to be added when AC-13's upload-script gap closes).
- **Verifies:** `templates/run.ps1` Step 3 invocation surface (read-safe concurrent installs); `00-overview.md` § "Per-Step Contract (Normative)" Step 3 row (success criteria extended to "concurrent installs from sibling runners do NOT corrupt the shared store"); `parallel-work-sync-output.md` (the `-uas` parallel-job pattern is the primary multi-runner trigger). Codifies the **Phase 153 A18-fu1 #3 audit-v7 D3 HIGH "Concurrency Race Condition in Shared Store"** finding into a closed-enumeration normative contract per Lesson #36 (cross-module link to `spec/13 AC-22` + `spec/27 AC-T-28`) + Lesson #40 triplet pattern (D3 HIGH + D2 MED + D5 LOW closed in single phase).

### AC-12: Indexed parallel job result ordering + null-return recovery (Phase 153 A18-fu1 #3)  `[medium]`
- **Given** the `-uas` (multi-site upload all) flag fans out N×M background jobs (N sites × M plugins) via `Start-Job` per the canonical pattern in `parallel-work-sync-output.md` § "Indexed Result Array Pattern",
- **When** all jobs complete (success, failure, or null-return on `Receive-Job`),
- **Then** the runner MUST satisfy: (a) **Output is indexed, not appended** — every job MUST be allocated a slot in a pre-sized `[System.Collections.ArrayList]` keyed by `$jobIndex` (sequential allocation BEFORE `Start-Job` calls), and result-write MUST go to `$results[$Index]`, never `$results.Add(...)` from inside the job (race condition on ArrayList resize). (b) **Final summary table MUST be sorted by `Index` ascending**, NOT by completion order — fresh implementers MUST `$results | Sort-Object Index | Format-Table` before any user-facing render. (c) **Null returns from `Receive-Job` MUST be handled gracefully** — when a job crashes mid-run (PowerShell process exit, SIGKILL, OOM), `Receive-Job` returns `$null` for that slot; the consumer MUST treat null as `Status = 'CRASHED'` + `ExitCode = -1` + `Error = 'Job returned null (process likely terminated)'` rather than throwing on `.Status` property access. (d) **Pre-allocated slot MUST persist** even on null-return so the index→site/plugin mapping survives — never `$results.RemoveAt($i)` on null. The runner MUST NOT (1) emit results in completion order without explicit Sort-Object Index (visually misleads the operator about which site failed); (2) use `$results += @{...}` from inside `Start-Job -ScriptBlock` (concurrent append on shared collection is a documented PowerShell race); (3) treat a null `Receive-Job` as success (it indicates abnormal termination); (4) reuse `$jobIndex` across the outer foreach loop without capturing into `$currentIndex = $jobIndex` BEFORE the closure (closure-over-loop-variable bug — all jobs see final value).
- **Source:** `parallel-work-sync-output.md` § "Indexed Result Array Pattern" + § "Job Execution"; `02-script-reference.md` (`-uas` flag row).
- **Verifies:** `parallel-work-sync-output.md` (existing pattern doc — this AC pins it as normative contract, not just illustrative); `templates/run.ps1` (when it implements `-uas`, MUST follow this contract). Codifies the **Phase 153 A18-fu1 #3 audit-v7 D2 MEDIUM "Missing AC for Multi-Site Parallelism"** finding per Lesson #19 (audit-boundary < verification-boundary — the implementation pattern existed in a sibling file but was never bound from §97; lifting it here makes it visible to context-bounded auditors and fresh implementers).

### AC-13: Downstream upload-script reference disambiguation (Phase 153 A18-fu1 #3)  `[low]`
- **Given** `02-script-reference.md` § "Script Version" header + `03-integration-guide.md` cite `upload-plugin-v2.ps1` (v2.1.0) and `upload-plugin-U-Q.ps1` (v1.1.0) as active components, AND `00-overview.md` § "Tree" lists `01-upload-plugin-v1.md` … `04-upload-plugin-custom.md` as **documentation files** (not the scripts themselves),
- **When** any LLM auditor or fresh implementer searches for `upload-plugin-v2.ps1` / `upload-plugin-U-Q.ps1` on disk and finds zero matches under `spec/11-powershell-integration/`,
- **Then** the implementer MUST treat both scripts as **downstream-repo assets** — they live in the consumer project's `wp-plugins/scripts/` folder per the per-project bootstrap pattern in `01-template-vs-project-differences.md`, NOT in this spec-only repo. The auditor MUST treat any `[D5] missing-file` finding citing `upload-plugin-v2.ps1` or `upload-plugin-U-Q.ps1` as a **harness misclassification** (mirror of Lesson #29 + spec/22 AC-78 / spec/03 AC-11 downstream-pin pattern). The shipped on-disk normative surface for upload-script behavior is: (a) `templates/run.ps1` (855 lines) — the canonical reference invocation harness; (b) `templates/powershell.json` — the canonical config schema consumers populate with `wpPlugins` block; (c) `02-script-reference.md` + `03-integration-guide.md` — the Param() flag contract + integration walkthrough. The implementer MUST NOT (1) author replacement upload scripts inside this spec repo (downstream concern); (2) treat the version banners (`upload-plugin-v2.ps1 2.1.0`) as a contract this repo enforces — they are version-pin advisories for downstream maintainers; (3) cite either path as "missing" in any spec-vs-code drift report. Per Lesson #36, the canonical cross-reference is to the consumer project's `wp-plugins/scripts/` tree (path is configurable per `powershell.json` `wpPlugins` block), NOT a fixed in-repo path.
- **Source:** `00-overview.md` § "Tree"; `01-template-vs-project-differences.md` § "Dependencies" row; `02-script-reference.md` § "Script Version" header; `03-integration-guide.md` § "Script Version" header.
- **Verifies:** `templates/run.ps1` (present, 855 lines — the in-repo canonical invocation harness); `templates/powershell.json` (present — schema instance); `01-upload-plugin-v[1-3].md` + `04-upload-plugin-custom.md` (DOCUMENTATION files for the downstream scripts, present on disk per §99 inventory). Codifies the **Phase 153 A18-fu1 #3 audit-v7 D5 LOW "Unresolved External Script References"** finding as a downstream-repo classification per Lesson #29 + Lesson #36 (mirror of spec/03 AC-11 downstream-pin AC; spec/22 AC-78 inventory pin).

### AC-14: Sibling File Delegation Map (Lesson #21 + Lesson #39 — intra-module audit-boundary pin for 13 sibling files)  `[critical]`
- **Given** spec/11-powershell-integration contains 13 normative sibling files outside the tier-1 audit bundle (`{00,97,98,99}-*.md`) — per AC-34-09, the auditor's tier-1 walker (~90 KB cap) does NOT see these files unless their normative content is explicitly bound from §97; AND a binding-density survey (`grep -c "<file>" 97-acceptance-criteria.md` per file, 2026-05-07) found 4 files with ≤1 §97 binding citation (`05-firewall-rules.md`, `06-php-known-issues.md`, `25-multi-site-deployment.md`, `readme.md`) — textbook Lesson #21 audit-boundary < verification-boundary gap; AND this is the **Lesson #39 fifth instance** (intra-module sibling-file axis), mirror of spec/22 AC-80 (33 siblings) + spec/13 AC-27 (20 siblings) + spec/04 AC-18 (8 siblings) + spec/02 AC-CG-21 (16 cross-language sub-folders);
- **When** an AI auditor walks spec/11 §97 and asks "for each sibling file in this module, which §97 AC governs it?" OR a downstream contributor opens any sibling file and asks "what §97 AC must I keep this file consistent with?",
- **Then** the table below MUST provide the canonical delegation — every sibling file maps to (a) its content kind, (b) the §97 AC family that governs it, (c) walker-tier visibility, (d) restatement-forbidden status per Lesson #36:

| Sibling file | Content kind | Governing §97 AC family | Tier visibility | Restate-in-§97 forbidden? |
|---|---|---|---|---|
| `01-configuration-schema.md` | normative-config | AC-01..AC-05 (overview) + downstream of AC-09 (per-step inputs) | tier-2 (walker-invisible) | YES (link to file, never inline schema) |
| `01-template-vs-project-differences.md` | normative-bootstrap | AC-11 (pnpm store paths) + AC-13 (downstream classification) | tier-2 | YES |
| `02-script-reference.md` | normative-flag-contract | AC-09 (Per-Step Contract) + AC-11 (`-MaintenanceMode`) + AC-13 (Script Version header) | tier-2 | YES (Param() flag table is canonical) |
| `03-integration-guide.md` | normative-walkthrough | AC-09 (pipeline steps) + AC-13 (Script Version) | tier-2 | YES |
| `04-error-codes.md` | normative-exit-codes | AC-09 (`{1..10}` + `9500..9599` cross-walk) | tier-2 | YES (full code table is canonical) |
| `05-firewall-rules.md` | normative-environment | AC-09 (pre-flight `{5,6,7}` codes) | tier-2 | YES (governed-but-unnamed prior to this AC) |
| `06-php-known-issues.md` | normative-edge-cases | AC-09 (Step 4 build edge cases) | tier-2 | YES (governed-but-unnamed prior to this AC) |
| `07-runner-interface.md` | normative-interface-contract | AC-09 (Per-Step Contract surface) | tier-2 | YES |
| `25-multi-site-deployment.md` | normative-deployment | AC-12 (`-uas` indexed parallelism) + AC-11 (pnpm store concurrency) | tier-2 | YES (governed-but-unnamed prior to this AC) |
| `parallel-work-sync-output.md` | normative-pattern | AC-12 (Indexed Result Array Pattern) + AC-11 (multi-runner trigger) | tier-2 | YES (lifted from illustrative to normative by AC-12) |
| `lifecycle-powershell-bootstrap-flow.mmd` | normative-diagram | AC-09 (pipeline steps Mermaid) | tier-2 | YES (diagram is canonical, prose MUST link) |
| `readme.md` | informative | (none — module entry pointer only) | tier-2 | informative-exempt |
| `changelog.md` | historical-trail | (none — superseded by §98 canonical changelog) | tier-2 | informative-exempt (legacy artifact, do NOT add new rows) |

**AND** all 13 sibling files are now GOVERNED-BY-NAME or explicitly informative-exempt (mirror of spec/13 AC-27's "no governed-but-unnamed" property; promotes the 4 previously low-binding files — `05-firewall-rules.md`, `06-php-known-issues.md`, `25-multi-site-deployment.md`, plus the unnumbered `parallel-work-sync-output.md` + `lifecycle-powershell-bootstrap-flow.mmd` — to explicit AC bindings).

**AND** the 2 informative-exempt rows (`readme.md`, `changelog.md`) MUST NOT accrue normative content — any new pipeline-behavior, error-code, or schema rule MUST land in a numbered sibling under the appropriate AC family, never in `readme.md` (entry pointer) or `changelog.md` (superseded by §98). An auditor finding new normative prose in either exempt file MUST flag it as a Lesson #25 dual-source drift (the §98 changelog is the single source of truth for chronological trail).

**AND** the table is **append-only within a phase** (rows MAY be added when new sibling files ship, never reworded; the "Governing §97 AC family" cell may be updated when an AC family number changes via §97-WINS evolution but the file's content kind is immutable per Lesson #25).

- **Source:** All 13 sibling files in `spec/11-powershell-integration/` (per `ls *.md *.mmd` survey 2026-05-07 excluding tier-1 `{00,97,98,99}-*.md`); §97 AC-01..AC-13 binding density survey.
- **Verifies:** intra-module audit-boundary pin (Lesson #21 sibling-file axis / Lesson #39 fifth instance); promotes 4 low-binding files (`05-firewall-rules.md`, `06-php-known-issues.md`, `25-multi-site-deployment.md`, `readme.md`) and 2 unnumbered files (`parallel-work-sync-output.md`, `lifecycle-powershell-bootstrap-flow.mmd`) from "governed-but-unnamed" / "unbound" to explicit §97 AC binding by name. Mirror of spec/22 AC-80 + spec/13 AC-27 + spec/04 AC-18 + spec/02 AC-CG-21 per Lesson #21 cross-language + intra-module dual-axis pattern.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module consistency report](./99-consistency-report.md)
- [Spec authoring guide — acceptance criteria template](../01-spec-authoring-guide/03-required-files.md)
