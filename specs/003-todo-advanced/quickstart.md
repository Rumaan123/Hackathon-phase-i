# Quickstart: Advanced Todo Features

**Branch**: `003-todo-advanced` | **Date**: 2026-02-16

## Prerequisites

- Python 3.13+
- UV (for virtual environment management)
- Existing Basic + Intermediate todo app codebase

## Setup

```bash
# Clone and switch to branch
git checkout 003-todo-advanced

# Run the app
cd src
python main.py
```

## New Features

### Due Dates

When adding or updating a task, you'll be prompted for an optional due date:

```
Enter due date (YYYY-MM-DD, today, tomorrow, or press Enter to skip): 2026-03-01
Enter due date (YYYY-MM-DD, today, tomorrow, or press Enter to skip): tomorrow
Enter due date (YYYY-MM-DD HH:MM for specific time): today 14:30
```

### Recurrence

When adding or updating a task, you'll be prompted for an optional recurrence:

```
Enter recurrence (daily/weekly/monthly, or press Enter to skip): weekly
```

When a recurring task is marked complete, it automatically resets:
- Status changes back to incomplete
- Due date advances by the interval

### Alert Indicators

The task list view now shows alert status:

```
ID   | Title                | Due Date            | Recurrence | Alert    | Priority | Tags            | Status
-----+----------------------+---------------------+------------+----------+----------+-----------------+-------
1    | Buy groceries        | 2026-02-15 23:59    | weekly     | OVERDUE  | high     | shopping        | [ ]
2    | Write report         | 2026-02-17 14:00    | -          | DUE SOON | medium   | work            | [ ]
3    | Read book            | 2026-03-01 23:59    | -          | -        | low      | -               | [ ]
```

### Save/Load (JSON Persistence)

New menu options to save and load tasks:

```
10. Save Tasks to File
11. Load Tasks from File
```

Tasks are saved to `tasks.json` in the current working directory.

## File Structure

```
src/
├── main.py      # Entry point — updated menu with save/load + startup alerts
├── models.py    # Task dataclass — new due_date, recurrence fields + helper functions
├── storage.py   # InMemoryStorage — updated methods + save/load JSON
└── cli.py       # CLI class — updated display + new save/load commands
```
