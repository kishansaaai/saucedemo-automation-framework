import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Covers all three SauceDemo checkout steps (info -> overview -> complete).
    One page object spans three URLs because the steps share a single linear
    wizard flow and don't warrant three near-empty classes; each method group
    is clearly namespaced (step_one_*, step_two_*, complete_*) so it stays
    readable without over-fragmenting the POM."""

    STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"
    STEP_TWO_URL = "https://www.saucedemo.com/checkout-step-two.html"
    COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

    # ---- step one: customer info -------------------------------------
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # ---- step two: overview --------------------------------------------
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    # ---- complete ---------------------------------------------------
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def fill_customer_info(self, first_name, last_name, postal_code):
        time.sleep(0.1)
        if first_name:
            self.type_text(self.FIRST_NAME_INPUT, first_name)
        if last_name:
            self.type_text(self.LAST_NAME_INPUT, last_name)
        if postal_code:
            self.type_text(self.POSTAL_CODE_INPUT, postal_code)

    def continue_to_overview(self):
        self.click(self.CONTINUE_BUTTON)
        # Wait up to 8 s for navigation away from step-one (either step-two loads
        # or validation blocks and we stay — either way wait settles the page).
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: "checkout-step-one.html" not in d.current_url
            )
        except Exception:
            pass  # validation blocked — we stay on step-one, that's expected

    def get_error_text(self):
        return self.get_text(self.ERROR_MESSAGE)

    def has_error(self):
        """Return True if the checkout form shows a validation error.

        Checks two signals:
          1. The <h3 data-test="error"> message element (full visible error).
          2. Any input marked with the 'input_error' CSS class — headless Chrome
             sometimes omits rendering the error text node but still marks fields
             invalid and blocks navigation, so the class check is the fallback.
        """
        if self.is_visible(self.ERROR_MESSAGE, timeout=3):
            return True
        # Headless fallback: React marks invalid inputs with input_error
        error_inputs = self.driver.find_elements(
            By.CSS_SELECTOR, "input.input_error"
        )
        return len(error_inputs) > 0

    def get_subtotal(self):
        text = self.get_text(self.SUBTOTAL_LABEL)  # "Item total: $29.99"
        return float(text.split("$")[1])

    def get_total(self):
        text = self.get_text(self.TOTAL_LABEL)  # "Total: $32.19"
        return float(text.split("$")[1])

    def finish(self):
        self.click(self.FINISH_BUTTON)

    def is_order_complete(self):
        return self.is_visible(self.COMPLETE_HEADER)

    def get_complete_header_text(self):
        return self.get_text(self.COMPLETE_HEADER)


