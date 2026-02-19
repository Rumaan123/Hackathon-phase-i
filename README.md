# Evolution of Todo - Console Application

A progressive, three-level console todo application built with Python 3.13+ using only standard library modules. Each level builds on the previous, evolving from a basic task manager to an intelligent scheduling tool with persistence.

## Feature Levels

### Basic Level
- Add new tasks with title and description
- Delete tasks by ID
- Update existing tasks
- View all tasks in a formatted table
- Mark tasks as complete/incomplete

### Intermediate Level
- Priority assignment (high/medium/low)
- Tags and categories (comma-separated, auto-deduplicated)
- Keyword search across title, description, and tags
- Filter by status, priority, or tag
- Sort by priority, title, or creation date

### Advanced Level
- Due dates with natural language input ("today", "tomorrow", "2026-03-01 15:00")
- Overdue and due-soon alerts (OVERDUE / DUE SOON indicators)
- Startup alert summary for pending deadlines
- Recurring tasks (daily/weekly/monthly) with auto-rescheduling on completion
- Monthly edge-case handling (Jan 31 -> Feb 28)
- JSON persistence (save/load tasks to `tasks.json`)
- Enhanced 9-column display with all fields

## Requirements

- Python 3.13+
- UV (for virtual environment management, optional)

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rumaan123/Hackathon-phase-i.git
   cd Hackathon-phase-i
   ```

2. **Create and activate virtual environment** (optional):
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Run the application**:
   ```bash
   cd src
   python main.py
   ```

## Usage

### Interactive Menu

```
Welcome to the Todo App!

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Search Tasks
7. Filter Tasks
8. Sort Tasks
9. Save Tasks to File
10. Load Tasks from File
11. Quit
```

### Adding a Task

```
Enter your choice: 1
Enter task title: Buy groceries
Enter task description: Milk, bread, eggs
Enter priority (high/medium/low, default=medium): high
Enter tags (comma-separated, or press Enter to skip): shopping, errands
Enter due date (YYYY-MM-DD, today, tomorrow, or Enter to skip): tomorrow
Enter recurrence (daily/weekly/monthly, or Enter to skip): weekly
Task added with ID: 1
```

### Viewing Tasks (Enhanced Display)

```
ID   | Title                | Description          | Due Date            | Recurrence | Alert    | Priority | Tags            | Status
-----+----------------------+----------------------+---------------------+------------+----------+----------+-----------------+-------
1    | Buy groceries        | Milk, bread, eggs    | 2026-02-17 23:59    | weekly     | DUE SOON | high     | shopping,erran  | [ ]
2    | Write report         | Q4 quarterly report  | 2026-02-14 23:59    | -          | OVERDUE  | medium   | work            | [ ]
3    | Read book            | -                    | 2026-03-01 23:59    | -          | -        | low      | -               | [ ]
```

### Due Date Formats

| Format | Example | Result |
|--------|---------|--------|
| ISO date | `2026-03-01` | March 1, 2026 at 23:59 |
| ISO date + time | `2026-03-01 15:00` | March 1, 2026 at 15:00 |
| Today | `today` | Today at 23:59 |
| Today + time | `today 14:30` | Today at 14:30 |
| Tomorrow | `tomorrow` | Tomorrow at 23:59 |
| Tomorrow + time | `tomorrow 09:00` | Tomorrow at 09:00 |

### Recurring Tasks

When a recurring task is marked complete, it automatically resets:
- Status changes back to incomplete
- Due date advances by the interval (daily/weekly/monthly)

```
Enter your choice: 5
Enter task ID to mark: 1
Recurring task rescheduled. New due date: 2026-02-24 23:59
```

### Updating Tasks

```
Enter your choice: 3
Enter task ID to update: 1
Enter new title (or press Enter to keep current):
Enter new description (or press Enter to keep current):
Enter new priority (high/medium/low, or press Enter to keep current):
Enter new tags (comma-separated, or press Enter to keep current):
Enter new due date (or Enter to keep, 'none' to clear): none
Enter new recurrence (daily/weekly/monthly, Enter to keep, 'none' to clear):
Task 1 updated successfully
```

### Searching, Filtering, and Sorting

```
# Search across title, description, and tags
Enter your choice: 6
Enter search keyword: groceries

# Filter by status, priority, or tag
Enter your choice: 7
Filter by (status/priority/tag): priority
Enter value: high

# Sort by priority, title, or date
Enter your choice: 8
Sort by (priority/title/date): priority
```

### Save and Load (JSON Persistence)

```
# Save all tasks to tasks.json
Enter your choice: 9
Tasks saved to tasks.json (3 tasks)

# Load tasks from tasks.json (on next app start or anytime)
Enter your choice: 10
Loaded 3 tasks from tasks.json
```

### Startup Alerts

When the app starts with overdue or upcoming tasks:

```
Welcome to the Todo App!
Alert: You have 2 overdue tasks and 1 due soon
```

## Error Handling

The application handles errors gracefully:

- **Empty title**: Prevents adding/updating with empty titles
- **Invalid task ID**: Shows error for non-existent IDs
- **Non-numeric ID**: Validates that IDs are integers
- **Invalid date format**: Clear error with accepted formats
- **Invalid recurrence**: Error listing valid options (daily, weekly, monthly)
- **Invalid priority**: Error listing valid options (high, medium, low)
- **Missing JSON file**: Friendly "No saved tasks found" message
- **Corrupted JSON file**: Error message, existing tasks unchanged
- **Invalid menu choice**: Displays error for unrecognized options

## Project Structure

```
hackathon-ii/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── models.py         # Task dataclass, Priority/RecurrenceInterval enums,
│   │                     # parse_due_date, advance_due_date, get_alert_status
│   ├── storage.py        # InMemoryStorage: CRUD, search, filter, sort,
│   │                     # save/load JSON, recurring task rescheduling
│   ├── cli.py            # CLI: commands, display, alerts, save/load
│   └── main.py           # Main menu loop with 11 options
├── specs/
│   ├── basic-todo/       # Basic level spec, plan, tasks
│   ├── 001-todo-intermediate-features/  # Initial intermediate spec
│   ├── 002-todo-intermediate/           # Intermediate spec, plan, tasks, research
│   └── 003-todo-advanced/              # Advanced spec, plan, tasks, research, data-model
├── history/
│   └── prompts/          # Prompt History Records (PHRs)
├── .specify/             # SpecKit Plus templates and scripts
├── test_app.py           # Manual test script
├── requirements.txt      # Python dependencies
├── setup.py              # Package setup
└── README.md             # This file
```

## Architecture

```
main.py (menu loop)
    └── cli.py (command handlers, display formatting)
        └── storage.py (data operations, persistence)
            └── models.py (data model, enums, helpers)
```

- **models.py**: `Task` dataclass (9 fields), `Priority` enum, `RecurrenceInterval` enum, helper functions for date parsing, due date advancement, and alert classification
- **storage.py**: `InMemoryStorage` class with 12 methods — CRUD, search, filter, sort, toggle (with recurring reschedule), JSON save/load
- **cli.py**: `CLI` class with 13 methods — all user-facing commands, table display, startup alerts
- **main.py**: Interactive menu loop with 11 options and startup alert integration

## Technical Details

| Aspect | Details |
|--------|---------|
| **Language** | Python 3.13+ |
| **Dependencies** | Standard library only (`dataclasses`, `datetime`, `calendar`, `json`, `enum`, `typing`) |
| **Storage** | In-memory `Dict[int, Task]` + optional JSON file persistence |
| **ID Generation** | Auto-incrementing integers starting from 1 |
| **Code Quality** | PEP 8 compliant, type hints, comprehensive docstrings, robust error handling |
| **Development** | Spec-Driven Development (SDD) using SpecKit Plus |

## Development Methodology

This project follows **Spec-Driven Development** with AI agents:

1. **Constitution** defines project principles and constraints
2. **Specification** (`/sp.specify`) captures user stories and requirements
3. **Planning** (`/sp.plan`) designs architecture and makes technical decisions
4. **Task Generation** (`/sp.tasks`) breaks work into executable tasks
5. **Implementation** (`/sp.implement`) executes tasks phase by phase

All development is fully traced with Prompt History Records (PHRs) in `history/prompts/`.

## License

This project is part of the Evolution of Todo hackathon.
