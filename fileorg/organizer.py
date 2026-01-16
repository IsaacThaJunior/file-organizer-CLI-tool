from pathlib import Path
from collections import defaultdict


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
        scanned_files = self.scan()
        grouped_files = defaultdict(list)
        size_in_bytes = 0
        for file in scanned_files:
            # Then we get each file extension
            file_extension = file.suffix.lower()

            # Then we get each file size
            file_size = file.stat().st_size
            size_in_bytes += file_size

            # Then we group the files by category
            category = self._get_category(file_extension)
            file_info = {
                "name": file.name,
                "size": self._human_readable_size(file_size),
                "extension": file_extension,
                "category": category,
                "path": file.as_posix(),
            }
            grouped_files[category].append(file_info)

        print(
            {
                "total_files": len(scanned_files),
                "total_size": self._human_readable_size(size_in_bytes),
                "Files": dict(grouped_files),
                "categories_found": list(grouped_files.keys()),
            }
        )

    def _get_category(self, extension: str) -> str:
        FILE_CATEGORIES = {
            "Images": [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".svg",
                ".webp",
                ".tiff",
            ],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt"],
            "Archives": [".zip", ".tar", ".gz", ".7z", ".rar", ".bz2"],
            "Code": [
                ".py",
                ".js",
                ".html",
                ".css",
                ".json",
                ".xml",
                ".java",
                ".cpp",
                ".c",
            ],
            "Audio": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"],
            "Video": [".mp4", ".avi", ".mov", ".mkv", ".webm", ".wmv"],
            "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
            "Presentations": [".ppt", ".pptx", ".odp"],
            "Executables": [".exe", ".app", ".sh", ".bat", ".msi", ".dmg"],
            "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
            "Databases": [".db", ".sqlite", ".sql"],
        }

        for category, extensions in FILE_CATEGORIES.items():
            if extension in extensions:
                return category
        return "Other"

    def _human_readable_size(self, size_bytes: int) -> str:
        """Convert bytes to human-readable format."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
