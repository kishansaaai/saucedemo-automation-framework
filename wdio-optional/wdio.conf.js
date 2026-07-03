// wdio.conf.js
// Optional secondary layer: same target app (saucedemo.com), same POM
// philosophy, different stack (JS/Mocha/WebdriverIO) instead of
// Python/Pytest/Selenium. This exists to demonstrate the POM pattern is a
// design principle, not a library feature -- it ports across language and
// tooling boundaries. The Python/Pytest suite is the primary, fully-featured
// framework; this is a lighter proof-of-concept layer.
exports.config = {
  runner: 'local',
  specs: ['./test/specs/**/*.spec.js'],
  maxInstances: 1,
  capabilities: [
    {
      browserName: 'chrome',
      'goog:chromeOptions': {
        args: ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--window-size=1400,1000'],
      },
    },
  ],
  logLevel: 'warn',
  baseUrl: 'https://www.saucedemo.com',
  waitforTimeout: 10000,
  connectionRetryTimeout: 120000,
  connectionRetryCount: 3,
  framework: 'mocha',
  reporters: ['spec'],
  mochaOpts: {
    ui: 'bdd',
    timeout: 60000,
  },
};
