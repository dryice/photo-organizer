import pytest
from photo_organizer.utils import sanitize_filename, setup_logging


def test_sanitize_filename_removes_invalid_chars():
    result = sanitize_filename("Camera/Model:Test")
    assert result == "Camera_Model_Test"


def test_sanitize_filename_handles_whitespace():
    result = sanitize_filename("  iPhone 6 Plus  ")
    assert result == "iPhone_6_Plus"


def test_sanitize_filename_empty():
    result = sanitize_filename("")
    assert result == "Unknown"
