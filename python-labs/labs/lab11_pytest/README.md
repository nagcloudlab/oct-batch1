# Lab 11 · Testing with pytest

**Goal:** this time *you* write the tests. `fee_calculator.py` is finished code with fee rules in its docstring;
you write a test suite for it using fixtures, `parametrize`, `pytest.raises` and `tmp_path`.
**Time:** ~35–40 minutes

## How this lab is checked
Your tests go in **`exercise.py`** (it plays the role of `test_fee_calculator.py`; `solution.py` holds the reference tests).
`test_lab11.py` copies your file next to `fee_calculator.py`, saves it as `test_fee_calculator.py` and runs pytest on it:

1. against the **real** `fee_calculator.py`: all your tests must pass, and at least 8 must run (each parametrize case counts);
2. against **7 broken copies**, each with one bug planted (cap removed, card minimum removed, zero amount accepted,
   unknown channel accepted, failed payments charged, wrong qr rate, amount left as text): for every bug, at least one of your tests must fail.

This is a small version of *mutation testing*: a test suite is only as good as the bugs it catches.
Do not edit `fee_calculator.py`.

## Tasks (in `exercise.py`)

1. **A fixture**: write `@pytest.fixture def sample_payments()` returning a few payment dicts (`amount`, `channel`, `status`),
   including a failed and a pending one; use it in a test of `total_fees`.
   *Hint:* a test receives a fixture by naming it as a parameter. Work out the expected total by hand from the rules.
2. **Parametrize**: one test, `@pytest.mark.parametrize("amount, channel, expected", [...])`, covering every rule:
   each channel's rate, the card minimum fee and the 250.00 cap.
   *Hint:* pick amounts that make the arithmetic easy (1000 → card 18.00, qr 5.00); add one case per boundary.
3. **Errors**: `with pytest.raises(ValueError, match="positive"):` for a zero and a negative amount, and one for an unknown channel.
   *Hint:* `match=` is a regular expression searched in the error message.
4. **Files with `tmp_path`**: write a two-row CSV into `tmp_path` (same header as `data/payments.csv`), call `load_payments`, check the rows.
   *Hint:* `tmp_path` is a fresh `pathlib.Path` directory per test: `(tmp_path / "p.csv").write_text(...)`.
5. **Stretch: `monkeypatch`**: `monkeypatch.setattr(fee_calculator, "FEE_CAP", 100.0)` and check that the new cap applies.
   *Hint:* monkeypatch undoes the change when the test ends, so other tests are not affected.

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab11_pytest/exercise.py -v      # run just your tests, on the real code
pytest labs/lab11_pytest -q                  # the checker: your tests vs the real code and the 7 bugs
pytest labs/lab11_pytest -q --solution       # the checker on the reference tests
```
