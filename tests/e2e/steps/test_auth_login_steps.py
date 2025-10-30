from pytest_bdd import scenario, given, when, then
from tests.utils.config import BASE_URL, DEFAULT_USERNAME, DEFAULT_PASSWORD
from tests.e2e.pages.auth_loginpage import auth_loginpage


@scenario("../features/auth_login.feature", "login to the application")
def test_auth_login():
    """pytest-bdd scenario binding for the auth login feature."""
    pass


@given("the user navigates to the login page")
def navigate_to_login(page):
    # Navigate to the configured base URL's login page
    # create and store the page object on the Playwright page so subsequent steps can reuse it
    page.auth_page = auth_loginpage(page)
    page.auth_page.navigate()


@when("the user logs in with valid credentials")
def login_with_env_creds(page):
    # Use the page object stored in the Given step (or create one if missing)
    auth_page = getattr(page, "auth_page", None)
    if auth_page is None:
        auth_page = auth_loginpage(page)

    # This will use DEFAULT_USERNAME/DEFAULT_PASSWORD from config when arguments are omitted
    auth_page.login()
    page.wait_for_load_state("networkidle")


@then("the logged in succesfully message should be displayed")
def verify_logged_in(page):
    """Verify successful login.

    Uses multiple verification strategies:
    1. Check for Logout/Sign Out elements
    2. Verify URL is no longer /login
    3. Take screenshot on failure (via conftest.py fixture)
    """
    # Prefer presence of a logout/profile element; otherwise ensure we're not on the login page.
    try:
        # Wait for any of these to appear (more reliable than immediate check)
        success_elements = [
            'text=Logout',
            'text=Sign Out',
            '[aria-label="User Menu"]',
            '.user-profile',  # common profile container class
        ]
        for selector in success_elements:
            try:
                if page.locator(selector).count() > 0:
                    return  # found a success indicator
            except Exception:
                continue

        # No explicit success elements found, check URL
        page.wait_for_load_state("networkidle")  # ensure navigation complete
        if "/login" not in page.url:
            return

        # If we get here, login likely failed
        raise AssertionError(
            f"Login verification failed. Current URL: {page.url}")
    except Exception as e:
        # Screenshot will be taken by conftest.py fixture on failure
        raise AssertionError(f"Login verification failed: {str(e)}")
