# app.py

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
