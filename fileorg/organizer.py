from pathlib import Path
from collections import defaultdict
import json
from datetime import datetime


class FileOrganizer:
    def __init__(self, directory: Path, dry_run: bool, undo: bool):
        self.directory = directory
        self.dry_run = dry_run
        self.undo_file_log = []
        self.undo = undo

    def call_funcs(self):
        if self.dry_run:
            self.display_summary()
            return

        if self.undo:
            self._handle_undo()
            return

        self.display_summary()
        response = input("Are you ready to organize the files? (y/n): ")
        if response.lower() == "y" or response.lower() == "yes":
            self.organize()
            print("✓ Files have been organized")
        else:
            print("✗ Files organization cancelled")

    def organize(self):
        """
        Organize the files in the directory. Create folders and then move filees into them
        """

        # Create folders from categories
        file_result = self.analyze()
        count = 0
        for category in file_result["categories_found"]:
            print(category)
            # check if the category already exists. If yes then we dont create it
            if Path(self.directory / category).is_dir():
                print(f"Folder: {category} already exists")
                print("We will just move files into them")
                continue
            Path(self.directory / category).mkdir(exist_ok=True)

        # Move files to folders
        # print("Moving files to folders")
        for category, files in file_result["Files"].items():
            for file in files:
                try:
                    # Move the file
                    count += 1
                    print(f"Moving {file['name']} to {category}")
                    print(
                        f"Moved {count} {'file' if count == 1 else 'files'} out of {file_result['total_files']}"
                    )
                    source = Path(file["path"])
                    destination = Path(self.directory / category / file["name"])

                    source.replace(destination)
                    self._move_files_log(source, destination, category)
                except Exception as e:
                    print(f"Error: {e}")

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

        return {
            "total_files": len(scanned_files),
            "total_size": self._human_readable_size(size_in_bytes),
            "Files": dict(grouped_files),
            "categories_found": list(grouped_files.keys()),
        }

    def display_summary(self):
        """
        Display a clean summary of file analysis. When dry_run is True

        """
        # Get analysis data
        details = self.analyze()

        # Show header

        print("=" * 50)
        print("📋 DRY RUN MODE - NO FILES WILL BE MOVED")
        print("=" * 50)

        # Show overall statistics
        print("\n📊 Overall Statistics:")
        print(f"   • Total files: {details['total_files']}")
        print(f"   • Total size: {details['total_size']}")
        print(f"   • Categories found: {len(details['categories_found'])}")

        # Show breakdown by category
        print("\n📂 Breakdown by Category:")
        print("-" * 40)

        # Get files grouped by category
        files_by_category = details.get("Files", {})

        for category, file_list in files_by_category.items():
            # Calculate total size for this category
            print(f"\n{category.upper()}:")
            print(f"  Count: {len(file_list)} files")

            # Show file details if verbose mode

            print("Files:")
            for file_info in file_list[:10]:  # Show first 10 files
                print(f"    • {file_info['name']} ({file_info['size']})")

            # If more than 10 files, show count
            if len(file_list) > 10:
                print(f"    • ... and {len(file_list) - 10} more files")

        # Show what will happen next

        print("\n" + "=" * 50)
        print("💡 DRY RUN COMPLETE")
        print("To actually organize files, run without --dry-run flag")
        print("=" * 50)

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

    def _move_files_log(self, source, destination, category):
        self.undo_file_log.append(
            {
                "source": str(source),
                "destination": str(destination),
                "Original Exists": source.exists(),
                "Folder moved to": category,
            }
        )

        undo_data = {
            "timestamp": datetime.now().isoformat(),
            "directory": str(self.directory),
            "operations": self.undo_file_log,
        }

        undo_file = Path.cwd() / "logs" / "undo.json"
        print(undo_file)
        # Create the directory if it doesn't exist
        undo_file.parent.mkdir(exist_ok=True, parents=True)

        with open(undo_file, "w") as f:
            json.dump(undo_data, f, indent=4)

    def _handle_undo(self):
        # 1) Check if undo log exists
        undo_file = Path.cwd() / "logs" / "undo.json"
        if not undo_file.exists():
            print("No undo logs found.")
            return

        # 2) Load undo data
        with open(undo_file, "r") as f:
            undo_data = json.load(f)

        # 3) Verify the undo is for the current directory
        if undo_data["directory"] != str(self.directory):
            print("No action has been taken in this directory to warrant undoing!")
            return

        folders_to_delete = set()
        moved_files_count = 0

        # 4) Move files back
        for operation in undo_data["operations"]:
            source = Path(operation["destination"])
            destination = Path(operation["source"])
            folder_name = operation.get("Folder moved to")

            # Track folders for later deletion
            if folder_name:
                folders_to_delete.add(folder_name)

            try:
                # Move file back to original location (overwrites if needed)
                if source.exists():
                    source.replace(destination)
                    moved_files_count += 1

                # If the file did not exist originally, remove it
                else:
                    print(f"Warning: {source} does not exist, skipping.")
            except Exception as e:
                print(f"Error moving {source} back to {destination}: {e}")


        # 5) Remove folders (only if empty)
        for folder in folders_to_delete:
            folder_path = Path(self.directory / folder)
            if folder_path.exists():
                try:
                    # Only remove if empty
                    if not any(folder_path.iterdir()):
                        folder_path.rmdir()
                except Exception as e:
                    print(f"Error removing folder {folder_path}: {e}")

        print(f"✓ Undo complete: {moved_files_count} files moved back")
