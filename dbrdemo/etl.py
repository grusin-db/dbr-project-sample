from . import spark


def get_big_taxi_trips():
    df = spark.table('samples.nyctaxi.trips') \
        .filter('fare_amount > 100')

    return df.collect()
