## Why

Today the organizer always copies files into the output tree. For large libraries (especially videos), users often want to *relocate* media into the organized structure to reclaim space and avoid maintaining two copies.

## What Changes

- Add a new CLI option to choose the file transfer behavior: copy (current behavior) or move.
- Default remains copy to preserve existing behavior.
- In move mode, successful organization removes the source file.
- Dry-run continues to preview actions without modifying the filesystem.

## Capabilities

### New Capabilities

- `file-transfer-mode`: Allow selecting whether organizing a file performs a copy or a move.

### Modified Capabilities

- (none)

## Impact

- `photo_organizer/cli.py`: Add and wire a new argument (e.g. `--mode copy|move`) into organizer behavior.
- `photo_organizer/organizer.py`: Implement move behavior alongside existing copy behavior.
- `tests/test_organizer.py`: Add coverage ensuring move mode removes the source file on success.
