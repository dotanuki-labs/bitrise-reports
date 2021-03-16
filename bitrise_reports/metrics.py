from .errors import BitriseMetricsExtractionError
from .models import BitriseBreakdown, BuildNumbers, BuildStack, MachineSize

from itertools import groupby

MACHINE_SIZE_CREDITS_MULTIPLIER = {
    MachineSize.small: 1,
    MachineSize.medium: 2,
    MachineSize.large: 4
}

MACHINE_TYPE_CREDITS_MULTIPLIER = {
    BuildStack. linux: 1,
    BuildStack. osx: 2
}


class MetricsCruncher(object):

    def breakdown_per_project(self, builds):
        count, summary = self.__breakdown_builds(builds, lambda k: k.project)
        return BitriseBreakdown('Project Numbers', summary)

    def breakdown_per_machine(self, builds):
        count, summary = self.__breakdown_builds(builds, lambda k: k.machine)
        return BitriseBreakdown('Breakdown per machine', summary)

    def breakdown_per_workflow(self, builds):
        count, summary = self.__breakdown_builds(builds, lambda k: k.workflow)
        return BitriseBreakdown('Breakdown per Workflow', summary)

    def __breakdown_builds(self, builds, criteria):
        count = 0
        summary = {}

        for key, grouped in groupby(builds, criteria):
            total, minutes, credits = self.__analyse(grouped)

            if key not in summary.keys():
                summary[key] = BuildNumbers(0, 0, 0)

            actual = summary[key]

            updated = BuildNumbers(
                count=actual.count + total,
                minutes=actual.minutes + minutes,
                credits=actual.credits + credits
            )

            summary[key] = updated
            count = count + total

        return count, summary

    def __analyse(self, builds):
        count = 0
        minutes = 0
        credits = 0

        for build in builds:
            count = count + 1
            minutes = minutes + build.duration
            credits = credits + self.__compute_credits(build)

        return [count, minutes, credits]

    def __compute_credits(self, build):
        machine_type = MACHINE_TYPE_CREDITS_MULTIPLIER[build.machine.stack]
        machine_size = MACHINE_SIZE_CREDITS_MULTIPLIER[build.machine.size]

        if machine_type is None or machine_size is None:
            error_message = f"Missing multiplier for {build.machine.size} | {build.machine.stack}"
            raise BitriseMetricsExtractionError(error_message)

        return machine_type * machine_size * build.duration
