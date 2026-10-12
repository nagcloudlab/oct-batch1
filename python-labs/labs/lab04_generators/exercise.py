"""Lab 04 · Iterators & generators: complete each part marked TODO."""
import csv  # noqa: F401  (you will need these)
import itertools  # noqa: F401
from typing import Iterable, Iterator


def read_rows(path) -> Iterator[dict]:
    """Task 1: generator. Open the CSV and yield one dict per row.

    Convert payment_id and account_id to int and amount to float.
    """
    raise NotImplementedError("TODO: task 1")


def with_status(rows: Iterable[dict], status: str) -> Iterator[dict]:
    """Task 2: generator. Yield only the rows whose status matches."""
    raise NotImplementedError("TODO: task 2")


def amounts(rows: Iterable[dict]) -> Iterator[float]:
    """Task 3: return a generator EXPRESSION of the rows' amounts."""
    raise NotImplementedError("TODO: task 3")


def first_n(iterable: Iterable, n: int) -> list:
    """Task 4: return the first n items as a list, consuming no more than n."""
    raise NotImplementedError("TODO: task 4")


class Batches:
    """Task 5: iterator handing out lists of up to `size` items.

    list(Batches(range(5), 2)) == [[0, 1], [2, 3], [4]]
    """

    def __init__(self, iterable: Iterable, size: int):
        raise NotImplementedError("TODO: task 5 (store an iterator over iterable, and size)")

    def __iter__(self):
        raise NotImplementedError("TODO: task 5")

    def __next__(self) -> list:
        raise NotImplementedError("TODO: task 5")


def daily_totals(rows: Iterable[dict]) -> Iterator[tuple[str, float]]:
    """Task 6: generator. Yield (date, total rounded to 2 dp) per day using itertools.groupby."""
    raise NotImplementedError("TODO: task 6")


def read_many(*paths) -> Iterator[dict]:
    """Task 7: one stream of rows from several CSV files, in order (itertools.chain)."""
    raise NotImplementedError("TODO: task 7")


def success_total(path, channel: str) -> float:
    """Task 8: total of successful payments on `channel`, rounded to 2 dp, via your generators."""
    raise NotImplementedError("TODO: task 8")
