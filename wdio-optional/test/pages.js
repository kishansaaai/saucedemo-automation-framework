// Lightweight POM mirroring pages/login_page.py and pages/inventory_page.py.
// Kept in one file for this optional layer since it only covers a login +
// smoke-check scenario; the Python suite is the full-coverage framework.

class LoginPage {
  get usernameInput() { return $('#user-name'); }
  get passwordInput() { return $('#password'); }
  get loginButton() { return $('#login-button'); }
  get errorMessage() { return $("[data-test='error']"); }

  async open() {
    await browser.url('/');
  }

  async login(username, password) {
    await this.usernameInput.setValue(username);
    await this.passwordInput.setValue(password);
    await this.loginButton.click();
  }
}

class InventoryPage {
  get pageTitle() { return $('.title'); }
  get cartBadge() { return $('.shopping_cart_badge'); }

  addToCart(itemName) {
    const slug = itemName.toLowerCase().replace(/ /g, '-').replace(/\./g, '');
    return $(`#add-to-cart-${slug}`);
  }

  async isLoaded() {
    return this.pageTitle.isDisplayed();
  }
}

module.exports = { LoginPage, InventoryPage };
