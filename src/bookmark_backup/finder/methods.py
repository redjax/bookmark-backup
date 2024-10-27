from __future__ import annotations

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

from bookmark_backup.core.constants import supported_browsers, supported_os_types
from bookmark_backup.core.validators import validate_browser, validate_os_type

CWD: Path = Path(__file__).parent
BOOKMARKS_FILE_PATH_JSON: Path = CWD / "bookmarks_file_paths.json"


def load_bookmarks_filepaths() -> dict:
    log.debug(f"Opening '{BOOKMARKS_FILE_PATH_JSON}'")
    with open(BOOKMARKS_FILE_PATH_JSON, "r") as f:
        data = f.read()

        _dict = json.loads(data)

    return _dict


def get_browser_bookmarks_filepath(os_type: str, browser: str) -> str:
    os_type = validate_os_type(os_type)
    browser = validate_browser(browser)

    bookmarks_filepaths = load_bookmarks_filepaths()

    bookmarks_file_path = Path(bookmarks_filepaths[os_type][browser]["bookmarks_file"])
    if "~" in str(bookmarks_file_path):
        bookmarks_file_path = bookmarks_file_path.expanduser()

    return str(bookmarks_file_path)
