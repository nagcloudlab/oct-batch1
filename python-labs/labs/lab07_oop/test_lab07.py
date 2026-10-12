import dataclasses

import pytest


def test_payment_is_a_dataclass_with_defaults(mod):
    p = mod.Payment(1, 4201, 250.0)
    assert dataclasses.is_dataclass(p)
    assert (p.status, p.channel, p.created_at) == ("pending", "app", "")
    assert "sort_index" not in repr(p)


def test_payment_is_frozen_and_hashable(mod):
    p = mod.Payment(1, 4201, 250.0, "success")
    with pytest.raises(dataclasses.FrozenInstanceError):
        p.amount = 1.0
    assert len({p, mod.Payment(1, 4201, 250.0, "success")}) == 1


def test_payment_validation(mod):
    with pytest.raises(ValueError):
        mod.Payment(1, 4201, 0)
    with pytest.raises(ValueError):
        mod.Payment(1, 4201, 10.0, "refunded")


def test_payment_ordering_and_from_row(mod):
    row = {"payment_id": "7", "account_id": "4201", "merchant_id": "",
           "created_at": "2026-01-02 10:00:00", "amount": "99.50", "status": "success", "channel": "qr"}
    late = mod.Payment.from_row(row)
    assert late == mod.Payment(7, 4201, 99.5, "success", "qr", "2026-01-02 10:00:00")
    early = mod.Payment(9, 4201, 10.0, "success", "app", "2026-01-01 09:00:00")
    same_time = mod.Payment(3, 4201, 10.0, "success", "app", "2026-01-02 10:00:00")
    assert sorted([late, early, same_time]) == [early, same_time, late]


def test_load_payments_for_asha(mod, payments_csv):
    asha = mod.load_payments(payments_csv, 4201)
    assert len(asha) == 31
    assert asha[0].payment_id == 14 and asha[0].created_at == "2026-01-04 09:23:00"
    assert asha == sorted(asha)


def test_account_balance_property(mod):
    acct = mod.Account(4201, "Asha", 500)
    assert acct.balance == 500.0 and isinstance(acct.balance, float)
    with pytest.raises(ValueError):
        acct.balance = -1
    with pytest.raises(TypeError):
        acct.balance = "500"
    with pytest.raises(TypeError):
        acct.balance = True
    with pytest.raises(ValueError):
        mod.Account(4202, "Ravi", -10)


def test_account_deposit_withdraw_history(mod):
    asha, ravi = mod.Account(4201, "Asha", 100), mod.Account(4301, "Ravi")
    asha.deposit(50)
    asha.withdraw(30)
    assert asha.balance == 120.0 and asha.history == [50, -30]
    assert ravi.history == []                      # not shared between instances
    with pytest.raises(ValueError):
        asha.withdraw(1000)                        # overdraft blocked by the setter
    assert asha.balance == 120.0
    with pytest.raises(ValueError):
        asha.deposit(0)


def test_account_repr_eq_order(mod):
    asha = mod.Account(4201, "Asha", 500)
    assert repr(asha) == "Account(4201, 'Asha', balance=500.00)"
    assert asha == mod.Account(4201, "Asha (copy)", 1)
    assert len({asha, mod.Account(4201, "Asha", 0)}) == 1
    ravi = mod.Account(4301, "Ravi", 200)
    assert ravi < asha and asha >= ravi
    assert max([ravi, asha]) is asha
    assert mod.Account.bank_code == asha.bank_code == "DEMO0001"


def test_channel_abc_and_composition(mod):
    with pytest.raises(TypeError):
        mod.Channel()
    assert mod.AppChannel().fee(1000) == 0.0
    assert mod.CardChannel().fee(1000) == 18.0
    assert mod.Checkout(mod.CardChannel()).total(2500) == 2545.0
    assert mod.Checkout(mod.AppChannel()).total(2500) == 2500.0
