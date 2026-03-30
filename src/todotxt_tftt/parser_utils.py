import argparse
import sys
import textwrap
from typing import Any, Protocol, override


class _SupportsWriteStr(Protocol):
    def write(self, s: str, /) -> object: ...


class FullyIndentedHelpParser(argparse.ArgumentParser):
    """
    Custom ArgumentParser that indents the entire help message, including the description and epilog, to better integrate with todo.sh's help output formatting. This makes the tftt action's help message stand out as a distinct section and helps visually separate it from the standard todo.sh help output when users run 'todo.sh help tftt'.
    """

    def __init__(self, *, indent_amount: int = 4, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.indent_prefix: str = " " * (indent_amount + 2)

    @override
    def print_help(self, file: _SupportsWriteStr | None = None) -> None:
        out_file = file if file is not None else sys.stdout
        if out_file is None:
            return

        indented = textwrap.indent(self.format_help(), self.indent_prefix)
        _ = out_file.write(textwrap.indent("tftt\n", self.indent_prefix[2:]))
        _ = out_file.write(indented)


class EnhancedHelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    """
    Combines raw description formatting with automatic default value display for each (non-surpressed) argument.
    """
