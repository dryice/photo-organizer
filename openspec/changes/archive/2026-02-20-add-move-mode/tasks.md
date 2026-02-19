## 1. CLI surface

- [x] 1.1 Add `--mode` argument with choices `copy|move` (default: `copy`) to `photo_organizer/cli.py`
- [x] 1.2 Parse `--mode` into a typed value and pass it into `Organizer`

## 2. Core implementation

- [x] 2.1 Add an enum-like type for transfer mode (similar to `DuplicateStrategy`)
- [x] 2.2 Update `Organizer` to perform `copy2` in copy mode and `move` in move mode
- [x] 2.3 Ensure `--dry-run` remains non-destructive for both modes (log-only)

## 3. Tests

- [x] 3.1 Add organizer test for move mode: destination exists and source no longer exists after success
- [x] 3.2 Add CLI parsing test covering `--mode` default and explicit values

## 4. Verify

- [x] 4.1 Run unit tests (`uv run pytest tests/ -v`)
- [x] 4.2 Run integration tests (`uv run pytest tests/test_integration.py -v`)
