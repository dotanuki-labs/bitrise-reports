# utils.py

import json
import os

FIXTURES_DIR = f"{os.getcwd()}/tests/fixtures"


def fixture(name):
    with open(f"{FIXTURES_DIR}/{name}.json") as payload:
        return json.load(payload)
