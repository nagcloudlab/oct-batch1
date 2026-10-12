# Lab 07 · OOP for production

**Goal:** model payments and accounts the way production code does: an immutable, validated, sortable
`Payment` dataclass; an `Account` whose balance rules are enforced by a property; and a small abstract base class
used through composition.
**Time:** ~35–40 minutes

## Tasks (all in `exercise.py`)

1. **`Payment` as a dataclass**: `@dataclass(frozen=True, order=True)` with fields `payment_id`, `account_id`, `amount`,
   `status="pending"`, `channel="app"`, `created_at=""`.
   *Hint:* delete the placeholder `__init__`; the decorator writes `__init__`, `__repr__` and `__eq__` for you.
2. **Validation**: `__post_init__` raises `ValueError` when `amount <= 0` or `status` is not in `VALID_STATUSES`.
   *Hint:* `__post_init__` runs right after the generated `__init__`.
3. **Ordering + alternative constructor**: payments sort by `(created_at, payment_id)`. Add a first field
   `sort_index: tuple = field(init=False, repr=False)` and set it in `__post_init__`. Add `@classmethod from_row(cls, row)`.
   *Hint:* the class is frozen, so use `object.__setattr__(self, "sort_index", ...)`. CSV values are strings: convert them.
4. **`load_payments(path, account_id)`**: the account's payments as `Payment` objects, oldest first. Asha's account 4201 has 31.
   *Hint:* `sorted(...)` just works once task 3 is done.
5. **`Account.balance` property**: the setter raises `TypeError` for non-numbers (including `bool`) and `ValueError` for negatives.
   *Hint:* store the value in `self._balance`; `__init__` already assigns `self.balance`, so it is validated too.
6. **`deposit` / `withdraw`**: reject amounts `<= 0`, update the balance, append `+amount` / `-amount` to `history`.
   *Hint:* `withdraw` needs no overdraft check of its own: `self.balance -= amount` goes through the setter.
7. **Dunder methods**: `__repr__` (`Account(4201, 'Asha', balance=500.00)`), `__eq__` + `__hash__` by `account_id`,
   `__lt__` by balance, and `@functools.total_ordering` on the class.
   *Hint:* return `NotImplemented` when the other object is not an `Account`.
8. **`Channel` abstract base class**: inherit from `ABC`, mark `fee` with `@abstractmethod`; `AppChannel` charges 0, `CardChannel` 1.8%.
   *Hint:* `Channel()` should now raise `TypeError`.
9. **`Checkout` (composition)**: holds a `Channel`; `total(amount)` adds the channel's fee.
   *Hint:* a checkout *has* a channel, it *is not* one: no inheritance needed.

*Note:* inside a class body, refer to the class itself in annotations as a string, e.g. `-> "Payment"`.

*Think:* why is `bank_code` a class attribute but `history` an instance attribute? What would go wrong with `history = []` at class level?

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab07_oop -q              # tests your exercise.py
pytest labs/lab07_oop -q --solution   # tests the worked solution
```
