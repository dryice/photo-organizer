import pytest
from datetime import datetime
from pathlib import Path
from photo_organizer.extractors.filename import FilenameExtractor


def test_filename_extractor_name():
    extractor = FilenameExtractor()
    assert extractor.name == "Filename"


def test_extract_android_img_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/IMG_20241015_143000.jpg"))

    assert result is not None
    assert result.date == datetime(2024, 10, 15, 14, 30, 0)


def test_extract_android_vid_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/VID_20241015_143000.mp4"))

    assert result is not None
    assert result.date == datetime(2024, 10, 15, 14, 30, 0)


def test_extract_from_folder_date():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/2024/10/15/random.jpg"))

    assert result is not None
    assert result.date == datetime(2024, 10, 15)


def test_extract_no_date_in_filename():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/IMG_0001.jpg"))

    assert result is None


def test_extract_camera_model_from_folder():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/2024/10/15/iPhone 6 Plus/IMG_0001.jpg"))

    assert result is not None
    assert result.camera_model == "iPhone 6 Plus"


def test_samsung_dcim_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/DCIM_20240101_001.jpg"))

    assert result is not None
    assert result.camera_model == "Samsung"


def test_samsung_mobile_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/SM-G991B_001.jpg"))

    assert result is None


def test_samsung_mobile_pattern_with_date():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/SM-G991B_20240101_001.jpg"))

    assert result is not None
    assert result.camera_model == "Samsung"


def test_sony_dsc_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/DSC_0001.jpg"))

    assert result is None


def test_sony_dsc_pattern_with_date():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/DSC_20240214_001.jpg"))

    assert result is not None
    assert result.camera_model == "Sony"


def test_pixel_pxl_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/PXL_20240218_001.jpg"))

    assert result is not None
    assert result.camera_model == "Pixel"


def test_dji_dji_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/DJI_20240510_001.jpg"))

    assert result is not None
    assert result.camera_model == "DJI"


def test_gopro_gp_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/GP010001.jpg"))

    assert result is None


def test_gopro_gp_pattern_with_date():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/GP_20240601_001.jpg"))

    assert result is not None
    assert result.camera_model == "GoPro"


def test_canon_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/Canon_20240320_001.jpg"))

    assert result is not None
    assert result.camera_model == "Canon"


def test_huawei_honor_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/Honor_20240601_001.jpg"))

    assert result is not None
    assert result.camera_model == "Huawei"


def test_htc_htc_pattern():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/photos/HTC_20240615_001.jpg"))

    assert result is not None
    assert result.camera_model == "HTC"


def test_camera_only_folder():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/Photos/Nikon/IMG_0001.jpg"))

    assert result is not None
    assert result.camera_model == "Nikon"
    assert result.date is None


def test_nested_camera_folder():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/2024/10/15/iPhone 14 Pro/IMG_0001.jpg"))

    assert result is not None
    assert result.camera_model == "iPhone 14 Pro"


def test_deep_nested_folder():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/2024/10/15/iPhone 14 Pro/subfolder/IMG_0001.jpg"))

    assert result is not None
    assert result.date == datetime(2024, 10, 15)
    assert result.camera_model == "iPhone 14 Pro"


def test_folder_with_spaces():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/2024/10/15/iPhone 14 Pro Max/IMG_0001.jpg"))

    assert result is not None
    assert result.camera_model == "iPhone 14 Pro Max"


def test_fallback_to_folder_brand():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/2024/10/15/Sony A7R IV/IMG_0001.jpg"))

    assert result is not None
    assert result.camera_model == "Sony A7R IV"


def test_no_camera_model_detected():
    extractor = FilenameExtractor()
    result = extractor.extract(Path("/2024/10/15/Photos/IMG_0001.jpg"))

    assert result is not None
    assert result.date == datetime(2024, 10, 15)
    assert result.camera_model is None
