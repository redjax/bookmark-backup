from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
import logging
from pathlib import Path
import shutil
import typing as t

log: logging.Logger = logging.getLogger(__name__)

from bookmark_backup import finder
from bookmark_backup.core import detect_env
from bookmark_backup.core.validators import validate_browser, validate_os_type

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ValidationError,
    computed_field,
    ConfigDict,
    model_validator,
)


class BookmarksFileBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    browser: str = Field(default=None)

    @computed_field
    @property
    def os_type(self) -> str:
        os_type: str = validate_os_type(os_type=detect_env.os_type())

        return os_type

    @computed_field
    @property
    def bookmarks_file(self) -> str:
        bookmarks_file = finder.get_browser_bookmarks_filepath(
            os_type=self.os_type, browser=self.browser
        ).title()

        return bookmarks_file

    @property
    def bookmarks_file_exists(self) -> bool:
        if self.bookmarks_file is None:
            return False
        _path = Path(self.bookmarks_file).expanduser()
        return _path.exists()

    @contextmanager
    def _safe_copy(self, dest: t.Union[str, Path], overwrite: bool = False):
        if not self.bookmarks_file_exists:
            raise FileNotFoundError(
                f"Could not find bookmarks file: {self.bookmarks_file}"
            )

        src_path = Path(self.bookmarks_file)
        dest_path = Path(dest).expanduser()

        if dest_path.exists() and not overwrite:
            raise FileExistsError(
                f"File '{dest_path}' already exists. Skipping file copy."
            )
        elif not dest_path.parent.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(src_path, dest_path)
            yield
        except PermissionError as exc:
            raise PermissionError(f"Permission denied: {exc}")
        except Exception as exc:
            raise Exception(f"Error copying file '{src_path}' to '{dest_path}': {exc}")

    def backup_bookmarks_file(
        self, backup_dest: t.Union[str, Path], overwrite: bool = False
    ):
        backup_dest = Path(backup_dest).expanduser()
        try:
            with self._safe_copy(dest=backup_dest, overwrite=overwrite):
                print(f"Successfully backed up to '{backup_dest}'.")
            return True
        except Exception as exc:
            print(f"Backup failed: {exc}")
            return False

    def restore_bookmarks_file(self, backup_src: str):
        backup_src = Path(backup_src).expanduser()
        if not backup_src.exists():
            raise FileNotFoundError(f"Could not find backup source file: {backup_src}")

        bookmarks_bak = f"{self.bookmarks_file}.bak"
        if self.bookmarks_file_exists:
            with self._safe_copy(dest=bookmarks_bak, overwrite=True):
                print(f"Backup of current bookmarks created at '{bookmarks_bak}'.")

        if self.bookmarks_file_exists:
            Path(self.bookmarks_file).unlink(missing_ok=True)

        shutil.copy2(src=backup_src, dst=self.bookmarks_file)


class VivaldiBookmarksFile(BookmarksFileBase):
    browser: str = Field(default="vivaldi", init=False)


class ChromeBookmarksFile(BookmarksFileBase):
    browser: str = Field(default="chrome", init=False)


class EdgeBookmarksFile(BookmarksFileBase):
    browser: str = Field(default="edge", init=False)
