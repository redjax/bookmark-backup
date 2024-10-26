import logging
from pathlib import Path

log = logging.getLogger(__name__)

from bookmark_backup.core import setup, detect_env
from bookmark_backup import finder
from bookmark_backup.domain.Bookmarks import (
    BookmarksFile,
    VivaldiBookmarksFile,
    ChromeBookmarksFile,
    EdgeBookmarksFile,
)


def main():
    vivaldi_bookmarks = VivaldiBookmarksFile()
    chrome_bookmarks = ChromeBookmarksFile()
    edge_bookmarks = EdgeBookmarksFile()

    log.debug(
        f"Vivaldi bookmarks file: {vivaldi_bookmarks.bookmarks_file}, exists: {vivaldi_bookmarks.bookmarks_file_exists}"
    )
    log.debug(
        f"Chrome bookmarks file: {chrome_bookmarks.bookmarks_file}, exists: {chrome_bookmarks.bookmarks_file_exists}"
    )
    log.debug(
        f"Edge bookmarks file: {edge_bookmarks.bookmarks_file}, exists: {edge_bookmarks.bookmarks_file_exists}"
    )

    vivaldi_bookmarks.backup_bookmarks_file(backup_dest="./vivaldi_bookmarks.json")


if __name__ == "__main__":
    setup.setup_logging(level="DEBUG")
    main()
