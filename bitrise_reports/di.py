# di.py

from . import cli
from .app import Application
from .bitrise import Bitrise
from .middleware import ProjectFinder, BuildsAnalyser
from .metrics import MetricsCruncher
from .reporting import StdoutReporter

FAKE_MODE = True


def inject(token, app, starting, ending):
    bitrise = Bitrise(token)
    finder = ProjectFinder(bitrise)
    analyser = BuildsAnalyser(bitrise, MetricsCruncher())
    criteria = cli.validate(app, starting, ending)
    reporter = StdoutReporter(criteria)
    return Application(finder, analyser, reporter, criteria)


class FakeApplication(object):
    def execute(self):
        print("Finshed fake app with success")
