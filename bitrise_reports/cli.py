# cli_parser.py

from .errors import CLIArgumentsError
from .models import EvaluationCriteria

from dateutil.parser import parse
import time
import logging


def parse_criteria(app, starting, ending):
    return EvaluationCriteria(
        _validate_app(app),
        _unixtime(f"{starting}T00:00:00+00:00"),
        _unixtime(f"{ending}T23:59:59+00:00")
    )


def _validate_app(app_name):
    if app_name:
        return app_name
    else:
        cause = "Missing bitrise app name"
        logging.error(cause)
        raise CLIArgumentsError(cause)


def _unixtime(datetime_str):
    try:
        parsed = parse(datetime_str)
        return int(time.mktime(parsed.timetuple()))
    except:
        cause = "Cannot convert date time"
        logging.exception(cause)
        raise CLIArgumentsError(cause)
