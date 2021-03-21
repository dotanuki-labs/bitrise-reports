# middleware.py

from bitrise_reports.errors import BitriseMiddlewareError

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
            cause = f"{name} not present among projects you have access"
            raise BitriseMiddlewareError(cause)

        return target


class BuildsAnalyser(object):
    def __init__(self, bitrise, cruncher):
        self.bitrise = bitrise
        self.cruncher = cruncher

    def analyse(self, project, starting, ending):
        builds = self.bitrise.builds_for_project(project, starting, ending)

        if not builds:
            logging.error(f"Cannot locate find builds for project : {project.id}")
            cause = f"{project.id} has no builds yet"
            raise BitriseMiddlewareError(cause)

        breakdowns = [
            self.cruncher.breakdown_per_project(builds),
            self.cruncher.breakdown_per_machine(builds),
            self.cruncher.breakdown_per_workflow(builds),
        ]

        return breakdowns
