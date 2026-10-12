"""Lab 09 · Type hints: complete each TODO.

Do NOT add `from __future__ import annotations` here: the tests read your annotations at runtime.
"""
import csv
from typing import Iterable, Optional, Protocol, TypedDict, Union


# ---------------------------------------------------------------- Task 1: TypedDict
class PaymentRow(TypedDict):
    """Task 1: declare all seven keys with their types:
    payment_id int, account_id int, merchant_id Optional[int], created_at str,
    amount float, status str, channel str."""
    payment_id: int
    # TODO: task 1, the other six keys


# ---------------------------------------------------------------- Task 2: annotate given code
def to_amount(value):
    """Task 2: add hints. Accepts a str, int or float; returns a float."""
    return round(float(value), 2)


def total_by_channel(rows):
    """Task 2: add hints. Takes any iterable of PaymentRow; returns {channel: total}."""
    totals = {}
    for r in rows:
        if r["status"] == "success":
            totals[r["channel"]] = totals.get(r["channel"], 0.0) + r["amount"]
    return {ch: round(total, 2) for ch, total in totals.items()}


# ---------------------------------------------------------------- Task 3-4: Optional
def parse_row(raw: dict[str, str]) -> PaymentRow:
    """Task 3: convert one csv.DictReader row (all strings) into a PaymentRow.

    ints for the ids, to_amount() for amount, merchant_id None when the field is empty.
    """
    raise NotImplementedError("TODO: task 3")


def find_payment(rows, payment_id):
    """Task 4: add hints (the return type is Optional[PaymentRow]) and implement:
    return the row with this payment_id, or None."""
    raise NotImplementedError("TODO: task 4")


# ---------------------------------------------------------------- Task 5: Protocol
class Notifier:
    """Task 5: make this a typing.Protocol with one method:
        def send(self, account_id: int, message: str) -> bool: ...
    """


def notify_failures(rows, notifier):
    """Task 5: add hints (notifier: Notifier, returns int) and implement:
    for each failed payment call notifier.send(account_id, f"payment {payment_id} failed")
    and return how many sends returned True."""
    raise NotImplementedError("TODO: task 5")


# ---------------------------------------------------------------- given helper
def load_rows(path: str) -> list[PaymentRow]:
    with open(path, newline="") as f:
        return [parse_row(raw) for raw in csv.DictReader(f)]
