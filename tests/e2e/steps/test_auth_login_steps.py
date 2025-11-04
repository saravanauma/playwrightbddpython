from pytest_bdd import scenario, given, when, then
from tests.utils.config import BASE_URL, DEFAULT_USERNAME, DEFAULT_PASSWORD
from tests.e2e.pages.auth_loginpage import auth_loginpage
from tests.utils.logger import logger


@scenario("../features/auth_login.feature", "login to the application")
def test_auth_login():
    """pytest-bdd scenario binding for the auth login feature."""
    logger.info("Starting scenario: login to the application")
    pass


@given("the user navigates to the login page")
def navigate_to_login(page):
    logger.info("Step: Navigating to the login page (%s/login)", BASE_URL)
    page.auth_page = auth_loginpage(page)
    page.auth_page.navigate()


@when("the user logs in with valid credentials")
def login_with_env_creds(page):
    logger.info("Step: Logging in with credentials (username: %s)",
                DEFAULT_USERNAME)
    auth_page = page.auth_page
    auth_page.login()
    logger.info("Login submitted, waiting for network idle...")
    page.wait_for_load_state("networkidle")
