"""Lab 02 · Comprehensions: worked solution."""
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


# ---------------------------------------------------------------- solutions
def amounts(rows: list[dict]) -> list[float]:
    """Task 1: every amount, in order."""
    return [r["amount"] for r in rows]


def failed_ids(rows: list[dict]) -> list[int]:
    """Task 2: the filter `if ...` goes at the END and drops rows."""
    return [r["payment_id"] for r in rows if r["status"] == "failed"]


def channels(rows: list[dict]) -> set[str]:
    """Task 3: braces + a single expression = set comprehension (duplicates vanish)."""
    return {r["channel"] for r in rows}


def by_id(rows: list[dict]) -> dict[int, dict]:
    """Task 4: braces + key: value = dict comprehension. A repeated key would overwrite."""
    return {r["payment_id"]: r for r in rows}


def kinds(rows: list[dict]) -> list[str]:
    """Task 5: a conditional EXPRESSION goes on the left; it transforms, it does not filter."""
    return ["p2p" if r["merchant_id"] is None else "merchant" for r in rows]


def big_payments(rows: list[dict], threshold: float) -> dict[int, float]:
    """Task 6: dict comprehension with a filter."""
    return {r["payment_id"]: r["amount"] for r in rows if r["amount"] >= threshold}


def flatten(batches: list[list[int]]) -> list[int]:
    """Task 7: read the for-clauses left to right, exactly like nested loops:

        for batch in batches:
            for pid in batch:
                out.append(pid)
    """
    return [pid for batch in batches for pid in batch]


def account_summary(rows: list[dict], account_id: int) -> dict[str, int]:
    """Task 8: filter first, then count per status.

    Note: this walks `mine` once per status (O(n * k)). Fine for three statuses,
    but collections.Counter (Lab 03) does the same job in a single pass.
    """
    mine = [r for r in rows if r["account_id"] == account_id]
    return {s: sum(1 for r in mine if r["status"] == s) for s in {r["status"] for r in mine}}
