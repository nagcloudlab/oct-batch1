"""Lab 11 · Testing with pytest: reference tests for fee_calculator.py.

Run them directly:  pytest labs/lab11_pytest/solution.py -v
"""
import pytest

import fee_calculator
from fee_calculator import calculate_fee, load_payments, total_fees

HEADER = "payment_id,account_id,merchant_id,created_at,amount,status,channel\n"


# ---------------------------------------------------------------- Task 1: a fixture
@pytest.fixture
def sample_payments() -> list[dict]:
    """Fresh test data for every test that asks for it (by naming it as a parameter)."""
    return [
        {"payment_id": "1", "amount": 1000.0, "channel": "card", "status": "success"},   # 18.00
        {"payment_id": "2", "amount": 2000.0, "channel": "qr", "status": "success"},     # 10.00
        {"payment_id": "3", "amount": 500.0, "channel": "app", "status": "success"},     #  0.00
        {"payment_id": "4", "amount": 9000.0, "channel": "card", "status": "failed"},    # not charged
        {"payment_id": "5", "amount": 9000.0, "channel": "qr", "status": "pending"},     # not charged
    ]


def test_total_fees_charges_only_successful_payments(sample_payments):
    assert total_fees(sample_payments) == 28.0


def test_total_fees_of_nothing_is_zero():
    assert total_fees([]) == 0


# ---------------------------------------------------------------- Task 2: parametrize
@pytest.mark.parametrize("amount, channel, expected", [
    (1000, "app", 0.0),
    (1000, "request", 0.0),
    (1000, "qr", 5.0),
    (1000, "card", 18.0),
    (50, "card", 2.0),           # card minimum fee
    (100_000, "card", 250.0),    # cap
    (100_000, "qr", 250.0),      # cap applies to every channel
])
def test_calculate_fee(amount, channel, expected):
    assert calculate_fee(amount, channel) == expected


# ---------------------------------------------------------------- Task 3: pytest.raises
@pytest.mark.parametrize("amount", [0, -10.5])
def test_rejects_non_positive_amounts(amount):
    with pytest.raises(ValueError, match="positive"):
        calculate_fee(amount, "app")


def test_rejects_unknown_channel():
    with pytest.raises(ValueError, match="unknown channel"):
        calculate_fee(100, "cash")


# ---------------------------------------------------------------- Task 4: tmp_path
def test_load_payments_reads_a_csv(tmp_path):
    csv_file = tmp_path / "payments.csv"
    csv_file.write_text(HEADER
                        + "14,4201,,2026-01-04 09:23:00,614.69,success,app\n"
                        + "15,4201,9,2026-01-05 10:00:00,1000.00,success,card\n")
    rows = load_payments(csv_file)
    assert len(rows) == 2
    assert rows[0]["amount"] == 614.69 and isinstance(rows[0]["amount"], float)
    assert total_fees(rows) == 18.0


# ---------------------------------------------------------------- Stretch: monkeypatch
def test_cap_is_read_at_call_time(monkeypatch):
    monkeypatch.setattr(fee_calculator, "FEE_CAP", 100.0)   # undone automatically after the test
    assert calculate_fee(100_000, "card") == 100.0
