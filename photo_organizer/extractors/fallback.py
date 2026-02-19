"""Fallback extractor using file system dates."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from photo_organizer.extractors.base import ExtractionResult, MetadataExtractor

logger = logging.getLogger(__name__)


class FallbackExtractor(MetadataExtractor):
    """Extract date from file system modification time."""

    @property
    def name(self) -> str:
        return "FileSystem"

    def extract(self, file_path: Path) -> Optional[ExtractionResult]:
        """Extract date from file modification time.

        This is the fallback method when no metadata is available.
        Uses the most recent of ctime (change time) and mtime (modification time).
        """
        try:
            stat = file_path.stat()
            # Use the earlier of ctime and mtime (more likely to be the original)
            timestamp = min(stat.st_ctime, stat.st_mtime)
            date = datetime.fromtimestamp(timestamp)

            return ExtractionResult(date=date, camera_model=None)

        except Exception as e:
            logger.debug(f"Fallback extraction failed for {file_path}: {e}")
            return None
