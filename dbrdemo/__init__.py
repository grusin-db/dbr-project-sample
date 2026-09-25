"""Expose the package version and lazily initialized Databricks helpers."""

import logging
from typing import Any

from databricks.labs.blueprint.logger import install_logger as _install_logger

from .foobar import create_foobar, write_foobar
from .session import get_dbutils, get_spark
from .version import __version__

logger = logging.getLogger(__name__)


def install_logger() -> None:
    """Install focused logging for dbrdemo.

    Returns:
        None.
    """
    _install_logger()
    logging.getLogger().setLevel(logging.CRITICAL)
    logger.setLevel(logging.DEBUG)
    logger.info("Using dbrdemo version: %s", __version__)


def __getattr__(name: str) -> Any:
    """Expose the Spark session and dbutils without connecting during import.

    Args:
        name: Attribute being accessed on the module.

    Returns:
        The Spark session for ``spark`` or the dbutils object for ``dbutils``.
    """
    if name == "spark":
        return get_spark()
    if name == "dbutils":
        return get_dbutils()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
