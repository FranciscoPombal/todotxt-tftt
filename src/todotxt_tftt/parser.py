import contextlib
import re
from datetime import date
from typing import Final

from todotxt_tftt.models import Status, Task

# Pre-compiled regular expressions for parse_task
RE_TODO_ID: Final[re.Pattern[str]] = re.compile(r"^(\d+)\s+(.*)")
RE_COMPLETION_DATE: Final[re.Pattern[str]] = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(.*)")
RE_PRIORITY: Final[re.Pattern[str]] = re.compile(r"^\(([A-Z])\)\s+(.*)")
RE_CREATION_DATE: Final[re.Pattern[str]] = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(.*)")
RE_TAGS: Final[re.Pattern[str]] = re.compile(r"((?:\s+[^:\s]+:\S+)+)$")
RE_STATUS: Final[re.Pattern[str]] = re.compile(r"(?:^|\s)status:(in_progress|blocked)(?=\s|$)")


def parse_task(line: str, /) -> Task | None:
    """
    Sequentially parses a todo.txt line according to strict format rules.
    This guarantees that strings like "x (A) foo" are treated as descriptions
    if they are not at the correct absolute starting positions.
    """
    line = line.strip("\n")
    if not line or line.startswith("--") or line.startswith("TODO:"):
        return None

    # Extract the todo.sh task ID prepended by the `ls` command
    if not (match_id := RE_TODO_ID.match(line)):
        return None

    task_id = int(match_id.group(1))
    text = match_id.group(2)
    original_text = text

    is_completed = False
    priority = None
    completion_date = None
    creation_date = None

    # 1. Completion marker
    if text.startswith("x "):
        is_completed = True
        text = text[2:]

        # 2. Completion date (only applies if task is completed)
        if match_completion_date := RE_COMPLETION_DATE.match(text):
            with contextlib.suppress(ValueError):
                completion_date = date.fromisoformat(match_completion_date.group(1))
                text = match_completion_date.group(2)

    # 3. Priority
    if match_priority := RE_PRIORITY.match(text):
        priority = match_priority.group(1)
        text = match_priority.group(2)

    # 4. Creation date
    if match_creation_date := RE_CREATION_DATE.match(text):
        with contextlib.suppress(ValueError):
            creation_date = date.fromisoformat(match_creation_date.group(1))
            text = match_creation_date.group(2)

    # Extract status tag only from the tags at the end of the string, only the last status tag defines the status if multiple are present.
    status: Status | None = None
    if (match_tags := RE_TAGS.search(original_text)) and (statuses := RE_STATUS.findall(match_tags.group(1))):
        with contextlib.suppress(ValueError):
            status = Status(statuses[-1])

    return Task(
        id=task_id,
        original_line=line,
        is_completed=is_completed,
        priority=priority,
        completion_date=completion_date,
        creation_date=creation_date,
        status=status,
    )
