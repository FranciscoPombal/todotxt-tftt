from datetime import date
from pathlib import Path

from todotxt_tftt.models import Status
from todotxt_tftt.parser import parse_task


def test_parse_task_from_todo_03() -> None:
    test_file = Path(__file__).parent.parent / "test_files" / "todo" / "todo_02.txt"
    lines = test_file.read_text().splitlines()

    # Prepend line numbers as todo.sh `ls` does
    numbered_lines = [f"{i + 1:02d} {line}" for i, line in enumerate(lines)]

    task1 = parse_task(numbered_lines[0])
    assert task1 is not None
    assert task1.id == 1
    assert task1.priority == "A"
    assert task1.creation_date == date(2026, 3, 12)
    assert task1.status == Status.IN_PROGRESS

    task2 = parse_task(numbered_lines[1])
    assert task2 is not None
    assert task2.id == 2
    assert task2.priority is None
    assert task2.creation_date == date(2026, 3, 12)
    assert task2.status is None

    task3 = parse_task(numbered_lines[2])
    assert task3 is not None
    assert task3.id == 3
    assert task3.priority == "B"
    assert task3.creation_date is None
    assert task3.status == Status.BLOCKED

    task4 = parse_task(numbered_lines[3])
    assert task4 is not None
    assert task4.id == 4
    assert task4.status == Status.BLOCKED

    task5 = parse_task(numbered_lines[4])
    assert task5 is not None
    assert task5.id == 5
    assert task5.is_completed is True
    assert task5.completion_date == date(2026, 3, 15)
    assert task5.creation_date == date(2026, 3, 12)
    assert task5.status is None
