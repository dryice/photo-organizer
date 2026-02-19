import pytest
from pathlib import Path
from photo_organizer.scanner import scan_directory, SUPPORTED_EXTENSIONS


def test_scan_directory_finds_photos(tmp_path):
    # Create test files
    (tmp_path / "photo1.jpg").touch()
    (tmp_path / "photo2.jpeg").touch()
    (tmp_path / "video.mp4").touch()
    (tmp_path / "readme.txt").touch()  # Should be ignored

    result = list(scan_directory(tmp_path))

    assert len(result) == 3
    assert all(isinstance(p, Path) for p in result)


def test_scan_directory_recursive(tmp_path):
    # Create nested structure
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (tmp_path / "root.jpg").touch()
    (subdir / "nested.jpg").touch()

    result = list(scan_directory(tmp_path))

    assert len(result) == 2


def test_supported_extensions():
    assert ".jpg" in SUPPORTED_EXTENSIONS
    assert ".mp4" in SUPPORTED_EXTENSIONS
    assert ".txt" not in SUPPORTED_EXTENSIONS
