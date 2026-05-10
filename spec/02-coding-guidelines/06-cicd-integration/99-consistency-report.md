# Consistency Report — CI/CD Integration

**Version:** 4.0.0
**Updated:** 2026-04-26
**Status:** Active (Phase 1 shipping)

> **v4.0.0 update (Phase 16o):** §97 fully rewritten from 7 prose criteria (AC-CI-001..007) to **20 module-specific Given/When/Then ACs** (AC-CI-01..AC-CI-20). New ACs codify CI/CD-pack-specific rules layered on cross-language parent: explicit AC-CL-* inheritance, stock-Ubuntu+python3≥3.10+bash baseline (zero installs Phase 1), SARIF 2.1.0 exact-version gate, POSIX exit codes 0/1/2 only, `^[a-z0-9]+-[a-z0-9-]+\.(sh|py)$` check-filename regex with registered language-id prefix, zero-edit plugin-addition rule + PR-template gate, plugin manifest TOML 5-key contract, SARIF rule-ID regex `^[A-Z]{2,4}-[A-Z]{1,3}-\d{1,3}$`, dogfooding gate (zero `level: error` against this repo), composite-Action zero-required-input UX, release ZIP + SHA-256 checksums for every `v*` tag, single-source-of-truth `VERSION` file (AC-CL-20 doc analogue), 5 mandatory CI templates (GitHub/GitLab/Azure/Jenkins/Bitbucket), `06-rules-mapping.md` every-rule-row table with relative spec-source links, closed severity enum {error,warning,note}, performance budget (single<5s, full<60s on 10k-LOC), middle-out cost-tiered probe order, idempotent+checksum-verified+non-interactive install.sh, per-check `_tests/fixtures/{good,bad}/` gate, self-application via `--self-test` mode. Legacy 7 prose criteria preserved as AC-CI-LEGACY-001..007 at end of §97. Module-level tree-health: 100/100 (A+).
>
> **🚨 B2 collision noted:** This module shares slot `06-` with `06-ai-optimization/` (both carry full §97 GWT contracts post-Phase-16n+16o). Resolution requires user decision; tracked in `mem://specs/full-tree-audit-v4`.
---

## File Inventory
<!-- verified-phase: 147 -->

| # | File | Status | Purpose |
|---|------|--------|---------|
| 1 | `00-overview.md` | ✅ Present | Module overview, scope, goals |
| 2 | `01-sarif-contract.md` | ✅ Present | SARIF 2.1.0 emission contract |
| 3 | `02-plugin-model.md` | ✅ Present | Language-plugin architecture |
| 4 | `03-language-roadmap.md` | ✅ Present | Phase 1/2/3 language coverage plan |
| 5 | `04-ci-templates.md` | ✅ Present | GitHub Actions / GitLab / Azure DevOps / Jenkins / Bitbucket templates |
| 6 | `05-distribution.md` | ✅ Present | How `linters-cicd/` is published |
| 7 | `06-rules-mapping.md` | ✅ Present | CODE RED rule ↔ linter checker mapping |
| 8 | `07-performance.md` | ✅ Present | Performance budget per linter run |
| 9 | `97-acceptance-criteria.md` | ✅ Present | Acceptance criteria for the linter pack |
| 10 | `98-faq.md` | ✅ Present | FAQ (note: occupies 98 slot conventionally used for changelog) |
| 11 | `99-troubleshooting.md` | ✅ Present | Troubleshooting guide (note: occupies 99 slot conventionally used for consistency report) |
| 12 | `99-consistency-report.md` | ✅ This file | Consistency report (added 2026-04-25 to satisfy the universal §99 convention) |

---

## Slot-Naming Notes

This module deviates from the universal `98-changelog.md` / `99-consistency-report.md` convention:

- `98-faq.md` occupies the 98 slot — the module has no formal changelog yet. Treat the FAQ as informal change history until a formal `98-changelog.md` is authored.
- `99-troubleshooting.md` occupies the 99 slot — kept for backward compatibility with existing cross-references. **This file (`99-consistency-report.md`) is the canonical §99 going forward.**

> Slot collision is recorded as a **known deviation, not an error**. Both 99-files coexist; the `-troubleshooting` suffix disambiguates.

---

## Cross-Reference Validation

| Source | Target | Status |
|--------|--------|--------|
| `00-overview.md` | `01-sarif-contract.md` | ✅ |
| `00-overview.md` | `02-plugin-model.md` | ✅ |
| `00-overview.md` | `06-rules-mapping.md` | ✅ |
| `04-ci-templates.md` | `01-sarif-contract.md` | ✅ |
| `06-rules-mapping.md` | `../01-cross-language/15-master-coding-guidelines/00-overview.md` | ✅ |

---

## Naming Compliance

- File prefixes: `00`, `01`–`07`, `97`, `98`, `99` — sequential except for slot-99 deviation noted above.
- Markdown headings consistent with neighbour modules ✅.
- No PascalCase database identifiers (process module, not data spec) — N/A ✅.

---

## Open Items

1. **Author formal `98-changelog.md`** — currently the module's history lives in PR descriptions and the FAQ. Low priority while still in Phase 1.
2. **Decide slot-99 disambiguation policy** — either keep both 99-files (current state) or rename `99-troubleshooting.md` → `08-troubleshooting.md`. Defer until owner decides.

---

## Health Score

92/100 (A−) — all required content present; deduction is for the dual-99 slot deviation and missing formal changelog. Both are documented and intentional, not silent drift.

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-25 | 1.0.0 | Initial consistency report (added during root §99 audit follow-up) |

### 2026-04-27 — Phase 76 deepening

- Mermaid lifecycle diagram added.
- SQL DDL audit-log schema inlined.
- Implementability raised 90 → 100.

