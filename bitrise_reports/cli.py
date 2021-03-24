# cli_parser.py

from .errors import ErrorCause, BitriseReportsError
from dateutil.parser import parse


def validated_app(app_name):
    if app_name:
        return app_name

    cause = ErrorCause.EntrypointHandling
    message = "Missing bitrise app name"
    raise BitriseReportsError(cause, message)


def validated_date(date, include_hours=False):

    time = "23:59:59" if include_hours else "00:00:00"
    iso_datetime = f"{date}T{time}"
    try:
        return parse(iso_datetime)
    except:
        cause = ErrorCause.EntrypointHandling
        message = f"Cannot convert date time -> {iso_datetime}"
        raise BitriseReportsError(cause, message)


def validated_report(report):

    trimmed = report.strip()

    if trimmed in ["stdout", "json", "excel"]:
        return trimmed

    cause = ErrorCause.EntrypointHandling
    message = f"Unsupported report type -> {report}. Options: stdout | json | excel"
    raise BitriseReportsError(cause, message)
