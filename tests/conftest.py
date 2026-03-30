import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True, scope="session")
def isolate_todo_env() -> None:
    """
    Ensure all tests use the sandboxed test_files configuration.
    """
    workspace_root = Path(__file__).parent.parent.resolve()
    todo_cfg = workspace_root / "test_files" / "todo.cfg"

    # Set TODO_SH to explicitly use the isolated config file.
    os.environ["TODO_SH"] = f"todo.sh -d {todo_cfg}"
