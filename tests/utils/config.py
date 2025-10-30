import os
from dotenv import load_dotenv
from pathlib import Path

# ================================================
# Load environment variables from .env (optional)
# ================================================
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# ================================================
# Environment configuration
# ================================================
ENV = os.getenv("ENV", "pre_staging").lower()

# Environment-specific URLs
BASE_URLS = {
    "pre_staging": "https://prestaging.app.dals.co.uk/",
    "staging": "https://staging.flipkart.com",
}

BASE_URL = BASE_URLS.get(ENV, BASE_URLS["pre_staging"])

# ================================================
# API configuration
# ================================================
API_BASE_URLS = {
    "pre_staging": "https://prestaging.app.dals.co.uk/",
    "staging": "https://staging.flipkart.com",
}

API_BASE_URL = API_BASE_URLS.get(ENV, API_BASE_URLS["pre_staging"])

# ================================================
# Database configuration
# ================================================
DB_CONFIG = {
    "pre_staging": {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "database": os.getenv("DB_NAME"),
        "ssl_disabled": os.getenv("DB_SSL_DISABLED", "true").lower() == "true"
    },
    "staging": {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "database": os.getenv("DB_NAME"),
        "ssl_disabled": os.getenv("DB_SSL_DISABLED", "true").lower() == "true"
    }
}

CURRENT_DB_CONFIG = DB_CONFIG.get(ENV, DB_CONFIG["pre_staging"])

# ================================================
# Playwright configuration
# ================================================
PLAYWRIGHT_CONFIG = {
    "headless": os.getenv("HEADLESS").lower() == "true",
    "slow_mo": int(os.getenv("SLOW_MO")),
    "timeout": int(os.getenv("PAGE_TIMEOUT"))
}

# ================================================
# Report configuration
# ================================================
REPORT_PATH = os.getenv("REPORT_PATH", "reports/")
ALLURE_RESULTS_PATH = os.path.join(REPORT_PATH, "allure-results")

# ================================================
# Default UI credentials (read from environment or .env)
# Preferred environment variable names: UI_USERNAME / UI_PASSWORD
# ================================================
DEFAULT_USERNAME = os.getenv("UI_USERNAME")
DEFAULT_PASSWORD = os.getenv("UI_PASSWORD")

# ================================================
# Helper: Print current configuration
# ================================================


def print_current_config():
    print(f"\n[ENVIRONMENT CONFIGURATION]")
    print(f"Environment: {ENV}")
    print(f"Base URL: {BASE_URL}")
    print(f"API Base URL: {API_BASE_URL}")
    print(f"Headless Mode: {PLAYWRIGHT_CONFIG['headless']}")
    print(f"DB Host: {CURRENT_DB_CONFIG['host']}")
    # Mask credentials when printing so secrets aren't shown in logs

    def _mask(value: str) -> str:
        if not value:
            return "<not set>"
        if len(value) <= 2:
            return "**"
        return value[0] + "*" * (len(value) - 2) + value[-1]

    print(f"Default Username: {_mask(DEFAULT_USERNAME)}")
    print(f"Default Password: {_mask(DEFAULT_PASSWORD)}")
    print(f"Report Path: {REPORT_PATH}\n")
