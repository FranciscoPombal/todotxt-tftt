import typing
from typing import Final

if typing.TYPE_CHECKING:
    from datetime import timedelta

COLOR_RESET: Final[str] = "\033[0m"
COLOR_DARK_GRAY: Final[str] = "\033[38;2;100;100;100m"
COLOR_LIGHT_GRAY: Final[str] = "\033[38;2;150;150;150m"


def calculate_date_color_gradient(age: timedelta, /, *, max_days: int) -> str:
    """
    Calculates an ANSI TrueColor escape sequence gradient (Green -> Yellow -> Red) based on an age timedelta.
    """
    safe_max_days = max(1, max_days)
    days = max(0, min(age.days, safe_max_days))
    ratio = days / safe_max_days

    # Gradient: Green (0) -> Yellow (0.5) -> Red (1.0)
    if ratio <= 0.5:
        r = int(255 * (ratio / 0.5))
        g = 255
    else:
        r = 255
        g = int(255 * (1.0 - (ratio - 0.5) / 0.5))

    return f"\033[38;2;{r};{g};0m"
