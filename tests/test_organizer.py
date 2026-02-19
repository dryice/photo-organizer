import pytest
from datetime import datetime
from pathlib import Path
from photo_organizer.organizer import Organizer, TransferMode
from photo_organizer.extractors.base import ExtractionResult


def test_build_target_path():
    organizer = Organizer(Path("/output"))
    result = ExtractionResult(
        date=datetime(2024, 10, 15, 14, 30, 0), camera_model="iPhone 14 Pro"
    )

    target = organizer.build_target_path(Path("/source/photo.jpg"), result)

    expected = Path("/output/2024/10/15/iPhone_14_Pro/photo.jpg")
    assert target == expected


def test_build_target_path_no_camera():
    organizer = Organizer(Path("/output"))
    result = ExtractionResult(date=datetime(2024, 10, 15), camera_model=None)

    target = organizer.build_target_path(Path("/source/photo.jpg"), result)

    expected = Path("/output/2024/10/15/Unknown/photo.jpg")
    assert target == expected


def test_organize_file_copies(tmp_path):
    # Setup
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()

    photo = source / "test.jpg"
    photo.write_text("photo content")

    organizer = Organizer(output)
    result = ExtractionResult(date=datetime(2024, 10, 15), camera_model="TestCamera")

    # Execute
    target = organizer.build_target_path(photo, result)
    organizer.organize_file(photo, target)

    # Verify
    assert target.exists()
    assert target.read_text() == "photo content"
    assert photo.exists()  # Source should remain


def test_organize_file_moves(tmp_path):
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()

    photo = source / "test.jpg"
    photo.write_text("photo content")

    organizer = Organizer(output, mode=TransferMode.MOVE)
    result = ExtractionResult(date=datetime(2024, 10, 15), camera_model="TestCamera")

    target = organizer.build_target_path(photo, result)
    assert organizer.organize_file(photo, target)

    assert target.exists()
    assert target.read_text() == "photo content"
    assert not photo.exists()
