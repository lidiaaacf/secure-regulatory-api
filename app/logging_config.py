import logging
from pythonjsonlogger import jsonlogger
from app.config import settings


def setup_logging(level: str | int = None):
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    if level is None:
        level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    log_handler.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[log_handler])
