---
content_axis: audit-corpus
axis_rationale: "Cross-spec audit findings, post-mortems, and historical drift analyses — describes other specs, does not specify object behaviour"
kind: tracker
---

# Audits

**Version:** 1.2.1
**Updated:** 2026-05-06 (Phase 154 Task #6 — `03-rebaselines/00-overview.md` v1.0.0 added as second substantive delegated child indexing 4 frozen baseline subdirs + live auditor output per Lesson #36. `02-post-mortems/` SKIPPED in same phase per Lesson #41 binding-mechanism survey precondition — 0 genuine drift post-mortems surveyed (24 phase-closing memos and 1 retrospective audit are not post-mortem-class material). Phase 154 Task #5 — `01-findings/00-overview.md` v1.0.0 added as substantive delegated child indexing 80 module-named audit memos by target spec module per Lesson #36. Phase 154 Task #4 — initial scaffold under No-Questions Mode Prompt 04; module created as planned home for cross-spec audit findings, drift post-mortems, and historical scorecard rebaselines previously scattered across `.lovable/memory/audit/`. Classified `kind: tracker` per Lesson #29.)


**Status:** Active (scaffold)  
**AI Confidence:** Production-Ready  
**Ambiguity:** Low

---

## Overview

`spec/29-audits/` is the canonical home for **cross-spec audit corpora** — finding registries, post-mortems, drift analyses, and historical scorecard rebaselines. It is **not** an object spec for any deliverable; every document under this module is a tracker that *describes* other specs (or archived specs under `spec/_archive/`).

This module exists to give such corpora a stable, indexable home so that:

1. **Audit findings** stop accumulating ad-hoc under `.lovable/memory/audit/` (which is contributor-private memory, not contributor-public spec surface).
2. **Module-kind misclassification** by AI auditors (Lesson #29 class) has a single forward-looking guard rather than per-module band-aids.
3. **Drift post-mortems** referenced from §98 changelogs across the tree have a citable URL.

---

## Module Kind Declaration (Normative)

This module is classified `kind: tracker` (audit-corpus). All future child files MUST inherit this classification unless they carry an explicit `kind:` override in their own front-matter.

**Implications** (per Lesson #29 / spec/25 AC-AI-09/10/11):

- Verbatim algorithm names, AC-IDs, file paths, and configuration values appearing in finding bodies are **auditor-quoted evidence**, not normative contract for spec/29.
- AI-implementability auditors MUST treat this module as `kind: tracker` and apply the spec/25 AC-AI-09/10/11 disambiguation pattern.
- Inventory tables citing "missing files" inside finding bodies refer to the **audited spec** (or its archive), not to spec/29's own file inventory.

---

## Keywords

`audit` · `tracker` · `post-mortem` · `drift` · `corpus` · `cross-spec`

---

## Scoring

| Metric | Value |
|--------|-------|
| AI Confidence | High |
| Ambiguity | Low |
| Module Kind | tracker (audit-corpus) |

---

## Document Inventory

| File | Purpose |
|------|---------|
| `00-overview.md` | This file — module index + kind declaration |
| `01-findings/00-overview.md` | Cross-spec audit findings index (delegates to `.lovable/memory/audit/` per Lesson #36) |
| `03-rebaselines/00-overview.md` | Historical scorecard rebaseline snapshots index (4 frozen `v2*/` subdirs + live auditor output) |
| `97-acceptance-criteria.md` | Module-kind contract ACs (AC-29-01..03) |
| `98-changelog.md` | Module changelog |
| `99-consistency-report.md` | Module health + audit |

**Planned children (Phase 155+):**

| Slot | Purpose |
|------|---------|
| `02-post-mortems/` | Drift post-mortems (SKIPPED Phase 154 Task #6 — 0 genuine post-mortems surveyed per Lesson #41; create on first genuine drift incident) |



---

## Cross-References

- **Lesson #29** (mem://process/phase-153-lessons §F): Audit-Corpus Modules — pattern that drove this scaffold.
- **spec/25-app-issues** AC-AI-09/10/11: precedent for module-kind pin in §97.
- **spec/_archive/21-git-logs-v1/**: archived spec referenced by spec/25 audit findings.
- `.lovable/memory/audit/`: contributor-private memo home; eventual graduation source for `01-findings/`.

---

## Status

**Scaffold-only.** Children under `01-findings/` / `02-post-mortems/` / `03-rebaselines/` have not yet been migrated. This phase ships the module shell + module-kind contract; migration is deferred to a future phase.
