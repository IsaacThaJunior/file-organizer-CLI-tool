from pathlib import Path


class FileOrganizer:
    def __init__(self, directory: Path, dry_run: bool):
        self.directory = directory
        self.dry_run = dry_run

    def scan(self) -> list[Path]:
        # Gets all items in the directory
        # filters to only files
        # returns the list of file paths in the directory
        files = [p for p in self.directory.iterdir() if p.is_file()]
        return files

    def analyze(self):
        # First, we call the scan method to get the list of files
        # The we get each file extension
        # The we get each file size
        # The we get each file creation date
        # Then file category?

        pass
