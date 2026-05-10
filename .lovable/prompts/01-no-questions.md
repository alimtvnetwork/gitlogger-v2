---
id: 01
title: No-Questions Mode (40-task budget)
status: completed
activated: 2026-04-28
deactivated: 2026-04-30
budget: 40
counter: 59
tags: [no question, not ques for 40]
---

# Prompt 01 — No-Questions Mode

## Activation

Activated 2026-04-28 by user directive. Spans the **next 40 tasks**.
After 40 completed tasks, resume normal question-asking behavior.

## Rules

1. **Do not ask the user any questions** for the next 40 tasks.
   Suppress `questions--ask_questions` calls; suppress inline confirmation prompts.
2. **Log all ambiguity** to `.lovable/question-and-ambiguity/xx-brief-title.md`
   (sequential numbering 01, 02, 03…) instead of asking.
3. **Infer the best interpretation** and continue working without interruption.
4. **Maintain a task counter** at `.lovable/question-and-ambiguity/task-counter.md`.
   Increment by 1 per completed user-facing task. At 40, deactivate this prompt.

## Ambiguity log entry contract (each file)

- **Task context** — feature / spec section the ambiguity relates to
- **Specific question** — the exact point of uncertainty
- **Inferred decision** — what assumption was made to proceed
- **Impact** — how the decision affects the implementation
- **Suggested clarification** — what the user should confirm later
- Markdown, ≤200 words, timestamped

## Inference doctrine

1. Match existing codebase style (spec-only project, lockstep rule, H10 filter).
2. Prefer the simpler implementation over the complex one.
3. Default to the most common UX/spec pattern for the context.
4. When in doubt: defer per H10 filter (mechanical detectability + active regression
   surface + low false-positive risk) before adding new lints/conventions.

## Deactivation

When `counter` reaches 40 in `task-counter.md`:
- Set `status: completed` and `deactivated: <date>` in this frontmatter.
- Update `.lovable/prompts.md` index row.
- Resume normal `questions--ask_questions` usage.

## Cross-references

- Prompts index: `.lovable/prompts.md`
- Ambiguity folder: `.lovable/question-and-ambiguity/`
- Task counter: `.lovable/question-and-ambiguity/task-counter.md`
