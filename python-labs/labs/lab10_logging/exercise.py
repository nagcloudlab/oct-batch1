"""Lab 10 · Logging: complete each TODO. No print() anywhere in this file!"""
import logging
from typing import Iterable, Optional

# Task 1: replace None with a module logger named after this module (getLogger(__name__)).
logger = None

LARGE_PAYMENT = 50_000.0
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


# ---------------------------------------------------------------- Task 2: don't log what you shouldn't
def mask_account(account_id: int) -> str:
    """Task 2: return "**" + the last two digits, e.g. 4201 -> "**01"."""
    raise NotImplementedError("TODO: task 2")


# ---------------------------------------------------------------- Task 3: choose the right level
def process_payment(payment: dict) -> bool:
    """Task 3: log what happens to one payment (a dict with payment_id, account_id, amount, status).

    Always use %-style arguments (logger.info("payment %s ...", pid)), never f-strings,
    and log the account only as mask_account(account_id).
      DEBUG    "processing payment %s acct=%s"                       always
      WARNING  "large payment %s acct=%s amount=%.2f"               amount > LARGE_PAYMENT
      ERROR    "payment %s failed acct=%s"                           status failed  -> return False
      INFO     "payment %s pending acct=%s"                          status pending -> return False
      INFO     "payment %s settled acct=%s amount=%.2f"              otherwise      -> return True
    """
    raise NotImplementedError("TODO: task 3")


# ---------------------------------------------------------------- Task 4: logging exceptions
def parse_amounts(texts: Iterable[str]) -> list[float]:
    """Task 4: return float(text) for every text that parses.

    For a bad one, call logger.exception("skipping bad amount %r", text) inside the except
    block (it logs at ERROR level and attaches the traceback) and carry on.
    """
    raise NotImplementedError("TODO: task 4")


# ---------------------------------------------------------------- Task 5: handlers and formatters
def configure_logging(level: str = "INFO", logfile: Optional[str] = None,
                      name: str = "payments") -> logging.Logger:
    """Task 5: set up and return logging.getLogger(name):
    - set its level to `level`
    - remove (and close) any handlers it already has, so calling this twice doesn't duplicate lines
    - add a StreamHandler, plus a FileHandler(logfile) when logfile is given
    - give every handler logging.Formatter(LOG_FORMAT)
    """
    raise NotImplementedError("TODO: task 5")
