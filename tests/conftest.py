"""Configure shared Databricks test fixtures."""

from collections.abc import Callable, Iterator

import pytest
from databricks.sdk import WorkspaceClient

from dbrdemo import get_spark, install_logger

install_logger()


@pytest.fixture
def ws() -> WorkspaceClient:
    """Create a workspace client from the configured Databricks profile.

    Returns:
        An authenticated workspace client.
    """
    return WorkspaceClient()


@pytest.fixture
def temporary_schema(make_random: Callable[[int], str]) -> Iterator[tuple[str, str]]:
    """Create a temporary schema through the selected Spark compute.

    Args:
        make_random: Pytester fixture that creates a random name.

    Yields:
        The catalog and temporary schema names.
    """
    spark = get_spark()
    row = spark.sql("SELECT current_catalog()").first()
    assert row is not None

    catalog = str(row[0])
    schema = f"dbrdemo_test_{make_random(8).lower()}"
    qualified_schema = f"`{catalog.replace('`', '``')}`.`{schema}`"

    spark.sql(f"CREATE SCHEMA {qualified_schema}")
    try:
        yield catalog, schema
    finally:
        spark.sql(f"DROP SCHEMA IF EXISTS {qualified_schema} CASCADE")
