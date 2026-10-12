"""Command line: python -m payments_tools.cli data/payments.csv --account 4201"""
import argparse
import sys
from typing import Optional

from .stats import summarize_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="payments_tools", description="Summarize a payments CSV.")
    parser.add_argument("path", help="CSV file with payments")
    parser.add_argument("--account", type=int, default=None, help="only this account_id")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Entry point. Takes argv as a parameter (None = sys.argv[1:]) so tests can call it directly."""
    args = build_parser().parse_args(argv)
    try:
        summary = summarize_file(args.path, args.account)
    except FileNotFoundError:
        print(f"error: no such file: {args.path}", file=sys.stderr)
        return 1
    for key in ("payments", "success", "failed", "pending"):
        print(f"{key}: {summary[key]}")
    print(f"success total: {summary['success_total']:.2f}")
    return 0


# Runs only when executed (python -m payments_tools.cli ...), never on import.
if __name__ == "__main__":
    sys.exit(main())
