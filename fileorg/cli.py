# This file will hold all the cli commands and args

import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI tool for organizing files in a directory"
    )
    parser.add_argument(
        "directory",
        type=validate_path,
        help="The directory to be organized",
    )
    parser.add_argument(
        "--undo",
        "-u",
        action="store_true",
        help="Allows you to undo the last action done by the program",
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Preview changes without moving files",
    )

    return parser.parse_args()


def validate_path(path_string) -> Path:
    path = Path(path_string)
    if path_string.startswith("~"):
        path = path.expanduser()

    if not path.exists:
        raise argparse.ArgumentTypeError(f"directory '{path_string}' does not exist")

    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"{path_string} is not a directory")
    return path
