# Lab 06 · Context managers in depth

**Goal:** guarantee clean-up and consistency around payment operations: timing a block, rolling back a failed transfer, deciding in `__exit__` which errors to swallow, and writing a file atomically.
**Time:** ~35 minutes

Recall the order: `with cm as x:` calls `cm.__enter__()` (its return value becomes `x`), runs the block, then **always** calls `cm.__exit__(exc_type, exc, tb)`. If `__exit__` returns `True`, the exception is swallowed; anything else lets it propagate.

## Tasks (all in `exercise.py`)

1. **`Timer`** (class) — `__enter__` starts a clock and returns the timer itself; `__exit__` stores the seconds taken in `self.elapsed`. Errors inside the block must still propagate.
   *Hint:* `time.perf_counter()`; return `False` (or `None`) from `__exit__`.
2. **`timer(label, log)`** — the same idea as a *generator-based* context manager: after the block, append `(label, seconds)` to the `log` list, **even if the block raised**.
   *Hint:* `@contextlib.contextmanager`, and put `yield` inside `try: ... finally:`.
3. **`Transaction(balances)`** (class) — protects a dict of account balances. On enter, take a snapshot; if the block raises, restore the dict **in place** to the snapshot and let the error propagate; on success, keep the changes.
   *Hint:* `dict(balances)` is a snapshot copy; `balances.clear()` then `balances.update(snapshot)` restores the same object. The given `transfer()` debits first and credits second, so without your rollback a bad destination account loses money.
4. **`Collect(*exc_types)`** (class) — swallows only the listed exception types and keeps them in `self.errors` (a list); any other exception propagates.
   *Hint:* in `__exit__`, `exc_type is not None and issubclass(exc_type, self.exc_types)`; returning `True` swallows.
5. **`parse_amounts(values)`** — convert strings to floats, silently skipping any that are not numbers (e.g. `"N/A"`).
   *Hint:* `with contextlib.suppress(ValueError):` around one conversion inside the loop.
6. **`atomic_write(path)`** — a generator-based context manager that yields a file opened for writing at `path + ".tmp"`. On success, close it and move it over `path` with `os.replace`. On error, close and delete the temp file and re-raise, so the original `path` is never left half-written.
   *Hint:* `try: yield f` / `except BaseException: ...; raise` / `else: os.replace(...)`.

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab06_context_managers -q              # tests your exercise.py
pytest labs/lab06_context_managers -q --solution   # tests the worked solution
```
