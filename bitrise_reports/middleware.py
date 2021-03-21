# middleware.py

from bitrise_reports.errors import BitriseMiddlewareError

import logging

class ProjectSlugFinder(object):
    def __init__(self, bitrise):
        self.bitrise = bitrise

    def find(self, name):
        projects = self.bitrise.available_projects()
        target = next(filter(lambda project: project.id == name, projects), None)

        if not target:
            logging.error("Cannot locate projects with name {name}")
            logging.error("Available projects for this user")
            logging.error(projects)
            message = f"{name} not available in the projects this user has access"
            raise BitriseMiddlewareError(message)

        return target
