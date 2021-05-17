# bitrise.py

from .errors import ErrorCause, BitriseReportsError
from .models import BitriseBuild, BitriseProject, BuildStack, ExecutionStatus
from .models import BuildMachine, BuildMinutes, BitriseWorkflow, MachineSize

from datetime import datetime
from math import ceil

import requests
import time

BITRISE_API_URL = "https://api.bitrise.io/v0.1"
FIRST_PAGE = "first-page"
NO_MORE_PAGES = "no-more-pages"


class Bitrise(object):
    def __init__(self, api_token):
        self.api = BitriseApiFetcher(api_token)
        self.converter = RawDataConverter()

    def available_projects(self):
        endpoint = f"{BITRISE_API_URL}/apps"
        raw_data = self.api.get(endpoint)
        return self.converter.projects_from(raw_data)

    def builds_for_project(self, project, starting=None, ending=None):
        endpoint = f"{BITRISE_API_URL}/apps/{project.slug}/builds"
        raw_data = self.api.get(endpoint, starting, ending)
        return self.converter.builds_from(raw_data, project)


class BitriseApiFetcher(object):
    def __init__(self, api_token):
        self.auth = {"Authorization": api_token}

    def get(self, endpoint, starting=None, ending=None):
        results = []
        next = FIRST_PAGE

        params = {}

        if starting:
            params["after"] = self.__unixtime(starting)

        if ending:
            params["before"] = self.__unixtime(ending)

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
            cause = ErrorCause.NetworkingInfrastructure
            message = f"""
            Error when retriving data from : {endpoint}
            Status = {response.status_code}
            """
            raise BitriseReportsError(cause, message)

    def __unixtime(self, datetime):
        return int(time.mktime(datetime.timetuple()))


class RawDataConverter(object):
    def projects_from(self, json):
        def conversion(json, project):
            return [BitriseProject(item["title"], item["slug"]) for item in json]

        return self.__safely_convert(conversion, json)

    def builds_from(self, json, project):
        def conversion(json, project):
            finished_builds = list(filter(lambda raw: raw["finished_at"] is not None, json))
            return [self.build_from(item, project) for item in finished_builds]

        return self.__safely_convert(conversion, json, project)

    def __safely_convert(self, callable, json, project=None):
        try:
            return callable(json, project)
        except:
            cause = ErrorCause.DataConversion
            message = "Could not parse/convert information from builds"
            raise BitriseReportsError(cause, message)

    def build_from(self, json, project):
        machine = self.machine_from(json["machine_type_id"], json["stack_identifier"])
        workflow = self.workflow_from(json["triggered_workflow"], project)
        minutes = self.minutes_from(
            json["triggered_at"], json["started_on_worker_at"], json["finished_at"]
        )

        status = self.status_from(json["status"])
        branch = self.branch_from(json["original_build_params"])
        return BitriseBuild(project, machine, workflow, minutes, status, branch)

    def machine_from(self, machine_type_id, stack_identifier):
        size = MachineSize(machine_type_id)
        stack = BuildStack("macos" if "osx" in stack_identifier else "linux")
        return BuildMachine(f"{stack.value}.{size.value}", size, stack)

    def workflow_from(self, triggered_workflow, bitrise_project):
        return BitriseWorkflow(triggered_workflow)

    def minutes_from(self, triggered_at, started_at, finished_at):
        triggered = self.__dt(triggered_at)
        started = self.__dt(started_at) if started_at is not None else triggered
        finished = self.__dt(finished_at)
        queued = self.__aproximate_minutes(started - triggered)
        building = self.__aproximate_minutes(finished - started)
        total = self.__aproximate_minutes(finished - triggered)
        return BuildMinutes(queued, building, total)

    def status_from(self, status):
        return ExecutionStatus(status) if status in range(1, 3) else ExecutionStatus.other

    def branch_from(self, build_parameters):
        return None if build_parameters is None else build_parameters["branch"]

    def __dt(self, timestamp):
        return datetime.fromisoformat(timestamp.replace("Z", ""))

    def __aproximate_minutes(self, diff):
        return ceil((diff.days * 24 * 60) + (diff.seconds / 60))
