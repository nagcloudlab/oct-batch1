# Lab 10 · Logging

**Goal:** replace `print()` debugging with real logging: a module logger, the right level for each event,
lazy `%s` arguments, masked account numbers, logged tracebacks, and handlers/formatters set up in one place.
The tests use pytest's built-in `caplog` fixture to capture and inspect your log records.
**Time:** ~30 minutes

## Tasks (all in `exercise.py`)

1. **Module logger**: `logger = logging.getLogger(__name__)`.
   *Hint:* `__name__` gives a dotted name per module, so you can later turn logging up or down per module.
2. **`mask_account(account_id)`**: `4201` → `"**01"`.
   *Hint:* logs are copied to many systems and kept for a long time; full account numbers should not end up there.
3. **`process_payment(payment)`**: log `DEBUG` on entry, `WARNING` for amounts above 50,000, `ERROR` for failed,
   `INFO` for pending and settled (exact messages are in the docstring); return whether it settled.
   *Hint:* `logger.info("payment %s settled acct=%s amount=%.2f", pid, acct, amount)`: pass values as arguments, so the string is only
   built when the record is actually emitted (and log tools can group lines that share a template).
4. **`parse_amounts(texts)`**: keep the floats that parse; for a bad value call `logger.exception(...)` inside `except` and carry on.
   *Hint:* `logger.exception` logs at ERROR level *and* attaches the traceback.
5. **`configure_logging(level, logfile, name)`**: the application-side setup: level, a `StreamHandler`, an optional `FileHandler`,
   one `Formatter(LOG_FORMAT)` on each, and no duplicate handlers when called twice.
   *Hint:* `logging.basicConfig(...)` does the same for the root logger in one line, and is fine in a small script's `main()`.
   Library modules should only create loggers, never configure them.

**Try it:** in a Python shell, `import logging; logging.basicConfig(level=logging.DEBUG)`, then call your
`process_payment(...)`, then repeat with `level=logging.WARNING` and see which lines disappear.

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab10_logging -q              # tests your exercise.py
pytest labs/lab10_logging -q --solution   # tests the worked solution
```
