from __future__ import annotations

import logging
import os
from pathlib import Path
import platform

log = logging.getLogger(__name__)


def os_type() -> str:
    """Detect environment's OS type.

    Returns:
        (str): "Windows", "Mac", or "Linux".

    """
    return platform.system()


def os_release() -> str | None:
    """Get the OS release name or version.

    Returns:
        (str): The OS release name or version.

    """
    os_name = os_type()

    os_release_dict = {"os": os_name, "release": None}

    if os_name == "Linux":
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME"):
                        os_release_dict = {
                            "os": os_name,
                            "release": line.split("=", 1)[1].strip().strip('"'),
                        }
                        # return line.split("=", 1)[1].strip().strip('"')
        except FileNotFoundError:
            try:
                with open("/proc/version") as f:
                    os_release_dict = {"os": os_name, "release": f.read().strip()}
                    # return f.read().strip()
            except FileNotFoundError:
                os_release_dict = {"os": os_name, "release": "unknown"}
    elif os_name == "Darwin":
        os_release_dict = {"os": os_name, "release": f"macOS {platform.mac_ver()[0]}"}
    elif os_name == "Windows":
        # return f"Windows {platform.win32_ver()[0]}"
        os_release_dict = {"os": os_name, "release": platform.win32_ver()[0]}
    else:
        log.warning(f"Unknown OS: {os_name}")
        os_release_dict = {"os": os_name, "release": "unknown"}

    return os_release_dict


def is_docker() -> bool:
    """Detect if environment is a Docker container.

    Description:
        Checks for the presence of a /proc/self/cgroup path.
        If the path exists, read the file and return True if
        the word 'docker' is found on a line.

    Returns:
        (bool): `True` if 'docker' line is found in file, else False.

    """
    if not Path("/proc/self/cgroup").exists():
        return False

    with open("/proc/self/cgroup", "r") as procfile:
        for line in procfile:
            fields: list[str] = line.strip().split("/")

            if fields[1] == "docker":
                return True

    return False


def is_wsl() -> bool:
    """Detect if the environment is running in Windows Subsystem for Linux (WSL).

    Returns:
        (bool): `True` if running in WSL, else False.

    """
    if os_type() == "Linux":
        try:
            with open("/proc/version", "r") as version_file:
                version_info = version_file.read()

                if "Microsoft" in version_info or "WSL" in version_info:
                    return True
        except FileNotFoundError:
            return False
    return False


def chrome_bookmarks_path(os_type: str = os_type(), os_release: str = os_release()):
    match os_type:
        case "Windows":
            local_appdata = Path(os.getenv("LOCALAPPDATA"))
            bookmarks_path = (
                local_appdata / "Google" / "Chrome" / "Default" / "Bookmarks"
            )

            return bookmarks_path
        case "Linux":
            ...
        case "Mac":
            ...
        case _:
            log.warning(f"Unsupported OS type: {os_type}")

            return None
