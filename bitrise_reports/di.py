# di.py

from . import cli
from .app import Application
from .bitrise import Bitrise
from .middleware import ProjectFinder, BuildsAnalyser
from .metrics import MetricsCruncher
from .reporting import MetricsReporter


def inject(token, app, starting, ending, output):
    bitrise = Bitrise(token)
    finder = ProjectFinder(bitrise)
    analyser = BuildsAnalyser(bitrise, MetricsCruncher())
    criteria = cli.validate(app, starting, ending)
    reporter = MetricsReporter(criteria, output)
    return Application(finder, analyser, reporter, criteria)
