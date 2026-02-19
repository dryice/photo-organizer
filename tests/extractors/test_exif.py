import pytest
from datetime import datetime
from pathlib import Path
from PIL import Image
from photo_organizer.extractors.exif import ExifExtractor


def test_exif_extractor_name():
    extractor = ExifExtractor()
    assert extractor.name == "EXIF"


def test_extract_from_image_with_exif(tmp_path):
    img_path = tmp_path / "test.jpg"
    img = Image.new("RGB", (100, 100), color="red")

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
    img_path = tmp_path / "noexif.jpg"
    img = Image.new("RGB", (100, 100), color="blue")
    img.save(img_path)

    extractor = ExifExtractor()
    result = extractor.extract(img_path)

    assert result is None


def test_extract_from_non_image(tmp_path):
    txt_path = tmp_path / "test.txt"
    txt_path.write_text("not an image")

    extractor = ExifExtractor()
    result = extractor.extract(txt_path)

    assert result is None


def test_extract_camera_model_with_make_only(tmp_path):
    img_path = tmp_path / "make_only.jpg"
    img = Image.new("RGB", (100, 100), color="green")

    exif = Image.Exif()
    exif[0x9003] = "2024:10:15 14:30:00"
    exif[0x010F] = "Canon"
    img.save(img_path, exif=exif)

    extractor = ExifExtractor()
    result = extractor.extract(img_path)

    assert result is not None
    assert result.date == datetime(2024, 10, 15, 14, 30, 0)
    assert result.camera_model == "Canon"


def test_extract_camera_model_with_model_only(tmp_path):
    img_path = tmp_path / "model_only.jpg"
    img = Image.new("RGB", (100, 100), color="yellow")

    exif = Image.Exif()
    exif[0x9003] = "2024:10:15 14:30:00"
    exif[0x0110] = "EOS R5"
    img.save(img_path, exif=exif)

    extractor = ExifExtractor()
    result = extractor.extract(img_path)

    assert result is not None
    assert result.date == datetime(2024, 10, 15, 14, 30, 0)
    assert result.camera_model == "EOS R5"


def test_extract_camera_model_make_contains_model(tmp_path):
    img_path = tmp_path / "make_contains_model.jpg"
    img = Image.new("RGB", (100, 100), color="purple")

    exif = Image.Exif()
    exif[0x9003] = "2024:10:15 14:30:00"
    exif[0x010F] = "Sony"
    exif[0x0110] = "Sony A7R IV"
    img.save(img_path, exif=exif)

    extractor = ExifExtractor()
    result = extractor.extract(img_path)

    assert result is not None
    assert result.camera_model == "Sony A7R IV"


def test_extract_camera_model_with_whitespace(tmp_path):
    img_path = tmp_path / "whitespace.jpg"
    img = Image.new("RGB", (100, 100), color="orange")

    exif = Image.Exif()
    exif[0x9003] = "2024:10:15 14:30:00"
    exif[0x010F] = "  Nikon  "
    exif[0x0110] = "  D7000  "
    img.save(img_path, exif=exif)

    extractor = ExifExtractor()
    result = extractor.extract(img_path)

    assert result is not None
    assert result.camera_model == "Nikon D7000"


def test_extract_camera_model_empty_strings(tmp_path):
    img_path = tmp_path / "empty_strings.jpg"
    img = Image.new("RGB", (100, 100), color="pink")

    exif = Image.Exif()
    exif[0x9003] = "2024:10:15 14:30:00"
    exif[0x010F] = ""
    exif[0x0110] = ""
    img.save(img_path, exif=exif)

    extractor = ExifExtractor()
    result = extractor.extract(img_path)

    assert result is not None
    assert result.camera_model is None
