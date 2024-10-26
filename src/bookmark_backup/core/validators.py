import logging
from pathlib import Path

from .constants import supported_browsers, supported_os_types


def validate_os_type(os_type: str) -> str:
    os_type = os_type.lower()
    valid_os_types = supported_os_types()

    if os_type in ["mac", "darwin", "macos", "mac os x"]:
        os_type = "mac"

    if not os_type in valid_os_types:
        raise ValueError(f"Invalid OS type: {os_type}. Must be one of {valid_os_types}")

    return os_type


def validate_browser(browser: str) -> str:
    browser = browser.lower()
    valid_browsers = supported_browsers()

    if browser not in valid_browsers:
        raise ValueError(
            f"Unsupported browser: {browser}. Must be one of {valid_browsers}"
        )

    return browser
