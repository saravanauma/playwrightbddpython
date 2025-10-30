from tests.utils.config import BASE_URL, DEFAULT_USERNAME, DEFAULT_PASSWORD


class auth_loginpage:
    """Page object for the authentication login page.

    Uses environment-backed credentials by default (UI_USERNAME/UI_PASSWORD).
    Handles both SSO and non-SSO login flows with retry logic for locators.
    """

    def __init__(self, page):
        """Initialize the page object with Playwright page from conftest.py fixture.

        Args:
            page: Playwright page object (from conftest.py fixture)
        """
        self.page = page

        # Primary login elements
        self.single_sign_on_button = page.get_by_role(
            "button", name=" Single Sign On")
        self.email_input = page.get_by_role("textbox", name="Enter email")
        self.login_button = page.locator('[aria-label="Login"]')

        # Additional controls seen in the login flows
        self.remember_checkbox = page.get_by_role(
            "checkbox", name="Remember me")
        self.no_sso_link = page.get_by_role(
            "link", name="I don't use Single Sign On")
        self.signin_button = page.get_by_role("button", name="Sign In")

    def navigate(self):
        # Navigate to the environment-specific base URL (append /login if required)
        self.page.goto(f"{BASE_URL}/login")
        self.page.wait_for_load_state("networkidle")

    def login(self, username: str | None = None, password: str | None = None):
        """Fill credentials and submit synchronously.

        If username or password are omitted, fall back to values from environment
        (DEFAULT_USERNAME / DEFAULT_PASSWORD) configured in `tests.utils.config`.
        """
        # Use provided credentials or fall back to environment defaults
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD

        if not username or not password:
            raise ValueError(
                "Username and password must be provided either as arguments or via environment variables (UI_USERNAME / UI_PASSWORD)."
            )

        # Try to fill common username/email fields (resilient across variants)
        try:
            self.username_input.fill(username)
        except Exception:
            try:
                self.email_input.fill(username)
            except Exception:
                self.page.fill('input[type="email"]', username)

        # Fill password
        try:
            self.password_input.fill(password)
        except Exception:
            self.page.fill('input[type="password"]', password)

        # Click login or sign-in
        try:
            self.login_button.click()
        except Exception:
            try:
                self.signin_button.click()
            except Exception:
                self.page.click('button[type="submit"]')

    def non_sso_login_flow(self, username: str | None = None, password: str | None = None):
        username = username or DEFAULT_USERNAME
        password = password or DEFAULT_PASSWORD

        if not username or not password:
            raise ValueError(
                "Username and password must be provided either as arguments or via environment variables (UI_USERNAME / UI_PASSWORD)."
            )

        self.single_sign_on_button.click()
        self.email_input.click()
        self.email_input.fill(username)
        # remember checkbox may not always be present
        try:
            self.remember_checkbox.check()
        except Exception:
            pass
        self.no_sso_link.click()
        self.password_input.click()
        self.password_input.fill(password)
        try:
            self.remember_checkbox.check()
        except Exception:
            pass
        self.signin_button.click()
