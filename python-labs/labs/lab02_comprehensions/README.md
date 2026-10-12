# Lab 02 · Comprehensions

**Goal:** turn loops over payment rows into list, set and dict comprehensions, and spot when a comprehension is the wrong tool.
**Time:** ~30 minutes

`load_rows(path)` is already written for you in `exercise.py`. It reads `data/payments.csv` and returns a list of dicts with
`payment_id`, `account_id`, `merchant_id` (`None` for person-to-person payments), `created_at`, `amount` (float), `status` and `channel`.

## Tasks (all in `exercise.py`)

1. **`amounts(rows)`** — a list of every payment amount, in file order.
   *Hint:* `[expression for item in iterable]`.
2. **`failed_ids(rows)`** — the `payment_id` of every payment whose status is `"failed"`.
   *Hint:* add a filter: `[... for r in rows if ...]`.
3. **`channels(rows)`** — the distinct channels used, as a set.
   *Hint:* a set comprehension uses `{ }` with a single expression.
4. **`by_id(rows)`** — a dict mapping `payment_id` to its row, so lookups by id are instant.
   *Hint:* dict comprehension `{key: value for ...}`.
5. **`kinds(rows)`** — for each row, `"p2p"` if `merchant_id` is `None`, otherwise `"merchant"`.
   *Hint:* the conditional expression goes on the *left*: `[a if cond else b for r in rows]`.
6. **`big_payments(rows, threshold)`** — `{payment_id: amount}` for payments with `amount >= threshold`.
   *Hint:* dict comprehension with a filter.
7. **`flatten(batches)`** — turn a list of lists of payment ids into one flat list.
   *Hint:* nested comprehension; the `for` clauses read in the same order as nested loops.
8. **`account_summary(rows, account_id)`** — `{status: count}` for one account (try Asha's account 4201).
   *Hint:* first filter the account's rows, then build a dict over the set of statuses.
   *Think:* this scans the rows once per status. When would a plain loop or `collections.Counter` (Lab 03) be better?

## When NOT to use a comprehension
- When you need side effects (printing, writing to a database): use a `for` loop.
- When it needs more than two `for`s or a complicated condition: readability wins.
- When the result is huge and you only iterate over it once: use a generator expression (Lab 04).

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab02_comprehensions -q              # tests your exercise.py
pytest labs/lab02_comprehensions -q --solution   # tests the worked solution
```
