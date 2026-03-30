import typing
from datetime import date

from todotxt_tftt.colors import COLOR_DARK_GRAY, COLOR_LIGHT_GRAY, COLOR_RESET, calculate_date_color_gradient

if typing.TYPE_CHECKING:
    from todotxt_tftt.models import SectionData, Task


def calculate_task_age_color(task: Task, /, *, today: date, max_days: int) -> str:
    """
    Returns an ANSI TrueColor escape sequence based on task age or state.
    """
    if task.is_completed:
        return COLOR_DARK_GRAY

    if task.creation_date is None:
        return COLOR_LIGHT_GRAY

    return calculate_date_color_gradient(today - task.creation_date, max_days=max_days)


def render_output(sections_data: list[SectionData], /, *, footer: list[str], max_days: int) -> None:
    """
    Renders the sections and footer to the console.
    """

    today = date.today()

    for i, section in enumerate(sections_data):
        warning = " ⚠️" if section.limit is not None and section.unfiltered_count > section.limit else ""
        print(f"# {section.name}{warning}")

        for t in section.tasks:
            color = calculate_task_age_color(t, today=today, max_days=max_days)
            print(f"{color}{t.original_line}{COLOR_RESET}")

        if section.limit is not None:
            print(f"{section.count} of {section.unfiltered_count} shown of max {section.limit}")
        else:
            print(f"{section.count} of {section.unfiltered_count} shown")

        if i < len(sections_data) - 1:
            print("---")

    # Restore the global footer tracked by todo.sh
    if footer:
        if not footer[0].startswith("--"):
            print("--")
        for f in footer:
            print(f)
