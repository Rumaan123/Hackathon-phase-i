import json
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from models import (Task, Priority, RecurrenceInterval,
                    parse_tags, parse_due_date, advance_due_date)


@dataclass
class InMemoryStorage:
    """In-memory storage for managing tasks."""

    def __init__(self) -> None:
        """Initialize storage with empty dictionary and task counter."""
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "",
                 priority: str = "medium", tags: str = "",
                 due_date: str = "", recurrence: str = "") -> int:
        """Add a new task to the storage.

        Args:
            title: Title of the task (required)
            description: Description of the task (optional)
            priority: Priority level as string - "high", "medium", or "low" (default: "medium")
            tags: Comma-separated tag string (optional)
            due_date: Due date string in supported format (optional)
            recurrence: Recurrence interval - "daily", "weekly", or "monthly" (optional)

        Returns:
            The unique ID assigned to the new task

        Raises:
            ValueError: If title is empty, priority is invalid, date format
                        is invalid, or recurrence interval is invalid
        """
        if not title:
            raise ValueError("Task title cannot be empty")

        try:
            priority_enum = Priority[priority.upper()]
        except KeyError:
            raise ValueError(
                f"Invalid priority '{priority}'. Valid options: high, medium, low"
            )

        parsed_tags = parse_tags(tags)

        parsed_due_date = None
        if due_date and due_date.strip():
            parsed_due_date = parse_due_date(due_date)

        parsed_recurrence = None
        if recurrence and recurrence.strip():
            try:
                parsed_recurrence = RecurrenceInterval(recurrence.strip().lower())
            except ValueError:
                raise ValueError(
                    f"Invalid recurrence '{recurrence}'. "
                    "Valid options: daily, weekly, monthly"
                )

        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False,
            priority=priority_enum,
            tags=parsed_tags,
            due_date=parsed_due_date,
            recurrence=parsed_recurrence,
        )

        self.tasks[self.next_id] = task
        self.next_id += 1

        return task.id

    def get_task_by_id(self, task_id: int) -> Task:
        """Retrieve a task by its unique ID.

        Args:
            task_id: The unique ID of the task to retrieve

        Returns:
            The Task object with the specified ID

        Raises:
            KeyError: If task with given ID does not exist
        """
        if task_id not in self.tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")

        return self.tasks[task_id]

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None,
                    priority: Optional[str] = None,
                    tags: Optional[str] = None,
                    due_date: Optional[str] = None,
                    recurrence: Optional[str] = None) -> None:
        """Update an existing task's fields.

        Args:
            task_id: The unique ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            priority: New priority as string (optional)
            tags: New comma-separated tag string (optional, replaces existing)
            due_date: New due date string, "none" to clear, None to keep (optional)
            recurrence: New recurrence interval, "none" to clear, None to keep (optional)

        Raises:
            KeyError: If task with given ID does not exist
            ValueError: If title is empty, priority/date/recurrence is invalid
        """
        task = self.get_task_by_id(task_id)

        if title is not None:
            if not title:
                raise ValueError("Task title cannot be empty")
            task.title = title

        if description is not None:
            task.description = description

        if priority is not None:
            try:
                task.priority = Priority[priority.upper()]
            except KeyError:
                raise ValueError(
                    f"Invalid priority '{priority}'. Valid options: high, medium, low"
                )

        if tags is not None:
            task.tags = parse_tags(tags)

        if due_date is not None:
            if due_date.strip().lower() == "none":
                task.due_date = None
            elif due_date.strip():
                task.due_date = parse_due_date(due_date)

        if recurrence is not None:
            if recurrence.strip().lower() == "none":
                task.recurrence = None
            elif recurrence.strip():
                try:
                    task.recurrence = RecurrenceInterval(
                        recurrence.strip().lower()
                    )
                except ValueError:
                    raise ValueError(
                        f"Invalid recurrence '{recurrence}'. "
                        "Valid options: daily, weekly, monthly"
                    )

    def delete_task(self, task_id: int) -> None:
        """Delete a task by its unique ID.

        Args:
            task_id: The unique ID of the task to delete

        Raises:
            KeyError: If task with given ID does not exist
        """
        if task_id not in self.tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")

        del self.tasks[task_id]

    def list_all_tasks(self) -> list[Task]:
        """Retrieve all tasks in the storage.

        Returns:
            List of all Task objects
        """
        return list(self.tasks.values())

    def toggle_complete(self, task_id: int) -> bool:
        """Toggle the completion status of a task.

        For recurring tasks with a due date, completing the task resets it
        to incomplete and advances the due date by the recurrence interval.

        Args:
            task_id: The unique ID of the task to toggle

        Returns:
            True if a recurring task was rescheduled, False for normal toggle

        Raises:
            KeyError: If task with given ID does not exist
        """
        task = self.get_task_by_id(task_id)
        task.completed = not task.completed

        # Handle recurring task rescheduling
        if (task.completed and task.recurrence is not None
                and task.due_date is not None):
            task.completed = False
            task.due_date = advance_due_date(task.due_date, task.recurrence)
            return True

        return False

    def search_tasks(self, keyword: str) -> list[Task]:
        """Search tasks by keyword across title, description, and tags.

        Performs case-insensitive substring matching.

        Args:
            keyword: Search keyword (non-empty string)

        Returns:
            List of tasks matching the keyword
        """
        keyword_lower = keyword.lower()
        return [
            task for task in self.tasks.values()
            if keyword_lower in task.title.lower()
            or keyword_lower in (task.description or "").lower()
            or any(keyword_lower in tag for tag in task.tags)
        ]

    def filter_tasks(self, filter_type: str, value: str) -> list[Task]:
        """Filter tasks by a single criterion.

        Args:
            filter_type: One of "status", "priority", or "tag"
            value: The value to filter by

        Returns:
            List of tasks matching the filter

        Raises:
            ValueError: If filter_type is invalid or value is invalid for the type
        """
        if filter_type == "status":
            if value.lower() == "completed":
                return [t for t in self.tasks.values() if t.completed]
            elif value.lower() == "incomplete":
                return [t for t in self.tasks.values() if not t.completed]
            else:
                raise ValueError(
                    f"Invalid status '{value}'. Valid options: completed, incomplete"
                )
        elif filter_type == "priority":
            try:
                priority_enum = Priority[value.upper()]
            except KeyError:
                raise ValueError(
                    f"Invalid priority '{value}'. Valid options: high, medium, low"
                )
            return [t for t in self.tasks.values() if t.priority == priority_enum]
        elif filter_type == "tag":
            value_lower = value.lower()
            return [t for t in self.tasks.values() if value_lower in t.tags]
        else:
            raise ValueError(
                f"Invalid filter type '{filter_type}'. Valid options: status, priority, tag"
            )

    def sort_tasks(self, criterion: str) -> list[Task]:
        """Sort all tasks by a given criterion.

        Args:
            criterion: One of "priority", "title", or "date"

        Returns:
            List of all tasks sorted by the criterion

        Raises:
            ValueError: If criterion is invalid
        """
        all_tasks = list(self.tasks.values())
        if criterion == "priority":
            return sorted(all_tasks, key=lambda t: t.priority.value)
        elif criterion == "title":
            return sorted(all_tasks, key=lambda t: t.title.lower())
        elif criterion == "date":
            return sorted(all_tasks, key=lambda t: t.created_at)
        else:
            raise ValueError(
                f"Invalid sort criterion '{criterion}'. Valid options: priority, title, date"
            )

    def save_to_json(self, filepath: str) -> None:
        """Save all tasks to a JSON file.

        Args:
            filepath: Path to the JSON file to write

        Serializes each task to a dict with type-specific conversions:
        - Priority → name lowercase string
        - RecurrenceInterval → value string or null
        - datetime → ISO format string or null
        """
        tasks_data = []
        for task in self.tasks.values():
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority.name.lower(),
                "tags": task.tags,
                "created_at": task.created_at.isoformat(),
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "recurrence": task.recurrence.value if task.recurrence else None,
            }
            tasks_data.append(task_dict)

        data = {
            "tasks": tasks_data,
            "next_id": self.next_id,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_from_json(self, filepath: str) -> None:
        """Load tasks from a JSON file, replacing current storage.

        Args:
            filepath: Path to the JSON file to read

        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file contains invalid or corrupted data
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"No saved tasks found at '{filepath}'")
        except json.JSONDecodeError:
            raise ValueError(
                f"File '{filepath}' contains invalid JSON data"
            )

        try:
            loaded_tasks: Dict[int, Task] = {}
            for task_dict in data["tasks"]:
                due_date = None
                if task_dict.get("due_date"):
                    due_date = datetime.fromisoformat(task_dict["due_date"])

                recurrence = None
                if task_dict.get("recurrence"):
                    recurrence = RecurrenceInterval(task_dict["recurrence"])

                task = Task(
                    id=task_dict["id"],
                    title=task_dict["title"],
                    description=task_dict.get("description", ""),
                    completed=task_dict.get("completed", False),
                    priority=Priority[task_dict["priority"].upper()],
                    tags=task_dict.get("tags", []),
                    created_at=datetime.fromisoformat(task_dict["created_at"]),
                    due_date=due_date,
                    recurrence=recurrence,
                )
                loaded_tasks[task.id] = task

            # Only replace storage if all tasks loaded successfully
            self.tasks = loaded_tasks
            self.next_id = data.get("next_id", max(loaded_tasks.keys(), default=0) + 1)
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Corrupted task data in '{filepath}': {e}")
