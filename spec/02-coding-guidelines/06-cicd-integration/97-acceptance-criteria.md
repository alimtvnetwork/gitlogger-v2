# Acceptance Criteria — CI/CD Integration

**Version:** 4.0.0
**Last Updated:** 2026-04-26 (Phase 16o: full GWT rewrite — replaced 7 prose criteria with 20 module-specific Given/When/Then ACs covering CI/CD-pack-specific rules + explicit inheritance from `../01-cross-language/97` (AC-CL-*). Old prose preserved as AC-CI-LEGACY-* at end.)
**Scope:** `spec/02-coding-guidelines/06-cicd-integration/` — Portable, language-agnostic linter pack (`linters-cicd/`) shipped to consumer CI/CD pipelines.

---

## Module Summary

§02/06-cicd-integration codifies the contract for `linters-cicd/`: a portable check-script directory + plugin model + SARIF 2.1.0 emitter + multi-platform CI templates (GitHub Actions, GitLab, Azure DevOps, Jenkins, Bitbucket) + ZIP/composite-Action/install.sh distribution + rules-mapping table linking each rule back to its canonical spec source + middle-out probe ordering + parallel-job + timeout budget. Every check exits `0` on clean / `1` on findings / `2` on tool error (POSIX-conventional). The pack runs on stock Ubuntu with only `python3 ≥ 3.10` + `bash` (zero `pip install` Phase 1). The pack dogfoods itself: running `./linters-cicd/run-all.sh --path .` against THIS repo MUST produce a SARIF file with zero CODE-RED findings. Adding a new language plugin MUST require zero edits to `run-all.sh`, `action.yml`, or any other language's check script. Inherits ALL **AC-CL-01..AC-CL-20** per AC-CL-01.

> **🚨 B2 collision warning:** This module shares slot `06-` with sibling `06-ai-optimization/` in violation of AC-CG-01 / AC-SAG-04. Both folders carry full §97 GWT contracts (AC-AI-* and AC-CI-*). Resolution requires user decision (rename one folder); both §97s become canonical for whichever folder retains the `06-` slot vs. moves.

---

## Inlined Contracts

```text
PARENT_INHERITANCE:        ../01-cross-language/97 (AC-CL-01..AC-CL-20)
PACK_ROOT:                 linters-cicd/
PACK_LAYOUT:
                           linters-cicd/
                             ├── run-all.sh                  (orchestrator)
                             ├── action.yml                  (composite Action)
                             ├── install.sh                  (one-liner)
                             ├── checks/                     (per-rule scripts)
                             │   ├── _shared/                (helpers)
                             │   ├── _tests/                 (fixture-driven)
                             │   └── <lang>-<rule-id>.{sh,py}
                             ├── plugins/                    (per-language)
                             │   └── <lang>/manifest.toml
                             ├── scripts/                    (utilities)
                             │   └── validate-sarif.py
                             ├── templates/                  (CI configs)
                             │   ├── github-actions.yml
                             │   ├── gitlab-ci.yml
                             │   ├── azure-pipelines.yml
                             │   ├── Jenkinsfile
                             │   └── bitbucket-pipelines.yml
                             └── VERSION                     (semver, single source)

CHECK_FILENAME_REGEX:      ^[a-z0-9]+-[a-z0-9-]+\.(sh|py)$
                           (language prefix - rule id - extension)
                           Examples: ts-no-enum.py, go-iota-wire.sh

EXIT_CODES:                0 = clean (no findings)
                           1 = findings present (rule violations)
                           2 = tool error (parse failure, IO error, etc.)
                           Any other exit code is FORBIDDEN.

SARIF_VERSION:             2.1.0 (exact, not 2.1.x)
SARIF_SCHEMA_URL:          https://json.schemastore.org/sarif-2.1.0
SARIF_DRIVER_NAME:         coding-guidelines-linters
SARIF_RULE_ID_REGEX:       ^[A-Z]{2,4}-[A-Z]{1,3}-\d{1,3}$
                           Examples: AC-TS-07, AC-CL-09, AC-AI-12

PLATFORM_BASELINE:         Ubuntu 22.04 LTS (stock GitHub Actions runner)
                           python3 >= 3.10 (system, no venv)
                           bash >= 5.0 (system)
                           ZERO `pip install` for Phase 1
                           ZERO `apt-get install` for Phase 1
                           ZERO project-local-path assumptions

DISTRIBUTION_CHANNELS:     1. ZIP one-liner: curl | bash install.sh
                           2. GitHub composite Action: uses: org/repo@vX.Y.Z
                           3. Manual checkout + ./run-all.sh

VERSIONING:                Single source of truth: linters-cicd/VERSION
                           SemVer MAJOR.MINOR.PATCH
                           Every git tag v* MUST attach a release ZIP +
                           checksums.txt (SHA-256) entry.

PLUGIN_MANIFEST_KEYS:      [plugin]
                             id            = "<lang-id>"           (kebab-case)
                             display_name  = "<Human Name>"
                             version       = "<semver>"
                             checks_dir    = "checks/"
                             rule_prefix   = "AC-XX-"               (matches AC-CL-* family)

PERFORMANCE_BUDGET:        Single check: < 5 s on 10k-LOC repo
                           Full run-all.sh: < 60 s on 10k-LOC repo
                           Parallelism: GNU parallel (or xargs -P) with
                           default = nproc/2, override via --jobs N.
                           Probe order: middle-out (cheapest checks first)
                           Per-check timeout: 30 s default, override per
                           check via plugin manifest [check.<id>] timeout_s.

DOGFOODING:                ./linters-cicd/run-all.sh --path . MUST
                           produce SARIF with zero `level: error` findings
                           against THIS repository on every CI run.

INHERITED_FROM_AC_CL:      AC-CL-12 kebab-case files (CHECK_FILENAME_REGEX above),
                           AC-CL-09 PascalCase wire (SARIF rule IDs),
                           AC-CL-19 behavior names (action.yml input names),
                           AC-CL-20 DRY rule-of-three (_shared/ helpers)
```

---

## Acceptance Criteria

### AC-CI-01 — Inherits all AC-CL-01..AC-CL-20 from cross-language parent

- **Given** any artifact (script, manifest, template, doc) under `linters-cicd/` or this spec folder,
- **When** reviewed,
- **Then** it MUST satisfy every AC-CL-* rule from `../01-cross-language/97-acceptance-criteria.md` (file naming, no-negative-polarity booleans, normative MUST language, etc.). Conflicts MUST resolve in favor of the cross-language rule per AC-CL-01. Any waiver MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** AC-CL-01 inheritance contract.

### AC-CI-02 — Pack runs on stock Ubuntu with only `python3 ≥ 3.10` + `bash` (zero installs Phase 1)

- **Given** a fresh stock Ubuntu 22.04 LTS GitHub Actions runner,
- **When** `./linters-cicd/run-all.sh --path <any-repo>` is executed without any prior `pip install` or `apt-get install`,
- **Then** every Phase 1 check MUST run to completion (exit 0/1/2 — see AC-CI-04). Adding `pip install <anything>` or `apt-get install <anything>` to the runner setup as a precondition for Phase 1 checks is FORBIDDEN. Phase 2/3 checks MAY require additional tooling; if so, each plugin manifest MUST declare deps under `[plugin.requires]`.
- **Verifies:** `00-overview.md` Layer 1 + `05-distribution.md`.

### AC-CI-03 — Every emitted SARIF file validates against schema 2.1.0 exactly

- **Given** any SARIF file written by any check,
- **When** `python3 linters-cicd/scripts/validate-sarif.py <file>` is run,
- **Then** the script MUST exit `0`. The file MUST declare `"version": "2.1.0"` (exact string) AND `"$schema": "https://json.schemastore.org/sarif-2.1.0"` (exact URL). SARIF 2.1.x point-version variants, draft 2.2, or vendor extensions in the `version` field are FORBIDDEN — they break GitHub/GitLab/Azure inline rendering.
- **Verifies:** `01-sarif-contract.md` + AC-CI-LEGACY-002.

### AC-CI-04 — POSIX-conventional exit codes: 0 clean / 1 findings / 2 tool-error; ALL others FORBIDDEN

- **Given** any check script in `linters-cicd/checks/`,
- **When** invoked,
- **Then** the exit code MUST be exactly one of: `0` (clean — no findings), `1` (findings present — rule violations), `2` (tool error — parse failure, IO error, missing input). Any other exit code (3+, negative, or `127` for missing-binary) is FORBIDDEN. Verified by `linters-cicd/checks/_tests/test_exit_codes.sh` which MUST run as part of CI. Tool-error MUST distinguish from findings — silently downgrading a tool error to "clean" is a CODE-RED bug.
- **Verifies:** `00-overview.md` + AC-CI-LEGACY-007.

### AC-CI-05 — Check filename regex `^[a-z0-9]+-[a-z0-9-]+\.(sh|py)$` (language-id prefix)

- **Given** every file in `linters-cicd/checks/` (excluding `_shared/` and `_tests/`),
- **When** the basename is parsed,
- **Then** it MUST match `^[a-z0-9]+-[a-z0-9-]+\.(sh|py)$`. The first segment MUST be a registered language id from a plugin manifest (`ts`, `go`, `php`, `rust`, `cs`, `cl` for cross-language, `ai` for ai-optimization, `ci` for self-tests). The remaining segments MUST describe the rule. Examples: `ts-no-enum.py`, `go-iota-wire.sh`, `cl-kebab-files.py`. Counter-examples (FORBIDDEN): `NoEnum.py`, `check_typescript_enum.py`, `001-rule.sh`, `ts_no_enum.py`. Mirrors AC-CL-12 + AC-CG file-slot stability.
- **Verifies:** `00-overview.md` Layer 1 + AC-CL-12.

### AC-CI-06 — Adding a language plugin requires ZERO edits to `run-all.sh`, `action.yml`, or sibling check scripts

- **Given** a PR adding a new language plugin (e.g. `plugins/kotlin/manifest.toml` + `checks/kt-*.{sh,py}`),
- **When** the PR diff is reviewed,
- **Then** it MUST contain ZERO line changes inside `run-all.sh`, `action.yml`, OR any check script for another language. ALL discovery MUST happen via filesystem glob + manifest parsing at runtime. PR-template checklist MUST include "□ This PR touches only the new plugin's directory + global registries (rules-mapping table). It does NOT modify run-all.sh, action.yml, or sibling language checks." Missing or unchecked box BLOCKS merge.
- **Verifies:** `02-plugin-model.md` + AC-CI-LEGACY-006.

### AC-CI-07 — Plugin manifest is TOML with required keys [plugin].{id,display_name,version,checks_dir,rule_prefix}

- **Given** every `plugins/<lang>/manifest.toml`,
- **When** parsed,
- **Then** the `[plugin]` table MUST contain ALL FIVE required keys: `id` (kebab-case lowercase, MUST match the language-prefix in AC-CI-05), `display_name` (human-readable string), `version` (SemVer), `checks_dir` (relative path string), `rule_prefix` (matches `^AC-[A-Z]{2,3}-$` — e.g. `AC-TS-`, `AC-GO-`, `AC-CL-`). Missing any key MUST cause `run-all.sh` to refuse to load the plugin AND emit an `AC-CI-07-VIOLATION` rule-id finding to SARIF.
- **Verifies:** `02-plugin-model.md`.

### AC-CI-08 — SARIF rule IDs match `^[A-Z]{2,4}-[A-Z]{1,3}-\d{1,3}$` (e.g. `AC-TS-07`)

- **Given** every `result.ruleId` and `tool.driver.rules[].id` field in any emitted SARIF,
- **When** validated,
- **Then** the value MUST match `^[A-Z]{2,4}-[A-Z]{1,3}-\d{1,3}$`. The first segment is a fixed prefix (`AC` for acceptance criteria, `AH` for anti-hallucination, `CHK` for checklist). The middle segment MUST be the language code (`TS`, `GO`, `PHP`, `RS`, `CS`, `CL`, `AI`, `CI`, `SAG`, `CG`). The numeric suffix MUST be 1-3 digits with no zero-padding. Free-form rule IDs (e.g. `no-enum`, `TypeScript.NoEnum`) are FORBIDDEN.
- **Verifies:** `01-sarif-contract.md` + `06-rules-mapping.md`.

### AC-CI-09 — Dogfooding gate: `./run-all.sh --path .` against THIS repo emits ZERO `level: error` findings

- **Given** the repository root,
- **When** `./linters-cicd/run-all.sh --path .` runs in CI,
- **Then** the resulting SARIF file MUST contain ZERO results with `"level": "error"`. `level: warning` and `level: note` are ALLOWED but tracked. A non-zero error count MUST fail CI. This is the "we eat our own dog food" gate — if the spec authors can't satisfy their own rules, the rules are unenforceable.
- **Verifies:** `00-overview.md` + AC-CI-LEGACY-003.

### AC-CI-10 — Composite GitHub Action exposed via single-line `uses:` with zero required inputs

- **Given** a downstream consumer's `.github/workflows/lint.yml`,
- **When** they add `- uses: <org>/coding-guidelines-linters@vX.Y.Z`,
- **Then** the Action MUST run with default inputs producing a SARIF artifact uploaded via `actions/upload-artifact` AND a workflow summary annotation. Required inputs in `action.yml` MUST be ZERO. Optional inputs ALLOWED: `path` (default `.`), `jobs` (default `nproc/2`), `severity-threshold` (default `error`), `fail-on-findings` (default `true`). Adding any required input is FORBIDDEN — it breaks the one-line UX.
- **Verifies:** `05-distribution.md` + AC-CI-LEGACY-004.

### AC-CI-11 — Every git tag `v*` attaches release ZIP + checksums.txt with SHA-256 entry

- **Given** any git tag matching `v[0-9]+\.[0-9]+\.[0-9]+`,
- **When** the GitHub Release is published,
- **Then** the release MUST include TWO assets: `coding-guidelines-linters-vX.Y.Z.zip` AND `checksums.txt`. `checksums.txt` MUST contain a SHA-256 line for the ZIP in `sha256sum`-compatible format (`<hex>  coding-guidelines-linters-vX.Y.Z.zip`). The ZIP MUST extract to a top-level `linters-cicd/` directory. SHA-256 mismatch or missing checksums.txt MUST fail the release CI gate.
- **Verifies:** `05-distribution.md` + AC-CI-LEGACY-005.

### AC-CI-12 — `linters-cicd/VERSION` is the SINGLE source of truth; duplicates FORBIDDEN

- **Given** the version string,
- **When** searched,
- **Then** it MUST appear in EXACTLY ONE place: `linters-cicd/VERSION`. `action.yml`, `install.sh`, `run-all.sh`, every `manifest.toml`, the SARIF `tool.driver.version` field, AND release-artifact filenames MUST READ from `VERSION` at build/run time. Hardcoding the version string in any OTHER file is FORBIDDEN and FAILS this AC. Mirrors AC-CL-20 DRY rule-of-three applied to versioning.
- **Verifies:** `05-distribution.md` + AC-CL-20.

### AC-CI-13 — CI templates ship for ALL FIVE platforms (GitHub, GitLab, Azure, Jenkins, Bitbucket); each runs the same SARIF gate

- **Given** `linters-cicd/templates/`,
- **When** listed,
- **Then** it MUST contain EXACTLY these five template files: `github-actions.yml`, `gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml`. Each template MUST: (a) install zero deps beyond Phase 1 baseline, (b) run `./linters-cicd/run-all.sh --path .`, (c) upload the SARIF artifact for that platform's native renderer, (d) fail the pipeline on `level: error` findings. Adding a sixth platform requires adding the template AND updating this AC's enumeration; removing a template is a BREAKING CHANGE requiring a major-version bump.
- **Verifies:** `04-ci-templates.md`.

### AC-CI-14 — `06-rules-mapping.md` table maps EVERY enforced rule to {spec-source, check-script, severity}

- **Given** `06-rules-mapping.md`,
- **When** parsed,
- **Then** it MUST contain a Markdown table with header columns EXACTLY: `Rule ID | Spec Source | Check Script | Severity`. Every rule the pack enforces MUST have one row. `Spec Source` MUST be a relative link to the canonical AC file (e.g. `../02-typescript/97-acceptance-criteria.md#ac-ts-07`). `Check Script` MUST be a relative path to the script in `linters-cicd/checks/`. `Severity` MUST be one of `error`, `warning`, `note` (matching SARIF level enum). Rows missing any cell FAIL this AC. Orphan check scripts (in `checks/` but not in the table) FAIL this AC.
- **Verifies:** `06-rules-mapping.md` + cross-spec traceability.

### AC-CI-15 — Severity vocabulary is CLOSED enum {error, warning, note}; freeform values FORBIDDEN

- **Given** any severity value (in the rules-mapping table, plugin manifests, SARIF results, or doc prose),
- **When** parsed,
- **Then** it MUST be one of: `error`, `warning`, `note` (lowercase, exact). Aliases (`critical`, `info`, `low`, `high`), capitalised variants (`Error`), or freeform values (`pretty bad`) are FORBIDDEN. The values map directly to SARIF 2.1.0's `level` enum + GitHub Code Scanning's three-tier UX. Mirrors AC-PHP-03 closed-enum + AC-AI-14 severity-enum patterns.
- **Verifies:** `06-rules-mapping.md` + `01-sarif-contract.md` + AC-AI-14.

### AC-CI-16 — Performance budget: single check < 5 s, full `run-all.sh` < 60 s on 10k-LOC repo

- **Given** any single check OR a full `run-all.sh` invocation against a 10k-LOC reference fixture (`linters-cicd/checks/_tests/fixtures/repo-10k/`),
- **When** measured (wall-clock),
- **Then** any single check MUST complete in < 5 s AND the full `run-all.sh` (with default parallelism = `nproc/2`) MUST complete in < 60 s. Exceeding either budget MUST emit an `AC-CI-16-PERF` warning to SARIF AND surface in the workflow summary. Per-check timeout default is 30 s (override via plugin manifest `[check.<id>] timeout_s`); a check exceeding its timeout MUST exit `2` (tool error) — silent stalls FORBIDDEN.
- **Verifies:** `07-performance.md`.

### AC-CI-17 — Middle-out probe order: cheapest checks first, expensive (tree-sitter, AST) last

- **Given** the ordering `run-all.sh` uses to schedule checks,
- **When** examined,
- **Then** it MUST follow middle-out: (1) regex/grep checks first (cheapest), (2) line-counter / structural checks next, (3) Python AST checks, (4) tree-sitter / language-server checks LAST. Within each tier, order is parallelism-driven (longest jobs first). Random ordering OR alphabetic ordering is FORBIDDEN — they defeat early-exit when `--fail-fast` is set. The ordering MUST be derivable from each plugin manifest's `[check.<id>] cost = "low" | "medium" | "high"` declaration.
- **Verifies:** `07-performance.md`.

### AC-CI-18 — `install.sh` one-liner is idempotent + checksum-verified + non-interactive

- **Given** the documented one-liner `curl -fsSL <url>/install.sh | bash`,
- **When** executed,
- **Then** the script MUST: (a) be idempotent (re-running yields the same final state — no version drift, no duplicate dirs), (b) verify the downloaded ZIP's SHA-256 against the inline expected hash before extracting, (c) run NON-interactively (no prompts, no TTY assumptions), (d) install into `${LINTERS_HOME:-$HOME/.linters-cicd}`, (e) print the installed version + path on success, (f) exit non-zero on ANY verification failure (network error, hash mismatch, extraction failure). Interactive prompts or unverified extraction are FORBIDDEN — they break CI usage.
- **Verifies:** `05-distribution.md`.

### AC-CI-19 — `_tests/` fixtures gate every check: known-bad MUST exit 1, known-good MUST exit 0

- **Given** every check script in `linters-cicd/checks/`,
- **When** `linters-cicd/checks/_tests/run-tests.sh` executes,
- **Then** for EACH check there MUST be: (a) a known-bad fixture (`_tests/fixtures/<check-id>/bad/`) that the check MUST flag (exit 1, ≥ 1 SARIF result), AND (b) a known-good fixture (`_tests/fixtures/<check-id>/good/`) that the check MUST pass (exit 0, zero SARIF results). Missing either fixture FAILS this AC AND blocks merge of the check. The test runner MUST exit non-zero if any check is missing fixtures OR fixtures behave unexpectedly. Mirrors AC-CL-13 deterministic-test-fixture rule.
- **Verifies:** `02-plugin-model.md` + AC-CL-13.

### AC-CI-20 — Self-application: this folder + `linters-cicd/` satisfy AC-CI-01..AC-CI-19

- **Given** the union of this spec folder AND the `linters-cicd/` runtime tree,
- **When** mechanically validated by `linters-cicd/run-all.sh --path linters-cicd/ --self-test`,
- **Then** AC-CI-01..AC-CI-19 above MUST all PASS. The pack MUST lint itself: every check filename satisfies AC-CI-05; every plugin manifest satisfies AC-CI-07; the rules-mapping table satisfies AC-CI-14; etc. The dogfooding extends from "lint the spec repo" (AC-CI-09) to "lint the linter pack itself" (this AC). Mirrors AC-AI-20 + AC-SAG-18 self-application doctest pattern. CODE-RED if violated.
- **Verifies:** Recursive self-check + AC-AI-20 + AC-SAG-18.

---

## Legacy Index (preserved for traceability)

The 7 prose criteria from v1.0.0 are preserved verbatim. They are NO LONGER authoritative — the GWT ACs above supersede them.

### AC-CI-LEGACY-001 — Portability

Each check script in `linters-cicd/checks/` runs on a stock Ubuntu runner with only `python3` (≥ 3.10) and `bash` available. **No** `pip install` required for Phase 1. → superseded by AC-CI-02.

### AC-CI-LEGACY-002 — SARIF compliance

`linters-cicd/scripts/validate-sarif.py` validates every emitted file against the official SARIF 2.1.0 schema. CI run is green. → superseded by AC-CI-03.

### AC-CI-LEGACY-003 — Self-test on this repo

Running `./linters-cicd/run-all.sh --path .` against this repository produces a SARIF file with **zero** CODE RED findings. → superseded by AC-CI-09.

### AC-CI-LEGACY-004 — Composite Action one-liner

A consumer can add coding-guidelines linting to their GitHub workflow with exactly one `uses:` line and no other config. → superseded by AC-CI-10.

### AC-CI-LEGACY-005 — Versioned release artifact

Every `v*` tag attaches `coding-guidelines-linters-vX.Y.Z.zip` to the GitHub Release with a SHA-256 entry in `checksums.txt`. → superseded by AC-CI-11.

### AC-CI-LEGACY-006 — Plugin model unchanged when adding language

Adding a new language plugin requires zero edits to `run-all.sh`, `action.yml`, or any check script for another language. → superseded by AC-CI-06.

### AC-CI-LEGACY-007 — Exit codes

Every check exits `0` on clean, `1` on findings, `2` on tool error. → superseded by AC-CI-04.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Cross-language parent (AC-CL-*)](../01-cross-language/97-acceptance-criteria.md)
- [SARIF contract](./01-sarif-contract.md)
- [Plugin model](./02-plugin-model.md)
- [Language roadmap](./03-language-roadmap.md)
- [CI templates](./04-ci-templates.md)
- [Distribution](./05-distribution.md)
- [Rules mapping](./06-rules-mapping.md)
- [Performance](./07-performance.md)
- [§02 parent governance](../97-acceptance-criteria.md)
- [B2 collision twin: AI-Optimization sibling](../06-ai-optimization/97-acceptance-criteria.md)
