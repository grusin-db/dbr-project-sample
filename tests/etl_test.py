from dbrdemo.etl import get_big_taxi_trips
from dbrdemo.test_utils import smart_verify

def test_taxis():
    df = get_big_taxi_trips()
    data = df.collect()

    assert len(data) == 7

def test_taxis_data():
    df = get_big_taxi_trips()

    smart_verify(df)



