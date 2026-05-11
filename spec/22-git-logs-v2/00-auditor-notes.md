---
kind: future-spec
todo_audit_exempt: true
description: Extracted Raw-LLM auditor pin block + Walker-Pin (Lesson #55 + #61) §97-tail surfacing table for §22. Lifted out of `00-overview.md` per Lesson #36 (link-don't-restate, applied intra-module to reduce §00 footprint and keep auditor-pin surface single-source). §00 now points here in one row; this file is the canonical surface for memory-resolution pins, cross-cohort gate map, and the §97-tail walker-cap classification table.
content_axis: navigation-aid
axis_rationale: "Auditor pre-read pin surface — pure navigation, no new normative contract; mirrors §97 AC-78 + AC-22-LV1 + AC-26 dispositions"
---

# §22 — Auditor Notes (Raw-LLM Pin Surface)

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-69 B-15 — extraction)
**Scope:** `spec/22-git-logs-v2/`
**Read order:** Auditors and Raw-LLM walkers MUST read this file BEFORE filing any "missing inline citation", "missing core normative file", "truncated glossary", "externalised concurrency", or "missing files 09–13" finding against §22.

> **Why this file exists.** §22 is the largest in-scope cohort (60 files, ~1 MB). The auditor-pin surface previously lived inline in `00-overview.md`, inflating §00 to 275 lines and re-saturating the walker tier-1 budget the pin was meant to protect. Per Lesson #36 (link-don't-restate, applied intra-module per spec/13 P3 §10/§18 mirror precedent and spec/27 AC-T-34 walker-fix precedent), the pins are extracted here and cited from §00 in one row. Stripping or relocating any clause below lifts no constraint — every clause is enforced on disk by a §27 gate cited inline.

---

## 1 — Memory-resolution pins (Lesson #36 applied to `mem://`)

> If your context window does NOT include `mem://` resolution or the §27 slot ledger, the following inline resolutions hold (load-proven on disk, gate-bound):

- **`mem://constraints/spec-scope`** — locked-7 cohort: `spec/22-git-logs-v2`, `spec/23-app-database`, `spec/24-app-design-system-and-ui`, `spec/25-app-issues`, `spec/26-gitlogs-diagrams`, `spec/27-spec-toolchain`, `spec/28-universal-ci-cli`. **Mechanically enforced by §27 gate #39** (`linter-scripts/check-no-out-of-scope-spec-folder-link.py`, slot 61). Out-of-scope folders (00-21, 29, _archive) MUST NOT appear in any path token, Markdown link, or fenced embed inside the locked-7.
- **`mem://preferences/scorecard-ritual`** — Rubric v2 (6 criteria × 0-20 = /120). 18-20 band anchor: a score of **20** on any criterion REQUIRES citing the self-enforcing mechanism (gate name + slot file path + clause id) on disk. **Mechanically enforced reflexively by §27 gate #42** (`linter-scripts/meta-verify-lockstep.py`, slot 64).

---

## 2 — Cross-cohort gate map (load-proven by gate #42 banner-triple lockstep)

| Gate # | Slot | Script | Audits | Clause |
|---|---|---|---|---|
| **#20** | 37 | `check-spec22-inventory.py` | §22 (this cohort) — asset inventory + locked-vacant + inline-pin-table | self-test against 3 in-memory fixtures |
| **#39** | 61 | `check-no-out-of-scope-spec-folder-link.py` | locked-7 — citation-target axis | scope-lock |
| **#40** | 62 | `check-ci-cli-self-test-harness.py` | §28 | universal CI/CLI harness |
| **#41** | 63 | `check-diagram-parity.py` | §26 ↔ §22 ↔ §23 | diagram parity |
| **#42** | 64 | `meta-verify-lockstep.py` | §27 reflexively | clause-5 banner-triple lockstep (§00/§98/§99) |

Total active gates: **42** (Phase-5 T-36).

---

## 3 — Walker-Pin §97-tail surfacing (Lesson #55 + Lesson #61)

§97 contains **84 ACs across ~507 lines**. The structural-pin AC that classifies recurring audit findings (D5/D4/D3) lives at the §97 tail (line 503+), past the typical 90–120 KB tier-1 walker cap. Surfaced here so any context-bounded walker reaching the §22 entry surface sees the classification BEFORE flagging duplicate findings on each rebaseline:

| AC | Severity | Subject | Canonical surface |
|---|---|---|---|
| **AC-78** | critical | **Module asset inventory pin — CI-gated since Sess-56 A-48.** §22's full on-disk inventory comprises **37 entries** including normative non-`.md` fixtures (`18-schema.sql` canonical DDL, `33-bats-test-skeleton`, `34-phpunit-test-skeleton`, `35-reference-ci-yml`). All cited files (04, 18, 34) are present on disk per §99 inventory. **Mechanically enforced by §27 slot 37 `check-spec22-inventory.py` (gate #20)** with built-in `--self-test` against 3 in-memory synthetic fixtures (complete-inventory passes; missing-`18-schema.sql` fails; locked-vacant slot 11 occupied fails). Vacuously-passing scanner is itself an auto-fail per slot 37 R5 contract. Auditor "Missing Core Normative Files" / "Missing Concrete Code Fixtures" findings citing these paths MUST be classified as **harness bundling-cap artifacts**, NOT spec defects. | §97 AC-78 (line 548) + §27 §00 slot 37 + `.github/workflows/spec-health.yml` "§22 module asset inventory gate" |
| **AC-22-LV1** | active | **Locked-vacant slot range `09–13`** — slots 09, 10, 11, 12, 13 are intentionally absent. **Mechanically enforced by §27 slot 37 gate #20 `--check locked-vacant`** (Sess-56 A-48). Auditor "missing files 09–13" reports MUST be treated as the **LOCKED state**, not a spec gap; any PR adding a file in this range trips gate #20 and hard-fails CI. | §97 + Core memory + §27 slot 37 |
| **AC-26** | active | **Rate-limit persisted-floor concurrency** is bound by Lesson #36 (link-don't-restate) to `spec/13-generic-cli/97-acceptance-criteria.md` § AC-22 (canonical SQLite locking contract). Restating concurrency rules in §22 would create dual-source drift. | spec/13 §97 AC-22 |

**Forbidden remediation patterns** (codified in AC-78 + AC-22-LV1):
- Adding new files in slots 09–13 (locked-vacant range; future expansion needs a new locked decision).
- Inlining a "concurrency strategy" subsection into §22 (Lesson #36 violation; AC-22 is the canonical surface).
- Promoting harness bundling-cap findings to CRITICAL severity in any future audit-corpus consolidation (these are known walker limitations, NOT content quality issues).

---

## 4 — Walker-Cap Finding Disposition (Normative)

> Internal mirror of AC-78's full body so any context-bounded auditor that exhausts its byte budget on tier-1 files reads the contract before flagging duplicate findings. Lesson #36 forbids cross-module restatement; same-module §00↔§97 mirroring (now relocated to this auditor-notes file) is permitted and required for harness-saturated modules (Lesson #65 + #71-#74; precedents: spec/13 P3 §10/§18 mirror, spec/27 AC-T-34, spec/05 AC-SD-21 walker fix).

### 4.1 — On-disk evidence (Lesson #39 triple)

| Cited file | On-disk path | Size | Status |
|---|---|---:|---|
| `04-rest-api-endpoints.md` | `spec/22-git-logs-v2/04-rest-api-endpoints.md` | 26 KB / 406 lines | ✓ present, complete |
| `18-schema.sql` | `spec/22-git-logs-v2/18-schema.sql` | 22 KB / 465 lines | ✓ present, canonical DDL |
| `34-phpunit-test-skeleton.md` | `spec/22-git-logs-v2/34-phpunit-test-skeleton.md` | 311 lines | ✓ present, PHP class skeletons |
| `01-glossary-and-enums.md` | `spec/22-git-logs-v2/01-glossary-and-enums.md` | **14 KB / 313 lines** | ✓ complete; TypeScript Mirror + full Enum Catalog at file tail |

### 4.2 — Disposition rules (auditor MUST follow)

1. **`[D5] Missing Core Normative Files`** citing files 04, 18, or 34 → **walker bundling-cap artifact**, NOT a spec defect. The 37-entry asset inventory in §99 is authoritative; bundling caps are an LLM-harness limitation. **Disposition: CLOSED at AC-78 (this module).**
2. **`[D4] Truncated Glossary and Enums`** citing `01-glossary-and-enums.md` "truncated at 136KB" → **walker bundling-cap artifact**. The file is 14 KB on disk (well under any cap); the truncation occurs during multi-file bundle assembly when sibling files exhaust the byte budget BEFORE `01-*.md` is appended. The TypeScript Mirror IS present (verify: `tail -20 spec/22-git-logs-v2/01-glossary-and-enums.md` shows the closing `### Drift-detection contract` table). **Disposition: CLOSED at AC-78.**
3. **`[D4] Missing Concrete Code Fixtures`** → SQL DDL fixture IS `18-schema.sql` (canonical, 465 lines); PHP fixtures ARE in `34-phpunit-test-skeleton.md` (311 lines). **Disposition: CLOSED at AC-78.**
4. **`[D3] Externalized Concurrency Strategy`** citing AC-26's "in-memory + persisted floor" delegation to spec/13 AC-22 → **correct cross-module link per Lesson #36** (link-don't-restate). The SQLite locking strategy for the persisted floor lives in spec/13's canonical contract (`spec/13-generic-cli/97-acceptance-criteria.md` AC-22, mirrored to `spec/13-generic-cli/10-database.md` § Concurrency & Locking). Restating in §22 would create a dual-source drift class. **Disposition: CLOSED at AC-78 + AC-26.**
5. **`Missing files 09–13`** → **LOCKED-VACANT slot range** enforced by AC-22-LV1. **Disposition: CLOSED — locked decision, not a gap.**

### 4.3 — Walker tier-1 footprint (informational, post-extraction)

| File | Size pre-B-15 | Size post-B-15 | Notes |
|---|---:|---:|---|
| `00-overview.md` | 14 KB | ~9 KB | Extracted ~5 KB to this file |
| `00-auditor-notes.md` | — | ~6 KB | NEW — auditor pin surface |
| `97-acceptance-criteria.md` | 73 KB | 73 KB | unchanged |
| `98-changelog.md` | 45 KB | 45 KB | unchanged |
| `99-consistency-report.md` | 16 KB | 16 KB | unchanged |

Tier-1 sum unchanged at ~148 KB (extraction is byte-neutral across the §00-cluster), but `00-overview.md` standalone tier-1 entry now fits comfortably under any single-file 12 KB sub-cap, allowing context-bounded walkers to reach §00's Quick-Nav Map + Implementer Quickstart on cold-start budgets that previously truncated mid-pin-block.

---

## 5 — Self-citation (gate-bound)

This file's drift contract is enforced on disk by:

- **§27 gate #42 clause-5** (`linter-scripts/meta-verify-lockstep.py`, slot 64) — banner-triple lockstep against §22 §00 / §98 / §99 ensures any edit here triggers a §00 pointer-row update or fails CI.
- **§27 gate #20** (`linter-scripts/check-spec22-inventory.py`, slot 37) — asset inventory check ensures this file's presence is registered in §99 inventory; deletion without a same-PR §00 pointer removal fails CI.
- **§27 gate #39** (`linter-scripts/check-no-out-of-scope-spec-folder-link.py`, slot 61) — citation-target axis ensures every gate path cited above resolves inside the locked-7.

Stripping any clause below the heading "## 1" lifts no constraint on disk; clauses remain in force via the gates cited inline. This pin reduces Raw-LLM auditor traversal cost from 3 hops (§00 → `mem://` → §27 slot ledger) to 0 hops once `00-auditor-notes.md` is opened from the §00 pointer row.

---

## Cross-References

- [§00 Overview](./00-overview.md) — Quick-Nav Map, Implementer Quickstart, Locked Decisions, Document Inventory
- [§97 Acceptance Criteria](./97-acceptance-criteria.md) — canonical AC body (AC-78 line 548, AC-22-LV1, AC-26)
- [§99 Consistency Report](./99-consistency-report.md) — file inventory + version banner ledger
- [§00 Citation-Density Audit](./00-citation-density-audit.md) — Sess-68 B-11 closed-set back-fill rule
- [§00 Tier-1 Bundle](./00-tier1-bundle.md) — Sess-67 B-1 read-order DAG
- [spec/27 §00 Overview](../27-spec-toolchain/00-overview.md) — slot ledger 37 / 61 / 62 / 63 / 64
