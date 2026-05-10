---
kind: future-spec
drift_acknowledged: 2026-04-26
---

# CI/CD Integration — Coding-Guidelines Linter Pack

> **Version:** 4.0.0
<!-- h10-verified-phase: 21 -->
> **Status:** Active (Phase 1 shipping)
> **Updated:** 2026-04-19
> **AI Confidence:** Production-Ready
> **Ambiguity:** None

---

## Keywords

`ci`, `cd`, `linter`, `sarif`, `github-actions`, `gitlab`, `azure-devops`,
`jenkins`, `bitbucket`, `coding-guidelines`, `code-red`

---

## Purpose

Ship a portable, language-agnostic linter pack — `linters-cicd/` — that any
CI/CD pipeline can integrate with one line to enforce the **CODE RED**
coding-guidelines rules in this repository.

The pack must:

1. Run on any CI without requiring this repo as a dependency.
2. Emit **SARIF 2.1.0** by default so GitHub, GitLab, and Azure DevOps
   render findings inline on pull requests.
3. Support a **plugin model** so adding a new language is one file plus a
   test fixture — never a refactor.
4. Be installable three ways: ZIP one-liner, GitHub composite Action, or
   manual checkout.

---

## Document Inventory

| File | Purpose |
|------|---------|
| `00-overview.md` | This file — high-level architecture |
| `01-sarif-contract.md` | SARIF 2.1.0 output schema each check must emit |
| `02-plugin-model.md` | How a new-language check is added |
| `03-language-roadmap.md` | Phase 1/2/3 rollout, current status per language |
| `04-ci-templates.md` | Inventory of CI platform templates |
| `05-distribution.md` | ZIP, composite Action, install.sh contract |
| `06-rules-mapping.md` | Each rule → spec source → check script → severity |
| `07-performance.md` | Middle-out probe order, parallel jobs, timeout budgets |
| `97-acceptance-criteria.md` | Testable AC for every public artifact |
| `98-faq.md` | Suppression, baselining, single-rule runs, version pinning |
| `99-troubleshooting.md` | python3 missing, tree-sitter wheel issues, SARIF >10 MB, false-positive triage, TOML parse errors |

---

## Architecture (3 layers)

### Layer 1 — Portable check scripts (`linters-cicd/checks/`)

Pure POSIX shell + Python 3 (no project-local paths, no external installs).
Each script:

- Accepts `--path <dir>`, `--format sarif|text`, `--severity error|warning`
- Exits `0` on no findings, `1` on findings, `2` on tool failure
- Writes SARIF to stdout or `--output <file>`

### Layer 2 — Pre-built linter configs (`linters-cicd/configs/`)

Drop-in configs that wrap the existing community linters where they
already cover a CODE RED rule (golangci-lint, ESLint, PHPCS).

### Layer 3 — CI templates (`linters-cicd/ci/`)

One ready-to-paste workflow per platform plus the GitHub composite Action
under `linters-cicd/action.yml`.

---

## Out of scope (v1)

- Auto-fix / codemod (read-only checks only)
- IDE plugins (already covered by `.cursorrules` + linter configs)
- Custom rule authoring DSL — rules are coded in Python, period

---

## Cross-References

- [Code Red Guidelines](../../17-consolidated-guidelines/00-overview.md)
- [CI/CD Pipeline Workflows](../../12-cicd-pipeline-workflows/00-overview.md)
- [Linter Scripts](../../../linter-scripts/) — existing in-repo guards

---

## Contributors

- **Md. Alim Ul Karim** — Creator & Lead Architect
- **Riseup Asia LLC** — Sponsor

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Status:** Forward-looking spec — drift expected.

Spec mandates `linters-cicd/` directory; current repo uses `linter-scripts/`. Rename is a downstream packaging concern tracked by the distribution repo.

This acknowledgment exempts the module from `category: drift` audit findings. See `.lovable/memory/index.md` Phase 27b note.


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

See `lifecycle-02-coding-guidelines-06-cicd-integration.mmd` for the visual workflow.

