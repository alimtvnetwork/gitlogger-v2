---
id: 04
title: No-Questions Mode (40-task budget, third activation)
status: active
activated: 2026-05-06
budget: 40
counter: 0
tags: [no question, not ques for 40]
---

# Prompt 04 — No-Questions Mode (third activation)

## Activation

Re-activated 2026-05-06 by user directive ("No-Questions Mode — AI Implementation Spec"). Spans the **next 40 tasks** counted from this activation, resetting the counter regardless of where Prompt 02 left off (32/40 at handover). Prompts 01 (2026-04-28 → 2026-04-30, 59/40 actual) and 02 (2026-05-05 → 2026-05-06, 32/40 at supersede) are precedents.

## Rules (verbatim from user prompt 2026-05-06)

1. **No questions to the user** for the next 40 tasks.
2. **Log all ambiguity** to `.lovable/question-and-ambiguity/xx-brief-title.md` (sequential `xx`).
3. Each ambiguity note MUST include:
   - Task context — what feature or spec the ambiguity relates to.
   - Specific question — the exact point of uncertainty.
   - Inferred decision — what assumption was made to proceed.
   - Impact — how the decision affects the implementation.
   - Suggested clarification — what the user should confirm later.
4. **Format**: markdown, ≤200 words per note, timestamp included.
5. **Inference guidelines**:
   - Align with existing codebase / spec style.
   - Prefer simpler implementation.
   - Default to the most common UX/spec pattern for the context.
6. **Forward momentum**: never block on ambiguity — log + proceed with best inference.
7. **Counter** in `.lovable/question-and-ambiguity/task-counter.md`. Increment on each completed task. Resume question-asking at 40/40.

## Scope clarification (inferred from session memory)

- "Task" = one user-issued work request (one `next` invocation, one named task, or one explicit ask). Sub-steps inside a single task do NOT increment the counter.
- "Question" excludes scorecard rendering (Core memory MANDATORY rule still applies — Lesson #40).
- "Question" excludes the closing one-line task-list summary at end of each response (Core memory rule).
- "Question" excludes mechanical version-bump confirmations within a phase — those are deterministic.

## Handover from Prompt 02

- Prompt 02 status updated to ⏸ superseded (was 32/40 active).
- Prompt 04 counter starts at 0/40.
- Ambiguity-log filename sequence continues from Prompt 02's last (next sequential `xx`).

## Deactivation

Auto-deactivates when counter hits 40/40, or earlier on explicit user override (e.g. "stop no-questions mode", "ask me", "questions back on").
