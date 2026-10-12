"""Lab 02 · Comprehensions: complete each function marked TODO."""
import csv
from typing import Optional


# ---------------------------------------------------------------- given helper
def load_rows(path) -> list[dict]:
    """Read the payments CSV into a list of dicts with converted types (given)."""
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            merchant: Optional[int] = int(r["merchant_id"]) if r["merchant_id"] else None
            rows.append({
                "payment_id": int(r["payment_id"]),
                "account_id": int(r["account_id"]),
                "merchant_id": merchant,
                "created_at": r["created_at"],
                "amount": float(r["amount"]),
                "status": r["status"],
                "channel": r["channel"],
            })
    return rows


# ---------------------------------------------------------------- your tasks
def amounts(rows: list[dict]) -> list[float]:
    """Task 1: return a list of every row's amount, in order (list comprehension)."""
    raise NotImplementedError("TODO: task 1")


def failed_ids(rows: list[dict]) -> list[int]:
    """Task 2: return payment_ids of rows whose status is 'failed' (comprehension with a filter)."""
    raise NotImplementedError("TODO: task 2")


def channels(rows: list[dict]) -> set[str]:
    """Task 3: return the set of distinct channels (set comprehension)."""
    raise NotImplementedError("TODO: task 3")


def by_id(rows: list[dict]) -> dict[int, dict]:
    """Task 4: return {payment_id: row} (dict comprehension)."""
    raise NotImplementedError("TODO: task 4")


def kinds(rows: list[dict]) -> list[str]:
    """Task 5: for each row return 'p2p' if merchant_id is None else 'merchant'."""
    raise NotImplementedError("TODO: task 5")


def big_payments(rows: list[dict], threshold: float) -> dict[int, float]:
    """Task 6: return {payment_id: amount} for rows with amount >= threshold."""
    raise NotImplementedError("TODO: task 6")


def flatten(batches: list[list[int]]) -> list[int]:
    """Task 7: flatten [[1, 2], [3], []] into [1, 2, 3] (nested comprehension)."""
    raise NotImplementedError("TODO: task 7")


def account_summary(rows: list[dict], account_id: int) -> dict[str, int]:
    """Task 8: return {status: count} for the given account's payments only."""
    raise NotImplementedError("TODO: task 8")
