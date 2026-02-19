import pytest
from pathlib import Path
from photo_organizer.duplicates import DuplicateHandler, DuplicateStrategy


def test_duplicate_strategy_enum():
    assert DuplicateStrategy.SKIP.value == "skip"
    assert DuplicateStrategy.OVERWRITE.value == "overwrite"
    assert DuplicateStrategy.RENAME.value == "rename"


def test_handle_new_file(tmp_path):
    handler = DuplicateHandler(DuplicateStrategy.RENAME)
    new_path = tmp_path / "test.jpg"

    result = handler.resolve(new_path)

    assert result == new_path


def test_handle_existing_skip(tmp_path):
    existing = tmp_path / "test.jpg"
    existing.touch()

    handler = DuplicateHandler(DuplicateStrategy.SKIP)
    result = handler.resolve(existing)

    assert result is None


def test_handle_existing_overwrite(tmp_path):
    existing = tmp_path / "test.jpg"
    existing.touch()

    handler = DuplicateHandler(DuplicateStrategy.OVERWRITE)
    result = handler.resolve(existing)

    assert result == existing


def test_handle_existing_rename(tmp_path):
    existing = tmp_path / "test.jpg"
    existing.touch()

    handler = DuplicateHandler(DuplicateStrategy.RENAME)
    result = handler.resolve(existing)

    assert result.name == "test_1.jpg"
    assert not result.exists()


def test_handle_multiple_renames(tmp_path):
    existing = tmp_path / "test.jpg"
    existing.touch()
    existing_1 = tmp_path / "test_1.jpg"
    existing_1.touch()

    handler = DuplicateHandler(DuplicateStrategy.RENAME)
    result = handler.resolve(existing)

    assert result.name == "test_2.jpg"
