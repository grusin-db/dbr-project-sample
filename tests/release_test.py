"""Test release wheel publishing."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from dbrdemo import release
from dbrdemo.release import find_wheel, normalize_volume_path, upload_wheel_to_volume


@pytest.mark.parametrize(
    ("volume", "expected"),
    [
        ("catalog.schema.packages", "/Volumes/catalog/schema/packages"),
        ("/Volumes/catalog/schema/packages/", "/Volumes/catalog/schema/packages"),
    ],
)
def test_normalize_volume_path(volume: str, expected: str) -> None:
    """Verify supported volume formats.

    Args:
        volume: Input volume name or path.
        expected: Expected normalized path.

    Returns:
        None.
    """
    assert normalize_volume_path(volume) == expected


def test_find_wheel(tmp_path: Path) -> None:
    """Verify that the built wheel is selected.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    wheel = tmp_path / "dbrdemo-0.1.0-py3-none-any.whl"
    wheel.touch()

    assert find_wheel(tmp_path) == wheel


@pytest.mark.parametrize(
    ("environment", "overwrite"),
    [
        ("dev", True),
        ("test", False),
        ("acc", False),
        ("prod", False),
    ],
)
def test_upload_wheel_to_volume(tmp_path: Path, environment: str, overwrite: bool) -> None:
    """Verify wheel upload through the Databricks Files API.

    Args:
        tmp_path: Temporary directory provided by pytest.
        environment: Release environment under test.
        overwrite: Expected Files API overwrite setting.

    Returns:
        None.
    """
    wheel = tmp_path / "dbrdemo-0.1.0-py3-none-any.whl"
    wheel.write_bytes(b"wheel")
    workspace_client = MagicMock()

    target = upload_wheel_to_volume(
        "catalog.schema.packages",
        wheel,
        environment,
        workspace_client,
    )

    assert target == "/Volumes/catalog/schema/packages/dbrdemo-0.1.0-py3-none-any.whl"
    workspace_client.files.upload.assert_called_once()
    assert workspace_client.files.upload.call_args.args[0] == target
    assert workspace_client.files.upload.call_args.kwargs == {"overwrite": overwrite}


def test_main_prints_notebook_install_commands(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    """Verify that upload output includes notebook installation commands.

    Args:
        monkeypatch: Pytest fixture for replacing release functions.
        capsys: Pytest fixture for capturing terminal output.
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    wheel = tmp_path / "dbrdemo-0.2.0-py3-none-any.whl"
    target = f"/Volumes/main/packages/prod/{wheel.name}"

    def fake_find_wheel(dist_dir: Path) -> Path:
        assert dist_dir == tmp_path
        return wheel

    def fake_upload_wheel_to_volume(volume: str, wheel_file: Path, environment: str) -> str:
        assert (volume, wheel_file, environment) == ("main.packages.prod", wheel, "prod")
        return target

    monkeypatch.setattr(release, "find_wheel", fake_find_wheel)
    monkeypatch.setattr(release, "upload_wheel_to_volume", fake_upload_wheel_to_volume)

    release.main(["--env", "prod", "--volume", "main.packages.prod", "--dist-dir", str(tmp_path)])

    assert capsys.readouterr().out == (
        f"Uploaded wheel: {target}\n"
        "\nInstall in a Databricks notebook:\n"
        f"%pip install -q {target}\n"
        "dbutils.library.restartPython()\n"
    )
