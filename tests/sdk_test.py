import io

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat


def test_workspace_client():
    w = WorkspaceClient()
    assert w.current_user.me()


def test_get_catalogs():
    w = WorkspaceClient()
    c = w.catalogs.list()
    assert c


def test_upload_yaml_config_file():
    w = WorkspaceClient()

    f = io.StringIO("some: initial text data")

    w.workspace.upload(path='/Shared/test3.yaml', content=f, format=ImportFormat.AUTO, overwrite=True)
