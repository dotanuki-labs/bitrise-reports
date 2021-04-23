# test_builds_analyser.py

from bitrise_reports.errors import ErrorCause, BitriseReportsError
from bitrise_reports.metrics import MetricsCruncher
from bitrise_reports.middleware import BuildsAnalyser
from bitrise_reports.models import (
    BitriseBuild,
    BuildMinutes,
    BitriseProject,
    BuildStack,
    MachineSize,
    BuildMachine,
    BitriseWorkflow,
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
    workflow = BitriseWorkflow("pull-request")
    builds = [
        BitriseBuild(project, machine, workflow, BuildMinutes(0, 0, 10)),
        BitriseBuild(project, machine, workflow, BuildMinutes(0, 0, 9)),
        BitriseBuild(project, machine, workflow, BuildMinutes(0, 0, 11)),
    ]

    bitrise = FakeBitrise([project], builds)
    analyser = BuildsAnalyser(bitrise, MetricsCruncher())

    # When
    breakdowns = analyser.analyse(project)

    # Then
    expected_breakdowns = 3
    assert len(breakdowns) == expected_breakdowns


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
