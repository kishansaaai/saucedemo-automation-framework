# SauceDemo Automation Framework

A production-grade, fully-featured UI automation framework built with Python, Selenium WebDriver, and Pytest. This repository serves as a comprehensive test suite designed to validate the core e-commerce workflows of [SauceDemo (Swag Labs)](https://www.saucedemo.com/). 

The framework is engineered with a strict focus on reliability in headless CI/CD environments, clean architecture through the Page Object Model (POM), and high maintainability.

## Table of Contents
- [Architecture & Design Patterns](#architecture--design-patterns)
- [Handling Headless Chrome Flakiness](#handling-headless-chrome-flakiness)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Test Execution Guide](#test-execution-guide)
- [Test Reports](#test-reports)
- [Continuous Integration](#continuous-integration)

---

## Architecture & Design Patterns

### Page Object Model (POM)
The framework strictly adheres to the Page Object Model design pattern. All UI locators and interactions are encapsulated within dedicated page classes (`pages/`). Test files (`tests/`) contain zero Selenium locators or WebDriver calls. This ensures that if the UI changes, updates are made in a single location, preventing brittle and high-maintenance test scripts.

### Pytest Fixtures & State Management
WebDriver lifecycle management is handled via Pytest fixtures in `conftest.py`. We use a `function` scoped driver fixture. This guarantees a completely pristine browser state (clean cookies, local storage, and session data) for every individual test. This deliberate design choice eliminates state leakage between tests and makes the suite inherently safe for parallel execution.

### Data-Driven Testing
The framework leverages `pytest.mark.parametrize` extensively. For instance, the core checkout flow is validated across multiple user personas (Standard User, Problem User, Performance Glitch User) using a single, parameterized test function. This maximizes test coverage while minimizing code duplication.

### Expected Failures
SauceDemo intentionally includes bugs for specific personas (e.g., the `problem_user` cannot update their Last Name in the checkout form). Instead of avoiding these, the framework tests them and marks them explicitly using `pytest.mark.xfail(strict=False)`. This documents known application bugs directly in the test suite without failing the CI pipeline.

---

## Handling Headless Chrome Flakiness

One of the major engineering challenges in modern UI automation is the unreliability of headless browsers when interacting with React-based applications on certain operating systems (like Windows). This framework implements robust, battle-tested workarounds:

1. **JavaScript Clicks:** Standard WebDriver `element.click()` can be silently dropped by headless Chrome. To guarantee absolute stability, all button clicks in this framework are executed natively via the browser engine using `driver.execute_script("arguments[0].click();", element)`.
2. **React Synthetic Event Setters:** Headless Chrome frequently drops individual keystrokes when using `send_keys()`. To solve this, the framework uses a custom JavaScript setter that directly accesses the React component's value descriptor and dispatches native `input` and `change` events. This ensures 100% reliability when populating forms, bypassing WebDriver entirely for text input.

---

## Project Structure

```text
saucedemo-framework/
├── pages/                  # Page Object classes (UI interaction logic)
│   ├── base_page.py        # Core Selenium wrapper (waits, JS clicks, JS typing)
│   ├── login_page.py       # Login screen interactions
│   ├── inventory_page.py   # Product listing and sorting
│   ├── cart_page.py        # Cart management
│   └── checkout_page.py    # Multi-step checkout wizard
├── tests/                  # Pytest test files (Business logic and assertions)
│   ├── test_login.py       # Authentication validation
│   ├── test_inventory.py   # Product listing validation
│   ├── test_cart.py        # Cart state persistence tests
│   └── test_checkout.py    # End-to-End purchase flows and validation checks
├── utils/                  # Test data and utility functions
│   └── test_data.py        # Centralized constants, credentials, and test payloads
├── reports/                # Generated test reports (HTML)
├── screenshots/            # Failure screenshots (auto-captured on test failure)
├── conftest.py             # Pytest fixtures and hooks (WebDriver setup, teardown, reporting)
├── pytest.ini              # Pytest configuration and CLI defaults
└── requirements.txt        # Project dependencies
```

---

## Prerequisites

Ensure you have the following installed on your local machine:
- **Python:** Version 3.12 or higher.
- **Git:** For version control.
- **Google Chrome:** The framework uses `webdriver-manager` to automatically download the ChromeDriver matching your installed Chrome version.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kishansaaai/saucedemo-automation-framework.git
   cd saucedemo-automation-framework
   ```

2. **Create and activate a virtual environment (Recommended):**
   ```bash
   # On Windows
   python -m venv venv
   source venv/Scripts/activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Test Execution Guide

The framework is highly configurable via the Pytest CLI.

### Standard Execution (Headless + HTML Report)
Run the entire test suite in headless mode (default) and generate a detailed HTML report:
```bash
pytest -v --html=reports/report.html --self-contained-html
```

### Visible Browser Execution (Headed Mode)
To watch the tests execute in a visible Chrome window, pass the custom `--no-headless` flag:
```bash
pytest --no-headless -v
```

### Running Specific Test Modules
Execute tests belonging to a specific feature area:
```bash
pytest tests/test_checkout.py -v
pytest tests/test_login.py -v
```

### Running Specific Test Cases
Execute a single test function by matching its name using the `-k` flag:
```bash
pytest -k "test_full_checkout_flow_completes" -v
```

### Parallel Execution (Optional)
Because the framework guarantees test isolation, you can drastically reduce execution time by running tests in parallel using `pytest-xdist`.
```bash
# Run tests across 4 parallel workers
pytest -n 4 -v
```

---

## Test Reports

The framework utilizes `pytest-html` to generate comprehensive test reports. 
- After a test run, open `reports/report.html` in your web browser.
- **Automatic Failure Screenshots:** A custom Pytest hook in `conftest.py` is configured to automatically capture a full-page screenshot the moment a test fails. This screenshot is encoded as a base64 string and embedded directly into the HTML report, allowing for immediate visual debugging without relying on external file artifacts.

---

## Continuous Integration

This repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that automatically runs the entire test suite on every push and pull request to the `main` branch. 
- The CI pipeline executes the tests on an `ubuntu-latest` runner using Headless Chrome.
- Test reports and failure screenshots are automatically uploaded as pipeline artifacts for review.
