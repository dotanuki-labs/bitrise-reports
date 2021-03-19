# test_app.py

from bitrise_reports.app import launch
from click.testing import CliRunner


def test_app_launched():

    # Given
    runner = CliRunner()
    args = ["--app=android-flagship", "--starting=2021-03-01", "--ending=2021-03-31"]

    # When
    result = runner.invoke(launch, args)
    print(result.output)

    # Then
    assert result.exit_code == 0
