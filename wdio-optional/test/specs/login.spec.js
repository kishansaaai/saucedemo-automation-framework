const { expect } = require('@wdio/globals') || {};
const { LoginPage, InventoryPage } = require('../pages');

// This mirrors tests/test_login.py::test_login_valid_users_reach_inventory
// and a slice of tests/test_cart.py, just enough to prove the POM pattern
// and core flows hold in a second stack. Not a full port of the Pytest suite.
describe('SauceDemo login + add to cart (WebdriverIO smoke layer)', () => {
  const loginPage = new LoginPage();
  const inventoryPage = new InventoryPage();

  it('logs in with standard_user and reaches the inventory page', async () => {
    await loginPage.open();
    await loginPage.login('standard_user', 'secret_sauce');
    await expect(await inventoryPage.isLoaded()).toBe(true);
  });

  it('shows a locked-out error for locked_out_user', async () => {
    await loginPage.open();
    await loginPage.login('locked_out_user', 'secret_sauce');
    const errorText = await loginPage.errorMessage.getText();
    await expect(errorText.toLowerCase()).toContain('locked out');
  });

  it('adds an item to the cart and updates the badge count', async () => {
    await loginPage.open();
    await loginPage.login('standard_user', 'secret_sauce');
    await inventoryPage.addToCart('Sauce Labs Backpack').click();
    const badgeText = await inventoryPage.cartBadge.getText();
    await expect(badgeText).toBe('1');
  });
});
