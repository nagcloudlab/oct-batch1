"""Shared pytest setup for all labs.

Run a lab against YOUR code:        pytest labs/lab02_comprehensions
Run it against the worked solution: pytest labs/lab02_comprehensions --solution
"""
import importlib.util
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).parent


def pytest_addoption(parser):
    parser.addoption("--solution", action="store_true",
                     help="test solution.py instead of exercise.py")


@pytest.fixture
def mod(request):
    """The module under test: exercise.py (default) or solution.py (--solution)."""
    name = "solution" if request.config.getoption("--solution") else "exercise"
    path = pathlib.Path(str(request.fspath)).parent / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"{path.parent.name}_{name}", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up here
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def payments_csv():
    """Path to the shared sample data: 1,000 payments."""
    return ROOT / "data" / "payments.csv"
