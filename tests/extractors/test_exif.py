import pytest
from datetime import datetime
from pathlib import Path
from PIL import Image
from photo_organizer.extractors.exif import ExifExtractor


def test_exif_extractor_name():
    extractor = ExifExtractor()
    assert extractor.name == "EXIF"


def test_extract_from_image_with_exif(tmp_path):
    # Create a test image with EXIF
    img_path = tmp_path / "test.jpg"
    img = Image.new("RGB", (100, 100), color="red")

    # Add EXIF data using Image.Exif
    exif = Image.Exif()
    exif[0x9003] = "2024:10:15 14:30:00"  # DateTimeOriginal
    exif[0x010F] = "Apple"  # Make
    exif[0x0110] = "iPhone 14 Pro"  # Model
    img.save(img_path, exif=exif)

    extractor = ExifExtractor()
    result = extractor.extract(img_path)

    assert result is not None
    assert result.date == datetime(2024, 10, 15, 14, 30, 0)
    assert result.camera_model == "Apple iPhone 14 Pro"


def test_extract_from_image_no_exif(tmp_path):
    # Create image without EXIF
    img_path = tmp_path / "noexif.jpg"
    img = Image.new("RGB", (100, 100), color="blue")
    img.save(img_path)

    extractor = ExifExtractor()
    result = extractor.extract(img_path)

    assert result is None


def test_extract_from_non_image(tmp_path):
    # Create a text file
    txt_path = tmp_path / "test.txt"
    txt_path.write_text("not an image")

    extractor = ExifExtractor()
    result = extractor.extract(txt_path)

    assert result is None
