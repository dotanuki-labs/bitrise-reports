# cli_parser.py

from .errors import ErrorCause, BitriseReportsError
from .models import EvaluationCriteria

from dateutil.parser import parse


def parse_criteria(app, starting, ending):
    iso_starting = f"{starting}T00:00:00"
    iso_ending = f"{ending}T23:59:59"
    return EvaluationCriteria(
        _validate_app(app), _unixtime(iso_starting), _unixtime(iso_ending)
    )


def _validate_app(app_name):
    if app_name:
        return app_name
    else:
        cause = ErrorCause.EntrypointHandling
        message = "Missing bitrise app name"
        raise BitriseReportsError(cause, message)


def _unixtime(datetime_str):
    try:
        return parse(datetime_str)
    except:
        cause = ErrorCause.EntrypointHandling
        message = f"Cannot convert date time -> {datetime_str}"
        raise BitriseReportsError(cause, message)
