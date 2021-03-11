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
    id:str
    size: MachineSize
    stack: BuildStack


@dataclass(frozen=True)
class BitriseProject():
    id: str
    slug: str


@dataclass(frozen=True)
class BitriseWorkflow():
    id: str


@dataclass(frozen=True)
class BitriseBuild:
    project: BitriseProject
    machine: BuildMachine
    workflow: str
    duration: int


@dataclass(frozen=True)
class BuildMinutes:
    total: int
    queued: int


@dataclass(frozen=True)
class BuildNumbers:
    count: int
    minutes: BuildMinutes
    credits: int = 0


@dataclass(frozen=True)
class BitriseReport:
    name:str
    details: Dict
