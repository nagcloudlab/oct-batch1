"""Tests for Lab 02 · Comprehensions."""
import pytest


@pytest.fixture
def rows(mod, payments_csv):
    return mod.load_rows(payments_csv)


def test_amounts(mod, rows):
    result = mod.amounts(rows)
    assert isinstance(result, list)
    assert len(result) == 1000
    assert result[:2] == [9464.99, 2174.16]
    assert round(sum(result), 2) == round(sum(r["amount"] for r in rows), 2)


def test_failed_ids(mod, rows):
    result = mod.failed_ids(rows)
    assert len(result) == 18
    lookup = {r["payment_id"]: r for r in rows}
    assert all(lookup[pid]["status"] == "failed" for pid in result)
    assert result == sorted(result)  # file order is kept


def test_channels(mod, rows):
    result = mod.channels(rows)
    assert isinstance(result, set)
    assert result == {"app", "qr", "card", "request"}


def test_by_id(mod, rows):
    result = mod.by_id(rows)
    assert isinstance(result, dict)
    assert len(result) == 1000
    assert result[1]["account_id"] == 4302
    assert result[3]["merchant_id"] is None


def test_kinds(mod, rows):
    result = mod.kinds(rows)
    assert len(result) == 1000
    assert result[:3] == ["merchant", "merchant", "p2p"]
    assert result.count("p2p") == 293


def test_big_payments(mod, rows):
    result = mod.big_payments(rows, 50_000)
    expected = sum(1 for r in rows if r["amount"] >= 50_000)
    assert len(result) == expected > 0
    assert all(amount >= 50_000 for amount in result.values())
    assert mod.big_payments(rows, 10**9) == {}


def test_flatten(mod):
    assert mod.flatten([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5]
    assert mod.flatten([]) == []


def test_account_summary_for_asha(mod, rows):
    assert mod.account_summary(rows, 4201) == {"success": 29, "failed": 1, "pending": 1}
    assert mod.account_summary(rows, -1) == {}
