"""Lab 12 tests a PACKAGE, not a single file, so instead of the shared `mod` fixture it uses `pkg`:
it imports payments_tools from exercise/ (default) or solution/ (--solution)."""
import ast
import importlib
import os
import pathlib
import subprocess
import sys

import pytest

HERE = pathlib.Path(__file__).parent
ASHA = {"payments": 31, "success": 29, "failed": 1, "pending": 1, "success_total": 21441.2}
ASHA_OUTPUT = "payments: 31\nsuccess: 29\nfailed: 1\npending: 1\nsuccess total: 21441.20\n"


def forget_package():
    for name in [m for m in sys.modules if m == "payments_tools" or m.startswith("payments_tools.")]:
        del sys.modules[name]


@pytest.fixture
def root(request):
    """The folder that contains the payments_tools package."""
    return HERE / ("solution" if request.config.getoption("--solution") else "exercise")


@pytest.fixture
def pkg(root):
    forget_package()
    sys.path.insert(0, str(root))
    try:
        yield importlib.import_module("payments_tools")
    finally:
        sys.path.remove(str(root))
        forget_package()


def run_module(root, *args):
    env = {**os.environ, "PYTHONPATH": str(root)}
    return subprocess.run([sys.executable, "-m", *args], capture_output=True, text=True, env=env, timeout=60)


def test_package_api(pkg):
    assert pkg.__version__ == "0.1.0"
    assert sorted(pkg.__all__) == ["load_payments", "summarize", "summarize_file"]
    assert pkg.load_payments is importlib.import_module("payments_tools.loader").load_payments
    assert pkg.summarize is importlib.import_module("payments_tools.stats").summarize


def test_stats_uses_a_relative_import(pkg, root):
    tree = ast.parse((root / "payments_tools" / "stats.py").read_text())
    relative = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.level >= 1]
    assert any(n.module == "loader" and "load_payments" in [a.name for a in n.names] for n in relative)


def test_summarize(pkg):
    rows = [{"account_id": 4201, "amount": 100.0, "status": "success"},
            {"account_id": 4201, "amount": 50.0, "status": "failed"},
            {"account_id": 4301, "amount": 70.25, "status": "success"}]
    assert pkg.summarize(rows) == {"payments": 3, "success": 2, "failed": 1, "pending": 0, "success_total": 170.25}
    assert pkg.summarize(rows, 4301)["payments"] == 1


def test_summarize_file_for_asha(pkg, payments_csv):
    assert pkg.summarize_file(payments_csv, 4201) == ASHA
    assert pkg.summarize_file(payments_csv)["payments"] == 1000


def test_cli_main_prints_summary(pkg, payments_csv, capsys):
    cli = importlib.import_module("payments_tools.cli")
    assert cli.main([str(payments_csv), "--account", "4201"]) == 0
    assert capsys.readouterr().out == ASHA_OUTPUT


def test_cli_main_missing_file(pkg, capsys):
    cli = importlib.import_module("payments_tools.cli")
    assert cli.main(["no_such_file.csv"]) == 1
    captured = capsys.readouterr()
    assert captured.out == "" and "no such file: no_such_file.csv" in captured.err


def test_run_cli_module_with_dash_m(root, payments_csv):
    result = run_module(root, "payments_tools.cli", str(payments_csv), "--account", "4201")
    assert result.returncode == 0, result.stderr
    assert result.stdout == ASHA_OUTPUT


def test_run_package_with_dash_m(root, payments_csv):
    result = run_module(root, "payments_tools", str(payments_csv), "--account", "4201")
    assert result.returncode == 0, result.stderr
    assert result.stdout == ASHA_OUTPUT
    assert run_module(root, "payments_tools", "missing.csv").returncode == 1
