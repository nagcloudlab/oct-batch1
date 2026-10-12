"""The code under test for Lab 11 (given, complete: do not edit it, write tests for it).

Fee rules for one payment:
- app and request payments are free
- qr payments cost 0.5% of the amount
- card payments cost 1.8% of the amount, but at least 2.00
- no fee is ever more than 250.00
- fees are rounded to 2 decimals
- the amount must be positive and the channel known, otherwise ValueError
"""
import csv
from typing import Iterable

RATES = {"app": 0.0, "request": 0.0, "qr": 0.005, "card": 0.018}
CARD_MIN_FEE = 2.00
FEE_CAP = 250.00


def calculate_fee(amount: float, channel: str) -> float:
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount}")
    if channel not in RATES:
        raise ValueError(f"unknown channel {channel!r}")
    fee = amount * RATES[channel]
    if channel == "card":
        fee = max(fee, CARD_MIN_FEE)
    return round(min(fee, FEE_CAP), 2)


def total_fees(payments: Iterable[dict]) -> float:
    """Total fee over the payments that succeeded (failed and pending ones are not charged)."""
    return round(sum(calculate_fee(p["amount"], p["channel"])
                     for p in payments if p["status"] == "success"), 2)


def load_payments(path) -> list[dict]:
    """Read a payments CSV: amount becomes a float, everything else stays a string."""
    with open(path, newline="") as f:
        return [{**row, "amount": float(row["amount"])} for row in csv.DictReader(f)]
