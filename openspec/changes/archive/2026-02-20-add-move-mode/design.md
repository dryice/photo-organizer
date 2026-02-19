## Context

The CLI currently always organizes files by copying (`shutil.copy2`) from the source tree into the output tree. This preserves file metadata and is non-destructive to the source.

We want an explicit “move” option so users can relocate files into the organized output structure (especially helpful for large video libraries) while keeping the default behavior unchanged.

Key existing components:

- `photo_organizer/cli.py`: argument parsing + main processing loop
- `photo_organizer/organizer.py`: constructs the destination path and performs the file transfer
- `photo_organizer/duplicates.py`: resolves name conflicts at the destination

## Goals / Non-Goals

**Goals:**

- Provide a user-facing mode switch (copy vs move) while keeping the default as copy.
- Keep behavior consistent with existing flags:
  - `--dry-run` must remain non-destructive (no file transfers, no deletes).
  - `--on-duplicate` strategies must continue to apply to the destination path.
- Preserve metadata to the same extent as today.

**Non-Goals:**

- No new configuration files or interactive prompts.
- No attempt to make operations transactional/atomic across an entire run.
- No checksum-based deduplication changes.

## Decisions

1. **CLI surface: add `--mode` with choices `copy|move` (default: `copy`).**
   - Rationale: mirrors existing patterns (`--on-duplicate` uses choices) and keeps UX explicit.
   - Alternative: separate `--move` boolean flag. Rejected because it scales poorly if more modes are added.

2. **Implement mode as a small enum-like type, following the project’s existing pattern (`DuplicateStrategy`).**
   - Rationale: keeps valid values centralized and avoids stringly-typed branching.
   - Alternative: keep as raw strings from argparse. Rejected to reduce typo risk and to align with existing style.

3. **Use `shutil.move` for move mode, `shutil.copy2` for copy mode.**
   - Rationale: `shutil.move` handles same-filesystem renames efficiently and performs copy+delete across filesystems.
   - Alternative: `copy2` + explicit `unlink`. Rejected for now to avoid duplicating edge-case handling already present in `shutil.move`.

## Risks / Trade-offs

- **Move mode is destructive** → Mitigation: default remains copy; `--dry-run` must never delete.
- **Cross-filesystem moves may be slower** (copy+delete) → Mitigation: documented via help text; behavior is expected.
- **Failure during move** could leave the source or destination in a partial state → Mitigation: rely on `shutil.move` semantics; log errors and return failure for that file.
