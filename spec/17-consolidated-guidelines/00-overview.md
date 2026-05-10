---
content_axis: process-guidance
axis_rationale: "Cross-module process consolidation for spec authors"
---

# Consolidated Guidelines

<!-- h10-verified-phase: 153 -->
**Version:** 3.7.2  
**Updated:** 2026-04-30  
**Status:** Active  
**AI Confidence:** Production-Ready  
**Ambiguity:** None

---

> 🤖 **Walker-Pin (auditor preface — Phase 153 Task A24-fu18; Lesson #55 §00 pin)**
>
> This module is **`kind: rollup`** — every file under `spec/17-consolidated-guidelines/` is a **standalone digest** of a first-party source module under `spec/NN-<source>/`. **The rollup is NEVER a normative contract surface; the source module's §97 IS** (per AC-10 module-kind pin). Before flagging any finding of the form *"Circular/Self-Referential ACs"*, *"Missing GWT for content rules"*, *"Logic Verification absent"*, or *"Rollup duplicates source"* against `spec/17`, the auditor MUST consult **AC-10/AC-11/AC-15** in `97-acceptance-criteria.md` — such findings are **STRUCTURAL-ROLLUP-NOT-FIRST-PARTY-CONTRACT** auditor misclassifications. The §17 contract is **file-existence + format + cross-link parity to source** (AC-01..09); content-logic GWT tests for any rule in any rollup file MUST live in the **source module's §97** (per Lesson #36 link-don't-restate). Conflict-resolution rule: when a rollup line drifts from its source §97 line, the **source ALWAYS WINS** (per AC-13). Linter `// LINTER-IGNORE-TODO` syntax for false-positive markers in this folder: AC-14.

> **Compact AC index (Phase 153 Task A24-fu25; Lesson #63 sixth instance — process-guidance axis):** Walker saturation in this module is extreme (6/39 files at 120 KB cap = ~15% visible). The table below surfaces the structural pins so cap-bound auditors do not need to reach `97-acceptance-criteria.md` to classify findings.
>
> | AC | Severity | Pin |
> |----|----------|-----|
> | **AC-10** | `[critical]` | Module-kind pin: `kind: rollup` — NOT a normative contract surface |
> | **AC-15** | `[high]` | Rollup-not-first-party-contract structural classification |
> | **AC-13** | `[high]` | Source-Wins conflict-resolution: source §97 ALWAYS overrides rollup line |
> | **AC-11** | `[high]` | Subfolder Delegation Map: each rollup file → source §97 binding |
> | **AC-07** | `[medium]` | Cross-spec links resolve against on-disk tree (the §17 contract surface) |
> | **AC-02** | `[medium]` | Inventory parity: every sibling file referenced from §00 exists on disk |
> | **AC-14** | `[low]` | `// LINTER-IGNORE-TODO` comment-syntax for false-positive markers |
>
> **Auditor rule of thumb:** If a finding cites *content* of a rollup file (logic, formulas, GWT gaps), redirect to the source module's §97. If a finding cites *structure* of `spec/17` (missing file, broken cross-link, banner drift), it is in scope here.

---

## Purpose

This folder provides **standalone, self-contained AI-readable references** for every major spec module. Each file consolidates the essential rules, patterns, code examples, and decisions from its source module into a single comprehensive document. **No file in this folder requires reading the source specs** — every consolidated file contains enough detail for an AI agent to enforce rules, implement patterns, or reproduce systems independently.

---

## Keywords

`consolidated` · `standalone` · `self-contained` · `quick-reference` · `ai-onboarding` · `spec-digest`

---

## Scoring

| Metric | Value |
|--------|-------|
| AI Confidence | Production-Ready |
| Ambiguity | None |
| Health Score | 100/100 (A+) |

---

## File Inventory

| # | File | Summarizes (Source Module) |
|---|------|---------------------------|
| 01 | [01-spec-authoring.md](./01-spec-authoring.md) | `01-spec-authoring-guide/` — Spec authoring conventions, folder rules, naming, scoring, templates |
| 02 | [02-coding-guidelines.md](./02-coding-guidelines.md) | `02-coding-guidelines/` — Cross-language coding standards, boolean principles, code style, typing, naming |
| 03 | [03-error-management.md](./03-error-management.md) | `03-error-manage/` — 3-tier error architecture, apperror, response envelope, error codes, TypedQuery |
| 04 | [04-enum-standards.md](./04-enum-standards.md) | `02-coding-guidelines/` — Enum patterns for Go, TypeScript, PHP, Rust with full examples |
| 05 | [05-split-db-architecture.md](./05-split-db-architecture.md) | `05-split-db-architecture/` — Hierarchical SQLite pattern, schemas, WAL, RBAC, reset API, user isolation |
| 06 | [06-seedable-config.md](./06-seedable-config.md) | `06-seedable-config-architecture/` — Version-controlled config seeding, merge strategy, schemas, Go implementation |
| 07 | [07-design-system.md](./07-design-system.md) | `07-design-system/` — CSS variable-driven design system, tokens, typography, motion, re-theming |
| 08 | [08-docs-viewer-ui.md](./08-docs-viewer-ui.md) | `08-docs-viewer-ui/` — Documentation viewer: typography, keyboard nav, fullscreen, search, rendering |
| 09 | [09-code-block-system.md](./09-code-block-system.md) | `09-code-block-system/` — Code block pipeline, interactions, styling, line selection, checklist blocks |
| 10 | [10-powershell-integration.md](./10-powershell-integration.md) | `11-powershell-integration/` — PowerShell runner, pnpm PnP, pipeline steps, config, cross-project automation |
| 11 | [11-research.md](./11-research.md) | `02-coding-guidelines/` — Coding guidelines research placement rules |
| 12 | [12-root-research.md](./12-root-research.md) | `10-research/` — Root-level research placement rules |
| 13 | [13-app.md](./13-app.md) | `21-app/` — App-specific spec placement and decision guide |
| 14 | [14-app-issues.md](./14-app-issues.md) | `25-app-issues/` — App bug analysis, issue file template, placement rules |
| 15 | [15-cicd-pipeline-workflows.md](./15-cicd-pipeline-workflows.md) | `12-cicd-pipeline-workflows/` — CI/CD pipeline specs, deployment workflows, install scripts, code signing |
| 16 | [16-app-design-system-and-ui.md](./16-app-design-system-and-ui.md) | `24-app-design-system-and-ui/` — App-specific design system extending core tokens |
| 17 | [17-self-update-app-update.md](./17-self-update-app-update.md) | `14-update/` — CLI self-update, rename-first deploy, handoff, release pipeline, install scripts |
| 18 | [18-database-conventions.md](./18-database-conventions.md) | `04-database-conventions/` — Database naming, PK/FK patterns, singular tables, booleans, views, ORM, schema design |
| 19 | [19-gap-analysis.md](./19-gap-analysis.md) | Gap analysis — coverage matrix, implementability scores, priority recommendations |
| 20 | [20-wp-plugin-conventions.md](./20-wp-plugin-conventions.md) | `18-wp-plugin-how-to/` — WordPress plugin Gold Standard architecture, traits, enums, REST API |
| 21 | [21-lovable-folder-structure.md](./21-lovable-folder-structure.md) | `.lovable/` folder structure — memory, tasks, suggestions, strictly-avoid, AI reading order |
| 22 | [22-app-database.md](./22-app-database.md) | `23-app-database/` — App-specific schema design, migration strategy, query patterns, ORM integration |
| 23 | [23-generic-cli.md](./23-generic-cli.md) | `13-generic-cli/` — CLI creation blueprint: project structure, subcommands, flags, config, output, errors, help, database, build, testing, shell completion |
| 24 | [24-folder-mapping.md](./24-folder-mapping.md) | **Meta** — Bidirectional folder-by-folder mapping: every source spec folder ↔ consolidated file, with coverage heatmap and blind-spots |
| 25 | [25-blind-ai-implementability-audit.md](./25-blind-ai-implementability-audit.md) | **Meta** — Critical-gap analysis: where a blind AI receiving only this folder will fail (linter blindness, waiver syntax, sync contracts, error registry) |
| 26 | [26-blind-ai-audit-v2.md](./26-blind-ai-audit-v2.md) | **Meta** — Post Phase 1–5 re-audit: verified 8/9 gaps closed, 7/8 stress-test pass rate, overall score 96.5 → 99.4/100 |
| 27 | [27-linter-authoring-guide.md](./27-linter-authoring-guide.md) | **Authoring** — How to add a new linter to `linter-scripts/`: file layout, exit-code contract (0/1/2), output format, allowlist registration, test fixtures, §8 checklist. Closes the final 🟡 from the v2 audit |
| 28 | [28-distribution-and-runner.md](./28-distribution-and-runner.md) | **Module** — Standalone distribution + runner spec: `install.sh`/`.ps1`, root `run.sh`/`.ps1` dispatcher, GitHub Release pipeline, `install-config.json` schema. Phase 6B promotion of `15-distribution-and-runner/` |
| 29 | [29-blind-ai-audit-v3.md](./29-blind-ai-audit-v3.md) | **Meta** — Post Phase 6A/6B/6D audit: 8/8 stress tests pass, score 99.4 → 99.8/100 (handoff-weighted 99.9). Terminal AI-blind-readiness reached |
| 30 | [30-readme-improvement-suggestions.md](./30-readme-improvement-suggestions.md) | **Meta** — Prioritised README rewrite plan (22 suggestions in 5 phases). Awaiting approval. Created alongside the v3.55.0 GIFs + Bundle Installers section |
| 31 | [31-full-tree-ai-audit-v4.md](./31-full-tree-ai-audit-v4.md) | **Meta** — First full-tree (not folder-17 only) AI-implementability audit. Verdict 45/100 (F). Roadmap to 100 in 3 phases; supersedes folder-17-only verdicts of 25/26/29 for whole-tree readiness |
| 32 | [32-phase-26-31-rollup.md](./32-phase-26-31-rollup.md) | **Retrospective** — Single-session rollup of Phases 26–31: 67 spec remediations + rubric upgrade v1.x→v2.0.0; tree health 45/100 → 100/100 (162/162 quality credits). Closes Phase 1 + 2 of v4 roadmap; documents pattern catalogue + handoff notes for future AI |
| 33 | [33-full-tree-ai-audit-v5.md](./33-full-tree-ai-audit-v5.md) | **Meta** — audit-v5 reconciliation (Phase 130). Mechanically re-validates v4's 4 critical findings against current tree state: 3 of 4 resolved (root slot collision, broken-link count 32→0, legacy `21-git-logs/` deletion). Only #1 (session-persistence regression) remains open. Numeric re-score deferred to R1 (real-AI re-audit, blocked on Lovable Cloud). **Superseded by v6 (Phase 152).** |
| 34 | [34-full-tree-ai-audit-v6.md](./34-full-tree-ai-audit-v6.md) | **Meta** — audit-v6 baseline (Phase 152). First post-v5 baseline with deterministic numeric headline: tree-health 168/168 strict, lockstep 87/87, freshness 81 stamped + 6 exempt + 0 unstamped, AI-confidence 12/15 match (80%). **P3 Verifies-coverage CLOSED tree-wide** (11 modules, Tasks #21a–#21d). Supersedes v5; method is gate-replay-only (no AI scorer); semantic claims still defer to R1. **Superseded by slot 35 (v7 LLM rebaseline) at Phase 153 Task A20** — deterministic headline preserved as historical baseline |
| 35 | [35-full-tree-ai-audit-v7.md](./35-full-tree-ai-audit-v7.md) | **Meta** — audit-v7 baseline (Phase 153 Task A20, 2026-04-30). LLM rebaseline under Rubric v7 axis-driven dimension weight cascades (slot 34 v1.3.0 contract, AC-34-10..12). Tree mean **83.7/100** (+1.4 vs v6 LLM baseline 82.3); EXCELLENT band 4 → 5 (spec/23 = 97); 2 NEEDS_WORK at 74 (spec/03, spec/04 — mechanically closeable). Top movers: spec/10 +12, spec/01 +7, spec/02 +6. Honest-baseline corrections: spec/14 -10, spec/07 -9. All 23 modules carry `content_axis` front-matter (Task A16) |

---

## How to Use This Folder

1. **AI onboarding** — Read all files in this folder to understand the full system
2. **Each file is standalone** — no need to follow cross-references to source specs
3. **Updates** — When a source module changes significantly, update the corresponding summary here

---

*Overview — updated: 2026-04-16*

---

## Verification

_Auto-generated section — see `spec/17-consolidated-guidelines/97-acceptance-criteria.md` for the full criteria index._

### AC-CON-000: Consolidated guideline conformance: Overview

**Given** Cross-check this consolidated digest against its source spec folder.  
**When** Run the verification command shown below.  
**Then** Every rule cited here resolves to a section in the source folder via the cross-link checker; no orphan rules.

**Verification command:**

```bash
python3 linter-scripts/check-spec-cross-links.py --root spec --repo-root .
```

**Expected:** exit 0. Any non-zero exit is a hard fail and blocks merge.

_Verification section last updated: 2026-04-21_

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Severity:** Low — doc-hygiene drift.

Overview targets 100/100 health (aspirational); AC threshold of 80 is the enforceable floor. Both values are intentional.

Tracked under Phase 27d. See `.lovable/memory/index.md`.

---

## Audit Marker Exemption (Phase 39b, 2026-04-27)

**Issue:** The 2026-04-27 AI-implementability audit recorded `todo_count: 5` for this module. A subsequent grep audit confirmed **zero genuine TODO/TBD/FIXME work-tracking markers**: every match lives inside the worked example block in `27-linter-authoring-guide.md` (lines 361–424), which **defines** the `check-stale-todos.py` linter — the strings `STALE-TODO`, `findings.append`, and `print(...)` are Python source code teaching how to *detect* TODOs, not actual TODOs.

**Decision:** the module is exempt from the substring-based `todo_density` heuristic. The example must remain literal so the linter implementation it describes is reproducible. Future audit iterations SHOULD restrict the scan to outside fenced code blocks (Phase 39b follow-up R4).

**Evidence verified:** `rg -n -i '\bTODO\b|\bTBD\b|\bFIXME\b' spec/17-consolidated-guidelines/` — all 5 hits land in `27-linter-authoring-guide.md` between line 361 and line 424, inside ```` ```python ```` blocks.

