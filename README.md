# TFTT for todo.sh

An add-on frontend for `todo.sh` implementing my **TFTT** to-do system written in Python.

**TFTT** stands for _**T**hree, **F**ive, **T**wenty, **T**hirty_.
The naming is a reference to the default numeric limits of the system, which is explained in more detail below.
There is no real science behind it like the fancy acronym might suggest, it's just how I prefer to use to-do lists.

## Installation

**Prerequisite:** [`uv`](https://docs.astral.sh/uv/) must be installed (available in your `PATH`).

Clone this repository directly into your `todo.sh` actions directory and run the installer:

```bash
cd $YOUR_TODO_SH_ACTIONS_DIRECTORY  # For example: ~/.config/todo/todo.actions.d/
git clone https://github.com/FranciscoPombal/todotxt-tftt.git tftt && cd tftt
./install.sh
```

Now run with `todo.sh tftt`.

## Features

- **Listing control**: Includes options to behave like `listall` or `listpri` rather than the default `list` action.
- **Simple task grouping**: Incomplete tasks are categorized into 3 hard-coded categories, **In Progress** (`status:in_progress`), **Blocked** (`status:blocked`), and **Backlog** (no `status` tag, or any other `status` tag).
- **Simple anti-accumulation system**: These categories have (soft) limits defaulting to 3, 5, and 20, respectively.

   _A warning symbol (⚠️) is displayed next to the category name of categories that have more tasks than their configured (soft) limits._

- **Task age gradient**: Tasks are colored with `TrueColor` fading from green, to yellow, to red based on the time elapsed since task creation, over a range of 30 days (configurable).
- **Support for incremental adoption**: Tasks without a creation date are still shown, but with a greyed-out color, distinct from that of completed/archived tasks.
- **`todo.sh` filter passthrough**: All `todo.sh` filtering terms are passed through without modification (e.g. `term`, `+project`, `@context`, ...).

## Usage

```sh
$ todo.sh help tftt
    tftt
      usage: tftt [-h] [-a | -p] [--max-blocked MAX_BLOCKED] [--max-in-progress MAX_IN_PROGRESS] [--max-backlog MAX_BACKLOG] [--max-days MAX_DAYS] [TERM ...]

      A frontend for todo.sh.

      Wraps the 'list' action by default (this can be changed to 'listall' or 'listpri' with flags described below).
      TERM(s) for filtering are passed directly to todo.sh wihtout modification.
      To filter by TERM(s) identical to flags this action recognizes, pass them after --.

      positional arguments:
        TERM                  filters applied natively via todo.sh (e.g., +project, @context, -TERM), passed directly without modification.

      options:
        -h, --help            show this help message and exit
        -a, --all             wrap the 'listall' action instead of 'list'
        -p, --pri             wrap the 'listpri' action instead of 'list'
        --max-blocked MAX_BLOCKED
                              maximum number of blocked tasks to display (default: 5)
        --max-in-progress MAX_IN_PROGRESS
                              maximum number of in-progress tasks to display (default: 3)
        --max-backlog MAX_BACKLOG
                              maximum number of backlog tasks to display (default: 20)
        --max-days MAX_DAYS   maximum number of days to saturate the age color gradient (default: 30)
```

## Development

This project is built using modern Python 3.14+ standards and managed via `uv`.

### Local Setup

If you are cloning this repository to contribute or develop:

1. Clone the repository anywhere on your machine.
2. Initialize the isolated development environment:

   ```bash
   uv sync --all-groups
   ```

3. Run the script standalone: `uv run todotxt-tftt --help` (or `uv run python3 -m todotxt_tftt --help`).

### Testing & Debugging

This project includes a "sandboxing" mechanism to ensure that running, debugging, or testing the codebase locally **never touches your production `todo.txt` data**.

All test configurations and debugging profiles automatically override the `TODO_SH` environment variable to invoke `todo.sh -d <workspace-root>/test_files/todo.cfg`.
This dummy configuration locks `todo.sh`'s `TODO_DIR`, `TODO_FILE`, `DONE_FILE`, and `REPORT_FILE` to the `test_files/` directory (e.g., pointing to mock files like `test_files/todo_01.txt`).

- **Running tests**: Run `uv run pytest`.
A session-scoped fixture inside `tests/conftest.py` dynamically injects the sandboxed `TODO_SH` command, meaning local execution safely redirects all filesystem interaction to the mock files.
- **Debugging (VS Code)**: The `.vscode/launch.json` profiles are pre-configured with the `-d test_files/todo.cfg` injection natively, allowing you to debug CLI workflows cleanly.

Files for testing are available at `test_files/*.txt`.
In addition, for testing purposes it is also possible to mock a `TODO` file dynamically using `pytest`'s `monkeypatch.setenv("TODO_FILE", "...")`.

## Implementation Details

Documentation of select impelmentation details.

### Installation Mechanism

`install.sh` could do nothing but create the symlink.
Even if the virtual environment doesn't exist when the user runs `todo.sh tftt`, the underlying `uv run` command will just immediately rebuild it in the background before executing the script.
However, doing `uv sync` at install-time has some advantages:

- If the environment setup is deferred to a later run of `todo.sh tftt`, the user's first interaction with this plugin in their terminal will hang silently for some seconds while `uv` sets up the virtual environment.

- `install.sh` acts as a "fail-fast" warning - if there is any problem setting up the virtual environment for the first time (for example, there is no Internet connectivity to download the required Python version) `install.sh` will fail immediately.

## License

GPLv3.
