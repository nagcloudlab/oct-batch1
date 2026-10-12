# Lab 09 · Type hints

**Goal:** add type hints to a small payments module (`TypedDict`, `Optional`, `Union`, `dict[str, float]`, `Protocol`)
and finish the functions they describe. The tests check both the behaviour and that the hints are really there
(`typing.get_type_hints`).
**Time:** ~30 minutes

Hints do nothing at runtime: Python does not check them. Their value comes from your editor and from a type checker such as **mypy**,
which reads them and catches mistakes (like forgetting that a function can return `None`) before the code runs.

## Tasks (all in `exercise.py`)

1. **`PaymentRow` TypedDict**: declare all seven keys: `payment_id: int`, `account_id: int`, `merchant_id: Optional[int]`,
   `created_at: str`, `amount: float`, `status: str`, `channel: str`.
   *Hint:* a `TypedDict` is still a plain `dict` at runtime; it only tells tools which keys exist and what type each value has.
2. **Annotate the given code**: `to_amount(value)` takes a `str`, `int` or `float` and returns `float`;
   `total_by_channel(rows)` takes `Iterable[PaymentRow]` and returns `dict[str, float]`.
   *Hint:* `Union[str, int, float]`. On Python 3.9, write `dict[str, float]` in annotations; the `X | Y` syntax needs 3.10.
3. **`parse_row(raw)`**: build a `PaymentRow` from one `csv.DictReader` row; `merchant_id` becomes `None` when empty.
   *Hint:* `PaymentRow(payment_id=..., ...)` or a dict literal both work.
4. **`find_payment(rows, payment_id)`**: annotate (`Optional[PaymentRow]` return) and implement: the matching row, or `None`.
   *Hint:* `Optional[X]` means `Union[X, None]`: a warning to callers to check for `None`.
5. **`Notifier` Protocol + `notify_failures(rows, notifier)`**: make `Notifier` a `typing.Protocol` with
   `send(self, account_id: int, message: str) -> bool`; `notify_failures` sends `"payment <id> failed"` for each failed payment
   and returns how many sends returned `True`.
   *Hint:* any class with a matching `send` method is accepted: the test passes in a fake that does not inherit from `Notifier`.

**Stretch:** run a type checker on your file and fix what it reports:
```bash
pip install mypy
mypy labs/lab09_typing/exercise.py
```
Then try it out: change `find_payment(rows, 3)["amount"]` somewhere and see mypy warn that the value might be `None`.

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab09_typing -q              # tests your exercise.py
pytest labs/lab09_typing -q --solution   # tests the worked solution
```
