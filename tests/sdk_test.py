"""Test Databricks SDK access with serverless Spark fixtures."""

import io

from databricks.sdk import WorkspaceClient

from dbrdemo import get_spark


def test_workspace_client(ws: WorkspaceClient) -> None:
    """Verify access to the current Databricks user.

    Args:
        ws: Authenticated workspace client provided by the shared fixture.

    Returns:
        None.
    """
    assert ws.current_user.me()


def test_get_catalogs(ws: WorkspaceClient) -> None:
    """Verify access to Unity Catalog.

    Args:
        ws: Authenticated workspace client provided by the shared fixture.

    Returns:
        None.
    """
    assert ws.catalogs.list()


def test_upload_file_to_volume(
    ws: WorkspaceClient,
    temporary_schema: tuple[str, str],
) -> None:
    """Verify file upload and download through a temporary volume.

    Args:
        ws: Authenticated workspace client provided by the shared fixture.
        temporary_schema: Catalog and temporary schema created through Spark.

    Returns:
        None.
    """
    catalog, schema = temporary_schema
    volume = "files"
    qualified_volume = f"`{catalog.replace('`', '``')}`.`{schema}`.`{volume}`"
    get_spark().sql(f"CREATE VOLUME {qualified_volume}")

    file_path = f"/Volumes/{catalog}/{schema}/{volume}/test3.yaml"

    ws.files.upload(file_path, io.BytesIO(b"some: initial text data 2222"), overwrite=True)

    contents = ws.files.download(file_path).contents
    assert contents is not None
    downloaded = contents.read()
    assert downloaded == b"some: initial text data 2222"
