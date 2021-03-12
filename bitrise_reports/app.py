# app.py


from . import cli_parser

import sys


def main(argv=None):
    answer = cli_parser.parse(argv)

    if answer == "42":
        print("Answer is correct!")
    else:
        print("This is not the answer for everything in the universe")
        sys.exit(1)
