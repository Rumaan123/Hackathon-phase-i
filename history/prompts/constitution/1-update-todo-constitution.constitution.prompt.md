---
id: 1
title: Update Todo Constitution
stage: constitution
date: 2026-02-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, todo-app, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
The Evolution of Todo - Project Constitution

This is the non-negotiable rulebook for all AI agents (Claude Code, Qwen CLI, Spec-Kit Plus, etc.) working on this project. Every spec, plan, task, and code generation MUST follow these rules first.

Project Core:
- Todo app evolves through three distinct feature levels: Basic, Intermediate, Advanced.
- All development is 100% agentic and spec-driven. No manual coding or direct edits allowed ever.
- Use Spec-Kit Plus commands (/sp.specify, /sp.plan, /sp.tasks, /sp.implement) only.
- Tech stack: Python 3.13+, UV for virtual env and deps, standard library priority.
- Design everything for extensibility: separate models, storage logic, CLI handling.
- In-memory storage by default; persistence only when level actually needs it.

Core Principles (apply to ALL levels):
- Follow clean Python code: PEP 8 style, type hints, docstrings on every function/class, strong error handling, input validation to avoid crashes.
- No global variables for task data – use classes or module-level instances.
- Traceability required: Keep all specs in history folder (versioned), log all prompts/iterations in CLAUDE.md, update README with level demos and setup.
- Build levels one by one: Finish and test previous level fully before starting next.

Basic Level (Core Essentials - MVP foundation):
Features (only these allowed in this level):
1. Add a new task with title and description.
2. Delete a task by its unique ID.
3. Update an existing task (change title and/or description).
4. View/list all tasks showing ID, title, description, and status ([ ] or [x]).
5. Mark task as complete or incomplete (toggle status).
Storage: Strictly in-memory only (use list or dict, no files or database).
Interface: Simple command-line console (text menu or basic commands).
Constraints: Use only Python standard library – no external packages at all.
Project structure must be:
- src/
  - main.py (CLI entry point and loop)
  - models.py (Task class with id, title, desc, completed bool)
  - storage.py (In-memory storage class or functions)
  - cli.py (user input handling and display)
Success for this level: Working console app that demos all 5 features perfectly.

Intermediate Level (Organization & Usability - builds directly on Basic):
Features (add these on top of Basic):
1. Assign priority to tasks (high, medium, low).
2. Add tags or categories (e.g. work, home, personal).
3. Search tasks by keyword (in title, description, tags).
4. Filter tasks by status, priority, tag, or date (if date added).
5. Sort tasks by priority, due date (if added), or alphabetically.
Storage: Still in-memory, but keep design extensible for future.
Interface: Improved console (better menus, formatted tables, more commands).
Constraints: Allow very minimal external libs only if truly needed (e.g. datetime for sorting).
Success for this level: All Basic features + all Intermediate features work smoothly together.

Advanced Level (Intelligent Features - builds on Intermediate):
Features (add these on top of previous levels):
1. Support recurring tasks (e.g. daily, weekly – auto reschedule when completed).
2. Set due dates and times with reminders (console alerts when due).
3. Browser notifications (if app starts evolving to web or hybrid).
Storage: Allow simple file/JSON persistence if needed for recurrence and reminders.
Interface: Enhanced console, with hints toward future web if applicable.
Constraints: Use justified external libs (datetime, json, maybe others for notifications).
Success for this level: Recurring logic works correctly, reminders trigger properly.

Workflow Rules:
- Always reference this constitution first in every agent prompt.
- Create separate spec files for each level (e.g. spec_basic.md, spec_intermediate.md).
- Document everything: Specs history folder, CLAUDE.md with used prompts and iterations.
- Test each level fully before moving to next.
- README.md must explain setup (uv sync, how to run) and show demos for current level.
```

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) with all the principles and requirements specified in the user input. The constitution now includes:

1. Core Principles covering the three-level evolution approach, agentic development, tech stack standards, extensible architecture, storage progression, and clean Python code standards
2. Additional constraints including no global variables policy, traceability requirements, and sequential level completion
3. Development workflow sections for Basic, Intermediate, and Advanced levels
4. Governance section outlining constitutional authority

The constitution serves as the non-negotiable rulebook for all AI agents working on this todo app project.

## Outcome

- ✅ Impact: Created comprehensive constitution for todo app project following three-level evolution approach
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with new constitution content
- 🔁 Next prompts: Ready to create specs for Basic level using /sp.specify
- 🧠 Reflection: Constitution establishes clear governance framework for progressive todo app development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Basic level spec development