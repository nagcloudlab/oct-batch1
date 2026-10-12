"""Lab 05 · Decorators in depth: worked solution."""
import csv
import functools
import time
from typing import Callable

# ---------------------------------------------------------------- given
TIMINGS: list = []          # task 1 appends (function_name, seconds) here
LOOKUPS: list = []          # load_fee_rate appends the channel every time it really runs

FEE_RATES = {"app": 0.0, "qr": 0.0025, "card": 0.018, "request": 0.001}


def load_fee_rate(channel: str) -> float:
    """Pretend to fetch a fee rate from a slow config service (given)."""
    LOOKUPS.append(channel)
    time.sleep(0.001)
    return FEE_RATES[channel]


# ---------------------------------------------------------------- solutions
def timed(func: Callable) -> Callable:
    """Task 1: functools.wraps copies __name__, __doc__, __module__ ... from func onto wrapper."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:  # record the time even if func raises
            TIMINGS.append((func.__name__, time.perf_counter() - start))
    return wrapper


def count_calls(func: Callable) -> Callable:
    """Task 2: state lives as an attribute on the wrapper function object."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


def retry(times: int, exceptions: tuple = (Exception,), delay: float = 0.0) -> Callable:
    """Task 3: a decorator WITH arguments is a function that RETURNS a decorator.

    @retry(times=3)          ->  settle = retry(times=3)(settle)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise          # out of attempts: re-raise the last error unchanged
                    time.sleep(delay)
        return wrapper
    return decorator


def require_role(role: str) -> Callable:
    """Task 4: check BEFORE calling; the protected function never runs for the wrong user."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(user: dict, *args, **kwargs):
            if role not in user.get("roles", ()):
                raise PermissionError(f"{func.__name__} needs role {role!r}")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


@functools.lru_cache(maxsize=None)
def fee_rate(channel: str) -> float:
    """Task 5: the first call per channel runs load_fee_rate; later calls come from the cache."""
    return load_fee_rate(channel)


def total_fees(path) -> float:
    """Task 6: 974 successful rows, but only 4 distinct channels -> 4 misses, 970 hits."""
    total = 0.0
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            if r["status"] == "success":
                total += round(float(r["amount"]) * fee_rate(r["channel"]), 2)
    return round(total, 2)
