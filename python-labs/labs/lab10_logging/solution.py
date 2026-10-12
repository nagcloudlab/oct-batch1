"""Lab 10 · Logging: worked solution."""
import logging
from typing import Iterable, Optional

# Task 1: one logger per module, named after the module. Library code never calls basicConfig:
# it only creates records; the application decides where they go (handlers) and how they look (formatters).
logger = logging.getLogger(__name__)

LARGE_PAYMENT = 50_000.0
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


# ---------------------------------------------------------------- Task 2: don't log what you shouldn't
def mask_account(account_id: int) -> str:
    """Show only the last two digits: logs end up in many places, account numbers should not."""
    return "**" + str(account_id)[-2:]


# ---------------------------------------------------------------- Task 3: choose the right level
def process_payment(payment: dict) -> bool:
    """Log what happens to one payment; return True when it settled."""
    pid, amount = payment["payment_id"], payment["amount"]
    acct = mask_account(payment["account_id"])
    # %-style args, not f-strings: the message is only built if the record is actually emitted.
    logger.debug("processing payment %s acct=%s", pid, acct)
    if amount > LARGE_PAYMENT:
        logger.warning("large payment %s acct=%s amount=%.2f", pid, acct, amount)
    if payment["status"] == "failed":
        logger.error("payment %s failed acct=%s", pid, acct)
        return False
    if payment["status"] == "pending":
        logger.info("payment %s pending acct=%s", pid, acct)
        return False
    logger.info("payment %s settled acct=%s amount=%.2f", pid, acct, amount)
    return True


# ---------------------------------------------------------------- Task 4: logging exceptions
def parse_amounts(texts: Iterable[str]) -> list[float]:
    """Parse what we can; log (with traceback) and skip what we cannot."""
    amounts = []
    for text in texts:
        try:
            amounts.append(float(text))
        except ValueError:
            # logger.exception = logger.error + the current traceback (exc_info=True)
            logger.exception("skipping bad amount %r", text)
    return amounts


# ---------------------------------------------------------------- Task 5: handlers and formatters
def configure_logging(level: str = "INFO", logfile: Optional[str] = None,
                      name: str = "payments") -> logging.Logger:
    """Application-side setup: console handler (+ optional file handler) on the `name` logger.

    Safe to call twice: existing handlers are removed first, so lines are not duplicated.
    """
    log = logging.getLogger(name)
    log.setLevel(level)
    for handler in list(log.handlers):
        log.removeHandler(handler)
        handler.close()
    formatter = logging.Formatter(LOG_FORMAT)
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if logfile:
        handlers.append(logging.FileHandler(logfile, encoding="utf-8"))
    for handler in handlers:
        handler.setFormatter(formatter)
        log.addHandler(handler)
    return log
