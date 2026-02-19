import pytest
from datetime import datetime
from pathlib import Path
from photo_organizer.extractors.filename import FilenameExtractor


def test_filename_extractor_name():
    extractor = FilenameExtractor()
    assert extractor.name == "Filename"


def test_extract_android_img_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/IMG_20241015_143000.jpg"))

    assert result is not None
    assert result.date == datetime(2024, 10, 15, 14, 30, 0)


def test_extract_android_vid_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/VID_20241015_143000.mp4"))

    assert result is not None
    assert result.date == datetime(2024, 10, 15, 14, 30, 0)


def test_extract_from_folder_date():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/2024/10/15/random.jpg"))

    assert result is not None
    assert result.date == datetime(2024, 10, 15)


def test_extract_no_date_in_filename():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/IMG_0001.jpg"))

    assert result is None


def test_extract_camera_model_from_folder():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/2024/10/15/iPhone 6 Plus/IMG_0001.jpg"))

    assert result is not None
    assert result.camera_model == "iPhone 6 Plus"
