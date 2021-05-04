# test_json_reporter.py


from bitrise_reports.models import EvaluationCriteria
from bitrise_reports.reporting import JsonReporter

from bitrise_reports.models import (
    BitriseBreakdown,
    BuildMachine,
    BitriseProject,
    BuildStack,
    BitriseWorkflow,
    CrunchedNumbers,
    MachineSize,
)

from datetime import datetime
from rich.console import Console

import json
import pytest


EVALUATION = EvaluationCriteria(
    bitrise_app="android-flagship",
    starting_at=datetime(2021, 2, 1),
    ending_at=datetime(2021, 2, 15),
)


def test_project_report(json_reporter):

    # Given
    project = BitriseProject("android-flagship", "adb55be2718fc923")
    numbers = CrunchedNumbers(count=1, queued=0, building=20, total=20, credits=40)
    details = {project: numbers}
    name = "Project Numbers"
    breakdowns = [BitriseBreakdown(name, details)]

    # When
    json_reporter.report(breakdowns)

    # Then
    report_path = f"{json_reporter.folder}/{json_reporter.filename}"

    expected = [
        {
            "description": "Project Numbers",
            "details": [
                {
                    "name": "android-flagship",
                    "count": 1,
                    "queued": 0,
                    "building": 20,
                    "total": 20,
                }
            ],
        }
    ]

    with open(report_path) as written:
        reported = json.load(written)
        assert reported == expected


def test_report_per_machine(json_reporter):

    # Given
    linux = BuildMachine("linux.g1large", MachineSize.g1medium, BuildStack.linux)
    mac = BuildMachine("mac.g1medium", MachineSize.g1large, BuildStack.linux)
    android_numbers = CrunchedNumbers(count=10, queued=0, building=30, total=30, credits=120)
    ios_numbers = CrunchedNumbers(count=5, queued=0, building=40, total=40, credits=160)

    details = {linux: android_numbers, mac: ios_numbers}
    name = "Per Machine"
    breakdowns = [BitriseBreakdown(name, details)]

    # When
    json_reporter.report(breakdowns)

    # Then
    report_path = f"{json_reporter.folder}/{json_reporter.filename}"

    expected = [
        {
            "description": "Per Machine",
            "details": [
                {
                    "name": "linux.g1large",
                    "count": 10,
                    "queued": 0,
                    "building": 30,
                    "total": 30,
                },
                {
                    "name": "mac.g1medium",
                    "count": 5,
                    "queued": 0,
                    "building": 40,
                    "total": 40,
                },
            ],
        }
    ]

    with open(report_path) as written:
        reported = json.load(written)
        assert reported == expected


def test_report_per_workflow(json_reporter):

    # Given
    unit_tests = BitriseWorkflow("unit-tests")
    code_checks = BitriseWorkflow("static-analysis")

    test_numbers = CrunchedNumbers(count=8, queued=0, building=20, total=20, credits=100)
    checks_numbers = CrunchedNumbers(count=5, queued=5, building=25, total=30, credits=120)

    details = {unit_tests: test_numbers, code_checks: checks_numbers}
    name = "Per Workflow"
    breakdowns = [BitriseBreakdown(name, details)]

    # When
    json_reporter.report(breakdowns)

    # Then
    report_path = f"{json_reporter.folder}/{json_reporter.filename}"

    expected = [
        {
            "description": "Per Workflow",
            "details": [
                {
                    "name": "unit-tests",
                    "count": 8,
                    "queued": 0,
                    "building": 20,
                    "total": 20,
                },
                {
                    "name": "static-analysis",
                    "count": 5,
                    "queued": 5,
                    "building": 25,
                    "total": 30,
                },
            ],
        }
    ]

    with open(report_path) as written:
        reported = json.load(written)
        assert reported == expected


@pytest.fixture
def json_reporter(tmpdir):
    return JsonReporter(
        criteria=EVALUATION,
        velocity=False,
        statuses=False,
        console=Console(),
        folder=tmpdir
    )
