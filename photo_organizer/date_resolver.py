"""Date resolution with priority chain of extractors."""

import logging
from pathlib import Path
from typing import Optional, List

from photo_organizer.extractors.base import ExtractionResult, MetadataExtractor

logger = logging.getLogger(__name__)


class DateResolver:
    """Resolves file date using a priority chain of extractors."""

    def __init__(self, extractors: List[MetadataExtractor]):
        """Initialize with ordered list of extractors.

        Extractors are tried in order until one succeeds.
        """
        self.extractors = extractors

    def resolve(self, file_path: Path) -> Optional[ExtractionResult]:
        """Resolve date and camera model for a file.

        Tries each extractor in priority order:
        1. EXIF metadata (most reliable)
        2. Filename patterns
        3. File system dates (fallback)

        Args:
            file_path: Path to the media file

        Returns:
            ExtractionResult with date and optional camera_model, or None
        """
        for extractor in self.extractors:
            try:
                result = extractor.extract(file_path)
                if result:
                    logger.debug(
                        f"{extractor.name} succeeded for {file_path.name}: "
                        f"{result.date}, camera={result.camera_model}"
                    )
                    return result
            except Exception as e:
                logger.debug(f"{extractor.name} failed for {file_path}: {e}")
                continue

        logger.warning(f"Could not extract date for {file_path}")
        return None
