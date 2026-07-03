"""
conftest.py

Holds fixtures shared across the whole test suite (driver lifecycle) and the
pytest hook that captures a screenshot whenever a test fails. Living at the
project root makes these fixtures auto-discovered by pytest for every test
module without explicit imports.
"""
import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser headless (default: True). Use --no-headless to see the browser.",
    )
    parser.addoption(
        "--no-headless",
        action="store_false",
        dest="headless",
        help="Run with a visible browser window (useful for local debugging).",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests against (chrome only in this reference impl).",
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Function-scoped on purpose: a fresh browser session per test means tests
    are isolated (no shared cookies/localStorage/cart-state leaking between
    tests), which is what makes them safe to run in parallel with
    pytest-xdist later and safe to run in any order.
    """
    headless = request.config.getoption("--headless")

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,1000")

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)  # we rely on explicit waits in BasePage, not implicit ones

    yield drv

    drv.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Screenshot-on-failure hook.

    Runs after every test phase (setup/call/teardown). We only care about
    the 'call' phase (the actual test body) failing, and only when the test
    used the `driver` fixture. The screenshot filename embeds the test name
    and a timestamp so repeated failures don't overwrite each other, and
    pytest-html picks up the file via the extra we attach to `item`.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            safe_name = item.name.replace("[", "_").replace("]", "").replace("/", "_")
            filename = f"{safe_name}_{int(time.time())}.png"
            filepath = os.path.join(SCREENSHOT_DIR, filename)
            try:
                driver_fixture.save_screenshot(filepath)
                # Attach to pytest-html report if the plugin is active.
                if hasattr(item.config, "_html"):
                    from pytest_html import extras
                    extra = getattr(report, "extra", [])
                    extra.append(extras.image(filepath))
                    report.extra = extra
            except Exception as exc:  # noqa: BLE001 - best-effort screenshot
                print(f"Could not capture screenshot: {exc}")
