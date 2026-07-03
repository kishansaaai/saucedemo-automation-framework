# SauceDemo Automation Framework

A robust, fully-featured UI automation framework built with Python, Selenium, and Pytest. This framework is designed to test the e-commerce flows of [SauceDemo (Swag Labs)](https://www.saucedemo.com/) with a focus on reliability in headless environments, clean architecture, and maintainability.

## Features

- **Page Object Model (POM):** Clean separation of UI locators/actions from test logic.
- **Robust Headless Execution:** Custom workarounds for known headless Chrome issues (e.g., JavaScript-based element clicking and React synthetic event triggers) to ensure 100% reliability in CI/CD pipelines.
- **Data-Driven Testing:** Uses `pytest.mark.parametrize` to run tests across multiple user personas (Standard, Problem, Performance Glitch).
- **Automated HTML Reporting:** Generates self-contained HTML reports with embedded screenshots for failed tests.
- **Parallel Execution Ready:** Designed with function-scoped WebDriver fixtures, making it fully compatible with `pytest-xdist` for parallel test execution without state leakage.
- **Graceful Failure Handling:** Expected failures (like hardcoded SauceDemo bugs for the `problem_user`) are explicitly marked using `pytest.mark.xfail`.

## Technology Stack

- **Language:** Python 3.12+
- **Browser Automation:** Selenium WebDriver
- **Testing Framework:** Pytest
- **Reporting:** pytest-html
- **WebDriver Management:** webdriver-manager (automatically downloads and manages ChromeDriver)

## Project Structure

```text
saucedemo-framework/
├── pages/                  # Page Object classes (UI interaction logic)
│   ├── base_page.py        # Core Selenium wrapper methods (waits, clicks, etc.)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                  # Pytest test files (Business logic and assertions)
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
├── utils/                  # Test data and utility functions
│   └── test_data.py
├── reports/                # Generated test reports
├── screenshots/            # Failure screenshots (auto-captured on test failure)
├── conftest.py             # Pytest fixtures and hooks (WebDriver setup, teardown, reporting)
├── pytest.ini              # Pytest configuration
└── requirements.txt        # Project dependencies
```

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/saucedemo-automation-framework.git
   cd saucedemo-automation-framework
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Tests

To run the entire test suite and generate an HTML report:

```bash
pytest -v --html=reports/report.html --self-contained-html
```

### Running specific tests:

- **Run only login tests:**
  ```bash
  pytest tests/test_login.py -v
  ```

- **Run checkout tests and show stdout:**
  ```bash
  pytest tests/test_checkout.py -v -s
  ```

- **Run a specific test by name:**
  ```bash
  pytest -k "test_full_checkout_flow_completes" -v
  ```

- **Run in headed mode (visible browser window):**
  *(By default, the framework runs in headless mode)*
  ```bash
  pytest --no-headless
  ```

## Test Reports

After running the tests, a detailed HTML report will be generated in the `reports/` directory (`reports/report.html`). 
If any test fails, a screenshot will automatically be captured and embedded directly into the HTML report for easy debugging.

## Key Design Decisions

- **JavaScript Clicks & React Event Setters:** Headless Chrome on Windows is known to occasionally drop standard WebDriver clicks and keystrokes, especially in React applications. To guarantee absolute stability, `base_page.py` utilizes `execute_script("arguments[0].click();")` for button interactions and dispatches native React synthetic `input` and `change` events when typing text.
- **Function-Scoped Drivers:** The WebDriver fixture in `conftest.py` is deliberately scoped to `function`. This ensures a pristine browser state (clean cookies and local storage) for every test, eliminating state leakage and making the suite safe for parallel execution.
