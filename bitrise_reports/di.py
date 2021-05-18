# di.py

from . import cli
from .app import Application
from .bitrise import Bitrise
from .middleware import ProjectFinder, BuildsAnalyser
from .metrics import MetricsCruncher
from .reporting import MetricsReporter
from .models import EvaluationCriteria


def inject(
    token,
    app,
    starting,
    ending,
    detailed_builds,
    detailed_timing,
    emulate_velocity,
    target_branch,
    report_style,
):

    bitrise = Bitrise(token)
    finder = ProjectFinder(bitrise)
    analyser = BuildsAnalyser(bitrise, MetricsCruncher(), target_branch)

    criteria = EvaluationCriteria(
        cli.validated_app(app),
        cli.validated_date(starting, include_hours=False),
        cli.validated_date(ending, include_hours=True),
    )

    report = cli.validated_report(report_style)
    reporter = MetricsReporter(criteria, detailed_builds, detailed_timing, emulate_velocity, report)

    return Application(finder, analyser, reporter, criteria)
