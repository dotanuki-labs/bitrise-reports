# cli_parser.py

from .errors import CLIArgumentsError
from .models import EvaluationCriteria

from dateutil import tz
from dateutil.parser import parse
import time
import logging

tzinfos = {"GMT": tz.gettz("UK/London")}


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
        cause = "Missing bitrise app name"
        logging.error(cause)
        raise CLIArgumentsError(cause)


def _unixtime(datetime_str):
    try:
        parsed = parse(datetime_str, tzinfos=tzinfos)
        return int(time.mktime(parsed.timetuple()))
    except:
        cause = "Cannot convert date time"
        logging.exception(cause)
        raise CLIArgumentsError(cause)
