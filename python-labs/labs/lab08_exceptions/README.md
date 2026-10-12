# Lab 08 · Errors & exceptions

**Goal:** design a small exception hierarchy for payments, translate low-level errors with `raise … from`,
and write a transfer that is all-or-nothing plus a "never crashes" wrapper using `try / except / else / finally`.
**Time:** ~30–35 minutes

A *ledger* in this lab is a plain dict `{account_id: balance}`, e.g. `{4201: 500.0, 4301: 120.0}` (Asha and Ravi).

## Tasks (all in `exercise.py`)

1. **The hierarchy**: make `InvalidAmount`, `AccountNotFound` and `InsufficientFunds` subclasses of `PaymentError`.
   *Hint:* one `except PaymentError:` should then catch all of them.
2. **`InsufficientFunds` carries data**: `__init__(self, account_id, requested, available)` stores the three values and builds the message
   `"account 4201: requested 500.00, available 120.00"`.
   *Hint:* finish with `super().__init__(message)` so `str(err)` works.
3. **`parse_amount(text)`**: `float(text)`; on failure `raise InvalidAmount(...) from err`; reject amounts `<= 0`.
   *Hint:* `from err` sets `__cause__`, so the traceback shows *"The above exception was the direct cause of…"*.
4. **`get_balance(ledger, account_id)`**: EAFP: `try: return ledger[account_id]` / `except KeyError:` → `raise AccountNotFound(...) from None`.
   *Hint:* `from None` hides the internal `KeyError` from the traceback. Compare with LBYL (`if account_id in ledger`).
5. **`transfer(ledger, src, dst, amount)`**: validate the amount, look up both balances, check funds, *then* update both.
   *Hint:* do every check before the first write: if anything raises, the ledger must be unchanged.
6. **`safe_transfer(...)`**: returns `(ok, message)` and never raises a `PaymentError`; always appends an audit line.
   *Hint:* catch `InsufficientFunds` before `PaymentError` (order matters); put the success return in `else:` and the audit in `finally:`.

*Think:* why not catch `Exception` in `safe_transfer`? What would happen to a genuine bug such as a `NameError`?

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab08_exceptions -q              # tests your exercise.py
pytest labs/lab08_exceptions -q --solution   # tests the worked solution
```
