import logging
import os
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass

log = logging.getLogger(__name__)


class Finder:
    def __init__(self, path: str):
        """Initialize the DirectoryController with a directory path."""
        self.path = Path(path)
        self.files: List[Path] = []
        self.dirs: List[Path] = []

        self.logger = log.getChild("Finder")

    def __enter__(self):
        self.crawl_directory()

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_val:
            self.logger.error(f"({exc_type}): {exc_val}")

            return False

        return True

    def crawl_directory(self) -> None:
        """Recursively crawl the directory and populate files and dirs lists."""
        if not self.path.is_dir():
            raise ValueError(f"{self.path} is not a valid directory.")

        for entry in os.scandir(self.path):
            entry_path = Path(entry.path)

            if entry.is_dir():
                self.dirs.append(entry_path)
                # Recursively crawl into subdirectories
                sub_controller = Finder(entry_path)
                sub_controller.crawl_directory()
                self.files.extend(sub_controller.files)
                self.dirs.extend(sub_controller.dirs)
            elif entry.is_file():
                self.files.append(entry_path)

    def search_in_names(self, text: str) -> Tuple[List[Path], List[Path]]:
        """Search for the specified text in file and directory names.

        Args:
            text (str): The text to search for in names.

        Returns:
            Tuple[List[Path], List[Path]]: Lists of matching files and directories.
        """
        matched_files = [file for file in self.files if text in file.name]
        matched_dirs = [dir for dir in self.dirs if text in dir.name]

        return matched_files, matched_dirs


# Example usage
if __name__ == "__main__":
    directory_path = "/path/to/your/directory"  # Replace with your directory path
    controller = Finder(directory_path)

    # Crawl the directory
    controller.crawl_directory()

    # Print all files and directories
    print("Files:")
    for file in controller.files:
        print(file)

    print("\nDirectories:")
    for dir in controller.dirs:
        print(dir)

    # Search for a text in file/directory names
    search_text = "example"  # Replace with your search text
    matched_files, matched_dirs = controller.search_in_names(search_text)

    print(f"\nMatched Files for '{search_text}':")
    for file in matched_files:
        print(file)

    print(f"\nMatched Directories for '{search_text}':")
    for dir in matched_dirs:
        print(dir)
