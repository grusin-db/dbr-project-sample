"""Test the sample foo/bar functionality."""

from collections.abc import Callable

from databricks.sdk.service.catalog import TableInfo

from dbrdemo import create_foobar, get_spark, write_foobar


def test_create_foobar() -> None:
    """Verify that foo and bar values are exposed as DataFrame columns.

    Returns:
        None.
    """
    row = create_foobar("hello", "world").first()

    assert row.asDict() == {"foo": "hello", "bar": "world"}


def test_write_foobar(make_table: Callable[..., TableInfo]) -> None:
    """Verify that a foo/bar row is appended to a Databricks table.

    Args:
        make_table: Fixture that creates and cleans up a temporary table.

    Returns:
        None.
    """
    table = make_table(columns=[("foo", "STRING"), ("bar", "STRING")])
    assert table.full_name

    write_foobar(table.full_name, "hello", "world")

    row = get_spark().table(table.full_name).first()
    assert row.asDict() == {"foo": "hello", "bar": "world"}
