import pytest
from lib.error_reporter import ErrorReporter

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Тест упал
        ErrorReporter.add_error(report)