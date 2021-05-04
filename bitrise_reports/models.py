# models.py

from dataclasses import dataclass
from enum import Enum
from typing import Dict
from datetime import datetime


class MachineSize(Enum):
    g1small = "standard"
    g1medium = "elite"
    g1large = "elite-xl"
    g2small = "g2.4core"
    g2medium = "g2.8core"
    g2large = "g2.12core"


class BuildStack(Enum):
    linux = "linux"
    osx = "macos"


class ExecutionStatus(Enum):
    success = 1
    error = 2
    other = 3


@dataclass(frozen=True)
class BuildMachine:
    id: str
    size: MachineSize
    stack: BuildStack


@dataclass(frozen=True)
class BitriseProject:
    id: str
    slug: str


@dataclass(frozen=True)
class BitriseWorkflow:
    id: str


@dataclass(frozen=True)
class BuildMinutes:
    queued: int
    building: int
    total: int


@dataclass(frozen=True)
class BitriseBuild:
    project: BitriseProject
    machine: BuildMachine
    workflow: str
    minutes: BuildMinutes
    status : ExecutionStatus


@dataclass(frozen=True)
class CrunchedNumbers:
    count: int
    queued: int
    building: int
    total: int
    successes: int = None
    failures: int = None
    credits: int = None


@dataclass(frozen=True)
class BitriseBreakdown:
    name: str
    details: Dict


@dataclass(frozen=True)
class EvaluationCriteria:
    bitrise_app: str
    starting_at: datetime
    ending_at: datetime
