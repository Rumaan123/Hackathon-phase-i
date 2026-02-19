# Data Model: Intermediate Todo Features

**Branch**: `002-todo-intermediate` | **Date**: 2026-02-15

## Entities

### Priority (Enum)

| Member | Value | Description |
|--------|-------|-------------|
| HIGH   | 1     | High priority task |
| MEDIUM | 2     | Medium priority (default) |
| LOW    | 3     | Low priority task |

**Notes**:
- Integer values enable natural sort ordering (lower value = higher priority)
- String lookup via member name: `Priority["HIGH"]` or custom from-string method
- Display as lowercase string: `priority.name.lower()`

### Task (Dataclass)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| id | int | (required) | Unique auto-incrementing identifier |
| title | str | (required) | Task title, non-empty |
| description | Optional[str] | "" | Task description |
| completed | bool | False | Completion status |
| priority | Priority | Priority.MEDIUM | Task priority level |
| tags | list[str] | [] (factory) | Lowercase, deduplicated tag list |
| created_at | datetime | now() (factory) | Creation timestamp |

**Validation Rules**:
- `title` must be non-empty string
- `priority` must be a valid Priority enum member
- `tags` are normalized on input: trimmed, lowercased, empty strings removed, duplicates removed
- `id` is assigned by storage, not user-provided

**State Transitions**:
- `completed`: False → True → False (toggle via `toggle_complete`)
- `priority`: Any → Any (via `update_task`)
- `tags`: Any → Any (replaced entirely via `update_task`)

### Helper Function: parse_tags

| Parameter | Type | Description |
|-----------|------|-------------|
| raw | str | Raw comma-separated tag input |
| **Returns** | list[str] | Cleaned, normalized, deduplicated tag list |

**Processing pipeline**: split(",") → strip() → lower() → filter(bool) → deduplicate(preserve order)

## Relationships

```text
Priority (enum) ──── used by ───→ Task.priority (1:1)
Task.tags ──── list of ───→ str (1:many, inline)
InMemoryStorage.tasks ──── dict of ───→ Task (1:many, keyed by id)
```

## Storage Interface Changes

| Method | Change | New Signature |
|--------|--------|---------------|
| add_task | UPDATED | `add_task(title, description, priority, tags) → int` |
| update_task | UPDATED | `update_task(task_id, title, description, priority, tags) → None` |
| search_tasks | NEW | `search_tasks(keyword) → list[Task]` |
| filter_tasks | NEW | `filter_tasks(filter_type, value) → list[Task]` |
| sort_tasks | NEW | `sort_tasks(criterion) → list[Task]` |
