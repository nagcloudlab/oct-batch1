"""Lab 07 · OOP for production: worked solution."""

import csv
import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

VALID_STATUSES = ("success", "failed", "pending")


# ---------------------------------------------------------------- Task 1-3: a value object
@dataclass(frozen=True, order=True)
class Payment:
    """One payment. Frozen = immutable and hashable; order=True gives <, <=, >, >=.

    order=True compares the fields as a tuple, in declaration order, so the first
    field is a derived sort key (created_at, payment_id) that is not part of __init__.
    """
    sort_index: tuple = field(init=False, repr=False)
    payment_id: int
    account_id: int
    amount: float
    status: str = "pending"
    channel: str = "app"
    created_at: str = ""

    def __post_init__(self) -> None:
        # Validate once, at construction: an invalid Payment can never exist.
        if self.amount <= 0:
            raise ValueError(f"amount must be positive, got {self.amount}")
        if self.status not in VALID_STATUSES:
            raise ValueError(f"unknown status {self.status!r}")
        # The dataclass is frozen, so normal assignment raises; object.__setattr__ is the
        # documented escape hatch for setting derived fields inside __post_init__.
        object.__setattr__(self, "sort_index", (self.created_at, self.payment_id))

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "Payment":
        """Alternative constructor: build a Payment from one csv.DictReader row."""
        return cls(
            payment_id=int(row["payment_id"]),
            account_id=int(row["account_id"]),
            amount=float(row["amount"]),
            status=row["status"],
            channel=row["channel"],
            created_at=row["created_at"],
        )


def load_payments(path, account_id: int) -> list[Payment]:
    """Task 4: the account's payments from the CSV, oldest first (uses Payment ordering)."""
    with open(path, newline="") as f:
        payments = [Payment.from_row(r) for r in csv.DictReader(f)
                    if int(r["account_id"]) == account_id]
    return sorted(payments)


# ---------------------------------------------------------------- Task 5-7: an entity with rules
@functools.total_ordering          # define __eq__ and __lt__, get the other four for free
class Account:
    """A bank account whose balance can never be negative."""

    bank_code = "DEMO0001"         # class attribute: shared by every Account

    def __init__(self, account_id: int, owner: str, balance: float = 0.0) -> None:
        self.account_id = account_id
        self.owner = owner
        self.balance = balance     # goes through the property setter, so it is validated too
        self.history: list[float] = []   # instance attribute: each account gets its own list

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        # bool is a subclass of int, so reject it explicitly
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"balance must be a number, got {type(value).__name__}")
        if value < 0:
            raise ValueError(f"balance cannot be negative: {value}")
        self._balance = float(value)

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount
        self.history.append(amount)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        self.balance -= amount        # the setter rejects an overdraft
        self.history.append(-amount)

    def __repr__(self) -> str:
        return f"Account({self.account_id}, {self.owner!r}, balance={self.balance:.2f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Account):
            return NotImplemented
        return self.account_id == other.account_id

    def __hash__(self) -> int:     # defining __eq__ removes __hash__; restore it consistently
        return hash(self.account_id)

    def __lt__(self, other: "Account") -> bool:
        if not isinstance(other, Account):
            return NotImplemented
        return self.balance < other.balance


# ---------------------------------------------------------------- Task 8-9: abc + composition
class Channel(ABC):
    """A payment channel. Subclasses must say how much a payment costs."""

    name = "base"

    @abstractmethod
    def fee(self, amount: float) -> float:
        ...


class AppChannel(Channel):
    name = "app"

    def fee(self, amount: float) -> float:
        return 0.0


class CardChannel(Channel):
    name = "card"

    def fee(self, amount: float) -> float:
        return round(amount * 0.018, 2)


class Checkout:
    """Composition: a Checkout HAS a Channel (it does not inherit from one)."""

    def __init__(self, channel: Channel) -> None:
        self.channel = channel

    def total(self, amount: float) -> float:
        return round(amount + self.channel.fee(amount), 2)
