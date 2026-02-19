"""Main entry point for the Todo application."""

from storage import InMemoryStorage
from cli import CLI


def main() -> None:
    """Main application entry point."""
    storage = InMemoryStorage()
    cli = CLI(storage)

    print("Welcome to the Todo App!")
    cli.show_startup_alerts()

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Update Task")
        print("4. View Task List")
        print("5. Mark Task Complete/Incomplete")
        print("6. Search Tasks")
        print("7. Filter Tasks")
        print("8. Sort Tasks")
        print("9. Save Tasks to File")
        print("10. Load Tasks from File")
        print("11. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            title = input("Enter task title: ").strip()
            description = input("Enter task description: ").strip()
            priority = input("Enter priority (high/medium/low, default=medium): ").strip()
            tags = input("Enter tags (comma-separated, or press Enter to skip): ").strip()
            due_date = input("Enter due date (YYYY-MM-DD, today, tomorrow, or Enter to skip): ").strip()
            recurrence = input("Enter recurrence (daily/weekly/monthly, or Enter to skip): ").strip()
            cli.add(
                title, description,
                priority if priority else "medium",
                tags, due_date, recurrence
            )

        elif choice == "2":
            task_id_str = input("Enter task ID to delete: ").strip()
            try:
                task_id = int(task_id_str)
                cli.delete(task_id)
            except ValueError:
                print("Error: Task ID must be a number")

        elif choice == "3":
            task_id_str = input("Enter task ID to update: ").strip()
            try:
                task_id = int(task_id_str)
                title = input("Enter new title (or press Enter to keep current): ").strip()
                description = input("Enter new description (or press Enter to keep current): ").strip()
                priority = input("Enter new priority (high/medium/low, or press Enter to keep current): ").strip()
                tags = input("Enter new tags (comma-separated, or press Enter to keep current): ").strip()
                due_date = input("Enter new due date (or Enter to keep, 'none' to clear): ").strip()
                recurrence = input("Enter new recurrence (daily/weekly/monthly, Enter to keep, 'none' to clear): ").strip()
                cli.update(
                    task_id,
                    title if title else None,
                    description if description else None,
                    priority if priority else None,
                    tags if tags else None,
                    due_date if due_date else None,
                    recurrence if recurrence else None,
                )
            except ValueError:
                print("Error: Task ID must be a number")

        elif choice == "4":
            cli.view()

        elif choice == "5":
            task_id_str = input("Enter task ID to mark: ").strip()
            try:
                task_id = int(task_id_str)
                cli.mark(task_id)
            except ValueError:
                print("Error: Task ID must be a number")

        elif choice == "6":
            keyword = input("Enter search keyword: ").strip()
            cli.search(keyword)

        elif choice == "7":
            filter_type = input("Filter by (status/priority/tag): ").strip().lower()
            value = input("Enter value: ").strip()
            cli.filter_tasks(filter_type, value)

        elif choice == "8":
            criterion = input("Sort by (priority/title/date): ").strip().lower()
            cli.sort(criterion)

        elif choice == "9":
            cli.save_tasks()

        elif choice == "10":
            cli.load_tasks()

        elif choice == "11":
            print("Goodbye!")
            break

        else:
            print(f"Unknown choice: {choice}")


if __name__ == "__main__":
    main()
