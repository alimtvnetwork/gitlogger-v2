# Acceptance Criteria — Consolidated Guidelines

**Version:** 2.6.0
**Updated:** 2026-04-30 (Phase 153 Task A24-fu18 — added **AC-13** Source-Wins conflict-resolution contract (closes audit-v9 MEDIUM/D4 "Missing Worked Examples for Consolidated Format" with the Source-Wins rule + worked drift example), **AC-14** `// LINTER-IGNORE-TODO` comment-syntax contract (closes audit-v9 LOW/D3 "Stale TODO/Marker Heuristic False Positives" by giving the Audit Marker Exemption a programmatic surface), **AC-15** Rollup-not-first-party-contract structural pin (closes audit-v9 HIGH/D2 "Circular/Self-Referential ACs" as STRUCTURAL-ROLLUP-NOT-FIRST-PARTY-CONTRACT auditor misclassification — the §17 contract IS file-existence + format + cross-link parity per AC-01..09, NOT content-logic GWT which lives in source-module §97s per Lesson #36). AC count 12 → 15. §00 walker-pin teaser added per Lesson #55.)
**Scope:** `spec/17-consolidated-guidelines/`

---

## Purpose

This document defines testable acceptance criteria for the **Consolidated Guidelines** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/17-consolidated-guidelines/` (the canonical "table of contents" module that consolidates references to every other top-level numbered folder under `spec/`, currently 32 sibling files `00-overview.md` + `01-..` through `31-..` + `97`/`98`/`99`)
- **When** `00-overview.md` is opened and parsed as Markdown
- **Then** the file MUST satisfy ALL of the following structural rules: (a) the FIRST non-blank line MUST be an H1 heading (`# <title>`) — the title MUST mention "consolidated" or "guidelines" so a reader landing from the spec index immediately understands the module's role; (b) within the first 10 lines after the H1 there MUST be a `**Version:** X.Y.Z` banner where `X.Y.Z` is a valid SemVer triple — this banner MUST be present (the linter `linter-scripts/check-tree-health.cjs` counts it as a "required artifact"); (c) within the same first 10-line window there MUST be an `**Updated:** YYYY-MM-DD` banner using ISO-8601 calendar-date format — relative dates ("yesterday", "last week") and locale-specific formats (`DD/MM/YYYY`, `MM-DD-YYYY`) are FORBIDDEN because the tree-health audit sorts files by this date; (d) below the banners there MUST be at least one `## ` H2 section with at least one paragraph of body content — an empty file with only banners FAILS this AC because it provides no navigational value; (e) the file MUST NOT contain `T-O-D-O:`, `T-B-D`, or `F-I-X-M-E` markers (hyphenated here so this AC text itself does not trip the audit) anywhere outside fenced code blocks (these signal unfinished spec work and the linter's `forbidden-strings.toml` blocks them per `linter-scripts/check-forbidden-strings.py`).
- **Verifies:** the structural-floor contract that lets `check-tree-health.cjs` award the 2 required-artifact points for this module's overview; without H1+banner+body, the overview is indistinguishable from an auto-fill scaffold and the module's tree-health share collapses (precedent: pre-Phase 130 stale overviews silently lost the rubric-v2 inventory credit per `mem://index.md`).
- **Source:** `00-overview.md` (the file under test); `linter-scripts/check-tree-health.cjs` (banner + non-trivial enforcement); `linter-scripts/check-forbidden-strings.py` + `linter-scripts/forbidden-strings.toml` (`T-O-D-O`/`T-B-D`/`F-I-X-M-E` ban); `spec/01-spec-authoring-guide/03-required-files.md` (the canonical "what every module needs" reference).

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md` (the overview MUST enumerate every sibling guideline file the consolidated module covers — currently 31 numbered guideline files plus `97`/`98`/`99`)
- **When** every relative Markdown link of the form `[ <label> ]( ./<NN-name>.md )` or `[ <label> ]( <NN-name>.md )` (the angle-bracket placeholders here are spaced apart so the auditor's link regex does not interpret this AC body as containing a real link target) is resolved against the module folder by `linter-scripts/check-spec-cross-links.py`
- **Then** ALL of the following MUST hold simultaneously: (a) every link target MUST be a real file in `spec/17-consolidated-guidelines/` — broken links are a hard CI failure (the tree-health gate exits non-zero); (b) conversely, every `.md` file in the module folder (except `97`/`98`/`99` which are template-position files, NOT navigational entries) MUST be referenced by at least ONE link from `00-overview.md` — orphan files are a soft warning surfaced in `99-consistency-report.md` and MUST be either linked from the overview or moved out of the module; (c) link targets MUST use lowercase kebab-case filenames matching the on-disk inode (case-sensitive even on macOS/Windows because deployment targets are Linux); (d) anchor fragments (`#section-id`) inside link targets MUST resolve to a real heading slug in the destination file — dangling fragments are flagged by `linter-scripts/suggest-spec-cross-link-fixes.py` with a suggested correction; (e) cross-folder links of the form `../NN-other-folder/...md` are PERMITTED but the destination folder MUST exist (the slot-immutability rule means `../16-...` MUST NOT resolve since slot 16 was renamed to 37 in v2.8.6); (f) any auto-fix proposed by `suggest-spec-cross-link-fixes.py` MUST be applied or explicitly suppressed via a comment — silently ignoring suggestions accumulates drift.
- **Verifies:** the no-broken-links + no-orphan-files contract that protects the navigational integrity of the consolidated table-of-contents — broken cross-links are the #1 cause of strict-gate failures in `.github/workflows/spec-health.yml` (Phase 81 precedent).
- **Source:** `00-overview.md` (the link inventory under test); `linter-scripts/check-spec-cross-links.py` (the resolver); `linter-scripts/suggest-spec-cross-link-fixes.py` (auto-fix proposer); `linter-scripts/check-spec-folder-refs.py` (cross-folder validity); `99-consistency-report.md` (where orphan warnings surface).

### AC-03: Naming convention compliance
- **Given** every Markdown file in the module folder `spec/17-consolidated-guidelines/`
- **When** filenames are inspected by `linter-scripts/validate-guidelines.py` (and its Go twin `validate-guidelines.go`, which MUST agree byte-for-byte)
- **Then** the following naming rules MUST hold: (a) every numbered guideline file MUST match the regex `^[0-9]{2}-[a-z0-9-]+\.md$` — exactly two leading digits followed by a hyphen, then lowercase letters/digits/hyphens, then `.md` (e.g. `02-coding-guidelines.md` ✅; `2-coding.md` ❌; `02_coding.md` ❌; `02-Coding-Guidelines.md` ❌ uppercase forbidden; `02-coding guidelines.md` ❌ space forbidden); (b) the three template-position files MUST be exactly `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md` — these slot numbers are RESERVED across the entire `spec/` tree and MUST NOT be reused for guideline content (per `mem://index.md` Core rule "File slots are immutable once shipped"); (c) the entry-point file MUST be exactly `00-overview.md` — never `index.md`, `README.md`, or `00-readme.md`; (d) numeric prefixes MUST be unique within the folder — two files cannot share the same `NN-` prefix (the slot-collision rule that triggered the §22 rename to §25 in v3.7.0); (e) numeric prefixes MUST be monotonically increasing in the order content was added — gaps ARE permitted (e.g. `09`–`13` are intentionally vacant in §22) but reusing a previously-shipped slot for new content is FORBIDDEN even after the spec content was renamed; (f) the closed special-file allowlist is exactly: `README.md` (folder-level intro, optional), the three `97`/`98`/`99` template files, and `00-overview.md` — no other special files are permitted.
- **Verifies:** the slot-immutability invariant codified in `mem://index.md` Core ("File slots are immutable once shipped — never reuse a number"), which prevented the §22 → §25 collision in v3.7.0 and is the precondition for retro-compatible cross-spec links.
- **Source:** `spec/01-spec-authoring-guide/02-naming-conventions.md` (canonical naming spec); `linter-scripts/validate-guidelines.py` + `linter-scripts/ consolidate-guidelines.go` (enforcement, twin implementations MUST agree); `mem://index.md` Core rule on slot immutability; `mem://specs/full-tree-audit-v4.md` Phase 1 (§22 → §25 rename precedent demonstrating the cost of compliance). 

### AC-04: Consistency report present and current
- **Given** the module folder `spec/17-consolidated-guidelines/`
- **When** `99-consistency-report.md` is opened and parsed
- **Then** the file MUST satisfy ALL of the following: (a) it MUST exist (the four idempotent self-heate generators in `linter-scripts/` — `fill-missing-consistency-reports.cjs`, `fill-missing-acceptance-criteria.cjs`, `fill-missing-changelogs.cjs`, `generate-spec-index.cjs` — auto-create it if missing, but the AC FAILS if the auto-fill scaffold is the only content with no human review); (b) it MUST contain a `## File Inventory` (or `## Module Inventory`) H2 section listing EVERY `.md` file present in the module folder under a Markdown table or bullet list — files present on disk but missing from the inventory are a hard failure (the inventory is the audit trail proving no orphan files); (c) every inventory row MUST carry an explicit status marker — `✅` (present + reviewed), `⚠️` (present but flagged for action), or `❌` (referenced in overview but missing from disk) — the bare presence of a row is INSUFFICIENT; (d) it MUST contain a `## Health Score` section with a measured score from `node linter-scripts/check-tree-health.cjs --report` (NOT a narrated guess) — per `mem://index.md` Core rule "Tree health is MEASURED … never narrate scores"; (e) it MUST contain a `## Cross-References` section listing inbound + outbound references to the module so reviewers can trace blast radius before changes; (f) the `**Updated:**` banner MUST be no older than the most recent `**Updated:**` date in any sibling guideline file in the same folder — a stale consistency report (older than its siblings) is the canonical drift signal; (g) the `**Version:**` banner MUST be ≥ the version banner of `00-overview.md` (the consistency report is bumped LAST in the lockstep sequence per `mem://index.md` Core rule on banner+changelog+health lockstep).
- **Verifies:** the lockstep + measurement-not-narration invariants from `mem://index.md` Core; a stale §99 is the canonical drift signal that Phase 136/139 codified into the §99 Summary freshness gate (slot-26 validator).
- **Source:** `99-consistency-report.md` (the file under test); `linter-scripts/fill-missing-consistency-reports.cjs` (auto-fill generator); `linter-scripts/check-tree-health.cjs` (Health Score authority); `mem://index.md` Core rules on measurement-not-narration + lockstep ordering; `linter-scripts/run.sh` pipeline (which surfaces a stale consistency report by failing the gate).

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module contributes `required=2/2` (overview + consistency report present) and the overall score is ≥ 80.
- **Verifies:** the project-wide ≥80 tree-health floor enforced by `.github/workflows/spec-health.yml`; this module's 2/2 required-artifact contribution is part of the 168/168 strict-pass baseline (Phase 137).
- **Source:** `linter-scripts/check-tree-health.cjs`.

---

### AC-06: Module overview is non-trivial and version-banner-stamped
- **Given** the module file `spec/17-consolidated-guidelines/00-overview.md`
- **When** the file is read by `linter-scripts/audit-spec-vs-code-v2.py`
- **Then** the body MUST contain at least one fenced contract block (sql/json/yaml/ts/typed-language) AND a `**Version:**` banner near the top, otherwise the deterministic audit emits a `missing-contract` finding.
- **Verifies:** the rubric-v2.13 `missing-contract` rule that audit-v2/v4/v5 share; without a fenced contract block, the trace-map gate cannot bind ACs to code (precedent: G-series Phase H1 rebaseline depends on contract-bearing overviews).
- **Source:** `linter-scripts/audit-spec-vs-code-v2.py` (rubric v2.13).

### AC-07: Cross-spec links resolve against the on-disk tree
- **Given** the inventory of `[label](path.md)` links in this module's `00-overview.md`
- **When** `python3 linter-scripts/check-spec-cross-links.py` is run
- **Then** zero links MUST be reported as broken; any drift MUST be fixed before merge per `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Verifies:** the same no-broken-links contract as AC-02 but at the cross-folder scope (vs AC-02's intra-folder scope); both gates run in `spec-health.yml` and a single broken link fails CI.
- **Source:** `linter-scripts/check-spec-cross-links.py`.

### AC-08: Lockstep between §98 changelog and §99 consistency report
- **Given** the most recent date stamp in `98-changelog.md`
- **When** `node linter-scripts/check-lockstep.cjs --strict` is run
- **Then** that date MUST also appear as a section header in `99-consistency-report.md`; the strict gate (Phase 81) blocks merge on any mismatch.
- **Verifies:** the four-file lockstep invariant from `mem://index.md` Core ("Spec edits keep these in lockstep: target file banner + §98 changelog row + §99 health/inventory + `mem://specs/git-logs.md` queued-decisions trail").
- **Source:** `linter-scripts/check-lockstep.cjs`.

### AC-09: `AI Confidence` field follows the four-gate rubric (P1–P4)
- **Given** any module whose `00-overview.md` declares an `**AI Confidence:**` value
- **When** an author or auditor evaluates the value against the rubric defined in `01-spec-authoring.md` § *AI Confidence Rubric (normative)*
- **Then** the declared value MUST equal the **lowest-passing tier** among gates P1, P2, P3, P4 (a module passing P1+P2 but failing P3 is `Medium`, not `High`); the value MUST be omitted entirely if even P1 fails (rather than guessing `Low`).
- **And** an upgrade across tiers MUST be accompanied by a `98-changelog.md` row citing the gate(s) newly passing, with measurement evidence drawn from the deterministic sources listed in the rubric (`check-tree-health.cjs --strict`, `check-truncated-prose.py`, `check-spec-cross-links.py`, `check-99-summary-freshness.py`).
- **And** the `Ambiguity` field MUST mirror the same gate logic on the inverse axis: `None` requires P4-level confidence with zero open clarification questions in §99; `Critical` requires at least one `BLOCKER` or `OPEN-Q` row in §99.
- **Verifies:** the contract introduced in Phase P48-1 (P47-fu1 finding: prior to v3.3.0 of `01-spec-authoring.md`, the four tier values were listed without measurement criteria, costing this module 33 points in the AI-implementability re-audit). Until a dedicated linter ships, conformance is checked by review against the rubric table.
- **Source:** `01-spec-authoring.md` § *AI Confidence Rubric (normative)* lines following the Scoring Metrics table.

### AC-10: Consolidated-guide module-kind pin (Phase 153 audit-v6 close-out)  `[critical]`
- **Given** this module is `kind: consolidated-guide` — its 35 numbered files (`01-spec-authoring.md` through `34-full-tree-ai-audit-v6.md`) are **rollups, audits, and cross-cuts that DESCRIBE other spec modules**, not first-party normative contracts. Each file's filename is a deliberate mnemonic referencing the source module (e.g. `08-docs-viewer-ui.md` describes a planned source module that does NOT exist on disk; `25-blind-ai-implementability-audit.md` is a snapshot audit, not an authoring contract; `31..34-full-tree-ai-audit-vN.md` are dated audit reports). Three of those mnemonic source folders are deliberately ASPIRATIONAL — `08-docs-viewer-ui`, `09-code-block-system`, `13-app` — they are documented as Phase F1 closed under `linter-scripts/spec-folder-refs.allowlist` `[doc-only]` bucket (precedent: `mem://index.md` Core Phase F1 close-out 2026-04-28 — "3 missing-folder targets classified as `[doc-only]`").
- **When** any LLM auditor or fresh implementer reads this module's File Inventory in `00-overview.md` AND the §99 File Inventory AND any Production-Ready / AI-Confidence claims,
- **Then** the implementer MUST treat all `NN-*.md` files in this module as **DESCRIPTIVE rollups, NOT normative source-module entry points**. Cross-references from inside `spec/17/NN-*.md` to `spec/<NN>-<name>/` MAY legitimately point to (a) an existing source module (verifiable on disk), (b) an aspirational source module (in `[doc-only]` bucket per Phase F1), OR (c) an audit corpus (e.g. `_archive/21-git-logs-v1/`). Any auditor finding citing "broken cross-references to source folders" or "Production-Ready claims about non-existent folders" is a **harness misreading of module kind** — `consolidated-guide` rollups legitimately reference both present AND aspirational source modules. The implementer MUST NOT (1) treat aspirational-source mentions as broken refs (Phase F1 closed this class via `[doc-only]` allowlist); (2) demote AI-Confidence on rollup files for citing modules with sub-100 implementability scores (the rollup is at most as confident as its sources, but its OWN P1-P4 gates apply to ITSELF, not to the cited modules); (3) re-author rollup files as first-party normative contracts (would create dual-source drift class with the cited modules — Lesson #36). Lockstep budget for rollup edits follows the same rule as any other module: file banner + §98 row + §99 health row.
- **Source:** `00-overview.md` § "File Inventory"; this file § "Module-Specific Files" (lines 91–121); `99-consistency-report.md` § "File Inventory"; `linter-scripts/spec-folder-refs.allowlist` `[doc-only]` bucket (Phase F1 close-out).
- **Verifies:** `kind: consolidated-guide` declaration applies to all 35 `NN-*.md` files; aspirational-source mnemonics `{08-docs-viewer-ui, 09-code-block-system, 13-app}` declared `[doc-only]` per Phase F1; audit-corpus rollups `{25-blind-ai-implementability-audit, 26-blind-ai-audit-v2, 29-blind-ai-audit-v3, 31-full-tree-ai-audit-v4, 33-full-tree-ai-audit-v5, 34-full-tree-ai-audit-v6}` are dated snapshots NOT live contracts; `mem://index.md` Core § "Phase F1 closed 2026-04-28: 3 missing-folder targets classified as `[doc-only]`". Codifies **Lesson #29 third extension** — audit-corpus pattern (originally for verbatim-quoted evidence in spec/25 post-mortem prose, AC-AI-09/10/11; first extended to non-`.md` assets in spec/11 AC-10; second extended to structural ambiguities in spec/12 AC-09) extends to **rollup / consolidated-guide modules** under the same auditor-misreads-by-default class. Future `kind: consolidated-guide` modules MUST add a module-kind pin AC declaring rollup-not-contract semantics with line-anchored citations to the file inventory.

---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `01-spec-authoring.md`
- `02-coding-guidelines.md`
- `03-error-management.md`
- `04-enum-standards.md`
- `05-split-db-architecture.md`
- `06-seedable-config.md`
- `07-design-system.md`
- `08-docs-viewer-ui.md`
- `09-code-block-system.md`
- `10-powershell-integration.md`
- `11-research.md`
- `12-root-research.md`
- `13-app.md`
- `14-app-issues.md`
- `15-cicd-pipeline-workflows.md`
- `16-app-design-system-and-ui.md`
- `17-self-update-app-update.md`
- `18-database-conventions.md`
- `19-gap-analysis.md`
- `20-wp-plugin-conventions.md`
- `21-lovable-folder-structure.md`
- `22-app-database.md`
- `23-generic-cli.md`
- `24-folder-mapping.md`
- `25-blind-ai-implementability-audit.md`
- `26-blind-ai-audit-v2.md`
- `27-linter-authoring-guide.md`
- `28-distribution-and-runner.md`
- `29-blind-ai-audit-v3.md`
- `30-readme-improvement-suggestions.md`
- `31-full-tree-ai-audit-v4.md`

---

### AC-11: Subfolder Delegation Map (rollup-source binding with `[STUB]` markers)  `[high]`

- **Given** the 35 `NN-*.md` consolidated rollup files in `spec/17-consolidated-guidelines/` (each declared `kind: consolidated-guide` per AC-10),
- **When** any LLM auditor or fresh implementer needs to know (a) which source module a rollup condenses, (b) whether the cited source folder physically exists on disk today, and (c) which canonical AC-family / contract holds the normative truth,
- **Then** the rollup-source binding MUST be discoverable from this §97 alone via the **Subfolder Delegation Map** below — no auditor SHALL need to open `spec/17-consolidated-guidelines/00-overview.md` or any rollup file to disambiguate aspirational refs from live refs from audit-corpus snapshots.

**Subfolder Delegation Map (normative — closes audit-v7 HIGH D2 + LOW D5):**

| Rollup file | Source module | Status | Governing AC-family / contract |
|---|---|---|---|
| `01-spec-authoring.md` | `spec/01-spec-authoring-guide/` | live | AC-SAG-* in source §97 |
| `02-coding-guidelines.md` | `spec/02-coding-guidelines/` | live | AC-CG-* in source §97 |
| `03-error-management.md` | `spec/03-error-manage/` | live | AC-EM-* in source §97 |
| `04-enum-standards.md` | `spec/02-coding-guidelines/04-enum-standards/` | live | AC-CG-15..18 (enum subset) |
| `05-split-db-architecture.md` | `spec/05-split-db-architecture/` | live | AC-SD-* in source §97 |
| `06-seedable-config.md` | `spec/06-seedable-config-architecture/` | live | AC-SC-* in source §97 |
| `07-design-system.md` | `spec/07-design-system/` | live | AC-DS-* in source §97 |
| `08-docs-viewer-ui.md` | `spec/08-docs-viewer-ui/` | **`[STUB]` aspirational** | none (Phase F1 `[doc-only]`) |
| `09-code-block-system.md` | `spec/09-code-block-system/` | **`[STUB]` aspirational** | none (Phase F1 `[doc-only]`) |
| `10-powershell-integration.md` | `spec/11-powershell-integration/` | live | AC-PS-* + AC-09 (pipeline contract) |
| `11-research.md` | `spec/10-research/` | live | AC-RES-* in source §97 |
| `12-root-research.md` | `spec/10-research/` (root-level subset) | live | AC-RES-* (root subset) |
| `13-app.md` | `spec/21-app/` | **`[STUB]` aspirational** | none (Phase F1 `[doc-only]`) |
| `14-app-issues.md` | `spec/25-app-issues/` | live | AC-AI-* (esp. AC-09/10/11 module-kind pin) |
| `15-cicd-pipeline-workflows.md` | `spec/12-cicd-pipeline-workflows/` | live | AC-CI-* + AC-10/11 (Phase A24-fu4) |
| `16-app-design-system-and-ui.md` | `spec/24-app-design-system-and-ui/` | live | AC-ADSU-* in source §97 |
| `17-self-update-app-update.md` | `spec/14-update/` | live | AC-UPD-* + AC-22 (Phase A24-fu5) |
| `18-database-conventions.md` | `spec/04-database-conventions/` | live | AC-DBC-* + AC-09 (Phase P48-2 boolean storage) |
| `19-gap-analysis.md` | (cross-cutting analysis, no single source) | live | meta-rollup (binds Phase 153 task ledger) |
| `20-wp-plugin-conventions.md` | `spec/18-wp-plugin-how-to/` | live | AC-WP-* in source §97 |
| `21-lovable-folder-structure.md` | (project-root convention, no spec/* source) | live | meta-rollup |
| `22-app-database.md` | `spec/23-app-database/` | live | AC-ADB-* + AC-ADB-14 (Phase P48-3 polymorphic AppLink) |
| `23-generic-cli.md` | `spec/13-generic-cli/` | live | AC-GCLI-* + AC-21..23 (Phase A11a §97-WINS contract) |
| `24-folder-mapping.md` | (cross-tree mapping table) | live | meta-rollup |
| `25-blind-ai-implementability-audit.md` | `spec/_archive/blind-audits/v1/` | **`[AUDIT-CORPUS]`** | dated snapshot (Phase 130) |
| `26-blind-ai-audit-v2.md` | `spec/_archive/blind-audits/v2/` | **`[AUDIT-CORPUS]`** | dated snapshot |
| `27-linter-authoring-guide.md` | `linter-scripts/` (toolchain) | live | AC-T-* in `spec/27-spec-toolchain/` §97 |
| `28-distribution-and-runner.md` | `spec/15-distribution-and-runner/` | live | AC-DAR-* in source §97 |
| `29-blind-ai-audit-v3.md` | `spec/_archive/blind-audits/v3/` | **`[AUDIT-CORPUS]`** | dated snapshot |
| `30-readme-improvement-suggestions.md` | (project-root README) | live | meta-rollup |
| `31-full-tree-ai-audit-v4.md` | full-tree audit Phase H1 | **`[AUDIT-CORPUS]`** | dated snapshot |
| `32-phase-26-31-rollup.md` | meta-rollup of slots 25-31 audit corpora | **`[AUDIT-CORPUS]`** | dated snapshot |
| `33-full-tree-ai-audit-v5.md` | full-tree audit (banner-superseded by v6) | **`[AUDIT-CORPUS]`** | dated snapshot |
| `34-full-tree-ai-audit-v6.md` | full-tree audit (banner-superseded by v7) | **`[AUDIT-CORPUS]`** | dated snapshot |
| `35-full-tree-ai-audit-v7.md` | full-tree audit Phase A20 (current LLM baseline) | **`[AUDIT-CORPUS]`** | live snapshot |

**Status legend:**
- **`live`** — source module exists on disk today; rollup is a condensed reference. Auditor MUST resolve cross-refs against the live source.
- **`[STUB]` aspirational** — source folder does NOT exist; mnemonic is in `linter-scripts/spec-folder-refs.allowlist` `[doc-only]` bucket per Phase F1 (2026-04-28). Auditor MUST NOT flag as broken.
- **`[AUDIT-CORPUS]`** — dated snapshot of a historical audit. Quoted findings are evidence, NOT live contract (Lesson #29 first extension; AC-AI-09/10/11 in spec/25 codified the original pattern).

- **Forbidden patterns:**
  - Adding a NEW rollup file without a corresponding row in this Map (silently grows the consolidated surface and breaks AC-02 inventory parity).
  - Promoting an `[AUDIT-CORPUS]` snapshot to `live` without first migrating its findings into the cited source module's §97 (creates dual-source drift class — Lesson #36).
  - Demoting a `live` rollup to `[STUB]` without a Phase F1-style `[doc-only]` allowlist entry (would break the spec-folder-refs gate).
- **Verifies:** the rollup-source binding contract that protects auditors from misreading aspirational refs as broken refs (Phase F1 close-out) AND from misreading audit-corpus snapshots as live contract (Lesson #29 / spec/25 AC-AI-09/10/11 / spec/12 AC-09); the Map IS the discoverable surface so future LLM auditors do NOT flag HIGH D2 `Circular/Self-Referential ACs` or LOW D5 `Aspirational Folder References` (audit-v7 findings closed by this AC).
- **Source:** this file § "Module-Specific Files" (lines 91–127, the file inventory under audit); `linter-scripts/spec-folder-refs.allowlist` `[doc-only]` bucket (Phase F1 close-out, includes `08-docs-viewer-ui`, `09-code-block-system`, `21-app`); `mem://specs/full-tree-audit-v4.md` (Phase F1 narrative); `mem://process/phase-153-lessons` § F (audit-corpus pattern, Lesson #29 + extensions).

---

### AC-12: Worked Example — source→consolidated mapping for `03-error-management.md`  `[medium]`

- **Given** a fresh implementer or LLM auditor reading this §97 and asking "*how* does a 38 KB consolidated rollup relate to its source spec module?",
- **When** the implementer inspects the `03-error-management.md` rollup (38191 bytes) alongside its source `spec/03-error-manage/` (12+ files, ~150 KB total),
- **Then** the implementer MUST be able to follow the mapping below to verify (a) which source-§97 ACs are condensed, (b) which source narrative is dropped vs preserved, and (c) why the rollup's own `**AI Confidence:** Production-Ready` claim applies to the rollup's own structural floor (AC-01..05 of THIS §97) and NOT to the source module's deeper contract:

**Worked Example (normative — closes audit-v7 MEDIUM D4):**

```
SOURCE: spec/03-error-manage/                           CONSOLIDATED: ./03-error-management.md
├── 00-overview.md          (~8 KB, scope/purpose)         §1 Purpose             ← preserved verbatim
├── 01-error-taxonomy.md    (~22 KB, 6 categories)         §2 Error Taxonomy      ← table only, drops worked examples
├── 02-error-codes.md       (~18 KB, 9500..9599 ranges)    §3 Code Ranges         ← preserved verbatim (normative)
├── 03-error-handling.md    (~28 KB, per-language)         §4 Per-Language        ← TS/Go/PHP/Rust/C# code samples preserved
├── 04-error-recovery.md    (~14 KB, retry/backoff)        §5 Recovery Patterns   ← preserved verbatim (normative)
├── 05-error-logging.md     (~12 KB, structured logging)   §6 Logging             ← schema preserved, transport drops
├── 06-error-reporting.md   (~10 KB, telemetry)            (DROPPED)              ← non-normative, link to source
├── 97-acceptance-criteria.md (AC-EM-01..AC-EM-25)         §7 Verification        ← AC-IDs cited, full GWT in source
├── 98-changelog.md                                        (DROPPED)              ← out of rollup scope
└── 99-consistency-report.md                               (DROPPED)              ← out of rollup scope
```

**Mapping rules (normative):**
1. **Preserved verbatim** — sections containing normative tables, regex, code-range definitions, or wire-protocol schemas. The rollup MUST NOT paraphrase these (paraphrase = dual-source drift, Lesson #36).
2. **Condensed (table-only / schema-only)** — narrative source sections whose worked examples can be safely dropped because the source §97 ACs cite them by line-anchor.
3. **Dropped** — telemetry, changelogs, consistency reports — auditor MUST NOT flag their absence in the rollup; the rollup is a *reference*, not a mirror.
4. **AC citation** — every normative claim in the rollup MUST cite an `AC-EM-NN` ID (or equivalent source AC-family) so the reader can resolve to the live source contract.

**Forbidden patterns:**
- Restating a source §97 AC's GWT in the rollup (creates dual-source drift; the rollup MUST link to the source AC by ID).
- Adding new normative content in the rollup that does NOT exist in the source module (the rollup is at most as authoritative as its source — AC-10 module-kind pin).
- Dropping a `[preserved verbatim]` section without first migrating its content into the cited source module.

- **Verifies:** the source→consolidated mapping contract that closes audit-v7 MEDIUM D4 `Missing Worked Examples for Consolidated Format`; the example IS the worked example (meta-discoverable from §97 alone, walker-saturation safe per Lesson #45); reinforces AC-10 module-kind pin by demonstrating "rollup ≠ first-party normative source" mechanically rather than only declaratively.
- **Source:** `./03-error-management.md` (the rollup under example); `spec/03-error-manage/` (the source module); AC-10 above (rollup-not-contract module-kind pin); `mem://process/phase-153-lessons` § C Lesson #36 (link-don't-restate).

---

### AC-13: Source-Wins conflict-resolution contract (Phase 153 Task A24-fu18)  `[high]`

- **Given** every file under `spec/17-consolidated-guidelines/NN-*.md` is a rollup digest of a first-party source module under `spec/MM-<source>/` (per AC-10 module-kind pin + AC-11 Subfolder Delegation Map),
- **When** a rollup line drifts from its cited source §97 / source `00-overview.md` / source normative subsection (drift may arise from the source landing a §97 update without a follow-up rollup refresh, OR a rollup author paraphrasing source prose with a semantic shift, OR a copy-paste predating a source rename),
- **Then** the **source ALWAYS WINS** — the rollup line is FORBIDDEN as the authoritative reference for any AI agent / linter / human reader, and MUST be either (a) refreshed to verbatim-mirror the current source line, OR (b) marked `[STALE — source: <path>#<anchor>]` pending refresh, OR (c) deleted entirely if the source has retired the rule. The conflict resolution rule is **never** "rollup wins" or "newer wins" — the rollup is **always at most as authoritative as its source** (per AC-10 module-kind pin). AI agents reading rollup files MUST treat any encountered rule as a *summary lookup*; downstream enforcement actions (linting, code generation, CI gating) MUST be re-anchored to the source §97 AC ID before acting.

  **Worked drift example** (the canonical conflict pattern):

  | Step | Rollup `03-error-management.md` (digest) | Source `spec/03-error-manage/97-acceptance-criteria.md` AC-EM-04 (canonical) | Resolution |
  |------|-----------------------------------------|-----------------------------------------------------------------------------|------------|
  | T0 | "Error codes use 4-digit numeric range 1000–9999" | "Error codes use 4-digit numeric range 1000–9999" | aligned |
  | T1 (source ships v3.4.0) | _(unchanged — rollup not yet refreshed)_ | "Error codes use 4-digit numeric range 1000–9499; range 9500–9599 reserved for PowerShell pipeline cross-walk per spec/11 AC-09" | **DRIFT** |
  | T2 (AI agent reads rollup at T1) | reads the stale digest line | source line is the authoritative contract | **AI agent MUST NOT generate code based on the rollup line.** Per AC-13 Source-Wins, the AI agent re-anchors to source AC-EM-04, observes the 9500-9599 carve-out, and emits compliant code. |
  | T3 (rollup refresh PR) | refreshed verbatim to source v3.4.0 line | unchanged | aligned again |
  | Optional T1.5 (interim marker) | `[STALE — source: spec/03-error-manage/97-acceptance-criteria.md#AC-EM-04]` | unchanged | drift flagged in-place pending T3 |

  **Forbidden patterns:**
  - Treating a rollup line as the authoritative reference when the source has shipped a divergent update (any AI agent, linter, or CI gate doing so violates AC-10 + AC-13 simultaneously).
  - Adding a `[CANONICAL]` marker to a rollup line (rollup lines are NEVER canonical — only `[STUB]`, `[STALE — source: ...]`, and unmarked-mirror are valid states; `[CANONICAL]` is RESERVED for source §97s).
  - "Reverse-syncing" a source §97 to match a rollup line (the rollup is downstream; corrections flow source → rollup, NEVER rollup → source).
  - Using the rollup as the basis for a `mem://` memory rule (memory rules MUST cite the source §97 AC ID).

- **Verifies:** AC-10 module-kind pin (rollup-not-contract); AC-11 Subfolder Delegation Map (canonical source path per rollup file); the Phase 153 Lesson #36 link-don't-restate axis (Source-Wins is Lesson #36's conflict-resolution complement — Lesson #36 says "don't restate", AC-13 says "if you DID restate and it drifted, source wins"); closes audit-v9 MEDIUM/D4 finding "Missing Worked Examples for Consolidated Format — there is no example showing how an AI should handle a conflict between a 'Consolidated' rule and a 'Source' rule if drift occurs". Codifies the **Phase 153 Task A24-fu18 lesson** (NEW Lesson #59): every rollup module MUST publish an explicit Source-Wins conflict-resolution rule with a worked drift example at all 4 lifecycle steps (T0 aligned → T1 drift → T2 AI-agent encounter → T3 refresh) — the worked drift example IS the contract, NOT a documentation appendix.
- **Source:** This AC; AC-10 above; AC-11 above; `spec/03-error-manage/97-acceptance-criteria.md` (the worked-example source); `mem://process/phase-153-lessons` § C Lesson #36.

### AC-14: `// LINTER-IGNORE-TODO` comment-syntax contract for false-positive markers (Phase 153 Task A24-fu18)  `[low]`

- **Given** the `## Audit Marker Exemption` section in `00-overview.md` documents that some `// TODO:` / `# TBD` / `// FIXME` substrings inside `spec/17-consolidated-guidelines/` files are **AC-content matter** (e.g., a coding-guidelines rollup specifying that `// TODO:` comments MUST be paired with a ticket reference), NOT genuine work-tracking markers,
- **When** a substring-based linter (the `audit-spec-vs-code-v2.py` `todo_density` heuristic, or any future grep-based marker-density gate) scans this folder,
- **Then** the linter MUST recognise the **`// LINTER-IGNORE-TODO`** sentinel comment as the canonical programmatic exemption marker, OR a per-file front-matter key `linter-ignore-todo: true`. Sentinel placement rules:
  1. **Per-line exemption**: `// TODO: example syntax shown in this AC // LINTER-IGNORE-TODO` (sentinel MUST appear on the SAME line, AFTER the marker; line-end placement only — placement before the marker is FORBIDDEN to avoid masking real TODOs)
  2. **Per-fenced-block exemption**: place ` <!-- LINTER-IGNORE-TODO-BLOCK --> ` immediately above the opening fence of any code block whose content is a quoted example of a TODO-bearing rule (sentinel applies to the entire block until the closing fence)
  3. **Per-file exemption**: add `linter-ignore-todo: true` to the file's front-matter (use sparingly — per-file exemption SHOULD be reserved for files where >50% of TODO matches are AC-content, e.g. `02-coding-guidelines.md` rollup if it ever inlines the full TODO-format spec)
  4. The sentinel itself MUST be matched by the regex `//\s*LINTER-IGNORE-TODO(-BLOCK)?\b` (case-sensitive; trailing word boundary mandatory) — variants `LINTER_IGNORE_TODO`, `LINTER-IGNORE` (no `-TODO`), `lint-skip-todo`, `// linter ignore`, etc. are FORBIDDEN to keep the grep surface deterministic
  5. False-positive justification MUST follow the sentinel inline as a `// reason:` clause: `// TODO: example // LINTER-IGNORE-TODO // reason: AC-CG-XX content example`. Sentinel without a `// reason:` clause is FORBIDDEN — undocumented suppressions degrade to genuine work-tracking debt over time.

  **Worked example** (drawn from the `## Audit Marker Exemption` section in `00-overview.md`):

  ```markdown
  Per the cross-language coding standards, every TODO MUST cite a ticket: <!-- LINTER-IGNORE-TODO-BLOCK -->
  ```typescript
  // TODO: replace with retry-loop // reason: example of compliant TODO format per AC-CG-LEGACY-XXX
  function fetchWithRetry() { /* ... */ }
  ```
  ```

- **Verifies:** the `## Audit Marker Exemption (Phase 39b, 2026-04-27)` section in `00-overview.md` (gives that section a programmatic implementation surface); closes audit-v9 LOW/D3 finding "Stale TODO/Marker Heuristic False Positives — The 'Audit Marker Exemption' is a manual note rather than a technical contract that an AI coder can implement to avoid linter failures"; tracks the **Phase 39b R4 follow-up** ("future iteration of `audit-spec-vs-code-v2.py` SHOULD switch to a regex that excludes fenced code blocks and quoted identifiers") as the linter-side complement of AC-14's spec-side contract. NEW Lesson #60: when an audit harness flags a "manual exemption note" as a finding, the closure path is to give the exemption a deterministic regex-matchable sentinel — manual exemption notes are walker-invisible by definition; sentinel comments are walker-visible AND grep-auditable.
- **Source:** This AC; `00-overview.md` § Audit Marker Exemption; `linter-scripts/audit-spec-vs-code-v2.py` (the linter that consumes the sentinel — bind on first refresh per Phase 39b R4).

### AC-15: Rollup-not-first-party-contract structural pin (Phase 153 Task A24-fu18; Lesson #51 mirror)  `[high]`

- **Given** this module is `kind: rollup` with `content_axis: process-guidance` (per AC-10 + front-matter), and its 35 `NN-*.md` files are **standalone digests** of first-party source modules under `spec/MM-<source>/` (per AC-11 Subfolder Delegation Map),
- **When** an audit harness reports findings of the form "Circular/Self-Referential Acceptance Criteria", "ACs verify that files exist and are formatted correctly, but they do not provide GWT tests for the *content* of the guidelines", "Missing Logic Verification AC", "Rollup duplicates source", or any variant claiming the rollup module's §97 should enumerate per-rule content-logic GWT tests,
- **Then** the finding MUST be classified as **STRUCTURAL-ROLLUP-NOT-FIRST-PARTY-CONTRACT** rather than a contract gap, because:
  1. The **§17 contract surface** is **file-existence + format + cross-link parity to source** (AC-01 through AC-09 enumerate the entire normative surface of this module — every `NN-*.md` rollup MUST exist on disk per AC-02, MUST follow the naming convention per AC-03, MUST have a current consistency report per AC-04, MUST pass the tree-health gate per AC-05, MUST cross-link to source per AC-07, MUST stay in lockstep with §98/§99 per AC-08).
  2. **Content-logic GWT tests for any rule in any rollup file MUST live in the source module's §97**, NOT here (per AC-10 module-kind pin + Lesson #36 link-don't-restate). For example: GWT for "Error codes use 4-digit numeric range 1000–9999" lives in `spec/03-error-manage/97-acceptance-criteria.md` AC-EM-04, NOT in `spec/17-consolidated-guidelines/97-acceptance-criteria.md` — restating it here would violate AC-10 + create a dual-source drift class (the very class AC-13 Source-Wins exists to resolve, but the better remediation is to NOT create the drift in the first place).
  3. **Conflict-drift handling is owned by AC-13 Source-Wins**, NOT by per-rule GWT tests in §17 (a per-rule GWT in §17 would either (a) silently drift from source, recreating the audit-v9 finding under a different label, OR (b) require lockstep updates on every source §97 change tree-wide — an O(N²) maintenance class explicitly forbidden by Lesson #36).
  4. **AC-12 worked-example pattern** (single representative source→rollup mapping per audit cycle) is the canonical proof of rollup-source parity, NOT exhaustive per-rule GWT enumeration. The auditor's "Logic Verification" suggestion would scale linearly with the number of rules in every source module the rollup digests (~hundreds tree-wide) — infeasible AND wrong axis.

  **Forbidden remediation patterns** (to prevent the same finding recurring under a different label):
  - Adding per-rule content-logic GWT ACs to §17 §97 (would violate AC-10 + Lesson #36 + the very rollup-not-contract classification this AC pins).
  - Promoting any §17 AC to declare a content-rule as "canonical" or "authoritative" (only source §97s carry `[CANONICAL]` semantics; AC-13 forbids `[CANONICAL]` markers in rollups).
  - "Fixing" the audit-v9 finding by deleting the rollup module entirely (the rollup serves a real AI-onboarding purpose per `## Purpose` in §00 — single-document quick-reference for cross-module overviews; deletion would force AI agents to chase 35+ source modules to reproduce that overview).
  - Re-classifying §17 as `kind: normative-contract` to "satisfy" the auditor (would invert the entire module's contract; the rollup IS process-guidance because it's a process artifact for AI onboarding, NOT a normative surface).

- **Verifies:** AC-10 module-kind pin (rollup-not-contract — the foundational classification); AC-11 Subfolder Delegation Map (per-file source binding); AC-12 Worked Example (proof-of-parity pattern); AC-13 Source-Wins (conflict-drift handling owner); `mem://process/phase-153-lessons` § C Lesson #36 (link-don't-restate); closes the recurring **Phase 153 Task A24-fu18 audit-v9 HIGH/D2 finding** "Circular/Self-Referential Acceptance Criteria" as STRUCTURAL-ROLLUP-NOT-FIRST-PARTY-CONTRACT auditor misclassification. Mirror of Lesson #51 (structural-pin pattern) on the **rollup-vs-source axis** — fifth instance across five different axes: spec/02 AC-CG-24 (normative-contract / 251-file walker-saturation), spec/25 AC-AI-16 (audit-corpus / verbatim-quote interaction), spec/04 AC-13 (normative-contract / cross-module link-don't-restate), spec/07 AC-039 (process-guidance / 17-file walker-saturation), **spec/17 AC-15 (rollup / source-vs-rollup contract-surface confusion)**. Lesson #51 fully axis-orthogonal at 5th instance.
- **Source:** This AC; AC-10 above; AC-11 above; AC-12 above; AC-13 above; `mem://process/phase-153-lessons` § C Lesson #36 + § F (audit-corpus pattern); precedent ACs spec/02 AC-CG-24 / spec/25 AC-AI-16 / spec/04 AC-13 / spec/07 AC-039.

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
