# test_component.py

from bitrise_reports.entrypoint import launch
from click.testing import CliRunner


def test_app_launched_with_success():

    # Given
    runner = CliRunner()
    args = [
        "--token=63a098a2-0f80-42ca-86c7-faba3e9c1730",
        "--app=android-flagship",
        "--starting=2021-03-01",
        "--ending=2021-03-31",
    ]

    # When
    result = runner.invoke(launch, args)

    # Then
    assert result.exit_code == 0


def test_app_launched_missing_parameters():

    # Given
    runner = CliRunner()
    args = [
        "--app=android-flagship",
        "--starting=2021-03-01",
        "--ending=2021-03-31",
    ]

    # When
    result = runner.invoke(launch, args)

    # Then
    assert result.exit_code != 0
