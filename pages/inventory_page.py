from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    URL = "https://www.saucedemo.com/inventory.html"

    # ---- locators ----------------------------------------------------
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def is_loaded(self):
        return self.is_visible(self.PAGE_TITLE)

    def add_to_cart(self, item_name):
        """Buttons are id'd as add-to-cart-<slugified-name>; building the
        locator from the product name keeps this generic across products."""
        slug = item_name.lower().replace(" ", "-").replace(".", "")
        locator = (By.ID, f"add-to-cart-{slug}")
        self.click(locator)

    def remove_from_cart(self, item_name):
        slug = item_name.lower().replace(" ", "-").replace(".", "")
        locator = (By.ID, f"remove-{slug}")
        self.click(locator)

    def get_cart_count(self):
        if self.is_visible(self.CART_BADGE, timeout=2):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def sort_by(self, option_value):
        """option_value examples: 'az', 'za', 'lohi', 'hilo'"""
        self.select_dropdown_by_value(self.SORT_DROPDOWN, option_value)

    def get_all_item_names(self):
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def get_all_item_prices(self):
        prices = self.find_all(self.ITEM_PRICE)
        return [float(p.text.replace("$", "")) for p in prices]

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)



