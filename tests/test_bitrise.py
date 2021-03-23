# test_bitrise.py

from .utils import fixture

from bitrise_reports.bitrise import Bitrise, BITRISE_API_URL
from bitrise_reports.models import BitriseProject, BuildMinutes, BitriseBuild
from bitrise_reports.models import (
    BuildMachine,
    BuildStack,
    MachineSize,
    BitriseWorkflow,
)

import responses


@responses.activate
def test_retrive_bitrise_projects():

    # Given
    apps = f"{BITRISE_API_URL}/apps"
    payload = fixture("bitrise_apps")

    responses.add(responses.GET, apps, json=payload, status=200)

    bitrise = Bitrise("fake-api-token")

    # When
    projects = bitrise.available_projects()

    # Then
    expected = [
        BitriseProject("android-flagship", "a2b473cfa869c525"),
        BitriseProject("ios-flagship", "2e3c8224cf0952f7"),
    ]

    assert projects == expected


@responses.activate
def test_retrive_builds_for_project():

    # Given
    project = BitriseProject("android-flagship", "f0a251acc3a5f5b7")
    endpoint = f"{BITRISE_API_URL}/apps/f0a251acc3a5f5b7/builds"
    payload = fixture("bitrise_builds")
    responses.add(responses.GET, endpoint, json=payload, status=200)

    bitrise = Bitrise("fake-api-token")

    # When
    builds = bitrise.builds_for_project(project)

    # Then
    linux = BuildMachine("linux.elite", MachineSize.medium, BuildStack.linux)
    workflow = BitriseWorkflow("pull-request")

    expected = [
        BitriseBuild(project, linux, workflow, BuildMinutes(0, 3, 3)),
        BitriseBuild(project, linux, workflow, BuildMinutes(0, 2, 2)),
    ]

    assert builds == expected
