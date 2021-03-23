# reporting.py

from dataclasses import asdict
from rich.console import Console
from rich.table import Table

import json
import os


class MetricsReporter:
    def __init__(self, dates, strategy, console=Console()):
        self.dates = dates
        self.contextual_delegate = ContextReporter(dates, console)
        self.output_delegate = self.__find_delegate(strategy, dates, console)

    def started(self, app):
        self.contextual_delegate.started(app)

    def feedback(self, project):
        self.contextual_delegate.feedback(project)

    def report(self, breakdowns):
        self.output_delegate.report(breakdowns)

    def __find_delegate(self, strategy, dates, console):
        delegates = {
            "stdout": StdoutReporter(dates, console),
            "json": JsonReporter(dates, console),
        }
        return delegates[strategy]


class ContextReporter:
    def __init__(self, dates, console):
        self.dates = dates
        self.console = console

    def started(self, app):
        self.__print("\nAnalysing", app, "cyan")

    def feedback(self, project):
        self.__print("\nFound slug", project.slug, "cyan")
        self.__print("Starting", self.__format_date(self.dates.starting_at), "pink")
        self.__print("Ending  ", self.__format_date(self.dates.ending_at), "pink")

    def __print(self, prefix, content, color):
        printer = self.console
        printer.print(f"{prefix} → [bold {color}]{content}[/bold {color}]")

    def __format_date(self, datetime):
        return f"{datetime:%A, %d %B (%Y)}"


class StdoutReporter(ContextReporter):
    def report(self, breakdowns):
        printer = self.console
        printer.print("\nBuilds processed with success!")
        printer.print(
            "[bold green]NOTE[/bold green] : build times in [bold cyan] minutes [/bold cyan] "
        )

        for breakdown in breakdowns:
            self.report_breakdown(breakdown)

    def report_breakdown(self, breakdown):
        printer = self.console
        printer.print(f"\n[bold green]{breakdown.name}[/bold green]")

        table = Table(show_header=True, header_style="bold magenta")
        table.pad_edge = False
        table.add_column("Name")
        table.add_column("Builds", justify="right")
        table.add_column("Queued time", justify="right")
        table.add_column("Building time", justify="right")
        table.add_column("Total time", justify="right")
        table.add_column("Credits Estimation", justify="right")

        sorted_by_total = sorted(
            breakdown.details.items(), key=lambda kv: kv[1].count, reverse=True
        )

        for entry, value in sorted_by_total:
            table.add_row(
                entry.id,
                f"{value.count}",
                f"{value.queued}",
                f"{value.building}",
                f"{value.total}",
                f"{value.credits}",
            )

        printer.print(table)


class JsonReporter(ContextReporter):
    def report(self, breakdowns):
        data = [self.__process(item) for item in breakdowns]
        filename = "bitrise-metrics.json"
        path = f"{os.getcwd()}/{filename}"

        with open(filename, "w") as writer:
            json.dump(data, writer, indent=4)
            self.console.print(f"\nWrote results at [bold green]{path}[/bold green]")

    def __process(self, breakdowns):
        flattened = {"description": breakdowns.name}

        for criteria, numbers in breakdowns.details.items():
            for key, value in list(asdict(numbers).items()):
                flattened[key] = value

        return flattened
