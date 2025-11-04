import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from tests.utils.config import REPORT_PATH
from tests.utils.logger import logger

try:
    import allure
    _HAS_ALLURE = True
except Exception:
    _HAS_ALLURE = False


SCREENSHOTS_DIR = Path(REPORT_PATH) / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def _timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def take_screenshot(page, name: Optional[str] = None, full_page: bool = False, attach: bool = True) -> str:
    """
    Take a screenshot using a Playwright `page` object.

    - Saves screenshot under `REPORT_PATH/screenshots`.
    - Returns the absolute path to the saved file.
    - Attaches to Allure if available and attach=True.

    Args:
        page: Playwright page instance
        name: Optional file-name prefix (without extension). If None, uses "screenshot".
        full_page: Whether to capture full page
        attach: If True and Allure is available, attach file to report

    Returns:
        str: path to the saved screenshot file
    """
    prefix = name or "screenshot"
    filename = f"{prefix}_{_timestamp()}.png"
    path = SCREENSHOTS_DIR / filename

    try:
        page.screenshot(path=str(path), full_page=full_page)
        logger.info("Saved screenshot: %s", path)

        if attach and _HAS_ALLURE:
            try:
                allure.attach.file(str(path), name=filename,
                                   attachment_type=allure.attachment_type.PNG)
            except Exception:
                logger.debug(
                    "Failed to attach screenshot to Allure", exc_info=True)

    except Exception as e:
        logger.exception("Failed to take screenshot: %s", e)

    return str(path)
