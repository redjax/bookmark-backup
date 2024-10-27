import logging
import typing as t
from pathlib import Path
from dataclasses import field, dataclass
from contextlib import contextmanager
import shutil

log: logging.Logger = logging.getLogger(__name__)

from bookmark_backup.core.validators import validate_browser, validate_os_type
from bookmark_backup.core import detect_env
from bookmark_backup import finder


@dataclass
class BookmarksFile:
    browser: str = field(init=False)

    def __post_init__(self):
        self.os_type: str = validate_os_type(os_type=detect_env.os_type())
        self.browser: str = validate_browser(browser=self.browser)
        self.bookmarks_file: str = finder.get_browser_bookmarks_filepath(
            os_type=self.os_type, browser=self.browser
        ).title()

    @property
    def bookmarks_file_exists(self) -> bool:
        if self.bookmarks_file is None:
            return False

        _path = Path(self.bookmarks_file)
        if "~" in str(_path):
            _path: Path = _path.expanduser()

        return _path.exists()

    @contextmanager
    def _safe_copy(self, dest: t.Union[str, Path], overwrite: bool = False):
        if self.bookmarks_file is None:
            raise ValueError("bookmarks_file should not be None.")
        if not self.bookmarks_file_exists:
            raise FileNotFoundError(
                f"Could not find bookmarks file: {self.bookmarks_file}"
            )

        src_path = Path(self.bookmarks_file)
        dest_path = Path(str(dest))
        if "~" in str(dest_path):
            dest_path = dest_path.expanduser()

        if dest_path.exists():
            if not overwrite:
                # yield
                raise FileExistsError(
                    f"File '{dest_path}' already exists. Skipping file copy."
                )
            else:
                log.warning(
                    f"Destination exists: {dest_path}. overwrite=True, continuing anyway."
                )

        if not dest_path.parent.exists():
            try:
                dest_path.mkdir(parents=True, exist_ok=True)
            except FileNotFoundError as fnf:
                log.warning(f"Could not find file '{dest_path}'.")
                yield
            except PermissionError as perm_err:
                log.error(
                    f"Permission denied copying file '{src_path}' to '{dest_path}'. Details: {exc}"
                )
                raise perm_err
            except Exception as exc:
                msg = (
                    f"({type(exc)}) Error creation destination directory '{dest_path}'"
                )
                log.error(msg)

                raise exc

        log.info(f"Copying file '{src_path}' to destination '{dest_path}'")
        try:
            shutil.copy2(src_path, dest_path)

            yield
        except PermissionError as perm_exc:
            log.error(
                f"Permission denied copying file '{src_path}' to destination '{dest_path}'. Details: {perm_exc}"
            )
            raise
        except Exception as exc:
            msg = f"({type(exc)}) An error occurred while copying file '{src_path}' to '{dest_path}'. Details: {exc}"
            log.error(msg)

            raise

    def backup_bookmarks_file(
        self, backup_dest: t.Union[str, Path], overwrite: bool = False
    ):
        if backup_dest is None:
            raise ValueError(f"Must pass a destination path as backup_dest.")

        backup_dest = (
            Path(str(backup_dest)).expanduser()
            if "~" in str(backup_dest)
            else Path(str(backup_dest))
        )

        try:
            with self._safe_copy(dest=backup_dest, overwrite=overwrite):
                log.info(
                    f"Successfully copied bookmarks file '{self.bookmarks_file}' to destination path '{backup_dest}'."
                )

            return True
        except PermissionError as perm_err:
            # log.error("Permission denied copying bookmarks file.")
            raise perm_err
        except FileExistsError as file_exists:
            raise file_exists
        except Exception as exc:
            msg = f"({type(exc)}) Failed copying bookmarks file."
            # log.error(msg)

            raise exc

    def restore_bookmarks_file(self, backup_src: str):
        if backup_src is None:
            raise ValueError(f"Must pass a destination path as backup_dest.")

        backup_src = (
            Path(str(backup_src)).expanduser()
            if "~" in str(backup_src)
            else Path(str(backup_src))
        )

        if not Path(str(backup_src)).exists:
            raise FileNotFoundError(f"Could not find backup source file: {backup_src}")

        bookmarks_bak = f"{self.bookmarks_file}.bak"

        if self.bookmarks_file_exists:
            print(f"Backing up existing [{self.browser}] bookmarks to .bak file.")
            ## Copy existing file to .bak
            try:
                with self._safe_copy(dest=bookmarks_bak, overwrite=True):
                    log.info(
                        f"Successfully copied bookmarks file '{self.bookmarks_file}' to destination path '{bookmarks_bak}'."
                    )

            except PermissionError as perm_err:
                # log.error("Permission denied copying bookmarks file.")
                raise perm_err
            except FileExistsError as file_exists:
                raise file_exists
            except Exception as exc:
                msg = f"({type(exc)}) Failed copying bookmarks file."
                # log.error(msg)

                raise exc

        print(f"Restoring [{self.browser}] bookmarks from file: {backup_src}")
        ## Overwrite existing file
        if self.bookmarks_file_exists:
            try:
                Path(str(self.bookmarks_file)).unlink()
            except Exception as exc:
                msg = f"({type(exc)}) Error removing existing bookmarks file '{self.bookmarks_file}'. Details: {exc}"
                log.error(msg)

                raise exc

        print(f"Copying bookmarks from file '{backup_src}' to '{self.bookmarks_file}'")
        try:
            shutil.copy2(src=backup_src, dst=self.bookmarks_file)
        except Exception as exc:
            msg = f"({type(exc)}) Error restoring bookmarks from backup file '{backup_src}'. Details: {exc}"
            log.error(msg)

            raise exc


@dataclass
class VivaldiBookmarksFile(BookmarksFile):
    def __post_init__(self) -> None:
        self.browser: str = "vivaldi"

        super().__post_init__()


@dataclass
class ChromeBookmarksFile(BookmarksFile):
    def __post_init__(self) -> None:
        self.browser: str = "chrome"

        super().__post_init__()


@dataclass
class EdgeBookmarksFile(BookmarksFile):
    def __post_init__(self) -> None:
        self.browser: str = "edge"

        super().__post_init__()
