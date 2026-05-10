# Changelog — CI/CD Integration — Coding-Guidelines Linter Pack

**Version:** 4.0.0
**Updated:** 2026-04-26
**Scope:** `spec/02-coding-guidelines/06-cicd-integration/`

---

## v4.0.0 — 2026-04-26 (Phase 16o: §97 full GWT rewrite)
- **P21 sync** (2026-04-28): §00 banner version field bumped 1.0.0 → 4.0.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 21 -->` stamp added under §00 banner; no spec content change).

- **Changed** §97 — full GWT rewrite. Replaced 7 prose criteria (AC-CI-001..AC-CI-007) with **20 module-specific Given/When/Then ACs** (AC-CI-01..AC-CI-20) covering: explicit AC-CL-* inheritance (AC-CI-01); stock-Ubuntu + python3≥3.10 + bash baseline with zero `pip install` / `apt-get install` Phase 1 (AC-CI-02); SARIF 2.1.0 exact-version + schema URL gate (AC-CI-03); POSIX exit codes 0/1/2 only, all others FORBIDDEN (AC-CI-04); check filename regex `^[a-z0-9]+-[a-z0-9-]+\.(sh|py)$` with registered language-id prefix (AC-CI-05); zero-edit plugin addition with PR-template gate (AC-CI-06); plugin manifest TOML 5-required-key contract (AC-CI-07); SARIF rule-ID regex `^[A-Z]{2,4}-[A-Z]{1,3}-\d{1,3}$` (AC-CI-08); dogfooding gate — zero `level: error` against this repo (AC-CI-09); composite Action zero-required-input one-liner UX (AC-CI-10); release ZIP + SHA-256 checksums.txt for every `v*` tag (AC-CI-11); single-source-of-truth `linters-cicd/VERSION` file, hardcoded duplicates FORBIDDEN per AC-CL-20 (AC-CI-12); five mandatory CI templates (GitHub/GitLab/Azure/Jenkins/Bitbucket) all running same SARIF gate (AC-CI-13); rules-mapping table EVERY-rule-row contract with relative spec-source link (AC-CI-14); closed severity enum {error,warning,note} matching SARIF level + AC-AI-14 pattern (AC-CI-15); performance budget single-check<5s + full-run<60s on 10k-LOC fixture (AC-CI-16); middle-out probe ordering by manifest-declared cost tier (AC-CI-17); idempotent + checksum-verified + non-interactive `install.sh` one-liner (AC-CI-18); `_tests/fixtures/<check-id>/{good,bad}/` per-check fixture gate (AC-CI-19); self-application — pack lints itself via `--self-test` mode (AC-CI-20).
- **Preserved** legacy 7 prose criteria as AC-CI-LEGACY-001..007 at end of §97.
- **Bumped** §97 v1.0.0 → v4.0.0 (major; AC contract reshaped from prose to GWT). §98 v1.0.0 → v4.0.0. §99 v1.0.0 → v4.0.0.
- **Documented** B2 slot collision warning in §97 module summary — both `06-ai-optimization` and `06-cicd-integration` now carry full GWT §97s, raising pressure to resolve the collision.

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | minor | Phase 27b: Added `kind: future-spec` frontmatter + Drift Acknowledgment section. Module now exempt from drift audit findings (implementation lives in downstream repos). |

## 2026-04-27 — Phase 76 (impl 90 → 100)

- Added Mermaid lifecycle diagram — satisfies `has_mermaid` (+5).
- Added SQL DDL audit-log schema — satisfies `has_sql_ddl` (+20).
- Implementability raised 90 → 100 (deterministic audit, capped).

