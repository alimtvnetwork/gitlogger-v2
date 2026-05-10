# Changelog

**Updated:** 2026-05-07

---

## Releases

| 1.2.1 | 2026-05-07 | Phase J7 — AC-Confidence honest baseline correction (Lesson #18 + #29). `**AI Confidence:**` banner re-derived from rubric: High → Production-Ready (P1: zero §97 GWT in tracker-kind module; auditor-correct). Lockstep §00/§98/§99 patch-bump only — no §97 contract change. |

### 1.2.0 — 2026-05-06 (Phase 154 Task #6)

**Second substantive child added under No-Questions Mode Prompt 04 (counter 7/40); `02-post-mortems/` SKIPPED per Lesson #41.**

- **Created** `03-rebaselines/00-overview.md` v1.0.0 — canonical index of 4 frozen baseline subdirectories under `.lovable/memory/audit/v2*/` (audit-v2 release, pre-Phase-16r recovery, pre-Phase-20 reorg, Phase 152 audit-v6 baseline) + live auditor output path. Mirrors `01-findings/` template.
- **Created** `03-rebaselines/99-consistency-report.md` v1.0.0 — submodule health (delegated-index pattern: §00 + §99 only).
- **Pattern:** Per Lesson #36 (link, never restate), index DELEGATES to physical `v2*/` snapshot directories. Renaming or moving them would break `mem://specs/full-tree-audit-v4` reference contracts.
- **`02-post-mortems/` SKIPPED**: per Lesson #41 binding-mechanism survey precondition, surveyed `.lovable/memory/audit/` for genuine drift post-mortems and found **0**: 24 `phase-*.md` memos are session-closure narratives (already excluded by Task #5b §00 per Lesson #36 canonical-surface principle); 1 retrospective memo (`03-error-manage__01-error-resolution__03-retrospectives.md`) is a spec-subsection audit, not a drift incident. Empty corpus — shipping a hollow `02-post-mortems/00-overview.md` listing 0 entries would violate Lesson #84 meta-deferral hygiene. Will scaffold on first genuine drift incident.
- **Gateway re-probe** (Lesson #38+#86 contract): `LOVABLE_API_KEY` SET ✅; `audit-ai-implementability.py --module 22-git-logs-v2 --force` → **HTTP 402 Payment Required** (6th oscillation observed; sequence: blocked→unblocked→blocked→unblocked→blocked→blocked). v5 rebaseline + spec/22 walker-cap re-eval remain budget-gated.
- **Lockstep:** §00 v1.1.0 → v1.2.0 (substantive new child + planned-children list updated); §98 v1.1.0 → v1.2.0; §99 v1.1.0 → v1.2.0; h10 stamp 154 → 154 (refresh same phase).
- **Tree expansion:** spec/29-audits surface grows from 5 files to 7 (new `03-rebaselines/00-overview.md` + `99-consistency-report.md`); lockstep gate 89/89 → 90/90; tree-health 174/174 → 177/177 strict expected.

### 1.1.0 — 2026-05-06 (Phase 154 Task #5)


**Substantive child added under No-Questions Mode Prompt 04 (counter 6/40).**

- **Created** `01-findings/00-overview.md` v1.0.0 — canonical index of cross-spec audit findings, classifying 80 module-named memos under `.lovable/memory/audit/` by target spec module (24 modules, ranging spec/01 through spec/26).
- **Pattern:** Per Lesson #36 (link, never restate), the index DELEGATES to physical memo files rather than copying or moving them. This preserves 200+ inbound references from `mem://index.md`, §98 rows, and closing memos at zero ripple cost.
- **Per Lesson #41** (binding-mechanism survey precondition): physical relocation of 80+ memos was rejected as a high-blast-radius, low-implementation-benefit operation. Delegation gives spec/29-audits a discoverable surface without breaking the historical narrative trail.
- **Excluded from index:** 23 `phase-*.md` session-narrative memos remain at `.lovable/memory/audit/` per the §98-row + closing-memo canonical-surface principle. 4 historical baseline subdirectories (`v2/`, `v2-deterministic/`, `v2-deterministic-pre-16r-baseline/`, `v2-deterministic-pre-phase20-baseline/`) remain frozen snapshots referenced from `mem://specs/full-tree-audit-v4`.
- **Lockstep:** §00 v1.0.0 → v1.1.0 (substantive new child); §98 v1.0.0 → v1.1.0; §99 v1.0.0 → v1.1.0; h10 stamp 154 → 154 (same phase, refresh).
- **Tree expansion:** spec/29-audits surface grows from 4 files to 5; lockstep gate 88/88 → 89/89; tree-health 172/172 strict expected.

### 1.0.0 — 2026-05-06 (Phase 154 Task #4)


**Initial scaffold under No-Questions Mode Prompt 04 (counter 4/40).**

- **Created** `spec/29-audits/` as the canonical home for cross-spec audit corpora (findings, post-mortems, rebaseline snapshots) — graduates from ad-hoc `.lovable/memory/audit/` accumulation.
- **Created** `00-overview.md` v1.0.0 with normative `## Module Kind Declaration` subsection (`kind: tracker` + `content_axis: audit-corpus`).
- **Created** `97-acceptance-criteria.md` v1.0.0 with **AC-29-01/02/03** (3 ACs, all module-kind contract):
  - **AC-29-01** `[critical]` — Module classified as audit-corpus tracker (Lesson #29 codified ex-ante, not retrofitted).
  - **AC-29-02** `[critical]` — Finding bodies are auditor-quoted evidence (mirror of spec/25 AC-AI-10).
  - **AC-29-03** `[high]` — Inventory references in finding bodies disambiguated (mirror of spec/25 AC-AI-11).
- **Created** `99-consistency-report.md` v1.0.0 with full File Inventory + Summary stamped `<!-- verified-phase: 154 -->`.
- **Migration deferred:** `01-findings/` / `02-post-mortems/` / `03-rebaselines/` placeholders documented in §00 inventory; population deferred to a later phase.

**Scope discipline:** Pure scaffold — no migration, no children populated. Three contract ACs only.

**Sister-module ripple:**
- `linter-scripts/spec-folder-refs.allowlist` — entry `29-audits` REMOVED per its own conditional-removal note (the live folder now exists; suppressing the ref would mask future drift). Removal carries the comment block update in the same data file (per content/lockstep driver split, Phase 153 lessons memo Section E).
- `.lovable/memory/index.md` — Phase 154 Task #4 closure entry appended.

**Lockstep:** New module — no §97 / §98 / §99 ripple to other modules. Tree-health expected to expand 168/168 → 172/172 (4 new full-marks rows for spec/29). Lockstep gate expected to expand 87/87 → 88/88 (one new module surface).

**Lesson #42 codified:** When scaffolding a new audit-corpus or tracker-kind module, ship the module-kind contract ACs in the SAME phase as the module shell — do not defer. Retrofitting (spec/25 Phase 153 Task A11c precedent) costs more contract surface and risks intervening misclassification. The "ex-ante module-kind pin" pattern is now the canonical template for any new `kind: tracker | post-mortem | audit | index` module.
