# Spec Authoring Guide — Acceptance Criteria

**Version:** 4.11.0
**Updated:** 2026-04-30 (Phase 153 Task A24-fu21 — spec/01 floor lift 83 → ≥90 expected. Added AC-SAG-30 linter-script-logic-anchor pin per Lesson #36 + AC-SAG-31 inlined-schema-version-pluralism pin. Co-applied Lesson #55 §00 walker-pin teaser. Closes audit-v9 MEDIUM D3 + LOW D1.)
**Scope:** `spec/01-spec-authoring-guide/` (the meta-spec — governs every other §97 / §98 / §99 / §00 in the tree).

---

## Module Summary

§01 is the **meta-spec** — it specifies how every OTHER spec in the repository must be authored, named, structured, cross-linked, and version-controlled. The 11 normative content files (`01-folder-structure.md` … `11-root-readme-conventions.md`) define the rules; this `97` codifies the rules as testable Given/When/Then criteria so an AI agent or linter can verify any spec module satisfies them. **Dogfooding rule**: this module MUST itself satisfy every AC it specifies — failures here cascade across the entire spec tree.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

```text
META_FOLDER:               spec/01-spec-authoring-guide/
NORMATIVE_FILES:           01-folder-structure.md, 02-naming-conventions.md,
                           03-required-files.md, 04-cli-module-template.md,
                           05-app-project-template.md, 06-non-cli-module-template.md,
                           07-memory-folder-guide.md, 08-cross-references.md,
                           09-exceptions.md, 10-mandatory-linter-infrastructure.md,
                           11-root-readme-conventions.md
                           (also non-numbered: 04-ai-onboarding-prompt.md)
REQUIRED_PER_MODULE:       00-overview.md, 97-acceptance-criteria.md,
                           98-changelog.md, 99-consistency-report.md
RESERVED_PREFIXES:         00=overview, 97=acceptance-criteria,
                           98=changelog, 99=consistency-report
NAMING_REGEX:              ^[0-9]{2}-[a-z0-9-]+(\.md)?$
NUMBERING_RANGES:          spec root: 01-99 (slot immutable once shipped)
                           subfolders: 01-99 within parent
OVERVIEW_REQUIRED_SECTIONS: H1 title, Version banner, Updated date, AI Confidence,
                            Ambiguity, Overview paragraph, Scoring table, Keywords,
                            Files inventory table, Cross-References table
CROSS_LINK_RULES:          relative paths only (../ or ./), .md extension required,
                           lowercase paths, target must exist on disk
LINTER_GATES:              node linter-scripts/check-tree-health.cjs (≥ 75 default, locked at 100)
                           node linter-scripts/generate-spec-index.cjs (regen on every spec edit)
                           python3 linter-scripts/check-spec-cross-links.py (zero broken)
                           bash linter-scripts/run.sh (full self-heal pipeline)
LOCKSTEP_RULE:             every spec edit MUST update target file banner +
                           §98 changelog row + §99 health/inventory + spec-index regen
SLOT_IMMUTABILITY:         once a numbered slot ships, it is permanent;
                           moves require a new slot + §99 audit row (precedent: §16→§37 v2.8.6)
```

---

## Acceptance Criteria

### AC-SAG-01 — Every spec module under `spec/` has the four required files

- **Given** any module folder under `spec/` (e.g. `spec/02-coding-guidelines/`, `spec/22-git-logs-v2/`, `spec/27-spec-toolchain/03-runner/`),
- **When** its file inventory is listed,
- **Then** it MUST contain `00-overview.md`, `97-acceptance-criteria.md`, `98-changelog.md`, AND `99-consistency-report.md` at minimum. Folders with fewer than 3 content files MAY omit `97`/`98` only if explicitly listed in `09-exceptions.md`. Modules missing any required file MUST be flagged by `node linter-scripts/check-tree-health.cjs --report` as `required=N/4` AND MUST drop the tree-health score below 100. The `_archive/` subtree is the ONLY whole-tree exemption; archived modules retain their last shipped state but are NOT re-validated.
- **Verifies:** `03-required-files.md` + `09-exceptions.md` + `linter-scripts/check-tree-health.cjs` contract.

### AC-SAG-02 — All spec files and folders use lowercase kebab-case with numeric prefixes

- **Given** any file or folder under `spec/`,
- **When** its name is matched against the regex `^[0-9]{2}-[a-z0-9-]+(\.md)?$`,
- **Then** it MUST match. Special files exempt from the numeric prefix: `readme.md` (root only), `consolidated-review-guide.md`, `consolidated-review-guide-condensed.md`, and the trailing `.gitkeep` markers. Uppercase letters, underscores, dots (other than the `.md` extension), and spaces are FORBIDDEN. The numeric prefix MUST be a two-digit zero-padded integer in `00-99`. Three-digit prefixes (`100-` etc.) MUST trigger a parent-folder split per `01-folder-structure.md`'s overflow rule.
- **Verifies:** `02-naming-conventions.md` (kebab-case + numeric prefix rules).

### AC-SAG-03 — Reserved prefixes 00/97/98/99 are used only for their designated purposes

- **Given** any file with prefix `00-`, `97-`, `98-`, or `99-`,
- **When** the file's purpose is inspected,
- **Then** `00-` MUST be `00-overview.md` (module entry point), `97-` MUST be `97-acceptance-criteria.md` (testable GWT ACs), `98-` MUST be `98-changelog.md` (reverse-chronological version history), AND `99-` MUST be `99-consistency-report.md` (file inventory + health metrics). Using `00-something-else.md`, `97-different.md`, etc. is FORBIDDEN. The prefixes `01-` through `96-` are free for content files.
- **Verifies:** `02-naming-conventions.md` reserved-prefix table + `03-required-files.md`.

### AC-SAG-04 — Slot numbers are immutable once shipped

- **Given** a numeric slot (e.g. `22-git-logs-v2/`) that has been merged to the main branch in any release,
- **When** a future change wants to relocate or rename the slot's content,
- **Then** the original slot number MUST NOT be reused for different content. The change MUST allocate a NEW slot (precedent: §22 collision → §25 `app-issues/`; §16 → §37 in folder-22 v2.8.6) AND MUST add an audit row to the source folder's `99-consistency-report.md` AND MUST add a corresponding row to `mem://specs/git-logs.md` queued-decisions trail. Renaming the kebab-case suffix (e.g. `22-git-logs/` → `22-git-logs-v2/`) is permitted ONLY for in-flight unreleased specs; once shipped, the suffix freezes too.
- **Verifies:** Memory rule "File slots are immutable once shipped" + Phase-1 Triage v3.7.0 precedent.

### AC-SAG-05 — Every `00-overview.md` includes the seven mandatory metadata sections

- **Given** any `00-overview.md` in the spec tree,
- **When** parsed,
- **Then** it MUST contain (in order): (1) H1 title matching the module name, (2) `**Version:**` SemVer banner, (3) `**Updated:**` ISO date, (4) `**AI Confidence:**` (Production-Ready / High / Medium / Low), (5) `**Ambiguity:**` (None / Low / Medium / High / Critical), (6) Keywords section with searchable tags, (7) Files inventory table with relative links AND descriptions, (8) Cross-References section. Missing any section MUST be flagged by the linter as a structural violation. The Scoring table (Health Score 0-100) MUST be present when the module has shipped (post-baseline).
- **Verifies:** `00-overview.md` "How to Write an Overview" section + `03-required-files.md`.

### AC-SAG-06 — `97-acceptance-criteria.md` files contain ≥ 5 GWT triplets, not table-row scaffolds

- **Given** any `97-acceptance-criteria.md`,
- **When** parsed,
- **Then** it MUST contain ≥ 5 `### AC-` headings, each followed by explicit `**Given**` / `**When**` / `**Then**` markers in that order, with each line of the triplet being a non-empty sentence. Table-row criteria (e.g. `| AC-001 | Boolean principles ... |`) MAY appear as a legacy index but MUST NOT be the sole content. Per the Phase 16d/e/f deepening sweep, the canonical depth target is 20 GWT ACs per module-level §97 and 40 for high-blast-radius modules (e.g. §22 has 68, §28 has 40). Modules with < 5 GWT ACs MUST be flagged for the next deepening phase.
- **Verifies:** `02-coding-guidelines/97-acceptance-criteria.md` AC-CG-10 + Phase 16e scan finding.

### AC-SAG-07 — Every `98-changelog.md` is reverse-chronological, SemVer-bumped on each edit

- **Given** any `98-changelog.md`,
- **When** parsed,
- **Then** entries MUST be ordered newest-first, each entry MUST have a `## [X.Y.Z] — YYYY-MM-DD` header, AND each header MUST follow [SemVer](https://semver.org/) (MAJOR.MINOR.PATCH). Editing the parent module file (`00-overview.md` or any content file) without bumping `98-changelog.md` is a CODE-RED maintenance violation. Categories MUST come from {`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`}. The SemVer bump rule: behavioral change to a normative contract → MAJOR; new AC or new content file → MINOR; typo / clarification → PATCH.
- **Verifies:** Memory rule "lockstep §98 + §99 + audit row" + `02-coding-guidelines/98-changelog.md` format precedent.

### AC-SAG-08 — Every `99-consistency-report.md` reflects the current file inventory within 7 days

- **Given** any `99-consistency-report.md`,
- **When** the `**Last Updated:**` date is compared against `git log --format=%ad -1 -- <module-folder>`,
- **Then** the gap MUST be ≤ 7 days. The report MUST contain: (1) Module Health table (boolean ✅/❌ for `00-overview.md present`, `99 present`, naming compliance, prefix uniqueness), (2) File Inventory table listing every file in the folder with status, (3) Health Score (0-100), (4) any module-specific gap list. The auto-generated banner stamp ("v3.2.0 — 2026-04-16") MUST match the SemVer in `98-changelog.md`'s top entry. Stale reports (> 7 days) MUST drop the module's tree-health score by 10 points.
- **Verifies:** `00-overview.md` Scoring section + `linter-scripts/check-tree-health.cjs` freshness check.

### AC-SAG-09 — All cross-references use relative paths with `.md` extension; never absolute, never bare

- **Given** any markdown link in any spec file,
- **When** the link is parsed,
- **Then** it MUST start with `./` or `../` (relative path), MUST end with `.md` (NEVER bare paths like `[link](../foo)`), MUST use lowercase kebab-case throughout the path, AND MUST resolve to an existing file on disk. Absolute paths (`/spec/...`), root-relative paths, GitHub URLs (`https://github.com/.../spec/...`), and protocol-less paths (`spec/...` without `./` prefix) are FORBIDDEN. The depth (count of `../`) MUST be exactly correct. Bidirectional linking is RECOMMENDED (if A links to B, B should link to A) but not strictly enforced — broken links ARE strictly enforced.
- **Verifies:** `08-cross-references.md` 7-rule checklist + `linter-scripts/check-spec-cross-links.py` contract.

### AC-SAG-10 — Spec-edit lockstep: target file + §98 + §99 + spec-index regen

- **Given** any edit to any spec content file (NOT including the four reserved files themselves),
- **When** the edit is committed,
- **Then** the SAME commit MUST also: (1) bump the target file's `**Version:**` banner if the file has one, (2) add a row to the same module's `98-changelog.md` describing the change, (3) update the same module's `99-consistency-report.md` (file inventory if files changed; Last Updated date always), AND (4) regenerate `spec/spec-index.md` via `node linter-scripts/generate-spec-index.cjs`. Skipping any of the four MUST be flagged as a lockstep violation. This rule is the highest-frequency CODE-RED violation in the spec tree per Phase 16e audit findings.
- **Verifies:** Memory rule "Spec edits keep these in lockstep" + `linter-scripts/generate-spec-index.cjs`.

### AC-SAG-11 — CLI modules follow the 3-folder pattern; app modules follow features+issues; flat modules use `06-non-cli-module-template.md`

- **Given** a new spec module is being created,
- **When** the author chooses a folder layout,
- **Then** CLI tool modules MUST follow `04-cli-module-template.md` (3-folder pattern: `01-backend/`, `02-frontend/`, `03-deploy/` or `03-diagrams/`); app/WordPress modules MUST follow `05-app-project-template.md` (`01-fundamentals.md` + `02-features/{NN}-{name}/{01-backend.md, 02-frontend.md, 03-wp-admin.md}` + `03-issues/`); flat research/utility modules MUST follow `06-non-cli-module-template.md`. Mixing patterns within one module is FORBIDDEN. The choice of pattern MUST be declared in the module's `00-overview.md` "Folder Structure" section.
- **Verifies:** `01-folder-structure.md` + `04-cli-module-template.md` + `05-app-project-template.md` + `06-non-cli-module-template.md`.

### AC-SAG-12 — Subfolders with 3+ content files MUST have their own `00-overview.md`

- **Given** a subfolder under any module that contains 3 or more `.md` files (excluding `97`/`98`/`99`),
- **When** its inventory is listed,
- **Then** the subfolder MUST contain its own `00-overview.md` summarizing what's inside, with the same metadata sections as a top-level overview (per AC-SAG-05). Subfolders with 1 or 2 files are exempt unless they themselves have nested subfolders. The exemption boundary is documented in `09-exceptions.md`.
- **Verifies:** `03-required-files.md` "Subfolder rules" + `09-exceptions.md`.

### AC-SAG-13 — `.lovable/memories/` is the canonical memory folder; `.lovable/memory/` is FORBIDDEN

- **Given** any reference to a memory file across the codebase or specs,
- **When** the path is inspected,
- **Then** it MUST use `.lovable/memories/` (plural). The legacy singular form `.lovable/memory/` is FORBIDDEN — if found in any audit, the contents MUST be migrated to `.lovable/memories/` AND the legacy folder deleted in the same PR. Memory files use lowercase kebab-case (numeric prefixes optional, unlike spec files), max depth `memories/{category}/{file}.md`, AND every memory file MUST be referenced from `00-memory-index.md`. Duplication of spec content into memories is FORBIDDEN — memories hold patterns, decisions, and conventions; specs hold contracts.
- **Verifies:** `07-memory-folder-guide.md` consolidation rule + `00-overview.md` "The .lovable/ Folder" section.

### AC-SAG-14 — Mandatory linter scripts are present before any spec validation runs

- **Given** any spec validation pipeline (`bash linter-scripts/run.sh` or any sub-step),
- **When** the pipeline starts,
- **Then** the following scripts MUST exist in `linter-scripts/` and be executable: `check-tree-health.cjs`, `generate-spec-index.cjs`, `check-spec-cross-links.py`, `validate-guidelines.go` (or `.py` twin), AND `run.sh` (orchestrator). Missing any script MUST cause the pipeline to exit non-zero with a clear "missing infrastructure" error — NEVER silently skip the check. The Python+Go twin requirement (per `27-spec-toolchain/97` AC-T-18) means byte-equivalent output between the two implementations is mandatory.
- **Verifies:** `10-mandatory-linter-infrastructure.md` + `27-spec-toolchain/97-acceptance-criteria.md` AC-T-18.

### AC-SAG-15 — Root `readme.md` follows the mandatory hero-block + author + badges + §9 release-blocker format

- **Given** the repository root `readme.md`,
- **When** parsed,
- **Then** it MUST contain (in order): (1) centered icon/logo, (2) hero block with project name + tagline, (3) author/company template block, (4) status badges (build, version, license), AND (5) a §9 "Release Blockers" checklist enumerating all currently-blocking issues. Any of (1)-(5) missing MUST block release. The §9 checklist MUST be the last numbered section before any appendices. This rule applies ONLY to the repo root `readme.md`, NOT to nested `readme.md` files (which are unconstrained).
- **Verifies:** `11-root-readme-conventions.md` § Mandatory Sections.

### AC-SAG-16 — AI Confidence and Ambiguity scores reflect actual spec readiness, not aspirational claims

- **Given** any `00-overview.md` declaring `**AI Confidence:** Production-Ready` AND `**Ambiguity:** None`,
- **When** an audit verifies the claim against actual content,
- **Then** the module MUST satisfy: (a) all interfaces fully typed, (b) ≥ 5 GWT ACs in `97`, (c) zero broken cross-links, (d) all referenced contracts inlined or linked to existing files, (e) `99-consistency-report.md` Health Score = 100. False "Production-Ready" claims MUST be downgraded by the auditor (precedent: full-tree audit v4 dropped tree score from claimed 100 → actual 45 in 2026-04-25). Aspirational scoring is a CODE-RED maintenance violation. The full-tree audit's findings are codified in `mem://specs/full-tree-audit-v4.md`.
- **Verifies:** `00-overview.md` Scoring Metrics section + `mem://specs/full-tree-audit-v4.md`.

### AC-SAG-17 — Reliability Risk Reports are mandatory before implementing Complex Agentic / End-to-End modules

- **Given** a spec module with `Complexity Tier: Complex Agentic` OR `End-to-End` OR with AI Confidence < 70%,
- **When** any implementation work begins,
- **Then** a Reliability Risk Report MUST exist at `spec/validation-reports/<module-name>.md` OR inline in the module's `00-overview.md`. The report MUST contain: Complexity Tier, Success Probability (%), Failure Modes, Risk Mitigations, Dependency Risks. Beginning implementation without the report for these tiers is FORBIDDEN. Simple/Medium tiers are exempt. The user-preference rule "Wants reliability reports before implementation" is the source of this AC.
- **Verifies:** `00-overview.md` "Reliability Check Report" section + user-preferences memory.

### AC-SAG-18 — Self-application: `01-spec-authoring-guide/` itself satisfies every AC it specifies (dogfooding)

- **Given** this module (`spec/01-spec-authoring-guide/`),
- **When** every AC above (AC-SAG-01..AC-SAG-17) is applied to this module's own files,
- **Then** every check MUST pass: four required files present (AC-SAG-01) ✅; all 16 files match naming regex (AC-SAG-02) ✅; reserved prefixes correct (AC-SAG-03) ✅; slot 01 has been stable since baseline (AC-SAG-04) ✅; `00-overview.md` has all seven sections (AC-SAG-05) ✅; this `97` has 20 GWT ACs (AC-SAG-06) ✅ — verified by self-application; `98-changelog.md` reverse-chronological + SemVer (AC-SAG-07) ✅; `99-consistency-report.md` updated within 7 days of this commit (AC-SAG-08) ✅; all cross-references relative + `.md` (AC-SAG-09) ✅; this commit updates §98 + §99 + spec-index in lockstep (AC-SAG-10) ✅; this module follows the flat (non-CLI, non-app) pattern per `06-non-cli-module-template.md` (AC-SAG-11) ✅. **The dogfooding rule is binding** — failure of any AC against this module is a meta-failure that cascades to every other module's compliance claim.
- **Verifies:** All preceding ACs + recursive self-check.

### AC-SAG-19 — Linter pipeline (`bash linter-scripts/run.sh`) exits 0; tree-health ≥ 75 (locked at 100)

- **Given** any commit touching files under `spec/`,
- **When** `bash linter-scripts/run.sh` runs in CI,
- **Then** the pipeline MUST exit 0 AND `node linter-scripts/check-tree-health.cjs --report` MUST output `PASS: tree health N ≥ threshold 75`. The default threshold is 75 but the project lock per `mem://specs/full-tree-audit-v4.md` Phase 3 is 100. CI MUST fail any PR that drops the score below the locked threshold. The pipeline order is: (1) cross-link check, (2) self-heal (`--fix`), (3) regen spec-index, (4) tree-health gate. Steps (1)–(3) are repeatable/idempotent; step (4) is the gate.
- **Verifies:** `10-mandatory-linter-infrastructure.md` + `27-spec-toolchain/97` AC-T-15/16/19.

### AC-SAG-20 — `spec-index.md` is auto-generated; manual edits are FORBIDDEN

- **Given** the file `spec/spec-index.md`,
- **When** any change to it is committed,
- **Then** the change MUST come from `node linter-scripts/generate-spec-index.cjs` (deterministic, content-derived). Manual edits to `spec-index.md` are FORBIDDEN — the file's content is fully reproducible from the rest of the spec tree, and divergence introduces drift. The script MUST be re-run as part of the AC-SAG-10 lockstep on every spec edit. The output is byte-identical between Python and Go twin generators per AC-T-18 (cross-toolchain stability).
- **Verifies:** `linter-scripts/generate-spec-index.cjs` contract + AC-SAG-10 lockstep + AC-T-18 (twin equivalence).

### AC-SAG-21 — `kind:` front-matter selects the auditor rubric branch (Phase 89)

- **Given** a module's `00-overview.md` declaring `kind: <value>` in YAML front-matter where `<value> ∈ {active-spec, future-spec, tracker, index, meta-toolchain}`,
- **When** `linter-scripts/audit-spec-vs-code-v2.py` runs in deterministic mode,
- **Then** the rubric branch chosen MUST match the value: `tracker` → tracker branch (impl baseline 75, cap 85 prose-only / 95 with ≥1 typed contract per v2.13); `index` → index branch (impl baseline 70 + 10 if `child_modules > 0`, cap 90 prose-only / 100 with ≥1 typed contract per v2.11); `meta-toolchain` → meta-toolchain branch (impl baseline 75, +10 if `has_normative_contract`, +5 if `md_files >= 30`, cap 100 per v2.10); `active-spec`/omitted/`future-spec` → normal contract module branch (impl baseline 30 + additive contract bonuses).
- **And** an unrecognised `kind:` value MUST default to the normal contract branch (no crash, no hard error). The full enum is enumerated in §00 OpenAPI `SpecAudit` schema.
- **Verifies:** `linter-scripts/audit-spec-vs-code-v2.py` rubric branches + `spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md` AC-31-15..AC-31-21.

### AC-SAG-22 — `todo_audit_exempt: true` opt-out is reviewer-gated (Phase 89, v2.14)

- **Given** a module's `00-overview.md` declaring `todo_audit_exempt: true` in YAML front-matter,
- **When** `linter-scripts/audit-spec-vs-code-v2.py` runs in deterministic mode,
- **Then** `metrics.todo_count` MUST be forced to `0` regardless of how many real `TODO:`/`TBD:`/`FIXME:` markers appear in prose, AND completeness scoring MUST NOT penalise the module for them.
- **And** the opt-out MUST only be set on auditor-self-reference modules (modules that legitimately quote work-tracker markers because they document the TODO detector itself — currently only `spec/27-spec-toolchain/`). Reviewer MUST reject the opt-in for any other module type, since misuse silently masks unresolved work.
- **And** the v2.14 tightened TODO regex requires the canonical work-tracker shape (`TODO:` / `TODO(name):` / `TODO -`); narrative mentions like "marked TODO" or "TODO/FIXME density" do **not** match, so most modules do not need this opt-out.
- **Verifies:** `linter-scripts/audit-spec-vs-code-v2.py` `TODO_EXEMPT_RX` + `spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md` AC-31-22.

### AC-SAG-23 — `lifecycle-spec-authoring.mmd` is the canonical lifecycle source of truth (Phase 93)

- **Given** the file [`lifecycle-spec-authoring.mmd`](./lifecycle-spec-authoring.mmd) in this folder,
- **When** any contributor (human or AI) needs to understand the end-to-end module lifecycle from authoring through CI to merge,
- **Then** the `.mmd` file MUST be the canonical reference and MUST encode (a) all 5 valid `kind:` values as branching paths from the entry node, (b) the 6-step local linter pipeline (`generate-spec-index.cjs` → `check-spec-cross-links.py` → `check-tree-health.cjs --strict` → `check-lockstep.cjs --strict` → `audit-spec-vs-code-v2.py` with `AUDIT_DETERMINISTIC=1` → `check-trace-map-regression.py`), (c) the 6-gate CI pipeline in `.github/workflows/spec-health.yml` including the Phase 91 CLI self-test step, (d) the failure-recovery loop pointing back to the author phase via the `--explain=<module>` debugging flag, and (e) the post-merge phase-memo step writing to `.lovable/memory/audit/v2-deterministic/`.
- **And** the inline mermaid excerpt in [`00-overview.md`](./00-overview.md) "Lifecycle Diagram" section MAY be a simplified summary of the `.mmd` file but MUST NOT contradict it; on contradiction the `.mmd` file wins. Reviewers MUST update both when changing the lifecycle.
- **And** any addition or removal of a local linter or CI gate MUST be reflected in the `.mmd` file in the same PR (lockstep with `.github/workflows/spec-health.yml` and `linter-scripts/run.sh`).
- **Verifies:** `spec/01-spec-authoring-guide/lifecycle-spec-authoring.mmd` (32 nodes, 6 styled classes) + `00-overview.md` "Lifecycle Diagram (Phase 66, expanded in Phase 93)" section + `.github/workflows/spec-health.yml` (6 gates) + `linter-scripts/run.sh` (6 local checks).

---

### AC-SAG-24 — Every `.mmd` file MUST parse cleanly with the mermaid library (Phase 97)

- **Given** any file under `spec/**` matching the glob `*.mmd`,
- **When** `node linter-scripts/check-mermaid-syntax.mjs` is invoked locally OR the "Mermaid diagram syntax gate" CI step runs,
- **Then** the file MUST parse without error using the official `mermaid` library (≥ v11) under a `jsdom` + `DOMPurify` shim, and the gate MUST report `<N>/<N> files parsed cleanly`.
- **And** common author mistakes that fail this gate include: (a) a bare `%%` line as a comment-block separator (mermaid mis-tokenises it as a `%%{init}%%` directive — use `%% --` instead), (b) unquoted node labels containing `@` or other reserved chars (e.g. `B[actions/checkout@v6]` must be `B["actions/checkout@v6"]`), (c) missing directive (`flowchart TD`, `graph TD`, `mindmap`, `sequenceDiagram`, `stateDiagram-v2`, …) before the first node.
- **And** the check MUST be deterministic and side-effect-free: zero file writes, zero network calls, zero environment dependencies beyond `node` + the project's `node_modules`.
- **And** if a contributor adds a new `.mmd` file with a syntax error, the gate MUST fail the PR with `<file path>` + first parser error line, NOT a stack trace from the mermaid library itself.
- **Verifies:** `linter-scripts/check-mermaid-syntax.mjs` + `.github/workflows/spec-health.yml` "Mermaid diagram syntax gate (Phase 97)" step + `package.json` devDependencies (`mermaid` ≥ 11, `jsdom` ≥ 20).

### AC-SAG-25 — `mermaid` and `jsdom` MUST be pinned to exact versions; major-version bumps require local syntax-gate re-run (Phase 101)

- **Given** the `package.json` lists `mermaid` (used both by the app and by `linter-scripts/check-mermaid-syntax.mjs`) and `jsdom` (used only by the syntax-gate script),
- **When** either dependency is declared,
- **Then** the version specifier MUST be an **exact pin** (e.g. `"mermaid": "11.14.0"`, `"jsdom": "20.0.3"`) — caret (`^`) and tilde (`~`) ranges are FORBIDDEN for these two packages.
- **And** the rationale is: AC-SAG-24's parse-clean guarantee is only as stable as the mermaid grammar; an unpinned caret range silently upgrades the grammar mid-PR (e.g. mermaid 11 → 12 may rename a directive), turning the gate from a quality signal into a flaky one. Pinning makes any grammar change an explicit, reviewable bump.
- **And** any PR that bumps the **major** version of `mermaid` or `jsdom` (e.g. `11.x.y` → `12.0.0`, or `20.x.y` → `21.0.0`) MUST: (1) include a note in `98-changelog.md` recording the bump and the bumper's local `bun linter-scripts/check-mermaid-syntax.mjs` run output (`<N>/<N> files parsed cleanly`), AND (2) re-run the full gate triad locally before merge: `bun linter-scripts/check-mermaid-syntax.mjs`, `bash linter-scripts/test/test-audit-deterministic-stability.sh`, and `bash linter-scripts/run.sh`.
- **And** **minor** and **patch** bumps (e.g. `11.14.0` → `11.15.0`) MAY be made without the local re-run requirement, but the CI gate still runs and MUST pass — pinning ensures CI sees the same version as the bumper's local environment.
- **And** the `dompurify` package is transitively pinned through mermaid's own `package.json` and is NOT a direct dependency; this AC does NOT require a separate `dompurify` pin in this repo.
- **Verifies:** `package.json` (lines for `mermaid` and `jsdom` show no `^` or `~`) + `bun.lock` (resolved versions match the pin exactly) + `98-changelog.md` (any major-bump entry includes the gate-run output line) + **AC-31-30** at [`spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md`](../27-spec-toolchain/31-audit-spec-vs-code-v2.md) — the **general pattern** of which AC-SAG-25 is the concrete instance for mermaid+jsdom. AC-31-30 enumerates the inventory of all currently-pinned grammar-defining libraries and the four-step protocol for adding new ones.

### AC-SAG-26 — Documentation-cadence retirement pattern (Phase 111, generalises Phase 100 + Phase 104)

- **Given** a recurring documentation cadence in the repository — defined as **any structural section, heading pattern, or bookkeeping convention that EVERY new artefact of a given class is expected to contain** (e.g. "Next phases (queued)" sections in phase memos under `.lovable/memory/audit/v2-deterministic/`; "Roadmap" sections in module overviews; "TODO inventory" tables in changelogs; recurring footer blocks; periodic-cadence headers like "Q1 priorities") — that has been observed across **3 or more historical instances**,
- **When** empirical evidence accumulates that the cadence is producing more drift / staleness / cognitive overhead than informational value — concretely measured by ANY of: (a) ≥ 2 instances where the cadence content was stale within 1 phase of being written; (b) ≥ 1 instance where two adjacent artefacts contradicted each other on the same cadence-controlled item; (c) the information the cadence carries has migrated to a single canonical source of truth (a tracker, a registry table, an AC `Verifies` clause, a generated artefact) that the cadence now duplicates,
- **Then** the cadence MAY be **formally retired** by issuing a **retirement memo** at `.lovable/memory/audit/v2-deterministic/phase-NNN-<cadence-name>-retirement.md` (or the equivalent canonical retrospectives location) that MUST contain: (a) the cadence's name + observable definition; (b) the empirical evidence that triggered retirement (concrete instance numbers, dates, drift examples); (c) the **canonical replacement source of truth** for the information the cadence used to carry; (d) the **CUTOFF_PHASE** (or equivalent boundary marker — date, version number, sequence number) above which new artefacts are subject to the retirement; (e) explicit out-of-scope statement that pre-cutoff artefacts are historical record and MUST NOT be retroactively edited.
- **And** within the same PR (or the immediately following PR if scope warrants), a **mechanical enforcement gate** MUST be authored that scans new artefacts (post-cutoff) and FAILS on the retired cadence's structural signature. The gate MUST: (i) live under `linter-scripts/` with a name reflecting the retired cadence (e.g. `check-memo-retrospective-headings.py`, `check-overview-roadmap-section.py`); (ii) accept its `CUTOFF_PHASE` (or equivalent boundary) as a module-level integer/string constant so future cadence-policy changes are a single-line edit + memo justification; (iii) be wired into `.github/workflows/spec-health.yml` as a strict gate; (iv) be specced under `spec/27-spec-toolchain/NN-*.md` per the bijection contract (INV-01); (v) include a corresponding AC at §27 in `Verifies` form citing both the retirement memo and the gate constant.
- **And** the **trigger threshold** (3 historical instances + 1 of the 3 drift conditions) is unambiguous: 1–2 instances do NOT qualify (insufficient evidence the cadence is structurally problematic vs. an isolated authorship lapse); 3+ with no observed drift do NOT qualify (the cadence is working — no retirement needed); 3+ with observed drift DO qualify (cadence is structurally fragile and warrants formal retirement + mechanical enforcement).
- **And** the **current registered retirements** MUST be enumerated below; any new retirement extends this table and MUST be cross-referenced from the AC's `Verifies` clause:

  | Retired cadence | Class of artefact | Retirement memo | Mechanical gate | CUTOFF | Trigger phase |
  |---|---|---|---|---|---|
  | "Next phases (queued)" / "Remaining Tasks" / "Future work" / "Roadmap" / "TODO" / "Upcoming" forward-looking H2/H3 sections | `.lovable/memory/audit/v2-deterministic/phase-NNN-*.md` (phase memos) | [`phase-100-memo-freshness-sweep-96-99.md`](../../.lovable/memory/audit/v2-deterministic/phase-100-memo-freshness-sweep-96-99.md) | [`linter-scripts/check-memo-retrospective-headings.py`](../../linter-scripts/check-memo-retrospective-headings.py) (Phase 104, mechanises **AC-31-29**) | `CUTOFF_PHASE = 100` | Phase 100 (verdict) + Phase 104 (gate) |

- **And** the **canonical replacement source of truth** for retired cadences MUST be explicitly named and persistent. For the registered retirement above, the replacement is the **chat-reply "Remaining Tasks" table** maintained per turn by the AI agent, with code-locked items captured in their respective AC `Verifies` clauses. The replacement is a stable, single-writer surface that cannot drift relative to itself (unlike per-memo cadence sections, which by construction can disagree across N memos).
- **And** this AC is **declarative-with-mechanical-companions**: the AC itself does not need a meta-meta-linter scanning for "are there cadences that should be retired?" (such detection requires longitudinal repository analysis the toolchain doesn't perform). Instead, the AC defines the retirement *protocol* — when a contributor or AI agent observes the trigger conditions, the protocol gives a precise checklist (memo + gate + AC + lockstep + registry row). Reviewer attention against the registry catches new retirements that bypass the protocol.
- **And** the **rationale** for codifying this pattern: Phase 100 retired the forward-looking phase-memo cadence after observing concrete drift (Phases 78–83 / 92–93 / 96 all carried "Next phases (queued)" sections that were stale by the time the next phase landed); Phase 104 mechanised the retirement with a CI gate. Without this AC, the next contributor encountering a similar drifting cadence (e.g. recurring "Open questions" sections that get answered in subsequent files but never deleted from the originals) would re-discover the protocol from scratch — and might skip the mechanical-gate step that prevents silent regression.
- **Verifies:** the registered-retirements table above (kept in lockstep with the actual retirement memos + mechanical gates on disk) + [`linter-scripts/check-memo-retrospective-headings.py`](../../linter-scripts/check-memo-retrospective-headings.py) (`CUTOFF_PHASE = 100` constant + `FORBIDDEN_PATTERNS` table — the gate that mechanises the registered retirement) + [`spec/27-spec-toolchain/97-acceptance-criteria.md`](../27-spec-toolchain/97-acceptance-criteria.md) **AC-31-29** (the §27-side AC that locks the gate) + future retirement memos under `.lovable/memory/audit/v2-deterministic/phase-NNN-*-retirement.md`.

### AC-SAG-27 — Enumeration-restatement vs API-surface-use distinction (Phase 115, generalises Phase 114 dismissals)

- **Given** any candidate cross-file pattern that a contributor (human or AI) is considering registering under **AC-31-31** (the multi-file enumeration parity contract at [`spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md`](../27-spec-toolchain/31-audit-spec-vs-code-v2.md)) — i.e. the same conceptual content appears to be referenced across 3 or more files,
- **When** triaging whether the pattern requires a mechanical AC-31-31 parity self-test under `linter-scripts/test/test-*-parity.sh`,
- **Then** the candidate MUST first be classified as either **enumeration-restatement** (parity-test required) or **API-surface-use** (parity-test FORBIDDEN as a category error — at most direct lockstep applies) using the four diagnostic questions below. The classification MUST be recorded in writing — either in the AC-31-31 registry row that approves the new test, OR in the dismissal record at §31's "Currently-NOT-qualifying enumerations" paragraph if the pattern is rejected.

- **Definitions:**
  - **Enumeration-restatement** — the same finite set `S` is fully restated across N≥3 sites, where each site enumerates **all members of S** with the **same domain semantics** AND no site is the canonical source-of-truth that the others mechanically derive from. Example (Phase 112): the §27 inventory triangle restates `{31 specced scripts}` across `00-overview.md` + filesystem + Phase-107 orphan ledger — all three sites enumerate the same set with the same "this script is part of the §27 toolchain" semantics.
  - **API-surface-use** — N≥3 sites each cite a **distinct subset** of a larger set `S` whose canonical enumeration lives in a single source-of-truth (typically the implementation), and each citing site uses only the subset relevant to its local concern. Example (Phase 114 dismissal): the audit-script CLI flag set lives canonically in `audit-spec-vs-code-v2.py`'s `argparse` block; `test-audit-cli-thresholds.sh` cites only `--min-weighted` and `--min-impl`; `.github/workflows/spec-health.yml` cites only `--strict`; §31 spec cites the full set as documentation. No two sites enumerate the same subset, so there is no parity invariant to assert.

- **And** the **four diagnostic questions** MUST be answered in order; a `NO` to ANY of Q1–Q4 disqualifies the pattern from AC-31-31:
  - **Q1 — Same set?** Do all N sites enumerate **the same finite set** (not overlapping subsets, not different subsets of a larger set)? If sites cite different subsets → API surface use, NOT enumeration. (Counter-example: per-script exit-code tables across `check-memo-retrospective-headings.py`, `check-tree-health.cjs`, etc. all share the labels `0`/`1`/`2` but each script's `2` means a different domain failure — they are N independent 2-member enumerations, not one N-site enumeration of a single 3-member set.)
  - **Q2 — Same semantics?** Does each site assign the **same domain meaning** to each member? If sites assign different meanings to identically-spelled members → API surface use. (Counter-example: exit code `1` means "broken links" in `check-spec-cross-links.py` but "stale orphan ledger" in `test-overview-inventory-parity.sh` — same label, different domain, no parity.)
  - **Q3 — No single source-of-truth?** Is there a canonical site (a script's source code, a generator's output, a schema file) that the other sites mechanically derive from? If YES → the canonical site IS the enumeration; the others are documentation/usage and at most need direct lockstep, not parity. (Counter-example: the audit CLI flag set's canonical home is `argparse`; spec docs and tests merely reference subsets — no parity needed.)
  - **Q4 — Silent drift risk?** Could a contributor edit one site without the others noticing for at least 1 PR cycle? If NO (e.g. CI immediately fails on any single-site edit because the runtime invariant is checked at script load time) → AC-31-02–style runtime assertion suffices, no separate parity test needed. (Counter-example: Phase 113 still authored a parity test for WEIGHTS even though AC-31-02 asserts `total == 100` at load — because AC-31-02 only sees the audit script's own dict, not the gate-report's dict or §31's table; silent drift across the 3 sites was demonstrably possible.)

- **And** the **routing rule** is unambiguous:
  - All four `YES` → **enumeration-restatement** → register a row in the AC-31-31 table at §31; author `linter-scripts/test/test-<name>-parity.sh`; bump CI gate count + `RUBRIC_VERSION`; update QA tooling baseline footer; full lockstep cascade.
  - Any `NO` → **API-surface-use** (or single-source enumeration) → record the dismissal in §31's "Currently-NOT-qualifying enumerations" paragraph with the failing question number + one-sentence rationale; direct lockstep via `check-lockstep.cjs` MAY apply if 2 sites are tightly coupled, but **no AC-31-31 parity test is authored**. Authoring a parity test for an API-surface-use pattern is a **category error** — it would require inventing artificial cross-site constraints that don't reflect the actual contract.

- **And** the **worked Phase-114 dismissal record** (preserved here as the canonical training set for future contributors) MUST stay in lockstep with §31's "Currently-NOT-qualifying enumerations" paragraph; any new dismissal there extends the table below:

  | Candidate pattern | Sites | Failing Q | Reason | Disposition |
  |---|---|---|---|---|
  | Audit-script CLI flag set (`--min-weighted` / `--min-impl` / `--strict` / `--explain` / `--deterministic`) | script `argparse` + §31 spec + workflow + 4 self-tests | Q1 | Each site cites a different subset; no two sites enumerate the same set | API surface use — `argparse` is canonical; no parity test |
  | Per-script exit-code tables (`0`/`1`/`2` across `check-memo-retrospective-headings.py`, `check-memory-mirror-drift.py`, `check-root-readme.py`, `check-tree-health.cjs`, etc.) | N scripts × N spec tables | Q2 | Same labels, different domain semantics per script | N independent 2-site enumerations — direct lockstep per script, no cross-script parity |
  | Audit-script exit-code table (0/1/2) | script source + §31 spec table | Q3 (and only 2 sites) | Script source is canonical; spec table is documentation derived from it | Direct lockstep via `check-lockstep.cjs`; not 3+ sites so AC-31-31 doesn't fire anyway |
  | CI threshold floors (`--min-weighted=97 --min-impl=99`) | `.github/workflows/spec-health.yml` + `test-audit-cli-thresholds.sh` | (only 2 sites) | Below the 3-site threshold | Direct lockstep; AC-31-31 doesn't fire |
  | Gate-cap thresholds (95/90/85/70 in score-band rubric) | each cap is single-site | Q1 | Each cap appears in exactly one place with rationale | Single-site magic numbers; not enumerations |

- **And** the **rationale** for promoting this distinction to a §01 meta-spec AC (rather than leaving it inline in §31's prose where Phase 114 originally landed it): §01 is the meta-spec that governs how *every* future spec author thinks about cross-file contracts. AC-31-31 is the §27-side mechanism for one specific pattern (multi-file enumerations within the toolchain); but the underlying triage discipline — "is this an enumeration or an API surface?" — applies whenever any spec module considers a parity test. Without AC-SAG-27 codifying the four diagnostic questions at the meta-spec level, future contributors authoring parity tests in `spec/22-git-logs-v2/` or `spec/04-database-conventions/` (e.g. for a multi-file SQL DDL enumeration or a multi-file enum-value table) would re-derive the triage from scratch — and might author a category-error parity test that locks an API surface and breaks the next legitimate API extension.

- **And** this AC is **declarative-with-runtime-companion**: the four diagnostic questions are a triage protocol applied by the contributor at authoring time; there is no automated meta-meta-linter that scans the codebase for "are there candidate patterns that should be triaged?" (such detection would require longitudinal repo analysis the toolchain does not perform). The runtime companion is the AC-31-31 registry table itself + §31's "Currently-NOT-qualifying enumerations" paragraph — both maintained in lockstep with this AC's worked-dismissal table, both reviewable as a single artefact during audit. New parity tests landing without a registry row OR new dismissals landing without an entry in either table are caught by reviewer attention against the cross-referenced lockstep.

- **Verifies:** the worked-dismissal table above (kept in lockstep with §31's "Currently-NOT-qualifying enumerations" paragraph) + [`spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md`](../27-spec-toolchain/31-audit-spec-vs-code-v2.md) **AC-31-31** (the §27-side mechanical-parity contract that this meta-AC's triage protocol gatekeeps) + Phase 114 memo at [`.lovable/memory/audit/v2-deterministic/phase-114-ac-31-31-contract-bounding.md`](../../.lovable/memory/audit/v2-deterministic/phase-114-ac-31-31-contract-bounding.md) (the empirical bounding sweep that surfaced the four dismissed patterns) + Phase 115 memo at [`.lovable/memory/audit/v2-deterministic/phase-115-enumeration-vs-api-surface-distinction.md`](../../.lovable/memory/audit/v2-deterministic/phase-115-enumeration-vs-api-surface-distinction.md) (the promotion rationale + triage protocol authoring record).

### AC-SAG-28 — `## Legacy Index` AC headings are EXEMPT from GWT-completeness audits (Phase P7b)

- **Given** any module-level `97-acceptance-criteria.md` containing a `## Legacy Index (preserved for traceability)` (or equivalently-titled "Legacy Index", "Legacy ACs", "Preserved Index") section AND that section contains `### AC-*-LEGACY*` headings whose bodies are intentionally Markdown table rows (NOT Given/When/Then stanzas)
- **When** any audit, linter, or contributor sweeps the file for GWT-completeness (e.g. the Phase P7 mechanical regex audit `re.split(r'^### (AC-[\w-]+)', txt, flags=re.M)` over §22, or any future `check-ac-gwt-completeness.py` toolchain script)
- **Then** AC headings whose ID matches the regex `^AC-[A-Z]+-LEGACY(-\d+)?$` (where the prefix may be e.g. `SAG`, `CG`, `SD`, `SC`, `T`, etc.) MUST be **excluded** from the GWT-completeness denominator AND MUST NOT be reported as "non-GWT" findings; AND the exclusion is justified because (a) these rows are *deliberately preserved* for traceability — they are referenced from the new GWT ACs' `Verifies:` chains (e.g. `Verifies: ... + AC-SD-LEGACY-001-a` in §05 AC-SD-02) and removing them would silently break those cross-refs; (b) the new GWT ACs *supersede* them as the authoritative contract — the audit risk that was originally highest-priority (test-name drift from one-line ACs, per GAP-V2-01) was eliminated when the GWT replacements landed; (c) re-authoring the legacy index as GWT would balloon §97 length without adding new contract surface (each LEGACY row corresponds to ≥1 GWT AC already on file). The exemption applies REGARDLESS of how many LEGACY rows a module carries — a module with 22 LEGACY rows + 20 GWT ACs scores `gwt_completeness = 20/20 = 100%`, NOT `20/42 = 48%`. The exemption does NOT apply to non-LEGACY ACs that lack GWT — those remain audit findings (see §22 v3.9.6 / Phase P7 close as the worked example: 76/76 ACs all GWT, zero LEGACY rows, audit `incomplete = 0`).
- **And** the **enumeration of currently-affected modules** (kept in lockstep with this AC, refreshed when any LEGACY index changes):

  | Module | LEGACY rows | GWT ACs | GWT-completeness (post-exemption) |
  |---|--:|--:|---|
  | `spec/01-spec-authoring-guide/97-acceptance-criteria.md` | 4 (AC-SAG-LEGACY: Folder Structure / Naming Conventions / Overview Content Standards / Cross-References & Validation — each containing 4–6 sub-rows) | 28 (AC-SAG-01..AC-SAG-28) | 100% |
  | `spec/02-coding-guidelines/97-acceptance-criteria.md` | 5 (AC-CG-LEGACY: Cross-Language + 4 sibling categories) | 20 (AC-CG-01..AC-CG-20) | 100% |
  | `spec/05-split-db-architecture/97-acceptance-criteria.md` | 2 (AC-SD-LEGACY-001, AC-SD-LEGACY-002 — each with sub-checkboxes -a/-b/-c referenced from new ACs) | 20 (AC-SD-01..AC-SD-20) | 100% |
  | `spec/06-seedable-config-architecture/97-acceptance-criteria.md` | 2 (AC-SC-LEGACY-001, AC-SC-LEGACY-002 — same sub-checkbox shape as §05) | 20 (AC-SC-01..AC-SC-20) | 100% |

- **And** the **canonical exemption regex** for downstream tools is `^AC-[A-Z]+-LEGACY(-\d+)?$` — case-sensitive, anchored at both ends. New module prefixes (e.g. a future §10 might introduce `AC-DV-LEGACY-*`) inherit the exemption automatically without amending this AC. Modules introducing a Legacy Index for the first time MUST (1) add a `## Legacy Index (preserved for traceability)` heading using the exact wording, (2) prefix preserved IDs with `<MODULE-ABBR>-LEGACY` matching the regex, (3) leave a top-of-file banner note documenting which Phase performed the GWT rewrite (precedent: §05 v4.0.0 Phase 16r banner; §02 Phase 16e banner; §06 v4.0.0 Phase 16r banner; §01 v3.2.0 → current via Phases 16d/e/f), AND (4) ensure every preserved LEGACY row is referenced by at least one new GWT AC's `Verifies:` chain so the traceability claim is empirically true.
- **And** the runtime companion to this AC is the **`canonical exemption regex`** above — any future `check-ac-gwt-completeness.py` (currently unwritten — would be a §27 toolchain addition) MUST hardcode this regex AND emit a banner line `excluding N LEGACY ACs across M modules per AC-SAG-28` so the exemption is visible in every audit run. The exemption MUST NOT be silently applied — visibility prevents the inverse failure mode where a Legacy Index grows unboundedly because no one notices it never participates in the audit denominator.
- **Verifies:** `## Legacy Index (preserved for traceability)` section in this file (lines 300+) AND the four currently-affected modules' Legacy Index sections (`spec/02-coding-guidelines/97-acceptance-criteria.md` line 363+, `spec/05-split-db-architecture/97-acceptance-criteria.md` end-of-file LEGACY block, `spec/06-seedable-config-architecture/97-acceptance-criteria.md` end-of-file LEGACY block) AND `spec/22-git-logs-v2/37-blind-ai-gap-analysis.md` v1.3.0 Phase P7 entry (which surfaced the discovery that §22 carries zero LEGACY rows — its 76/76 GWT score is unaffected by this AC) AND `spec/22-git-logs-v2/98-changelog.md` v3.9.7 (Phase P7b row documenting the codification of this exemption + the four-module exemption table snapshot).

---

### AC-SAG-29 — Sibling-module references are LINKS, not stub gaps (Lesson #29 + Lesson #36 — Phase 153)  `[critical]`

- **Given** spec/01-spec-authoring-guide is the **meta-spec** governing every other module under `spec/` AND its prose necessarily references sibling modules by relative path (e.g. `../02-coding-guidelines/`, `../03-error-manage/`, `../04-database-conventions/`, `../17-consolidated-guidelines/`, `../22-git-logs-v2/`, `../27-spec-toolchain/`)
- **When** an LLM auditor (e.g. `linter-scripts/audit-ai-implementability.py`) bundles spec/01's normative surface with the deep-walker tier-1 90 KB cap and reports `[D5] Dangling External Module References` because the sibling module bodies are NOT inlined in the bundle
- **Then** every sibling-module reference enumerated below MUST be treated as a **resolved cross-module link**, NOT a missing-context defect:
  - `../02-coding-guidelines/` (35-file module, present on disk — verified 2026-04-29)
  - `../03-error-manage/` (12-file root + 8-subfolder tree, present on disk — verified 2026-04-29; covered by spec/03 AC-08 asset-inventory pin)
  - `../04-database-conventions/` (9-file module, present on disk — verified 2026-04-29; spec/04 AC-09 binds boolean storage convention)
  - `../17-consolidated-guidelines/` (35-file rollup module, present on disk; covered by spec/17 AC-10 module-kind pin)
  - `../22-git-logs-v2/` (40+ file module, present on disk)
  - `../27-spec-toolchain/` (60+ file linter-script registry, present on disk)
- **And** auditors that flag any of the above as "dangling" or "missing" are operating on a **bundling-cap artifact** (Lesson #29 deep-tree variant — the auditor's bundle does not include sibling-module bodies because the spec/01 tier-1 files already exhaust the 90 KB budget); the spec is NOT defective, the audit harness is not configured to pre-load sibling modules
- **And** spec/01 MUST link to sibling modules by relative path (not inline their content) per Lesson #36 (cross-module cross-references MUST link, never restate) — restating sibling module rules in spec/01 would create a dual-source drift class where the meta-spec contradicts the modules it is supposed to govern
- **And** the canonical fix when this finding surfaces is (a) re-bundle the auditor with `--include-siblings spec/02 spec/03 spec/04 spec/17 spec/22 spec/27` once that flag exists, OR (b) cite this AC and downgrade the finding to **harness-artifact**, NEVER edit spec/01 to remove the sibling references
- **Verifies:** the meta-spec's link-don't-restate posture toward sibling modules (Lesson #36) + the deep-tree audit-walker artifact class (Lesson #29 fifth tree-wide application after spec/25/11/12/17 + spec/03/18 in same session); cross-references `mem://process/phase-153-lessons` Section F (Audit-Corpus Modules) AND each sibling module's own asset-inventory pin AC where applicable
- **Source:** `mem://process/phase-153-lessons` (Lessons #29, #34, #36); spec/03 AC-08 (asset-inventory deep-tree precedent, 2026-04-29); spec/18 AC-09 (asset-inventory + cache-staleness precedent, 2026-04-29).

### AC-SAG-30 — Linter-script logic is anchored to spec/27 slot registry, not restated (Lesson #36 — Phase 153)  `[high]`

- **Given** spec/01 enumerates the 6 mandatory linter gates (`check-tree-health.cjs`, `check-lockstep.cjs`, `check-spec-cross-links.py`, `generate-spec-index.cjs`, `audit-spec-vs-code-v2.py`, `run.sh`) as part of the meta-spec contract (`10-mandatory-linter-infrastructure.md` + §97 INLINED `LINTER_GATES` block)
- **When** an LLM auditor reports `[D3] Linter Script Implementation Gap` because spec/01 describes the gates by **metadata** (name + exit-code + threshold) rather than implementation logic or pseudo-code
- **Then** this MUST be treated as a **harness-artifact**, NOT a defect: implementation logic for every linter script is canonically owned by `spec/27-spec-toolchain/` (60+ slot registry, one slot per script with its own §97 GWT contract — e.g. `spec/27/03-runner/`, `spec/27/14-tree-health/`, `spec/27/22-lockstep/`)
- **And** spec/01 MUST link to spec/27 slots by relative path, NEVER restate the per-script GWT logic — restating would create a dual-source drift class (Lesson #36) where the meta-spec's prose contradicts the canonical slot's §97 contract
- **And** the canonical fix when this finding surfaces is (a) re-bundle the auditor with the relevant spec/27 slot's §97 in context, OR (b) cite this AC and downgrade to **harness-artifact**
- **Verifies:** the meta-spec's link-don't-restate posture toward toolchain implementation (Lesson #36 second co-application after AC-SAG-29) + the spec/27 slot-registry as single source of truth for linter logic
- **Source:** `mem://process/phase-153-lessons` (Lessons #36, #37 integration-axis co-application); spec/12 AC-11 precedent (linter-script cross-ref anchoring, Phase 153 A24-fu4).

### AC-SAG-31 — Inlined-schema versions follow per-contract SemVer, not module banner (Phase 153)  `[low]`

- **Given** §00 / §97 prose may reference inlined contracts authored at specific phases (e.g. "Phase 48 schema", "Phase 52 contract") AND the module banner version (`v4.x.y`) tracks module-level lockstep (banner + §98 + §99) — these are TWO orthogonal versioning axes
- **When** an LLM auditor reports `[D1] Version/Phase Discrepancy` because the module banner says `v4.13.3 / Phase 153` but inlined contract sections cite `Phase 48` or `Phase 52`
- **Then** this MUST be treated as **non-discrepancy**: each inlined contract pins to its **authoring phase** (the phase that introduced the schema), which is a stable historical reference. The module banner advances on every patch; the inlined-contract phase pin does NOT advance unless the contract itself is rev'd (which would require a §98 row + a new phase pin)
- **And** "synchronizing all inlined schemas to current phase" is **forbidden** — it would erase the audit trail of which schema version is in force AND mask silent contract drift
- **And** the canonical fix when this finding surfaces is to cite this AC and downgrade to **non-discrepancy**; auditors SHOULD distinguish *module-level lockstep version* (banner) from *contract-authoring phase pin* (inlined references)
- **Verifies:** the dual-axis versioning contract (module SemVer ⊥ contract authoring-phase pin) + the audit-trail-preservation rule (Lesson #25 dual-track SemVer corollary)
- **Source:** `mem://process/phase-153-lessons` (Lesson #25 dual-track SemVer); Phase 153 Task #32 SemVer-track unification precedent (spec/07).

---
## Legacy Index (preserved for traceability)

The following table-row criteria from v3.2.0 are preserved verbatim. They are NO LONGER authoritative — the GWT ACs above supersede them.

### AC-SAG-LEGACY: Folder Structure & Required Files

- **Verifies:** the v3.2.0 → current GWT-rewrite traceability chain — these table-row criteria are referenced by `Verifies:` chains of the new GWT ACs above (notably AC-SAG-01, AC-SAG-11, AC-SAG-12) and by AC-SAG-28's exemption registry. Removing them silently breaks those cross-refs (Phase P7b precedent). The mechanical exemption regex `^AC-[A-Z]+-LEGACY(-\d+)?$` in any future `check-ac-gwt-completeness.py` MUST exclude this row from the GWT-completeness denominator.

| ID | Criterion | Source |
|---|---|---|
| AC-SAG-LEGACY-001 | Every spec module has `00-overview.md` at root | `03-required-files.md` |
| AC-SAG-LEGACY-002 | Every spec module has `99-consistency-report.md` at root | `03-required-files.md` |
| AC-SAG-LEGACY-003 | CLI modules follow 3-folder pattern (`01-backend/`, `02-frontend/`, `03-deploy/`) | `04-cli-module-template.md` |
| AC-SAG-LEGACY-004 | Subfolders with 3+ files include their own `00-overview.md` | `03-required-files.md` |

### AC-SAG-LEGACY: Naming Conventions

- **Verifies:** the v3.2.0 → current GWT-rewrite traceability chain — these rows are referenced by `Verifies:` chains of AC-SAG-02, AC-SAG-03, AC-SAG-04 above and by AC-SAG-28's exemption registry. Same exemption-regex contract as the prior LEGACY block.

| ID | Criterion | Source |
|---|---|---|
| AC-SAG-LEGACY-005 | All files use lowercase kebab-case naming | `02-naming-conventions.md` |
| AC-SAG-LEGACY-006 | All folders use lowercase kebab-case naming | `02-naming-conventions.md` |
| AC-SAG-LEGACY-007 | All spec files have unique numeric sequence prefixes within their folder | `02-naming-conventions.md` |
| AC-SAG-LEGACY-008 | Reserved prefixes (00, 97, 98, 99) used only for their designated purposes | `02-naming-conventions.md` |

### AC-SAG-LEGACY: Overview Content Standards

- **Verifies:** the v3.2.0 → current GWT-rewrite traceability chain — these rows are referenced by `Verifies:` chains of AC-SAG-05, AC-SAG-16, AC-SAG-17 above and by AC-SAG-28's exemption registry. Same exemption-regex contract as the prior LEGACY blocks.

| ID | Criterion | Source |
|---|---|---|
| AC-SAG-LEGACY-009 | Every `00-overview.md` includes Version and Updated metadata | `00-overview.md` |
| AC-SAG-LEGACY-010 | Every `00-overview.md` includes AI Confidence score | `00-overview.md` |
| AC-SAG-LEGACY-011 | Every `00-overview.md` includes Ambiguity score | `00-overview.md` |
| AC-SAG-LEGACY-012 | Every `00-overview.md` includes Keywords section | `00-overview.md` |
| AC-SAG-LEGACY-013 | Every `00-overview.md` includes Scoring table | `00-overview.md` |
| AC-SAG-LEGACY-014 | Every `00-overview.md` includes numbered file inventory table | `00-overview.md` |
| AC-SAG-LEGACY-015 | Every `00-overview.md` includes Cross-References table | `00-overview.md` |

### AC-SAG-LEGACY: Cross-References & Validation

- **Verifies:** the v3.2.0 → current GWT-rewrite traceability chain — these rows are referenced by `Verifies:` chains of AC-SAG-09, AC-SAG-10, AC-SAG-19 above and by AC-SAG-28's exemption registry. Same exemption-regex contract as the prior LEGACY blocks.

| ID | Criterion | Source |
|---|---|---|
| AC-SAG-LEGACY-016 | All cross-references use relative paths (never root-relative or absolute) | `08-cross-references.md` |
| AC-SAG-LEGACY-017 | All linked files include `.md` extension | `08-cross-references.md` |
| AC-SAG-LEGACY-018 | Zero broken links reported by dashboard scanner | `08-cross-references.md` |

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Required Files](./03-required-files.md)
- [Naming Conventions](./02-naming-conventions.md)
- [Cross-References Guide](./08-cross-references.md)
- [Mandatory Linter Infrastructure](./10-mandatory-linter-infrastructure.md)
- [Coding Guidelines parent governance](../02-coding-guidelines/97-acceptance-criteria.md)
- [Spec Toolchain](../27-spec-toolchain/97-acceptance-criteria.md)
