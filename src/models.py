import calendar
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class Priority(Enum):
    """Task priority levels with integer values for sort ordering."""
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class RecurrenceInterval(Enum):
    """Supported recurring task intervals."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


def parse_tags(raw: str) -> list[str]:
    """Parse comma-separated tag input into a clean, deduplicated list.

    Processing pipeline: split by comma, strip whitespace, lowercase,
    filter empty strings, deduplicate while preserving insertion order.

    Args:
        raw: Raw comma-separated tag string (e.g., " Work , home, Work ")

    Returns:
        Cleaned tag list (e.g., ["work", "home"])
    """
    if not raw or not raw.strip():
        return []
    tags = [tag.strip().lower() for tag in raw.split(",")]
    tags = [tag for tag in tags if tag]
    return list(dict.fromkeys(tags))


def parse_due_date(raw: str) -> datetime:
    """Parse a due date string into a datetime object.

    Accepted formats:
    - "YYYY-MM-DD" → date at 23:59
    - "YYYY-MM-DD HH:MM" → date at specified time
    - "today" → today at 23:59
    - "today HH:MM" → today at specified time
    - "tomorrow" → tomorrow at 23:59
    - "tomorrow HH:MM" → tomorrow at specified time

    Args:
        raw: Raw date input string

    Returns:
        Parsed datetime object

    Raises:
        ValueError: If the format is invalid
    """
    text = raw.strip().lower()
    if not text:
        raise ValueError("Due date cannot be empty")

    default_time = (23, 59)

    # Handle "today" and "tomorrow" shortcuts
    if text.startswith("today") or text.startswith("tomorrow"):
        if text.startswith("tomorrow"):
            base_date = datetime.now().date() + timedelta(days=1)
            remainder = text[len("tomorrow"):].strip()
        else:
            base_date = datetime.now().date()
            remainder = text[len("today"):].strip()

        if remainder:
            # Parse HH:MM time
            try:
                time_parts = remainder.split(":")
                hour = int(time_parts[0])
                minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    raise ValueError("Invalid time")
                return datetime(base_date.year, base_date.month, base_date.day,
                                hour, minute)
            except (IndexError, ValueError):
                raise ValueError(
                    f"Invalid time format '{remainder}'. Use HH:MM (e.g., 14:30)"
                )
        else:
            return datetime(base_date.year, base_date.month, base_date.day,
                            default_time[0], default_time[1])

    # Handle ISO format: "YYYY-MM-DD" or "YYYY-MM-DD HH:MM"
    parts = text.split()
    try:
        date_part = datetime.strptime(parts[0], "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(
            f"Invalid date format '{raw.strip()}'. "
            "Use YYYY-MM-DD, 'today', or 'tomorrow'"
        )

    if len(parts) > 1:
        # Parse time part
        try:
            time_parts = parts[1].split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time")
            return datetime(date_part.year, date_part.month, date_part.day,
                            hour, minute)
        except (IndexError, ValueError):
            raise ValueError(
                f"Invalid time format '{parts[1]}'. Use HH:MM (e.g., 14:30)"
            )
    else:
        return datetime(date_part.year, date_part.month, date_part.day,
                        default_time[0], default_time[1])


def advance_due_date(due_date: datetime,
                     interval: RecurrenceInterval) -> datetime:
    """Advance a due date by one recurrence interval.

    Args:
        due_date: Current due date
        interval: Recurrence interval to advance by

    Returns:
        New due date advanced by one interval

    Note:
        For monthly recurrence, if the original day exceeds the last day
        of the target month, the date is clamped to the last day
        (e.g., Jan 31 → Feb 28).
    """
    if interval == RecurrenceInterval.DAILY:
        return due_date + timedelta(days=1)
    elif interval == RecurrenceInterval.WEEKLY:
        return due_date + timedelta(weeks=1)
    elif interval == RecurrenceInterval.MONTHLY:
        year = due_date.year
        month = due_date.month + 1
        if month > 12:
            month = 1
            year += 1
        last_day = calendar.monthrange(year, month)[1]
        day = min(due_date.day, last_day)
        return due_date.replace(year=year, month=month, day=day)
    else:
        raise ValueError(f"Unknown recurrence interval: {interval}")


def get_alert_status(task: 'Task') -> Optional[str]:
    """Determine the alert status for a task based on its due date.

    Args:
        task: Task to evaluate

    Returns:
        "OVERDUE" if incomplete and past due,
        "DUE SOON" if incomplete and due within 24 hours,
        None otherwise (no alert, no due date, or completed)
    """
    if task.completed or task.due_date is None:
        return None

    now = datetime.now()
    if task.due_date < now:
        return "OVERDUE"
    elif task.due_date - now <= timedelta(hours=24):
        return "DUE SOON"
    return None


@dataclass
class Task:
    """Represents a todo task."""
    id: int
    title: str
    description: Optional[str]
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    recurrence: Optional[RecurrenceInterval] = None
