# Lab 05 · Decorators in depth

**Goal:** write production-style decorators (timing, call counting, retry, role checks) that keep the wrapped function's identity, and use `functools.lru_cache` to stop paying for the same slow lookup twice.
**Time:** ~35 minutes

A decorator is a function that takes a function and returns a replacement for it. `@timed` above `def settle(...)` simply means `settle = timed(settle)`.

## Tasks (all in `exercise.py`)

1. **`timed(func)`** — call `func`, measure how long it took with `time.perf_counter()`, append `(func.__name__, seconds)` to the module-level list `TIMINGS`, and return the result unchanged.
   *Hint:* decorate the inner `wrapper` with `@functools.wraps(func)`, or `settle.__name__` becomes `"wrapper"` and its docstring disappears (the test checks this).
2. **`count_calls(func)`** — a decorator that counts calls in an attribute: after three calls, `f.calls == 3`.
   *Hint:* functions are objects; set `wrapper.calls = 0` before returning `wrapper`, and increment it inside.
3. **`retry(times, exceptions=(Exception,), delay=0.0)`** — a decorator *with arguments*. Call the function up to `times` times while it raises one of `exceptions`, sleeping `delay` seconds between tries. If the last try fails, re-raise that error. Other exception types must propagate immediately, without retrying.
   *Hint:* three levels: `retry(...)` returns `decorator(func)`, which returns `wrapper(*args, **kwargs)`.
4. **`require_role(role)`** — a decorator with an argument for functions whose first argument is a `user` dict like `{"name": "Asha", "roles": {"customer"}}`. If `role` is not in `user["roles"]`, raise `PermissionError` without calling the function.
   *Hint:* this is the `with_auth` idea from class, now with a parameter.
5. **`fee_rate(channel)`** — return the fee rate for a channel by calling the given (slow) `load_fee_rate(channel)`, and cache it with `@functools.lru_cache(maxsize=None)` so each channel is looked up only once.
   *Hint:* the decorated function gains `fee_rate.cache_info()` and `fee_rate.cache_clear()`.
6. **`total_fees(path)`** — stream the CSV and add up `round(amount * fee_rate(channel), 2)` for every **successful** payment; return the total rounded to 2 decimals.
   *Hint:* 970 of the 974 rate lookups should be cache hits; check with `fee_rate.cache_info()`.

**Caution with `lru_cache`:** only cache *pure* functions whose arguments are hashable. Never cache something whose answer changes over time (a balance, "now") without a way to expire it.

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab05_decorators -q              # tests your exercise.py
pytest labs/lab05_decorators -q --solution   # tests the worked solution
```
