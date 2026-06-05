"""
Cart tests: add/remove items and cart persistence across navigation.

'Persistence' here means the cart badge count (and cart contents) must
survive navigating away from the inventory page and back -- e.g. via the
product sort dropdown, or opening/closing the cart page -- without a
server round trip resetting it. This is a common regression class in SPA-ish
apps that manage cart state client-side.
"""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils import test_data as data


def _login(driver, username=data.STANDARD_USER):
    login_page = LoginPage(driver).load()
    login_page.login(username, data.VALID_PASSWORD)
    return InventoryPage(driver)


def test_add_single_item_updates_badge(driver):
    inventory_page = _login(driver)
    inventory_page.add_to_cart(data.SAMPLE_PRODUCT)
    assert inventory_page.get_cart_count() == 1


def test_add_multiple_items_updates_badge(driver):
    inventory_page = _login(driver)
    inventory_page.add_to_cart(data.SAMPLE_PRODUCT)
    inventory_page.add_to_cart(data.SAMPLE_PRODUCT_2)
    assert inventory_page.get_cart_count() == 2


def test_remove_item_from_inventory_page(driver):
    inventory_page = _login(driver)
    inventory_page.add_to_cart(data.SAMPLE_PRODUCT)
    assert inventory_page.get_cart_count() == 1

    inventory_page.remove_from_cart(data.SAMPLE_PRODUCT)
    assert inventory_page.get_cart_count() == 0


def test_remove_item_from_cart_page(driver):
    inventory_page = _login(driver)
    inventory_page.add_to_cart(data.SAMPLE_PRODUCT)
    inventory_page.go_to_cart()

    cart_page = CartPage(driver)
    assert cart_page.get_item_count() == 1
    cart_page.remove_item(data.SAMPLE_PRODUCT)
    assert cart_page.get_item_count() == 0


def test_cart_persists_after_sorting(driver):
    """Adding to cart, then re-sorting the product grid, should not clear
    the cart -- sorting only reorders the DOM, it shouldn't touch cart state."""
    inventory_page = _login(driver)
    inventory_page.add_to_cart(data.SAMPLE_PRODUCT)
    inventory_page.sort_by("za")
    assert inventory_page.get_cart_count() == 1


def test_cart_persists_when_navigating_to_cart_and_back(driver):
    inventory_page = _login(driver)
    inventory_page.add_to_cart(data.SAMPLE_PRODUCT)
    inventory_page.add_to_cart(data.SAMPLE_PRODUCT_2)

    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    assert cart_page.get_item_count() == 2

    cart_page.continue_shopping()
    inventory_page = InventoryPage(driver)
    assert inventory_page.get_cart_count() == 2


@pytest.mark.parametrize("username", data.FUNCTIONAL_USERS)
def test_cart_persists_across_users(driver, username):
    """Data-driven: the persistence behavior itself should hold for every
    functional user type, not just standard_user."""
    inventory_page = _login(driver, username)
    inventory_page.add_to_cart(data.SAMPLE_PRODUCT)
    inventory_page.go_to_cart()

    cart_page = CartPage(driver)
    assert cart_page.get_item_count() == 1
    assert data.SAMPLE_PRODUCT in cart_page.get_item_names()


def test_removing_nonexistent_cart_does_not_error(driver):
    """Negative/edge case: visiting the cart page with nothing added should
    render an empty cart rather than erroring out."""
    inventory_page = _login(driver)
    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    assert cart_page.get_item_count() == 0


