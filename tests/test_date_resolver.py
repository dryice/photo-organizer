import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock
from photo_organizer.date_resolver import DateResolver
from photo_organizer.extractors.base import ExtractionResult


def test_resolver_priority_chain():
    """Test that resolver tries extractors in priority order."""
    # Create mock extractors
    exif_extractor = Mock()
    filename_extractor = Mock()
    fallback_extractor = Mock()

    # EXIF succeeds
    exif_extractor.extract.return_value = ExtractionResult(
        date=datetime(2024, 10, 15), camera_model="iPhone"
    )
    exif_extractor.name = "EXIF"

    resolver = DateResolver([exif_extractor, filename_extractor, fallback_extractor])
    result = resolver.resolve(Path("/test.jpg"))

    assert result.date == datetime(2024, 10, 15)
    assert result.camera_model == "iPhone"
    exif_extractor.extract.assert_called_once()
    filename_extractor.extract.assert_not_called()


def test_resolver_fallback_chain():
    """Test that resolver falls back when extractors fail."""
    exif_extractor = Mock()
    filename_extractor = Mock()
    fallback_extractor = Mock()

    # EXIF fails, filename succeeds
    exif_extractor.extract.return_value = None
    exif_extractor.name = "EXIF"

    filename_extractor.extract.return_value = ExtractionResult(
        date=datetime(2024, 5, 20), camera_model="Android"
    )
    filename_extractor.name = "Filename"

    resolver = DateResolver([exif_extractor, filename_extractor, fallback_extractor])
    result = resolver.resolve(Path("/test.jpg"))

    assert result.date == datetime(2024, 5, 20)
    assert result.camera_model == "Android"
    exif_extractor.extract.assert_called_once()
    filename_extractor.extract.assert_called_once()


def test_resolver_all_fail():
    """Test behavior when all extractors fail."""
    exif_extractor = Mock()
    exif_extractor.extract.return_value = None
    exif_extractor.name = "EXIF"

    filename_extractor = Mock()
    filename_extractor.extract.return_value = None
    filename_extractor.name = "Filename"

    fallback_extractor = Mock()
    fallback_extractor.extract.return_value = None
    fallback_extractor.name = "Fallback"

    resolver = DateResolver([exif_extractor, filename_extractor, fallback_extractor])
    result = resolver.resolve(Path("/test.jpg"))

    assert result is None
