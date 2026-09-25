"""Test the sample foo/bar functionality."""

from dbrdemo import create_foobar, get_spark, write_foobar


def test_create_foobar() -> None:
    """Verify that foo and bar values are exposed as DataFrame columns.

    Returns:
        None.
    """
    row = create_foobar("hello", "world").first()
    assert row is not None

    assert row.asDict() == {"foo": "hello", "bar": "world"}


def test_write_foobar(temporary_schema: tuple[str, str]) -> None:
    """Verify that a foo/bar row is appended to a Databricks table.

    Args:
        temporary_schema: Catalog and temporary schema created through Spark.

    Returns:
        None.
    """
    catalog, schema = temporary_schema
    table_name = f"`{catalog.replace('`', '``')}`.`{schema}`.`foobar`"

    write_foobar(table_name, "hello", "world")

    row = get_spark().table(table_name).first()
    assert row is not None
    assert row.asDict() == {"foo": "hello", "bar": "world"}
