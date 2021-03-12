# test_data_converter.py

from bitrise_reports.models import BitriseProject, BitriseBuild, BuildMinutes
from bitrise_reports.models import (
    BuildStack,
    MachineSize,
    BuildMachine,
    BitriseWorkflow,
)
from bitrise_reports.bitrise import RawDataConverter

import pytest


@pytest.mark.parametrize(
    "machine_type_id,stack_id,id,size,stack",
    [
        (
            "elite",
            "osx-xcode-12.0.x",
            "macos.elite",
            MachineSize.medium,
            BuildStack.osx,
        ),
        (
            "elite-xl",
            "android-docker-linux",
            "linux.elite-xl",
            MachineSize.large,
            BuildStack.linux,
        ),
        (
            "standard",
            "android-docker-linux",
            "linux.standard",
            MachineSize.small,
            BuildStack.linux,
        ),
    ],
)
def test_convert_machines(machine_type_id, stack_id, id, size, stack):
    converter = RawDataConverter()

    converted = converter.machine_from(machine_type_id, stack_id)

    expected = BuildMachine(id, size, stack)
    assert converted == expected


def test_convert_workflow():
    converter = RawDataConverter()
    project = BitriseProject("my-project", "c92318adbbe2755f")
    workflow = "pull-request"

    converted = converter.workflow_from(workflow, project)

    expected = BitriseWorkflow("pull-request")
    assert converted == expected


def test_convert_minutes():
    converter = RawDataConverter()

    triggered_at = "2021-03-01T09:05:52Z"
    started_at = "2021-03-01T09:06:42Z"
    finished_at = "2021-03-01T09:16:45Z"

    converted = converter.minutes_from(triggered_at, started_at, finished_at)

    queued = 0
    building = 11
    total = 11
    assert converted == BuildMinutes(queued, building, total)


def convert_bitrise_build():
    converter = RawDataConverter()
    android = BitriseProject("my-project", "c92318adbbe2755f")

    build = {
        "triggered_at": "2021-03-01T09:05:22Z",
        "started_on_worker_at": "2021-03-01T09:06:33Z",
        "finished_at": "2021-03-01T09:35:45Z",
        "machine_type_id": "elite-xl",
        "stack_identifier": "android-docker-linux",
        "triggered_workflow": "espresso-tests",
    }

    converted = converter.convert_build(build, android)

    expected = BitriseBuild(
        project=android,
        machine=BuildMachine(MachineSize.medium, BuildStack.osx),
        workflow=BitriseWorkflow("espresso-tests"),
        minutes=BuildMinutes(1, 35, 36),
    )

    assert converted == expected
