# Data Model: Advanced Todo Features

**Branch**: `003-todo-advanced` | **Date**: 2026-02-16

## Entities

### RecurrenceInterval (Enum) — NEW

| Member  | Value     | Description                    |
|---------|-----------|--------------------------------|
| DAILY   | "daily"   | Task recurs every day          |
| WEEKLY  | "weekly"  | Task recurs every 7 days       |
| MONTHLY | "monthly" | Task recurs every calendar month |

**Notes**:
- String values for clean display and JSON serialization
- Validation via `RecurrenceInterval(value)` — raises `ValueError` on invalid input
- Display: `interval.value` → `"daily"`, `"weekly"`, `"monthly"`

### Task (Dataclass) — UPDATED

| Field       | Type                         | Default           | Description                          | Change   |
|-------------|------------------------------|-------------------|--------------------------------------|----------|
| id          | int                          | (required)        | Unique auto-incrementing identifier  | existing |
| title       | str                          | (required)        | Task title, non-empty                | existing |
| description | Optional[str]                | ""                | Task description                     | existing |
| completed   | bool                         | False             | Completion status                    | existing |
| priority    | Priority                     | Priority.MEDIUM   | Task priority level                  | existing |
| tags        | list[str]                    | [] (factory)      | Lowercase, deduplicated tag list     | existing |
| created_at  | datetime                     | now() (factory)   | Creation timestamp                   | existing |
| due_date    | Optional[datetime]           | None              | Optional due date/time               | **NEW**  |
| recurrence  | Optional[RecurrenceInterval] | None              | Optional recurrence interval         | **NEW**  |

**Validation Rules** (additions):
- `due_date`: `None` (no due date) or a valid `datetime` instance
- `recurrence`: `None` (non-recurring) or a valid `RecurrenceInterval` member
- A task may have `due_date` only, `recurrence` only, both, or neither
- Recurrence without a due date is stored but has no scheduling effect

**State Transitions** (additions):
- `due_date`: None → datetime → None (set/update/clear via "none")
- `recurrence`: None → RecurrenceInterval → None (set/update/clear via "none")
- On completion of recurring task with due_date: `completed` → False, `due_date` += interval

### Helper Functions — NEW

#### parse_due_date(raw: str) -> datetime

| Parameter   | Type | Description                                     |
|-------------|------|-------------------------------------------------|
| raw         | str  | Raw date input string                           |
| **Returns** | datetime | Parsed datetime object                      |
| **Raises**  | ValueError | If format is invalid                       |

**Accepted formats**:
- `"YYYY-MM-DD"` → date at 23:59
- `"YYYY-MM-DD HH:MM"` → date at specified time
- `"today"` → today at 23:59
- `"today HH:MM"` → today at specified time
- `"tomorrow"` → tomorrow at 23:59
- `"tomorrow HH:MM"` → tomorrow at specified time

**Processing**: Normalize to lowercase → check for "today"/"tomorrow" prefix → parse remaining time or default to 23:59 → construct datetime

#### advance_due_date(due_date: datetime, interval: RecurrenceInterval) -> datetime

| Parameter   | Type                | Description                              |
|-------------|---------------------|------------------------------------------|
| due_date    | datetime            | Current due date                         |
| interval    | RecurrenceInterval  | Interval to advance by                   |
| **Returns** | datetime            | New due date advanced by one interval    |

**Logic**:
- DAILY: `due_date + timedelta(days=1)`
- WEEKLY: `due_date + timedelta(weeks=1)`
- MONTHLY: Increment month (handle year rollover), clamp day to last day of target month using `calendar.monthrange()`

#### get_alert_status(task: Task) -> Optional[str]

| Parameter   | Type          | Description                                        |
|-------------|---------------|----------------------------------------------------|
| task        | Task          | Task to evaluate                                   |
| **Returns** | Optional[str] | `"OVERDUE"`, `"DUE SOON"`, or `None`              |

**Logic**:
- If `task.completed` or `task.due_date is None` → `None`
- If `task.due_date < datetime.now()` → `"OVERDUE"`
- If `task.due_date - datetime.now() <= timedelta(hours=24)` → `"DUE SOON"`
- Otherwise → `None`

## Relationships

```text
Priority (enum) ──── used by ───→ Task.priority (1:1)              [existing]
RecurrenceInterval (enum) ── used by ──→ Task.recurrence (0..1:1)  [NEW]
Task.tags ──── list of ───→ str (1:many, inline)                   [existing]
Task.due_date ──── optional ───→ datetime (0..1:1)                 [NEW]
InMemoryStorage.tasks ──── dict of ───→ Task (1:many, keyed by id) [existing]
```

## Storage Interface Changes

| Method           | Change  | New Signature                                                    |
|------------------|---------|------------------------------------------------------------------|
| add_task         | UPDATED | `add_task(title, description, priority, tags, due_date, recurrence) → int` |
| update_task      | UPDATED | `update_task(task_id, title, description, priority, tags, due_date, recurrence) → None` |
| toggle_complete  | UPDATED | `toggle_complete(task_id) → None` (handles recurring reschedule) |
| save_to_json     | NEW     | `save_to_json(filepath: str) → None`                            |
| load_from_json   | NEW     | `load_from_json(filepath: str) → None`                          |

## JSON Persistence Schema

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, bread, eggs",
      "completed": false,
      "priority": "medium",
      "tags": ["shopping", "errands"],
      "created_at": "2026-02-16T10:30:00",
      "due_date": "2026-02-17T23:59:00",
      "recurrence": "weekly"
    }
  ],
  "next_id": 2
}
```

**Serialization rules**:
- `Priority` → `.name.lower()` (e.g., `"medium"`)
- `RecurrenceInterval` → `.value` or `null` (e.g., `"weekly"`)
- `datetime` → `.isoformat()` (e.g., `"2026-02-16T23:59:00"`)
- `None` fields → `null` in JSON

**Deserialization rules**:
- `"priority"` → `Priority[value.upper()]`
- `"recurrence"` → `RecurrenceInterval(value)` if not `null`, else `None`
- `"due_date"` → `datetime.fromisoformat(value)` if not `null`, else `None`
- `"created_at"` → `datetime.fromisoformat(value)`
