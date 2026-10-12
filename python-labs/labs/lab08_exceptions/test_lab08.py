import pytest


@pytest.fixture
def ledger():
    return {4201: 500.0, 4301: 120.0}


def test_hierarchy(mod):
    for cls in (mod.InvalidAmount, mod.AccountNotFound, mod.InsufficientFunds):
        assert issubclass(cls, mod.PaymentError)
    assert issubclass(mod.PaymentError, Exception)
    assert not issubclass(mod.PaymentError, (ValueError, KeyError))


def test_insufficient_funds_carries_data(mod):
    err = mod.InsufficientFunds(4201, 500, 120)
    assert (err.account_id, err.requested, err.available) == (4201, 500, 120)
    assert str(err) == "account 4201: requested 500.00, available 120.00"


def test_parse_amount_ok_and_raise_from(mod):
    assert mod.parse_amount("250.50") == 250.5
    with pytest.raises(mod.InvalidAmount) as info:
        mod.parse_amount("12,50")
    assert isinstance(info.value.__cause__, ValueError)      # raise ... from err
    with pytest.raises(mod.InvalidAmount) as info:
        mod.parse_amount("-5")
    assert info.value.__cause__ is None


def test_get_balance_eafp_from_none(mod, ledger):
    assert mod.get_balance(ledger, 4201) == 500.0
    with pytest.raises(mod.AccountNotFound) as info:
        mod.get_balance(ledger, 9999)
    assert info.value.__suppress_context__ is True             # raise ... from None
    assert isinstance(info.value.__context__, KeyError)


def test_transfer_success(mod, ledger):
    mod.transfer(ledger, 4201, 4301, 250.25)
    assert ledger == {4201: 249.75, 4301: 370.25}


@pytest.mark.parametrize("src,dst,amount,exc", [
    (4301, 4201, 500.0, "InsufficientFunds"),
    (4201, 9999, 10.0, "AccountNotFound"),
    (9999, 4201, 10.0, "AccountNotFound"),
    (4201, 4301, 0, "InvalidAmount"),
])
def test_transfer_failures_leave_ledger_untouched(mod, ledger, src, dst, amount, exc):
    before = dict(ledger)
    with pytest.raises(getattr(mod, exc)):
        mod.transfer(ledger, src, dst, amount)
    assert ledger == before


def test_safe_transfer_success_and_audit(mod, ledger):
    audit = []
    assert mod.safe_transfer(ledger, 4201, 4301, "250", audit) == (True, "moved 250.00 from 4201 to 4301")
    assert audit == ["4201->4301 250: ok"]


def test_safe_transfer_failures_never_raise(mod, ledger):
    audit = []
    ok, msg = mod.safe_transfer(ledger, 4301, 4201, "1000", audit)
    assert not ok and msg == "declined: account 4301: requested 1000.00, available 120.00"
    ok, msg = mod.safe_transfer(ledger, 4201, 4301, "ten", audit)
    assert not ok and msg.startswith("rejected: ")
    ok, msg = mod.safe_transfer(ledger, 4201, 1234, "10", audit)
    assert not ok and msg.startswith("rejected: ")
    assert audit == ["4301->4201 1000: declined", "4201->4301 ten: rejected", "4201->1234 10: rejected"]
    assert ledger == {4201: 500.0, 4301: 120.0}
