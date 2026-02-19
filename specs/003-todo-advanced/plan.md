# Implementation Plan: Advanced Todo Features

**Branch**: `003-todo-advanced` | **Date**: 2026-02-16 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-todo-advanced/spec.md`

## Summary

Extend the existing Basic + Intermediate console todo app with three intelligent time-based features: due dates with passive console alerts (OVERDUE/DUE SOON), recurring tasks that auto-reschedule on completion, and optional JSON file persistence. The implementation modifies four existing files (`models.py`, `storage.py`, `cli.py`, `main.py`) using only Python stdlib modules (`datetime`, `calendar`, `json`). All Basic and Intermediate features remain backward-compatible.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (`dataclasses`, `datetime`, `calendar`, `json`, `enum`, `typing`)
**Storage**: In-memory (extending existing `InMemoryStorage`) + optional JSON file persistence (`tasks.json`)
**Testing**: Manual console testing + pytest (`test_app.py` exists)
**Target Platform**: Console / CLI (cross-platform)
**Project Type**: Single project
**Performance Goals**: All operations complete instantly (in-memory, <100 tasks typical)
**Constraints**: No external libraries, console alerts only (no push notifications), no timezone handling
**Scale/Scope**: Single-user console app, <1000 tasks in-memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Three-Level Evolution | PASS | Building Advanced on completed Basic + Intermediate |
| II. 100% Agentic & Spec-Driven | PASS | Using /sp.specify → /sp.plan → /sp.tasks flow |
| III. Tech Stack (Python 3.13+, UV, stdlib) | PASS | Only `calendar` and `json` added — both stdlib |
| IV. Extensible Architecture | PASS | New fields added with defaults; new methods extend existing classes |
| V. Storage Progression (persistence at Advanced) | PASS | Constitution explicitly allows file/JSON persistence at Advanced level |
| VI. Clean Python Standards | PASS | PEP 8, type hints, docstrings, error handling planned |
| No Global Variables | PASS | Using class instances (InMemoryStorage, CLI) |
| Traceability | PASS | Spec, plan, research, data-model, PHRs all maintained |
| Sequential Level Completion | PASS | Basic + Intermediate code exists and is complete |

All gates pass. No violations.

## Project Structure

### Documentation (this feature)

```text
specs/003-todo-advanced/
├── plan.md              # This file
├── research.md          # Phase 0: technology decisions
├── data-model.md        # Phase 1: updated entity model
├── quickstart.md        # Phase 1: dev setup guide
└── tasks.md             # Phase 2 output (/sp.tasks - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # CLI entry point — add menu options 10-11 (save/load), startup alerts
├── models.py            # Task dataclass — add due_date, recurrence fields + helper functions
├── storage.py           # InMemoryStorage — update add/update/toggle + add save/load JSON
└── cli.py               # CLI class — update display, add save/load commands
```

**Structure Decision**: Retain existing flat `src/` layout. No new files needed — all changes extend existing modules. This minimizes diff size and preserves the existing architecture.

## Architecture

### Component Diagram

```text
┌───────────────────────────────────────────────────────────┐
│                        main.py                             │
│  Menu loop: 1-Add 2-Del 3-Update 4-View 5-Mark           │
│  6-Search 7-Filter 8-Sort                                 │
│  NEW: 9-SaveJSON 10-LoadJSON 11-Quit                      │
│  NEW: Startup alert summary (overdue + due soon counts)   │
└──────────────────────────┬────────────────────────────────┘
                           │ delegates to
                           ▼
┌───────────────────────────────────────────────────────────┐
│                         cli.py                             │
│  Existing: add, delete, update, view, mark, search,       │
│            filter_tasks, sort                              │
│  UPDATED:  add (due_date, recurrence params)              │
│            update (due_date, recurrence params)            │
│            view (enhanced table: Due Date, Recurrence,     │
│                  Alert columns)                            │
│            mark (handles recurring task reschedule msg)    │
│  NEW:      save_tasks()                                   │
│            load_tasks()                                    │
│            show_startup_alerts()                           │
└──────────────────────────┬────────────────────────────────┘
                           │ calls
                           ▼
┌───────────────────────────────────────────────────────────┐
│                       storage.py                           │
│  Existing: add_task, get_task_by_id, update_task,         │
│            delete_task, list_all_tasks, toggle_complete,   │
│            search_tasks, filter_tasks, sort_tasks          │
│  UPDATED:  add_task (due_date, recurrence params)         │
│            update_task (due_date, recurrence params)       │
│            toggle_complete (recurring reschedule logic)    │
│  NEW:      save_to_json(filepath) → None                  │
│            load_from_json(filepath) → None                │
└──────────────────────────┬────────────────────────────────┘
                           │ uses
                           ▼
┌───────────────────────────────────────────────────────────┐
│                       models.py                            │
│  EXISTING: Priority(Enum), parse_tags(), Task             │
│  UPDATED Task dataclass:                                  │
│    NEW: due_date: Optional[datetime] = None               │
│    NEW: recurrence: Optional[RecurrenceInterval] = None   │
│  NEW: RecurrenceInterval(Enum): DAILY, WEEKLY, MONTHLY   │
│  NEW: parse_due_date(raw: str) → datetime                 │
│  NEW: advance_due_date(due_date, interval) → datetime     │
│  NEW: get_alert_status(task) → Optional[str]              │
└───────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Add with due date/recurrence**: `main.py` prompts for due_date + recurrence → `cli.add()` parses/validates via `parse_due_date()` → `storage.add_task()` creates Task with new fields
2. **View with alerts**: `cli.view()` → for each task, calls `get_alert_status()` → renders enhanced table with Due Date, Recurrence, Alert columns
3. **Mark recurring task**: `cli.mark()` → `storage.toggle_complete()` detects recurring task → resets completed, advances due_date via `advance_due_date()` → prints reschedule message
4. **Startup alerts**: `main.py` → `cli.show_startup_alerts()` → iterates tasks, counts overdue/due-soon using `get_alert_status()` → prints summary
5. **Save/Load**: `cli.save_tasks()` → `storage.save_to_json("tasks.json")` serializes all tasks to JSON. `cli.load_tasks()` → `storage.load_from_json("tasks.json")` deserializes and populates storage.

## Key Decisions

### D1: Date Parsing — Custom vs Library

| Option | Pros | Cons |
|--------|------|------|
| **Custom parser (chosen)** | No external deps, handles "today"/"tomorrow" natively | More code to write |
| `dateutil` library | Full natural language support | External dependency, violates constitution |

**Decision**: Custom `parse_due_date()` function in `models.py` that handles ISO format and "today"/"tomorrow" shortcuts. Uses `datetime.strptime()` for ISO and `datetime.now().date() + timedelta()` for shortcuts. Defaults time to 23:59 when not specified.

### D2: Alert Computation — Dynamic vs Stored

| Option | Pros | Cons |
|--------|------|------|
| **Dynamic computation (chosen)** | Always accurate, no stale state | Computed on every view |
| Stored field | Faster lookup | Becomes stale, needs refresh logic |

**Decision**: Compute alert status dynamically via `get_alert_status()` at display time. Performance is negligible for <1000 tasks.

### D3: Recurring Task Completion Behavior

| Option | Pros | Cons |
|--------|------|------|
| **Reset + advance (chosen)** | Single task, clean history | Loses completion record |
| Create new task + mark old complete | Preserves history | Task ID changes, more complex |

**Decision**: On completion of a recurring task, reset `completed = False` and advance `due_date`. This matches the spec requirement and keeps the task list clean.

### D4: Monthly Recurrence Edge Case

| Option | Pros | Cons |
|--------|------|------|
| **Clamp to last day (chosen)** | Standard calendar behavior | Requires `calendar.monthrange()` |
| Skip to 1st of following month | Simple | Unintuitive |

**Decision**: Use `calendar.monthrange()` to clamp to last valid day. Jan 31 → Feb 28/29.

### D5: JSON Persistence — Opt-in via Menu

| Option | Pros | Cons |
|--------|------|------|
| **Explicit save/load commands (chosen)** | User controls when to persist | Manual step |
| Auto-save on every change | No data loss risk | Adds I/O on every operation, unexpected side effects |

**Decision**: Save and Load are explicit menu options (9 and 10). File is always `tasks.json` in the working directory. No auto-save.

### D6: RecurrenceInterval — Enum with String Values

**Decision**: Use `enum.Enum` with string values (`"daily"`, `"weekly"`, `"monthly"`) for clean display and JSON serialization. Parallels the `Priority` enum pattern from Intermediate.

## Implementation Phases

### Phase A: Data Model Extension (models.py)

1. Add `RecurrenceInterval` enum with DAILY, WEEKLY, MONTHLY (string values)
2. Add `parse_due_date(raw: str) -> datetime` function
3. Add `advance_due_date(due_date, interval) -> datetime` function using `calendar.monthrange()`
4. Add `get_alert_status(task) -> Optional[str]` function
5. Update `Task` dataclass: add `due_date` and `recurrence` fields with `None` defaults
6. Verify backward compatibility (existing Task creation still works)

### Phase B: Storage Layer Extension (storage.py)

1. Update `add_task()` signature: add `due_date` and `recurrence` parameters with defaults
2. Update `update_task()` signature: add `due_date` and `recurrence` parameters
3. Update `toggle_complete()`: detect recurring task, reset + advance due date
4. Add `save_to_json(filepath: str) → None` with custom serialization
5. Add `load_from_json(filepath: str) → None` with custom deserialization + error handling

### Phase C: CLI Layer Enhancement (cli.py)

1. Update `add()` method: accept and pass due_date/recurrence strings, validate via `parse_due_date()`
2. Update `update()` method: accept due_date/recurrence, handle "none" to clear
3. Update `_display_tasks()`: add Due Date, Recurrence, Alert columns using `get_alert_status()`
4. Update `mark()` method: print reschedule message for recurring tasks
5. Add `save_tasks()` method
6. Add `load_tasks()` method
7. Add `show_startup_alerts()` method

### Phase D: Main Menu Update (main.py)

1. Update add flow: prompt for optional due date and recurrence
2. Update update flow: prompt for due date and recurrence (Enter to keep, "none" to clear)
3. Add menu options for Save Tasks (9) and Load Tasks (10)
4. Renumber Quit to option 11
5. Add startup alert summary after welcome message
6. Wire load-tasks option to populate storage before startup alerts

### Phase E: Testing & Validation

1. Test all Basic + Intermediate features still work unchanged
2. Test due date parsing: ISO, today, tomorrow, with/without time, invalid formats
3. Test alert classification: overdue, due soon, no alert, completed tasks
4. Test recurring task completion: daily, weekly, monthly, edge cases
5. Test monthly edge cases: Jan 31 → Feb 28/29
6. Test save/load: round-trip all fields, empty list, missing file, corrupted file
7. Test startup alert summary: overdue count, due-soon count, no alerts
8. Run existing test_app.py to verify no regressions

## Testing Strategy

### Manual Console Test Flows

| Test | Input | Expected Output |
|------|-------|-----------------|
| Add with due date (ISO) | Due: "2026-03-01" | Task created, due date shows "2026-03-01 23:59" |
| Add with due date + time | Due: "2026-03-01 15:00" | Task created, due date shows "2026-03-01 15:00" |
| Add with "today" | Due: "today" | Due date = today at 23:59 |
| Add with "tomorrow 14:30" | Due: "tomorrow 14:30" | Due date = tomorrow at 14:30 |
| Add with invalid date | Due: "not-a-date" | Error message, no task created |
| Add with recurrence | Recurrence: "weekly" | Task created with weekly recurrence |
| Add with invalid recurrence | Recurrence: "biweekly" | Error message listing valid options |
| View overdue task | Task due in the past | Alert column shows "OVERDUE" |
| View due-soon task | Task due within 24h | Alert column shows "DUE SOON" |
| View future task | Task due >24h away | Alert column shows "-" |
| View completed overdue | Completed task, past due | No alert shown |
| Mark recurring daily | Mark daily task complete | Reset to incomplete, due date +1 day |
| Mark recurring weekly | Mark weekly task complete | Reset to incomplete, due date +7 days |
| Mark recurring monthly | Mark monthly Jan 31 task | Reset to incomplete, due date = Feb 28 |
| Mark non-recurring | Mark regular task complete | Normal toggle behavior |
| Save tasks | Choose save option | "Tasks saved to tasks.json" |
| Load tasks | Choose load option | "Loaded X tasks from tasks.json" |
| Load missing file | No tasks.json exists | "No saved tasks found" |
| Load corrupted file | Invalid JSON in tasks.json | Error message, in-memory tasks unchanged |
| Startup alerts | App start with overdue/due-soon tasks | Summary printed |
| Update clear due date | Due: "none" | Due date removed |
| Update clear recurrence | Recurrence: "none" | Recurrence removed |
| Update keep due date | Due: (empty Enter) | Due date unchanged |

### Edge Case Tests

| Edge Case | Input | Expected |
|-----------|-------|----------|
| Recurrence without due date | Recurrence: "daily", no due date | Stored but no reschedule effect |
| Past due date on creation | Due: "2020-01-01" | Created, immediately shown as OVERDUE |
| Multiple completions of recurring | Mark complete 3 times | Due date advances 3 intervals |
| Monthly from Jan 31 | Monthly, due Jan 31 | Next: Feb 28 (or 29 in leap year) |
| Monthly from Mar 31 | Monthly, due Mar 31 | Next: Apr 30 |
| Save empty task list | No tasks, save | Valid JSON with empty list |
| Save/load round-trip | All field types | All preserved exactly |

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Breaking Basic/Intermediate features | High | Low | New fields have None defaults; test backward compatibility first |
| Date parsing edge cases | Medium | Medium | Comprehensive test cases; clear error messages on invalid input |
| JSON serialization losing data | Medium | Low | Round-trip tests for all field types; type-specific serializers |

## Complexity Tracking

No constitution violations. No complexity justifications needed.
