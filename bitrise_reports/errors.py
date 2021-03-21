# errors.py

from enum import Enum


class CLIArgumentsError(RuntimeError):
    def __init__(self, cause):
        self.cause = cause


class BitriseMiddlewareError(RuntimeError):
    def __init__(self, cause):
        self.cause = cause


class BitriseIntegrationError(RuntimeError):
    def __init__(self, cause):
        self.cause = cause


class BitriseMetricsExtractionError(RuntimeError):
    def __init__(self, cause):
        self.cause = cause


class ErrorCause(Enum):
    Networking = 1
    HttpRest = 2
    ApiDataConversion = 3
    CannotExtractMetrics = 4
