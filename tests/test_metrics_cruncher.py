# test_metrics_cruncher.py

from bitrise_reports.models import (
    BitriseBuild,
    BuildNumbers,
    BitriseProject,
    BuildStack,
    MachineSize,
    BuildMachine,
    BitriseWorkflow,
)
from bitrise_reports.metrics import MetricsCruncher

import pytest

ANDROID_PROJECT = BitriseProject("android-flagship", "adb55be2718fc923")
IOS_PROJECT = BitriseProject("ios-flagship", "fe9dd48ffd73cd3d")

LINUX_MEDIUM = BuildMachine("linux.elite", MachineSize.medium, BuildStack.linux)
LINUX_LARGE = BuildMachine("linux.large", MachineSize.large, BuildStack.linux)
OSX_MEDIUM = BuildMachine("macos.medium", MachineSize.medium, BuildStack.osx)

PR_WORKFLOW = BitriseWorkflow("pull-request")
PR_PARALLEL_WORKFLOW = BitriseWorkflow("pull-request-parallel")
QA_RELEASE = BitriseWorkflow("qa-release")
LIVE_RELEASE = BitriseWorkflow("live-release")
TEST_FLIGHT_RELEASE = BitriseWorkflow("test-flight-release")
FULL_BUILD = BitriseWorkflow("full-build")


def test_onebuild_oneproject_permachine_breakdown(cruncher):

    # Given
    builds = [BitriseBuild(ANDROID_PROJECT, LINUX_MEDIUM, PR_WORKFLOW, 20)]

    # When
    breakdown = cruncher.breakdown_per_machine(builds)

    # Then
    expected = {LINUX_MEDIUM: BuildNumbers(count=1, minutes=20, credits=40)}
    assert breakdown.details == expected


def test_onebuild_oneproject_perworkfow_breakdown(cruncher):

    # Given
    builds = [BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_WORKFLOW, 25)]

    # When
    breakdown = cruncher.breakdown_per_workflow(builds)

    # Then
    expected = {PR_WORKFLOW: BuildNumbers(count=1, minutes=25, credits=100)}
    assert breakdown.details == expected


def test_onebuild_oneproject_perproject_breakdown(cruncher):

    # Given
    builds = [BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_WORKFLOW, 30)]

    # When
    breakdown = cruncher.breakdown_per_project(builds)

    expected = {ANDROID_PROJECT: BuildNumbers(count=1, minutes=30, credits=120)}

    assert breakdown.details == expected


def test_oneproject_multiplebuilds_permachine_breakdown(cruncher):

    # Given
    builds = [
        BitriseBuild(ANDROID_PROJECT, LINUX_MEDIUM, PR_WORKFLOW, 10),
        BitriseBuild(ANDROID_PROJECT, LINUX_MEDIUM, PR_PARALLEL_WORKFLOW, 10),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_WORKFLOW, 10),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_PARALLEL_WORKFLOW, 10),
    ]

    # When
    breakdown = cruncher.breakdown_per_machine(builds)

    # Then
    expected = {
        LINUX_MEDIUM: BuildNumbers(count=2, minutes=20, credits=40),
        LINUX_LARGE: BuildNumbers(count=2, minutes=20, credits=80),
    }

    assert breakdown.details == expected


def test_oneproject_multiplebuilds_perproject_breakdown(cruncher):

    # Given
    builds = [
        BitriseBuild(ANDROID_PROJECT, LINUX_MEDIUM, PR_WORKFLOW, 30),
        BitriseBuild(ANDROID_PROJECT, LINUX_MEDIUM, PR_PARALLEL_WORKFLOW, 20),
        BitriseBuild(ANDROID_PROJECT, LINUX_MEDIUM, QA_RELEASE, 40),
        BitriseBuild(ANDROID_PROJECT, LINUX_MEDIUM, LIVE_RELEASE, 40),
    ]

    # When
    breakdown = cruncher.breakdown_per_project(builds)

    # Then
    expected = {ANDROID_PROJECT: BuildNumbers(count=4, minutes=130, credits=260)}
    assert breakdown.details == expected


def test_multiplebuilds_multipleprojects_permachine_breakdown(cruncher):

    # Given
    builds = [
        BitriseBuild(ANDROID_PROJECT, LINUX_MEDIUM, PR_WORKFLOW, 25),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_PARALLEL_WORKFLOW, 15),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, LIVE_RELEASE, 30),
        BitriseBuild(IOS_PROJECT, OSX_MEDIUM, FULL_BUILD, 90),
        BitriseBuild(IOS_PROJECT, OSX_MEDIUM, PR_WORKFLOW, 40),
        BitriseBuild(IOS_PROJECT, OSX_MEDIUM, TEST_FLIGHT_RELEASE, 50),
    ]

    # When
    breakdown = cruncher.breakdown_per_machine(builds)

    # Then
    expected = {
        LINUX_MEDIUM: BuildNumbers(count=1, minutes=25, credits=50),
        LINUX_LARGE: BuildNumbers(count=2, minutes=45, credits=180),
        OSX_MEDIUM: BuildNumbers(count=3, minutes=180, credits=720),
    }

    assert breakdown.details == expected


def test_multiplebuilds_multipleprojects_perproject_breakdown(cruncher):

    # Given
    builds = [
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_WORKFLOW, 25),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_WORKFLOW, 20),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_PARALLEL_WORKFLOW, 15),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, QA_RELEASE, 30),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, LIVE_RELEASE, 30),
        BitriseBuild(IOS_PROJECT, OSX_MEDIUM, FULL_BUILD, 90),
        BitriseBuild(IOS_PROJECT, OSX_MEDIUM, PR_WORKFLOW, 40),
        BitriseBuild(IOS_PROJECT, OSX_MEDIUM, PR_WORKFLOW, 30),
        BitriseBuild(IOS_PROJECT, OSX_MEDIUM, TEST_FLIGHT_RELEASE, 50),
    ]

    # When
    breakdown = cruncher.breakdown_per_project(builds)

    # Then
    expected = {
        ANDROID_PROJECT: BuildNumbers(count=5, minutes=120, credits=480),
        IOS_PROJECT: BuildNumbers(count=4, minutes=210, credits=840),
    }

    assert breakdown.details == expected


def test_multiplebuilds_multipleprojects_workflow_breakdown(cruncher):

    # Given
    builds = [
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_WORKFLOW, 25),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_WORKFLOW, 20),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_PARALLEL_WORKFLOW, 14),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, PR_PARALLEL_WORKFLOW, 36),
        BitriseBuild(ANDROID_PROJECT, LINUX_LARGE, LIVE_RELEASE, 30),
        BitriseBuild(IOS_PROJECT, OSX_MEDIUM, FULL_BUILD, 60),
        BitriseBuild(IOS_PROJECT, OSX_MEDIUM, PR_WORKFLOW, 40),
        BitriseBuild(IOS_PROJECT, OSX_MEDIUM, PR_WORKFLOW, 30),
    ]
    # When
    breakdown = cruncher.breakdown_per_workflow(builds)

    # Then
    expected = {
        PR_WORKFLOW: BuildNumbers(count=4, minutes=115, credits=460),
        PR_PARALLEL_WORKFLOW: BuildNumbers(count=2, minutes=50, credits=200),
        LIVE_RELEASE: BuildNumbers(count=1, minutes=30, credits=120),
        FULL_BUILD: BuildNumbers(count=1, minutes=60, credits=240),
    }

    assert breakdown.details == expected


@pytest.fixture
def cruncher():
    return MetricsCruncher()
