---
id: 2
title: Basic Todo Spec Creation
stage: spec
date: 2026-02-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: basic-todo
branch: master
user: user
command: /sp.specify
labels: [todo-app, basic, spec, hackathon]
links:
  spec: specs/basic-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/basic-todo/spec.md
  - specs/basic-todo/checklists/requirements.md
tests:
  - none
---

## Prompt

```text
Basic Level Specification Prompt for /sp.specify

/sp.specify Basic Level for The Evolution of Todo App

Project: The Evolution of Todo – Phase I / Basic Level MVP
Objective: Build a minimal, in-memory, command-line todo application using only the 5 core features. Strictly follow the project constitution rules. Use agentic/spec-driven workflow with Spec-Kit Plus and Claude Code. No manual coding allowed.

Target Audience / Use Case:
- Hackathon judges evaluating clean agentic development process
- Developers who want a simple, extensible todo CLI foundation

Focus:
- Perfect implementation of exactly 5 basic features
- In-memory storage only (data lost on app exit)
- Robust console interface with clear user feedback
- Modular, clean, Pythonic code structure as per constitution

Success Criteria:
- App starts and shows a menu or accepts commands (add, view, update, delete, mark, quit)
- All 5 features work correctly in one runtime session
- No crashes on invalid input (graceful error messages)
- Tasks displayed clearly with ID, title, description (shortened if long), and status [ ] / [x]
- Code is modular: separate Task model, in-memory storage logic, CLI handling
- README.md updated with how to run + example commands demo
- All development traceable via specs history and CLAUDE.md

Required Features (exactly these – nothing more, nothing less):
1. Add Task
   - User enters title and description
   - Auto-assign unique ID (incremental integer or UUID)
   - Add to in-memory list/dict
2. Delete Task
   - User provides ID
   - Remove task if found, show confirmation/error
3. Update Task
   - User provides ID + new title and/or description
   - Update only provided fields, keep others unchanged
4. View Task List
   - Show all tasks numbered or with IDs
   - Format: ID | Title | Description | Status
   - Status shown as [ ] incomplete or [x] complete
5. Mark as Complete / Incomplete
   - User provides ID
   - Toggle completed boolean
   - Show updated status

Constraints:
- Storage: In-memory only – use list of Task objects or dict with ID as key
- No external libraries – Python standard library only
- Python version: 3.13+
- Environment: UV managed virtual env
- Interface: Simple print() and input() based console loop
- IDs: Must be unique and easy to type (prefer int starting from 1)
- Input validation: Handle non-numeric IDs, missing fields, out-of-range IDs
- Extensibility: Task class should allow easy addition of fields later (priority, due_date, etc.)

Not Building / Out of Scope for this spec:
- Saving or loading tasks from file/database
- Priorities, tags, categories, search, filter, sort
- Due dates, recurrence, reminders
- Colors in console, rich formatting libraries
- Unit tests (unless added in later plan)
- Multi-user or authentication
- Web or GUI interface

Output Format:
- Generate a detailed Markdown specification file named spec_basic.md
- Include sections:
  - Overview and Goals
  - User Stories / Acceptance Criteria (one per feature)
  - Data Model (Task class fields and types)
  - CLI Flow / Command Examples
  - Edge Cases and Error Handling
  - Alignment with Project Constitution
  - Next Steps (plan generation)
```

## Response snapshot

Created the basic todo application specification (specs/basic-todo/spec.md) following all required sections. The specification includes:

1. Overview and Goals - Defining the MVP purpose
2. User Stories and Acceptance Criteria - Five detailed user stories covering each required feature
3. Data Model - Task class with id, title, description, and completed fields
4. CLI Flow - Example command flow showing user interaction
5. Edge Cases and Error Handling - Covering various error scenarios
6. Alignment with Project Constitution - Ensuring compliance with project rules
7. Next Steps - Planning for implementation

Also created a quality checklist to validate the specification completeness.

## Outcome

- ✅ Impact: Successfully created comprehensive specification for basic todo app following project constitution
- 🧪 Tests: none
- 📁 Files: Created specs/basic-todo/spec.md and specs/basic-todo/checklists/requirements.md
- 🔁 Next prompts: Ready to generate implementation plan with /sp.plan
- 🧠 Reflection: Specification clearly defines scope and requirements for MVP development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with /sp.plan to create implementation plan