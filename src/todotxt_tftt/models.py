import typing
from dataclasses import dataclass
from enum import StrEnum, auto

if typing.TYPE_CHECKING:
    from datetime import date


class Status(StrEnum):
    IN_PROGRESS = auto()
    BLOCKED = auto()


class SectionName(StrEnum):
    IN_PROGRESS = "In progress"
    BLOCKED = "Blocked"
    BACKLOG = "Backlog"
    DONE = "Done"


class TodoAction(StrEnum):
    LIST = auto()
    LISTALL = auto()
    LISTPRI = auto()


@dataclass(frozen=True, slots=True, kw_only=True)
class Task:
    id: int
    original_line: str
    is_completed: bool
    priority: str | None
    completion_date: date | None
    creation_date: date | None
    status: Status | None


@dataclass(frozen=True, slots=True, kw_only=True)
class SectionLimits:
    blocked: int
    in_progress: int
    backlog: int


@dataclass(frozen=True, slots=True, kw_only=True)
class AppConfig:
    limits: SectionLimits
    max_days: int
    show_all: bool
    show_prioritized: bool
    remaining_args: list[str]


@dataclass(frozen=True, slots=True, kw_only=True)
class SectionData:
    name: SectionName
    tasks: list[Task]
    count: int
    unfiltered_count: int
    limit: int | None


type TaskGroups = dict[SectionName, list[Task]]
