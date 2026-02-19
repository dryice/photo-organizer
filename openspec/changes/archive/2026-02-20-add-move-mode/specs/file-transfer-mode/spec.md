## ADDED Requirements

### Requirement: User can select file transfer mode

The system SHALL allow the user to choose whether organizing a file performs a copy (preserving the source file) or a move (removing the source file after a successful transfer).

#### Scenario: Default mode is copy
- **WHEN** the user does not specify a transfer mode
- **THEN** the system copies files into the output directory

#### Scenario: Explicit copy mode
- **WHEN** the user specifies copy mode
- **THEN** the system copies files into the output directory
- **AND** the source file remains at its original location

#### Scenario: Explicit move mode
- **WHEN** the user specifies move mode
- **THEN** the system moves files into the output directory
- **AND** the source file no longer exists at its original location after a successful move

### Requirement: Dry run does not modify the filesystem

When dry run is enabled, the system SHALL not create or modify output files and SHALL not remove or modify source files regardless of transfer mode.

#### Scenario: Dry run with copy mode
- **WHEN** the user runs with dry run enabled in copy mode
- **THEN** the system reports the planned copy operations
- **AND** no files are copied
- **AND** the source files remain unchanged

#### Scenario: Dry run with move mode
- **WHEN** the user runs with dry run enabled in move mode
- **THEN** the system reports the planned move operations
- **AND** no files are moved
- **AND** the source files remain unchanged
