"""Summaries of payment data."""
from typing import Iterable, Optional

from .loader import load_payments   # relative import: "loader, from this same package"

STATUSES = ("success", "failed", "pending")


def summarize(payments: Iterable[dict], account_id: Optional[int] = None) -> dict:
    """Count payments per status and total the successful amounts (optionally for one account)."""
    rows = [p for p in payments if account_id is None or p["account_id"] == account_id]
    summary: dict = {"payments": len(rows)}
    for status in STATUSES:
        summary[status] = sum(1 for p in rows if p["status"] == status)
    summary["success_total"] = round(sum(p["amount"] for p in rows if p["status"] == "success"), 2)
    return summary


def summarize_file(path, account_id: Optional[int] = None) -> dict:
    return summarize(load_payments(path), account_id)
