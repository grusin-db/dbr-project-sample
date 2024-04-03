import pytest


def test_pytest():
    print("test is ok?")
    assert True


def test_exception():
    with pytest.raises(Exception):
        1 / 0
