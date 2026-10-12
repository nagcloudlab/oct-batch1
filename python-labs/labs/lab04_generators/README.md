# Lab 04 · Iterators & generators

**Goal:** process a payments file lazily, one row at a time, by chaining small generators into a pipeline, and use `itertools` instead of hand-written loops.
**Time:** ~35 minutes

Think of a generator as a tap, not a bucket: it hands out one row when asked, then pauses at `yield` until you ask again. A 10 GB file costs the same memory as a 10 KB one.

## Tasks (all in `exercise.py`)

1. **`read_rows(path)`** — a *generator function* that opens the CSV and `yield`s one dict per row, converting `payment_id`, `account_id` to `int` and `amount` to `float` (other fields stay strings).
   *Hint:* put the `yield` inside `with open(...)`, so the file stays open only while rows are being pulled.
2. **`with_status(rows, status)`** — a generator that yields only the rows with that status. It must work on *any* iterable, even an endless one.
   *Hint:* a `for` loop with `if ...: yield r`.
3. **`amounts(rows)`** — return a *generator expression* of the amounts (not a list).
   *Hint:* `( ... for r in rows)` with round brackets.
4. **`first_n(iterable, n)`** — a list of the first `n` items, without consuming more than `n`.
   *Hint:* `itertools.islice(iterable, n)`; slicing `[:n]` does not work on generators.
5. **`Batches(iterable, size)`** — a class implementing the iterator protocol that hands out lists of up to `size` items (e.g. to insert rows into a database 100 at a time).
   *Hint:* `__iter__` returns `self`; `__next__` builds the next batch with `islice` and raises `StopIteration` when it is empty.
6. **`daily_totals(rows)`** — a generator yielding `(date, total)` per day, `total` rounded to 2 decimals. The rows are already sorted by `created_at`; the date is `created_at[:10]`.
   *Hint:* `itertools.groupby(rows, key=...)` groups **consecutive** items with the same key.
7. **`read_many(*paths)`** — one stream of rows from several files, in order (e.g. monthly exports).
   *Hint:* `itertools.chain.from_iterable(read_rows(p) for p in paths)`.
8. **`success_total(path, channel)`** — the total amount of successful payments on one channel, rounded to 2 decimals, built from your generators. Nothing should ever hold the whole file in memory.
   *Hint:* `sum(amounts(... with_status(read_rows(path), "success") ...))`.

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab04_generators -q              # tests your exercise.py
pytest labs/lab04_generators -q --solution   # tests the worked solution
```
