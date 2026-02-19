"""Duplicate file handling strategies."""

import logging
from enum import Enum
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class DuplicateStrategy(Enum):
    """Strategy for handling duplicate filenames."""

    SKIP = "skip"
    OVERWRITE = "overwrite"
    RENAME = "rename"


class DuplicateHandler:
    """Handle duplicate filename conflicts."""

    def __init__(self, strategy: DuplicateStrategy):
        self.strategy = strategy

    def resolve(self, target_path: Path) -> Optional[Path]:
        """Resolve duplicate filename conflict.

        Args:
            target_path: Desired target path

        Returns:
            Resolved path (may be modified), or None if skipping
        """
        if not target_path.exists():
            return target_path

        if self.strategy == DuplicateStrategy.SKIP:
            logger.warning(f"Skipping duplicate: {target_path}")
            return None

        if self.strategy == DuplicateStrategy.OVERWRITE:
            logger.warning(f"Overwriting: {target_path}")
            return target_path

        if self.strategy == DuplicateStrategy.RENAME:
            return self._generate_unique_path(target_path)

        return target_path

    def _generate_unique_path(self, target_path: Path) -> Path:
        """Generate a unique path by appending _N before extension."""
        stem = target_path.stem
        suffix = target_path.suffix
        parent = target_path.parent

        counter = 1
        while True:
            new_name = f"{stem}_{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                logger.info(f"Renaming duplicate to: {new_path.name}")
                return new_path
            counter += 1
