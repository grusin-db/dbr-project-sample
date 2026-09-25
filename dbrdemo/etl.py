"""Sample ETL logic run through Databricks Connect."""

from pyspark.sql import DataFrame

from . import spark


def get_big_taxi_trips() -> DataFrame:
    """Return NYC taxi trips with a fare above 100.

    Returns:
        A Spark DataFrame of rows from ``samples.nyctaxi.trips`` where
        ``fare_amount > 100``.
    """
    return spark.table('samples.nyctaxi.trips').filter('fare_amount > 100')
