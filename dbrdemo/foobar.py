"""Create the sample foo/bar DataFrame."""

from pyspark.sql import DataFrame

from .session import get_spark


def create_foobar(foo: str, bar: str) -> DataFrame:
    """Create a one-row DataFrame containing foo and bar values.

    Args:
        foo: Value for the ``foo`` column.
        bar: Value for the ``bar`` column.

    Returns:
        A DataFrame with ``foo`` and ``bar`` string columns.
    """
    return get_spark().createDataFrame([(foo, bar)], "foo string, bar string")


def write_foobar(table_name: str, foo: str, bar: str) -> None:
    """Append one foo/bar row to a Databricks table.

    Args:
        table_name: Three-level table name in ``catalog.schema.table`` format.
        foo: Value for the ``foo`` column.
        bar: Value for the ``bar`` column.

    Returns:
        None.
    """
    create_foobar(foo, bar).write.mode("append").saveAsTable(table_name)
