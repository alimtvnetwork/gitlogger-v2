# Acceptance Criteria: Static Analysis & Linter Enforcement

**Version:** 4.1.0
**Last Updated:** 2026-04-26 (Phase 16p: full GWT rewrite — replaced 7 stub checkboxes with 20 module-specific Given/When/Then ACs covering SonarQube→linter mapping, threshold enforcement, and CI quality gate. Old stubs preserved as AC-SA-LEGACY-* at end.)
**Scope:** `spec/02-coding-guidelines/01-cross-language/16-static-analysis/` — Cross-language static analysis rule mapping, SonarQube coverage, linter configuration, and unified CI quality gate.

---

## Module Summary

§02/01/16-static-analysis codifies the contract for mapping every enforceable coding guideline to a concrete linter rule across 8 languages (TypeScript, Go, PHP, C#, Rust, VB.NET, Node.js, Python). It defines: universal thresholds (15-line functions, 3 params, complexity ≤ 10, nesting ≤ 1), SonarQube rule ID coverage (S138, S107, S3776, S134, S1126, S4144, S1481/S1144), per-language linter configuration with exact rule names and config values, a unified CI quality gate referencing all 8 languages, and the cross-language rule matrix as a side-by-side comparison table. Every rule mapping MUST be bidirectional: the spec → linter config AND the linter finding → spec rule. Inherits ALL **AC-CL-01..AC-CL-20** per AC-CL-01.

---

## Inlined Contracts

```text
PARENT_INHERITANCE:        ../01-cross-language/97 (AC-CL-01..AC-CL-20)
LANGUAGES_COVERED:         8 (TypeScript, Go, PHP, C#, Rust, VB.NET, Node.js, Python)
SONARQUBE_RULES:           7 (S138, S107, S3776, S134, S1126, S4144, S1481/S1144)
UNIVERSAL_THRESHOLDS:
  Function length:         ≤ 15 lines
  Parameter count:         ≤ 3
  Cognitive complexity:    ≤ 10
  Nesting depth:           ≤ 1
LINTER_CONFIG_FORMAT:      Per-language Markdown file with {Rule ID, Linter, Rule Name, Config} table
CI_QUALITY_GATE:           Unified gate in 09-ci-pipeline-quality-gate.md
RULE_MATRIX_FORMAT:        Side-by-side Markdown table: Language × SonarQube Rule
```

---

## Acceptance Criteria

### AC-SA-01 — Inherits all AC-CL-01..AC-CL-20 from cross-language parent

- **Given** any artifact (doc, config, script, matrix table) under `16-static-analysis/`,
- **When** reviewed,
- **Then** it MUST satisfy every AC-CL-* rule from `../01-cross-language/97-acceptance-criteria.md`. Conflicts MUST resolve in favor of the cross-language rule per AC-CL-01. Any waiver (e.g., AC-CL-12 file naming for `.editorconfig` files) MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** AC-CL-01 inheritance contract.

### AC-SA-02 — Exactly 8 language linter specs, each with dedicated {NN}-<lang>-<tool>.md file

- **Given** the `16-static-analysis/` folder,
- **When** its file inventory is listed,
- **Then** it MUST contain EXACTLY 8 language-specific linter spec files: `02-go-golangci-lint.md`, `03-php-phpcs-phpstan.md`, `04-csharp-stylecop.md`, `05-rust-clippy.md`, `06-vb-dotnet-analyzers.md`, `07-nodejs-eslint.md`, `08-python-ruff.md`. TypeScript ESLint lives at `../../02-typescript/11-eslint-enforcement.md` (cross-referenced, not duplicated). A 9th language file OR a missing language file FAILS this AC. Each file MUST contain: (a) a `{Rule ID, Linter, Rule Name, Config}` table with ≥ 10 rows, (b) a `## Exemptions` section documenting suppression syntax, (c) a `## CI Integration` subsection with copy-pasteable config snippet.
- **Verifies:** `00-overview.md` Document Inventory + AC-SA-LEGACY-001.

### AC-SA-03 — All 8 specs enforce identical universal thresholds: 15-line functions, 3 params, complexity ≤ 10, nesting ≤ 1

- **Given** any of the 8 language linter spec files,
- **When** their threshold tables are compared,
- **Then** EVERY spec MUST declare the SAME four values: (a) max function length = 15 lines, (b) max parameters = 3, (c) max cognitive complexity = 10, (d) max nesting depth = 1. ANY deviation (e.g., one language allows 20-line functions) FAILS this AC. The threshold MUST be enforced by the linter configuration (not merely documented). Each spec's CI snippet MUST include the linter flag that enforces the threshold (e.g., `--max-lines-per-function 15`, `funlen: 15`).
- **Verifies:** `10-cross-language-rule-matrix.md` §1 Universal Thresholds + AC-SA-LEGACY-002.

### AC-SA-04 — Every enforceable rule maps to a SonarQube rule ID; every SonarQube rule maps to ≥ 1 linter rule

- **Given** the `10-cross-language-rule-matrix.md` file,
- **When** its rule mapping tables are parsed,
- **Then** EVERY enforceable guideline MUST have a `SonarQube` column with a valid rule ID (e.g., `S138`, `S107`, `S3776`, `S134`, `S1126`, `S4144`, `S1481`/`S1144`). EVERY SonarQube rule ID in the matrix MUST have ≥ 1 corresponding linter rule entry across the 8 languages. Orphan SonarQube IDs (no linter mapping) OR orphan linter rules (no SonarQube ID) FAIL this AC. The matrix MUST cover at minimum these 7 SonarQube rules: S138 (function length), S107 (parameter count), S3776 (cognitive complexity), S134 (nesting depth), S1126 (redundant boolean), S4144 (duplicate method), S1481/S1144 (unused variable).
- **Verifies:** `10-cross-language-rule-matrix.md` §2 SonarQube Rule → Linter Rule Matrix + AC-SA-LEGACY-003.

### AC-SA-05 — Integration checklist uses standardized table format with 🔲 status per language

- **Given** any language spec file under `16-static-analysis/`,
- **When** its integration checklist section is located,
- **Then** it MUST use a Markdown table with header columns EXACTLY: `Status | Rule | Linter | Config | Notes`. The `Status` column MUST use 🔲 (unchecked) or ✅ (checked) emoji — text-only `[]` or `[x]` is FORBIDDEN. Each row MUST represent one linter rule. The table MUST contain ≥ 10 rows. A checklist in prose bullet form OR without the 🔲/✅ status column FAILS this AC.
- **Verifies:** `00-overview.md` integration checklist format + AC-SA-LEGACY-004.

### AC-SA-06 — CI pipeline spec defines a unified quality gate referencing all 8 languages with fail-on-error

- **Given** `09-ci-pipeline-quality-gate.md`,
- **When** its quality gate section is parsed,
- **Then** it MUST define a SINGLE unified gate that: (a) runs ALL 8 language linter suites in parallel (not sequential), (b) fails the pipeline if ANY suite emits `level: error` findings, (c) produces a SINGLE aggregated SARIF artifact uploaded to the CI platform's code-scanning UI, (d) references each language by its canonical spec file path (e.g., `../../02-typescript/11-eslint-enforcement.md`), (e) includes copy-pasteable GitHub Actions AND GitLab CI YAML snippets. A gate that runs languages sequentially OR produces per-language separate artifacts OR lacks the YAML snippets FAILS this AC.
- **Verifies:** `09-ci-pipeline-quality-gate.md` + AC-SA-LEGACY-005.

### AC-SA-07 — Cross-language rule matrix covers all 7 SonarQube rules across all 8 languages with coverage badges

- **Given** `10-cross-language-rule-matrix.md`,
- **When** its coverage summary is parsed,
- **Then** it MUST contain an 8×8 matrix (Language × SonarQube Rule) showing which rules are enforced NATIVE (✅), enforced via FALLBACK/reviewer (🟡), or NOT enforced (❌). The matrix MUST cover ALL 8 languages (TypeScript, Go, PHP, C#, Rust, VB.NET, Node.js, Python) and ALL 7 SonarQube rules (S138, S107, S3776, S134, S1126, S4144, S1481/S1144). A matrix missing a language OR a rule OR without the coverage badges FAILS this AC. The matrix MUST be machine-parseable (Markdown table, not image or Mermaid diagram).
- **Verifies:** `10-cross-language-rule-matrix.md` §3 Coverage Summary + AC-SA-LEGACY-006.

### AC-SA-08 — TypeScript ESLint spec cross-referenced from overview, lives at `../../02-typescript/11-eslint-enforcement.md`

- **Given** `00-overview.md` Document Inventory,
- **When** the TypeScript row is examined,
- **Then** it MUST reference `../../02-typescript/11-eslint-enforcement.md` (relative path from `16-static-analysis/` to the TypeScript folder) with a hyperlink, NOT duplicate the spec inline. The overview MUST NOT contain a `01-typescript-eslint.md` file — that slot is intentionally vacant (01 reserved for the cross-ref). The `11-eslint-enforcement.md` file MUST exist at the target path and MUST contain a `{Rule ID, Linter, Rule Name, Config}` table with ≥ 10 rows. A broken cross-reference link OR an inline duplicate OR a missing target file FAILS this AC.
- **Verifies:** `00-overview.md` Document Inventory + `../../02-typescript/11-eslint-enforcement.md` existence.

### AC-SA-09 — Every language spec includes Keywords and Scoring sections

- **Given** any of the 8 language spec files (or the TypeScript cross-reference target),
- **When** its frontmatter is parsed,
- **Then** it MUST contain a `## Keywords` section with ≥ 3 comma-separated keywords AND a `## Scoring` section with a Markdown table containing at minimum the rows: `00-overview.md present | ✅`, `AI Confidence assigned | ✅`, `Ambiguity assigned | ✅`, `Keywords present | ✅`, `Scoring table present | ✅`. A spec missing either section OR with empty keywords OR without the scoring table FAILS this AC.
- **Verifies:** AC-SA-LEGACY-002 + all 8 language spec files.

### AC-SA-10 — Every language spec documents exemption/suppression syntax with before/after examples

- **Given** any of the 8 language spec files,
- **When** its `## Exemptions` section is parsed,
- **Then** it MUST contain: (a) the EXACT suppression syntax for that language's linter (e.g., `// eslint-disable-next-line max-lines-per-function` for ESLint, `//nolint:funlen` for golangci-lint, `// phpcs:ignore Generic.Metrics.FunctionLength` for PHPCS), (b) a `❌ Before` example showing the violation WITH suppression comment, (c) a `✅ After` example showing the refactored code WITHOUT suppression (suppression is a smell, not a solution), (d) a `⚠️ Permitted` subsection listing the 3 allowed exemption categories: (1) generated code, (2) third-party vendored code, (3) performance-critical hot paths with benchmark proof. Any other suppression reason FAILS this AC. A spec missing the `## Exemptions` section OR without before/after examples OR without the 3 permitted categories FAILS this AC.
- **Verifies:** AC-SA-LEGACY-003 + all 8 language spec files.

### AC-SA-11 — CI pipeline quality gate runs all 8 languages in parallel with single aggregated SARIF artifact

- **Given** `09-ci-pipeline-quality-gate.md`,
- **When** its CI template sections are parsed,
- **Then** it MUST contain copy-pasteable YAML for BOTH GitHub Actions AND GitLab CI. Each template MUST: (a) define a `lint` job/stage that runs ALL 8 language suites in parallel (matrix strategy or parallel steps, NOT sequential), (b) upload a SINGLE aggregated SARIF file to the platform's code-scanning UI (`github/codeql-action/upload-sarif` for GitHub, `code_quality` artifact for GitLab), (c) fail the pipeline on ANY `level: error` finding, (d) include a `workflow_dispatch` trigger (GitHub) or `workflow` keyword (GitLab) for manual runs. A template running languages sequentially OR producing per-language SARIFs OR missing either platform's YAML FAILS this AC.
- **Verifies:** `09-ci-pipeline-quality-gate.md` + AC-SA-LEGACY-005.

### AC-SA-12 — Cross-language rule matrix is machine-parseable 8×8 with coverage badges

- **Given** `10-cross-language-rule-matrix.md`,
- **When** its coverage summary is parsed,
- **Then** it MUST contain a Markdown table with EXACTLY 9 columns: `SonarQube Rule | TypeScript | Go | PHP | C# | Rust | VB.NET | Node.js | Python`. The header row MUST use exact language names (not abbreviations). There MUST be EXACTLY 7 data rows (one per SonarQube rule: S138, S107, S3776, S134, S1126, S4144, S1481/S1144). Each cell MUST contain ONE of: `✅` (native linter enforcement), `🟡` (fallback/reviewer enforcement), or `❌` (not enforced). Empty cells OR freeform text OR emoji other than these three FAIL this AC. The table MUST be machine-parseable (standard Markdown pipe table, no HTML, no images, no Mermaid). A script parsing the table MUST be able to extract the coverage status for any {language, rule} pair without regex heuristics.
- **Verifies:** `10-cross-language-rule-matrix.md` §3 Coverage Summary + AC-SA-LEGACY-006.

### AC-SA-13 — Every SonarQube rule has a "native" (✅) mapping in ≥ 4 languages

- **Given** the coverage matrix from AC-SA-12,
- **When** each SonarQube rule row is tallied,
- **Then** EVERY rule MUST have `✅` (native enforcement) in at MINIMUM 4 of the 8 languages. A rule with only 3 or fewer `✅` mappings is a coverage gap and MUST be documented in `99-consistency-report.md` with a remediation plan (e.g., "Add PHPCS custom sniff for S3776"). Rules with 0 `✅` across all 8 languages MUST be removed from the matrix (they are unenforceable fantasies). This AC ensures the matrix represents reality, not aspiration.
- **Verifies:** `10-cross-language-rule-matrix.md` + `99-consistency-report.md` coverage gap table.

### AC-SA-14 — Linter configuration is version-pinned and reproducible

- **Given** any linter config file referenced by a language spec,
- **When** its version is examined,
- **Then** EVERY linter tool version MUST be pinned to an exact SemVer (e.g., `eslint@8.57.0`, `golangci-lint@v1.57.2`, `phpstan@1.10.59`). `latest` tags, floating minor ranges (`^1.0.0`), or unpinned installs are FORBIDDEN — they cause non-reproducible CI failures when a linter releases a new rule. Each spec MUST include a `## Tool Versions` subsection listing the pinned version AND a `## Reproducing` subsection with the EXACT install command (e.g., `npm install eslint@8.57.0 --save-dev`). The version pin MUST be updated within 30 days of a new stable release (tracked in `99-consistency-report.md` Validation History).
- **Verifies:** All 8 language spec files + `99-consistency-report.md`.

### AC-SA-15 — Every language spec includes a copy-pasteable CI config snippet

- **Given** any of the 8 language spec files,
- **When** its `## CI Integration` section is parsed,
- **Then** it MUST contain a fenced code block (language-yaml or language-json) with a copy-pasteable configuration snippet for that language's linter. The snippet MUST be complete (not pseudo-code): for GitHub Actions, it MUST include `name`, `on`, `jobs`, `steps` with `uses`, `with`, and `run`; for GitLab CI, it MUST include `stages`, `variables`, `script`, and `artifacts`. The snippet MUST reference the version-pinned tool from AC-SA-14. A `## CI Integration` section with only prose description OR pseudo-code OR missing version pin FAILS this AC.
- **Verifies:** All 8 language spec files + `09-ci-pipeline-quality-gate.md`.

### AC-SA-16 — Suppression syntax is documented with 3 permitted categories and before/after examples

- **Given** any of the 8 language spec files,
- **When** its `## Exemptions` section is parsed,
- **Then** it MUST contain: (a) the EXACT suppression comment/syntax for that language (e.g., `// eslint-disable-next-line rule-name` for ESLint, `//nolint:rule-id` for golangci-lint, `// phpcs:ignore Standard.Category.Sniff` for PHPCS, `#pragma warning disable ID` for Roslyn, `#[allow(clippy::rule)]` for Clippy), (b) a `❌ Before` code example showing the violation WITH suppression comment (smell), (c) a `✅ After` code example showing the refactored code WITHOUT suppression (preferred), (d) a `⚠️ Permitted` subsection listing EXACTLY 3 allowed exemption categories: (1) generated code (auto-generated by tool, never hand-edited), (2) third-party vendored code (external dependency copied into repo), (3) performance-critical hot path with benchmark proof (microsecond-level, reproducible benchmark attached). Any other suppression reason FAILS this AC. A spec missing the `## Exemptions` section OR without before/after examples OR without the 3 permitted categories FAILS this AC.
- **Verifies:** All 8 language spec files + AC-SA-LEGACY-003.

### AC-SA-17 — The cross-language rule matrix is a machine-parseable 8×8 Markdown table with coverage badges

- **Given** `10-cross-language-rule-matrix.md`,
- **When** its coverage summary is parsed,
- **Then** it MUST contain a Markdown table with EXACTLY 9 columns: `SonarQube Rule | TypeScript | Go | PHP | C# | Rust | VB.NET | Node.js | Python`. The header row MUST use exact language names (not abbreviations). There MUST be EXACTLY 7 data rows (one per SonarQube rule: S138, S107, S3776, S134, S1126, S4144, S1481/S1144). Each cell MUST contain ONE of: `✅` (native linter enforcement), `🟡` (fallback/reviewer enforcement), or `❌` (not enforced). Empty cells OR freeform text OR emoji other than these three FAIL this AC. The table MUST be machine-parseable (standard Markdown pipe table, no HTML, no images, no Mermaid). A script parsing the table MUST be able to extract the coverage status for any {language, rule} pair without regex heuristics.
- **Verifies:** `10-cross-language-rule-matrix.md` §3 Coverage Summary + AC-SA-LEGACY-006.

### AC-SA-18 — Every SonarQube rule has "native" (✅) mapping in ≥ 4 languages; 0-✅ rules are removed

- **Given** the coverage matrix from AC-SA-17,
- **When** each SonarQube rule row is tallied,
- **Then** EVERY rule MUST have `✅` (native enforcement) in at MINIMUM 4 of the 8 languages. A rule with only 3 or fewer `✅` mappings is a coverage gap and MUST be documented in `99-consistency-report.md` with a remediation plan (e.g., "Add PHPCS custom sniff for S3776"). Rules with 0 `✅` across all 8 languages MUST be removed from the matrix (they are unenforceable fantasies). This AC ensures the matrix represents reality, not aspiration.
- **Verifies:** `10-cross-language-rule-matrix.md` + `99-consistency-report.md` coverage gap table.

### AC-SA-19 — Linter tool versions are pinned to exact SemVer; `latest` tags and floating ranges FORBIDDEN

- **Given** any linter config file referenced by a language spec,
- **When** its version is examined,
- **Then** EVERY linter tool version MUST be pinned to an exact SemVer (e.g., `eslint@8.57.0`, `golangci-lint@v1.57.2`, `phpstan@1.10.59`, `stylecop.analyzers@1.2.0-beta.507`). `latest` tags, floating minor ranges (`^1.0.0`), `~` ranges, or unpinned installs are FORBIDDEN — they cause non-reproducible CI failures when a linter releases a new rule. Each spec MUST include a `## Tool Versions` subsection listing the pinned version AND a `## Reproducing` subsection with the EXACT install command (e.g., `npm install eslint@8.57.0 --save-dev`). The version pin MUST be updated within 30 days of a new stable release (tracked in `99-consistency-report.md` Validation History).
- **Verifies:** All 8 language spec files + `99-consistency-report.md`.

### AC-SA-20 — Self-application doctest: `run-all.sh` against this spec folder produces zero `level: error` findings

- **Given** the repository root,
- **When** `./linters-cicd/run-all.sh --path spec/02-coding-guidelines/01-cross-language/16-static-analysis/` runs in CI,
- **Then** the resulting SARIF file MUST contain ZERO results with `"level": "error"`. `level: warning` and `level: note` are ALLOWED but tracked. A non-zero error count MUST fail CI. This is the dogfooding gate — the static-analysis spec authors must satisfy their own cross-language rules. The check MUST include: (a) all 8 language spec files are parseable Markdown, (b) the rule matrix table has exactly 9 columns and 7 rows, (c) every SonarQube ID in the matrix appears in at least 4 `✅` cells, (d) every linter version is pinned to exact SemVer, (e) every file name matches `^[0-9]{2}-[a-z0-9-]+\.md$`. Any violation emits `AC-SA-20-<detail>` as the ruleId in SARIF.
- **Verifies:** `00-overview.md` + AC-CL-20 self-application + AC-CI-09 dogfooding pattern.

---

## Legacy Criteria (preserved for traceability)

### AC-SA-LEGACY-001 — Every supported language (8) has a dedicated linter spec

> Original stub: "- [ ] Every supported language (8) has a dedicated linter spec"
> Replaced by: AC-SA-02 (exact file inventory + content requirements).


> **Verifies:** Legacy stub preserved for traceability; the live contract is asserted by **AC-SA-02** above. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-SA-LEGACY-002 — All specs enforce identical thresholds: 15-line functions, 3 params, complexity ≤ 10

> Original stub: "- [ ] All specs enforce identical thresholds: 15-line functions, 3 params, complexity ≤ 10"
> Replaced by: AC-SA-03 (four thresholds + linter config enforcement + no deviation).


> **Verifies:** Legacy stub preserved for traceability; the live contract is asserted by **AC-SA-03** above. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-SA-LEGACY-003 — SonarQube rule IDs mapped for every enforceable rule per language

> Original stub: "- [ ] SonarQube rule IDs mapped for every enforceable rule per language"
> Replaced by: AC-SA-04 (bidirectional mapping + 7-rule minimum + no orphan rules).


> **Verifies:** Legacy stub preserved for traceability; the live contract is asserted by **AC-SA-04** above. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-SA-LEGACY-004 — Integration checklist uses standardized table format with 🔲 status

> Original stub: "- [ ] Integration checklist uses standardized table format with 🔲 status"
> Replaced by: AC-SA-05 (exact table format + 🔲/✅ emoji + ≥ 10 rows).


> **Verifies:** Legacy stub preserved for traceability; the live contract is asserted by **AC-SA-05** above. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-SA-LEGACY-005 — CI pipeline spec defines a unified quality gate referencing all 8 languages

> Original stub: "- [ ] CI pipeline spec defines a unified quality gate referencing all 8 languages"
> Replaced by: AC-SA-06 (parallel execution + single SARIF + fail-on-error + both platform YAMLs).


> **Verifies:** Legacy stub preserved for traceability; the live contract is asserted by **AC-SA-06** above. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-SA-LEGACY-006 — Cross-language rule matrix covers all 7 SonarQube rules across all 8 languages

> Original stub: "- [ ] Cross-language rule matrix covers all 7 SonarQube rules across all 8 languages"
> Replaced by: AC-SA-07 (machine-parseable 8×8 table + coverage badges + no HTML/Mermaid).


> **Verifies:** Legacy stub preserved for traceability; the live contract is asserted by **AC-SA-07** above. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-SA-LEGACY-007 — TypeScript ESLint spec cross-referenced from overview

> Original stub: "- [ ] TypeScript ESLint spec cross-referenced from overview (lives in `02-typescript/`)"
> Replaced by: AC-SA-08 (exact cross-ref path + hyperlink + no duplicate + target file existence).

> **Verifies:** Legacy stub preserved for traceability; the live contract is asserted by **AC-SA-08** above. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
