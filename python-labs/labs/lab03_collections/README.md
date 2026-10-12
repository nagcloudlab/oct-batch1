# Lab 03 · Collections & performance

**Goal:** pick the right container for the job: sets and dicts for fast membership, set algebra for comparisons, and the `collections` toolbox (`Counter`, `defaultdict`, `namedtuple`, `deque`) for everyday payment analytics.
**Time:** ~35 minutes

`load_rows(path)` is given in `exercise.py` (same as Lab 02): a list of dicts with `payment_id`, `account_id`, `merchant_id` (`None` for person-to-person), `created_at`, `amount`, `status`, `channel`.

## Tasks (all in `exercise.py`)

1. **`channel_counts(rows)`** — a `Counter` of payments per channel.
   *Hint:* `Counter(iterable)` counts in one pass; feed it a generator expression.
2. **`top_merchants(rows, n)`** — the `n` merchants with the most payments, as `[(merchant_id, count), ...]`, busiest first. Skip person-to-person payments (`merchant_id is None`).
   *Hint:* `Counter.most_common(n)`.
3. **`ids_by_account(rows)`** — a `defaultdict(list)` mapping `account_id` to the list of its `payment_id`s, in file order.
   *Hint:* with `defaultdict(list)` you can `append` to a key that does not exist yet.
4. **`Payment` + `to_payments(rows)`** — define `Payment` as a `namedtuple` with fields `payment_id, account_id, amount, status, channel` (in that order), then convert every row into a `Payment`.
   *Hint:* `namedtuple("Payment", [...])`; build each one with keyword arguments.
5. **`last_ids(rows, n)`** — a `deque` holding only the last `n` payment ids seen (a "recent activity" window).
   *Hint:* `deque(iterable, maxlen=n)` drops old items from the left automatically.
6. **`flagged_payments(rows, watchlist)`** — payment ids whose `account_id` is on the watchlist. The watchlist arrives as a **list**.
   *Hint:* `x in some_list` is O(n) per check; convert it to a `set` once, then each check is O(1). (The test checks that you do!)
7. **`channel_overlap(rows, a, b)`** — compare the accounts that used channel `a` with those that used channel `b`. Return `{"both": ..., "only_a": ..., "only_b": ...}`, each a set of account ids.
   *Hint:* set algebra: `&` intersection, `-` difference.
8. **`daily_totals(rows)`** — total amount per `(account_id, date)` pair, as a dict keyed by a **tuple**, rounded to 2 decimals. The date is the first 10 characters of `created_at`.
   *Hint:* tuples are hashable, so they can be dict keys; a list cannot (`TypeError: unhashable type: 'list'`). `defaultdict(float)` helps.

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab03_collections -q              # tests your exercise.py
pytest labs/lab03_collections -q --solution   # tests the worked solution
```
