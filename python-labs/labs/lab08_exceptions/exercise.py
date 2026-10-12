"""Lab 08 · Errors & exceptions: complete each TODO."""
from typing import Optional


# ---------------------------------------------------------------- Task 1-2: the hierarchy
class PaymentError(Exception):
    """Task 1: the base class for every payment problem (given)."""


class InvalidAmount(Exception):
    """Task 1: should be a PaymentError (fix the base class)."""


class AccountNotFound(Exception):
    """Task 1: should be a PaymentError (fix the base class)."""


class InsufficientFunds(Exception):
    """Task 2: should be a PaymentError that carries the numbers.

    __init__(self, account_id, requested, available) stores all three as attributes and calls
    super().__init__ with the message "account 4201: requested 500.00, available 120.00".
    """


# ---------------------------------------------------------------- Task 3: raise ... from
def parse_amount(text: str) -> float:
    """Task 3: turn input like '250.50' into a positive float.

    - float(text) fails  -> raise InvalidAmount(...) from the original error (so __cause__ is set)
    - amount <= 0        -> raise InvalidAmount(...)
    """
    raise NotImplementedError("TODO: task 3")


# ---------------------------------------------------------------- Task 4: EAFP lookups
def get_balance(ledger: dict[int, float], account_id: int) -> float:
    """Task 4: return ledger[account_id]; if missing raise AccountNotFound ... from None.

    EAFP: use try/except KeyError, not `if account_id in ledger`.
    """
    raise NotImplementedError("TODO: task 4")


# ---------------------------------------------------------------- Task 5: all-or-nothing transfer
def transfer(ledger: dict[int, float], src: int, dst: int, amount: float) -> None:
    """Task 5: move `amount` from src to dst (round new balances to 2 decimals).

    Raise InvalidAmount (amount <= 0), AccountNotFound (via get_balance) or
    InsufficientFunds(src, amount, balance). The ledger must be untouched when anything fails.
    """
    raise NotImplementedError("TODO: task 5")


# ---------------------------------------------------------------- Task 6: try / except / else / finally
def safe_transfer(ledger: dict[int, float], src: int, dst: int, amount_text: str,
                  audit: list[str]) -> tuple[bool, str]:
    """Task 6: parse + transfer without ever raising a PaymentError.

    Returns
      (True,  "moved 250.00 from 4201 to 4301")   success          (use `else:`)
      (False, "declined: <error message>")        InsufficientFunds
      (False, "rejected: <error message>")        any other PaymentError
    In `finally:` ALWAYS append f"{src}->{dst} {amount_text}: {outcome}" to audit,
    where outcome is "ok", "declined" or "rejected".
    """
    raise NotImplementedError("TODO: task 6")
