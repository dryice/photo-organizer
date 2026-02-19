import pytest
from datetime import datetime
from pathlib import Path
from photo_organizer.extractors.base import ExtractionResult, MetadataExtractor


def test_extraction_result_creation():
    result = ExtractionResult(
        date=datetime(2024, 10, 15, 14, 30, 0), camera_model="iPhone 14 Pro"
    )
    assert result.date.year == 2024
    assert result.camera_model == "iPhone 14 Pro"


def test_extraction_result_optional_camera():
    result = ExtractionResult(date=datetime.now())
    assert result.camera_model is None


def test_extractor_is_abstract():
    with pytest.raises(TypeError):
        MetadataExtractor()
