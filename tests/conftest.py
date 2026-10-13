import multiprocessing.util

import pytest


@pytest.fixture(autouse=True)
def restore_legacy_logging():
    """Keep the preserved constructor's stderr handlers inside each test."""
    logger = multiprocessing.util.get_logger()
    original_handlers = tuple(logger.handlers)
    original_level = logger.level
    yield
    for handler in tuple(logger.handlers):
        if handler not in original_handlers:
            logger.removeHandler(handler)
            handler.close()
    logger.setLevel(original_level)
