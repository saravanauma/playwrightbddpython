import pytest
from playwright.sync_api import sync_playwright
from tests.utils.config import PLAYWRIGHT_CONFIG, REPORT_PATH
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path


def ensure_playwright_browsers():
    """Ensure required Playwright browsers are installed."""
    try:
        result = subprocess.run(
            ["playwright", "install", "chromium"],
            capture_output=True,
            text=True,
            check=True,
        )
        print("✓ Playwright browsers installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing browsers: {e.stderr}")
        return False
    except FileNotFoundError:
        print("playwright not found in PATH. Installing browsers may require:")
        print("    playwright install")
        return False


# Create directories for storing screenshots and videos
SCREENSHOTS_DIR = Path(REPORT_PATH) / "screenshots"
VIDEOS_DIR = Path(REPORT_PATH) / "videos"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(
                headless=PLAYWRIGHT_CONFIG['headless'],
                slow_mo=PLAYWRIGHT_CONFIG['slow_mo']
            )
            yield browser
            browser.close()
        except Exception as e:
            if "Executable doesn't exist" in str(e):
                if ensure_playwright_browsers():
                    # Retry browser launch after installation
                    browser = p.chromium.launch(
                        headless=PLAYWRIGHT_CONFIG['headless'],
                        slow_mo=PLAYWRIGHT_CONFIG['slow_mo']
                    )
                    yield browser
                    browser.close()
                else:
                    pytest.skip(
                        "Playwright browsers not installed. Run: playwright install")


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

    yield page

    # Take screenshot on test failure
    if request.node.rep_call.failed:
        screenshot_path = SCREENSHOTS_DIR / \
            f"{request.node.name}_{get_timestamp()}_failed.png"
        page.screenshot(path=str(screenshot_path))

    # Close context (this will automatically save the video)
    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

# Add metadata to pytest-html report


def pytest_configure(config):
    if config.pluginmanager.hasplugin("html"):
        config._metadata = getattr(config, "_metadata", {})
        config._metadata["Project Name"] = "Flipkart Automation Framework"
        config._metadata["Framework"] = "Playwright + Pytest + BDD"
        config._metadata["Author"] = "Saravanakumar Veluchamy"
        config._metadata["Environment"] = "QA"

        # Add screenshot and video paths to report
        config._metadata["Screenshots"] = str(SCREENSHOTS_DIR)
        config._metadata["Videos"] = str(VIDEOS_DIR)


def pytest_html_report_title(report):
    report.title = "Flipkart Automation Test Report"

# Helper function to attach screenshots and videos to allure report


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        try:
            # If allure is available, attach screenshots and videos
            import allure
            if report.failed:
                screenshot_path = SCREENSHOTS_DIR / \
                    f"{item.name}_{get_timestamp()}_failed.png"
                if screenshot_path.exists():
                    allure.attach.file(
                        str(screenshot_path),
                        name="Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )

            video_path = VIDEOS_DIR / f"{item.name}_{get_timestamp()}.webm"
            if video_path.exists():
                allure.attach.file(
                    str(video_path),
                    name="Video",
                    attachment_type=allure.attachment_type.WEBM
                )
        except ImportError:
            pass  # Allure not installed, skip attachments
