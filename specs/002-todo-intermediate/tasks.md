# Tasks: Intermediate Todo Features

**Input**: Design documents from `/specs/002-todo-intermediate/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested in spec. Manual console testing defined in plan.md testing strategy.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No new project setup needed — project already exists with Basic Level complete. This phase verifies the existing structure.

- [x] T001 Verify existing project structure and Basic Level code in src/models.py, src/storage.py, src/cli.py, src/main.py

**Checkpoint**: Basic Level code confirmed working, ready for extension.

---

## Phase 2: Foundational (Data Model Extension)

**Purpose**: Core data model changes that ALL user stories depend on. Must complete before any user story work.

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T002 Add Priority enum (HIGH=1, MEDIUM=2, LOW=3) to src/models.py
- [x] T003 Add parse_tags(raw: str) -> list[str] helper function to src/models.py — implements split by comma, strip whitespace, lowercase, filter empties, deduplicate preserving order
- [x] T004 Update Task dataclass in src/models.py — add priority: Priority (default MEDIUM), tags: list[str] (default empty list via field), created_at: datetime (default datetime.now() via field)
- [x] T005 Update InMemoryStorage.add_task() in src/storage.py — add priority: str = "medium" and tags: str = "" parameters, parse and validate priority, call parse_tags(), pass to Task constructor
- [x] T006 Update InMemoryStorage.update_task() in src/storage.py — add priority: Optional[str] = None and tags: Optional[str] = None parameters, validate and apply when provided

**Checkpoint**: Data model extended. Existing Basic features still work via default parameter values.

---

## Phase 3: User Story 1 + 2 — Add Tasks with Priority/Tags & Enhanced Display (Priority: P1)

**Goal**: Users can create tasks with priority and tags, and view them in an enhanced table format showing all fields.

**Independent Test**: Add a task with priority "high" and tags "work,urgent", then run view to see the enhanced table with Priority and Tags columns populated.

### Implementation

- [x] T007 [US1] Update CLI.add() in src/cli.py — add priority: str = "medium" and tags: str = "" parameters, validate priority against Priority enum, display error for invalid values, pass to storage.add_task()
- [x] T008 [US1] Update main.py add flow (choice "1") — add prompts for priority (with default "medium") and tags (comma-separated, optional), pass to cli.add()
- [x] T009 [US2] Update CLI.view() in src/cli.py — change table header to "ID | Title | Description | Priority | Tags | Status", format each row with priority.name.lower(), comma-joined tags (or "-" if empty), truncate description to 20 chars and tags to 15 chars

**Checkpoint**: Users can add tasks with priority/tags and see them in enhanced view. Basic add (without priority/tags) still works with defaults.

---

## Phase 4: User Story 3 — Filter Tasks (Priority: P2)

**Goal**: Users can filter the task list by a single criterion: status (completed/incomplete), priority (high/medium/low), or tag.

**Independent Test**: Add tasks with different priorities and statuses, then filter by priority "high" to see only high-priority tasks.

### Implementation

- [x] T010 [US3] Add filter_tasks(filter_type: str, value: str) -> list[Task] method to src/storage.py — implement three filter types: "status" (match completed bool), "priority" (match Priority enum), "tag" (case-insensitive tag membership), raise ValueError for invalid filter_type
- [x] T011 [US3] Add CLI.filter_tasks(filter_type: str, value: str) method to src/cli.py — call storage.filter_tasks(), display results using same table format as view(), show "No tasks match the filter" if empty, handle ValueError for invalid filter type
- [x] T012 [US3] Add filter menu option (choice "7") to src/main.py — prompt for filter type (status/priority/tag), prompt for value, call cli.filter_tasks()

**Checkpoint**: Filter works independently for each criterion type. No combined filters (per clarification).

---

## Phase 5: User Story 4 — Search Tasks (Priority: P2)

**Goal**: Users can search tasks by keyword across title, description, and tags using case-insensitive substring matching.

**Independent Test**: Add tasks with distinct titles/descriptions/tags, search for a keyword, verify matching tasks are returned.

### Implementation

- [x] T013 [P] [US4] Add search_tasks(keyword: str) -> list[Task] method to src/storage.py — lowercase keyword, check if keyword appears as substring in title.lower(), description.lower(), or any tag (already lowercase), return matching tasks via list comprehension
- [x] T014 [US4] Add CLI.search(keyword: str) method to src/cli.py — validate keyword is non-empty, call storage.search_tasks(), display results using same table format as view(), show "No tasks match the search" if empty
- [x] T015 [US4] Add search menu option (choice "6") to src/main.py — prompt for search keyword, call cli.search()

**Checkpoint**: Search returns correct results across all fields, case-insensitive, substring matching.

---

## Phase 6: User Story 5 — Sort Tasks (Priority: P3)

**Goal**: Users can sort the task list by priority (high first), title (A-Z), or creation date (oldest first).

**Independent Test**: Add tasks with different priorities/titles, sort by priority and verify high comes before medium before low.

### Implementation

- [x] T016 [P] [US5] Add sort_tasks(criterion: str) -> list[Task] method to src/storage.py — implement three sort keys: "priority" (key=lambda t: t.priority.value), "title" (key=lambda t: t.title.lower()), "date" (key=lambda t: t.created_at), raise ValueError for invalid criterion
- [x] T017 [US5] Add CLI.sort(criterion: str) method to src/cli.py — validate criterion, call storage.sort_tasks(), display results using same table format as view(), show "No tasks exist" if empty, handle ValueError for invalid criterion
- [x] T018 [US5] Add sort menu option (choice "8") to src/main.py — prompt for sort criterion (priority/title/date), call cli.sort()

**Checkpoint**: Sort reorders correctly for all three criteria. Stable sort preserves relative order for equal elements.

---

## Phase 7: User Story 6 — Update Tasks with Priority and Tags (Priority: P3)

**Goal**: Users can update an existing task's priority and tags after creation.

**Independent Test**: Create a task with priority "medium", update it to "high" with new tags, verify changes appear in view.

### Implementation

- [x] T019 [US6] Update CLI.update() in src/cli.py — add priority and tags parameters, pass to storage.update_task(), validate priority if provided, display success/error messages
- [x] T020 [US6] Update main.py update flow (choice "3") — add prompts for optional new priority and optional new tags after existing title/description prompts, pass to cli.update()

**Checkpoint**: Priority and tags can be changed on existing tasks. Original update behavior (title/description only) still works.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, edge cases, and backward compatibility.

- [x] T021 Validate all five Basic features (add, delete, update, view, mark) still work correctly with default parameters in src/main.py
- [x] T022 Validate edge cases: duplicate tags, empty tags, whitespace tags, invalid priority, empty search, empty filter results, empty sort in src/cli.py and src/storage.py
- [x] T023 Renumber menu options in src/main.py — ensure Search=6, Filter=7, Sort=8, Quit=9 with correct numbering and clean display
- [x] T024 Run quickstart.md validation — verify setup instructions and example session work end-to-end

**Checkpoint**: All intermediate features working. All Basic features unchanged. No crashes on invalid input.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — verify existing code
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1+US2 (Phase 3)**: Depends on Phase 2 — MVP milestone
- **US3 Filter (Phase 4)**: Depends on Phase 2 (and Phase 3 for display helper reuse)
- **US4 Search (Phase 5)**: Depends on Phase 2 — independent of US3
- **US5 Sort (Phase 6)**: Depends on Phase 2 — independent of US3/US4
- **US6 Update (Phase 7)**: Depends on Phase 2 (storage.update_task already updated)
- **Polish (Phase 8)**: Depends on all user story phases complete

### User Story Dependencies

- **US1+US2 (P1)**: Requires Phase 2 only. No dependencies on other stories.
- **US3 Filter (P2)**: Requires Phase 2. Reuses display format from US2 (Phase 3).
- **US4 Search (P2)**: Requires Phase 2. Independent of other stories. T013 is parallelizable.
- **US5 Sort (P3)**: Requires Phase 2. Independent of other stories. T016 is parallelizable.
- **US6 Update (P3)**: Requires Phase 2 (T006 already updates storage). Independent of US3-US5.

### Within Each User Story

- Storage layer methods before CLI methods
- CLI methods before main.py menu integration

### Parallel Opportunities

- T013 [US4] and T016 [US5] can run in parallel (different methods in storage.py, but same file — safe if done as separate additions)
- US3, US4, US5, US6 can all start after Phase 2 completes (if team has capacity)
- Within Phase 2: T002 and T003 can be developed concurrently (different constructs in models.py)

---

## Parallel Example: After Phase 2

```text
# After foundational phase, these story phases can proceed in parallel:
Phase 3 (US1+US2): CLI add/view + main.py add flow
Phase 4 (US3):     Storage filter + CLI filter + main.py filter
Phase 5 (US4):     Storage search + CLI search + main.py search
Phase 6 (US5):     Storage sort + CLI sort + main.py sort
Phase 7 (US6):     CLI update + main.py update flow
```

---

## Implementation Strategy

### MVP First (US1 + US2 Only)

1. Complete Phase 1: Verify existing code
2. Complete Phase 2: Data model extension (Priority enum, parse_tags, updated Task)
3. Complete Phase 3: US1+US2 (add with priority/tags + enhanced view)
4. **STOP and VALIDATE**: Add tasks with priority/tags, view enhanced table
5. Demo if ready — users can now organize tasks

### Incremental Delivery

1. Phase 1+2 → Foundation ready
2. Add US1+US2 → Test independently → Demo (MVP — tasks have priority and tags)
3. Add US3 (Filter) → Test independently → Demo (users can filter)
4. Add US4 (Search) → Test independently → Demo (users can search)
5. Add US5 (Sort) → Test independently → Demo (users can sort)
6. Add US6 (Update) → Test independently → Demo (users can update priority/tags)
7. Phase 8 Polish → Full validation → Complete

---

## Notes

- [P] tasks = different files or independent additions, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable after Phase 2
- No test tasks generated (not explicitly requested in spec)
- Commit after each phase or logical group
- Stop at any checkpoint to validate story independently
- Total: 24 tasks across 8 phases
