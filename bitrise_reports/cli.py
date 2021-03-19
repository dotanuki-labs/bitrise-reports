# cli_parser.py

from . errors import CLIArgumentsError
from . models import EvaluationCriteria

from datetime import datetime
import time
import logging


def parse_criteria(app, starting, ending):
    return EvaluationCriteria(
        _validate_app(app),
        _unixtime(starting),
        _unixtime(ending)
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
        parsed = datetime.strptime(datetime_str, '%Y-%m-%d')
        return int(time.mktime(parsed.timetuple()))
    except:
        cause = "Missing bitrise app name"
        logging.exception(cause)
        raise CLIArgumentsError(cause)
