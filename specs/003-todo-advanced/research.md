# Research: Advanced Todo Features

**Branch**: `003-todo-advanced` | **Date**: 2026-02-16

## R1: Date Parsing — Natural Language Shortcuts

**Decision**: Custom parser supporting ISO format ("YYYY-MM-DD", "YYYY-MM-DD HH:MM") and shortcuts ("today", "tomorrow") with optional "HH:MM" suffix
**Rationale**: Python's `datetime.strptime()` handles ISO format directly. For "today"/"tomorrow", we compute `datetime.now().date()` + `timedelta(days=0|1)` and append the time component. A dedicated `parse_due_date(raw: str) -> datetime` function in `models.py` centralizes this logic. When no time is given, default to 23:59.
**Alternatives considered**:
- `dateutil.parser.parse()` — rejected: external dependency violates constitution (stdlib only)
- `datetime.fromisoformat()` — partially usable for ISO strings, but doesn't handle "today"/"tomorrow" or the default-time-to-23:59 rule; custom wrapper still needed

## R2: Due Date Alert Classification

**Decision**: Compute alert status at display time using datetime comparison
**Rationale**: Instead of storing alert status, compute it dynamically:
- `OVERDUE`: `task.due_date < datetime.now()` and `not task.completed`
- `DUE SOON`: `task.due_date - datetime.now() <= timedelta(hours=24)` and `not task.completed`
- No alert: all other cases, or completed tasks
This avoids state staleness and keeps the model simple.
**Alternatives considered**:
- Storing alert status as a field — rejected: becomes stale if not updated constantly
- Background thread for real-time checks — rejected: spec explicitly says passive console alerts only

## R3: Recurring Task Rescheduling

**Decision**: On completion of a recurring task, reset `completed = False` and advance `due_date` by the interval
**Rationale**: Use `dateutil.relativedelta` — wait, that's external. Instead, implement interval advancement manually:
- **Daily**: `due_date + timedelta(days=1)`
- **Weekly**: `due_date + timedelta(weeks=1)`
- **Monthly**: Custom logic using `calendar.monthrange()` to handle month-end edge cases (Jan 31 → Feb 28/29)
Python's `calendar` module is stdlib and provides `monthrange(year, month)` to determine the last day of a month.
**Alternatives considered**:
- `dateutil.relativedelta(months=1)` — rejected: external dependency
- Simple `timedelta(days=30)` for monthly — rejected: inaccurate (months vary 28-31 days)

## R4: Monthly Recurrence Edge Cases

**Decision**: When advancing by one month, clamp to last day of target month if the original day exceeds it
**Rationale**: Using `calendar.monthrange(year, month)[1]` gives the last day. Algorithm: increment month (handle year rollover when month > 12), then clamp day to `min(original_day, last_day_of_new_month)`. Example: Jan 31 → Feb 28 (non-leap) or Feb 29 (leap).
**Alternatives considered**:
- Skip to next month's first day — rejected: unintuitive for users
- Error/warning — rejected: silent clamping is standard calendar behavior

## R5: RecurrenceInterval Implementation

**Decision**: Use `enum.Enum` with string values for display and validation
**Rationale**: Similar to `Priority`, an Enum provides type safety and easy validation. Values: `DAILY = "daily"`, `WEEKLY = "weekly"`, `MONTHLY = "monthly"`. Use `RecurrenceInterval(value)` for string-to-enum conversion. Display via `.value` for lowercase output.
**Alternatives considered**:
- Plain strings — rejected: no type safety, validation scattered
- `IntEnum` with day counts — rejected: monthly is not a fixed day count

## R6: JSON Persistence Format

**Decision**: Serialize tasks to a list of dicts in `tasks.json` using `json` module (stdlib)
**Rationale**: Each task is serialized to a dict with all fields. Special handling needed for:
- `Priority` enum → store as string (`"high"`, `"medium"`, `"low"`)
- `RecurrenceInterval` enum → store as string or `null`
- `datetime` → store as ISO string (`isoformat()`)
- On load, reverse the conversions
The `json` module with a custom encoder/decoder handles this cleanly.
**Alternatives considered**:
- `pickle` — rejected: binary format, not human-readable, security concerns
- `shelve` — rejected: overkill for a single list of tasks
- `sqlite3` — rejected: unnecessary complexity for simple flat storage

## R7: Startup Alert Summary

**Decision**: Compute overdue and due-soon counts at app start and print a summary
**Rationale**: On startup (in `main.py`), iterate all tasks, classify alerts using the same logic as the display, and print: "You have X overdue tasks and Y due soon." Only print if X > 0 or Y > 0. This requires the storage to be populated first (relevant when loading from JSON).
**Alternatives considered**:
- Always print (even when 0/0) — rejected: noisy for no benefit
- Print per-task alerts on startup — rejected: too verbose; summary is cleaner
