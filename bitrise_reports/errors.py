# errors.py

from enum import Enum


class BitriseIntegrationError(RuntimeError):
    def __init__(self, cause):
        self.cause = cause


class ErrorCause(Enum):
    Networking = 1
    HttpRest = 2
    ApiDataConversion = 3
