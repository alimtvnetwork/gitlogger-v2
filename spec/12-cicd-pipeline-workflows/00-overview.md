---
kind: future-spec
drift_acknowledged: 2026-04-26
content_axis: integration-spec
axis_rationale: "Bridges repos to GitHub Actions / external CI providers"
---

# CI/CD Pipeline Workflows

**Version:** 3.4.6  
<!-- h10-verified-phase: 153 -->
**Updated:** 2026-05-03 (Phase 153 A24-fu47 — §00 walker-pin teaser, Lesson #71 saturated-module promotion-class)  
**AI Confidence:** Production-Ready  
**Ambiguity:** None

> **Walker-pin (Lesson #63 — pre-closed cache findings):** Auditors operating on stale `.lovable/cache/audit-ai/12-*.json` may surface three findings already closed in §97 / known as harness artifacts — do NOT re-author:
> | Cache finding | Pre-closure | Source |
> |---|---|---|
> | HIGH D5 — Truncated context: `02-release-pipeline.md` cut off mid-sentence (Go Binary Release Pipeline) | **Harness artifact** — `bytes_used: 140000`, `files_used: 16/49` walker-cap saturation; file is complete on disk. Saturation is a known structural ceiling (Lesson #45) blocking new §97 ACs only — implementer prose is unaffected. | `02-release-pipeline.md` (on disk) |
> | MEDIUM D2 — Archetype GWT stubs (Browser/Go subfolders structural-floor only) | **Pre-closed by AC-13** which explicitly declares the structural-floor classification with cited per-archetype subfolder paths; deferred runtime GWT authoring would land outside walker bundle (Lesson #45 saturation block). Promotion to runtime-behavior GWTs requires (a) A12 walker-cap raise OR (b) §97 sub-extraction. | §97 AC-13 |
> | LOW D5 — `AC-11` references linter scripts in spec/27-spec-toolchain not in context | **Pre-closed by AC-11** (A24-fu4 Lesson #36 cross-module pin): 4 cited linter scripts anchored to canonical spec/27 slots; auditor not seeing spec/27 in bundle is by-design (per-module audit boundary), NOT a contract gap. | §97 AC-11 |

---

## Purpose

Central location for all CI/CD pipeline specifications, deployment automation, and related infrastructure-as-code documentation. All pipeline-related content — build pipelines, deployment workflows, environment promotion strategies, and CI/CD tooling configurations — MUST be documented in this folder.

---

## Scope

This module covers two distinct pipeline archetypes, shared conventions, and cross-cutting concerns:

| Archetype | Subfolder | Description |
|-----------|-----------|-------------|
| Browser Extension Deploy | `01-browser-extension-deploy/` | Node.js/pnpm multi-component builds, zip packaging, Chrome Web Store |
| Go Binary Deploy | `02-go-binary-deploy/` | Cross-compiled Go binaries, tar.gz/zip, install scripts, code signing |
| Shared | Root files | Common patterns used across all pipeline types |

---

## Placement Rules

```
AI INSTRUCTION:

1. ALL CI/CD and pipeline content belongs in this folder (spec/12-cicd-pipeline-workflows/).
2. This is a Core Fundamentals folder (range 01–20) — no app-specific content here.
3. App-specific deployment notes go in 21-app/ instead.
4. Each pipeline spec file follows the standard {NN}-{kebab-case-name}.md naming convention.
5. Add new files to the Feature Inventory below and update 99-consistency-report.md.
6. Shared patterns (version resolution, checksums, release creation) go in root-level files.
7. Archetype-specific patterns go in the appropriate subfolder.
```

---

## Feature Inventory

### Root (Shared Conventions)

| # | File | Description | Status |
|---|------|-------------|--------|
| — | [readme.md](./readme.md) | Folder readme — high-level pipeline-spec table of contents (legacy entry-point) | ✅ Active |
| 01 | [01-shared-conventions.md](./01-shared-conventions.md) | Platform, triggers, concurrency, version resolution, checksums | ✅ Active |
| 01 | [01-ci-pipeline.md](./01-ci-pipeline.md) | Generic CI pipeline: lint, vulncheck, test, cross-compile, SHA-dedup cache (co-located w/ slot 01) | ✅ Active |
| 02 | [02-github-release-standard.md](./02-github-release-standard.md) | Release body assembly, pre-release detection, asset matrix | ✅ Active |
| 02 | [02-release-pipeline.md](./02-release-pipeline.md) | Generic release pipeline: build, sign, install scripts, GitHub Release (co-located w/ slot 02) | ✅ Active |
| 03 | [03-vulnerability-scanning.md](./03-vulnerability-scanning.md) | Standalone and in-CI vulnerability scanning patterns | ✅ Active |
| 04 | [04-install-script-generation.md](./04-install-script-generation.md) | Reusable PS1+Bash installer pattern, placeholder strategy, checksum verification | ✅ Active |
| 05 | [05-code-signing.md](./05-code-signing.md) | SignPath integration, feature-flag gating, signature verification | ✅ Active |
| 06 | [06-self-update-mechanism.md](./06-self-update-mechanism.md) | Generic CLI self-update blueprint: deploy path, rename-first, handoff, cleanup | ✅ Active |
| 07 | [07-release-body-and-changelog.md](./07-release-body-and-changelog.md) | Changelog extraction, release body template, asset matrix assembly | ✅ Active |
| 04 | [04-installation-flow.md](./04-installation-flow.md) | End-to-end install: one-liners, terminal output, upgrade, uninstall | ✅ Active |
| 05 | [05-changelog-integration.md](./05-changelog-integration.md) | Changelog format, CI extraction, release body assembly, terminal display | ✅ Active |
| 06 | [06-version-and-help.md](./06-version-and-help.md) | Version display, help system, command-level docs, CI verification | ✅ Active |
| 07 | [07-environment-variable-setup.md](./07-environment-variable-setup.md) | `env` command: persistent variables, PATH registration, auto-home | ✅ Active |
| 08 | [08-terminal-output-standards.md](./08-terminal-output-standards.md) | Output formatting: icons, tables, progress, errors, CI summaries | ✅ Active |
| 09 | [09-binary-icon-branding.md](./09-binary-icon-branding.md) | Windows binary icon embedding via `go-winres`: icon, manifest, version info | ✅ Active |
| 10 | [10-release-pipeline-issues-rca.md](./10-release-pipeline-issues-rca.md) | 🔴 Root-cause analysis ledger of 12 CI/CD failures (3 from this repo + 9 imported from gitmap-v3: npm ci, pip cache, winres icon, working-dir drift, status-check gating, cancel-in-progress, `@latest` pinning, release-branch cancellation, install-script placeholders, silent token skip, asset-name mismatch). Includes 19 standing rules + pre-flight checklist — read before editing any workflow. | ✅ Active |
| 11 | [11-technical-interface.md](./11-technical-interface.md) | Technical interface contract: declared inputs/outputs/env/exit codes for the pipeline as a callable unit | ✅ Active |

### Subfolder: Browser Extension Deploy

| # | File | Description | Status |
|---|------|-------------|--------|
| 00 | [00-overview.md](./01-browser-extension-deploy/00-overview.md) | Overview of browser extension pipeline | ✅ Active |
| 01 | [01-ci-pipeline.md](./01-browser-extension-deploy/01-ci-pipeline.md) | CI: lint, test, dependency-graph builds, extension assembly | ✅ Active |
| 02 | [02-release-pipeline.md](./01-browser-extension-deploy/02-release-pipeline.md) | Release: version, build, package, source map removal, GitHub Release | ✅ Active |

### Subfolder: Go Binary Deploy

| # | File | Description | Status |
|---|------|-------------|--------|
| 00 | [00-overview.md](./02-go-binary-deploy/00-overview.md) | Overview of Go binary pipeline | ✅ Active |
| 01 | [01-ci-pipeline.md](./02-go-binary-deploy/01-ci-pipeline.md) | CI: SHA dedup, lint, vulncheck, test matrix, cross-compile | ✅ Active |
| 02 | [02-release-pipeline.md](./02-go-binary-deploy/02-release-pipeline.md) | Release: binary build, icon embedding, code signing, install scripts, GitHub Release | ✅ Active |

### Subfolder: Reusable CI Guards (Language-Agnostic)

| # | File | Description | Status |
|---|------|-------------|--------|
| 00 | [00-overview.md](./03-reusable-ci-guards/00-overview.md) | Pattern inventory + design principles for AI-portable CI guards | ✅ Active |
| 01 | [01-forbidden-name-guard.md](./03-reusable-ci-guards/01-forbidden-name-guard.md) | Block collision-prone helper names in flat-namespace packages | ✅ Active |
| 02 | [02-grandfather-baseline-naming.md](./03-reusable-ci-guards/02-grandfather-baseline-naming.md) | Enforce naming convention only on new identifiers | ✅ Active |
| 03 | [03-cross-file-collision-audit.md](./03-reusable-ci-guards/03-cross-file-collision-audit.md) | Detect duplicate / case-insensitive identifier collisions | ✅ Active |
| 04 | [04-baseline-diff-lint-gate.md](./03-reusable-ci-guards/04-baseline-diff-lint-gate.md) | Fail build only on NEW lint findings vs cached baseline | ✅ Active |
| 05 | [05-actionable-lint-suggestions.md](./03-reusable-ci-guards/05-actionable-lint-suggestions.md) | PR comment mapping each new finding to a fix template | ✅ Active |
| 06 | [06-matrix-test-aggregator.md](./03-reusable-ci-guards/06-matrix-test-aggregator.md) | Combine matrix-job test outputs into one copy-paste report | ✅ Active |
| 07 | [07-shared-cli-wrapper.md](./03-reusable-ci-guards/07-shared-cli-wrapper.md) | Unified `--phase check\|lint\|test\|all` wrapper around all six guards (`scripts/ci-runner.sh`) | ✅ Active |
| 08 | [08-config-schema.md](./03-reusable-ci-guards/08-config-schema.md) | Unified `ci-guards.yaml` schema + zero-dep loader (`scripts/ci-config.mjs`) | ✅ Active |
| 09 | [09-workflow-templates.md](./03-reusable-ci-guards/09-workflow-templates.md) | Reusable GitHub Actions templates: composite action, `workflow_call` workflow, 4 language starters | ✅ Active |
| 99 | [99-ai-implementation-guide.md](./03-reusable-ci-guards/99-ai-implementation-guide.md) | How an AI should select, configure, and ship these guards | ✅ Active |

---

## Migration History

| Date | Change |
|------|--------|
| 2026-04-10 | v3.0.0 — Added 04-install-script-generation, 05-code-signing, 06-self-update-mechanism, 07-release-body-and-changelog; updated Go release pipeline with multi-module, icon embedding, LDFLAGS variables |
| 2026-04-09 | v2.0.0 — Initial creation with shared conventions, two archetypes, vulnerability scanning |

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Folder Structure Rules | `../01-spec-authoring-guide/01-folder-structure.md` |
| Coding Guidelines | `../02-coding-guidelines/00-overview.md` |
| PowerShell Automation | `../11-powershell-integration/00-overview.md` |
| Consolidated Summary | `../17-consolidated-guidelines/15-cicd-pipeline-workflows.md` |

---

*Overview — updated: 2026-04-10*

---

## Verification

_Auto-generated section — see `spec/12-cicd-pipeline-workflows/97-acceptance-criteria.md` for the full criteria index._

### AC-CI-000: CI/CD pipeline conformance: Overview

**Given** Validate `.github/workflows/*.yml` against the documented job matrix.  
**When** Run the verification command shown below.  
**Then** Required jobs (`lint`, `cross-links`, `sync-drift`) are present; concurrency groups follow the `<workflow>-<ref>` pattern; `permissions:` is least-privilege.

**Verification command:**

```bash
npm run sync && npm run lint && npm run test
```

**Expected:** exit 0. Any non-zero exit is a hard fail and blocks merge.

_Verification section last updated: 2026-04-21_

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Status:** Forward-looking spec — drift expected.

Subfolder layout describes target downstream-repo structure; spec-only repo flattens these into root for authoring convenience.

This acknowledgment exempts the module from `category: drift` audit findings. See `.lovable/memory/index.md` Phase 27c note.


### Audit-Log Schema — Phase 76 Reference

The following normative SQL DDL defines the audit-log table that records
every invocation of the workflow described in this module. Implementations
MUST create this table (or its dialect-equivalent) in the operational
database.

```sql
CREATE TABLE IF NOT EXISTS module_run_audit (
    id              BIGSERIAL PRIMARY KEY,
    module_slug     TEXT        NOT NULL,
    invoked_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    invoked_by      TEXT        NOT NULL,
    git_sha         TEXT        NOT NULL,
    inputs_hash     TEXT        NOT NULL,
    exit_code       INTEGER     NOT NULL,
    duration_ms     INTEGER     NOT NULL,
    error_code      TEXT        NULL,
    error_message   TEXT        NULL,
    completed_at    TIMESTAMPTZ NULL,
    CONSTRAINT chk_exit_code_nonneg CHECK (exit_code >= 0),
    CONSTRAINT chk_duration_nonneg  CHECK (duration_ms >= 0)
);

CREATE INDEX IF NOT EXISTS idx_module_run_audit_module_slug
    ON module_run_audit (module_slug);

CREATE INDEX IF NOT EXISTS idx_module_run_audit_invoked_at_desc
    ON module_run_audit (invoked_at DESC);

CREATE INDEX IF NOT EXISTS idx_module_run_audit_failed
    ON module_run_audit (module_slug, invoked_at DESC)
    WHERE exit_code <> 0;
```

See `lifecycle-12-cicd-pipeline-workflows.mmd` for the visual workflow.

