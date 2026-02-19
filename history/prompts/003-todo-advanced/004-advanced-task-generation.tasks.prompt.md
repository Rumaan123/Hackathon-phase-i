---
id: 004
title: Advanced Todo Task Generation
stage: tasks
date: 2026-02-16
surface: agent
model: claude-opus-4-6
feature: 003-todo-advanced
branch: 003-todo-advanced
user: user
command: /sp.tasks
labels: ["tasks", "advanced-features", "due-dates", "recurrence", "persistence"]
links:
  spec: specs/003-todo-advanced/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-todo-advanced/tasks.md
tests:
  - null
---

## Prompt

/sp.tasks

## Response snapshot

Generated 32 implementation tasks for Advanced Todo Features organized into 8 phases:

- Phase 1 (Setup): 5 tasks — RecurrenceInterval enum, parse_due_date, advance_due_date, get_alert_status, Task dataclass update
- Phase 2 (Foundational): 3 tasks — update add_task, update_task, toggle_complete in storage
- Phase 3 (US1 - Due Dates, P1 MVP): 5 tasks — CLI add/update/display + main.py prompts
- Phase 4 (US2 - Alerts, P1): 3 tasks — alert column, startup alerts, main.py wiring
- Phase 5 (US3 - Recurring, P2): 5 tasks — CLI add/update/mark + main.py prompts
- Phase 6 (US4 - Enhanced Display, P2): 2 tasks — recurrence column, column width adjustment
- Phase 7 (US5 - JSON Persistence, P3): 5 tasks — save/load storage + CLI + menu
- Phase 8 (Polish): 4 tasks — backward compatibility, regression, edge cases

Two parallel tracks identified: US1→US2→US3→US4 (sequential) and US5 (independent after Phase 2). MVP scope: 13 tasks (Phases 1-3).

## Outcome

- ✅ Impact: Complete task list ready for implementation via /sp.implement
- 🧪 Tests: No test tasks generated (not requested in spec)
- 📁 Files: 1 file created (tasks.md)
- 🔁 Next prompts: /sp.implement to execute all tasks, or manual execution phase by phase
- 🧠 Reflection: Tasks follow same incremental pattern as 002-todo-intermediate. All changes to existing files only.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Format validation PASS (all tasks have checkbox, ID, story label where applicable, file paths)
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
