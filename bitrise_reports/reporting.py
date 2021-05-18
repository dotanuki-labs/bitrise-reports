# reporting.py

from rich.console import Console
from rich.table import Table
from openpyxl import Workbook

import json
import os


class MetricsReporter:
    def __init__(
        self,
        criteria,
        detailed_builds,
        detailed_timing,
        emulate_velocity,
        report_style,
        console=Console(),
    ):
        self.contextual_delegate = ContextReporter(
            criteria, detailed_builds, detailed_timing, emulate_velocity, console
        )
        self.delegates = {
            "stdout": StdoutReporter(
                criteria, detailed_builds, detailed_timing, emulate_velocity, console
            ),
            "json": JsonReporter(
                criteria, detailed_builds, detailed_timing, emulate_velocity, console
            ),
            "excel": ExcelReporter(
                criteria, detailed_builds, detailed_timing, emulate_velocity, console
            ),
        }
        self.output_delegate = self.__find_delegate(report_style)

    def started(self, app):
        self.contextual_delegate.started(app)

    def feedback(self, project):
        self.contextual_delegate.feedback(project)

    def report(self, breakdowns):
        self.output_delegate.report(breakdowns)

    def __find_delegate(self, strategy):
        return self.delegates[strategy]


class ContextReporter:
    def __init__(self, criteria, detailed_builds, detailed_timing, emulate_velocity, console):
        self.criteria = criteria
        self.detailed_builds = detailed_builds
        self.detailed_timing = detailed_timing
        self.emulate_velocity = emulate_velocity
        self.console = console

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
        printer.print("")
        printer.print("Builds processed with success!")
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

        if self.detailed_builds:
            table.add_column("Successes", justify="right")
            table.add_column("Failures", justify="right")
            table.add_column("Abortions", justify="right")

        table.add_column("Total time", justify="right")

        if self.detailed_timing:
            table.add_column("Queued time", justify="right")
            table.add_column("Building time", justify="right")

        if self.emulate_velocity:
            table.add_column("Credits Estimation", justify="right")

        sorted_by_total = sorted(
            breakdown.details.items(), key=lambda kv: kv[1].count, reverse=True
        )

        for entry, value in sorted_by_total:
            rows = [entry.id, f"[bold cyan]{value.count}[/bold cyan]"]

            if self.detailed_builds:
                rows.append(f"{value.successes}")
                rows.append(f"{value.failures}")
                rows.append(f"{value.abortions}")

            rows.append(f"[bold cyan]{value.total}[/bold cyan]")
            if self.detailed_timing:
                rows.append(f"{value.queued}")
                rows.append(f"{value.building}")

            if self.emulate_velocity:
                rows.append(f"{value.credits}")

            table.add_row(*rows)

        printer.print(table)


class JsonReporter(ContextReporter):
    def __init__(
        self,
        criteria,
        detailed_builds,
        detailed_timing,
        emulate_velocity,
        console,
        filename="bitrise-metrics.json",
        folder=os.getcwd(),
    ):
        super(JsonReporter, self).__init__(
            criteria, detailed_builds, detailed_timing, emulate_velocity, console
        )
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
            entry = {"name": analysed.id, "count": value.count}

            if self.detailed_builds:
                entry["successes"] = value.successes
                entry["failures"] = value.failures
                entry["abortions"] = value.abortions

            entry["total"] = value.total
            if self.detailed_timing:
                entry["queued"] = value.queued
                entry["building"] = value.building

            if self.emulate_velocity:
                entry["credits"] = value.total.credits

            flattened["details"].append(entry)

        return flattened


class ExcelReporter(ContextReporter):
    def __init__(
        self,
        criteria,
        detailed_builds,
        detailed_timing,
        emulate_velocity,
        console,
        filename="bitrise-metrics.xlsx",
        path=f"{os.getcwd()}/bitrise-metrics.xlsx",
        workbook=Workbook(),
    ):
        super(ExcelReporter, self).__init__(
            criteria, detailed_builds, detailed_timing, emulate_velocity, console
        )
        self.filename = filename
        self.path = path
        self.workbook = workbook
        self.sheet = workbook.active
        self.actual_column_index = 65 # ASCII for "A"

    def report(self, breakdowns):

        self.sheet.column_dimensions["A"].width = 25

        for column in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
            self.sheet.column_dimensions[column].auto_size = True
            self.sheet.column_dimensions[column].bestFit = True

        line = 1

        for breakdown in breakdowns:
            self.reset_column_index()
            self.update(line, breakdown.name)
            line = line + 1

            sorted_by_total = sorted(
                breakdown.details.items(), key=lambda kv: kv[1].count, reverse=True
            )

            self.update_and_move_column(line, "Name")

            self.update_and_move_column(line, "Total Builds")
            if self.detailed_builds:
                self.update_and_move_column(line, "Build successes")
                self.update_and_move_column(line, "Build failures")
                self.update_and_move_column(line, "Build abortions")

            self.update_and_move_column(line, "Total time")
            if self.detailed_timing:
                self.update_and_move_column(line, "Queued time")
                self.update_and_move_column(line, "Building time")

            if self.emulate_velocity:
                self.update_and_move_column(line, "Credits estimation")

            
            for entry, value in sorted_by_total:
                line = line + 1

                self.reset_column_index()
                self.update_and_move_column(line, entry.id)
                self.update_and_move_column(line, value.count)

                if self.detailed_builds:
                    self.update_and_move_column(line, value.successes)
                    self.update_and_move_column(line, value.failures)
                    self.update_and_move_column(line, value.abortions)

                self.update_and_move_column(line, value.total)
                if self.detailed_timing:
                    self.update_and_move_column(line, value.queued)
                    self.update_and_move_column(line, value.building)

                if self.emulate_velocity:
                    self.update_and_move_column(line, value.credits)

            line = line + 2

        self.workbook.save(filename=self.filename)
        self.console.print(f"\nWrote results at [bold green]{self.path}[/bold green]")

    def update(self, line, value):
        self.sheet[f"{chr(self.actual_column_index)}{line}"] = value

    def update_and_move_column(self, line, value):
        self.sheet[f"{chr(self.actual_column_index)}{line}"] = value
        self.actual_column_index = self.actual_column_index + 1

    def reset_column_index(self):
        self.actual_column_index = 65