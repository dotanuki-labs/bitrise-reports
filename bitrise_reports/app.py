# app.py


from . import cli

import click
import logging
import sys

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


@click.command()
@click.option("--app", required=True, help="The title of your app in Bitrise")
@click.option("--starting", required=True, help="Starting date to drive the analysis (YYYY-MM-DD)")
@click.option("--ending", required=True, help="Ending date to drive the analysis (YYYY-MM-DD)")
def launch(app, starting, ending):
    try:
        criteria = cli.parse_criteria(app, starting, ending)
        LOG.info(f"{criteria}")
        sys.exit(0)
    except Exception as e:
        LOG.exception("Could not complete analysis. Aborting.")
        LOG.error(e)
        sys.exit(1)
