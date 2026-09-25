"""Expose the package version and lazily initialized Databricks helpers."""

from databricks.labs.blueprint.logger import install_logger

install_logger()

import logging
from typing import Any

logging.getLogger().setLevel(level=logging.CRITICAL)
logger = logging.getLogger('dbrdemo')
logger.setLevel(logging.DEBUG)

from .foobar import create_foobar, write_foobar
from .session import get_dbutils, get_spark
from .version import __version__

logger.info(f"Using dbrdemo version: {__version__}")


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
