# test_metrics_cruncher.py

from bitrise_reports.models import (
    BitriseBuild,
    BuildMachine,
    BuildMinutes,
    BitriseProject,
    BuildStack,
    BitriseWorkflow,
    CrunchedNumbers,
    ExecutionStatus,
    MachineSize,
)
from bitrise_reports.metrics import MetricsCruncher

import pytest

ANDROID = BitriseProject("android-flagship", "adb55be2718fc923")
IOS = BitriseProject("ios-flagship", "fe9dd48ffd73cd3d")

LINUX_MEDIUM = BuildMachine("linux.elite", MachineSize.g1medium, BuildStack.linux)
LINUX_LARGE = BuildMachine("linux.large", MachineSize.g1large, BuildStack.linux)
OSX_MEDIUM = BuildMachine("macos.medium", MachineSize.g1medium, BuildStack.osx)

PR_WORKFLOW = BitriseWorkflow("pull-request")
PARALLEL_WORKFLOW = BitriseWorkflow("pull-request-parallel")
QA_RELEASE = BitriseWorkflow("qa-release")
LIVE_RELEASE = BitriseWorkflow("live-release")
TEST_FLIGHT_RELEASE = BitriseWorkflow("test-flight-release")
FULL_BUILD = BitriseWorkflow("full-build")
SUCCESS = ExecutionStatus.success


def test_onebuild_permachine_breakdown(cruncher):

    # Given
    minutes = BuildMinutes(queued=0, building=20, total=20)
    builds = [BitriseBuild(ANDROID, LINUX_MEDIUM, PR_WORKFLOW, minutes, SUCCESS)]

    # When
    breakdown = cruncher.breakdown_per_machine(builds)

    # Then
    numbers = CrunchedNumbers(
        count=1, queued=0, building=20, total=20, successes=1, failures=0, abortions=0, credits=40
    )

    expected = {LINUX_MEDIUM: numbers}
    assert breakdown.details == expected


def test_onebuild_perworkfow_breakdown(cruncher):

    # Given
    minutes = BuildMinutes(queued=2, building=20, total=22)
    builds = [BitriseBuild(ANDROID, LINUX_LARGE, PR_WORKFLOW, minutes, SUCCESS)]

    # When
    breakdown = cruncher.breakdown_per_workflow(builds)

    # Then
    numbers = CrunchedNumbers(
        count=1, queued=2, building=20, total=22, successes=1, failures=0, abortions=0, credits=88
    )

    expected = {PR_WORKFLOW: numbers}
    assert breakdown.details == expected


def test_onebuild_perproject_breakdown(cruncher):

    # Given
    minutes = BuildMinutes(queued=0, building=30, total=30)
    builds = [BitriseBuild(ANDROID, LINUX_LARGE, PR_WORKFLOW, minutes, SUCCESS)]

    # When
    breakdown = cruncher.breakdown_per_project(builds)

    numbers = CrunchedNumbers(
        count=1, queued=0, building=30, total=30, successes=1, failures=0, abortions=0, credits=120
    )

    expected = {ANDROID: numbers}

    assert breakdown.details == expected


def test_multiplebuilds_permachine_breakdown(cruncher):

    # Given
    minutes = BuildMinutes(queued=0, building=10, total=10)
    builds = [
        BitriseBuild(ANDROID, LINUX_MEDIUM, PR_WORKFLOW, minutes, SUCCESS),
        BitriseBuild(ANDROID, LINUX_MEDIUM, PARALLEL_WORKFLOW, minutes, SUCCESS),
        BitriseBuild(ANDROID, LINUX_LARGE, PR_WORKFLOW, minutes, SUCCESS),
        BitriseBuild(ANDROID, LINUX_LARGE, PARALLEL_WORKFLOW, minutes, SUCCESS),
    ]

    # When
    breakdown = cruncher.breakdown_per_machine(builds)

    # Then
    expected = {
        LINUX_MEDIUM: CrunchedNumbers(
            count=2,
            queued=0,
            building=20,
            total=20,
            successes=2,
            failures=0,
            abortions=0,
            credits=40,
        ),
        LINUX_LARGE: CrunchedNumbers(
            count=2,
            queued=0,
            building=20,
            total=20,
            successes=2,
            failures=0,
            abortions=0,
            credits=80,
        ),
    }

    assert breakdown.details == expected


def test_multiplebuilds_perproject_breakdown(cruncher):

    # Given
    builds = [
        BitriseBuild(ANDROID, LINUX_MEDIUM, PR_WORKFLOW, BuildMinutes(0, 30, 30), SUCCESS),
        BitriseBuild(ANDROID, LINUX_MEDIUM, PARALLEL_WORKFLOW, BuildMinutes(0, 20, 20), SUCCESS),
        BitriseBuild(ANDROID, LINUX_MEDIUM, QA_RELEASE, BuildMinutes(0, 40, 40), SUCCESS),
        BitriseBuild(ANDROID, LINUX_MEDIUM, LIVE_RELEASE, BuildMinutes(0, 40, 40), SUCCESS),
    ]

    # When
    breakdown = cruncher.breakdown_per_project(builds)

    # Then
    numbers = CrunchedNumbers(
        count=4,
        queued=0,
        building=130,
        total=130,
        successes=4,
        failures=0,
        abortions=0,
        credits=260,
    )

    expected = {ANDROID: numbers}
    assert breakdown.details == expected


@pytest.fixture
def cruncher():
    return MetricsCruncher()
