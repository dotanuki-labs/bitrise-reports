# test_project_slug_finder.py


from bitrise_reports.middleware import ProjectFinder
from bitrise_reports.errors import BitriseMiddlewareError
from bitrise_reports.models import BitriseProject

import pytest


class FakeBitrise(object):
    def __init__(self, apps):
        self.apps = apps

    def available_projects(self):
        return self.apps


def test_project_found():

    # Given
    apps = [
        BitriseProject("android-flagship", "a2b473cfa869c525"),
        BitriseProject("ios-flagship", "2e3c8224cf0952f7"),
    ]

    bitrise = FakeBitrise(apps)
    finder = ProjectFinder(bitrise)

    # When
    app = finder.find("android-flagship")

    # Then
    assert app == apps[0]


def test_project_not_found():

    # Given
    apps = [
        BitriseProject("android-flagship", "a2b473cfa869c525"),
        BitriseProject("ios-flagship", "2e3c8224cf0952f7"),
    ]

    bitrise = FakeBitrise(apps)
    finder = ProjectFinder(bitrise)

    with pytest.raises(Exception) as error:

        # When
        finder.find("android-flagship")

        # Then
        assert error is BitriseMiddlewareError
