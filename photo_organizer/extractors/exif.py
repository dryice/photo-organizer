"""EXIF metadata extractor using Pillow."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from PIL import Image
from PIL.ExifTags import TAGS

from photo_organizer.extractors.base import ExtractionResult, MetadataExtractor

logger = logging.getLogger(__name__)


class ExifExtractor(MetadataExtractor):
    """Extract date and camera info from EXIF metadata."""

    @property
    def name(self) -> str:
        return "EXIF"

    def extract(self, file_path: Path) -> Optional[ExtractionResult]:
        """Extract metadata from image EXIF data."""
        try:
            with Image.open(file_path) as img:
                exif = img._getexif()
                if not exif:
                    return None

                # Extract date
                date = self._extract_date(exif)
                if not date:
                    return None

                # Extract camera model
                camera_model = self._extract_camera_model(exif)

                return ExtractionResult(date=date, camera_model=camera_model)

        except Exception as e:
            logger.debug(f"EXIF extraction failed for {file_path}: {e}")
            return None

    def _extract_date(self, exif: dict) -> Optional[datetime]:
        """Extract date from EXIF tags."""
        # Priority: DateTimeOriginal > DateTimeDigitized > DateTime
        date_tags = [
            0x9003,
            0x9004,
            0x0132,
        ]  # DateTimeOriginal, DateTimeDigitized, DateTime

        for tag in date_tags:
            if tag in exif:
                try:
                    date_str = exif[tag]
                    # EXIF date format: "YYYY:MM:DD HH:MM:SS"
                    return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                except (ValueError, TypeError):
                    continue

        return None

    def _extract_camera_model(self, exif: dict) -> Optional[str]:
        """Extract camera make and model from EXIF."""
        make = exif.get(0x010F, "")  # Make
        model = exif.get(0x0110, "")  # Model

        # Clean up the values
        make = make.strip() if make else ""
        model = model.strip() if model else ""

        # If model already contains make, just use model
        if make and model:
            if model.startswith(make):
                return model
            return f"{make} {model}".strip()

        return model or make or None
