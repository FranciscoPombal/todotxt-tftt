# AGENTS.md

## Setup

- The dev dependencies are not installed by default by `uv sync`, you must use `uv sync --all-groups`.

- Use `uv` to run dev tools (if dev tools are not available, you probably forgot to `uv sync --all-groups`):

  - `mypy`: invoke it on the module, like `uv run mypy -m todotxt_tftt ...`
  - `pyright`: `uv run pyright`
  - `ruff`: `uv run ruff check`

## Code Style

- Use positional-only (`/`) and keyword-only (`*`) parameter boundaries on all new functions.
- No external dependencies outside of `pytest` and `hypothesis` or related official add-on packages for testing.

## Running & Testing

- Run with: `uv run todotxt-tftt --help` (or `uv run python3 -m todotxt_tftt --help`).

- Run tests with: `uv run pytest`.

- Refer to [the README's section on Testing & Debugging](README.md#testing--debugging) for more information on how tests are set up and how new ones should be implemented.
