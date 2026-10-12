"""Command line: python -m payments_tools.cli data/payments.csv --account 4201"""
import argparse
import sys
from typing import Optional

from .stats import summarize_file


def build_parser() -> argparse.ArgumentParser:
    """Given: the command-line arguments."""
    parser = argparse.ArgumentParser(prog="payments_tools", description="Summarize a payments CSV.")
    parser.add_argument("path", help="CSV file with payments")
    parser.add_argument("--account", type=int, default=None, help="only this account_id")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Task 3: parse argv with build_parser().parse_args(argv), summarize the file and print

        payments: 31
        success: 29
        failed: 1
        pending: 1
        success total: 21441.20

    then return 0. If the file does not exist, print "error: no such file: <path>"
    to sys.stderr and return 1.
    """
    raise NotImplementedError("TODO: task 3")


# Task 4: add the guard so that `python -m payments_tools.cli ...` calls main() and exits
# with its return code (sys.exit(main())), but importing this module runs nothing.
