# This file will hold all the cli commands and args

import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI tool for organizing files in a directory"
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="The directory to be organized",
    )
    parser.add_argument(
        "--by",
        "-b",
        choices=["type", "date", "size", "name"],
        default="type",
        help="Organization strategy",
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Preview changes without moving files",
    )

    if Path(parser.directory).is_dir():
        print("Directory exists")
    else:
        print("Directory does not exist")

    return parser.parse_args()



