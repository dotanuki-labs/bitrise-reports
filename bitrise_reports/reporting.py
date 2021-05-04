# reporting.py

from rich.console import Console
from rich.table import Table
from openpyxl import Workbook

import json
import os


class MetricsReporter:
    def __init__(self, criteria, velocity, statuses, strategy, console=Console()):
        self.contextual_delegate = ContextReporter(criteria, velocity, statuses, console)
        self.delegates = {
            "stdout": StdoutReporter(criteria, velocity, statuses, console),
            "json": JsonReporter(criteria, velocity, statuses, console),
            "excel": ExcelReporter(criteria, velocity, statuses, console),
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
    def __init__(self, criteria, velocity, statuses, console):
        self.criteria = criteria
        self.console = console
        self.velocity = velocity
        self.statuses = statuses

    def started(self, app):
        self.__print("\nAnalysing", app, "cyan")

    def feedback(self, project):
        self.__print("\nFound slug", project.slug, "cyan")
        self.__print("Starting", self.__format_date(self.criteria.starting_at), "pink")
        self.__print("Ending  ", self.__format_date(self.criteria.ending_at), "pink")

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

        if self.statuses:
            table.add_column("Successes", justify="right")
            table.add_column("Failures", justify="right")

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

            if self.statuses:
                rows.append(f"{value.successes}")
                rows.append(f"{value.failures}")

            if self.velocity:
                rows.append(f"{value.credits}")

            table.add_row(*rows)

        printer.print(table)


class JsonReporter(ContextReporter):
    def __init__(
        self,
        criteria,
        velocity,
        statuses,
        console,
        filename="bitrise-metrics.json",
        folder=os.getcwd(),
    ):
        super(JsonReporter, self).__init__(criteria, velocity, statuses, console)
        self.filename = filename
        self.folder = folder

    def report(self, breakdowns):
        data = [self.__process(item) for item in breakdowns]
        path = f"{self.folder}/{self.filename}"

        with open(path, "w") as writer:
            json.dump(data, writer, indent=4)
            self.console.print(f"\nWrote results at [bold green]{path}[/bold green]")

    def __process(self, breakdown):
        flattened = {"description": breakdown.name, "details": []}

        sorted_by_total = sorted(
            breakdown.details.items(), key=lambda kv: kv[1].count, reverse=True
        )

        for analysed, value in sorted_by_total:
            entry = {
                "name": analysed.id,
                "count": value.count,
                "queued": value.queued,
                "building": value.building,
                "total": value.total,
            }

            if self.statuses:
                entry["successes"] = value.successes
                entry["failures"] = value.failures

            if self.velocity:
                entry["credits"] = value.total.credits

            flattened["details"].append(entry)

        return flattened


class ExcelReporter(ContextReporter):
    def report(self, breakdowns):
        excel_file = "bitrise-metrics.xlsx"
        path = f"{os.getcwd()}/{excel_file}"

        workbook = Workbook()
        sheet = workbook.active

        sheet.column_dimensions["A"].width = 25

        for column in ["A", "B", "C", "D", "E", "F", "G", "H"]:
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

            velocity_column = "H" if self.statuses else "F"

            if self.statuses:
                sheet[f"F{line}"] = "Build successes"
                sheet[f"G{line}"] = "Build failures"

            if self.velocity:
                sheet[f"{velocity_column}{line}"] = "Credits estimation"

            for entry, value in sorted_by_total:
                line = line + 1

                sheet[f"A{line}"] = entry.id
                sheet[f"B{line}"] = value.count
                sheet[f"C{line}"] = value.queued
                sheet[f"D{line}"] = value.building
                sheet[f"E{line}"] = value.total

                if self.statuses:
                    sheet[f"F{line}"] = value.successes
                    sheet[f"G{line}"] = value.failures

                if self.velocity:
                    sheet[f"{velocity_column}{line}"] = value.credits

            line = line + 2

        workbook.save(filename=excel_file)
        self.console.print(f"\nWrote results at [bold green]{path}[/bold green]")
