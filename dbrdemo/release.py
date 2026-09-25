"""Publish built wheels to a Unity Catalog volume."""

import argparse
from collections.abc import Sequence
from pathlib import Path

from databricks.sdk import WorkspaceClient

SUPPORTED_ENVIRONMENTS = ("dev", "test", "acc", "prod")


def normalize_volume_path(volume: str) -> str:
    """Normalize a Unity Catalog volume name or path.

    Args:
        volume: Volume as ``catalog.schema.volume`` or ``/Volumes/...``.

    Returns:
        The normalized path without a trailing slash.
    """
    value = volume.strip().rstrip("/")
    if value.startswith("/Volumes/"):
        return value

    parts = value.split(".")
    if len(parts) != 3 or any(not part for part in parts):
        raise ValueError("VOLUME must be catalog.schema.volume or /Volumes/catalog/schema/volume")
    return f"/Volumes/{'/'.join(parts)}"


def find_wheel(dist_dir: Path) -> Path:
    """Find the single wheel in a distribution directory.

    Args:
        dist_dir: Directory containing the built wheel.

    Returns:
        The wheel path.
    """
    wheels = sorted(dist_dir.glob("*.whl"))
    if len(wheels) != 1:
        raise ValueError(f"Expected one wheel in {dist_dir}, found {len(wheels)}")
    return wheels[0]


def upload_wheel_to_volume(
    volume: str,
    wheel_file: Path,
    environment: str,
    workspace_client: WorkspaceClient | None = None,
) -> str:
    """Upload a wheel to a Unity Catalog volume.

    Args:
        volume: Volume as ``catalog.schema.volume`` or ``/Volumes/...``.
        wheel_file: Local wheel path.
        environment: Release environment controlling overwrite protection.
        workspace_client: Optional authenticated workspace client.

    Returns:
        The uploaded workspace file path.
    """
    target = f"{normalize_volume_path(volume)}/{wheel_file.name}"
    client = workspace_client or WorkspaceClient()
    with wheel_file.open("rb") as contents:
        client.files.upload(target, contents, overwrite=environment == "dev")
    return target


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Optional command-line argument sequence.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Upload the built dbrdemo wheel to a Unity Catalog volume")
    parser.add_argument("--volume", required=True)
    parser.add_argument("--env", choices=SUPPORTED_ENVIRONMENTS, required=True)
    parser.add_argument("--dist-dir", default="dist", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """Upload the built wheel from command-line arguments.

    Args:
        argv: Optional command-line argument sequence.

    Returns:
        None.
    """
    args = parse_args(argv)
    target = upload_wheel_to_volume(args.volume, find_wheel(args.dist_dir), args.env)
    print(f"Uploaded wheel: {target}")
    print("\nInstall in a Databricks notebook:")
    print(f"%pip install -q {target}")
    print("dbutils.library.restartPython()")


if __name__ == "__main__":
    main()
