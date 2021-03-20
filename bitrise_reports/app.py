# app.py


from . import cli

import click
import logging
import sys

APP_HELP = "The title of your app in Bitrise"
ENDING_HELP = "Ending date to drive the analysis (YYYY-MM-DD)"
START_HELP = "Starting date to drive the analysis (YYYY-MM-DD)"
TOKEN_HELP = "A Personal Access Token for Bitrise API"

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


@click.command()
@click.option("--token", required=True, help=TOKEN_HELP)
@click.option("--app", required=True, help=APP_HELP)
@click.option("--starting", required=True, help=START_HELP)
@click.option("--ending", required=True, help=ENDING_HELP)
def launch(token, app, starting, ending):
    try:
        criteria = cli.parse_criteria(app, starting, ending)
        LOG.info(f"{criteria}")
        sys.exit(0)
    except Exception as e:
        LOG.exception("Could not complete analysis. Aborting.")
        LOG.error(e)
        sys.exit(1)
