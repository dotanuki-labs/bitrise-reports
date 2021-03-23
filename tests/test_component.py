# test_component.py

from bitrise_reports.entrypoint import launch
from bitrise_reports.bitrise import BITRISE_API_URL
from click.testing import CliRunner

import json
import os
import responses

FIXTURES_DIR = f"{os.getcwd()}/tests/fixtures"


def fixture(name):
    with open(f"{FIXTURES_DIR}/{name}.json") as payload:
        return json.load(payload)


@responses.activate
def test_app_launched_with_success():

    # Given
    runner = CliRunner()
    app_name = "android-flagship"
    app_slug = "a2b473cfa869c525"

    args = [
        "--token=63a098a2-0f80-42ca-86c7-faba3e9c1730",
        f"--app={app_name}",
        "--starting=2021-03-01",
        "--ending=2021-03-31",
    ]

    apps = f"{BITRISE_API_URL}/apps"
    builds = f"{BITRISE_API_URL}/apps/{app_slug}/builds"
    responses.add(responses.GET, apps, json=fixture("bitrise_apps"), status=200)
    responses.add(responses.GET, builds, json=fixture("bitrise_builds"), status=200)

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
