import pytest
from src.utils.logger import logger


def test_logger_exists():
    """Test that logger is properly configured."""
    assert logger is not None
    assert logger.name == "intelligent_data_viz"


def test_logger_has_handlers():
    """Test that logger has console and file handlers."""
    assert len(logger.handlers) >= 2
    handler_types = [type(h).__name__ for h in logger.handlers]
    assert "StreamHandler" in handler_types
    assert "FileHandler" in handler_types


def test_logger_can_log(caplog):
    """Test that logger can write log messages."""
    import logging

    with caplog.at_level(logging.INFO):
        logger.info("Test message")
        assert "Test message" in caplog.text

    with caplog.at_level(logging.ERROR):
        logger.error("Test error")
        assert "Test error" in caplog.text
