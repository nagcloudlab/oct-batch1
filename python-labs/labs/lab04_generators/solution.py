"""Lab 04 · Iterators & generators: worked solution."""
import csv
import itertools
from typing import Iterable, Iterator


def read_rows(path) -> Iterator[dict]:
    """Task 1: execution pauses at each `yield`; the file stays open only while we are being read."""
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            r["payment_id"] = int(r["payment_id"])
            r["account_id"] = int(r["account_id"])
            r["amount"] = float(r["amount"])
            yield r


def with_status(rows: Iterable[dict], status: str) -> Iterator[dict]:
    """Task 2: a filter stage. It pulls one row, maybe yields it, then pulls the next."""
    for r in rows:
        if r["status"] == status:
            yield r


def amounts(rows: Iterable[dict]) -> Iterator[float]:
    """Task 3: round brackets make a generator expression: nothing runs until someone iterates."""
    return (r["amount"] for r in rows)


def first_n(iterable: Iterable, n: int) -> list:
    """Task 4: islice is the lazy version of [:n]; it stops pulling after n items."""
    return list(itertools.islice(iterable, n))


class Batches:
    """Task 5: the iterator protocol by hand: __iter__ returns self, __next__ returns the next value
    or raises StopIteration when there is nothing left.

    list(Batches(range(5), 2)) == [[0, 1], [2, 3], [4]]
    """

    def __init__(self, iterable: Iterable, size: int):
        self._it = iter(iterable)  # an iterator remembers where it stopped
        self.size = size

    def __iter__(self):
        return self

    def __next__(self) -> list:
        batch = list(itertools.islice(self._it, self.size))
        if not batch:
            raise StopIteration
        return batch


def daily_totals(rows: Iterable[dict]) -> Iterator[tuple[str, float]]:
    """Task 6: groupby only groups CONSECUTIVE equal keys, so the input must be sorted by that key."""
    for day, day_rows in itertools.groupby(rows, key=lambda r: r["created_at"][:10]):
        yield day, round(sum(r["amount"] for r in day_rows), 2)


def read_many(*paths) -> Iterator[dict]:
    """Task 7: chain glues iterables end to end; each file is opened only when reached."""
    return itertools.chain.from_iterable(read_rows(p) for p in paths)


def success_total(path, channel: str) -> float:
    """Task 8: a lazy pipeline. Each row flows through every stage before the next row is read."""
    successful = with_status(read_rows(path), "success")
    on_channel = (r for r in successful if r["channel"] == channel)
    return round(sum(amounts(on_channel)), 2)
