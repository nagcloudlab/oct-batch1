"""Tests for Lab 05 · Decorators in depth."""
import csv

import pytest


def test_timed_records_and_returns(mod):
    @mod.timed
    def settle(amount):
        """Settle one payment."""
        return amount * 2

    assert settle(21) == 42
    assert settle.__name__ == "settle"          # needs functools.wraps
    assert settle.__doc__ == "Settle one payment."
    name, seconds = mod.TIMINGS[-1]
    assert name == "settle" and seconds >= 0


def test_count_calls(mod):
    @mod.count_calls
    def ping():
        return "pong"

    assert ping.calls == 0
    for _ in range(3):
        assert ping() == "pong"
    assert ping.calls == 3
    assert ping.__name__ == "ping"


def test_retry_succeeds_after_failures(mod):
    attempts = []

    @mod.retry(times=3, exceptions=(ConnectionError,))
    def fetch_status(ref):
        attempts.append(ref)
        if len(attempts) < 3:
            raise ConnectionError("bank switch timeout")
        return "success"

    assert fetch_status("REF123") == "success"
    assert attempts == ["REF123"] * 3
    assert fetch_status.__name__ == "fetch_status"


def test_retry_gives_up_and_reraises(mod):
    attempts = []

    @mod.retry(times=2, exceptions=(ConnectionError,))
    def always_down():
        attempts.append(1)
        raise ConnectionError("still down")

    with pytest.raises(ConnectionError, match="still down"):
        always_down()
    assert len(attempts) == 2


def test_retry_does_not_retry_other_errors(mod):
    attempts = []

    @mod.retry(times=5, exceptions=(ConnectionError,))
    def bad_input():
        attempts.append(1)
        raise ValueError("amount must be positive")

    with pytest.raises(ValueError):
        bad_input()
    assert len(attempts) == 1


def test_require_role(mod):
    calls = []

    @mod.require_role("ops")
    def reverse_payment(user, payment_id):
        calls.append(payment_id)
        return f"{user['name']} reversed {payment_id}"

    ravi = {"name": "Ravi", "roles": {"ops", "customer"}}
    asha = {"name": "Asha", "roles": {"customer"}}
    assert reverse_payment(ravi, 17) == "Ravi reversed 17"
    with pytest.raises(PermissionError):
        reverse_payment(asha, 18)
    assert calls == [17]                        # the protected body never ran for Asha
    assert reverse_payment.__name__ == "reverse_payment"


def test_fee_rate_is_cached(mod):
    assert mod.fee_rate("card") == 0.018
    assert mod.fee_rate("card") == 0.018
    assert mod.fee_rate("qr") == 0.0025
    assert mod.LOOKUPS == ["card", "qr"]        # the slow lookup ran once per channel
    info = mod.fee_rate.cache_info()
    assert (info.hits, info.misses) == (1, 2)


def test_total_fees(mod, payments_csv):
    with open(payments_csv, newline="") as f:
        expected = round(sum(round(float(r["amount"]) * mod.FEE_RATES[r["channel"]], 2)
                             for r in csv.DictReader(f) if r["status"] == "success"), 2)
    assert mod.total_fees(payments_csv) == expected
    info = mod.fee_rate.cache_info()
    assert (info.hits, info.misses) == (970, 4)
