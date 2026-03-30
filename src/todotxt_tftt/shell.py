import os
import shlex
import subprocess

from todotxt_tftt.config import ENV_TODO_SH, PLAIN_MODE_ARG
from todotxt_tftt.models import AppConfig, Task, TodoAction
from todotxt_tftt.parser import parse_task


class TodoShellError(Exception):
    """Raised when the todo.sh subprocess fails."""


def get_todo_output(todo_sh: str, /, *, args: list[str]) -> tuple[list[Task], list[str]]:
    """
    Runs todo.sh with the given arguments in plain mode and parses the output into tasks and footer metadata.
    """

    cmd = [*shlex.split(todo_sh), PLAIN_MODE_ARG, *args]
    try:
        result = subprocess.run(cmd, text=True, capture_output=True, check=True)  # noqa: S603 - false positive; adding shell=True here would be a shell injection risk, and we don't need shell features for this command.
        output = result.stdout
    except subprocess.CalledProcessError as e:
        err = TodoShellError(f"Error running {todo_sh}")
        err.add_note(f"Failed to execute command: {' '.join(cmd)}")
        if e.stderr:
            err.add_note(f"Command stderr output: {e.stderr.strip()}")
        raise err from e

    tasks: list[Task] = list()
    footer: list[str] = list()

    for line in output.splitlines():
        if line.startswith("--") or line.startswith("TODO:"):
            footer.append(line)
            continue

        task = parse_task(line)
        if task:
            tasks.append(task)
        elif line.strip():
            # Catch stray lines as footer metadata just in case
            footer.append(line)

    return tasks, footer


def fetch_tasks(config: AppConfig, /) -> tuple[list[Task], list[Task], list[str]]:
    """
    Runs todo.sh in plain mode, forwarding all arguments to leverage built-in filtering.
    """
    todo_sh = os.environ.get(ENV_TODO_SH, "todo.sh")

    action = TodoAction.LIST
    if config.show_all:
        action = TodoAction.LISTALL
    elif config.show_prioritized:
        action = TodoAction.LISTPRI

    filters = config.remaining_args
    action_args = [action.value, *filters]

    # Fetch filtered tasks
    tasks, footer = get_todo_output(todo_sh, args=action_args)

    # Fetch unfiltered tasks
    base_action = TodoAction.LISTALL if config.show_all else TodoAction.LIST
    if not filters and action == base_action:
        unfiltered_tasks = tasks
    else:
        unfiltered_tasks, _ = get_todo_output(todo_sh, args=[base_action.value])

    return tasks, unfiltered_tasks, footer
