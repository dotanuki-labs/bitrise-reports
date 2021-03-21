# app.py


from . import di

import click
import logging
import sys

APP_HELP = "The title of your app in Bitrise"
ENDING_HELP = "Ending date to drive the analysis (YYYY-MM-DD)"
START_HELP = "Starting date to drive the analysis (YYYY-MM-DD)"
BITRISE_PAT_HELP = "A Personal Access Token (PAT) for Bitrise API"

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("--token", required=True, help=BITRISE_PAT_HELP)
@click.option("--app", required=True, help=APP_HELP)
@click.option("--starting", required=True, help=START_HELP)
@click.option("--ending", required=True, help=ENDING_HELP)
def launch(token, app, starting, ending):
    try:
        app = di.inject(token, app, starting, ending)
        app.execute()
        sys.exit(0)
    except Exception as e:
        logging.exception("Could not complete analysis. Aborting.")
        logging.error(e)
        sys.exit(1)


class Application(object):
    def __init__(self, finder, analyser, reporter, criteria):
        self.project_finder = finder
        self.project_analyser = analyser
        self.results_reporter = reporter
        self.execution_criteria = criteria

    def execute(self):
        bitrise_app, starting, ending = self.criteria
        project = self.project_finder.find(bitrise_app)
        breakdowns = self.project_analyser.analyse(project, starting, ending)
        self.results_reporter.report(breakdowns, starting, ending)
