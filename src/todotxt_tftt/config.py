import argparse
from typing import Final

from todotxt_tftt.models import AppConfig, SectionLimits
from todotxt_tftt.parser_utils import EnhancedHelpFormatter, FullyIndentedHelpParser

# Configuration
TODO_SH_ACTION_NAME: Final[str] = "tftt"
TODO_SH_ACTION_DESCRIPTION: Final[str] = (
    "A frontend for todo.sh.\n\n"
    "Wraps the 'list' action by default (this can be changed to 'listall' or 'listpri' with flags described below).\n"
    "TERM(s) for filtering are passed directly to todo.sh wihtout modification.\n"
    "To filter by TERM(s) identical to flags this action recognizes, pass them after --.\n"
)
DEFAULT_MAX_DAYS: Final[int] = 30
DEFAULT_MAX_BLOCKED: Final[int] = 5
DEFAULT_MAX_IN_PROGRESS: Final[int] = 3
DEFAULT_MAX_BACKLOG: Final[int] = 20
PLAIN_MODE_ARG: Final[str] = "-p"  # Use plain mode to get unformatted output from todo.sh (no colors)
ENV_TODO_SH: Final[str] = "TODO_SH"  # Environment variable to specify the path to todo.sh


def parse_args(args: list[str], /) -> AppConfig:
    """
    Parses command-line arguments and returns an AppConfig object.
    """

    parser = FullyIndentedHelpParser(
        prog=TODO_SH_ACTION_NAME,
        description=TODO_SH_ACTION_DESCRIPTION,
        suggest_on_error=True,
        formatter_class=EnhancedHelpFormatter,
    )
    # Because we use argparse.ArgumentDefaultsHelpFormatter, we need to set default=argparse.SUPPRESS for these boolean flags to avoid cluttering the help output with "default: False" for each.
    # In doing so, we must handle the fact that no attribute corresponding to these options is added if the command-line argument was not present at all, which is why we use getattr with a default of False when accessing them later.
    # We capture the return value of add_argument for these flags so we can refer to them without hardcoding the attribute names, which keeps the code more robust to future changes in the flag names or dest values.
    # We also have to do all this for the positional "terms" argument to avoid cluttering the help output with "default: None".
    list_action_wrapping_option_group = parser.add_mutually_exclusive_group()
    option_all = list_action_wrapping_option_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        default=argparse.SUPPRESS,
        help="wrap the 'listall' action instead of 'list'",
    )
    option_pri = list_action_wrapping_option_group.add_argument(
        "-p",
        "--pri",
        action="store_true",
        default=argparse.SUPPRESS,
        help="wrap the 'listpri' action instead of 'list'",
    )
    _ = parser.add_argument(
        "--max-blocked",
        type=int,
        default=DEFAULT_MAX_BLOCKED,
        help="maximum number of blocked tasks to display",
    )
    _ = parser.add_argument(
        "--max-in-progress",
        type=int,
        default=DEFAULT_MAX_IN_PROGRESS,
        help="maximum number of in-progress tasks to display",
    )
    _ = parser.add_argument(
        "--max-backlog",
        type=int,
        default=DEFAULT_MAX_BACKLOG,
        help="maximum number of backlog tasks to display",
    )
    _ = parser.add_argument(
        "--max-days",
        type=int,
        default=DEFAULT_MAX_DAYS,
        help="maximum number of days to saturate the age color gradient",
    )
    arg_terms = parser.add_argument(
        "terms",
        nargs="*",
        metavar="TERM",
        default=argparse.SUPPRESS,
        help="filters applied natively via todo.sh (e.g., +project, @context, -TERM), passed directly without modification.",
    )

    parsed_args, remaining_args = parser.parse_known_args(args)

    limits = SectionLimits(
        blocked=parsed_args.max_blocked,
        in_progress=parsed_args.max_in_progress,
        backlog=parsed_args.max_backlog,
    )

    # Merge explicitly parsed positional terms with any extra unknown flags (like raw strings that start with dashes, e.g. -TERM)
    terms: list[str] = getattr(parsed_args, arg_terms.dest, list())
    filters: list[str] = terms + remaining_args

    return AppConfig(
        limits=limits,
        max_days=parsed_args.max_days,
        show_all=getattr(parsed_args, option_all.dest, False),
        show_prioritized=getattr(parsed_args, option_pri.dest, False),
        remaining_args=filters,
    )
