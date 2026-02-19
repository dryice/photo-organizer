import pytest
import os
import time
from datetime import datetime
from pathlib import Path
from photo_organizer.extractors.fallback import FallbackExtractor


def test_fallback_extractor_name():
    extractor = FallbackExtractor()
    assert extractor.name == "FileSystem"


def test_extract_from_file_ctime(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")

    # Set a specific modification time
    specific_time = datetime(2024, 6, 15, 10, 30, 0)
    os.utime(file_path, (specific_time.timestamp(), specific_time.timestamp()))

    extractor = FallbackExtractor()
    result = extractor.extract(file_path)

    assert result is not None
    assert result.date.date() == specific_time.date()
    assert result.camera_model is None
