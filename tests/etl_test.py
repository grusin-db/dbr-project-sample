from dbrdemo import spark
from dbrdemo.etl import get_big_taxi_trips

def test_taxis():
    data = get_big_taxi_trips()
    
    assert len(data) == 7