# File: app/logger.py

import logging
from app.config import get_settings

settings = get_settings()

LOG_LEVEL = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

logger = logging.getLogger("hardchews-bot")
