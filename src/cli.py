from typing import Optional
from storage import InMemoryStorage
from models import Task, RecurrenceInterval, parse_due_date, get_alert_status


class CLI:
    """Command Line Interface for the Todo application."""

    def __init__(self, storage: InMemoryStorage) -> None:
        """Initialize CLI with storage instance."""
        self.storage = storage

    def add(self, title: str, description: Optional[str] = "",
            priority: str = "medium", tags: str = "",
            due_date: str = "", recurrence: str = "") -> None:
        """Add a new task through the CLI.

        Args:
            title: Title of the task
            description: Description of the task (optional)
            priority: Priority level - "high", "medium", or "low" (default: "medium")
            tags: Comma-separated tag string (optional)
            due_date: Due date string in supported format (optional)
            recurrence: Recurrence interval - "daily", "weekly", or "monthly" (optional)
        """
        try:
            task_id = self.storage.add_task(
                title, description, priority, tags, due_date, recurrence
            )
            print(f"Task added with ID: {task_id}")
        except ValueError as e:
            print(f"Error: {e}")

    def delete(self, task_id: int) -> None:
        """Delete a task by ID."""
        try:
            self.storage.delete_task(task_id)
            print(f"Task {task_id} deleted successfully")
        except KeyError as e:
            print(f"Error: {e}")

    def update(self, task_id: int, title: Optional[str] = None,
               description: Optional[str] = None,
               priority: Optional[str] = None,
               tags: Optional[str] = None,
               due_date: Optional[str] = None,
               recurrence: Optional[str] = None) -> None:
        """Update a task's fields.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            tags: New comma-separated tag string (optional)
            due_date: New due date string, "none" to clear (optional)
            recurrence: New recurrence interval, "none" to clear (optional)
        """
        try:
            self.storage.update_task(
                task_id, title, description, priority, tags,
                due_date, recurrence
            )
            print(f"Task {task_id} updated successfully")
        except (KeyError, ValueError) as e:
            print(f"Error: {e}")

    def _display_tasks(self, tasks: list[Task]) -> None:
        """Display a list of tasks in enhanced table format with all columns.

        Args:
            tasks: List of Task objects to display
        """
        print(
            f"{'ID':<4} | {'Title':<20} | {'Description':<20} | "
            f"{'Due Date':<19} | {'Recurrence':<10} | {'Alert':<8} | "
            f"{'Priority':<8} | {'Tags':<15} | {'Status':<6}"
        )
        print(
            f"{'-'*4}-+-{'-'*20}-+-{'-'*20}-+-"
            f"{'-'*19}-+-{'-'*10}-+-{'-'*8}-+-"
            f"{'-'*8}-+-{'-'*15}-+-{'-'*6}"
        )
        for task in tasks:
            status = "[x]" if task.completed else "[ ]"
            desc = (task.description or "")[:20]
            if len(task.description or "") > 20:
                desc = desc[:17] + "..."
            tags_str = ",".join(task.tags) if task.tags else "-"
            if len(tags_str) > 15:
                tags_str = tags_str[:12] + "..."
            priority_str = task.priority.name.lower()

            # Due date formatting
            if task.due_date:
                due_str = task.due_date.strftime("%Y-%m-%d %H:%M")
            else:
                due_str = "-"

            # Recurrence formatting
            if task.recurrence:
                rec_str = task.recurrence.value
            else:
                rec_str = "-"

            # Alert status
            alert = get_alert_status(task) or "-"

            print(
                f"{task.id:<4} | {task.title:<20} | {desc:<20} | "
                f"{due_str:<19} | {rec_str:<10} | {alert:<8} | "
                f"{priority_str:<8} | {tags_str:<15} | {status:<6}"
            )

    def view(self) -> None:
        """View all tasks in enhanced table format."""
        tasks = self.storage.list_all_tasks()

        if not tasks:
            print("No tasks exist")
            return

        self._display_tasks(tasks)

    def mark(self, task_id: int) -> None:
        """Toggle task completion status.

        For recurring tasks, prints a reschedule message instead of
        the standard completion toggle message.
        """
        try:
            rescheduled = self.storage.toggle_complete(task_id)
            task = self.storage.get_task_by_id(task_id)

            if rescheduled:
                due_str = task.due_date.strftime("%Y-%m-%d %H:%M")
                print(
                    f"Recurring task rescheduled. "
                    f"New due date: {due_str}"
                )
            else:
                status = "[x]" if task.completed else "[ ]"
                print(f"Task {task_id} marked as complete. Status: {status}")
        except KeyError as e:
            print(f"Error: {e}")

    def search(self, keyword: str) -> None:
        """Search tasks by keyword across title, description, and tags.

        Args:
            keyword: Search keyword (non-empty string)
        """
        if not keyword or not keyword.strip():
            print("Error: Please provide a search keyword")
            return

        results = self.storage.search_tasks(keyword.strip())

        if not results:
            print("No tasks match the search")
            return

        print(f"Search results for '{keyword.strip()}':")
        self._display_tasks(results)

    def filter_tasks(self, filter_type: str, value: str) -> None:
        """Filter tasks by a single criterion.

        Args:
            filter_type: One of "status", "priority", or "tag"
            value: The value to filter by
        """
        try:
            results = self.storage.filter_tasks(filter_type, value)
        except ValueError as e:
            print(f"Error: {e}")
            return

        if not results:
            print("No tasks match the filter")
            return

        print(f"Filter results ({filter_type}={value}):")
        self._display_tasks(results)

    def sort(self, criterion: str) -> None:
        """Sort and display all tasks by a given criterion.

        Args:
            criterion: One of "priority", "title", or "date"
        """
        tasks = self.storage.list_all_tasks()
        if not tasks:
            print("No tasks exist")
            return

        try:
            sorted_tasks = self.storage.sort_tasks(criterion)
        except ValueError as e:
            print(f"Error: {e}")
            return

        print(f"Tasks sorted by {criterion}:")
        self._display_tasks(sorted_tasks)

    def save_tasks(self) -> None:
        """Save all tasks to tasks.json file."""
        try:
            self.storage.save_to_json("tasks.json")
            count = len(self.storage.list_all_tasks())
            print(f"Tasks saved to tasks.json ({count} tasks)")
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self) -> None:
        """Load tasks from tasks.json file."""
        try:
            self.storage.load_from_json("tasks.json")
            count = len(self.storage.list_all_tasks())
            print(f"Loaded {count} tasks from tasks.json")
        except FileNotFoundError:
            print("No saved tasks found")
        except ValueError as e:
            print(f"Error loading tasks: {e}")

    def show_startup_alerts(self) -> None:
        """Display a summary of overdue and due-soon tasks on startup."""
        tasks = self.storage.list_all_tasks()
        overdue_count = 0
        due_soon_count = 0

        for task in tasks:
            alert = get_alert_status(task)
            if alert == "OVERDUE":
                overdue_count += 1
            elif alert == "DUE SOON":
                due_soon_count += 1

        if overdue_count > 0 or due_soon_count > 0:
            parts = []
            if overdue_count > 0:
                parts.append(f"{overdue_count} overdue task{'s' if overdue_count != 1 else ''}")
            if due_soon_count > 0:
                parts.append(f"{due_soon_count} due soon")
            print(f"Alert: You have {' and '.join(parts)}")

    def handle_command(self, command: str) -> bool:
        """Handle a single command.

        Args:
            command: The command string to process

        Returns:
            True if command was handled, False if unknown command
        """
        parts = command.strip().split(maxsplit=1)

        if not parts:
            return False

        cmd = parts[0].lower()

        if cmd == "add":
            if len(parts) < 2:
                print("Error: Missing title for add command")
                return True

            # Parse title and description from command
            rest = parts[1].strip()
            if rest.startswith('"'):
                # Parse quoted title
                title_parts = []
                current = rest
                while current:
                    if current.startswith('"'):
                        # Find closing quote
                        end_quote = current.find('"', 1)
                        if end_quote == -1:
                            # No closing quote, treat rest as title
                            title_parts.append(current[1:].strip())
                            break
                        else:
                            title_parts.append(current[1:end_quote].strip())
                            current = current[end_quote+1:].strip()
                            # Check for description after space
                            if current and current.startswith('"'):
                                desc_end = current.find('"', 1)
                                if desc_end == -1:
                                    description = current[1:].strip()
                                    current = ""
                                else:
                                    description = current[1:desc_end].strip()
                                    current = current[desc_end+1:].strip()
                            else:
                                description = ""
                            break
                    else:
                        # No quotes, split by first space
                        space_idx = current.find(' ')
                        if space_idx == -1:
                            title = current.strip()
                            description = ""
                            break
                        else:
                            title = current[:space_idx].strip()
                            description = current[space_idx+1:].strip()
                            break

                title = " ".join(title_parts)
            else:
                # No quotes, simple split
                space_idx = parts[1].find(' ')
                if space_idx == -1:
                    title = parts[1].strip()
                    description = ""
                else:
                    title = parts[1][:space_idx].strip()
                    description = parts[1][space_idx+1:].strip()

            self.add(title, description)
            return True

        elif cmd == "delete":
            if len(parts) < 2:
                print("Error: Missing task ID for delete command")
                return True

            try:
                task_id = int(parts[1])
                self.delete(task_id)
            except ValueError:
                print("Error: Task ID must be a number")
            return True

        elif cmd == "update":
            if len(parts) < 2:
                print("Error: Missing task ID for update command")
                return True

            try:
                task_id = int(parts[1])
                # Parse title and description from remaining parts
                rest = parts[1].strip()
                if len(parts) > 2:
                    rest = parts[2].strip()
                    if rest.startswith('"'):
                        # Parse quoted title
                        title_parts = []
                        current = rest
                        while current:
                            if current.startswith('"'):
                                end_quote = current.find('"', 1)
                                if end_quote == -1:
                                    title_parts.append(current[1:].strip())
                                    break
                                else:
                                    title_parts.append(current[1:end_quote].strip())
                                    current = current[end_quote+1:].strip()
                                    if current and current.startswith('"'):
                                        desc_end = current.find('"', 1)
                                        if desc_end == -1:
                                            description = current[1:].strip()
                                            current = ""
                                        else:
                                            description = current[1:desc_end].strip()
                                            current = current[desc_end+1:].strip()
                                    else:
                                        description = ""
                                    break
                            else:
                                space_idx = current.find(' ')
                                if space_idx == -1:
                                    title = current.strip()
                                    description = ""
                                    break
                                else:
                                    title = current[:space_idx].strip()
                                    description = current[space_idx+1].strip()
                                    break
                        title = " ".join(title_parts)
                    else:
                        space_idx = rest.find(' ')
                        if space_idx == -1:
                            title = rest.strip()
                            description = ""
                        else:
                            title = rest[:space_idx].strip()
                            description = rest[space_idx+1].strip()
                else:
                    title = None
                    description = None

                self.update(task_id, title, description)
            except ValueError:
                print("Error: Task ID must be a number")
            return True

        elif cmd == "view":
            self.view()
            return True

        elif cmd == "mark":
            if len(parts) < 2:
                print("Error: Missing task ID for mark command")
                return True

            try:
                task_id = int(parts[1])
                self.mark(task_id)
            except ValueError:
                print("Error: Task ID must be a number")
            return True

        elif cmd == "quit":
            print("Goodbye!")
            return False

        else:
            print(f"Unknown command: {cmd}")
            return True
