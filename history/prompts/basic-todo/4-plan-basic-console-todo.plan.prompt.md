---
id: 4
title: Plan Basic Console Todo App
stage: plan
date: 2026-02-10
surface: agent
model: claude-sonnet-4-5
feature: basic-todo
branch: basic-todo
user:
command: /sp.plan
labels: [plan, basic-todo]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/basic-todo/plan_basic_console.md
tests:
 - Manual testing of CLI workflow
 - Edge case validation
 - Performance testing with multiple tasks
---

## Prompt

Basic Level Console Todo App for The Evolution of Todo

Reference: Use the previously generated /sp.specify output (spec_basic.md or similar) as the main source of truth. Strictly follow project constitution: agentic workflow, no manual coding, clean modular Python code, in-memory only, Python 3.13+, UV env, stdlib only.

Core Objective for this Plan:
Create a detailed technical implementation plan for the Basic Level MVP: a simple command-line todo application that supports exactly the 5 core features using a text-based console interface (while True loop with input() and print()).

Architecture Sketch (include a text-based diagram in the plan output):
- Components:
  - Task Model (models.py): Dataclass or simple class for Task (id: int, title: str, description: str, completed: bool)
  - InMemoryStorage (storage.py): Class or functions to manage a list/dict of tasks (add, get_by_id, update, delete, list_all, toggle_complete)
  - CLI Handler (cli.py): Functions for user input parsing, command execution, display formatting
  - Main Entry (main.py): While loop for menu/commands, calls CLI and storage
- Text Diagram Example:
  User (console input)
          |
      main.py (CLI loop)
          |
    ├── cli.py (parse commands: add/view/etc.)
    ├── storage.py (CRUD on in-memory data)
    └── models.py (Task class)

Decisions Needing Documentation (list important choices with options and tradeoffs):
1. Storage Structure:
   - Option: List of Task objects
     - Pros: Simple, easy iteration for list/view
     - Cons: Slower lookup by ID (O(n))
   - Option: Dict with ID as key
     - Pros: Fast lookup/delete/update (O(1))
     - Cons: Slightly more code for listing
   - Chosen: Dict[int, Task] – better performance for delete/update by ID
2. ID Generation:
   - Incremental int (start from 1, auto-increment)
     - Pros: Short, easy to type/remember
     - Cons: Potential conflicts if scaled (but fine for basic)
   - UUID
     - Pros: Unique forever
     - Cons: Long strings, harder in console
   - Chosen: Incremental int – user-friendly for CLI
3. Command Interface:
   - Option: Simple text commands (e.g., "add Title: desc")
     - Pros: Minimal, quick
   - Option: Numbered menu (1. Add, 2. View...)
     - Pros: Beginner-friendly, less typing errors
   - Chosen: Hybrid – numbered menu + direct commands for speed
4. Input Parsing:
   - Manual string split/parsing
     - Pros: No deps
     - Cons: Error-prone
   - Chosen: Manual + basic validation – keep stdlib only

Research Approach:
- Research-concurrent: Reference Python best practices (dataclasses, typing, PEP 8) as needed during implementation steps. No heavy upfront research.

Quality Validation & Testing Strategy:
- Validation Checks based on Acceptance Criteria:
  - Add: New task appears in list with correct status [ ]
  - View: All tasks formatted clearly (ID | Title | Desc | Status)
  - Update/Delete/Mark: Changes reflect immediately, invalid ID shows error message
  - No crashes on bad input (e.g., non-int ID, empty title)
- Testing Steps:
  1. Run app: uv run src/main.py
  2. Manual flow: Add 3 tasks → View → Update one → Mark complete → Delete one → View again
  3. Edge cases: Invalid commands, duplicate titles (allowed), empty desc, quit command
  4. README demo: Include sample session transcript for judges
- No unit tests in basic (focus functional demo), but plan can suggest optional if time

Technical Details:
- Use research-concurrent approach: Pull Python stdlib examples (input validation, string formatting) during Claude Code steps
- Follow constitution: PEP 8, type hints (from typing), docstrings, error handling (try/except + user messages)
- Organize plan by phases: Architecture → Decisions → Tasks Breakdown → Testing → Risks

## Outcome

- ✅ Impact: Comprehensive implementation plan created for Basic Level Console Todo App
- 🧪 Tests: Manual testing strategy defined for all 5 core features and edge cases
- 📁 Files: plan_basic_console.md generated with detailed architecture and tasks
- 🔄 Next prompts: Ready for /sp.tasks to break plan into granular agent-executable tasks
- 🧠 Reflection: Plan aligns with constitution and specification, provides clear path for implementation