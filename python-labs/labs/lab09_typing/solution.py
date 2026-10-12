"""Lab 09 · Type hints: worked solution.

Check it with a type checker too:  pip install mypy  &&  mypy labs/lab09_typing/solution.py
"""
import csv
from typing import Iterable, Optional, Protocol, TypedDict, Union


# ---------------------------------------------------------------- Task 1: TypedDict
class PaymentRow(TypedDict):
    """The shape of one parsed CSV row: a dict whose keys and value types are known."""
    payment_id: int
    account_id: int
    merchant_id: Optional[int]      # None for person-to-person payments
    created_at: str
    amount: float
    status: str
    channel: str


# ---------------------------------------------------------------- Task 2: annotate given code
def to_amount(value: Union[str, int, float]) -> float:
    """Accept '250.50', 250 or 250.5 and return a float rounded to 2 decimals."""
    return round(float(value), 2)


def total_by_channel(rows: Iterable[PaymentRow]) -> dict[str, float]:
    """Sum of successful amounts per channel."""
    totals: dict[str, float] = {}
    for r in rows:
        if r["status"] == "success":
            totals[r["channel"]] = totals.get(r["channel"], 0.0) + r["amount"]
    return {ch: round(total, 2) for ch, total in totals.items()}


# ---------------------------------------------------------------- Task 3-4: Optional
def parse_row(raw: dict[str, str]) -> PaymentRow:
    """Convert one csv.DictReader row (all strings) into a PaymentRow."""
    return PaymentRow(
        payment_id=int(raw["payment_id"]),
        account_id=int(raw["account_id"]),
        merchant_id=int(raw["merchant_id"]) if raw["merchant_id"] else None,
        created_at=raw["created_at"],
        amount=to_amount(raw["amount"]),
        status=raw["status"],
        channel=raw["channel"],
    )


def find_payment(rows: Iterable[PaymentRow], payment_id: int) -> Optional[PaymentRow]:
    """The row with this payment_id, or None. Optional[...] warns callers to handle None."""
    for r in rows:
        if r["payment_id"] == payment_id:
            return r
    return None


# ---------------------------------------------------------------- Task 5: Protocol
class Notifier(Protocol):
    """Anything with a matching send() method is a Notifier: no inheritance needed."""

    def send(self, account_id: int, message: str) -> bool:
        ...


def notify_failures(rows: Iterable[PaymentRow], notifier: Notifier) -> int:
    """Send one message per failed payment; return how many sends succeeded."""
    sent = 0
    for r in rows:
        if r["status"] == "failed":
            if notifier.send(r["account_id"], f"payment {r['payment_id']} failed"):
                sent += 1
    return sent


# ---------------------------------------------------------------- given helper
def load_rows(path: str) -> list[PaymentRow]:
    with open(path, newline="") as f:
        return [parse_row(raw) for raw in csv.DictReader(f)]
