"""Utility functions for photo organizer."""

import re
import logging
import sys
from pathlib import Path


def sanitize_filename(name: str) -> str:
    """Sanitize a string for use as a filename.

    Replaces invalid characters with underscores and strips whitespace.
    """
    if not name or not name.strip():
        return "Unknown"

    # Replace invalid filename characters with underscore
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", name.strip())
    # Replace multiple spaces/underscores with single underscore
    sanitized = re.sub(r"[\s_]+", "_", sanitized)
    return sanitized


def setup_logging(level: str = "INFO") -> None:
    """Configure logging for the application."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
