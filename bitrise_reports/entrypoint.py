# app.py


from . import di
from .errors import BitriseReportsError

import click
import logging
import sys

APP_HELP = "The title of your app in Bitrise"
ENDING_HELP = "Ending date to drive the analysis (YYYY-MM-DD)"
START_HELP = "Starting date to drive the analysis (YYYY-MM-DD)"
BITRISE_PAT_HELP = "A Personal Access Token (PAT) for Bitrise API"
VELOCITY_HELP = "Estimate Bitrise Velocity credits related to builds"
OUTPUT_HELP = "The style of report you want (stdout | json | excel). Defaults to stdout"

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("--token", required=True, help=BITRISE_PAT_HELP)
@click.option("--app", required=True, help=APP_HELP)
@click.option("--starting", required=True, help=START_HELP)
@click.option("--ending", required=True, help=ENDING_HELP)
@click.option("--velocity", is_flag=True, default=False, help=VELOCITY_HELP)
@click.option("--report", required=False, default="stdout", help=OUTPUT_HELP)
def launch(token, app, starting, ending, velocity, report):
    try:
        app = di.inject(token, app, starting, ending, velocity, report)
        app.execute()
        sys.exit(0)
    except Exception as error:
        logging.exception("Could not complete analysis. Aborting.")
        if error is BitriseReportsError:
            logging.error(error.message)
        else:
            logging.error(error)
        sys.exit(1)
