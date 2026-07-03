"""
Centralized test data.

Design decision (why a single source of truth for users):
    SauceDemo ships several fixed accounts, each simulating a different class
    of production bug. Keeping them here (instead of inline string literals
    in every test) means:
      - One place to update if SauceDemo ever changes credentials.
      - Tests can be parametrized over *lists* of these constants, so adding
        a new user type to a suite is a one-line change, not a copy-pasted
        test function.
"""

VALID_PASSWORD = "secret_sauce"

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
PERFORMANCE_GLITCH_USER = "performance_glitch_user"
ERROR_USER = "error_user"
VISUAL_USER = "visual_user"

# Users expected to be able to log in and shop normally (used for
# data-driven / parametrized functional tests).
FUNCTIONAL_USERS = [
    STANDARD_USER,
    PROBLEM_USER,
    PERFORMANCE_GLITCH_USER,
]

# A representative product name present on every account's inventory page.
SAMPLE_PRODUCT = "Sauce Labs Backpack"
SAMPLE_PRODUCT_2 = "Sauce Labs Bike Light"

CHECKOUT_INFO = {
    "first_name": "Jane",
    "last_name": "Doe",
    "postal_code": "94107",
}
