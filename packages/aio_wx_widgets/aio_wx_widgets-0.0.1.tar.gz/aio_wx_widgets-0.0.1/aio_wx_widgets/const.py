"""Constants."""

import logging
import os

_LOGGER = logging.getLogger(__name__)


def is_debugging() -> bool:
    """Check if app is in debugging mode."""
    if os.getenv("DEBUGGING") == "1":
        return True
    return False
