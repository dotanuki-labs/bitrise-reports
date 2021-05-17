# test_builds_analyser.py

from bitrise_reports.errors import ErrorCause, BitriseReportsError
from bitrise_reports.metrics import MetricsCruncher
from bitrise_reports.middleware import BuildsAnalyser
from bitrise_reports.models import (
    BitriseBuild,
    BuildMachine,
    BuildMinutes,
    BuildStack,
    BitriseProject,
    BitriseWorkflow,
    ExecutionStatus,
    MachineSize,
)

import pytest


class FakeBitrise(object):
    def __init__(self, apps, builds):
        self.apps = apps
        self.builds = builds

    def available_projects(self):
        return self.apps

    def builds_for_project(self, project, starting, ending):
        return self.builds


def test_builds_analysed_with_success():

    # Given
    project = BitriseProject("android-flagship", "a2b473cfa869c525")
    machine = BuildMachine("linux.elite-xl", MachineSize.g1large, BuildStack.linux)
    workflow = BitriseWorkflow("checks")
    status = ExecutionStatus.success

    builds = [
        BitriseBuild(project, machine, workflow, BuildMinutes(0, 0, 10), status),
        BitriseBuild(project, machine, workflow, BuildMinutes(0, 0, 9), status),
        BitriseBuild(project, machine, workflow, BuildMinutes(0, 0, 11), status),
    ]

    bitrise = FakeBitrise([project], builds)
    analyser = BuildsAnalyser(bitrise, MetricsCruncher())

    # When
    breakdowns, analysed_builds = analyser.analyse(project)

    # Then
    assert len(breakdowns) == 3
    assert analysed_builds == 3


def test_builds_analysed_with_for_target_branch():

    # Given
    project = BitriseProject("android-flagship", "a2b473cfa869c525")
    machine = BuildMachine("linux.elite-xl", MachineSize.g1large, BuildStack.linux)
    workflow = BitriseWorkflow("checks")
    status = ExecutionStatus.success
    target_branch = "main"

    builds = [
        BitriseBuild(project, machine, workflow, BuildMinutes(0, 0, 50), status, "main"),
        BitriseBuild(project, machine, workflow, BuildMinutes(0, 0, 52), status, "main"),
        BitriseBuild(project, machine, workflow, BuildMinutes(0, 0, 51), status, "new-feature"),
    ]

    bitrise = FakeBitrise([project], builds)
    analyser = BuildsAnalyser(bitrise, MetricsCruncher(), target_branch)

    # When
    breakdowns, analysed_builds = analyser.analyse(project)

    # Then
    assert len(breakdowns) == 3
    assert analysed_builds == 2


def test_builds_analysed_failed():

    # Given
    project = BitriseProject("android-flagship", "a2b473cfa869c525")
    builds = []

    bitrise = FakeBitrise([project], builds)
    analyser = BuildsAnalyser(bitrise, MetricsCruncher())

    with pytest.raises(Exception) as error:

        # When
        analyser.analyse(project)

        # Then
        # Then
        assert error is BitriseReportsError
        assert error.cause == ErrorCause.MiddlewareOrchestration
