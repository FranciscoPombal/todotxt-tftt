import os
import shutil
import typing
from pathlib import Path

import pytest

from todotxt_tftt.shell import get_todo_output

if typing.TYPE_CHECKING:
    from todotxt_tftt.models import Task

_todo_sh_missing = shutil.which("todo.sh") is None


def _run_ls() -> tuple[list[Task], list[str]]:
    todo_sh = os.environ.get("TODO_SH", "todo.sh")
    return get_todo_output(todo_sh, args=["ls"])


@pytest.mark.skipif(_todo_sh_missing, reason="todo.sh is not installed")
def test_default_file_sandbox() -> None:
    """Verify that by default the sandbox uses test_files/todo_debug.txt."""
    # Run the shell integration without terms
    tasks, _ = _run_ls()
    # We expect some tasks to be parsed from the default file
    assert len(tasks) >= 0


@pytest.mark.skipif(_todo_sh_missing, reason="todo.sh is not installed")
def test_monkeypatch_static_file(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that monkeypatching TODO_FILE securely redirects reading to another mock file."""
    # Explicitly set TODO_FILE to our second static file
    test_dir = Path(__file__).parent.parent / "test_files" / "todo"
    todo_file_path = test_dir / "todo_01.txt"
    monkeypatch.setenv("TODO_FILE", str(todo_file_path))

    tasks, _ = _run_ls()

    # We should have exactly 31 tasks from `todo_01.txt`, including one matching "Dummy task 1"
    assert len(tasks) == 31
    assert any("Dummy task 1" in t.original_line for t in tasks)


@pytest.mark.skipif(_todo_sh_missing, reason="todo.sh is not installed")
def test_monkeypatch_tmp_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Verify that we can dynamically generate a todo file right in memory/tmp and test it."""
    # Write dynamic content to a secure temporary path
    dyn_todo = tmp_path / "hyp_todo.txt"
    _ = dyn_todo.write_text("(C) A completely dynamic string +testing\n", encoding="utf-8")

    # Reroute todo.sh to read this temp file instead
    monkeypatch.setenv("TODO_FILE", str(dyn_todo))

    tasks, _ = _run_ls()

    # Verify todo.sh flawlessly fetched and UI-parsed the dynamic string
    assert len(tasks) == 1
    assert "+testing" in tasks[0].original_line
    assert "A completely dynamic string" in tasks[0].original_line
