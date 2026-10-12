"""Tests for Lab 03 · Collections & performance."""
from collections import Counter, defaultdict, deque

import pytest


@pytest.fixture
def rows(mod, payments_csv):
    return mod.load_rows(payments_csv)


def test_channel_counts(mod, rows):
    counts = mod.channel_counts(rows)
    assert isinstance(counts, Counter)
    assert counts == Counter({"app": 586, "qr": 242, "card": 107, "request": 65})
    assert counts["cash"] == 0  # a Counter returns 0 for missing keys


def test_top_merchants(mod, rows):
    top = mod.top_merchants(rows, 3)
    assert len(top) == 3
    assert all(m is not None for m, _ in top)
    counts = [c for _, c in top]
    assert counts == sorted(counts, reverse=True)
    best = max(Counter(r["merchant_id"] for r in rows if r["merchant_id"]).values())
    assert counts[0] == best


def test_ids_by_account(mod, rows):
    grouped = mod.ids_by_account(rows)
    assert isinstance(grouped, defaultdict)
    assert len(grouped[4201]) == 31  # Asha's account
    assert grouped[4201] == sorted(grouped[4201])
    assert sum(len(ids) for ids in grouped.values()) == 1000


def test_payment_namedtuple(mod, rows):
    assert mod.Payment._fields == ("payment_id", "account_id", "amount", "status", "channel")
    payments = mod.to_payments(rows)
    assert len(payments) == 1000
    first = payments[0]
    assert isinstance(first, tuple)
    assert first.payment_id == 1 and first.account_id == 4302
    assert first.amount == 9464.99 and first.channel == "app"


def test_last_ids(mod, rows):
    window = mod.last_ids(rows, 5)
    assert isinstance(window, deque)
    assert window.maxlen == 5
    assert list(window) == [r["payment_id"] for r in rows[-5:]]


class CountingList(list):
    """A list that counts how often `x in list` is used (the slow O(n) path)."""

    def __init__(self, *args):
        super().__init__(*args)
        self.in_checks = 0

    def __contains__(self, item):
        self.in_checks += 1
        return super().__contains__(item)


def test_flagged_payments_uses_a_set(mod, rows):
    watchlist = CountingList([4201, 4302, 999_999])
    flagged = mod.flagged_payments(rows, watchlist)
    expected = [r["payment_id"] for r in rows if r["account_id"] in {4201, 4302}]
    assert flagged == expected
    assert watchlist.in_checks == 0, "convert the watchlist to a set before looping"


def test_channel_overlap(mod, rows):
    result = mod.channel_overlap(rows, "app", "card")
    app = {r["account_id"] for r in rows if r["channel"] == "app"}
    card = {r["account_id"] for r in rows if r["channel"] == "card"}
    assert result == {"both": app & card, "only_a": app - card, "only_b": card - app}
    assert not (result["only_a"] & result["only_b"])


def test_daily_totals(mod, rows):
    totals = mod.daily_totals(rows)
    assert totals[(4302, "2026-01-01")] == 9464.99
    assert all(isinstance(k, tuple) and len(k) == 2 for k in totals)
    assert round(sum(totals.values()), 2) == round(sum(r["amount"] for r in rows), 2)
