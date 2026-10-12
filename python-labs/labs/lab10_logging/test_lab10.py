import logging

import pytest

ASHA_OK = {"payment_id": 14, "account_id": 4201, "amount": 614.69, "status": "success"}


@pytest.fixture
def records(mod, caplog):
    """caplog captures records from every logger; we keep only this module's records."""
    caplog.set_level(logging.DEBUG, logger=mod.__name__)
    return lambda: [r for r in caplog.records if r.name == mod.__name__]


def test_module_logger(mod):
    assert isinstance(mod.logger, logging.Logger)
    assert mod.logger.name == mod.__name__


def test_mask_account(mod):
    assert mod.mask_account(4201) == "**01"
    assert mod.mask_account(4577) == "**77"


def test_success_logs_debug_then_info(mod, records):
    assert mod.process_payment(ASHA_OK) is True
    logged = [(r.levelname, r.getMessage()) for r in records()]
    assert logged == [("DEBUG", "processing payment 14 acct=**01"),
                      ("INFO", "payment 14 settled acct=**01 amount=614.69")]


@pytest.mark.parametrize("status,level,message", [
    ("failed", "ERROR", "payment 14 failed acct=**01"),
    ("pending", "INFO", "payment 14 pending acct=**01"),
])
def test_failed_and_pending(mod, records, status, level, message):
    assert mod.process_payment({**ASHA_OK, "status": status}) is False
    assert (level, message) in [(r.levelname, r.getMessage()) for r in records()]


def test_large_payment_warning(mod, records):
    mod.process_payment({**ASHA_OK, "amount": 95966.57})
    warnings = [r.getMessage() for r in records() if r.levelno == logging.WARNING]
    assert warnings == ["large payment 14 acct=**01 amount=95966.57"]


def test_lazy_formatting_and_no_raw_account_number(mod, records):
    mod.process_payment(ASHA_OK)
    mod.process_payment({**ASHA_OK, "status": "failed", "amount": 60000})
    recs = records()
    assert len(recs) >= 5          # debug+info, then debug+warning+error
    for r in recs:
        assert r.args, f"use %-style args, not an f-string: {r.msg!r}"
        assert "4201" not in r.getMessage()


def test_parse_amounts_logs_exception(mod, records):
    assert mod.parse_amounts(["10.5", "12,50", "7"]) == [10.5, 7.0]
    errors = [r for r in records() if r.levelno == logging.ERROR]
    assert len(errors) == 1
    assert errors[0].getMessage() == "skipping bad amount '12,50'"
    assert errors[0].exc_info and errors[0].exc_info[0] is ValueError   # traceback attached


def test_configure_logging_file_and_idempotent(mod, tmp_path):
    logfile = tmp_path / "app.log"
    name = "lab10_test_app"
    try:
        log = mod.configure_logging("WARNING", str(logfile), name=name)
        log = mod.configure_logging("INFO", str(logfile), name=name)       # called twice on purpose
        assert log is logging.getLogger(name) and log.level == logging.INFO
        assert len(log.handlers) == 2
        log.debug("not shown")
        log.info("settled %s", 14)
        for h in log.handlers:
            h.flush()
        lines = logfile.read_text().splitlines()
        assert len(lines) == 1 and lines[0].endswith(f"INFO {name}: settled 14")
    finally:
        for h in list(logging.getLogger(name).handlers):
            logging.getLogger(name).removeHandler(h)
            h.close()
