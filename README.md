# Basic Level Console Todo Application

A minimal, in-memory, command-line todo application that implements core task management functionality. This MVP follows clean Python code standards using only Python standard library components.

## Features

- ✅ Add new tasks with title and description
- ✅ Delete tasks by ID
- ✅ Update existing tasks
- ✅ View all tasks in a formatted list
- ✅ Mark tasks as complete/incomplete

## Requirements

- Python 3.13+
- UV (for virtual environment management)

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hackathon-ii
   ```

2. **Create and activate virtual environment** (optional but recommended):
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

When you run the application, you'll see a numbered menu with the following options:

```
Welcome to the Todo App!

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
```

### Command Syntax

#### 1. Add Task
- Select option `1` from the menu
- Enter task title when prompted
- Enter task description when prompted
- System assigns a unique ID and confirms addition

#### 2. Delete Task
- Select option `2` from the menu
- Enter the task ID to delete
- System confirms deletion or shows error if ID doesn't exist

#### 3. Update Task
- Select option `3` from the menu
- Enter the task ID to update
- Enter new title (or press Enter to keep current)
- Enter new description (or press Enter to keep current)
- System confirms update

#### 4. View Task List
- Select option `4` from the menu
- System displays all tasks in a formatted table:
  - ID | Title | Description | Status
  - Status shows `[ ]` for incomplete, `[x]` for complete
  - Long descriptions are truncated with "..."

#### 5. Mark Task Complete/Incomplete
- Select option `5` from the menu
- Enter the task ID to toggle
- System toggles completion status and shows updated status

#### 6. Quit
- Select option `6` to exit the application

## Sample Session

```
Welcome to the Todo App!

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
Enter your choice: 1
Enter task title: Buy groceries
Enter task description: Need to buy milk, bread, eggs
Task added with ID: 1

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
Enter your choice: 1
Enter task title: Write report
Enter task description: Complete quarterly report
Task added with ID: 2

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
Enter your choice: 4
ID | Title | Description | Status
1 | Buy groceries | Need to buy milk, bread, eggs | [ ]
2 | Write report | Complete quarterly report | [ ]

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
Enter your choice: 5
Enter task ID to mark: 1
Task 1 marked as complete. Status: [x]

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
Enter your choice: 4
ID | Title | Description | Status
1 | Buy groceries | Need to buy milk, bread, eggs | [x]
2 | Write report | Complete quarterly report | [ ]

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
Enter your choice: 3
Enter task ID to update: 2
Enter new title (or press Enter to keep current): Write quarterly report
Enter new description (or press Enter to keep current): Complete Q4 2026 report
Task 2 updated successfully

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
Enter your choice: 4
ID | Title | Description | Status
1 | Buy groceries | Need to buy milk, bread, eggs | [x]
2 | Write quarterly report | Complete Q4 2026 report | [ ]

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
Enter your choice: 2
Enter task ID to delete: 1
Task 1 deleted successfully

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
Enter your choice: 4
ID | Title | Description | Status
2 | Write quarterly report | Complete Q4 2026 report | [ ]

Options:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task Complete/Incomplete
6. Quit
Enter your choice: 6
Goodbye!
```

## Error Handling

The application handles various error scenarios gracefully:

- **Empty title**: Prevents adding/updating tasks with empty titles
- **Invalid task ID**: Shows error message when ID doesn't exist
- **Non-numeric ID**: Validates that IDs are numeric integers
- **Invalid menu choice**: Displays error for unrecognized options

## Project Structure

```
hackathon-ii/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── models.py         # Task dataclass definition
│   ├── storage.py        # In-memory storage implementation
│   ├── cli.py            # CLI command handlers
│   └── main.py           # Main application entry point
├── specs/
│   └── basic-todo/
│       ├── spec.md       # Feature specification
│       ├── plan_basic_console.md  # Implementation plan
│       └── tasks.md      # Task breakdown
└── README.md             # This file
```

## Architecture

The application follows a clean, modular architecture:

- **models.py**: Defines the Task dataclass with id, title, description, and completed fields
- **storage.py**: Implements InMemoryStorage class with CRUD operations
- **cli.py**: Handles user input, command parsing, and output formatting
- **main.py**: Provides the main application loop and menu interface

## Technical Details

- **Storage**: In-memory dictionary (Dict[int, Task])
- **ID Generation**: Auto-incrementing integers starting from 1
- **Data Persistence**: None (data is lost when application exits)
- **Dependencies**: Python standard library only
- **Code Quality**: PEP 8 compliant, type hints, comprehensive docstrings

## Future Enhancements

This Basic Level serves as a foundation for future levels:

- **Intermediate Level**: Priority assignment, tags/categories, search, filtering, sorting
- **Advanced Level**: Recurring tasks, due dates, reminders, browser notifications, file persistence

## License

This project is part of the Evolution of Todo hackathon.

## Contributing

This is a hackathon project following spec-driven development methodology. All development is conducted using AI agents and Spec-Kit Plus commands.