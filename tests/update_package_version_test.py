"""Test environment-specific package version updates."""

from pathlib import Path

import pytest

from update_package_version import build_package_version, update_package_version


@pytest.mark.parametrize(
    ("environment", "expected"),
    [
        ("dev", "0.1.0.dev0+2026.09.25.7.abc123"),
        ("test", "0.1.0b0+2026.09.25.7.abc123"),
        ("acc", "0.1.0rc0+2026.09.25.7.abc123"),
        ("prod", "0.1.0"),
    ],
)
def test_build_package_version(environment: str, expected: str) -> None:
    """Verify each supported environment version.

    Args:
        environment: Release environment under test.
        expected: Expected PEP 440 version.

    Returns:
        None.
    """
    actual = build_package_version(
        current_version="0.1.0rc0+previous",
        environment=environment,
        date_str="2026.09.25",
        daily_build_number=7,
        commit="ABC123",
    )

    assert actual == expected


def test_update_package_version(tmp_path: Path) -> None:
    """Verify package and distribution version files are updated.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    version_file = tmp_path / "version.py"
    dist_version_file = tmp_path / ".dist_version"
    version_file.write_text("__version__ = '2.3.4'\n", encoding="utf-8")

    result = update_package_version(
        environment="test",
        daily_build_number=9,
        date_str="2026.09.25",
        commit="def456",
        version_file=version_file,
        dist_version_file=dist_version_file,
    )

    assert result == "2.3.4b0+2026.09.25.9.def456"
    assert version_file.read_text(encoding="utf-8") == "__version__ = '2.3.4b0+2026.09.25.9.def456'\n"
    assert dist_version_file.read_text(encoding="utf-8") == "2.3.4b0+2026.09.25.9.def456\n"
