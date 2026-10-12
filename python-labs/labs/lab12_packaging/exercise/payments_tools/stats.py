"""Summaries of payment data."""
from typing import Iterable, Optional

# Task 2: import load_payments from the loader module of THIS package with a relative import.

STATUSES = ("success", "failed", "pending")


def summarize(payments: Iterable[dict], account_id: Optional[int] = None) -> dict:
    """Task 2: return
        {"payments": n, "success": n, "failed": n, "pending": n, "success_total": amount}
    over all payments, or only those of account_id when given.
    Every status key is present (0 if none); success_total is rounded to 2 decimals."""
    raise NotImplementedError("TODO: task 2")


def summarize_file(path, account_id: Optional[int] = None) -> dict:
    """Task 2: load the file with load_payments and summarize it."""
    raise NotImplementedError("TODO: task 2")
