# reporting.py

from dataclasses import asdict
from rich.console import Console
from rich.table import Table
from openpyxl import Workbook

import json
import os


class MetricsReporter:

    def __init__(self, dates, velocity, strategy, console=Console()):
        self.contextual_delegate = ContextReporter(dates,velocity, console)
        self.delegates = {
            "stdout": StdoutReporter(dates, velocity, console),
            "json": JsonReporter(dates, velocity, console),
            "excel": ExcelReporter(dates, velocity, console),
        }
        self.output_delegate = self.__find_delegate(strategy)

    def started(self, app):
        self.contextual_delegate.started(app)

    def feedback(self, project):
        self.contextual_delegate.feedback(project)

    def report(self, breakdowns):
        self.output_delegate.report(breakdowns)

    def __find_delegate(self, strategy):
        return self.delegates[strategy]


class ContextReporter:
    def __init__(self, dates, velocity, console):
        self.dates = dates
        self.console = console
        self.velocity = velocity

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

        if self.velocity:
            table.add_column("Credits Estimation", justify="right")

        sorted_by_total = sorted(
            breakdown.details.items(), key=lambda kv: kv[1].count, reverse=True
        )

        for entry, value in sorted_by_total:
            rows = [
                entry.id,
                f"{value.count}",
                f"{value.queued}",
                f"{value.building}",
                f"{value.total}",
            ]

            if self.velocity:
                rows.append(f"{value.credits}")

            table.add_row(*rows)

        printer.print(table)


class JsonReporter(ContextReporter):
    def report(self, breakdowns):
        data = [self.__process(item) for item in breakdowns]
        filename = "bitrise-metrics.json"
        path = f"{os.getcwd()}/{filename}"

        with open(filename, "w") as writer:
            json.dump(data, writer, indent=4)
            self.console.print(f"\nWrote results at [bold green]{path}[/bold green]")

    def __process(self, breakdown):
        flattened = {"description": breakdown.name}

        for project, numbers in breakdown.details.items():
            for key, value in list(asdict(numbers).items()):
                flattened[key] = value

        return flattened


class ExcelReporter(ContextReporter):
    def report(self, breakdowns):
        excel_file = "bitrise-metrics.xlsx"
        path = f"{os.getcwd()}/{excel_file}"

        workbook = Workbook()
        sheet = workbook.active

        sheet.column_dimensions["A"].width = 25

        for column in ["A", "B", "C", "D", "E", "F"]:
            sheet.column_dimensions[column].auto_size = True
            sheet.column_dimensions[column].bestFit = True

        line = 1

        for breakdown in breakdowns:
            sheet[f"A{line}"] = breakdown.name
            line = line + 1

            sorted_by_total = sorted(
                breakdown.details.items(), key=lambda kv: kv[1].count, reverse=True
            )

            sheet[f"A{line}"] = "Name"
            sheet[f"B{line}"] = "Builds"
            sheet[f"C{line}"] = "Queued time"
            sheet[f"D{line}"] = "Building time"
            sheet[f"E{line}"] = "Total time"
            sheet[f"F{line}"] = "Credits estimation"

            for entry, value in sorted_by_total:
                line = line + 1

                sheet[f"A{line}"] = entry.id
                sheet[f"B{line}"] = value.count
                sheet[f"C{line}"] = value.queued
                sheet[f"D{line}"] = value.building
                sheet[f"E{line}"] = value.total
                sheet[f"F{line}"] = value.credits

            line = line + 2

        workbook.save(filename=excel_file)
        self.console.print(f"\nWrote results at [bold green]{path}[/bold green]")
