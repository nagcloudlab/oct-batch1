"""Lab 07 · OOP for production: complete each TODO."""

import csv
import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

VALID_STATUSES = ("success", "failed", "pending")


# ---------------------------------------------------------------- Task 1-3: a value object
class Payment:
    """Tasks 1-3: turn this into a dataclass.

    Task 1: @dataclass(frozen=True, order=True) with fields
            payment_id: int, account_id: int, amount: float,
            status: str = "pending", channel: str = "app", created_at: str = "".
    Task 2: __post_init__ raises ValueError if amount <= 0 or status not in VALID_STATUSES.
    Task 3: ordering = by (created_at, payment_id). Add a FIRST field
            sort_index: tuple = field(init=False, repr=False) and set it in __post_init__
            with object.__setattr__(self, "sort_index", (...)).
            Also add a @classmethod from_row(cls, row) that builds a Payment from a csv.DictReader row.
    """

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("TODO: tasks 1-3 (delete this __init__ once Payment is a dataclass)")


def load_payments(path, account_id: int) -> list[Payment]:
    """Task 4: return the account's payments from the CSV as Payment objects, oldest first.

    Use Payment.from_row and sorted() (which relies on the ordering from task 3).
    """
    raise NotImplementedError("TODO: task 4")


# ---------------------------------------------------------------- Task 5-7: an entity with rules
class Account:
    """A bank account whose balance can never be negative.

    Given: the class attribute bank_code and __init__.
    Task 5: a `balance` property; the setter raises TypeError for non-numbers (bool counts as
            a non-number) and ValueError for negatives, and stores a float in self._balance.
    Task 6: deposit(amount) / withdraw(amount): ValueError if amount <= 0; update balance
            (withdraw relies on the setter to block an overdraft); append +amount / -amount to history.
    Task 7: __repr__ -> "Account(4201, 'Asha', balance=500.00)"; __eq__ and __hash__ by account_id;
            __lt__ by balance, plus @functools.total_ordering on the class for <=, >, >=.
    """

    bank_code = "DEMO0001"         # class attribute: shared by every Account

    def __init__(self, account_id: int, owner: str, balance: float = 0.0) -> None:
        self.account_id = account_id
        self.owner = owner
        self.balance = balance     # once task 5 is done, this goes through the setter
        self.history: list[float] = []   # instance attribute: each account gets its own list

    def deposit(self, amount: float) -> None:
        raise NotImplementedError("TODO: task 6")

    def withdraw(self, amount: float) -> None:
        raise NotImplementedError("TODO: task 6")


# ---------------------------------------------------------------- Task 8-9: abc + composition
class Channel:
    """Task 8: make Channel an abstract base class (inherit from ABC) with an
    @abstractmethod fee(self, amount) -> float, so Channel() itself cannot be created."""

    name = "base"

    def fee(self, amount: float) -> float:
        raise NotImplementedError("TODO: task 8")


class AppChannel(Channel):
    """Task 8: fee is always 0.0."""
    name = "app"


class CardChannel(Channel):
    """Task 8: fee is 1.8% of the amount, rounded to 2 decimals."""
    name = "card"


class Checkout:
    """Task 9 (composition): a Checkout HAS a Channel.

    __init__(channel) stores it; total(amount) returns amount + channel fee, rounded to 2 decimals.
    """

    def __init__(self, channel: Channel) -> None:
        raise NotImplementedError("TODO: task 9")

    def total(self, amount: float) -> float:
        raise NotImplementedError("TODO: task 9")
