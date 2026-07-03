"""
BasePage: shared Selenium plumbing for every page object.

Design decision (POM):
    Every concrete page (LoginPage, InventoryPage, ...) inherits from this
    class instead of re-implementing waits/finds. This means:
      - Locators live next to the page they belong to (single source of truth).
      - If SauceDemo changes a wait strategy or we swap explicit waits for
        something else, we change it in ONE place.
      - Tests never call driver.find_element(...) directly -> tests read like
        business language ("login_page.login(user, pw)") instead of Selenium
        boilerplate. This is the core interview point for POM: it separates
        "how to interact with the UI" (pages) from "what behavior we're
        verifying" (tests).
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class BasePage:
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    # ---- element helpers -------------------------------------------------
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        # Use JavaScript click to bypass headless Chrome silent drop issues
        self.driver.execute_script("arguments[0].click();", el)

    def type_text(self, locator, text):
        el = self.find(locator)
        # React-specific value setter to bypass headless keystroke dropping
        script = """
        var element = arguments[0];
        var value = arguments[1];
        var prototype = Object.getPrototypeOf(element);
        var valSetter = Object.getOwnPropertyDescriptor(prototype, "value")?.set;
        if (!valSetter) {
            prototype = window.HTMLInputElement.prototype;
            valSetter = Object.getOwnPropertyDescriptor(prototype, "value").set;
        }
        valSetter.call(element, value);
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
        """
        self.driver.execute_script(script, el, text)
        time.sleep(0.05)

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator, timeout=None):
        try:
            WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, fragment, timeout=None):
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT).until(
            EC.url_contains(fragment)
        )

    def select_dropdown_by_value(self, locator, value):
        from selenium.webdriver.support.ui import Select
        Select(self.find(locator)).select_by_value(value)

    def current_url(self):
        return self.driver.current_url

    def take_screenshot(self, name):
        """Used by the pytest failure hook, but exposed here too in case a
        page wants to snapshot mid-flow for debugging."""
        path = f"screenshots/{name}_{int(time.time())}.png"
        self.driver.save_screenshot(path)
        return path
