# test_cli.py

from bitrise_reports import cli
from bitrise_reports.errors import CLIArgumentsError

import pytest


def test_extract_criteria():

    # Given
    app = "android-flagship"
    starting = "2021-03-01"
    ending = "2021-03-31"

    # When
    criteria = cli.parse_criteria(app, starting, ending)

    # Then
    assert criteria is not None


def test_fail_when_missing_app():

    with pytest.raises(Exception) as error:
        # Given
        app = ""
        starting = "2021-03-01"
        ending = "2021-03-31"

        # When
        cli.parse_criteria(app, starting, ending)

        # Then
        assert error.cause is CLIArgumentsError


def test_fail_with_broken_date_format():

    with pytest.raises(Exception) as error:

        # Given
        app = "android-flagship"
        starting = "20210301"
        ending = "20210331"

        # When
        cli.parse_criteria(app, starting, ending)

        # Then
        assert error.cause is CLIArgumentsError
