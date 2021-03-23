# test_bitrise_api_fetcher.py

from bitrise_reports.bitrise import BitriseApiFetcher
from bitrise_reports.errors import ErrorCause, BitriseReportsError
from datetime import datetime

import json
import os
import pytest
import responses

FAKE_ENDPOINT = "https://fake.api.bitrise.com/android-versions"
FIXTURES_DIR = f"{os.getcwd()}/tests/fixtures"


def fixture(name):
    with open(f"{FIXTURES_DIR}/{name}.json") as payload:
        return json.load(payload)


@responses.activate
def test_fetch_one_page():

    # Given
    fetcher = BitriseApiFetcher("fake-api-token")
    data = fixture("bitrise_200OK")

    responses.add(
        responses.GET, FAKE_ENDPOINT, json=data, status=200, match_querystring=True
    )

    # When
    android_versions = fetcher.get(FAKE_ENDPOINT)

    # Then
    assert len(android_versions) == 4


@responses.activate
def test_fetch_several_pages():

    # Given
    fetcher = BitriseApiFetcher("fake-api-token")
    next = f"{FAKE_ENDPOINT}?next=29"

    responses.add(
        responses.GET,
        FAKE_ENDPOINT,
        match_querystring=True,
        json=fixture("bitrise_200OK_page01"),
        status=200,
    )

    responses.add(
        responses.GET,
        next,
        match_querystring=True,
        json=fixture("bitrise_200OK_page02"),
        status=200,
    )

    # When
    android_versions = fetcher.get(FAKE_ENDPOINT)

    # Then
    assert len(android_versions) == 6


@responses.activate
def test_fetch_several_pages_on_timewindow():

    # Given
    fetcher = BitriseApiFetcher("fake-api-token")

    starting_millis = 1614553200
    ending_millis = 1617227999
    starting_dt = datetime.fromtimestamp(starting_millis)
    ending_dt = datetime.fromtimestamp(ending_millis)

    base = f"{FAKE_ENDPOINT}?after={starting_millis}&before={ending_millis}"
    next = f"{FAKE_ENDPOINT}?next=29&after={starting_millis}&before={ending_millis}"

    responses.add(
        responses.GET,
        base,
        match_querystring=True,
        json=fixture("bitrise_200OK_page01"),
        status=200,
    )

    responses.add(
        responses.GET,
        next,
        match_querystring=True,
        json=fixture("bitrise_200OK_page02"),
        status=200,
    )

    # When
    android_versions = fetcher.get(FAKE_ENDPOINT, starting_dt, ending_dt)

    # Then
    assert len(android_versions) == 6


@responses.activate
def test_http_error():

    with pytest.raises(Exception) as error:

        # Given
        responses.add(
            responses.GET, FAKE_ENDPOINT, json=fixture("bitrise_5xx"), status=503
        )
        fetcher = BitriseApiFetcher("fake-api-token")

        # When
        fetcher.get(FAKE_ENDPOINT)

        # Then
        assert error is BitriseReportsError
        assert error.cause == ErrorCause.NetworkingInfrastructure
