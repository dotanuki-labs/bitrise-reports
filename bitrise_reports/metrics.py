# metrics.py

from .models import (
    BitriseBreakdown,
    BuildMinutes,
    BuildStack,
    CrunchedNumbers,
    ExecutionStatus,
    MachineSize,
)

from itertools import groupby

LINUX_CREDITS_MULTIPLIER = {
    MachineSize.g1small: 1,
    MachineSize.g1medium: 2,
    MachineSize.g1large: 4,
}

OSX_CREDITS_MULTIPLIER = {
    MachineSize.g1small: 2,
    MachineSize.g1medium: 4,
    MachineSize.g2small: 2,
    MachineSize.g2medium: 4,
    MachineSize.g2large: 6,
}


class MetricsCruncher(object):
    def breakdown_per_project(self, builds):
        _, summary = self.__breakdown_builds(builds, lambda k: k.project)
        return BitriseBreakdown("Project Numbers", summary)

    def breakdown_per_machine(self, builds):
        _, summary = self.__breakdown_builds(builds, lambda k: k.machine)
        return BitriseBreakdown("Per machine", summary)

    def breakdown_per_workflow(self, builds):
        _, summary = self.__breakdown_builds(builds, lambda k: k.workflow)
        return BitriseBreakdown("Per Workflow", summary)

    def __breakdown_builds(self, builds, criteria):
        count = 0
        summary = {}

        for key, grouped in groupby(builds, criteria):
            total, minutes, successes, failures, abortions, credits = self.__analyse(grouped)

            if key not in summary.keys():
                numbers = CrunchedNumbers(0, 0, 0, 0, 0, 0, 0, 0)
                summary[key] = numbers

            actual = summary[key]

            updated = CrunchedNumbers(
                count=actual.count + total,
                queued=actual.queued + minutes.queued,
                building=actual.building + minutes.building,
                total=actual.total + minutes.total,
                successes=actual.successes + successes,
                failures=actual.failures + failures,
                abortions=actual.abortions + abortions,
                credits=actual.credits + credits,
            )

            summary[key] = updated
            count = count + total

        return count, summary

    def __analyse(self, builds):
        count = 0
        minutes = BuildMinutes(0, 0, 0)
        successes = 0
        failures = 0
        abortions = 0
        credits = 0

        for build in builds:
            count = count + 1
            minutes = self.__sum_minutes(minutes, build.minutes)
            successes = successes + 1 if build.status == ExecutionStatus.success else successes
            failures = failures + 1 if build.status == ExecutionStatus.error else failures
            abortions = abortions + 1 if build.status == ExecutionStatus.aborted else abortions
            credits = credits + self.__compute_credits(build)

        return [count, minutes, successes, failures, abortions, credits]

    def __sum_minutes(self, target, another):
        return BuildMinutes(
            target.queued + another.queued,
            target.building + another.building,
            target.total + another.total,
        )

    def __compute_credits(self, build):
        mac = build.machine.stack == BuildStack.osx
        multiplier = OSX_CREDITS_MULTIPLIER if mac else LINUX_CREDITS_MULTIPLIER
        return multiplier[build.machine.size] * build.minutes.total
