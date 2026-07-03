from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "https://www.saucedemo.com/cart.html"

    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def get_item_names(self):
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def get_item_count(self):
        return len(self.find_all(self.CART_ITEM)) if self.is_visible(self.CART_ITEM, timeout=2) else 0

    def remove_item(self, item_name):
        slug = item_name.lower().replace(" ", "-").replace(".", "")
        locator = (By.ID, f"remove-{slug}")
        self.click(locator)

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
