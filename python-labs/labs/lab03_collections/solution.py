"""Lab 03 · Collections & performance: worked solution."""
import csv
from collections import Counter, defaultdict, deque, namedtuple
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
def channel_counts(rows: list[dict]) -> Counter:
    """Task 1: Counter counts anything hashable in a single pass."""
    return Counter(r["channel"] for r in rows)


def top_merchants(rows: list[dict], n: int) -> list[tuple[int, int]]:
    """Task 2: filter out person-to-person payments, then let most_common sort for us."""
    counts = Counter(r["merchant_id"] for r in rows if r["merchant_id"] is not None)
    return counts.most_common(n)


def ids_by_account(rows: list[dict]) -> defaultdict:
    """Task 3: no `if key not in d: d[key] = []` dance; the factory creates the list."""
    grouped: defaultdict = defaultdict(list)
    for r in rows:
        grouped[r["account_id"]].append(r["payment_id"])
    return grouped


# Task 4a: a lightweight, immutable record with named fields (still a tuple underneath).
Payment = namedtuple("Payment", ["payment_id", "account_id", "amount", "status", "channel"])


def to_payments(rows: list[dict]) -> list:
    """Task 4b: build each Payment from the matching dict keys."""
    return [
        Payment(payment_id=r["payment_id"], account_id=r["account_id"],
                amount=r["amount"], status=r["status"], channel=r["channel"])
        for r in rows
    ]


def last_ids(rows: list[dict], n: int) -> deque:
    """Task 5: a bounded deque keeps the newest n items; older ones fall off the left."""
    return deque((r["payment_id"] for r in rows), maxlen=n)


def flagged_payments(rows: list[dict], watchlist: list[int]) -> list[int]:
    """Task 6: one O(len(watchlist)) conversion, then O(1) per lookup.

    `r["account_id"] in watchlist` on the raw list would scan the list for EVERY row:
    1,000 rows x 10,000 watchlist entries = 10 million comparisons.
    """
    watched = set(watchlist)
    return [r["payment_id"] for r in rows if r["account_id"] in watched]


def channel_overlap(rows: list[dict], a: str, b: str) -> dict[str, set[int]]:
    """Task 7: build two sets, then let set algebra do the comparing."""
    used_a = {r["account_id"] for r in rows if r["channel"] == a}
    used_b = {r["account_id"] for r in rows if r["channel"] == b}
    return {"both": used_a & used_b, "only_a": used_a - used_b, "only_b": used_b - used_a}


def daily_totals(rows: list[dict]) -> dict[tuple[int, str], float]:
    """Task 8: a tuple key is hashable (immutable), so it can index a dict."""
    totals: defaultdict = defaultdict(float)
    for r in rows:
        totals[(r["account_id"], r["created_at"][:10])] += r["amount"]
    return {key: round(total, 2) for key, total in totals.items()}
