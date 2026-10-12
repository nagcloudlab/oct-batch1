"""Tests for Lab 04 · Iterators & generators."""
import csv
import inspect
import itertools


def _expected_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _typed_rows(path):
    """Independent reader, so tasks 2 and 6 can be tested before task 1 is done."""
    rows = _expected_rows(path)
    for r in rows:
        r["amount"] = float(r["amount"])
    return rows


def test_read_rows_is_a_lazy_generator(mod, payments_csv, tmp_path):
    gen = mod.read_rows(payments_csv)
    assert inspect.isgenerator(gen)
    first = next(gen)
    assert first["payment_id"] == 1 and first["account_id"] == 4302
    assert first["amount"] == 9464.99 and first["channel"] == "app"
    assert sum(1 for _ in gen) == 999

    # Laziness: a broken LAST line must not stop us reading the first row.
    lines = payments_csv.read_text().splitlines()[:3] + ["999,not-a-number,,2026-07-01 00:00:00,1.00,success,app"]
    broken = tmp_path / "broken.csv"
    broken.write_text("\n".join(lines) + "\n")
    assert next(mod.read_rows(broken))["payment_id"] == 1


def test_with_status_filters_lazily(mod, payments_csv):
    failed = mod.with_status(iter(_typed_rows(payments_csv)), "failed")
    assert inspect.isgenerator(failed)
    assert sum(1 for _ in failed) == 18
    # Works on an endless stream: only possible if nothing is collected into a list.
    endless = itertools.cycle([{"status": "pending"}, {"status": "success"}])
    assert next(mod.with_status(endless, "success")) == {"status": "success"}


def test_amounts_is_a_generator_expression(mod):
    result = mod.amounts([{"amount": 10.0}, {"amount": 2.5}])
    assert inspect.isgenerator(result)
    assert list(result) == [10.0, 2.5]


def test_first_n_consumes_only_n(mod):
    numbers = iter(range(10))
    assert mod.first_n(numbers, 3) == [0, 1, 2]
    assert next(numbers) == 3
    assert mod.first_n(itertools.count(), 2) == [0, 1]


def test_batches_iterator_protocol(mod):
    batches = mod.Batches(range(5), 2)
    assert iter(batches) is batches
    assert next(batches) == [0, 1]
    assert list(batches) == [[2, 3], [4]]
    assert list(mod.Batches([], 3)) == []


def test_daily_totals(mod, payments_csv):
    days = list(mod.daily_totals(iter(_typed_rows(payments_csv))))
    expected = {}
    for r in _expected_rows(payments_csv):
        day = r["created_at"][:10]
        expected[day] = expected.get(day, 0.0) + float(r["amount"])
    assert [d for d, _ in days] == list(expected)
    assert days[0] == ("2026-01-01", round(expected["2026-01-01"], 2))
    assert all(total == round(expected[d], 2) for d, total in days)


def test_read_many_chains_files(mod, payments_csv):
    stream = mod.read_many(payments_csv, payments_csv)
    ids = [r["payment_id"] for r in stream]
    assert len(ids) == 2000
    assert ids[999] == 1000 and ids[1000] == 1


def test_success_total(mod, payments_csv):
    rows = _expected_rows(payments_csv)
    for channel in ("app", "card"):
        expected = round(sum(float(r["amount"]) for r in rows
                             if r["status"] == "success" and r["channel"] == channel), 2)
        assert mod.success_total(payments_csv, channel) == expected
