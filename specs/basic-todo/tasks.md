---
description: "Task list for Basic Level Console Todo App implementation"
---

# Tasks: Basic Level Console Todo App

**Input**: Design documents from `/specs/basic-todo/`
**Prerequisites**: plan_basic_console.md (required), spec.md (required for user stories)

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are generated based on the implementation plan and specification.

  Tasks are organized by user story to enable independent implementation and testing of each story.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python project with UV environment
- [X] T003 [P] Create src/ directory structure (models.py, storage.py, cli.py, main.py)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create Task dataclass in src/models.py (id: int, title: str, description: str, completed: bool)
- [X] T005 [P] Implement InMemoryStorage class in src/storage.py with methods: add_task(), get_task_by_id(), update_task(), delete_task(), list_all_tasks(), toggle_complete()
- [X] T006 [P] Create CLI class in src/cli.py with methods for each command: add(), delete(), update(), view(), mark_complete()
- [X] T007 [P] Create main.py with main() function containing while True loop for menu display and user input handling
- [X] T008 [P] Implement input validation and error handling across all components
- [X] T009 [P] Add display formatting functions for task list presentation

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks with title and description, which are stored in memory and assigned unique IDs

**Independent Test**: Add a task with title and description, verify it appears in the task list with correct status [ ]

### Implementation for User Story 1

- [X] T010 [P] [US1] Implement add_task() method in InMemoryStorage class (depends on T004, T005)
- [X] T011 [P] [US1] Implement add() method in CLI class for task addition (depends on T006)
- [X] T012 [P] [US1] Add input prompts for title and description in CLI add() method (depends on T011)
- [X] T013 [US1] Implement ID generation and assignment in add_task() method (depends on T010)
- [X] T014 [US1] Add confirmation message display after task addition (depends on T011)
- [X] T015 [US1] Validate non-empty title before adding task (depends on T012)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Delete Task (Priority: P2)

**Goal**: Users can delete existing tasks by their unique ID, with appropriate error handling

**Independent Test**: Add a task, then delete it by ID, verify it's removed from the task list

### Implementation for User Story 2

- [X] T016 [P] [US2] Implement delete_task() method in InMemoryStorage class (depends on T005)
- [X] T017 [P] [US2] Implement delete() method in CLI class for task deletion (depends on T006)
- [X] T018 [P] [US2] Add input prompt for task ID in CLI delete() method (depends on T017)
- [X] T019 [US2] Validate ID format and existence before deletion (depends on T018)
- [X] T020 [US2] Add confirmation or error message after deletion attempt (depends on T017)
- [X] T021 [US2] Handle non-existent ID case with appropriate error message (depends on T019)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task (Priority: P3)

**Goal**: Users can update existing tasks' title and/or description, with partial updates allowed

**Independent Test**: Add a task, update its title or description, verify changes are applied correctly

### Implementation for User Story 3

- [X] T022 [P] [US3] Implement update_task() method in InMemoryStorage class (depends on T005)
- [X] T023 [P] [US3] Implement update() method in CLI class for task updates (depends on T006)
- [X] T024 [P] [US3] Add input prompts for task ID, new title, and new description in CLI update() method (depends on T023)
- [X] T025 [US3] Implement partial update logic (update only provided fields) (depends on T022)
- [X] T026 [US3] Add confirmation or error message after update attempt (depends on T023)
- [X] T027 [US3] Handle empty title case during updates (depends on T024)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - View Task List (Priority: P3)

**Goal**: Users can view all tasks in a formatted table showing ID, title, description, and completion status

**Independent Test**: Add multiple tasks, view task list, verify correct formatting and display of all tasks

### Implementation for User Story 4

- [X] T028 [P] [US4] Implement list_all_tasks() method in InMemoryStorage class (depends on T005)
- [X] T029 [P] [US4] Implement view() method in CLI class for displaying task list (depends on T006)
- [X] T030 [P] [US4] Create display formatting function for task list table (depends on T009)
- [X] T031 [US4] Add task list display with ID, title, description, and status [ ]/[x] (depends on T029)
- [X] T032 [US4] Implement description text shortening for long descriptions (depends on T030)
- [X] T033 [US4] Add "No tasks exist" message when task list is empty (depends on T028)

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P3)

**Goal**: Users can toggle task completion status, with confirmation of the updated status

**Independent Test**: Add a task, mark it complete, verify status changes to [x], mark it incomplete, verify status changes back to [ ]

### Implementation for User Story 5

- [X] T034 [P] [US5] Implement toggle_complete() method in InMemoryStorage class (depends on T005)
- [X] T035 [P] [US5] Implement mark_complete() method in CLI class for toggling status (depends on T006)
- [X] T036 [P] [US5] Add input prompt for task ID in CLI mark_complete() method (depends on T035)
- [X] T037 [US5] Implement status toggle logic and confirmation message (depends on T034)
- [X] T038 [US5] Display updated status [x] or [ ] after toggle operation (depends on T037)
- [X] T039 [US5] Validate task ID existence before toggling status (depends on T036)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final refinements

- [X] T040 [P] Update README with setup instructions and usage examples
- [X] T041 [P] Add sample session transcript for judges
- [X] T042 [P] Document command syntax and options in README
- [X] T043 [P] Add error handling for invalid menu choices
- [X] T044 [P] Implement graceful exit handling for quit command
- [X] T045 [P] Add type hints to all functions and classes
- [X] T046 [P] Add comprehensive docstrings for all functions and classes
- [X] T047 [P] Final code cleanup and PEP 8 compliance check
- [X] T048 [P] Run integration test of complete user workflow
- [X] T049 [P] Verify all error messages are helpful and clear

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tasks within a story can proceed in the order listed (dependencies shown)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members
- All polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all User Story 1 tasks in parallel:
Task: "Implement add_task() method in InMemoryStorage class"
Task: "Implement add() method in CLI class for task addition"
Task: "Add input prompts for title and description in CLI add() method"
Task: "Implement ID generation and assignment in add_task() method"
Task: "Add confirmation message display after task addition"
Task: "Validate non-empty title before adding task"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

**Total Task Count**: 49 tasks
**Tasks per User Story**:
- User Story 1 (Add): 6 tasks
- User Story 2 (Delete): 6 tasks
- User Story 3 (Update): 6 tasks
- User Story 4 (View): 6 tasks
- User Story 5 (Mark Complete): 6 tasks
**Parallel Opportunities**: High - multiple tasks can run in parallel within each phase
**Independent Test Criteria**: Each user story has clear independent test criteria defined
**Suggested MVP Scope**: User Story 1 (Add Task) only - provides core functionality