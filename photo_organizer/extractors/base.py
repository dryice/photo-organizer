"""Base class for metadata extractors."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class ExtractionResult:
    """Result from metadata extraction."""

    date: Optional[datetime] = None
    camera_model: Optional[str] = None


class MetadataExtractor(ABC):
    """Abstract base class for metadata extractors."""

    @abstractmethod
    def extract(self, file_path: Path) -> Optional[ExtractionResult]:
        """Extract metadata from a file.

        Args:
            file_path: Path to the media file

        Returns:
            ExtractionResult if successful, None otherwise
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return extractor name for logging/debugging."""
        pass
