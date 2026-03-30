import typing
from datetime import date, timedelta

if typing.TYPE_CHECKING:
    import pytest

from todotxt_tftt.colors import COLOR_DARK_GRAY, COLOR_LIGHT_GRAY, COLOR_RESET
from todotxt_tftt.models import SectionData, SectionName, Task
from todotxt_tftt.ui import calculate_task_age_color, render_output


def test_calculate_task_age_color_completed() -> None:
    task = Task(
        id=1,
        original_line="x 2026-03-15 A done task",
        is_completed=True,
        priority=None,
        completion_date=date(2026, 3, 15),
        creation_date=date(2026, 3, 10),
        status=None,
    )
    color = calculate_task_age_color(task, today=date(2026, 3, 15), max_days=30)
    assert color == COLOR_DARK_GRAY


def test_calculate_task_age_color_no_creation_date() -> None:
    task = Task(
        id=2,
        original_line="A task with no date",
        is_completed=False,
        priority=None,
        completion_date=None,
        creation_date=None,
        status=None,
    )
    color = calculate_task_age_color(task, today=date(2026, 3, 15), max_days=30)
    assert color == COLOR_LIGHT_GRAY


def test_calculate_task_age_color_with_date() -> None:
    today = date(2026, 3, 15)
    creation_date = today - timedelta(days=15)
    task = Task(
        id=3,
        original_line="2026-03-01 A half-aged task",
        is_completed=False,
        priority=None,
        completion_date=None,
        creation_date=creation_date,
        status=None,
    )
    color = calculate_task_age_color(task, today=today, max_days=30)
    # At 15 out of 30 days (0.5 ratio), we expect yellow (255 r, 255 g, 0 b)
    assert color == "\033[38;2;255;255;0m"


def test_render_output_clean(capsys: pytest.CaptureFixture[str]) -> None:
    task1 = Task(
        id=1,
        original_line="(A) Buy groceries",
        is_completed=False,
        priority="A",
        completion_date=None,
        creation_date=None,
        status=None,
    )

    sections = [
        SectionData(
            name=SectionName.BACKLOG,
            tasks=[task1],
            count=1,
            unfiltered_count=2,
            limit=20,
        )
    ]

    footer = ["TODO: 1 of 5 tasks shown"]

    render_output(sections, footer=footer, max_days=30)

    captured = capsys.readouterr()
    stdout = captured.out

    # Assert section name is printed without warning
    assert "# Backlog\n" in stdout
    # Assert task is printed with light gray (since no date)
    assert f"{COLOR_LIGHT_GRAY}(A) Buy groceries{COLOR_RESET}" in stdout
    # Assert footer is printed
    assert "1 of 2 shown of max 20" in stdout
    assert "--\nTODO: 1 of 5 tasks shown" in stdout


def test_render_output_with_warning_and_separators(capsys: pytest.CaptureFixture[str]) -> None:
    section1 = SectionData(
        name=SectionName.IN_PROGRESS,
        tasks=[],
        count=0,
        unfiltered_count=5,  # over limit warning!
        limit=3,
    )
    section2 = SectionData(
        name=SectionName.BLOCKED,
        tasks=[],
        count=0,
        unfiltered_count=1,
        limit=5,
    )

    render_output([section1, section2], footer=[], max_days=30)

    captured = capsys.readouterr()
    stdout = captured.out

    # Assert section 1 has warning
    assert "# In progress ⚠️\n" in stdout
    # Assert section 1 limits
    assert "0 of 5 shown of max 3" in stdout

    # Assert section separator
    assert "---" in stdout

    # Assert section 2 has no warning
    assert "# Blocked\n" in stdout
    assert "0 of 1 shown of max 5" in stdout
