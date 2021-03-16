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


def test_onebuild_oneproject_permachine_breakdown(cruncher):

    # Given
    project = BitriseProject("android-flagship", "adb55be2718fc923")
    linuxMedium = BuildMachine("linux.elite", MachineSize.medium, BuildStack.linux)
    workflow = BitriseWorkflow("pull-request")

    builds = [BitriseBuild(project, linuxMedium, workflow, 20)]

    # When
    breakdown = cruncher.breakdown_per_machine(builds)

    # Then
    expected = {linuxMedium: BuildNumbers(count=1, minutes=20, credits=40)}

    assert breakdown.details == expected


def test_onebuild_oneproject_perworkfow_breakdown(cruncher):

    # Given
    project = BitriseProject("android-flagship", "adb55be2718fc923")
    linux = BuildMachine("linux.large", MachineSize.large, BuildStack.linux)
    workflow = BitriseWorkflow("pull-request")

    builds = [BitriseBuild(project, linux, workflow, 25)]

    # When
    breakdown = cruncher.breakdown_per_workflow(builds)

    # Then
    expected = {workflow: BuildNumbers(count=1, minutes=25, credits=100)}

    assert breakdown.details == expected


def test_onebuild_oneproject_perproject_breakdown(cruncher):

    # Given
    project = BitriseProject("android-flagship", "adb55be2718fc923")
    linux = BuildMachine("linux.large", MachineSize.large, BuildStack.linux)
    workflow = BitriseWorkflow("pull-request")

    builds = [BitriseBuild(project, linux, workflow, 30)]

    # When
    breakdown = cruncher.breakdown_per_project(builds)

    expected = {project: BuildNumbers(count=1, minutes=30, credits=120)}

    assert breakdown.details == expected


def test_oneproject_multiplebuilds_permachine_breakdown(cruncher):

    # Given
    project = BitriseProject("android-flagship", "adb55be2718fc923")
    linuxMedium = BuildMachine("linux.medium", MachineSize.medium, BuildStack.linux)
    linuxLarge = BuildMachine("linux.large", MachineSize.large, BuildStack.linux)

    builds = [
        BitriseBuild(project, linuxMedium, BitriseWorkflow("pull-request"), 10),
        BitriseBuild(
            project, linuxMedium, BitriseWorkflow("pull-request-parallel"), 10
        ),
        BitriseBuild(project, linuxLarge, BitriseWorkflow("pull-request"), 10),
        BitriseBuild(project, linuxLarge, BitriseWorkflow("pull-request-parallel"), 10),
    ]

    # When
    breakdown = cruncher.breakdown_per_machine(builds)

    # Then
    expected = {
        linuxMedium: BuildNumbers(count=2, minutes=20, credits=40),
        linuxLarge: BuildNumbers(count=2, minutes=20, credits=80),
    }

    assert breakdown.details == expected


def test_oneproject_multiplebuilds_perproject_breakdown(cruncher):

    # Given
    project = BitriseProject("android-flagship", "adb55be2718fc923")
    linux = BuildMachine("linux.medium", MachineSize.medium, BuildStack.linux)

    builds = [
        BitriseBuild(project, linux, BitriseWorkflow("pull-request"), 30),
        BitriseBuild(project, linux, BitriseWorkflow("pull-request-parallel"), 20),
        BitriseBuild(project, linux, BitriseWorkflow("qa-release"), 40),
        BitriseBuild(project, linux, BitriseWorkflow("internal-release"), 40),
    ]

    # When
    breakdown = cruncher.breakdown_per_project(builds)

    # Then
    expected = {project: BuildNumbers(count=4, minutes=130, credits=260)}

    assert breakdown.details == expected


def test_multiplebuilds_multipleprojects_permachine_breakdown(cruncher):

    # Given
    android = BitriseProject("android-machete", "be2755fc92318adb")
    ios = BitriseProject("number26ios", "dd4fd73cd3dfe98f")

    linuxMedium = BuildMachine("linux.medium", MachineSize.medium, BuildStack.linux)
    linuxLarge = BuildMachine("linux.large", MachineSize.large, BuildStack.linux)
    osxMedium = BuildMachine("macos.medium", MachineSize.medium, BuildStack.osx)

    builds = [
        BitriseBuild(android, linuxMedium, BitriseWorkflow("pull-request"), 25),
        BitriseBuild(android, linuxLarge, BitriseWorkflow("pull-request-parallel"), 15),
        BitriseBuild(android, linuxLarge, BitriseWorkflow("live-release"), 30),
        BitriseBuild(ios, osxMedium, BitriseWorkflow("regression"), 90),
        BitriseBuild(ios, osxMedium, BitriseWorkflow("pull-request"), 40),
        BitriseBuild(ios, osxMedium, BitriseWorkflow("test-flight"), 50),
    ]

    # When
    breakdown = cruncher.breakdown_per_machine(builds)

    # Then
    expected = {
        linuxMedium: BuildNumbers(count=1, minutes=25, credits=50),
        linuxLarge: BuildNumbers(count=2, minutes=45, credits=180),
        osxMedium: BuildNumbers(count=3, minutes=180, credits=720),
    }

    assert breakdown.details == expected


def test_multiplebuilds_multipleprojects_perproject_breakdown(cruncher):

    # Given
    android = BitriseProject("android-machete", "be2755fc92318adb")
    ios = BitriseProject("number26ios", "dd4fd73cd3dfe98f")

    linux = BuildMachine("linux.large", MachineSize.large, BuildStack.linux)
    osx = BuildMachine("macos.medium", MachineSize.medium, BuildStack.osx)

    builds = [
        BitriseBuild(android, linux, BitriseWorkflow("pull-request"), 25),
        BitriseBuild(android, linux, BitriseWorkflow("pull-request"), 20),
        BitriseBuild(android, linux, BitriseWorkflow("pull-request-parallel"), 15),
        BitriseBuild(android, linux, BitriseWorkflow("qa-release"), 30),
        BitriseBuild(android, linux, BitriseWorkflow("live-release"), 30),
        BitriseBuild(ios, osx, BitriseWorkflow("regression"), 90),
        BitriseBuild(ios, osx, BitriseWorkflow("pull-request"), 40),
        BitriseBuild(ios, osx, BitriseWorkflow("pull-request"), 30),
        BitriseBuild(ios, osx, BitriseWorkflow("test-flight"), 50),
    ]

    # When
    breakdown = cruncher.breakdown_per_project(builds)

    # Then
    expected = {
        android: BuildNumbers(count=5, minutes=120, credits=480),
        ios: BuildNumbers(count=4, minutes=210, credits=840),
    }

    assert breakdown.details == expected


def test_multiplebuilds_multipleprojects_workflow_breakdown(cruncher):

    # Given
    android = BitriseProject("android-machete", "be2755fc92318adb")
    ios = BitriseProject("number26ios", "dd4fd73cd3dfe98f")

    linux = BuildMachine("linux.large", MachineSize.large, BuildStack.linux)
    osx = BuildMachine("macos.medium", MachineSize.medium, BuildStack.osx)

    builds = [
        BitriseBuild(android, linux, BitriseWorkflow("pull-request"), 25),
        BitriseBuild(android, linux, BitriseWorkflow("pull-request"), 20),
        BitriseBuild(android, linux, BitriseWorkflow("pull-request-parallel"), 14),
        BitriseBuild(android, linux, BitriseWorkflow("pull-request-parallel"), 36),
        BitriseBuild(android, linux, BitriseWorkflow("live-release"), 30),
        BitriseBuild(ios, osx, BitriseWorkflow("regression"), 60),
        BitriseBuild(ios, osx, BitriseWorkflow("pull-request"), 40),
        BitriseBuild(ios, osx, BitriseWorkflow("pull-request"), 30),
    ]
    # When
    breakdown = cruncher.breakdown_per_workflow(builds)

    # Then
    expected = {
        BitriseWorkflow("pull-request"): BuildNumbers(
            count=4, minutes=115, credits=460
        ),
        BitriseWorkflow("pull-request-parallel"): BuildNumbers(
            count=2, minutes=50, credits=200
        ),
        BitriseWorkflow("live-release"): BuildNumbers(count=1, minutes=30, credits=120),
        BitriseWorkflow("regression"): BuildNumbers(count=1, minutes=60, credits=240),
    }

    assert breakdown.details == expected


@pytest.fixture
def cruncher():
    return MetricsCruncher()
