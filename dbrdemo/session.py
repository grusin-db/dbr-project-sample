"""Manage lazy Spark and dbutils sessions.

- Reuse the active Spark session on Databricks compute.
- Create a Databricks Connect session locally.
- Cache both objects after first use.
"""

import logging

from databricks.sdk import WorkspaceClient
from databricks.sdk.dbutils import RemoteDbUtils
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)

_spark: SparkSession | None = None
_dbutils: RemoteDbUtils | None = None


def get_spark() -> SparkSession:
    """Return the cached Spark session, creating it on first use.

    Returns:
        The active Spark session, or a new Databricks Connect session.
    """
    global _spark
    if _spark is None:
        _spark = _create_spark()
    return _spark


def get_dbutils() -> RemoteDbUtils:
    """Return the cached dbutils, creating it on first use.

    Returns:
        The dbutils object from a ``WorkspaceClient``.
    """
    global _dbutils
    if _dbutils is None:
        _dbutils = WorkspaceClient().dbutils
    return _dbutils


def _create_spark() -> SparkSession:
    """Reuse the active Spark session, or build one via Databricks Connect.

    Returns:
        A configured Spark session.
    """
    spark = SparkSession.getActiveSession()

    if spark is None:
        logger.debug("No active session; connecting via Databricks Connect...")
        # databricks.connect is only installed locally, not on a cluster.
        from databricks.connect import DatabricksSession

        spark = DatabricksSession.builder.getOrCreate()

    # Set any project-wide Spark configs here, e.g.:
    # spark.conf.set("spark.sql.session.timeZone", "UTC")

    return spark
