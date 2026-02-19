# Tasks: Advanced Todo Features

**Input**: Design documents from `/specs/003-todo-advanced/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested in spec. Test tasks omitted. Manual console test flows defined in plan.md.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root

---

## Phase 1: Setup

**Purpose**: No new project structure needed — extending existing files. This phase adds the new enum and helper functions to the data model.

- [x] T001 Add `RecurrenceInterval` enum (DAILY, WEEKLY, MONTHLY with string values) to `src/models.py`
- [x] T002 Add `parse_due_date(raw: str) -> datetime` function to `src/models.py` — supports ISO format ("YYYY-MM-DD", "YYYY-MM-DD HH:MM"), "today", "tomorrow", optional "HH:MM" suffix, default time 23:59; raises ValueError on invalid input
- [x] T003 Add `advance_due_date(due_date: datetime, interval: RecurrenceInterval) -> datetime` function to `src/models.py` — daily (+1 day), weekly (+7 days), monthly (increment month with calendar.monthrange() clamping for edge cases like Jan 31 → Feb 28)
- [x] T004 Add `get_alert_status(task: Task) -> Optional[str]` function to `src/models.py` — returns "OVERDUE" if incomplete + past due, "DUE SOON" if incomplete + due within 24h, None otherwise; completed tasks always return None
- [x] T005 Update `Task` dataclass in `src/models.py` — add `due_date: Optional[datetime] = None` and `recurrence: Optional[RecurrenceInterval] = None` fields after existing fields

**Checkpoint**: Data model extended. All existing Basic + Intermediate code still works (new fields have None defaults).

---

## Phase 2: Foundational (Storage Layer Updates)

**Purpose**: Update storage methods to accept and handle the new fields. MUST complete before user story CLI work.

**⚠️ CRITICAL**: No user story CLI work can begin until this phase is complete.

- [x] T006 Update `add_task()` in `src/storage.py` — add optional parameters `due_date: str = ""` and `recurrence: str = ""`; parse due_date via `parse_due_date()` if non-empty; validate recurrence via `RecurrenceInterval(value)` if non-empty; pass parsed values to Task constructor
- [x] T007 Update `update_task()` in `src/storage.py` — add optional parameters `due_date: Optional[str] = None` and `recurrence: Optional[str] = None`; if value is "none" clear the field (set to None); if non-empty string parse/validate and set; if None (not provided) keep current value
- [x] T008 Update `toggle_complete()` in `src/storage.py` — after toggling, if task becomes completed AND has recurrence AND has due_date: reset completed to False, advance due_date via `advance_due_date()`, return True to indicate reschedule happened; otherwise return False for normal toggle

**Checkpoint**: Storage layer handles all new fields. Existing add/update/toggle calls still work with default parameters.

---

## Phase 3: User Story 1 — Set Due Dates on Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can set, update, and clear due dates when adding or updating tasks. Due dates display in the task list.

**Independent Test**: Add a task with due date "2026-03-01", view task list, verify due date column shows "2026-03-01 23:59". Add a task without due date, verify "-" in due date column. Update a task's due date, verify change. Enter invalid date, verify error message.

### Implementation for User Story 1

- [x] T009 [US1] Update `cli.add()` in `src/cli.py` — add `due_date: str = ""` parameter; if non-empty, validate via `parse_due_date()` and catch ValueError to print error and return early; pass to `storage.add_task()`
- [x] T010 [US1] Update `cli.update()` in `src/cli.py` — add `due_date: Optional[str] = None` parameter; pass to `storage.update_task()` (handles "none" to clear, empty to keep)
- [x] T011 [US1] Update `cli._display_tasks()` in `src/cli.py` — add "Due Date" column; format as "YYYY-MM-DD HH:MM" if set, "-" if None; adjust column widths
- [x] T012 [US1] Update add flow in `src/main.py` — add input prompt: "Enter due date (YYYY-MM-DD, today, tomorrow, or Enter to skip): "; pass to `cli.add()`
- [x] T013 [US1] Update update flow in `src/main.py` — add input prompt: "Enter new due date (or Enter to keep, 'none' to clear): "; pass to `cli.update()`

**Checkpoint**: Due dates can be set, displayed, updated, and cleared. Invalid dates show errors. Tasks without due dates work as before.

---

## Phase 4: User Story 2 — Due Date Reminders and Alerts (Priority: P1)

**Goal**: Overdue and due-soon tasks show visual indicators in the task list. App startup shows alert summary.

**Independent Test**: Add tasks with past due dates and near-future due dates. View task list. Verify "OVERDUE" and "DUE SOON" appear in Alert column. Verify completed tasks with past due dates show no alert. Restart app and verify startup summary.

**Dependencies**: Requires US1 (due dates must be settable to test alerts)

### Implementation for User Story 2

- [x] T014 [US2] Update `cli._display_tasks()` in `src/cli.py` — add "Alert" column; call `get_alert_status()` for each task; display "OVERDUE", "DUE SOON", or "-"
- [x] T015 [US2] Add `show_startup_alerts()` method to CLI class in `src/cli.py` — iterate all tasks, count overdue and due-soon using `get_alert_status()`; print "You have X overdue tasks and Y due soon" only if X > 0 or Y > 0
- [x] T016 [US2] Update `src/main.py` — call `cli.show_startup_alerts()` after welcome message

**Checkpoint**: Alerts display correctly in task list and on startup. Completed tasks are never flagged.

---

## Phase 5: User Story 3 — Recurring Tasks (Priority: P2)

**Goal**: Users can set recurrence (daily/weekly/monthly) on tasks. Completing a recurring task resets it and advances the due date.

**Independent Test**: Add a weekly recurring task with due date "2026-02-15". Mark it complete. Verify it resets to incomplete with due date "2026-02-22". Add a monthly task due Jan 31, mark complete, verify due date becomes Feb 28. Add invalid recurrence "biweekly", verify error message.

**Dependencies**: Requires US1 (due dates) for reschedule to work meaningfully

### Implementation for User Story 3

- [x] T017 [US3] Update `cli.add()` in `src/cli.py` — add `recurrence: str = ""` parameter; if non-empty, validate via `RecurrenceInterval(value)` and catch ValueError to print error listing valid options (daily, weekly, monthly); pass to `storage.add_task()`
- [x] T018 [US3] Update `cli.update()` in `src/cli.py` — add `recurrence: Optional[str] = None` parameter; pass to `storage.update_task()` (handles "none" to clear, empty to keep)
- [x] T019 [US3] Update `cli.mark()` in `src/cli.py` — check return value from `toggle_complete()`; if reschedule happened, print message like "Recurring task rescheduled. New due date: YYYY-MM-DD HH:MM"
- [x] T020 [US3] Update add flow in `src/main.py` — add input prompt: "Enter recurrence (daily/weekly/monthly, or Enter to skip): "; pass to `cli.add()`
- [x] T021 [US3] Update update flow in `src/main.py` — add input prompt: "Enter new recurrence (daily/weekly/monthly, Enter to keep, 'none' to clear): "; pass to `cli.update()`

**Checkpoint**: Recurring tasks can be created, rescheduled on completion, updated, and cleared. Non-recurring tasks behave identically to before.

---

## Phase 6: User Story 4 — Enhanced Display (Priority: P2)

**Goal**: Task list view shows all new columns: Due Date, Recurrence, Alert alongside existing columns.

**Independent Test**: Add tasks with various combinations of due dates and recurrence. View the list. Verify all columns render correctly with proper alignment and truncation.

**Dependencies**: Requires US1 (due dates) and US3 (recurrence) for complete display

### Implementation for User Story 4

- [x] T022 [US4] Update `cli._display_tasks()` in `src/cli.py` — add "Recurrence" column; display interval value if set, "-" if None; ensure full column header row and separator line include all columns: ID, Title, Description, Due Date, Recurrence, Alert, Priority, Tags, Status
- [x] T023 [US4] Adjust column widths and truncation in `cli._display_tasks()` in `src/cli.py` — ensure readable alignment for the expanded table (Due Date: 19 chars, Recurrence: 10 chars, Alert: 8 chars)

**Checkpoint**: Complete enhanced display with all Advanced columns. Backward-compatible for tasks with no due date or recurrence (shows "-").

---

## Phase 7: User Story 5 — JSON Persistence (Priority: P3)

**Goal**: Users can save all tasks to `tasks.json` and load them back, preserving all fields.

**Independent Test**: Add tasks with all field types (priority, tags, due date, recurrence). Save to file. Clear storage or restart. Load from file. Verify all data preserved. Test missing file (friendly message). Test corrupted file (error message, in-memory unchanged).

**Dependencies**: None on other user stories (operates on whatever tasks exist)

### Implementation for User Story 5

- [x] T024 [US5] Add `save_to_json(filepath: str) -> None` method to `InMemoryStorage` in `src/storage.py` — serialize all tasks to JSON dict list with custom handling: Priority → name.lower(), RecurrenceInterval → .value or null, datetime → .isoformat() or null; include next_id; write with json.dump(indent=2)
- [x] T025 [US5] Add `load_from_json(filepath: str) -> None` method to `InMemoryStorage` in `src/storage.py` — read JSON file; deserialize each task dict back to Task object with reverse conversions: Priority[value.upper()], RecurrenceInterval(value), datetime.fromisoformat(); restore next_id; handle FileNotFoundError (raise with friendly message), json.JSONDecodeError and KeyError/ValueError (raise with error message); do NOT clear existing tasks on error
- [x] T026 [US5] Add `save_tasks()` method to CLI class in `src/cli.py` — call `storage.save_to_json("tasks.json")`; print "Tasks saved to tasks.json"; catch exceptions and print error
- [x] T027 [US5] Add `load_tasks()` method to CLI class in `src/cli.py` — call `storage.load_from_json("tasks.json")`; print "Loaded X tasks from tasks.json"; catch FileNotFoundError and print "No saved tasks found"; catch other exceptions and print error message
- [x] T028 [US5] Update menu in `src/main.py` — add option 9 "Save Tasks to File" calling `cli.save_tasks()`; add option 10 "Load Tasks from File" calling `cli.load_tasks()`; renumber Quit to option 11

**Checkpoint**: Full save/load round-trip works. All task fields preserved. Graceful handling of missing/corrupted files.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and backward compatibility checks

- [x] T029 Verify all Basic features (add, delete, update, view, mark) still work without specifying due_date or recurrence in `src/` files
- [x] T030 Verify all Intermediate features (priority, tags, search, filter, sort) still work unchanged in `src/` files
- [x] T031 Run existing `test_app.py` and verify no regressions
- [x] T032 Test edge cases from plan.md: recurring task without due date, past due date on creation, monthly Jan 31 → Feb 28, save empty list, corrupted JSON file

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2
- **US2 (Phase 4)**: Depends on US1 (needs due dates to test alerts)
- **US3 (Phase 5)**: Depends on US1 (needs due dates for reschedule)
- **US4 (Phase 6)**: Depends on US1 + US3 (needs all columns to display)
- **US5 (Phase 7)**: Depends on Phase 2 only (can run after foundational, parallel with US1-US4)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational)
                        │
                        ├──→ US1 (Due Dates) ──→ US2 (Alerts)
                        │         │                    │
                        │         └──→ US3 (Recurring) ─┤
                        │                   │           │
                        │                   └──→ US4 (Display)
                        │
                        └──→ US5 (JSON Persistence) ←── can start in parallel

                        All stories ──→ Phase 8 (Polish)
```

### Within Each User Story

- CLI changes before main.py changes (cli methods must exist before menu wires them)
- Display updates integrate incrementally (US1 adds Due Date column, US2 adds Alert, US4 adds Recurrence)

### Parallel Opportunities

- T001-T005 (Phase 1) are sequential within `src/models.py` (same file)
- T006-T008 (Phase 2) are sequential within `src/storage.py` (same file)
- US5 (T024-T028) can run in parallel with US1-US4 after Phase 2
- T029-T032 (Phase 8) are independent validation tasks and can run in parallel

---

## Parallel Example: After Phase 2

```text
# These can run in parallel after Foundational phase:
Track A: US1 → US2 → US3 → US4  (sequential due to dependencies)
Track B: US5                      (independent, only needs Phase 2)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T008)
3. Complete Phase 3: User Story 1 — Due Dates (T009-T013)
4. **STOP and VALIDATE**: Add a task with a due date, view the list, verify due date displays

### Incremental Delivery

1. Setup + Foundational → Model and storage ready
2. Add US1 (Due Dates) → Test → First visible feature
3. Add US2 (Alerts) → Test → Due dates now actionable
4. Add US3 (Recurring) → Test → Auto-scheduling works
5. Add US4 (Display) → Test → Complete enhanced view
6. Add US5 (Persistence) → Test → Data survives restarts
7. Polish → Final validation of all features together

---

## Summary

| Metric | Value |
|--------|-------|
| **Total tasks** | 32 |
| **Phase 1 (Setup)** | 5 tasks |
| **Phase 2 (Foundational)** | 3 tasks |
| **US1 - Due Dates (P1)** | 5 tasks |
| **US2 - Alerts (P1)** | 3 tasks |
| **US3 - Recurring (P2)** | 5 tasks |
| **US4 - Display (P2)** | 2 tasks |
| **US5 - Persistence (P3)** | 5 tasks |
| **Phase 8 (Polish)** | 4 tasks |
| **Parallel tracks** | 2 (US1-4 sequential, US5 independent) |
| **MVP scope** | Phase 1 + 2 + US1 = 13 tasks |

---

## Notes

- No test tasks generated (not requested in spec)
- All changes are to existing files — no new source files created
- New model fields have None defaults — full backward compatibility
- Display column additions are incremental (US1 → US2 → US4)
- Commit after each phase checkpoint for safe rollback points
