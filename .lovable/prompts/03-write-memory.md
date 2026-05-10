---
id: "03"
title: Write Memory
status: active
activated: 2026-05-06
tags: ["write memory", "end memory"]
---

# Write Memory

> **Purpose:** After completing work or at the end of a session, the AI must persist everything it learned, did, and left undone — so the next AI session can pick up seamlessly with zero context loss.
>
> **When to run:** At the end of every session, after completing a task batch, or when explicitly asked to "update memory" or "write memory" or "end memory".

---

## Trigger phrases

`write memory` · `end memory` · `update memory`

## Project-specific application (spec-only repo)

This project is **spec-only** with a sophisticated, already-canonical memory layout. The generic template below is adapted as follows:

| Generic template path | This project's actual canonical path | Notes |
|---|---|---|
| `.lovable/memory/index.md` | `.lovable/memory/index.md` (mem://index.md) | ✅ exists, always-in-context |
| `.lovable/plan.md` | Index Memories list + `task-counter.md` "Last task" trail | spec-driven roadmap lives in §99 audit rows + §98 changelogs |
| `.lovable/suggestions.md` | `.lovable/question-and-ambiguity/*.md` | per-question files + README index |
| `.lovable/pending-issues/` | spec-module §99 consistency reports + `kind: tracker` modules | issues are spec-internal, not session bugs |
| `.lovable/solved-issues/` | `.lovable/memory/audit/v2-deterministic/phase-NN-*.md` memos | one memo per closed phase |
| `.lovable/strictly-avoid.md` | `.lovable/memory/constraints/forbidden-trace-map-ideas.md` + Core "never" rules in index.md | constraints are slot-locked |
| `.lovable/cicd-issues/` | `.github/workflows/spec-health.yml` strict gates + Phase memos | CI issues = gate failures, tracked per-phase |

**DO NOT** create `.lovable/plan.md`, `.lovable/suggestions.md`, `.lovable/pending-issues/`, `.lovable/solved-issues/`, `.lovable/cicd-issues/`, or `.lovable/cicd-index.md` in this repo — they would fragment the canonical single-source-of-truth structure (violates Lesson #36 + Core memory rule "one memory folder").

**DO** at end of session:
1. Append/update Index Memories list in `.lovable/memory/index.md` with phase outcome (1-paragraph summary, mention key Lessons codified, banner versions, gate state).
2. Create one phase memo at `.lovable/memory/audit/v2-deterministic/phase-NN-<slug>.md` capturing Why/Change/Verification/Effect.
3. Update `.lovable/question-and-ambiguity/task-counter.md` "Counter" + "Last task" + "Outcome" lines.
4. If a new standing user directive emerged, add a prompt file under `.lovable/prompts/NN-<slug>.md` and index row in `.lovable/prompts.md`.
5. List remaining tasks at end of every reply (per Core rule).

## Anti-corruption rules (apply always)

1. Never delete history — preserve §98 changelog rows, §99 audit rows, prior memo files.
2. Never overwrite `mem://index.md` blindly — `code--write` REPLACES; include ALL existing content.
3. Never create `.lovable/memories/` (with trailing s) — the canonical path is `.lovable/memory/`.
4. Never split single-source-of-truth files (Lesson #36).
5. Never re-baseline audit caches without re-probing the gateway (Lessons #34, #86, #89).
6. All new md files: lowercase + hyphen-separated (per project naming convention).

## File-naming rules

- Phase memos: `phase-NN-<slug>.md` (lowercase, hyphenated)
- Prompt files: `NN-<slug>.md` (zero-padded, lowercase, hyphenated, frontmatter required)
- Question-and-ambiguity files: `NN-<slug>.md`

## Final confirmation format

```
✅ Memory update complete.
- Phase: <NN> · <slug>
- Memo: .lovable/memory/audit/v2-deterministic/phase-NN-<slug>.md
- Index updated: yes/no
- Counter: X/40
- Gates: lockstep · tree-health · version-parity · freshness · folder-refs (all GREEN/list reds)
- Remaining tasks: [bullet list]
- Next on `next`: <action>
```
