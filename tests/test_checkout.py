"""
Checkout flow tests: full end-to-end purchase, price-math sanity check, and
negative cases for each required field being empty.
"""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils import test_data as data


def _login_and_add_item(driver, username=data.STANDARD_USER):
    login_page = LoginPage(driver).load()
    login_page.login(username, data.VALID_PASSWORD)
    inventory_page = InventoryPage(driver)
    inventory_page.add_to_cart(data.SAMPLE_PRODUCT)
    inventory_page.go_to_cart()
    CartPage(driver).checkout()
    return CheckoutPage(driver)


@pytest.mark.parametrize(
    "username",
    [
        data.STANDARD_USER,
        pytest.param(
            data.PROBLEM_USER,
            marks=pytest.mark.xfail(
                reason="problem_user has a hardcoded bug on SauceDemo where Last Name input updates are blocked",
                strict=False,
            ),
        ),
        data.PERFORMANCE_GLITCH_USER,
    ],
)
def test_full_checkout_flow_completes(driver, username):
    """End-to-end happy path: login -> add to cart -> checkout info ->
    overview -> finish -> confirmation. Parametrized across user types so we
    know the *entire* purchase funnel, not just login, works for each."""
    checkout_page = _login_and_add_item(driver, username)

    checkout_page.fill_customer_info(**data.CHECKOUT_INFO)
    checkout_page.continue_to_overview()

    assert "checkout-step-two.html" in checkout_page.current_url()

    checkout_page.finish()

    assert checkout_page.is_order_complete()
    assert "thank you" in checkout_page.get_complete_header_text().lower()


def test_checkout_overview_total_includes_tax(driver):
    checkout_page = _login_and_add_item(driver)
    checkout_page.fill_customer_info(**data.CHECKOUT_INFO)
    checkout_page.continue_to_overview()

    subtotal = checkout_page.get_subtotal()
    total = checkout_page.get_total()
    assert total > subtotal, "Total should be greater than subtotal once tax is applied"


@pytest.mark.parametrize(
    "first_name,last_name,postal_code,missing_field",
    [
        ("", "Doe", "94107", "first name"),
        ("Jane", "", "94107", "last name"),
        ("Jane", "Doe", "", "postal code"),
        ("", "", "", "first name"),
    ],
    ids=["missing_first_name", "missing_last_name", "missing_postal_code", "all_fields_empty"],
)
def test_checkout_blocks_on_missing_required_fields(
    driver, first_name, last_name, postal_code, missing_field
):
    """Negative/edge case: submitting the checkout-info step with any
    required field blank must block progression and show an inline error,
    never silently advance to the overview step."""
    checkout_page = _login_and_add_item(driver)
    checkout_page.fill_customer_info(first_name, last_name, postal_code)
    checkout_page.continue_to_overview()

    assert checkout_page.has_error(), f"Expected a validation error for missing {missing_field}"
    assert "checkout-step-two.html" not in checkout_page.current_url()


def test_checkout_can_be_cancelled_from_overview(driver):
    """Edge case: cancelling from the overview step should return to
    inventory without completing the order, and cart contents should
    remain untouched."""
    checkout_page = _login_and_add_item(driver)
    checkout_page.fill_customer_info(**data.CHECKOUT_INFO)
    checkout_page.continue_to_overview()

    checkout_page.click(CheckoutPage.CANCEL_BUTTON)

    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded()
    assert inventory_page.get_cart_count() == 1, "Cart should still hold the item after cancelling checkout"

