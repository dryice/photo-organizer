import pytest
from pathlib import Path
from photo_organizer.cli import parse_args


def test_parse_args_required():
    args = parse_args(["--source", "/input", "--output", "/output"])
    assert args.source == Path("/input")
    assert args.output == Path("/output")


def test_parse_args_defaults():
    args = parse_args(["--source", "/input", "--output", "/output"])
    assert args.dry_run is False
    assert args.on_duplicate == "rename"
    assert args.log_level == "INFO"
    assert args.mode == "copy"


@pytest.mark.parametrize("mode", ["copy", "move"])
def test_parse_args_mode(mode):
    args = parse_args(["--source", "/input", "--output", "/output", "--mode", mode])
    assert args.mode == mode


def test_parse_args_dry_run():
    args = parse_args(["--source", "/input", "--output", "/output", "--dry-run"])
    assert args.dry_run is True


def test_parse_args_duplicate_strategy():
    args = parse_args(
        ["--source", "/input", "--output", "/output", "--on-duplicate", "skip"]
    )
    assert args.on_duplicate == "skip"
