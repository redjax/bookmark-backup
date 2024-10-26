import logging

log = logging.getLogger(__name__)

from bookmark_backup.cli import cli_main


def main(log_level: str = "INFO"):
    log_level = log_level.upper()
    cli_main.main(log_level=log_level)


if __name__ == "__main__":
    log_level = "NOTSET"

    main(log_level=log_level)
