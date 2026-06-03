"""
Login flow tests.

Why parametrize here:
    `test_login_valid_users_reach_inventory` runs the exact same assertion
    logic (login succeeds -> inventory page loads) for three different
    account types. Without parametrize we'd either copy/paste three near-
    identical test functions or loop *inside* one test -- which hides which
    specific user failed in the pytest report. `@pytest.mark.parametrize`
    gives us N distinct, individually-reportable test cases from one
    function body, each shown separately in the HTML report
    (e.g. test_login_valid_users_reach_inventory[problem_user]).
"""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils import test_data as data


@pytest.mark.parametrize("username", data.FUNCTIONAL_USERS)
def test_login_valid_users_reach_inventory(driver, username):
    login_page = LoginPage(driver).load()
    login_page.login(username, data.VALID_PASSWORD)

    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded(), f"{username} did not land on inventory page after login"
    assert "inventory.html" in inventory_page.current_url()


def test_login_locked_out_user_is_blocked(driver):
    """locked_out_user is SauceDemo's built-in 'disabled account' scenario."""
    login_page = LoginPage(driver).load()
    login_page.login(data.LOCKED_OUT_USER, data.VALID_PASSWORD)

    assert login_page.has_error()
    assert "locked out" in login_page.get_error_text().lower()
    # Negative assertion: we must NOT have navigated away from the login page.
    assert "inventory.html" not in login_page.current_url()


@pytest.mark.parametrize(
    "username,password,expected_error_fragment",
    [
        ("", "", "username is required"),
        ("standard_user", "", "password is required"),
        ("not_a_real_user", "wrong_password", "do not match"),
    ],
    ids=["empty_credentials", "missing_password", "invalid_credentials"],
)
def test_login_negative_cases(driver, username, password, expected_error_fragment):
    """Edge/negative cases for the login flow: blank fields and bad creds
    should all surface the SauceDemo inline error, never a silent failure
    or a crash."""
    login_page = LoginPage(driver).load()
    login_page.login(username, password)

    assert login_page.has_error(), "Expected an inline error message but none appeared"
    assert expected_error_fragment in login_page.get_error_text().lower()



