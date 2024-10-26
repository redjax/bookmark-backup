import logging
import argparse
import sys

log = logging.getLogger(__name__)

from bookmark_backup.core.validators import validate_browser, validate_os_type
from bookmark_backup.core import detect_env
from bookmark_backup import finder
from bookmark_backup.domain.Bookmarks import (
    BookmarksFile,
    EdgeBookmarksFile,
    ChromeBookmarksFile,
    VivaldiBookmarksFile,
)


def backup(browser: str, dest: str, overwrite: bool):
    # Backup functionality (not yet implemented)
    match browser:
        case "vivaldi":
            bookmarks = VivaldiBookmarksFile()
        case "chrome":
            bookmarks = ChromeBookmarksFile()
        case "edge":
            bookmarks = EdgeBookmarksFile()
        case _:
            raise ValueError(f"Invalid browser: {browser}.")

    print(
        f"Backing up [{browser}] bookmarks to destination: {dest} (overwrite: {overwrite})"
    )

    try:
        bookmarks.backup_bookmarks_file(backup_dest=dest, overwrite=overwrite)
        print(f"Saved [{browser}] bookmarks to file: {dest}")

        return True
    except FileExistsError as file_exists:
        print(
            f"[WARNING] Backup destination '{dest}' already exists, and overwrite=False. Did not copy bookmarks file."
        )
        sys.exit(1)
    except PermissionError as perm_err:
        print(
            f"[ERROR] Permission denied copying [{browser}] bookmarks file to path: {dest}. Details: {perm_err}"
        )
        sys.exit(1)
    except Exception as exc:
        msg = f"({type(exc)}) Error backing up [{browser}] bookmarks. Details: {exc}"
        log.error(msg)

        raise exc


def restore(browser: str):
    # Raise NotImplementedError as restore is not yet implemented
    raise NotImplementedError("The restore functionality is not implemented yet.")


def check_inputs(browser: str):
    browser = validate_browser(browser)
    os_type: str = validate_os_type(os_type=detect_env.os_type())


def main(log_level: str = "CRITICAL"):
    logging.basicConfig(
        level=log_level.upper(),
        format="%(asctime)s | [%(levelname)s] | (%(name)s) > %(module)s.%(funcName)s:%(lineno)s|> %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    logging.getLogger("bookmarks_backup").setLevel("NOTSET")
    logging.getLogger("Bookmarks").setLevel("NOTSET")

    parser = argparse.ArgumentParser(description="Browser bookmarks management CLI.")
    parser.add_argument(
        "--browser", type=str, required=True, help="Specify the browser name."
    )

    # Define subparsers for the 'backup' and 'restore' commands
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # 'backup' command
    backup_parser = subparsers.add_parser("backup", help="Backup browser bookmarks")
    backup_parser.add_argument(
        "--dest", type=str, required=True, help="Destination path for the backup"
    )
    backup_parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite existing backup",
    )

    # 'restore' command
    restore_parser = subparsers.add_parser("restore", help="Restore browser bookmarks")
    # No additional arguments for restore

    args = parser.parse_args()

    check_inputs(browser=args.browser)

    # Route to the appropriate function based on the command
    if args.command == "backup":
        backup(browser=args.browser, dest=args.dest, overwrite=args.overwrite)
    elif args.command == "restore":
        restore(browser=args.browser)
    else:
        print("Unknown command")
        sys.exit(1)


if __name__ == "__main__":
    main()
