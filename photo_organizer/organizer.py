"""File organization logic."""

import logging
import shutil
from pathlib import Path
from typing import Optional

from photo_organizer.extractors.base import ExtractionResult
from photo_organizer.utils import sanitize_filename

logger = logging.getLogger(__name__)


class Organizer:
    """Organize files into structured output directory."""

    def __init__(self, output_root: Path, dry_run: bool = False):
        """Initialize organizer.

        Args:
            output_root: Root directory for organized files
            dry_run: If True, only log actions without executing
        """
        self.output_root = output_root
        self.dry_run = dry_run

    def build_target_path(self, source_path: Path, metadata: ExtractionResult) -> Path:
        """Build target path based on metadata.

        Structure: output/YYYY/MM/DD/camera_model/filename
        """
        date = metadata.date
        camera_model = metadata.camera_model or "Unknown"

        # Sanitize camera model for filesystem
        safe_camera = sanitize_filename(camera_model)

        # Build path components
        year = f"{date.year:04d}"
        month = f"{date.month:02d}"
        day = f"{date.day:02d}"

        target_dir = self.output_root / year / month / day / safe_camera
        target_path = target_dir / source_path.name

        return target_path

    def organize_file(self, source_path: Path, target_path: Path) -> bool:
        """Copy file from source to target.

        Args:
            source_path: Source file path
            target_path: Target file path

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.dry_run:
                logger.info(f"[DRY RUN] Would copy: {source_path} -> {target_path}")
                return True

            # Create target directory if needed
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy the file
            shutil.copy2(source_path, target_path)
            logger.info(f"Copied: {source_path.name} -> {target_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to copy {source_path}: {e}")
            return False
