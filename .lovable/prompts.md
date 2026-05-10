# Prompts Index

Standing user directives that govern AI behavior across multiple sessions.
Each row points to a prompt file under `.lovable/prompts/`.

| ID | Title | Status | Activated | Budget | Counter | Tags |
|----|-------|--------|-----------|--------|---------|------|
| 01 | [No-Questions Mode](./prompts/01-no-questions.md) | ✅ completed | 2026-04-28 | 40 tasks | 59/40 (deactivated 2026-04-30) | `no question`, `not ques for 40` |
| 02 | [No-Questions Mode (re-activation)](./prompts/02-no-questions.md) | ⏸ superseded | 2026-05-05 | 40 tasks | 32/40 (superseded by 04 on 2026-05-06) | `no question`, `not ques for 40` |
| 03 | [Write Memory](./prompts/03-write-memory.md) | 🟢 active | 2026-05-06 | n/a (workflow) | n/a | `write memory`, `end memory`, `update memory` |
| 04 | [No-Questions Mode (third activation)](./prompts/04-no-questions.md) | 🟢 active | 2026-05-06 | 40 tasks | 0/40 | `no question`, `not ques for 40` |

## Status legend

- 🟢 active — currently in force
- ⏸ paused — temporarily suspended
- ✅ completed — budget exhausted or user-deactivated
- 🗄 archived — historical reference only

## Conventions

- Sequential numbering: `01-`, `02-`, `03-`…
- Filename: `<id>-<kebab-brief-title>.md`
- Each prompt file MUST carry frontmatter (`id`, `title`, `status`, `activated`).
- Index row tags MUST mirror the prompt's frontmatter `tags:` list.
- Update Counter column whenever the task counter advances.
