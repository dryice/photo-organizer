# Photo & Video Organizer

A Python CLI tool to organize photo and video files from a source directory into a structured output directory based on date and camera model information.

## Features

- 📁 **Recursive Scanning** - Scans source directories recursively for media files
- 📅 **Smart Date Extraction** - Uses multiple methods in priority order:
  1. EXIF metadata (DateTimeOriginal)
  2. Filename patterns (e.g., `IMG_20241015_143000.jpg`)
  3. Folder structure (e.g., `/2024/10/15/`)
  4. File system dates (fallback)
- 📷 **Camera Model Detection** - Extracts camera info from EXIF or folder names
- 🔄 **Duplicate Handling** - Skip, overwrite, or auto-rename duplicates
- 🧪 **Dry Run Mode** - Preview operations without modifying files
- 📊 **Progress Logging** - See what's happening with configurable verbosity

## Supported Formats

**Photos:** JPG, JPEG, PNG, TIFF, NEF (Nikon RAW), CR2 (Canon RAW), ARW (Sony RAW), DNG, HEIC/HEIF

**Videos:** MP4, M4V, MOV, AVI, MKV, WebM

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for fast, reliable Python package management.

```bash
# Clone or navigate to the repository
cd photo-organizer

# Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"

# Or run without activating (uv run handles the venv automatically)
uv run photo-organizer --help
```

**Requirements:**
- Python 3.8+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

## Usage

### Basic Usage

```bash
# Using uv run (recommended - no venv activation needed)
uv run python -m photo_organizer --source /path/to/photos --output /path/to/organized

# Or if you activated the virtual environment
python -m photo_organizer --source /path/to/photos --output /path/to/organized
```

### Dry Run (Preview Only)

```bash
uv run python -m photo_organizer --source /path/to/photos --output /path/to/organized --dry-run
```

### Handle Duplicates

```bash
# Skip duplicates
uv run python -m photo_organizer --source /path/to/photos --output /path/to/organized --on-duplicate skip

# Overwrite duplicates
uv run python -m photo_organizer --source /path/to/photos --output /path/to/organized --on-duplicate overwrite

# Rename duplicates (default)
uv run python -m photo_organizer --source /path/to/photos --output /path/to/organized --on-duplicate rename
```

### Debug Logging

```bash
uv run python -m photo_organizer --source /path/to/photos --output /path/to/organized --log-level DEBUG
```

## Output Structure

Files are organized into the following structure:

```
output/
├── 2024/
│   ├── 10/
│   │   ├── 15/
│   │   │   ├── iPhone_14_Pro/
│   │   │   │   ├── IMG_0001.jpg
│   │   │   │   ├── IMG_0002.jpg
│   │   │   │   └── ...
│   │   │   └── Nikon_D7000/
│   │   │       ├── DSC_0001.nef
│   │   │       └── ...
│   │   └── 16/
│   │       └── ...
│   └── 09/
│       └── ...
└── 2023/
    └── ...
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_scanner.py -v

# Run with coverage
uv run pytest tests/ --cov=photo_organizer --cov-report=html
```

### Project Structure

```
photo_organizer/
├── __init__.py              # Package initialization
├── __main__.py              # Entry point
├── cli.py                   # Command-line interface
├── scanner.py               # File discovery
├── date_resolver.py         # Date extraction priority chain
├── organizer.py             # File organization logic
├── duplicates.py            # Duplicate handling
├── utils.py                 # Utility functions
└── extractors/              # Metadata extractors
    ├── base.py              # Abstract base class
    ├── exif.py              # EXIF metadata extraction
    ├── filename.py          # Filename pattern extraction
    └── fallback.py          # File system date fallback

tests/                       # Test suite
├── extractors/              # Extractor tests
├── test_cli.py
├── test_scanner.py
├── test_date_resolver.py
├── test_duplicates.py
├── test_organizer.py
├── test_utils.py
└── test_integration.py      # Integration tests
```

## Dependency Management

This project uses `uv` which handles dependencies automatically:

- **Runtime dependencies** (Pillow) are defined in `pyproject.toml` under `[project.dependencies]`
- **Development dependencies** (pytest) are in `[project.optional-dependencies.dev]`
- **Transitive dependencies** (pluggy, pygments, etc.) are resolved automatically by uv
- To update dependencies: `uv pip install -e ".[dev]" --upgrade`

## Examples

### Organize iPhone Photos

```bash
uv run python -m photo_organizer \
  --source ~/Pictures/iPhone \
  --output ~/Pictures/Organized \
  --dry-run
```

### Process RAW Files

```bash
uv run python -m photo_organizer \
  --source ~/Pictures/RAW \
  --output ~/Pictures/Organized \
  --on-duplicate skip \
  --log-level INFO
```

## License

MIT License
