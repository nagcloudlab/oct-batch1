# Python labs: intermediate to production-ready

Hands-on labs for the Python day. Every lab works on the same small dataset of digital payments
(`data/payments.csv`, 1,000 rows) and checks your work with automated tests.

## Setup (once)

```bash
cd python-labs
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Python 3.9 or newer.

## How every lab works

Each lab folder has:

| File | What it is |
|---|---|
| `README.md` | the goal and the numbered tasks, with hints |
| `exercise.py` | **your file**: complete the functions and classes marked `TODO` |
| `test_labNN.py` | automated checks; don't edit |
| `solution.py` | a worked solution; try first, peek later |

Run the checks against your code:

```bash
pytest labs/lab02_comprehensions -q
```

Red tests show what is still missing. When everything is green, the lab is done.
Compare with the worked solution:

```bash
pytest labs/lab02_comprehensions -q --solution
```

## The labs

| Lab | Topic |
|---|---|
| lab02_comprehensions | list, dict and set comprehensions |
| lab03_collections | choosing list / set / dict; Counter, defaultdict, namedtuple, deque |
| lab04_generators | iterators, generators and lazy pipelines over a file |
| lab05_decorators | functools.wraps, decorators with arguments, caching, retry |
| lab06_context_managers | contextlib, cleanup on errors, a timer, a rollback |
| lab07_oop | properties, dunder methods, dataclasses, composition |
| lab08_exceptions | custom exception hierarchy, raise … from, EAFP |
| lab09_typing | type hints on a small module |
| lab10_logging | module loggers, levels, handlers, logging exceptions |
| lab11_pytest | write your own tests: fixtures, parametrize, raises |
| lab12_packaging | a small package, `__name__ == "__main__"`, imports |

The data: `payment_id, account_id, merchant_id, created_at, amount, status, channel`
(`merchant_id` is empty for payments to people; channels are app, qr, card, request;
statuses are success, failed, pending). Account 4201 belongs to Asha and has 31 payments.
