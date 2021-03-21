# bitrise.py

from .errors import ErrorCause, BitriseIntegrationError, BitriseMiddlewareError
from .models import BitriseBuild, BitriseProject, BuildStack
from .models import BuildMachine, BuildMinutes, BitriseWorkflow, MachineSize

from datetime import datetime
from math import ceil

import logging
import requests

BITRISE_API_URL = "https://api.bitrise.io/v0.1"
FIRST_PAGE = "first-page"
NO_MORE_PAGES = "no-more-pages"


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


class Bitrise(object):
    def __init__(self, api_token):
        self.api = BitriseApiFetcher(api_token)
        self.converter = RawDataConverter()

    def available_projects(self):
        endpoint = f"{BITRISE_API_URL}/apps"
        raw_data = self.api.get(endpoint)
        return self.converter.projects_from(raw_data)

    def builds_for_project(self, project):
        endpoint = f"{BITRISE_API_URL}/apps/{project.slug}/builds"
        raw_data = self.api.get(endpoint)
        return self.converter.builds_from(raw_data, project)


class BitriseApiFetcher(object):
    def __init__(self, api_token):
        self.auth = {"Authorization": api_token}

    def get(self, endpoint, starting=None, ending=None):
        results = []
        next = FIRST_PAGE

        params = {}

        if starting:
            params["after"] = starting

        if ending:
            params["before"] = ending

        while next != NO_MORE_PAGES:

            if next != FIRST_PAGE:
                params["next"] = next

            fetched, next_page = self.__get_page(endpoint, params)
            results.extend(fetched)
            next = next_page

        return results

    def __get_page(self, endpoint, args=None):
        response = requests.get(endpoint, headers=self.auth, params=args)

        if response.status_code == requests.codes.ok:
            data = response.json()["data"]
            paging = response.json()["paging"]
            next = paging["next"] if "next" in paging.keys() else NO_MORE_PAGES
            return data, next
        else:
            raise BitriseIntegrationError(ErrorCause.Http)


class RawDataConverter(object):
    def projects_from(self, json):
        def conversion(json, project):
            return [BitriseProject(item["title"], item["slug"]) for item in json]

        return self.__safely_convert(conversion, json)

    def builds_from(self, json, project):
        def conversion(json, project):
            finished_builds = list(
                filter(lambda raw: raw["finished_at"] is not None, json)
            )
            return [self.build_from(item, project) for item in finished_builds]

        return self.__safely_convert(conversion, json, project)

    def __safely_convert(self, callable, json, project=None):
        try:
            return callable(json, project)
        except Exception as e:
            print(e)
            logging.exception("An exception occurred")
            logging.error("Could not parse/convert information from builds")
            raise BitriseIntegrationError(ErrorCause.ApiDataConversion)

    def build_from(self, json, project):
        machine = self.machine_from(json["machine_type_id"], json["stack_identifier"])
        workflow = self.workflow_from(json["triggered_workflow"], project)
        minutes = self.minutes_from(
            json["triggered_at"], json["started_on_worker_at"], json["finished_at"]
        )
        return BitriseBuild(project, machine, workflow, minutes)

    def machine_from(self, machine_type_id, stack_identifier):
        size = MachineSize(machine_type_id)
        stack = BuildStack("macos" if "osx" in stack_identifier else "linux")
        return BuildMachine(f"{stack.value}.{size.value}", size, stack)

    def workflow_from(self, triggered_workflow, bitrise_project):
        return BitriseWorkflow(triggered_workflow)

    def minutes_from(self, triggered_at, started_at, finished_at):
        triggered = datetime.fromisoformat(triggered_at.replace("Z", ""))
        started = datetime.fromisoformat(triggered_at.replace("Z", ""))
        finished = datetime.fromisoformat(finished_at.replace("Z", ""))
        queued = self.__aproximate_minutes(started - triggered)
        building = self.__aproximate_minutes(finished - started)
        total = self.__aproximate_minutes(finished - triggered)
        return BuildMinutes(queued, building, total)

    def __aproximate_minutes(self, diff):
        return ceil((diff.days * 24 * 60) + (diff.seconds / 60))
