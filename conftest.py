import pytest
from playwright.sync_api import sync_playwright
from tests.utils.config import PLAYWRIGHT_CONFIG, REPORT_PATH
from tests.utils.logger import logger, init_logging  # new
from tests.utils.screenshot import take_screenshot as _take_screenshot
from tests.db.fixtures import db_connection, db_cursor
from tests.utils.logger import logger
from datetime import datetime
from pathlib import Path

init_logging()
logger.debug("conftest loaded; REPORT_PATH=%s", REPORT_PATH)


# Create directories for storing screenshots and videos
SCREENSHOTS_DIR = Path(REPORT_PATH) / "screenshots"
VIDEOS_DIR = Path(REPORT_PATH) / "videos"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


"""
Database test configuration and fixtures.
Import and expose fixtures from fixtures.py to make them available to all tests.
"""

# Import and expose the fixtures (this makes them available to pytest)
__all__ = ['db_connection', 'db_cursor']

# Log DB test configuration on import
logger.info("Database test configuration loaded")


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=PLAYWRIGHT_CONFIG['headless'],
            slow_mo=PLAYWRIGHT_CONFIG['slow_mo'])
        yield browser
        browser.close()


@pytest.fixture
def page(browser, request):
    # Create browser context with video recording
    video_path = VIDEOS_DIR / f"{request.node.name}_{get_timestamp()}.webm"
    context = browser.new_context(
        record_video_dir=str(VIDEOS_DIR),
        record_video_size={"width": 1280, "height": 720}
    )

    # Create new page
    page = context.new_page()
    # Store page and context on request.node for access in hooks
    request.node._pw_page = page
    request.node._pw_context = context

    yield page

    # Close context (this will automatically save the video)
    context.close()


@pytest.fixture
def take_screenshot(request):
    """Fixture that provides the `take_screenshot(page, name=None, full_page=False)` helper.

    Usage in tests/steps/pages:
        def test_example(page, take_screenshot):
            take_screenshot(page, name="my_step")
    """
    return _take_screenshot


def pytest_html_report_title(report):
    report.title = "Test Automation Test Report"

# Unified pytest_runtest_makereport: attach screenshot and video to Allure for each test


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    # Only attach artifacts after test call phase
    if report.when == "call":
        # Attach screenshot to Allure (if available and page exists)
        page = getattr(item, "_pw_page", None)
        try:
            import allure
            if page is not None:
                result = "failed" if report.failed else "passed"
                # Take screenshot and attach to Allure
                from tests.utils.screenshot import take_screenshot as _take_screenshot
                screenshot_path = _take_screenshot(
                    page, name=f"{item.name}_{result}", attach=False)
                allure.attach.file(
                    str(screenshot_path),
                    name=f"Screenshot ({result})",
                    attachment_type=allure.attachment_type.PNG
                )
            # Attach video if available
            context = getattr(item, "_pw_context", None)
            if context is not None:
                # Playwright saves video to record_video_dir, but need to get the path from the page
                try:
                    video = None
                    if page is not None and hasattr(page, "video") and page.video:
                        video = page.video.path()
                    if video and Path(video).exists():
                        allure.attach.file(
                            str(video),
                            name="Video",
                            attachment_type=allure.attachment_type.WEBM
                        )
                except Exception:
                    pass
        except ImportError:
            pass  # Allure not installed, skip attachments
