# app.py


from . import di

import click
import logging
import sys

HELP_APP = "The title of your app in Bitrise"
HELP_ENDING_DATE = "Ending date to drive the analysis (YYYY-MM-DD)"
HELP_STARTING_DATE = "Starting date to drive the analysis (YYYY-MM-DD)"
HELP_BITRISE_PAT = "A Personal Access Token (PAT) for Bitrise API"
HELP_VELOCITY = "Estimate Bitrise Velocity credits related to builds"
HELP_BUILDS = "Details all statusus for all builds (success, failure and aborted)"
HELP_TIMING = "Expand show also queued and building time for all builds"
HELP_REPORT_STYLE = "The style of report you want (stdout | json | excel). Defaults to stdout"
HELP_TARGET_BRANCH = "The target branch to perform the analysis"

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("--token", required=True, help=HELP_BITRISE_PAT)
@click.option("--app", required=True, help=HELP_APP)
@click.option("--starting", required=True, help=HELP_STARTING_DATE)
@click.option("--ending", required=True, help=HELP_ENDING_DATE)
@click.option("--detailed-builds", is_flag=True, default=False, help=HELP_BUILDS)
@click.option("--detailed-timing", is_flag=True, default=False, help=HELP_TIMING)
@click.option("--emulate-velocity", is_flag=True, default=False, help=HELP_VELOCITY)
@click.option("--target-branch", required=False, default=None, help=HELP_TARGET_BRANCH)
@click.option("--report-style", required=False, default="stdout", help=HELP_REPORT_STYLE)
def launch(
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
    app = di.inject(
        token,
        app,
        starting,
        ending,
        detailed_builds,
        detailed_timing,
        emulate_velocity,
        target_branch,
        report_style,
    )
    app.execute()
    sys.exit(0)
