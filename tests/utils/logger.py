import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from tests.utils.config import REPORT_PATH, print_current_config

# Ensure log directory exists (uses REPORT_PATH from tests.utils.config)
LOG_DIR = Path(REPORT_PATH) / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

logger = logging.getLogger("playwrightbdd")
logger.setLevel(logging.DEBUG)

# Formatter
fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(fmt)
logger.addHandler(ch)

# Rotating file handler (5 MB, 3 backups)
fh = RotatingFileHandler(str(LOG_FILE), maxBytes=5 *
                         1024 * 1024, backupCount=3, encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(fmt)
logger.addHandler(fh)


def init_logging():
    """
    Ensure logger is initialized and write a startup entry.
    Call this from test bootstrap (e.g. conftest.py).
    """
    logger.info("Logger initialized. Log file: %s", LOG_FILE)
    try:
        # print_current_config masks secrets and prints config to stdout/log
        print_current_config()
    except Exception:
        logger.debug(
            "print_current_config failed or not available", exc_info=True)
