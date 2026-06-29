import sys
from pathlib import Path

from loguru import logger

from config.settings import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Remove Loguru's default console logger
logger.remove()

# Console logger
logger.add(
    sys.stdout,
    level=settings.log_level,
    colorize=True,
)

# File logger
logger.add(
    LOG_DIR / "app.log",
    level=settings.log_level,
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    enqueue=True,
)

logger.info("Logger initialized.")
