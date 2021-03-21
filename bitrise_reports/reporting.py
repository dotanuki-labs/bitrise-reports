# reporting.py

import logging


class SimpleReporter(object):
    def report(self, breakdowns, starting, ending):
        logging.info("Finished analysis")
