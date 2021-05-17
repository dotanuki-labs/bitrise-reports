# di.py

from . import cli
from .app import Application
from .bitrise import Bitrise
from .middleware import ProjectFinder, BuildsAnalyser
from .metrics import MetricsCruncher
from .reporting import MetricsReporter
from .models import EvaluationCriteria


def inject(token, app, starting, ending, branch, velocity, statuses, report):

    bitrise = Bitrise(token)
    finder = ProjectFinder(bitrise)
    analyser = BuildsAnalyser(bitrise, MetricsCruncher(), branch)

    criteria = EvaluationCriteria(
        cli.validated_app(app),
        cli.validated_date(starting, include_hours=False),
        cli.validated_date(ending, include_hours=True),
    )

    reporter = MetricsReporter(criteria, velocity, statuses, cli.validated_report(report))

    return Application(finder, analyser, reporter, criteria)
