# middleware.py

from .errors import ErrorCause, BitriseReportsError

import logging


class ProjectFinder(object):
    def __init__(self, bitrise):
        self.bitrise = bitrise

    def find(self, name):
        projects = self.bitrise.available_projects()
        target = next(filter(lambda project: project.id == name, projects), None)

        if not target:
            logging.error("Cannot locate an app with name: {name}")
            logging.error("Available projects for this user")
            logging.error(projects)
            cause = ErrorCause.MiddlewareOrchestration
            message = f"{name} not present among projects you have access"
            raise BitriseReportsError(cause, message)

        return target


class BuildsAnalyser(object):
    def __init__(self, bitrise, cruncher, target_branch=None):
        self.bitrise = bitrise
        self.cruncher = cruncher
        self.target_branch = target_branch

    def analyse(self, project, starting=None, ending=None):
        all_builds = self.bitrise.builds_for_project(project, starting, ending)
        target_builds = self.__prune(all_builds)

        if not target_builds:
            message = f"Missing builds for project : {project.id} and branch : {self.target_branch}"
            logging.error(message)
            cause = f"{project.id} has no builds matching criteria"
            message = f"{project.id} has no builds matching criteria"
            raise BitriseReportsError(cause, message)

        breakdowns = [
            self.cruncher.breakdown_per_project(target_builds),
            self.cruncher.breakdown_per_machine(target_builds),
            self.cruncher.breakdown_per_workflow(target_builds),
        ]

        return breakdowns, len(target_builds)

    def __prune(self, builds):
        if self.target_branch is None:
            return builds
        return list(filter(lambda build: build.head_branch == self.target_branch, builds))
