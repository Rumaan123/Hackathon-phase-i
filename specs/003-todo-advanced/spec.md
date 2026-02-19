# Feature Specification: Advanced Todo Features

**Feature Branch**: `003-todo-advanced`
**Created**: 2026-02-15
**Status**: Draft
**Input**: User description: "Add intelligent features to the console todo app: recurring tasks, due dates with reminders. Builds on Basic + Intermediate levels."

## Overview

The Advanced Level extends the existing Basic + Intermediate todo application with intelligent time-based features: due dates with reminder alerts, and recurring tasks that auto-reschedule on completion. Storage remains primarily in-memory with optional JSON file persistence for cross-session recurrence. The console interface is enhanced to display due dates, overdue indicators, and recurrence information.

### Goals

1. Allow users to set due dates and times on tasks and receive console alerts for overdue or upcoming items
2. Support recurring tasks that automatically reschedule their next occurrence when marked complete
3. Optionally persist task data to a JSON file so recurring tasks survive application restarts
4. Maintain full backward compatibility with all Basic and Intermediate features

### Assumptions

- Due dates are optional; tasks without due dates behave exactly as before
- Recurring interval is optional and independent of due date (though recurring tasks typically have a due date)
- "Due soon" means the task is due within the next 24 hours
- "Overdue" means the current date/time has passed the task's due date
- Reminders are passive — displayed when viewing tasks or on app start, not real-time push notifications
- Date input supports ISO format ("YYYY-MM-DD HH:MM") and natural shortcuts ("today", "tomorrow") with optional time
- If no time is specified for a due date, it defaults to end of day (23:59)
- Recurring tasks: when marked complete, the task is reset to incomplete with the due date advanced by the interval
- JSON persistence is opt-in (user chooses to save/load), not automatic
- Only three recurrence intervals are supported: daily, weekly, monthly

### Non-Goals

- Full web UI or browser notification implementation (console alerts only)
- Complex calendar integration or timezone handling
- Push notifications or real-time background timers
- Advanced recurrence rules (e.g., "every 2nd Tuesday", "weekdays only")
- Multi-user or shared task lists

## Clarifications

### Session 2026-02-15

- Q: Where should the JSON persistence file be stored? → A: Fixed file `tasks.json` in the current working directory. No user-configurable path.
- Q: How should users clear (remove) a due date or recurrence on update? → A: Type "none" to clear the field. Empty Enter keeps the current value (consistent with existing update behavior).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Set Due Dates on Tasks (Priority: P1)

As a user, I want to assign a due date and time when creating or updating a task so I know when each task needs to be completed.

**Why this priority**: Due dates are the foundational time-based data that reminders and recurrence depend on. Without due dates, no other Advanced feature can function.

**Independent Test**: Can be fully tested by adding a task with a due date, viewing the task list, and verifying the due date appears correctly.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** I add a task with due date "2026-03-01 15:00", **Then** the task is created with the due date stored and displayed in the view.
2. **Given** the app is running, **When** I add a task with due date "tomorrow", **Then** the due date is set to tomorrow at 23:59.
3. **Given** the app is running, **When** I add a task with due date "today 14:30", **Then** the due date is set to today at 14:30.
4. **Given** the app is running, **When** I add a task without a due date, **Then** the task is created with no due date (displayed as "-" in the view).
5. **Given** the app is running, **When** I add a task with an invalid due date (e.g., "not-a-date"), **Then** an error message is displayed and no task is created.
6. **Given** a task exists, **When** I update its due date, **Then** the due date is changed and the updated value appears in the view.

---

### User Story 2 - Due Date Reminders and Alerts (Priority: P1)

As a user, I want to see visual indicators for overdue and upcoming tasks so I can prioritize what needs attention.

**Why this priority**: Reminders provide the core value proposition of due dates — without them, due dates are just passive data with no actionable feedback.

**Independent Test**: Can be tested by adding tasks with past and near-future due dates, then viewing the task list and verifying "Overdue" and "Due soon" labels appear.

**Acceptance Scenarios**:

1. **Given** a task has a due date in the past, **When** I view the task list, **Then** the task shows an "OVERDUE" indicator next to its due date.
2. **Given** a task is due within the next 24 hours, **When** I view the task list, **Then** the task shows a "DUE SOON" indicator.
3. **Given** a task has a future due date more than 24 hours away, **When** I view the task list, **Then** the due date is shown without any indicator.
4. **Given** overdue or due-soon tasks exist, **When** the app starts, **Then** a summary of alerts is printed (e.g., "You have 2 overdue tasks and 1 due soon").
5. **Given** a completed task has a past due date, **When** I view the task list, **Then** no overdue indicator is shown (completed tasks are not flagged).

---

### User Story 3 - Recurring Tasks (Priority: P2)

As a user, I want to create tasks that automatically reschedule after completion so I don't have to manually recreate repeating items.

**Why this priority**: Recurrence builds on due dates (P1) and adds automation. It is the most complex feature but delivers significant value for routine tasks.

**Independent Test**: Can be tested by creating a recurring weekly task with a due date, marking it complete, and verifying the task resets to incomplete with the due date advanced by one week.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** I add a task with recurring interval "weekly" and due date "2026-02-15", **Then** the task is created with the recurrence interval stored and displayed.
2. **Given** a recurring daily task with due date "2026-02-15" exists, **When** I mark it complete, **Then** the task is reset to incomplete with due date changed to "2026-02-16".
3. **Given** a recurring weekly task with due date "2026-02-15" exists, **When** I mark it complete, **Then** the task is reset to incomplete with due date changed to "2026-02-22".
4. **Given** a recurring monthly task with due date "2026-02-15" exists, **When** I mark it complete, **Then** the task is reset to incomplete with due date changed to "2026-03-15".
5. **Given** a non-recurring task exists, **When** I mark it complete, **Then** it remains completed with no rescheduling (standard toggle behavior).
6. **Given** a task exists, **When** I add an invalid recurrence interval (e.g., "biweekly"), **Then** an error message is displayed listing valid intervals.
7. **Given** a recurring task exists, **When** I update it to remove the recurrence interval, **Then** the task becomes non-recurring and behaves normally on completion.

---

### User Story 4 - Enhanced Display with Due Dates and Recurrence (Priority: P2)

As a user, I want the task list view to show due dates, recurrence intervals, and alert indicators so I have a complete picture of my tasks.

**Why this priority**: The display must surface all new Advanced fields to make them useful. Without visible due dates and recurrence info, users cannot act on them.

**Independent Test**: Can be tested by adding tasks with various due dates and recurrence settings, then viewing the list and verifying all columns render correctly.

**Acceptance Scenarios**:

1. **Given** tasks exist with due dates and recurrence, **When** I view the task list, **Then** the table includes columns for Due Date, Recurrence, and Alert alongside existing columns.
2. **Given** a task has no due date, **When** I view the task list, **Then** the Due Date column shows "-".
3. **Given** a task has no recurrence, **When** I view the task list, **Then** the Recurrence column shows "-".
4. **Given** a task is overdue, **When** I view the task list, **Then** the Alert column shows "OVERDUE".
5. **Given** a task is due within 24 hours, **When** I view the task list, **Then** the Alert column shows "DUE SOON".

---

### User Story 5 - JSON Persistence (Priority: P3)

As a user, I want to optionally save my tasks to a file and load them back so recurring tasks and due dates survive application restarts.

**Why this priority**: Persistence is valuable but optional. In-memory storage is sufficient for single sessions, and persistence adds complexity. Lower priority since Basic + Intermediate worked without it.

**Independent Test**: Can be tested by adding tasks, saving to file, restarting the app, loading from file, and verifying all task data (including priority, tags, due dates, recurrence) is restored.

**Acceptance Scenarios**:

1. **Given** tasks exist in memory, **When** I choose "Save Tasks", **Then** all tasks are written to a JSON file and a confirmation is displayed.
2. **Given** a valid JSON file exists, **When** I choose "Load Tasks" on app start or via menu, **Then** tasks are loaded into memory and available for use.
3. **Given** the JSON file does not exist, **When** I choose "Load Tasks", **Then** a friendly message is displayed ("No saved tasks found") and the app continues with empty storage.
4. **Given** the JSON file is corrupted or invalid, **When** I choose "Load Tasks", **Then** an error message is displayed and existing in-memory tasks are not affected.
5. **Given** tasks with all fields (priority, tags, due date, recurrence) exist, **When** I save and reload, **Then** all fields are faithfully preserved.

---

### Edge Cases

- What happens when a recurring monthly task is due on Jan 31 and the next month has fewer days (e.g., Feb)? The due date should advance to the last day of the next month (Feb 28/29).
- What happens when a user enters a due date in the past? The task is created with the past due date and immediately shown as "OVERDUE".
- What happens when a recurring task is marked complete multiple times quickly? Each completion advances the due date by one interval.
- What happens when a task has a recurrence interval but no due date? The recurrence is stored but has no effect until a due date is set.
- What happens when the user enters just a date with no time (e.g., "2026-03-01")? The time defaults to 23:59 (end of day).
- What happens when saving to JSON with an empty task list? A valid JSON file is written containing an empty list.
- What happens when a completed non-recurring task has an overdue due date? No alert is shown (completed tasks are not flagged).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support setting an optional due date and time on each task
- **FR-002**: System MUST accept due dates in ISO format ("YYYY-MM-DD" or "YYYY-MM-DD HH:MM")
- **FR-003**: System MUST accept natural date shortcuts: "today" and "tomorrow", optionally followed by a time ("HH:MM")
- **FR-004**: System MUST default to 23:59 when a due date is provided without a time
- **FR-005**: System MUST reject invalid date formats with a clear error message
- **FR-006**: System MUST display an "OVERDUE" indicator for incomplete tasks whose due date has passed
- **FR-007**: System MUST display a "DUE SOON" indicator for incomplete tasks due within 24 hours
- **FR-008**: System MUST display a startup alert summary showing counts of overdue and due-soon tasks
- **FR-009**: System MUST NOT flag completed tasks as overdue or due soon
- **FR-010**: System MUST support three recurring intervals: "daily", "weekly", "monthly"
- **FR-011**: System MUST reject invalid recurrence intervals with a clear error message listing valid options
- **FR-012**: System MUST auto-reschedule recurring tasks when marked complete: reset to incomplete, advance due date by the interval
- **FR-013**: System MUST correctly handle month-end edge cases for monthly recurrence (e.g., Jan 31 → Feb 28)
- **FR-014**: System MUST allow removing recurrence from a task via update by typing "none" (empty Enter keeps current value)
- **FR-015**: System MUST display due date, recurrence interval, and alert status in the task list view
- **FR-016**: System MUST allow updating a task's due date and recurrence interval after creation (type "none" to clear, empty Enter to keep current)
- **FR-017**: System MUST optionally save all tasks to a fixed file (`tasks.json`) in the current working directory on user command
- **FR-018**: System MUST optionally load tasks from `tasks.json` in the current working directory on user command
- **FR-019**: System MUST handle missing or corrupted JSON files gracefully without crashing
- **FR-020**: System MUST preserve all task fields (including priority, tags, due date, recurrence) during save/load
- **FR-021**: System MUST preserve all existing Basic and Intermediate features without breaking changes

### Key Entities

- **Task** (updated): Represents a todo item. Existing attributes plus: optional due date/time, optional recurrence interval (daily/weekly/monthly). A task may have a due date, a recurrence interval, both, or neither.
- **RecurrenceInterval**: Represents how often a task repeats. Values: daily, weekly, monthly. Used to calculate the next due date when a recurring task is completed.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a task with a due date in a single command and see confirmation within 1 second
- **SC-002**: Overdue tasks are correctly flagged with 100% accuracy when viewed
- **SC-003**: Due-soon tasks (within 24 hours) are correctly flagged with 100% accuracy when viewed
- **SC-004**: Recurring tasks auto-reschedule with the correct next due date 100% of the time when marked complete
- **SC-005**: Startup alerts accurately report the count of overdue and due-soon tasks
- **SC-006**: All 10 Basic + Intermediate features continue to work identically to their previous behavior
- **SC-007**: Save and load preserves all task data with zero data loss across application restarts
- **SC-008**: Invalid inputs (bad dates, invalid intervals, corrupted files) produce clear error messages without crashing
- **SC-009**: 100% of user interactions complete without unhandled exceptions
