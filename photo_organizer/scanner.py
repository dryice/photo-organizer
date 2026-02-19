"""File scanning module."""

from pathlib import Path
from typing import Iterator


SUPPORTED_EXTENSIONS = {
    # Photos
    ".jpg",
    ".jpeg",
    ".jpe",
    ".png",
    ".tif",
    ".tiff",
    ".nef",  # Nikon RAW
    ".cr2",  # Canon RAW
    ".arw",  # Sony RAW
    ".dng",  # Adobe Digital Negative
    ".heic",
    ".heif",  # iPhone
    # Videos
    ".mp4",
    ".m4v",
    ".mov",
    ".qt",
    ".avi",
    ".mkv",
    ".webm",
}


def scan_directory(source: Path) -> Iterator[Path]:
    """Recursively scan directory for supported media files.

    Args:
        source: Root directory to scan

    Yields:
        Path objects for each supported file found
    """
    if not source.exists():
        raise FileNotFoundError(f"Source directory not found: {source}")

    for path in source.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path
