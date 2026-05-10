---
kind: index
description: Top-level routing index for app issue analysis (parent of two child trackers). Exempt from missing-contract / untestable rubric findings — child trackers carry their own kind:tracker exemption.
content_axis: audit-corpus
axis_rationale: "Routing parent of kind:tracker post-mortems (Lesson #29)"
produced_for:
  # Producer-side inverse-binding (A-29, Sess-49) — mirror of §26→§22 `produced_for:` (A-27, Sess-47)
  # and §28 producer-side (A-29 same-session twin). §25 OWNS post-mortems whose findings drive
  # §22 evolution; rows below bind each tracker child to the §22 AC whose closure it backs.
  # Resolved by gate #10 dual-key contract (§27 A-28, Sess-48). Lesson #29 tracker exemption
  # preserved (kind:tracker children remain exempt from missing-contract findings).
  - file: 02-consolidated-audit-findings/00-overview.md
    fulfills: spec/22-git-logs-v2 §97 AC-78 "Module asset inventory pin (37-entry inventory + DDL/REST/PHP fixtures)" — 24 line-anchored findings drive §22 inventory closure
  - file: 02-consolidated-audit-findings/00-overview.md
    fulfills: spec/22-git-logs-v2 §97 AC-79 "Cross-Module Externalized Citation Map (Lesson #36/#37 link-don't-restate anchor table)" — findings cite §22 file:line, never restated
  - file: 01-phase-2-git-logs-audit/00-overview.md
    fulfills: spec/22-git-logs-v2 §97 AC-22-CE1 "Co-edit cohorts: schema/endpoint/CLI changes MUST move sibling files in the same commit" — superseded first-pass tracker preserved for traceability of cohort drift class
---

# App Issues

**Version:** 3.7.0  
<!-- h10-verified-phase: 153 -->
**Updated:** 2026-05-10 (Session 49 audit-task A-29 — added `produced_for:` producer-side front-matter binding child trackers (02-consolidated, 01-phase-2) to §22 AC-78/AC-79/AC-22-CE1. Mirrors §26→§22 producer-side (A-27 Sess-47) and §28 producer-side (A-29 same-session twin). Resolved by §27 gate #10 dual-key contract (A-28 Sess-48). Lesson #29 tracker exemption preserved. Prior: Phase 153 Task S25-02.)
**AI Confidence:** Production-Ready  
**Ambiguity:** None

---

## Overview

App-specific issue analysis, root cause analysis, bug documentation, and solution guidance at the root spec level. This folder tracks problems encountered during application development, their diagnosis, and their resolution.

---

## Placement Rule

Any content that analyzes bugs, failures, root causes, or fixes for application-level work belongs here. General coding principle violations or cross-cutting concerns belong in the core fundamentals range (`01–20`).

---

## Contents

| # | Folder | Status | Description |
|---|--------|--------|-------------|
| 01 | [01-phase-2-git-logs-audit/](./01-phase-2-git-logs-audit/00-overview.md) | **superseded** by 02 (preserved for traceability) | Phase-2 spec-only audit of `spec/_archive/21-git-logs-v1/` — first pass; contained false-positives later corrected by the consolidated tracker. |
| 02 | [02-consolidated-audit-findings/](./02-consolidated-audit-findings/00-overview.md) | **active** (start here) | Single source of truth — 24 numbered findings with file paths + verbatim evidence snippets. Re-scored every Phase-2 item against line-anchored evidence. |

> **Reading order (Phase P11):** Start at `02-consolidated-audit-findings/` for the current state. `01-phase-2-git-logs-audit/` is preserved for traceability only — it predates the line-anchored evidence pass and reports two files as "missing" that actually exist. The supersession is symmetric: declared in 02's "Correction notice", in 01's banner, and in this routing table.

---

## AI Implementer Quickstart

**This folder is `kind: index` — a routing parent over `kind: tracker` post-mortems. You do not "implement" findings here; you read them to avoid repeating the bug.**

1. **Start here:** [`02-consolidated-audit-findings/`](./02-consolidated-audit-findings/00-overview.md) — single source of truth (24 numbered findings, line-anchored evidence).
2. **Skip:** `01-phase-2-git-logs-audit/` — superseded; preserved only for traceability.
3. **Before changing §22 (git-logs-v2):** grep this folder for the file path you're touching; if a finding cites it, read the resolution before editing.
4. **New finding?** Add it to `02-consolidated-audit-findings/` with verbatim evidence snippet + file:line anchor; never inline post-mortems into the source spec.

**Hard rules:** trackers are exempt from missing-contract / untestable rubric findings (Lesson #29) · never restate findings — link via AC-AI-17 · evidence MUST be line-anchored, not paraphrased.

---

## Cross-References

| Reference | Location |
|-----------|----------|
| App Specs (legacy v1 git-logs) | [../_archive/21-git-logs-v1/00-overview.md](../_archive/21-git-logs-v1/00-overview.md) |
| Spec Authoring Guide | [../01-spec-authoring-guide/00-overview.md](../01-spec-authoring-guide/00-overview.md) |

---

## Process Terminology

This module's prose (§97 / §98 / §99 + child trackers) routinely cites contributor-process artifacts that live OUTSIDE `spec/` by design (per Lesson #36 — link-don't-restate). Use this glossary as the one-hop disambiguation pointer:

| Term | Form | Authority (single source of truth) |
|------|------|------------------------------------|
| **Phase NN** | Phase ordinal (e.g. `Phase 152`, `Phase 153`) | `mem://index.md` Core narrative + per-phase closing memo `.lovable/memory/audit/v2-deterministic/phase-NNN-*.md` |
| **Lesson #NN** | Numbered contributor rule (e.g. `Lesson #29`, `Lesson #36`, `Lesson #50`) | `mem://process/phase-153-lessons` (consolidated catalogue, sections A–G) |
| **Task XNN / X-NN-fu / SNN-NN** | Per-task tracker ID inside a phase (e.g. `A11c`, `A24-fu12`, `S22-01`, `S26-fu`) | `.lovable/memory/audit/v2-deterministic/phase-NNN-task-XNN-*.md` (one closing memo per task) |
| **AC-NN** / **AC-XX-NN** | Numbered acceptance criterion in a §97 file | The owning module's `97-acceptance-criteria.md` (look up by ID prefix; e.g. `AC-AI-*` = `spec/25-app-issues/97-acceptance-criteria.md`, `AC-CG-*` = `spec/02-coding-guidelines/97-acceptance-criteria.md`) |

These references are intentional bidirectional links between spec content and contributor memory — they are NOT spec-internal terminology. AC-AI-17 codifies this disambiguation contract and pins the `[D1] Ambiguous 'Phase 153' references` audit finding class as link-don't-restate compliance.

---

## Verification

_Auto-generated section — see `spec/25-app-issues/97-acceptance-criteria.md` for the full criteria index._

### AC-AI-000: App issues triage conformance: Overview

**Given** Audit issue write-ups for the required Reproduction / Cause / Fix / Prevention sections.  
**When** Run the verification command shown below.  
**Then** Every issue file contains all four sections and references at least one commit or PR.

**Verification command:**

```bash
python3 linter-scripts/check-spec-cross-links.py --root spec --repo-root .
```

**Expected:** exit 0. Any non-zero exit is a hard fail and blocks merge.

_Verification section last updated: 2026-04-21_

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Status:** Forward-looking spec — drift expected.

AC-AI-000 issue-file format is forward-looking; concrete issue files will be authored as work progresses.

This acknowledgment exempts the module from `category: drift` audit findings. See `.lovable/memory/index.md` Phase 27c note.

### Out-of-Scope Material — Routing Pin (Normative)

The CI workflow YAML (Phase-74 5-stage pipeline) and the `IndexEntryStatus`
TypeScript enum / `IndexEntry` interface (Phase-80) previously inlined here
are **out of scope for §25**. §25 owns only the issue-lifecycle and audit
catalog. Canonical owners:

| Removed material                                  | Canonical owner | Rationale                                    |
|---------------------------------------------------|-----------------|----------------------------------------------|
| `spec-gate-stage-{1..5}` CI workflow YAML         | **§28** (universal CI/CLI) | All cross-module pipeline stages live in §28. |
| Per-module gate-runner invocation patterns        | **§27** (spec-toolchain)   | §27 owns linter-script contracts.            |
| `IndexEntryStatus` enum + `IndexEntry` interface  | **§27** (spec-toolchain)   | Index/registry types are toolchain artifacts.|

**No CI YAML and no enum/interface DDL was materialised elsewhere in this
turn** — the routing pin reserves the contract; materialisation is tracked
as a separate follow-up task. AI walkers reading §25 in isolation MUST NOT
re-inline these blocks; consult §27 / §28 for the authoritative form.

See [`lifecycle-25-app-issues-lifecycle.mmd`](./lifecycle-25-app-issues-lifecycle.mmd) for the visual lifecycle.
