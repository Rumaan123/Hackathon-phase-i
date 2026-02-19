# Quickstart: Intermediate Todo Features

**Branch**: `002-todo-intermediate` | **Date**: 2026-02-15

## Prerequisites

- Python 3.13+
- UV package manager

## Setup

```bash
# Clone and checkout branch
git checkout 002-todo-intermediate

# Create virtual environment with UV
uv venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install in development mode
uv pip install -e .
```

## Running the App

```bash
cd src
python main.py
```

## New Commands (Intermediate Level)

The app menu now includes:

```
1. Add Task          (updated: prompts for priority and tags)
2. Delete Task
3. Update Task       (updated: prompts for priority and tags)
4. View Task List    (updated: shows priority and tags columns)
5. Mark Complete/Incomplete
6. Search Tasks      (NEW)
7. Filter Tasks      (NEW)
8. Sort Tasks        (NEW)
9. Quit
```

## Example Session

```
> 1 (Add Task)
Enter task title: Buy groceries
Enter task description: Weekly shopping
Enter priority (high/medium/low, default=medium): high
Enter tags (comma-separated, or press Enter to skip): shopping,errands

Task added with ID: 1

> 4 (View)
ID | Title          | Description      | Priority | Tags              | Status
---|----------------|------------------|----------|-------------------|-------
1  | Buy groceries  | Weekly shopping  | high     | shopping,errands  | [ ]

> 6 (Search)
Enter search keyword: shop
Results:
ID | Title          | Description      | Priority | Tags              | Status
1  | Buy groceries  | Weekly shopping  | high     | shopping,errands  | [ ]

> 7 (Filter)
Filter by (status/priority/tag): priority
Enter value: high
Results:
ID | Title          | Description      | Priority | Tags              | Status
1  | Buy groceries  | Weekly shopping  | high     | shopping,errands  | [ ]
```

## Running Tests

```bash
pytest test_app.py -v
```

## Files Modified

| File | Changes |
|------|---------|
| `src/models.py` | Added Priority enum, parse_tags(), updated Task with priority/tags/created_at |
| `src/storage.py` | Updated add/update, added search/filter/sort methods |
| `src/cli.py` | Updated add/update/view, added search/filter/sort methods |
| `src/main.py` | Added menu options 6-8, updated add/update prompts |
