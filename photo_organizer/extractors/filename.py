"""Filename pattern extractor."""

import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from photo_organizer.extractors.base import ExtractionResult, MetadataExtractor

logger = logging.getLogger(__name__)


class FilenameExtractor(MetadataExtractor):
    """Extract date from filename patterns and folder structure."""

    @property
    def name(self) -> str:
        return "Filename"

    def extract(self, file_path: Path) -> Optional[ExtractionResult]:
        """Extract date from filename or folder structure."""
        date = None
        camera_model = None

        # Try filename patterns first
        date = self._extract_from_filename(file_path.name)

        # If no date in filename, try folder structure
        if not date:
            date, camera_model = self._extract_from_folder(file_path.parent)
        else:
            # Still try to get camera model from folder
            _, camera_model = self._extract_from_folder(file_path.parent)

        if date:
            return ExtractionResult(date=date, camera_model=camera_model)

        return None

    def _extract_from_filename(self, filename: str) -> Optional[datetime]:
        """Extract date from common filename patterns."""
        # Pattern: IMG_YYYYMMDD_HHMMSS or VID_YYYYMMDD_HHMMSS
        pattern = r"(?:IMG|VID)_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})"
        match = re.search(pattern, filename)

        if match:
            year, month, day, hour, minute, second = match.groups()
            try:
                return datetime(
                    int(year), int(month), int(day), int(hour), int(minute), int(second)
                )
            except ValueError:
                pass

        # Pattern: YYYYMMDD anywhere in filename
        pattern = r"(\d{4})(\d{2})(\d{2})"
        match = re.search(pattern, filename)

        if match:
            year, month, day = match.groups()
            try:
                return datetime(int(year), int(month), int(day))
            except ValueError:
                pass

        return None

    def _extract_from_folder(
        self, folder: Path
    ) -> tuple[Optional[datetime], Optional[str]]:
        """Extract date and camera model from folder path.

        Looks for patterns like:
        - /YYYY/MM/DD/
        - /YYYY/MM/DD/camera_name/
        """
        date = None
        camera_model = None

        parts = list(folder.parts)

        # Look for YYYY/MM/DD pattern in the path
        for i in range(len(parts) - 2):
            try:
                year = int(parts[i])
                month = int(parts[i + 1])
                day = int(parts[i + 2])

                if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                    date = datetime(year, month, day)
                    # Camera model might be the next folder
                    if i + 3 < len(parts):
                        camera_model = parts[i + 3]
                    break
            except ValueError:
                continue

        return date, camera_model
