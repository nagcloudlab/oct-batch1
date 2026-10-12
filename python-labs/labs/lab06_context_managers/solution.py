"""Lab 06 · Context managers in depth: worked solution."""
import contextlib
import os
import time
from typing import Iterable, Iterator, Optional, TextIO


# ---------------------------------------------------------------- given helper
def transfer(balances: dict, src: int, dst: int, amount: float) -> None:
    """Move money between accounts (given). Debits FIRST, credits SECOND.

    Raises ValueError for insufficient funds (before touching anything) and
    KeyError for an unknown destination account (AFTER the debit!).
    """
    if balances[src] < amount:
        raise ValueError(f"insufficient funds in account {src}")
    balances[src] -= amount
    balances[dst] = balances[dst] + amount   # KeyError here leaves src already debited


# ---------------------------------------------------------------- solutions
class Timer:
    """Task 1: __enter__ returns self so `as t` gives us the timer object."""

    def __init__(self) -> None:
        self.elapsed: Optional[float] = None

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.elapsed = time.perf_counter() - self._start
        return False  # never swallow errors: a timer has no business hiding failures


@contextlib.contextmanager
def timer(label: str, log: list) -> Iterator[None]:
    """Task 2: code before `yield` is __enter__, code after it is __exit__.

    An exception in the with-block is re-raised AT the yield, so `finally` is what
    makes the log entry happen on failure too.
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        log.append((label, time.perf_counter() - start))


class Transaction:
    """Task 3: all-or-nothing updates to a balances dict."""

    def __init__(self, balances: dict):
        self.balances = balances

    def __enter__(self) -> dict:
        self._snapshot = dict(self.balances)  # shallow copy is enough: values are numbers
        return self.balances

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is not None:
            # Restore IN PLACE so every holder of a reference to this dict sees the rollback.
            self.balances.clear()
            self.balances.update(self._snapshot)
        return False  # rollback, then let the caller see the original error


class Collect:
    """Task 4: __exit__ decides: return True to swallow, False to propagate."""

    def __init__(self, *exc_types: type):
        self.exc_types = exc_types
        self.errors: list = []

    def __enter__(self) -> "Collect":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is not None and issubclass(exc_type, self.exc_types):
            self.errors.append(exc)
            return True
        return False


def parse_amounts(values: Iterable[str]) -> list[float]:
    """Task 5: suppress(ValueError) is a tidy `try: ... except ValueError: pass`."""
    amounts = []
    for v in values:
        with contextlib.suppress(ValueError):
            amounts.append(float(v))
    return amounts


@contextlib.contextmanager
def atomic_write(path) -> Iterator[TextIO]:
    """Task 6: readers see either the old file or the complete new one, never half of it."""
    tmp = f"{path}.tmp"
    f = open(tmp, "w", newline="")
    try:
        yield f
    except BaseException:
        f.close()
        os.remove(tmp)
        raise
    else:
        f.close()
        os.replace(tmp, path)  # atomic rename on the same filesystem
