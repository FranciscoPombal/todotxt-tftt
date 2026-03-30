import sys
from datetime import date
from typing import assert_never

from todotxt_tftt.config import parse_args
from todotxt_tftt.models import SectionData, SectionLimits, SectionName, Status, Task, TaskGroups
from todotxt_tftt.shell import TodoShellError, fetch_tasks
from todotxt_tftt.ui import render_output


def group_tasks(tasks: list[Task], /) -> TaskGroups:
    """
    Groups tasks into sections based on their status and completion state.
    """
    sections: TaskGroups = {name: [] for name in SectionName}

    for t in tasks:
        match t:
            case Task(is_completed=True):
                sections[SectionName.DONE].append(t)
            case Task(status=Status.IN_PROGRESS):
                sections[SectionName.IN_PROGRESS].append(t)
            case Task(status=Status.BLOCKED):
                sections[SectionName.BLOCKED].append(t)
            case _:
                sections[SectionName.BACKLOG].append(t)
    return sections


def build_sections_data(
    filtered_tasks: list[Task], unfiltered_tasks: list[Task], /, *, limits: SectionLimits
) -> list[SectionData]:
    """
    Aggregates filtered operations, unfiltered global counts, and user limits gracefully into a flat list structure.
    """
    sections_with_filtered_tasks: TaskGroups = group_tasks(filtered_tasks)
    sections_with_unfiltered_tasks: TaskGroups = group_tasks(unfiltered_tasks)

    def get_limit(name: SectionName, limits: SectionLimits, /) -> int | None:
        match name:
            case SectionName.BLOCKED:
                return limits.blocked
            case SectionName.IN_PROGRESS:
                return limits.in_progress
            case SectionName.BACKLOG:
                return limits.backlog
            case SectionName.DONE:
                return None
            case _ as unreachable:
                assert_never(unreachable)

    return [
        SectionData(
            name=name,
            tasks=sorted(
                sections_with_filtered_tasks[name],
                key=lambda t: (
                    1 if t.id == 0 else 0,  # Archived tasks (id=0) at the very bottom
                    0 if t.priority is not None else 1,  # Prioritized tasks first
                    t.priority or "",  # Sort by priority A-Z
                    1 if t.creation_date is None else 0,  # Force dateless tasks to the bottom
                    t.creation_date if t.creation_date else date.min,
                    t.id,
                ),
            ),
            count=len(sections_with_filtered_tasks[name]),
            unfiltered_count=len(sections_with_unfiltered_tasks[name]),
            limit=get_limit(name, limits),
        )
        for name in SectionName
    ]


def main() -> None:
    args = sys.argv[1:]
    config = parse_args(args)
    try:
        tasks, unfiltered_tasks, footer = fetch_tasks(config)
    except TodoShellError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    # Build the combined SectionData models
    sections_data = build_sections_data(tasks, unfiltered_tasks, limits=config.limits)

    # Print formatted output
    render_output(sections_data, footer=footer, max_days=config.max_days)
