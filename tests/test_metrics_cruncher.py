# test_metrics_cruncher.py

from bitrise_reports.models import BitriseProject, BitriseBuild, BuildNumbers
from bitrise_reports.models import BuildStack, MachineSize, BuildMachine, BitriseWorkflow
from bitrise_reports.metrics import MetricsCruncher


def test_onebuild_oneproject_permachine_breakdown():

    # Given
    project = BitriseProject('android-flagship', 'adb55be2718fc923')
    linuxMedium = BuildMachine('linux.elite', MachineSize.medium, BuildStack.linux)
    workflow = BitriseWorkflow('pull-request')

    builds = [
        BitriseBuild(project, linuxMedium, workflow, 20)
    ]

    cruncher = MetricsCruncher()

    # When
    breakdown = cruncher.breakdown_per_machine(builds)

    # Then
    expected = {
        linuxMedium: BuildNumbers(count=1, minutes=20, credits=40)
    }

    assert breakdown.details == expected
