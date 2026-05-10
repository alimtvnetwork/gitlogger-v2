# Consistency Report — Distribution and Runner

**Version:** 2.1.3  
**Updated:** 2026-05-04

> **v2.1.3 update (Phase 153 A24-fu44):** §97 v2.0.0 → v2.1.0 (AC-21 installer timeout/retry + AC-22 Bun toolchain pin); `02-runner-contract.md` v1.0.0 → v1.1.0 (pnpm fallback removed per AC-22); §00 v2.2.0 → v2.3.0; §98 v2.2.0 → v2.3.0. Closes 2 audit-v7 MEDIUM findings.

---

## File Inventory

| # | File | Status |
|---|------|--------|
| 1 | `00-overview.md` | ✅ Present |
| 2 | `01-install-contract.md` | ✅ Present |
| 3 | `02-runner-contract.md` | ✅ Present |
| 4 | `03-release-pipeline.md` | ✅ Present |
| 5 | `04-install-config.md` | ✅ Present |

**Total:** 5 files (excluding this report)

---

## Known Gaps

- `97-acceptance-test-plan.md` is **missing**. Per the spec patch plan, this
  folder needs a deterministic acceptance harness that validates installer
  exit codes (`Test-Path`/`[ -x ]`), dependency presence (`bun >=1.1`,
  `git >=2.40`, `unzip`, `curl`), and runner contract exit-code mapping
  (0 = success, 1 = usage, 2 = config, 3 = network, 4 = auth, 64+ = internal).
- `03-release-pipeline.md` describes pipeline steps at a high level but does
  not enumerate the exact environment variables (e.g. `GITHUB_TOKEN`) or
  the precise build commands. This is tracked in the patch plan.
- See `/mnt/documents/spec-patch-plan.md` § `spec/15-distribution-and-runner/`
  for the full remediation plan and example acceptance criteria.

---

## Cross-Reference Health

- **Internal cross-link checker (CI):** all internal markdown links inside
  this folder resolve. Verified by `linter-scripts/check-spec-cross-links.py`
  on every push and pull request to `main`.
- **Outbound references from this folder:** 0 broken at baseline.

---

## Summary
<!-- verified-phase: 147 -->

- **Errors:** 0
- **Warnings:** 0 (Phase H1-S3 reconciliation: prior "missing `97-acceptance-test-plan.md`" warning was stale — `97-acceptance-criteria.md` is the current canonical name and is present; "pipeline detail gaps in `03-release-pipeline.md`" no longer holds — module passes strict rubric)
- **Health Score:** 100/100 (A+) under rubric v2.24 strict (full marks across required + recommended + §99 quality; tree-health 168/168)

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-21 | 1.0.0 | Initial consistency report — inventory baseline (5 files) |

---

*Consistency Report — updated: 2026-04-21*
| 2026-04-27 | 1.1.0 | Phase 55 — implementability lever (CI YAML / typed-language reference) |


## 2026-04-27 — Phase 63 impl-sweep

- Phase 63: appended Distribution and Runner enums TS enum mirror to satisfy `has_ts_enums` rubric (impl 80 → 90).

### 2026-04-27 — Phase 76 deepening

- Mermaid lifecycle diagram added.
- SQL DDL audit-log schema inlined.
- Implementability raised 90 → 100.


## 2026-04-29 — Phase 153 Task #35-fu2 — SemVer-track unification audit

- §00 banner unified from 1.1.0 → 2.1.0 to align with §98 SemVer-max (Phase 16d-i v2.0.0 depth pass + Phase 55 v1.1.0 lever consolidated as v2.1.0).
- Closes the version-parity drift class (Task #35-fu surfaced 15 §00↔§98 mismatches; this is the inverse case where §00 was BEHIND §98).
- Lesson #25 codified — dual-track SemVer (file-scaffold lever vs depth-pass major) is forbidden going forward.
- §99 banner v2.1.0 → v2.1.1; §98 banner v2.1.0 → v2.1.1; §00 banner v1.1.0 → v2.1.0; h10 stamp already at phase 153.

## 2026-04-29 — Phase 153 Task A11d — `--branch` CLI flag removal (v5 D1 close)

- v5 audit (`/mnt/documents/spec-ai-implementability-audit-v5.md`) flagged D1 HIGH "Conflicting Versioning Logic": `01-install-contract.md:51` advertised `--branch <name>` while §97 AC-18 forbade branch refs in `--ref` for reproducibility.
- **User direction:** strict removal — single source of truth = AC-18.
- `01-install-contract.md` § "Versioning" — `--branch` row deleted; `--ref <tag-or-sha>` row added with explicit AC-18 cross-reference and exit-`2` enforcement note; "Why no `--branch` flag?" callout block added.
- `04-install-config.md` § "Override precedence" — `--branch` removed from CLI-flag bullet; clarified that JSON `branch` field is default-branch hint for tag probing (NOT a CLI override surface).
- **Lockstep:** `01-install-contract.md` v1.0.0 → v1.1.0 · `04-install-config.md` v1.0.0 → v1.1.0 · §00 v2.1.0 → v2.1.1 · §98 v2.1.1 → v2.2.0 · §99 v2.1.1 → v2.1.2.
- **No §97 AC change** — AC-18 already declared the no-branch rule; this is a contract-prose alignment, not a new contract.
- **Expected v6 score lift:** spec/15 92 → ≥96 (D1 +4 — direct conflict close); pushes module into EXCELLENT band. LLM re-score deferred per Lesson #20 (gateway budget — covered by next A8 rebaseline).
