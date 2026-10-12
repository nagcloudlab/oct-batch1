"""Checks YOUR tests (exercise.py, or solution.py with --solution).

Good tests pass on correct code and fail on broken code. So we run your tests:
  1. against the real fee_calculator.py   -> they must all pass
  2. against copies with one bug planted  -> each bug must make at least one test fail
"""
import ast
import pathlib
import subprocess
import sys

import pytest

HERE = pathlib.Path(__file__).parent
REAL = (HERE / "fee_calculator.py").read_text()

# (bug description, original code, broken code)
MUTANTS = [
    ("fee cap removed", "return round(min(fee, FEE_CAP), 2)", "return round(fee, 2)"),
    ("card minimum removed", "fee = max(fee, CARD_MIN_FEE)", "fee = fee"),
    ("zero amount accepted", "if amount <= 0:", "if amount < 0:"),
    ("unknown channel accepted", "if channel not in RATES:\n        raise", "if channel not in RATES:\n        return 0.0\n        raise"),
    ("failed payments charged", 'if p["status"] == "success"', 'if p["status"] != "pending"'),
    ("qr rate 10x too high", '"qr": 0.005', '"qr": 0.05'),
    ("amount left as text", '"amount": float(row["amount"])', '"amount": row["amount"]'),
]


def run_tests(test_file: pathlib.Path, calculator_source: str, workdir: pathlib.Path):
    """Run pytest on a copy of test_file next to the given fee_calculator source."""
    workdir.mkdir()
    (workdir / "pytest.ini").write_text("[pytest]\n")
    (workdir / "fee_calculator.py").write_text(calculator_source)
    (workdir / "test_fee_calculator.py").write_text(test_file.read_text())
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_fee_calculator.py"],
        cwd=workdir, capture_output=True, text=True, timeout=120,
    )


def uses(tree: ast.AST, feature: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            decorators = [ast.unparse(d) for d in node.decorator_list]
            if feature == "fixture" and any(d.startswith("pytest.fixture") for d in decorators):
                return True
            if feature == "parametrize" and any(d.startswith("pytest.mark.parametrize") for d in decorators):
                return True
            if feature == "tmp_path" and node.name.startswith("test") and \
                    "tmp_path" in [a.arg for a in node.args.args]:
                return True
        if feature == "raises" and isinstance(node, ast.Call) and ast.unparse(node.func) == "pytest.raises":
            return True
    return False


_real_results: dict = {}


def real_run(test_file: pathlib.Path, tmp_path: pathlib.Path):
    """Run the tests on the real code once per test-file content (cached)."""
    key = test_file.read_text()
    if key not in _real_results:
        _real_results[key] = run_tests(test_file, REAL, tmp_path / "real")
    return _real_results[key]


@pytest.mark.parametrize("feature", ["fixture", "parametrize", "raises", "tmp_path"])
def test_your_tests_use(mod, feature):
    tree = ast.parse(pathlib.Path(mod.__file__).read_text())
    assert uses(tree, feature), f"none of your tests uses {feature}"


def test_your_tests_pass_on_the_real_code(mod, tmp_path):
    result = real_run(pathlib.Path(mod.__file__), tmp_path)
    assert result.returncode == 0, result.stdout[-3000:]
    passed = int(result.stdout.strip().splitlines()[-1].split(" passed")[0].split()[-1])
    assert passed >= 8, f"only {passed} tests ran: aim for at least 8 (parametrize cases count)"


@pytest.mark.parametrize("bug,original,broken", MUTANTS, ids=[m[0] for m in MUTANTS])
def test_your_tests_catch_the_bug(mod, tmp_path, bug, original, broken):
    assert original in REAL, "fee_calculator.py was edited: restore the original"
    assert real_run(pathlib.Path(mod.__file__), tmp_path).returncode == 0, \
        "first make your tests pass on the real code (see test_your_tests_pass_on_the_real_code)"
    result = run_tests(pathlib.Path(mod.__file__), REAL.replace(original, broken), tmp_path / "mutant")
    assert result.returncode == 1, f"no test failed when the code had this bug: {bug}"
