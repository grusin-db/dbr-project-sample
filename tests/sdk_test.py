"""Test Databricks SDK access with pytester fixtures."""

import io
from collections.abc import Callable

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import VolumeInfo


def test_workspace_client(ws: WorkspaceClient) -> None:
    """Verify access to the current Databricks user.

    Args:
        ws: Authenticated workspace client provided by pytester.

    Returns:
        None.
    """
    assert ws.current_user.me()


def test_get_catalogs(ws: WorkspaceClient) -> None:
    """Verify access to Unity Catalog.

    Args:
        ws: Authenticated workspace client provided by pytester.

    Returns:
        None.
    """
    assert ws.catalogs.list()


def test_upload_file_to_volume(
    ws: WorkspaceClient,
    make_volume: Callable[[], VolumeInfo],
) -> None:
    """Verify file upload and download through a temporary volume.

    Args:
        ws: Authenticated workspace client provided by pytester.
        make_volume: Fixture that creates and cleans up a temporary volume.

    Returns:
        None.
    """
    volume = make_volume()
    file_path = f"/Volumes/{volume.catalog_name}/{volume.schema_name}/{volume.name}/test3.yaml"

    ws.files.upload(file_path, io.BytesIO(b"some: initial text data 2222"), overwrite=True)

    downloaded = ws.files.download(file_path).contents.read()
    assert downloaded == b"some: initial text data 2222"
