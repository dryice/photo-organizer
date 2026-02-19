"""Integration test for photo organizer."""

import pytest
from datetime import datetime
from pathlib import Path
from PIL import Image
from photo_organizer.cli import main


def test_integration_full_workflow(tmp_path, caplog):
    """Test the complete workflow with real files."""
    # Setup directories
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()

    # Create test images with EXIF
    for i, (date_str, camera) in enumerate(
        [
            ("2024:10:15 14:30:00", "iPhone 14 Pro"),
            ("2024:10:15 15:00:00", "iPhone 14 Pro"),
            ("2024:09:20 10:00:00", "Samsung S21"),
        ]
    ):
        img_path = source / f"photo_{i}.jpg"
        img = Image.new("RGB", (100, 100), color="red")

        # Add EXIF data
        exif = Image.Exif()
        exif[0x9003] = date_str
        make, model = camera.split()[0], " ".join(camera.split()[1:])
        exif[0x010F] = make
        exif[0x0110] = model
        img.save(img_path, exif=exif)

    # Create file without EXIF (should use filename pattern)
    noexif_path = source / "VID_20240810_120000.mp4"
    noexif_path.write_text("fake video")

    # Run organizer
    result = main(
        ["--source", str(source), "--output", str(output), "--log-level", "DEBUG"]
    )

    assert result == 0

    # Verify structure
    assert (output / "2024" / "10" / "15" / "iPhone_14_Pro" / "photo_0.jpg").exists()
    assert (output / "2024" / "10" / "15" / "iPhone_14_Pro" / "photo_1.jpg").exists()
    assert (output / "2024" / "09" / "20" / "Samsung_S21" / "photo_2.jpg").exists()
    assert (
        output / "2024" / "08" / "10" / "Unknown" / "VID_20240810_120000.mp4"
    ).exists()


def test_integration_dry_run(tmp_path, caplog):
    """Test dry-run mode doesn't copy files."""
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()

    # Create test file
    img_path = source / "test.jpg"
    img = Image.new("RGB", (100, 100), color="blue")
    exif = Image.Exif()
    exif[0x9003] = "2024:06:01 12:00:00"
    exif[0x010F] = "Test"
    exif[0x0110] = "Camera"
    img.save(img_path, exif=exif)

    # Run with dry-run
    result = main(["--source", str(source), "--output", str(output), "--dry-run"])

    assert result == 0

    # Verify no files were copied
    assert not list(output.rglob("*.jpg"))
    assert img_path.exists()
