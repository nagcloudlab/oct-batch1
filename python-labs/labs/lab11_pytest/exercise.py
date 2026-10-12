"""Lab 11 · Testing with pytest: YOUR tests for fee_calculator.py go in this file.

This file plays the role of test_fee_calculator.py. Run just your tests with:
    pytest labs/lab11_pytest/exercise.py -v
Replace every stub below with real tests (rename them, add more, delete the stubs).
"""
import pytest

import fee_calculator
from fee_calculator import calculate_fee, load_payments, total_fees


# ---------------------------------------------------------------- Task 1: a fixture
def test_total_fees_charges_only_successful_payments():
    """Task 1: write a fixture `sample_payments` returning a few payment dicts
    (amount, channel, status), including at least one failed and one pending payment.
    Then make this test take `sample_payments` as a parameter and check total_fees()."""
    raise NotImplementedError("TODO: task 1")


# ---------------------------------------------------------------- Task 2: parametrize
def test_calculate_fee():
    """Task 2: ONE parametrized test (amount, channel, expected) that covers every fee rule
    in fee_calculator's docstring: each channel's rate, the card minimum and the cap."""
    raise NotImplementedError("TODO: task 2")


# ---------------------------------------------------------------- Task 3: errors
def test_rejects_bad_input():
    """Task 3: check that a zero or negative amount and an unknown channel raise ValueError
    (use the pytest.raises context manager; match= checks the message)."""
    raise NotImplementedError("TODO: task 3")


# ---------------------------------------------------------------- Task 4: files
def test_load_payments_reads_a_csv():
    """Task 4: ask for the built-in tmp_path fixture, write a two-row CSV into it
    (same header as data/payments.csv), call load_payments() and check the rows
    (is the amount a float?)."""
    raise NotImplementedError("TODO: task 4")
