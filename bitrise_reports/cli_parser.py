# cli_parser.py

import argparse
import sys


def parse(args):
    parser = argparse.ArgumentParser(
        prog="<Your program name>", description="<Your program description>"
    )

    parser.add_argument(
        "-a", "--answer", action="store", required=True, help="The answer to validate"
    )

    try:
        parsed = parser.parse_args(args)
        return parsed.answer
    except:
        print("Learn more about with python-cli-tool-scaffold --help")
        sys.exit(0)
