"""Lab 03 · Collections & performance: complete each part marked TODO."""
import csv
from collections import Counter, defaultdict, deque, namedtuple  # noqa: F401  (you will need these)
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
def channel_counts(rows: list[dict]) -> Counter:
    """Task 1: return a Counter of payments per channel."""
    raise NotImplementedError("TODO: task 1")


def top_merchants(rows: list[dict], n: int) -> list[tuple[int, int]]:
    """Task 2: return [(merchant_id, count), ...] for the n busiest merchants (skip merchant_id None)."""
    raise NotImplementedError("TODO: task 2")


def ids_by_account(rows: list[dict]) -> defaultdict:
    """Task 3: return a defaultdict(list) of account_id -> [payment_id, ...] in file order."""
    raise NotImplementedError("TODO: task 3")


# Task 4a: replace None with a namedtuple called "Payment"
# with fields payment_id, account_id, amount, status, channel (in that order).
Payment = None  # TODO: task 4a


def to_payments(rows: list[dict]) -> list:
    """Task 4b: convert every row dict into a Payment namedtuple."""
    raise NotImplementedError("TODO: task 4b")


def last_ids(rows: list[dict], n: int) -> deque:
    """Task 5: return a deque holding only the last n payment_ids."""
    raise NotImplementedError("TODO: task 5")


def flagged_payments(rows: list[dict], watchlist: list[int]) -> list[int]:
    """Task 6: return payment_ids whose account_id is in watchlist (a list!).

    Convert the watchlist to a set ONCE so each membership check is O(1).
    """
    raise NotImplementedError("TODO: task 6")


def channel_overlap(rows: list[dict], a: str, b: str) -> dict[str, set[int]]:
    """Task 7: return {"both": ..., "only_a": ..., "only_b": ...} as sets of account_ids."""
    raise NotImplementedError("TODO: task 7")


def daily_totals(rows: list[dict]) -> dict[tuple[int, str], float]:
    """Task 8: return {(account_id, "YYYY-MM-DD"): total_amount rounded to 2 dp}."""
    raise NotImplementedError("TODO: task 8")
