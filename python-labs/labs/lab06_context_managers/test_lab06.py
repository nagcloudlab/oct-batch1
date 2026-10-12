"""Tests for Lab 06 · Context managers in depth."""
import csv
import time

import pytest


class CrashError(Exception):
    """A test-only error (NOT a RuntimeError, so NotImplementedError cannot pass for it)."""


def test_timer_class(mod):
    with mod.Timer() as t:
        time.sleep(0.01)
    assert isinstance(t, mod.Timer)
    assert t.elapsed >= 0.01

    t2 = mod.Timer()
    with pytest.raises(ZeroDivisionError):
        with t2:
            1 / 0
    assert t2.elapsed is not None and t2.elapsed >= 0


def test_timer_function_logs_even_on_error(mod):
    log = []
    with mod.timer("settle-batch", log):
        time.sleep(0.005)
    with pytest.raises(CrashError):
        with mod.timer("broken-batch", log):
            raise CrashError("bank switch down")
    assert [label for label, _ in log] == ["settle-batch", "broken-batch"]
    assert log[0][1] >= 0.005


def test_transaction_commits(mod):
    balances = {4201: 5000.0, 4302: 100.0}
    with mod.Transaction(balances):
        mod.transfer(balances, 4201, 4302, 1200.0)
    assert balances == {4201: 3800.0, 4302: 1300.0}


def test_transaction_rolls_back_in_place(mod):
    balances = {4201: 5000.0, 4302: 100.0}
    same_object = balances
    with pytest.raises(KeyError):
        with mod.Transaction(balances):
            mod.transfer(balances, 4201, 4302, 200.0)   # succeeds...
            mod.transfer(balances, 4201, 9999, 500.0)   # ...then fails after debiting
    assert same_object is balances
    assert balances == {4201: 5000.0, 4302: 100.0}       # both transfers undone


def test_collect_swallows_only_listed_types(mod):
    with mod.Collect(ValueError, KeyError) as c:
        raise ValueError("bad amount")
    with c:
        {}["missing"]
    assert [type(e) for e in c.errors] == [ValueError, KeyError]

    with pytest.raises(TypeError):
        with mod.Collect(ValueError):
            raise TypeError("not collected")


def test_parse_amounts(mod, payments_csv):
    assert mod.parse_amounts(["10.50", "N/A", "", "3", "1e3"]) == [10.5, 3.0, 1000.0]
    with open(payments_csv, newline="") as f:
        raw = [r["amount"] for r in csv.DictReader(f)]
    assert len(mod.parse_amounts(raw + ["oops"])) == 1000


def test_atomic_write_success(mod, tmp_path):
    target = tmp_path / "report.csv"
    target.write_text("old\n")
    with mod.atomic_write(target) as f:
        f.write("account_id,total\n4201,9100.50\n")
        assert target.read_text() == "old\n"            # not visible until the block ends
    assert target.read_text() == "account_id,total\n4201,9100.50\n"
    assert [p.name for p in tmp_path.iterdir()] == ["report.csv"]


def test_atomic_write_failure_keeps_original(mod, tmp_path):
    target = tmp_path / "report.csv"
    target.write_text("old\n")
    with pytest.raises(CrashError):
        with mod.atomic_write(target) as f:
            f.write("half a rep")
            raise CrashError("crash mid-write")
    assert target.read_text() == "old\n"
    assert [p.name for p in tmp_path.iterdir()] == ["report.csv"]   # temp file cleaned up
