# Lab 12 · Modules, packages & environments

**Goal:** turn loose functions into a small, importable, runnable package: a public API in `__init__.py`,
relative imports between modules, a command-line entry point guarded by `if __name__ == "__main__":`,
and `python -m` for both a module and the whole package.
**Time:** ~30–35 minutes

## The layout
This lab works on a **package**, so it has folders instead of `exercise.py` / `solution.py`:
```
lab12_packaging/
├── exercise/payments_tools/      <- you edit these files
│   ├── __init__.py               public API (task 1)
│   ├── loader.py                 load_payments(): given, complete
│   ├── stats.py                  summarize() (task 2)
│   ├── cli.py                    main() + __main__ guard (tasks 3-4)
│   └── __main__.py               python -m payments_tools (task 5)
├── solution/payments_tools/      the worked solution (+ solution/pyproject.toml for the stretch task)
└── test_lab12.py                 imports payments_tools from exercise/ (or solution/ with --solution)
```

## Tasks (in `exercise/payments_tools/`)

1. **`__init__.py`: the public API**: `from .loader import load_payments`, `from .stats import summarize, summarize_file`,
   `__version__ = "0.1.0"`, and `__all__` listing the three public names.
   *Hint:* users can then write `from payments_tools import summarize` without knowing which module it lives in.
2. **`stats.py`**: add the relative import `from .loader import load_payments`, then write `summarize(payments, account_id=None)`
   (counts per status + `success_total`) and `summarize_file(path, account_id=None)`.
   *Hint:* the leading dot means "from this package"; it keeps working if the package is renamed or installed.
3. **`cli.py`: `main(argv=None)`**: parse the arguments, print the summary (format in the docstring), return `0`;
   for a missing file print an error to `sys.stderr` and return `1`.
   *Hint:* taking `argv` as a parameter lets tests call `main([...])` directly; `parse_args(None)` falls back to `sys.argv[1:]`.
4. **`cli.py`: the guard**: `if __name__ == "__main__": sys.exit(main())`.
   *Hint:* on import `__name__` is `"payments_tools.cli"`; when run with `-m` it is `"__main__"`.
5. **`__main__.py`**: make `python -m payments_tools ...` work by calling `cli.main`.

Try it from the `python-labs/` folder once the tasks are done (the `PYTHONPATH` tells Python where the package lives):
```bash
PYTHONPATH=labs/lab12_packaging/exercise python -m payments_tools data/payments.csv --account 4201
PYTHONPATH=labs/lab12_packaging/exercise python -m payments_tools.cli data/payments.csv
```
Running `python labs/lab12_packaging/exercise/payments_tools/cli.py` directly fails with
*"attempted relative import with no known parent package"*: modules inside a package are run with `-m`.

**Stretch: environments and installing:**
```bash
python -m venv .venv && source .venv/bin/activate      # an isolated environment (Windows: .venv\Scripts\activate)
pip install -r requirements.txt                         # pinned dependencies for the labs
cd labs/lab12_packaging/solution && pip install -e .    # install the package from pyproject.toml in editable mode
payments-summary ../../../data/payments.csv --account 4201   # the console script declared in pyproject.toml
pip freeze                                              # what is installed, with versions
```

## Run
From the `python-labs/` folder:
```bash
pytest labs/lab12_packaging -q              # tests exercise/payments_tools
pytest labs/lab12_packaging -q --solution   # tests solution/payments_tools
```
