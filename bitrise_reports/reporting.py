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
            entry = {
                "name": analysed.id,
                "count": value.count
            }

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
    def report(self, breakdowns):
        excel_file = "bitrise-metrics.xlsx"
        path = f"{os.getcwd()}/{excel_file}"

        workbook = Workbook()
        sheet = workbook.active

        sheet.column_dimensions["A"].width = 25

        for column in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
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

            velocity_column = "I" if self.detailed_builds else "F"

            if self.detailed_builds:
                sheet[f"F{line}"] = "Build successes"
                sheet[f"G{line}"] = "Build failures"
                sheet[f"H{line}"] = "Build abortions"

            if self.emulate_velocity:
                sheet[f"{velocity_column}{line}"] = "Credits estimation"

            for entry, value in sorted_by_total:
                line = line + 1

                sheet[f"A{line}"] = entry.id
                sheet[f"B{line}"] = value.count
                sheet[f"C{line}"] = value.queued
                sheet[f"D{line}"] = value.building
                sheet[f"E{line}"] = value.total

                if self.detailed_builds:
                    sheet[f"F{line}"] = value.successes
                    sheet[f"G{line}"] = value.failures
                    sheet[f"H{line}"] = value.abortions

                if self.emulate_velocity:
                    sheet[f"{velocity_column}{line}"] = value.credits

            line = line + 2

        workbook.save(filename=excel_file)
        self.console.print(f"\nWrote results at [bold green]{path}[/bold green]")
