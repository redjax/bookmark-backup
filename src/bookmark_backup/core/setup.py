from __future__ import annotations

import logging

log = logging.getLogger(__name__)


def setup_logging(
    level: str = "INFO",
    fmt: str = "%(asctime)s | [%(levelname)s] | (%(name)s) > %(module)s.%(funcName)s:%(lineno)s |> %(message)s",
    datefmt: str = "%Y-%m-%dT%H:%M:%S",
    silence_loggers: list[str] = [],
):
    logging.basicConfig(level=level.upper(), format=fmt, datefmt=datefmt)

    if silence_loggers:
        for logger in silence_loggers:
            logging.getLogger(logger).setLevel("WARNING")
