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

    # Device-specific camera patterns for common manufacturers
    DEVICE_PATTERNS = {
        # Samsung
        "samsung_dcim": r"DCIM_\d+",
        "samsung_samsung_old": r"SAMSUNG_\d+",
        "samsung_mobile": r"SM-\w+|SCH-\w+",  # SM/ SCH cameras (e.g., SM-G991B, SCH-I535)
        # Sony
        "sony_dsc": r"DSC_\d{4}",
        "sony_ilce": r"ILCE-\d+\w*",  # ILCE sensors (e.g., ILCE-7RM4, ILCE-6600, ILCE-7M3)
        # Google Pixel
        "pixel_pxl": r"PXL_\d{4}",  # Google Pixel phones
        # DJI
        "dji_dji": r"DJI_\d{4}",  # Drones
        # GoPro
        "gopro_gp": r"GP\d{6}|GP_\d+",  # HERO/5/6/7/8/10/12 cameras
        # Canon video prefix (PowerShot/EOS)
        "canon_mvi": r"MVI_\d{4}",
        # Canon
        "canon_canon": r"Canon_\d{4}",
        "canon_older": r"\bCanon(?:_.*|$)",
        # Huawei
        "huawei_honor": r"Honor_\d{4}",  # Honor series
        # HTC
        "htc_htc": r"HTC_\d{4}",
        # Additional device-specific patterns that include camera model
        "model_in_folder": r"(?:iPhone|Pixel|Galaxy|Nexus|Redmi|Poco|Moto|OnePlus|ROG|Zenfone|Mi A|Mi Mix|Redmi Note|Find X|CPH|GMK|Pixel Fold|Surface|Tecno|Honor|View|Vivo|Oppo|Realme|Nubia|Nokia|Lumia|Motorola|Asus|Blackview|Lenovo|Alcatel|AGM|Infinix|TCL|ZTE|Cat|BQ|Ulefone|Fairphone|Nothing|Palm|Orange|Sharp|T-Mobile|Vertu|Xperia|Xperia pro|Sony Ericsson)",
    }

    # Brand name mappings for proper capitalization
    BRAND_NAME_MAP = {
        "dji": "DJI",
        "htc": "HTC",
        "gopro": "GoPro",
    }

    # Camera brands for folder-based detection
    CAMERA_BRANDS = [
        "iphone",
        "ipad",
        "ipod",
        "pixel",
        "galaxy",
        "nexus",
        "redmi",
        "poco",
        "moto",
        "oneplus",
        "rog",
        "zenfone",
        "nikon",
        "canon",
        "sony",
        "panasonic",
        "lumix",
        "fujifilm",
        "olympus",
        "pentax",
        "leica",
        "hasselblad",
        "dji",
        "gopro",
        "huawei",
        "honor",
        "htc",
        "xiaomi",
        "oppo",
        "vivo",
        "realme",
        "nokia",
        "motorola",
        "asus",
        "lenovo",
        "lg",
        "samsung",
    ]

    @property
    def name(self) -> str:
        return "Filename"

    def extract(self, file_path: Path) -> Optional[ExtractionResult]:
        """Extract date from filename or folder structure."""
        date = None
        camera_model = None

        date = self._extract_from_filename(file_path.name)

        if not date:
            date, camera_model = self._extract_from_folder(file_path.parent)
        else:
            camera_model = self._detect_camera_model_from_name(file_path.name)
            _, folder_camera = self._extract_from_folder(file_path.parent)

            if folder_camera:
                camera_model = folder_camera

        if date or camera_model:
            return ExtractionResult(date=date, camera_model=camera_model)

        return None

    def _detect_camera_model_from_name(self, name: str) -> Optional[str]:
        """Detect camera model from device-specific patterns."""
        name_lower = name.lower()

        for pattern_name, pattern in self.DEVICE_PATTERNS.items():
            if re.search(pattern.lower(), name_lower):
                parts = pattern_name.split("_")
                if len(parts) >= 2:
                    brand = parts[0].lower()
                    return self.BRAND_NAME_MAP.get(brand, brand.capitalize())
                brand = pattern_name.split("_")[0].lower()
                return self.BRAND_NAME_MAP.get(brand, brand.capitalize())

        return None

    def _extract_from_filename(self, filename: str) -> Optional[datetime]:
        """Extract date from common filename patterns."""
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
        - /Photos/Nikon/ (camera-only folder)
        - /YYYY/MM/DD/camera1/camera2/ (nested camera folders)
        """
        date = None
        camera_model = None
        generic_folders = {
            "photos",
            "videos",
            "camera",
            "pictures",
            "images",
            "media",
            "dcim",
        }

        parts = list(folder.parts)

        for i in range(len(parts) - 2):
            try:
                year = int(parts[i])
                month = int(parts[i + 1])
                day = int(parts[i + 2])

                if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                    date = datetime(year, month, day)
                    if i + 3 < len(parts):
                        potential_camera = parts[i + 3]
                        if potential_camera.lower() not in generic_folders:
                            camera_model = potential_camera
                    break
            except ValueError:
                continue

        if not camera_model:
            for i in range(len(parts) - 1, -1, -1):
                folder_name = parts[i]

                if folder_name.lower() in generic_folders:
                    continue

                detected_camera = self._detect_camera_model_from_name(folder_name)
                if detected_camera:
                    camera_model = detected_camera
                    break

                folder_name_lower = folder_name.lower()
                for brand in self.CAMERA_BRANDS:
                    pattern = r"\b" + re.escape(brand) + r"\b"
                    if re.search(pattern, folder_name_lower):
                        camera_model = folder_name
                        break

                if camera_model:
                    break

        return date, camera_model
