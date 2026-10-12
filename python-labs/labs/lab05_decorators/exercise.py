"""Lab 05 · Decorators in depth: complete each part marked TODO."""
import csv  # noqa: F401  (you will need these)
import functools  # noqa: F401
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


# ---------------------------------------------------------------- your tasks
def timed(func: Callable) -> Callable:
    """Task 1: record (func.__name__, elapsed_seconds) in TIMINGS; keep the name and docstring."""
    raise NotImplementedError("TODO: task 1")


def count_calls(func: Callable) -> Callable:
    """Task 2: count calls in a `calls` attribute on the returned wrapper."""
    raise NotImplementedError("TODO: task 2")


def retry(times: int, exceptions: tuple = (Exception,), delay: float = 0.0) -> Callable:
    """Task 3: decorator factory. Retry up to `times` attempts on `exceptions`, then re-raise."""
    raise NotImplementedError("TODO: task 3")


def require_role(role: str) -> Callable:
    """Task 4: decorator factory. Raise PermissionError unless role in user["roles"] (first argument)."""
    raise NotImplementedError("TODO: task 4")


def fee_rate(channel: str) -> float:
    """Task 5: return load_fee_rate(channel), cached with functools.lru_cache(maxsize=None)."""
    raise NotImplementedError("TODO: task 5")


def total_fees(path) -> float:
    """Task 6: sum round(amount * fee_rate(channel), 2) over successful payments; round to 2 dp."""
    raise NotImplementedError("TODO: task 6")
