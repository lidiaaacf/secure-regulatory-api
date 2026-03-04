import logging
from pythonjsonlogger.jsonlogger import JsonFormatter
import pytest
from app.logging_config import setup_logging
from app.config import settings


@pytest.fixture(autouse=True)
def reset_logging():
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.NOTSET)
    yield
    root_logger.handlers.clear()
    root_logger.setLevel(logging.NOTSET)


def test_setup_logging_uses_default_level_from_settings(monkeypatch):
    monkeypatch.setattr(settings, "LOG_LEVEL", "INFO")
    setup_logging()

    logger = logging.getLogger()
    assert logger.level == logging.INFO
    assert any(isinstance(h.formatter, JsonFormatter) for h in logger.handlers)


def test_setup_logging_uses_custom_level():
    setup_logging(level=logging.DEBUG)

    logger = logging.getLogger()
    assert logger.level == logging.DEBUG
    assert any(isinstance(h.formatter, JsonFormatter) for h in logger.handlers)


def test_setup_logging_applies_jsonformatter(monkeypatch):
    monkeypatch.setattr(settings, "LOG_LEVEL", "WARNING")
    setup_logging()

    logger = logging.getLogger()
    assert any(isinstance(h.formatter, JsonFormatter) for h in logger.handlers)
