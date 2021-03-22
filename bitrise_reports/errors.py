# errors.py

from enum import Enum


class BitriseReportsError(RuntimeError):
    def __init__(self, cause, message):
        self.cause = cause
        self.message = message


class ErrorCause(Enum):
    NetworkingInfrastructure = 1
    DataConversion = 2
    MetricsExtraction = 3
    MiddlewareOrchestration = 4
    EntrypointHandling = 5
