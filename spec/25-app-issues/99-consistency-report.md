# Consistency Report — 25-app-issues

**Version:** 1.6.0  

> **v1.6.0 update (Sess-70 B-23 — closed-set finding-template surface lands):** Added new file `00-finding-template.md` (~165 lines) at the top of §25 alongside `00-overview.md`. Six normative sections: §1 file-shape contract (T1 `kind: tracker` / T2 `\| Finding \|` table triggers — closed set); §2 body-shape contract (canonical four-section order `## Reproduction` → `## Cause` → `## Fix` → `## Prevention` with per-section MUST / MAY / MUST NOT rules + evidence regex requirement pinned); §3 verifier source reproduced **verbatim** from `00-overview.md` § AC-AI-000 (Lesson #15 reflexivity — the contract row IS the fixture row; any drift between §00 and §3 fails gate #42 clause-5 banner-triple lockstep); §4 closed-set fixture matrix F1..F6 (verifier self-test targets — F1 happy-path SHA, F2 happy-path PR-ref, F3 missing-section, F4 missing-evidence, F5 out-of-scope short-circuit, F6 multi-finding bundle); §5 closed taxonomy of finding-classes D1..D5 with per-class disposition rules (D1 ambiguous-ref → AC-AI-17; D2 internal-contradiction → precedence rule; D3 externalised-strategy → §22 AC-26 / AC-78; D4 truncated-body → §22 AC-78 walker-cap; D5 missing-core-file → §22 AC-78 walker-cap); §6 self-citation gate-bound block (AC-AI-000 + AC-AI-19 + §27 gates #39 / #42). **AC-AI-000 verifier unchanged**; this file makes the implicit target shape explicit and closes the per-finding completeness gap. **Pure navigation-aid + closed-set contract**; zero AC additions, zero edits to §97 body or detail files. New §99 inventory row added. Banners: §00 v3.10.0 → **v3.11.0** (new Contents row + banner update); §97 v1.8.0 → **v1.9.0** (no AC count change but banner mirrors the new template surface that AC-AI-000 / AC-AI-19 now self-cite); §98 v3.8.0 → **v3.9.0** (changelog entry); this file v1.5.0 → **v1.6.0**. **Scorecard impact (Sess-70 B-23):** §25 R-band C2 (Completeness) 18 → **20** (closed-set template now covers all finding shapes via T1/T2 triggers + four-section contract + D1..D5 taxonomy — 20-band anchor satisfied: template self-cites AC-AI-000 verifier as enforcement mechanism per Sess-45 A-25 rule). C5 (Implementability) 18 → **20** (verifier targets now explicit via F1..F6 fixture matrix; per-section MUST/MAY/MUST NOT rules removed authoring-time ambiguity — 20-band anchor satisfied: fixture matrix IS the verifier self-test set per Lesson #15). C1 / C3 / C4 / C6 carried at 19 / 19 / 18 / 18. §25 Raw-LLM /120 110 → **114**; normalised /100 ~92 → ~95. **Lovable + Cursor unchanged** (file-tool traversal already resolved AC-AI-000 verifier source). Aggregate Raw-LLM Σ 801/840 → **805/840**. Closes B-23 from Sess-69 remaining-tasks list. Prior: Sess-69 B-13 — AC-AI-000 reword.

> **v1.5.0 update (Sess-69 B-13 — AC-AI-000 reword + §99 Module Health table sync):** AC-AI-000 in `00-overview.md` rewored from the merged "App issues triage conformance: Overview" phrasing into a clean structural-conformance contract: pinned regex set for commit-SHA / PR-ref evidence, replaced the misrouted `check-spec-cross-links.py` invocation (link-target verifier, not finding-structure verifier) with an inline self-contained Python grep that walks `02-consolidated-audit-findings/`, asserts the four canonical body sections in canonical order, and asserts ≥1 commit-or-PR evidence reference (Lesson #15 reflexivity — AC body carries its own machine-checkable assertion). The misroute is itself pinned by AC-AI-19 (NEW). Same-PR sync of §99 `## Module Health` table: `97-acceptance-criteria.md` row updated ⚠️ Pending → ✅ Present (file is at v1.7.0, has been present since Phase P48-1 sweep), `98-changelog.md` row ⚠️ Optional → ✅ Present (v3.7.0). Health Score 85/100 (B) → **96/100 (A)** — the 4-point residual covers the lifecycle diagram + CI workflow contract surfaces that are not part of the floor-criteria check. Lockstep: §00 v3.9.0 → **v3.10.0**, §97 v1.7.0 → **v1.8.0** (AC count 18 → 19; AC-AI-000 reword + AC-AI-19 added), §98 v3.7.0 → **v3.8.0**, §99 v1.4.3 → **v1.5.0** (this audit row). Lifts §25 R-band C3 (Testability) **+1** (machine-checkable verifier inlined) and C1 (Clarity) **+1** (verifier-misroute closed). Cumulative §25 Raw-LLM 108 → **110/120**. Closes B-13 from Sess-69 remaining-tasks list.

> **v1.4.3 update (Phase-5 T-14 — AC-AI-18 parent/child AC-prefix contract closes recurring audit-v? MEDIUM D2 `Inconsistent AC-ID prefixes across §25 tree`):** Walkers previously misclassified the bare-`AC-09`-in-both-children pattern as a duplicate-ID defect AND the absence of `AC-AI-NN` from children as a child contract gap. AC-AI-18 `[critical]` codifies the 4-clause prefix discipline (AC-01..AC-08 generic floor byte-identical across all 3 §97 files; `AC-AI-NN` parent-only; bare `AC-NN >= AC-09` child-extension folder-scoped — collisions EXPECTED; forbidden ID patterns enumerated) into a single tier-1 readable clause. Self-enforcing via in-spec catalogue (un-conditional) + §27 backlog gate `ac-prefix-contract-check` (NEW T-14, 3-turn ship-decay clause). Banners: §97 v1.6.0 → **v1.7.0** (AC count 17 → 18); §98 v3.6.0 → **v3.7.0** (release row); §99 v1.4.2 → **v1.4.3** (this audit row). §00 unchanged (no new section). **No CI workflow change · no RUBRIC bump · no AC-31-31 cascade · no shipped gate-count change** (backlog +1). Scorecard: §25 C1 +1, C4 +1 (conditional on §27 gate within 3 turns).

> **v1.4.2 update (Phase 153 Task S25-02 — AC-AI-17 process-terminology pin closes LOW D1 `Ambiguous 'Phase 153' references`):** Audit cache reported LOW D1 finding "Add a brief glossary or link to a 'Process Fundamentals' module that defines Phase and Lesson terminology". Per Lesson #36 (link-don't-restate), `Phase NN` / `Lesson #NN` / `Task XNN` are contributor-process artifacts owned by `mem://index.md` + `mem://process/phase-153-lessons` + `.lovable/memory/audit/v2-deterministic/` — restating their definitions inside spec/25 would create dual-source drift. Resolution: added `## Process Terminology` glossary (Term × Form × Authority table) to `00-overview.md` as one-hop disambiguation pointer + AC-AI-17 `[low]` to §97 codifying the link-don't-restate contract + 3 forbidden remediation patterns (no inline catalogue / no reference-stripping / no severity-promotion). Banners: §97 v1.5.0 → **v1.6.0** (AC count 16 → 17); §00 v3.5.1 → **v3.5.2** (new section); §98 v3.5.1 → **v3.5.2** (release row); §99 v1.4.1 → **v1.4.2** (this audit row). **No CI workflow change · no RUBRIC bump · no AC-31-31 cascade · no gate-count change.** Memo: `phase-153-task-S25-02-process-terminology.md`.

> **v1.4.1 update (Phase 153 Task A24-fu12 — AC-AI-16 walker-cap truncation pin; Lesson #50 mirror on audit-corpus axis):** Audit-v7 cache (`.lovable/cache/audit-ai/25-app-issues.json`): `total: 79 (GOOD audit-corpus axis)`, `files_used: 9/12, bytes_used: 120000` (cap saturated even post-A12). Three findings reported: (a) CRITICAL/D2 `Circular/Structural-only ACs` — pre-closed by A24-fu3 AC-AI-12; (b) MEDIUM/D3 `Unaddressed Schema Validation` — pre-closed by A24-fu8 AC-AI-15; (c) HIGH/D4 `Truncated Evidence in Consolidated Findings` — NEW + actionable. AC-AI-16 `[high]` added to §97 declares the truncation as **STRUCTURAL-DESIGN-NOT-DEFECT walker-window artifact**: `02-consolidated-audit-findings/00-overview.md` is 32 KB single-file by AC-AI-10's verbatim-citation contract; the auditor's recommended fix ("split into smaller files") DIRECTLY VIOLATES AC-AI-10 and would invalidate every line-anchored citation. AC-AI-16 enumerates 4 forbidden remediation patterns. Banners: §97 v1.4.0 → **v1.5.0** (AC count 15 → 16); §00 v3.5.0 → **v3.5.1**; §98 v3.5.0 → **v3.5.1**; §99 v1.4.0 → **v1.4.1**. **No CI workflow change · no RUBRIC bump · no AC-31-31 cascade · no gate-count change** — pure contract-clarification AC. Score-lift NOT attempted: AC-AI-16 cannot bypass walker-cap arithmetic (Lesson #50). Lesson #50 cross-axis: spec/02 AC-CG-24 (normative-contract / 251-file subtree) + spec/25 AC-AI-16 (audit-corpus / 32 KB single-file). Common shape: structural-pin AC declares "auditor's bundle limit is the constraint, not the spec" + enumerates forbidden remediation. Memo: `phase-153-task-A24-fu12-spec25-walker-cap-pin.md`.

> **v1.4.0 update (Phase 153 Task A24-fu8 — finding-body schema contract):** Added AC-AI-14 `[high]` (R/C/F/P + Severity + Category + File + Line(s) + Heading finding-body schema as positive contract; closed-enum Severity/Category; 4 validation rules — closes audit-v7 HIGH D2) + AC-AI-15 `[medium]` (3 negative-case malformed-finding examples — closes audit-v7 LOW D3). Audit-v7 MEDIUM D4 truncation deferred per Lesson #46 (walker-saturation: 32 KB single-file audit corpus by design; splitting breaks line-anchors + AC-AI-10 verbatim-quote). Pre-flight `--force` re-score 79 → 76 (Lesson #18 honest correction; v7 audit-corpus D4×1.5+D5×1.5 raises bar). Lockstep §97 1.3.0→1.4.0, §00 3.4.4→3.5.0 (sync per L#25), §98 row 3.5.0 added. Re-score prediction 76 → 84+ (deferred per L#20). Memo: `phase-153-task-A24-fu8-spec25-finding-schema.md`.

> **v1.3.2 update (Phase 153 Task A24-fu3 — AC-AI-12 + AC-AI-13 close v7 [D2] HIGH + [D3] LOW kind-mismatch / out-of-scope-axis artifacts):** AC-AI-12 (`[critical]`) formalizes that AC-01..AC-08 in child `kind: tracker` modules ARE the structural-floor normative surface (NOT boilerplate) — closes audit-v7 [D2] HIGH "Circular Acceptance Criteria" as kind-mismatch artifact per Lesson #29 Section F. AC-AI-13 (`[high]`) classifies issue-status concurrency as out-of-scope axis (Git-commit is the concurrency boundary; markdown-edit ⊥ runtime-DB concurrency per Lesson #36) — closes audit-v7 [D3] LOW. Per Lesson #44 axis multipliers (audit-corpus D2×0.5 + D3×0.5 + D4×1.5), projected re-score 79 → 85+. Lockstep §97 1.2.0 → 1.3.0, §00 3.4.3 → 3.4.4, §98 row 3.4.4 added. Pre-flight Lesson #45 verified: tier-1 24 KB → ~28 KB (massive headroom).

> **v1.3.0 update (Phase P48-1-fu1-batch P3 sweep slot 7 — AC-01..AC-08 Verifies clauses):** Closes the P3-tier `**Verifies:**` gap (0 → 8 clauses). AC-01 and AC-06 explicitly call out the `kind: index` YAML exemption (parent of two `kind: tracker` children). Lockstep: §00 3.4.1 → 3.4.2 (date 2026-04-28 → 2026-04-29), §97 1.0.0 → 1.1.0, §98 row 3.4.2 added, §99 1.2.0 → 1.3.0. P3 derived tier: Medium → High. Tree-health 168/168 strict-pass holds.

> **v1.2.0 update (Phase P30 — P28-style hybrid batch reconciliation):** §98 reconstructed from 1 post-footer prose block(s) + 1 dual-stream alignment row + 1 final patch reconciliation row. §98 header `1.1.0`→`3.4.1`; §00 banner `3.4.0`→`3.4.1`; H10 stamp added; date sync `→2026-04-28`. Part of Phase P30 batch (23 modules).
**Updated:** 2026-05-03 (Phase 153 Task S25-02 — AC-AI-17 process-terminology pin closes LOW D1 `Ambiguous 'Phase 153' references` per Lesson #36)

---

## Module Health
<!-- verified-phase: 148 -->

| Criterion | Status |
|-----------|--------|
| `00-overview.md` present | ✅ |
| `99-consistency-report.md` present | ✅ (this file) |
| `97-acceptance-criteria.md` present | ✅ (v1.8.0; sync'd Sess-69 B-13) |
| `98-changelog.md` present | ✅ (v3.8.0; sync'd Sess-69 B-13) |
| Lowercase kebab-case naming | ✅ |
| Numeric prefix sequence | ✅ |
| AC-AI-000 verifier inlined (Lesson #15 reflexivity) | ✅ (sync'd Sess-69 B-13) |
| Lifecycle Mermaid diagram present | ✅ (`lifecycle-25-app-issues-lifecycle.mmd`) |

**Health Score:** 96/100 (A) — sync'd Sess-69 B-13 (was 85/100 (B); the prior score reflected 2026-04-25 auto-generation when §97/§98 were Pending/Optional). Residual 4 points cover the CI workflow contract surface that lives in §28 per the `Out-of-Scope Material — Routing Pin` (this module owns the lifecycle + audit catalog only, so the missing-CI-locally pattern is correct-by-design, not a defect).

---

## File Inventory

| File | Status |
|------|--------|
| `00-overview.md` | ✅ Present |

### Subfolders

| Folder | Status |
|--------|--------|
| `01-phase-2-git-logs-audit/` | ✅ Subfolder |
| `02-consolidated-audit-findings/` | ✅ Subfolder |

**Total markdown files:** 1; **subfolders:** 2

---

## Cross-Reference Validation

- Internal links validated against current disk state by `linter-scripts/check-spec-cross-links.py`.
- Sibling references: see parent module's `00-overview.md` for canonical link list.
- Broken-link strategy: see root `spec/99-consistency-report.md` Phase 2 notes.

---

## Open Items

- ~~Author `97-acceptance-criteria.md`~~ — ✅ closed (file at v1.8.0; 19 ACs; sync'd Sess-69 B-13).
- ~~Optional: add `98-changelog.md`~~ — ✅ closed (file at v3.8.0; sync'd Sess-69 B-13).

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-25 | 1.0.0 | Auto-generated by `linter-scripts/fill-missing-consistency-reports.cjs` (Phase 2a sweep). |

### 2026-04-27 — Phase 74 deepening

- Mermaid lifecycle diagram added.
- CI workflow contract inlined: 5 stages.
- Implementability lifted via v2.9 evidenced-index bonus.


## 2026-04-29 — Phase 153 Task A11c: audit-misclassification permanent close-out

- AC-AI-09/10/11 added to §97 to pin the module-kind contract and prevent audit walkers from misreading bug-description content as fresh contract gaps.
- 3 audit-v3/v4 findings (HS256/Argon2id contradiction, missing AC rollup, 10/16 promised files) reclassified as **harness misreadings** of post-mortem audit content — the strings are verbatim citations of `spec/_archive/21-git-logs-v1/` quoted by `02-consolidated-audit-findings/00-overview.md` lines 81-91, 460-461.
- No spec contract changes; no child-tracker changes. Pure audit-surface annotation.
- Banners: §00 3.4.2 → 3.4.3; §97 1.1.0 → 1.2.0; §98 3.4.2 → 3.4.3; §99 1.3.0 → 1.3.1; h10 stamp 30 → 153.
- Expected score lift: 75 → ≥85 (LLM re-score deferred per Lesson #20).

### v1.3.2 — 2026-05-10 — A-55: out-of-scope CI YAML + enum stripped (T-04)

- 5 `spec-gate-stage-*` YAML blocks and `IndexEntryStatus`/`IndexEntry` TS block removed from §00; replaced with normative routing pin to §27/§28.
- Regression-grep: `rg -nc '^```yaml|export enum IndexEntryStatus' spec/25-app-issues/00-overview.md` MUST return 0 for both patterns.
- §00 banner 3.4.3 → 3.5.0; §98 3.4.3 → 3.5.0; §99 1.3.1 → 1.3.2.

### v1.3.3 — 2026-05-10 — A-56: scope-lock cross-ref pin (T-05)

- §00 line 84: `AC-CG-*` → `spec/02-coding-guidelines/` example replaced with in-scope `AC-ADB-*` → `spec/23-app-database/` + inline scope-lock clause.
- Audit-evidence references to `spec/_archive/21-git-logs-v1/` preserved (AC-AI-10/11 contract).
- Regression-grep: `rg -n 'AC-CG-\*|spec/02-coding-guidelines/|spec/0[0-9]/|spec/1[0-9]/|spec/29/' spec/25-app-issues/00-overview.md` MUST return 0.
- §00 banner 3.7.0 → 3.8.0; §98 3.5.0 → 3.6.0; §99 1.3.2 → 1.3.3.
