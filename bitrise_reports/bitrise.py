# bitrise.py

from .errors import ErrorCause, BitriseIntegrationError
from .models import BitriseBuild, BitriseProject, BuildStack
from .models import BuildMachine, BuildMinutes, BitriseWorkflow, MachineSize

from datetime import datetime
from math import ceil

import logging
import requests

BITRISE_API = 'https://api.bitrise.io/v0.1'
FIRST_PAGE = 'first-page'
NO_MORE_PAGES = 'no-more-pages'


# class BuildsRetriever(object):

#     def __init__(self, api_token=None, api_url=BITRISE_API):
#         self.api_url = api_url
#         self.api = BitriseApiFetcher(api_token)
#         self.converter = RawDataConverter()

#     def available_apps(self):
#         endpoint = f"{self.api_url}/apps"
#         raw_data = self.api.get(endpoint, self.auth)
#         return self.converter.projects_from(raw_data)

#     def builds_for_project(self, project):
#         endpoint = f"{self.api_url}/apps/{project.slug}/builds"
#         raw_data = self.api.get(endpoint, self.auth)
#         return self.converter.builds_from(raw_data)


class BitriseApiFetcher(object):

    def __init__(self, api_token):
        self.auth = {'Authorization': api_token}

    def get_paged(self, endpoint):
        results = []
        next = FIRST_PAGE

        while next != NO_MORE_PAGES:
            params = None if next == FIRST_PAGE else {'next': next}
            fetched, next_page = self.get(endpoint, params)
            results.extend(fetched)
            next = next_page

        return results

    def get(self, endpoint, args=None):
        response = requests.get(endpoint, headers=self.auth, params=args)
        if response.status_code == requests.codes.ok:
            data = response.json()['data']
            paging = response.json()['paging']
            next = paging['next'] if 'next' in paging.keys() else NO_MORE_PAGES
            return data, next
        else:
            raise BitriseIntegrationError(ErrorCause.Http)


class RawDataConverter(object):

    def projects_from(self, json):
        try:
            return [BitriseProject(item['title'], item['slug']) for item in json['data']]
        except:
            logging.exception("An exception occurred")
            logging.error("Could not parse/convert information from projects")
            raise BitriseIntegrationError(ErrorCause.ApiDataConversion)

    def builds_from(self, json, project):
        try:
            finished_builds = list(filter(lambda raw: raw['finished_at'] is not None, json['data']))
            next = json['paging']['next'] if 'next' in json['paging'].keys() else NO_MORE_PAGES
            converted = [self.single_build(item, project) for item in finished_builds]
            return converted, next
        except:
            logging.exception("An exception occurred")
            logging.error("Could not parse/convert information from builds")
            raise BitriseIntegrationError(ErrorCause.ApiDataConversion)

    def build_from(self, json, project):
        machine = self.machine(json['machine_type_id'], json['stack_identifier'])
        workflow = self.bitrise_workflow(json['triggered_workflow'], project)
        minutes = self.minutes(json['triggered_at'], json['started_on_worker_at'], json['finished_at'])
        return BitriseBuild(project, machine, workflow, minutes)

    def machine_from(self, machine_type_id, stack_identifier):
        size = MachineSize(machine_type_id)
        stack = BuildStack('macos' if 'osx' in stack_identifier else 'linux')
        return BuildMachine(f"{stack.value}.{size.value}", size, stack)

    def workflow_from(self, triggered_workflow, bitrise_project):
        return BitriseWorkflow(triggered_workflow)

    def minutes_from(self, triggered_at, started_at, finished_at):
        triggered = datetime.fromisoformat(triggered_at.replace('Z',''))
        started = datetime.fromisoformat(triggered_at.replace('Z',''))
        finished = datetime.fromisoformat(finished_at.replace('Z',''))
        queued = self.__aproximate_minutes(started - triggered)
        building = self.__aproximate_minutes(finished - started)
        total = self.__aproximate_minutes(finished - triggered)
        return BuildMinutes(queued, building, total)

    def __aproximate_minutes(self, diff):
        return ceil((diff.days * 24 * 60) + (diff.seconds / 60))
