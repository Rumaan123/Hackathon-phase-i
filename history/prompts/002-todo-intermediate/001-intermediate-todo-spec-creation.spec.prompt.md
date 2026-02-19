---
id: 001
title: Intermediate Todo Spec Creation
stage: spec
date: 2026-02-15
surface: agent
model: claude-opus-4-6
feature: 002-todo-intermediate
branch: 002-todo-intermediate
user: architect
command: /sp.specify
labels: ["spec", "intermediate", "priorities", "tags", "search", "filter", "sort"]
links:
  spec: specs/002-todo-intermediate/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-todo-intermediate/spec.md
  - specs/002-todo-intermediate/checklists/requirements.md
tests:
  - none
---

## Prompt

Intermediate Level for The Evolution of Todo App

Project: The Evolution of Todo – Intermediate Level (builds on Basic Level)
Objective: Extend the console todo app with organization and usability features. Keep in-memory storage, console interface. Follow project constitution: modular code, type hints, docstrings, error handling, Python 3.13+, UV env, stdlib only.

Target Features (add these on top of Basic 5 features):
1. Priorities: Assign high/medium/low to each task.
2. Tags/Categories: Assign multiple tags (e.g., work, home, personal) to tasks.
3. Search: Search tasks by keyword in title, description, tags.
4. Filter: Filter tasks by status (completed/incomplete), priority, tag.
5. Sort: Sort tasks by priority (high first), alphabetically by title, or by creation date (if added).

Success Criteria:
- All Basic features still work perfectly.
- New features integrate seamlessly (e.g., add task with priority/tag, view shows them).
- Search returns matching tasks (case-insensitive).
- Filter shows only matching (e.g., only high priority).
- Sort reorders list correctly.
- Robust input: Invalid priority/tag show error, no crashes.
- Display improved: View list shows priority and tags (e.g., ID | Title | Desc | Priority | Tags | Status).
- Extensibility: Task model updated with priority (enum or str), tags (list of str).

Constraints:
- Storage: In-memory only (extend existing storage class).
- Interface: Enhanced console (better formatting, perhaps table-like view).
- No external libs (stdlib only).
- Priorities: Use enum or simple strings "high", "medium", "low".
- Tags: List of strings, comma-separated input.
- Search/Filter/Sort: Efficient (list comprehension or sorted()).

Not Building:
- Due dates, recurrence, reminders (save for Advanced).
- Persistence, web UI, colors (keep simple).
- Complex tag management (no tag creation UI, just add on task).

## Response snapshot

Generated comprehensive specification for the Intermediate Level todo features. Created `specs/002-todo-intermediate/spec.md` with 6 user stories (P1-P3), 19 functional requirements, 6 edge cases, 8 success criteria, and a quality checklist. Branch `002-todo-intermediate` created and checked out. All checklist items pass validation — no clarification markers needed.

## Outcome

- ✅ Impact: Feature spec created covering priorities, tags, search, filter, sort with full acceptance scenarios
- 🧪 Tests: No tests yet (spec phase); acceptance scenarios define test criteria for implementation
- 📁 Files: 2 files created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: /sp.clarify or /sp.plan to proceed to architecture planning
- 🧠 Reflection: User provided detailed requirements making spec generation straightforward with no ambiguity

## Evaluation notes (flywheel)

- Failure modes observed: create-new-feature.ps1 had a parameter binding error but branch and spec dir were created successfully
- Graders run and results (PASS/FAIL): Quality checklist PASS (all items checked)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
