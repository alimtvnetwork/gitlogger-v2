---
id: 02
title: No-Questions Mode (40-task budget, second activation)
status: active
activated: 2026-05-05
budget: 40
counter: 0
tags: [no question, not ques for 40]
---

# Prompt 02 — No-Questions Mode (re-activation)

## Activation

Re-activated 2026-05-05 by user directive ("No-Questions Mode — AI Implementation Spec"). Spans the **next 40 tasks** counted from this activation. Prompt 01 (2026-04-28 → 2026-04-30, 59/40 actual) is the precedent.

## Rules

1. **Do not ask the user any questions** for the next 40 tasks. Suppress `questions--ask_questions` calls; suppress inline confirmation prompts; do NOT write "Confirm?", "Should I?", "Pick A or B?".
2. **Log all ambiguity** to `.lovable/question-and-ambiguity/<NN>-<brief-title>.md` (sequential, continuing from the existing series — next free index = 05). Use the entry contract below.
3. **Infer the best interpretation** per the Inference Guidelines and continue working without interruption.
4. **Maintain a task counter** at `.lovable/question-and-ambiguity/task-counter.md` (NEW section "## Prompt 02 counter"). Increment by 1 per completed user-facing task (one user message → one unit of work). Setup/admin sub-steps inside a single task do NOT each count separately. At 40, mark this prompt `completed` and resume normal Q&A.

## Ambiguity log entry contract

Each `.lovable/question-and-ambiguity/<NN>-*.md` MUST include:

- **Task context** — feature/spec the ambiguity relates to
- **Specific question** — exact point of uncertainty
- **Inferred decision** — assumption made to proceed
- **Impact** — how the decision affects implementation
- **Suggested clarification** — what the user should confirm on review
- **Timestamp** — date the ambiguity arose

Keep each entry under 200 words. Markdown headers, no prose padding.

## Inference Guidelines

1. Choose the interpretation that aligns with the existing codebase style.
2. Prefer the simpler implementation over the complex one.
3. Default to the most common UX/spec-engineering pattern for the given context.
4. Document the inference in the ambiguity log so the user can override it later.
5. Do NOT block progress — complete the task with the inferred approach.

## Lesson carried from Prompt 01

Counter drift: hand-incrementing was unreliable across multi-sub-task phases (15 → 59 silently). Mitigation under Prompt 02: increment the counter on the SAME tool turn that closes the user-facing task; do not defer.
