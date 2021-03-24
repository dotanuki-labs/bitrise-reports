# test_cli.py

from bitrise_reports import cli
from bitrise_reports.errors import ErrorCause, BitriseReportsError

import pytest


def test_app_validation_success():
    app = "android-flagship"

    validated = cli.validated_app(app)

    assert validated == app


def test_app_validation_failed():
    with pytest.raises(Exception) as error:

        cli.validated_app(None)

        assert error is BitriseReportsError
        assert error.cause == ErrorCause.EntrypointHandling


def test_date_validation_success():
    day = "2021-03-01"

    validated = cli.validated_date(day, include_hours=True)

    assert validated is not None


def test_date_validation_failed():
    with pytest.raises(Exception) as error:

        day = "20210301"

        cli.validated_date(day, include_hours=True)

        assert error is BitriseReportsError
        assert error.cause == ErrorCause.EntrypointHandling


def test_report_validation_success():
    report = "excel"

    validated = cli.validated_report(report)

    assert validated == report


def test_report_validation_failed():
    with pytest.raises(Exception) as error:

        report = "xml"

        cli.validated_report(report)

        assert error is BitriseReportsError
        assert error.cause == ErrorCause.EntrypointHandling
