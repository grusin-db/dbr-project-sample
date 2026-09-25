"""Verify the pytest setup."""

import pytest


def test_pytest() -> None:
    """Verify that pytest executes tests.

    Returns:
        None.
    """
    assert True


def test_exception() -> None:
    """Verify that pytest detects an expected exception.

    Returns:
        None.
    """
    with pytest.raises(ZeroDivisionError):
        1 / 0
