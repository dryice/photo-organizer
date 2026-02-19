"""Command-line interface for photo organizer."""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from photo_organizer.scanner import scan_directory
from photo_organizer.extractors.exif import ExifExtractor
from photo_organizer.extractors.filename import FilenameExtractor
from photo_organizer.extractors.fallback import FallbackExtractor
from photo_organizer.date_resolver import DateResolver
from photo_organizer.organizer import Organizer, TransferMode
from photo_organizer.duplicates import DuplicateHandler, DuplicateStrategy
from photo_organizer.utils import setup_logging

logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Organize photo and video files by date and camera model.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --source /path/to/photos --output /organized
  %(prog)s --source /input --output /output --dry-run
  %(prog)s --source /input --output /output --on-duplicate skip
        """,
    )

    parser.add_argument(
        "--source",
        "-s",
        type=Path,
        required=True,
        help="Source directory containing photos and videos",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        required=True,
        help="Output directory for organized files",
    )

    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Preview actions without modifying files",
    )

    parser.add_argument(
        "--mode",
        choices=[mode.value for mode in TransferMode],
        default=TransferMode.COPY.value,
        help="How to transfer files into output: copy (default) or move",
    )

    parser.add_argument(
        "--on-duplicate",
        choices=["skip", "overwrite", "rename"],
        default="rename",
        help="How to handle duplicate filenames (default: rename)",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging verbosity (default: INFO)",
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point."""
    parsed_args = parse_args(args)

    # Setup logging
    setup_logging(parsed_args.log_level)

    # Validate paths
    if not parsed_args.source.exists():
        logger.error(f"Source directory not found: {parsed_args.source}")
        return 1

    if not parsed_args.output.exists():
        logger.info(f"Creating output directory: {parsed_args.output}")
        parsed_args.output.mkdir(parents=True, exist_ok=True)

    # Initialize components
    extractors = [
        ExifExtractor(),
        FilenameExtractor(),
        FallbackExtractor(),
    ]
    resolver = DateResolver(extractors)

    strategy = DuplicateStrategy(parsed_args.on_duplicate)
    duplicate_handler = DuplicateHandler(strategy)

    organizer = Organizer(
        output_root=parsed_args.output,
        dry_run=parsed_args.dry_run,
        mode=TransferMode(parsed_args.mode),
    )

    # Process files
    logger.info(f"Scanning {parsed_args.source}...")
    files = list(scan_directory(parsed_args.source))
    logger.info(f"Found {len(files)} supported files")

    if not files:
        logger.warning("No files to process")
        return 0

    processed = 0
    skipped = 0
    errors = 0

    for i, file_path in enumerate(files, 1):
        logger.debug(f"Processing ({i}/{len(files)}): {file_path}")

        # Extract metadata
        metadata = resolver.resolve(file_path)
        if not metadata:
            logger.warning(f"Could not determine date for: {file_path}")
            errors += 1
            continue

        # Build target path
        target_path = organizer.build_target_path(file_path, metadata)

        # Handle duplicates
        resolved_path = duplicate_handler.resolve(target_path)
        if resolved_path is None:
            logger.info(f"Skipped (duplicate): {file_path.name}")
            skipped += 1
            continue

        # Organize file
        if organizer.organize_file(file_path, resolved_path):
            processed += 1
        else:
            errors += 1

    # Summary
    logger.info("=" * 50)
    logger.info("Processing complete!")
    logger.info(f"  Processed: {processed}")
    logger.info(f"  Skipped:   {skipped}")
    logger.info(f"  Errors:    {errors}")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
