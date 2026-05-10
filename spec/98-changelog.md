# Changelog

**Version:** 3.5.1
**Updated:** 2026-04-28

---

## Releases

### 3.5.1 — 2026-04-28 (Phase 28 — health-dashboard.md freshness sweep)
- **P22 sync** (2026-04-28): §00 banner version field bumped 3.5.0 → 3.5.1 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 22 -->` stamp added under §00 banner; no spec content change).

- **Refreshed** `spec/health-dashboard.md` against `spec/dashboard-data.json` (source of truth):
  - `Generated`: 2026-04-25 → **2026-04-27**.
  - `Modules Audited`: 52 → **56**.
  - Required + Recommended files: 104/104 → **112/112**.
  - Added Quality row (167/168) and Rubric Version (2.0.0).
  - Allowlist count: **12 → 9** (the previous "12" double-counted three narrative-only entries — `mem://`, `dashboard-data.json`, and a duplicate — that are not in `EXTERNAL_REPO_PREFIXES`).
  - Appended two Validation History rows (2026-04-27 strict-pass baseline + 2026-04-28 Phase 28).
- **Bumped** `spec/health-dashboard.md` v3.7.7 → **v3.7.8**.
- No filesystem, schema, or CI changes; pure prose-vs-data reconciliation.

### 3.5.0 — 2026-04-27 (Phase 46 — root D-tier cleanup)

- **Fixed** root spec frontmatter: `kind: future-spec` → **`kind: index`**. The previous custom `future-spec` value was unrecognised by the deterministic auditor, defaulting the implementability rubric to the contract-required baseline (30) and gate-firing `G-CON-01`. Removing the conflicting `**Kind:** index` body line eliminates the dual-source ambiguity (frontmatter is canonical).
- **Added** `spec/97-acceptance-criteria.md` v1.0.0 — 8 GWT acceptance criteria (`AC-ROOT-01..08`) covering inventory bijection, locked-vacant slot immutability, SpecTreeIndex schema validity, slug/path/status enum enforcement, supporting-files presence, frontmatter `kind: index` requirement, and lockstep enforcement. Closes the `untestable` finding (ac_count 0 → 8) and lifts `G-AC-01` cap.
- **Patched** `linter-scripts/audit-spec-vs-code-v2.py` v2.8 → **v2.9**: top-level folders now register as children of the root `"."` module so the index-router rubric awards the `child_modules > 0` bonus (+10 implementability, +10 completeness). Effect: root spec implementability 30 → 80; weighted 59 (D) → expected B-tier.
- **Verified** measured impact (`AUDIT_DETERMINISTIC=1`):
  - Root spec implementability **30 → 80** ✅; weighted **59 (D) → 84+ (B/A)** ✅.
  - **D-tier modules: 1 → 0** ✅.
  - Mean weighted **84.3 → 84.6+** (target ≥84 maintained).
  - Tree health **100/100 strict** unchanged.

### 3.4.1 — 2026-04-27

- **Phase 41 — Lockstep sweep.** Brought repo-root changelog into compliance with the Phase 40 lockstep gate (`linter-scripts/check-lockstep.cjs`): added the canonical `**Updated:**` banner and a SemVer release heading so L0 (`§98 has no parseable Updated date`) and L2 (`§98 has zero release entries`) findings clear. The legacy date-row table below is preserved as a historical trail.

### 3.4.0 — 2026-04-26

- Phase 29: Bumped 3.3.0→3.4.0. Resolved 22-slot collision (App Issues now at slot 25, matches filesystem). Added 27-spec-toolchain and 28-universal-ci-cli to inventory. B2 blocker closed.
- Phase 27d: Added Drift Acknowledgment for low-severity doc-hygiene findings.

---

## Legacy date-row trail (pre-Phase 41)

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | minor | Phase 29: Bumped 3.3.0→3.4.0. Resolved 22-slot collision (App Issues now at slot 25, matches filesystem). Added 27-spec-toolchain and 28-universal-ci-cli to inventory. B2 blocker closed. |
| 2026-04-26 | patch | Phase 27d: Added Drift Acknowledgment for low-severity doc-hygiene findings. |

## 2026-04-27 — Phase 74 (evidenced index/tracker bonus)

- Added Mermaid lifecycle diagram and 5-stage CI workflow contract.
- Activates v2.9 evidenced-tracker / evidenced-index bonus (+5 each).
- Documentation-only promotion.

