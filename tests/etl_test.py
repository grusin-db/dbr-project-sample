"""Test the sample ETL transformation."""

from dbrdemo.etl import get_big_taxi_trips


def test_taxis() -> None:
    """Verify that the sample query returns the expected rows.

    Returns:
        None.
    """
    df = get_big_taxi_trips()
    data = df.collect()

    assert len(data) == 7
