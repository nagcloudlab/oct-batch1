import inspect
import typing
from typing import Optional, Union

import pytest

RAW = {"payment_id": "3", "account_id": "4135", "merchant_id": "", "created_at": "2026-01-01 17:57:00",
       "amount": "359.70", "status": "success", "channel": "card"}


def test_typeddict_declares_all_keys(mod):
    assert mod.PaymentRow.__annotations__ == {
        "payment_id": int, "account_id": int, "merchant_id": Optional[int], "created_at": str,
        "amount": float, "status": str, "channel": str,
    }
    assert mod.PaymentRow.__required_keys__ == frozenset(mod.PaymentRow.__annotations__)


def test_parse_row(mod):
    row = mod.parse_row(RAW)
    assert row == {"payment_id": 3, "account_id": 4135, "merchant_id": None, "created_at": "2026-01-01 17:57:00",
                   "amount": 359.7, "status": "success", "channel": "card"}
    assert mod.parse_row({**RAW, "merchant_id": "14"})["merchant_id"] == 14


def test_find_payment_returns_row_or_none(mod, payments_csv):
    rows = mod.load_rows(payments_csv)
    assert mod.find_payment(rows, 3)["account_id"] == 4135
    assert mod.find_payment(rows, 99999) is None


def test_total_by_channel_and_to_amount(mod, payments_csv):
    totals = mod.total_by_channel(mod.load_rows(payments_csv))
    assert totals == {"app": 1566306.47, "qr": 677757.86, "card": 190855.3, "request": 207149.61}
    assert mod.to_amount("250.50") == 250.5
    assert mod.to_amount(250) == 250.0 and mod.to_amount(99.999) == 100.0


def test_notify_failures_with_any_object_that_has_send(mod, payments_csv):
    class FakeSms:                       # does NOT inherit from Notifier: structural typing
        def __init__(self):
            self.sent = []

        def send(self, account_id: int, message: str) -> bool:
            self.sent.append((account_id, message))
            return account_id != 4201    # pretend Asha's phone is unreachable

    sms = FakeSms()
    rows = mod.load_rows(payments_csv)
    ok = mod.notify_failures(rows, sms)
    assert len(sms.sent) == 18
    assert ok == 18 - sum(1 for r in rows if r["status"] == "failed" and r["account_id"] == 4201)
    assert all(msg.startswith("payment ") and msg.endswith(" failed") for _, msg in sms.sent)


@pytest.mark.parametrize("name", ["to_amount", "total_by_channel", "parse_row", "find_payment", "notify_failures"])
def test_every_function_is_fully_annotated(mod, name):
    fn = getattr(mod, name)
    hints = typing.get_type_hints(fn)
    params = list(inspect.signature(fn).parameters)
    missing = [p for p in params + ["return"] if p not in hints]
    assert not missing, f"{name} is missing hints for {missing}"


def test_specific_hints(mod):
    assert typing.get_type_hints(mod.to_amount)["value"] == Union[str, int, float]
    assert typing.get_type_hints(mod.find_payment)["return"] == Optional[mod.PaymentRow]
    ret = typing.get_type_hints(mod.total_by_channel)["return"]
    assert typing.get_origin(ret) is dict and typing.get_args(ret) == (str, float)
    hints = typing.get_type_hints(mod.notify_failures)
    assert hints["notifier"] is mod.Notifier and hints["return"] is int


def test_notifier_is_a_protocol(mod):
    assert getattr(mod.Notifier, "_is_protocol", False) is True
    hints = typing.get_type_hints(mod.Notifier.send)
    assert hints == {"account_id": int, "message": str, "return": bool}
