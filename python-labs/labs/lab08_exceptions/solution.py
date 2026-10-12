"""Lab 08 · Errors & exceptions: worked solution."""
from typing import Optional


# ---------------------------------------------------------------- Task 1-2: the hierarchy
class PaymentError(Exception):
    """Base class: callers can catch every payment problem with one except clause."""


class InvalidAmount(PaymentError):
    """The amount is not a positive number."""


class AccountNotFound(PaymentError):
    """No such account in the ledger."""


class InsufficientFunds(PaymentError):
    """The source account cannot cover the transfer. Carries the numbers, not just a message."""

    def __init__(self, account_id: int, requested: float, available: float) -> None:
        self.account_id = account_id
        self.requested = requested
        self.available = available
        super().__init__(
            f"account {account_id}: requested {requested:.2f}, available {available:.2f}"
        )


# ---------------------------------------------------------------- Task 3: raise ... from
def parse_amount(text: str) -> float:
    """Turn user input like '250.50' into a positive float, or raise InvalidAmount."""
    try:
        amount = float(text)
    except (TypeError, ValueError) as err:
        # `from err` keeps the original error as __cause__: the traceback shows both.
        raise InvalidAmount(f"not a number: {text!r}") from err
    if amount <= 0:
        raise InvalidAmount(f"amount must be positive, got {amount}")
    return amount


# ---------------------------------------------------------------- Task 4: EAFP lookups
def get_balance(ledger: dict[int, float], account_id: int) -> float:
    """EAFP: just try the lookup and translate KeyError into our own exception."""
    try:
        return ledger[account_id]
    except KeyError:
        # `from None` hides the KeyError: it is an implementation detail callers don't need.
        raise AccountNotFound(f"no account {account_id}") from None


# ---------------------------------------------------------------- Task 5: all-or-nothing transfer
def transfer(ledger: dict[int, float], src: int, dst: int, amount: float) -> None:
    """Move money between accounts. Either both balances change, or neither does."""
    if amount <= 0:
        raise InvalidAmount(f"amount must be positive, got {amount}")
    src_balance = get_balance(ledger, src)       # validate everything first ...
    dst_balance = get_balance(ledger, dst)
    if src_balance < amount:
        raise InsufficientFunds(src, amount, src_balance)
    ledger[src] = round(src_balance - amount, 2)  # ... then mutate, once nothing can fail
    ledger[dst] = round(dst_balance + amount, 2)


# ---------------------------------------------------------------- Task 6: try / except / else / finally
def safe_transfer(ledger: dict[int, float], src: int, dst: int, amount_text: str,
                  audit: list[str]) -> tuple[bool, str]:
    """Never raises for payment problems: returns (ok, message) and always writes an audit line."""
    outcome: Optional[str] = None
    try:
        amount = parse_amount(amount_text)
        transfer(ledger, src, dst, amount)
    except InsufficientFunds as err:          # most specific first
        outcome = "declined"
        return False, f"declined: {err}"
    except PaymentError as err:               # then the base class catches the rest
        outcome = "rejected"
        return False, f"rejected: {err}"
    else:                                     # runs only when the try block raised nothing
        outcome = "ok"
        return True, f"moved {amount:.2f} from {src} to {dst}"
    finally:                                  # runs on every path, even after `return`
        audit.append(f"{src}->{dst} {amount_text}: {outcome}")
