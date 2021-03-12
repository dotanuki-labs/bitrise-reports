# test_bitrise.py

from bitrise_reports.bitrise import Bitrise, BITRISE_API_URL
from bitrise_reports.models import BitriseProject, BuildMinutes, BitriseBuild
from bitrise_reports.models import (
    BuildMachine,
    BuildStack,
    MachineSize,
    BitriseWorkflow,
)

import json
import responses


@responses.activate
def test_retrive_bitrise_projects():

    # Given
    apps = f"{BITRISE_API_URL}/apps"
    response = """
        {
            "data": [
                {
                    "slug": "a2b473cfa869c525",
                    "title": "android-flagship",
                    "project_type": "other",
                    "provider": "github",
                    "repo_owner": "disruptive",
                    "repo_url": "git@github.com:disruptive/android-flagship.git",
                    "repo_slug": "android-flagship",
                    "is_disabled": false,
                    "status": 1,
                    "is_public": false,
                    "owner": {
                        "account_type": "organization",
                        "name": "Disruptive Business Gmbh",
                        "slug": "4babd835c067be82"
                    },
                    "avatar_url": null
                },
                {
                    "slug": "2e3c8224cf0952f7",
                    "title": "ios-flagship",
                    "project_type": "other",
                    "provider": "github",
                    "repo_owner": "disruptive",
                    "repo_url": "git@github.com:disruptive/ios-flagship.git",
                    "repo_slug": "ios-flagship",
                    "is_disabled": false,
                    "status": 1,
                    "is_public": false,
                    "owner": {
                        "account_type": "organization",
                        "name": "Disruptive Business Gmbh",
                        "slug": "4babd835c067be82"
                    },
                    "avatar_url": null
                }
            ],
            "paging": {
                "total_item_count": 2,
                "page_item_limit": 50
            }
        }
    """

    responses.add(responses.GET, apps, json=json.loads(response), status=200)

    bitrise = Bitrise("fake-api-token")

    # When
    projects = bitrise.available_projects()

    # Then
    expected = [
        BitriseProject("android-flagship", "a2b473cfa869c525"),
        BitriseProject("ios-flagship", "2e3c8224cf0952f7"),
    ]

    assert projects == expected


@responses.activate
def test_retrive_builds_for_project():

    # Given
    project = BitriseProject("android-flagship", "f0a251acc3a5f5b7")
    endpoint = f"{BITRISE_API_URL}/apps/f0a251acc3a5f5b7/builds"

    response = """
        {
            "data": [
                {
                    "triggered_at": "2021-03-02T18:54:55Z",
                    "started_on_worker_at": "2021-03-02T18:54:55Z",
                    "environment_prepare_finished_at": "2021-03-02T18:54:55Z",
                    "finished_at": "2021-03-02T18:57:04Z",
                    "slug": "0e1fafb36766368d",
                    "status": 2,
                    "status_text": "error",
                    "abort_reason": null,
                    "is_on_hold": false,
                    "branch": "ufs/tests",
                    "build_number": 99999,
                    "commit_hash": "2c138116613c2941f69e3226eeb298a4ee5d73e8",
                    "commit_message": "Added tests",
                    "tag": null,
                    "triggered_workflow": "pull-request",
                    "triggered_by": "webhook",
                    "machine_type_id": "elite",
                    "stack_identifier": "linux-docker-android",
                    "original_build_params": {
                        "branch": "ufs/tests",
                        "workflow_id": "pull-request"
                    },
                    "pull_request_id": 0,
                    "pull_request_target_branch": null,
                    "pull_request_view_url": null,
                    "commit_view_url": null
                },
                {
                    "triggered_at": "2021-03-02T17:36:55Z",
                    "started_on_worker_at": "2021-03-02T17:36:55Z",
                    "environment_prepare_finished_at": "2021-03-02T17:36:55Z",
                    "finished_at": "2021-03-02T17:38:53Z",
                    "slug": "4fa1441c5406f543",
                    "status": 2,
                    "status_text": "error",
                    "abort_reason": null,
                    "is_on_hold": false,
                    "branch": "ufs/tests",
                    "build_number": 100000,
                    "commit_hash": "7e38e36ef723354fd6598c68b0ab57da7abd2b7e",
                    "commit_message": "Fixing wrong validation",
                    "tag": null,
                    "triggered_workflow": "pull-request",
                    "triggered_by": "webhook",
                    "machine_type_id": "elite",
                    "stack_identifier": "linux-docker-android",
                    "original_build_params": {
                        "branch": "ufs/tests",
                        "workflow_id": "pull-request"
                    },
                    "pull_request_id": 0,
                    "pull_request_target_branch": null,
                    "pull_request_view_url": null,
                    "commit_view_url": null
                }
            ],
            "paging": {
                "total_item_count": 2,
                "page_item_limit": 50
            }
        }
    """

    responses.add(responses.GET, endpoint, json=json.loads(response), status=200)

    bitrise = Bitrise("fake-api-token")

    # When
    builds = bitrise.builds_for_project(project)

    # Then
    linux = BuildMachine("linux.elite", MachineSize.medium, BuildStack.linux)
    workflow = BitriseWorkflow("pull-request")

    expected = [
        BitriseBuild(project, linux, workflow, BuildMinutes(0, 3, 3)),
        BitriseBuild(project, linux, workflow, BuildMinutes(0, 2, 2)),
    ]

    assert builds == expected
