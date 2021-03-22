# models.py

from dataclasses import dataclass
from enum import Enum
from typing import Dict


class MachineSize(Enum):
    small = "standard"
    medium = "elite"
    large = "elite-xl"


class BuildStack(Enum):
    linux = "linux"
    osx = "macos"


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


@dataclass(frozen=True)
class CrunchedNumbers:
    count: int
    queued: int
    building: int
    total: int
    credits: int = None


@dataclass(frozen=True)
class BitriseBreakdown:
    name: str
    details: Dict


@dataclass(frozen=True)
class EvaluationCriteria:
    bitrise_app: str
    starting_at: int
    ending_at: int
